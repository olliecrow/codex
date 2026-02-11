---
name: wait-for-job
description: Wait for long-running external tasks to finish before continuing work. Use when Codex must block on cluster jobs, batch pipelines, CI runs, or other asynchronous operations by polling status every N seconds (default 120) and proceeding only after completion, with a hard timeout cap of 8 hours.
---

# Wait For Job

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: immediately take the next highest-value in-scope action when it is clear.
- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material risk tradeoffs, missing required data/access, or destructive/irreversible actions outside policy.
- Drive work to complete outcomes with verification, not partial handoffs.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes. Example loops (adapt as needed, not rigid): issue-resolution `investigate -> plan -> fix -> verify -> battletest -> organise-docs -> git-commit -> re-review`; cleanup `scan -> prioritize -> clean -> verify -> re-scan`; docs `audit -> update -> verify -> re-audit`.
- Keep looping until actual completion criteria are met: no actionable in-scope items remain, verification is green, and confidence is high.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

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
