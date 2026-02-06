#!/usr/bin/env python3
"""Poll a shell command until completion or failure."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Pattern

FATAL_EXIT_CODES = {126, 127}
MAX_TIMEOUT_SECONDS = 8 * 60 * 60


def _positive_int(value: str) -> int:
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("value must be > 0")
    return parsed_value


def _non_negative_int(value: str) -> int:
    parsed_value = int(value)
    if parsed_value < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")
    return parsed_value


def _bounded_timeout_seconds(value: str) -> int:
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("value must be > 0")
    if parsed_value > MAX_TIMEOUT_SECONDS:
        raise argparse.ArgumentTypeError(
            f"value must be <= {MAX_TIMEOUT_SECONDS} (8 hours)"
        )
    return parsed_value


def _compile_regex(pattern: str, label: str) -> Pattern[str]:
    try:
        return re.compile(pattern)
    except re.error as error:
        raise ValueError(f"invalid {label}: {error}") from error


def _run_check_command(check_cmd: str) -> tuple[int, str]:
    completed = subprocess.run(
        ["/bin/sh", "-lc", check_cmd],
        capture_output=True,
        text=True,
        check=False,
    )
    output_parts = []
    if completed.stdout:
        output_parts.append(completed.stdout.strip())
    if completed.stderr:
        output_parts.append(completed.stderr.strip())
    combined_output = "\n".join(part for part in output_parts if part).strip()
    return completed.returncode, combined_output


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _compact_output(raw_output: str, limit: int = 300) -> str:
    normalized_output = " ".join(raw_output.split())
    if len(normalized_output) <= limit:
        return normalized_output
    return f"{normalized_output[:limit]}..."


def _print_attempt(
    attempt: int,
    exit_code: int,
    status: str,
    output: str,
    quiet: bool,
) -> None:
    if quiet:
        return
    print(
        f"[{_utc_timestamp()}] attempt={attempt} exit_code={exit_code} status={status}",
        flush=True,
    )
    if output:
        print(f"  output={_compact_output(output)}", flush=True)


def _timed_out(start_time: float, timeout_seconds: int) -> bool:
    return time.monotonic() - start_time >= timeout_seconds


def _matches_any(patterns: list[Pattern[str]], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Poll a command until completion. "
            "Default interval is 120 seconds."
        )
    )
    parser.add_argument(
        "--check-cmd",
        required=True,
        help="Shell command used to check task status",
    )
    parser.add_argument(
        "--success-regex",
        help=(
            "Regex that marks completion based on command output. "
            "If omitted, completion is exit code 0."
        ),
    )
    parser.add_argument(
        "--failure-regex",
        action="append",
        default=[],
        help="Regex that marks terminal failure based on command output (repeatable)",
    )
    parser.add_argument(
        "--interval-seconds",
        type=_positive_int,
        default=120,
        help="Polling interval in seconds (default: 120)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=_bounded_timeout_seconds,
        default=MAX_TIMEOUT_SECONDS,
        help=(
            "Timeout in seconds. Must be <= 28800 (8 hours). "
            "Default: 28800."
        ),
    )
    parser.add_argument(
        "--max-attempts",
        type=_non_negative_int,
        default=0,
        help="Maximum polling attempts. Use 0 for unlimited attempts (default: 0)",
    )
    parser.add_argument(
        "--retry-on-nonzero",
        action="store_true",
        help=(
            "In regex mode, continue polling when the check command exits non-zero "
            "instead of failing immediately."
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only terminal outcome messages",
    )
    return parser


def run_poll_loop(args: argparse.Namespace) -> int:
    success_pattern: Pattern[str] | None = None
    if args.success_regex:
        success_pattern = _compile_regex(args.success_regex, "--success-regex")

    failure_patterns = [
        _compile_regex(pattern, "--failure-regex")
        for pattern in args.failure_regex
    ]

    start_time = time.monotonic()
    attempt = 0

    while True:
        attempt += 1
        exit_code, output = _run_check_command(args.check_cmd)

        if output and _matches_any(failure_patterns, output):
            _print_attempt(
                attempt=attempt,
                exit_code=exit_code,
                status="failure_pattern_matched",
                output=output,
                quiet=args.quiet,
            )
            print("terminal failure pattern detected", flush=True)
            return 2

        if success_pattern is None:
            if exit_code == 0:
                _print_attempt(
                    attempt=attempt,
                    exit_code=exit_code,
                    status="completed",
                    output=output,
                    quiet=args.quiet,
                )
                print("task completed", flush=True)
                return 0
            if exit_code in FATAL_EXIT_CODES:
                _print_attempt(
                    attempt=attempt,
                    exit_code=exit_code,
                    status="fatal_command_error",
                    output=output,
                    quiet=args.quiet,
                )
                print(
                    f"fatal check command error (exit code {exit_code})",
                    flush=True,
                )
                return 2
            _print_attempt(
                attempt=attempt,
                exit_code=exit_code,
                status="pending",
                output=output,
                quiet=args.quiet,
            )
        else:
            if output and success_pattern.search(output):
                _print_attempt(
                    attempt=attempt,
                    exit_code=exit_code,
                    status="completed",
                    output=output,
                    quiet=args.quiet,
                )
                print("task completed", flush=True)
                return 0
            if exit_code != 0 and not args.retry_on_nonzero:
                terminal_state = (
                    "fatal_command_error"
                    if exit_code in FATAL_EXIT_CODES
                    else "nonzero_exit_in_regex_mode"
                )
                _print_attempt(
                    attempt=attempt,
                    exit_code=exit_code,
                    status=terminal_state,
                    output=output,
                    quiet=args.quiet,
                )
                print(
                    "check command exited non-zero in regex mode; "
                    "use --retry-on-nonzero to keep polling",
                    flush=True,
                )
                return 2
            _print_attempt(
                attempt=attempt,
                exit_code=exit_code,
                status="pending",
                output=output,
                quiet=args.quiet,
            )

        if args.max_attempts and attempt >= args.max_attempts:
            print("max attempts reached", flush=True)
            return 1
        if _timed_out(start_time, args.timeout_seconds):
            print("timeout reached", flush=True)
            return 1

        time.sleep(args.interval_seconds)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        return run_poll_loop(args)
    except ValueError as error:
        parser.error(str(error))
    except KeyboardInterrupt:
        print("interrupted", flush=True)
        return 130
    return 2


if __name__ == "__main__":
    sys.exit(main())
