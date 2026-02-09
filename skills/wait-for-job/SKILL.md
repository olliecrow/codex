---
name: wait-for-job
description: Wait for long-running external tasks to finish before continuing work. Use when Codex must block on cluster jobs, batch pipelines, CI runs, or other asynchronous operations by polling status every N seconds (default 120) and proceeding only after completion, with a hard timeout cap of 8 hours.
---

# Wait For Job

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

Block until an external task is complete, then continue with downstream analysis or execution. Use the bundled poller to avoid racing ahead while jobs are still running.

## Workflow

1. Define completion and failure signals.
- Choose completion mode:
  - Exit-code mode: command exits `0` only when the task is complete.
  - Regex mode: command output matches a completion regex.
- Define optional failure regexes (`Failed`, `Error`, `Cancelled`) for hard-stop conditions.
2. Run the poller with explicit limits.
- Keep `--interval-seconds` at `120` unless the user asks for different polling cadence.
- Use `--timeout-seconds` with an upper bound of `28800` (8 hours). The script enforces this cap and defaults to `28800`.
3. Continue only on success.
- Exit code `0`: proceed with the next requested step.
- Non-zero exit: stop and report the reason; do not continue silently.

## Cluster defaults (Slurm)

- For Slurm job waits, filter polling to the current project/user scope whenever that context is available.
- If project cluster env is required, prefer loading it explicitly (for example via `CLUSTER_ENV_FILE=\"$PWD/.env\"`).
- If `.env` is missing, attempt high-confidence reconstruction from project conventions first; if confidence is low, fail fast and ask.
- If waits expose clearly lingering/stuck jobs, hand off to cluster triage/cancellation workflow before resuming normal execution.

## Quick Start

### Exit-code mode

Use when status command can return `0` only once complete.

```bash
python "/path/to/wait-for-job/scripts/poll_until_done.py" \
  --check-cmd "test -f /tmp/job.done" \
  --interval-seconds 120
```

### Regex mode (cluster-style polling)

Use when status command always exits `0` but output changes over time.

```bash
python "/path/to/wait-for-job/scripts/poll_until_done.py" \
  --check-cmd "kubectl get job my-job -n my-namespace -o jsonpath='{.status.conditions[*].type}'" \
  --success-regex "Complete" \
  --failure-regex "Failed" \
  --interval-seconds 120
```

## Script

Use `scripts/poll_until_done.py`.

Arguments:
- `--check-cmd`: shell command to evaluate each poll.
- `--success-regex`: optional regex that marks completion from command output.
- `--failure-regex`: optional repeatable regex for terminal failure output.
- `--interval-seconds`: polling interval (default `120`).
- `--timeout-seconds`: wall-clock timeout in seconds, required range `1..28800` (default `28800`).
- `--max-attempts`: max polling attempts (`0` disables cap).
- `--retry-on-nonzero`: in regex mode, continue polling when command exits non-zero.
- `--quiet`: print only terminal outcome messages.

Exit codes:
- `0`: task completed.
- `1`: timeout or max attempts reached.
- `2`: failure condition detected or fatal command error.
- `130`: interrupted.

## Agent Rules

- Wait for poller completion before doing downstream steps.
- Report the exact check command and completion signal used.
- Ask for clarification only when completion signal cannot be inferred.
