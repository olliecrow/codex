---
name: cluster-monitor
description: Patiently monitor long-running Slurm cluster jobs with intermittent polling, low-noise log/output checks, and conservative intervention. Use when jobs run for hours/days and Codex should mostly wait, detect systemic failure patterns, intervene only when learning value collapses (for example high repeated OOM rates in sweeps), then clean up, fix, resubmit, and continue monitoring until completion and immediate post-run analysis.
---

# cluster-monitor

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

Monitor cluster jobs with patience and minimal intervention. Focus on protecting experiment learning value, not forcing every single job to succeed. Queue waiting is usually acceptable; systemic run failure is not.

## Proactive autonomy and knowledge compounding

- Be proactive: immediately take the next highest-value in-scope action when it is clear.
- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material risk tradeoffs, missing required data/access, or destructive/irreversible actions outside policy.
- If blocked by command/tool/env failures, attempt high-confidence fallbacks autonomously before escalating (for example `rg` -> `find`/`grep`, `python` -> `python3`, alternate repo-native scripts).
- When the workflow uses `plan/`, ensure required plan directories exist before reading/writing them (create when edits are allowed; otherwise use an in-memory fallback and call it out).
- Treat transient external failures (network/SSH/remote APIs/timeouts) as retryable by default: run bounded retries with backoff and capture failure evidence before concluding blocked.
- On repeated invocations for the same objective, resume from prior findings/artifacts and prioritize net-new progress over rerunning identical work unless verification requires reruns.
- Drive work to complete outcomes with verification, not partial handoffs.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes. Example loops (adapt as needed, not rigid): issue-resolution `investigate -> plan -> fix -> verify -> battletest -> organise-docs -> git-commit -> re-review`; cleanup `scan -> prioritize -> clean -> verify -> re-scan`; docs `audit -> update -> verify -> re-audit`.
- Keep looping until actual completion criteria are met: no actionable in-scope items remain, verification is green, and confidence is high.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Never squash commits; always use merge commits when integrating branches.
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Monitoring posture (must follow)

- Be patient by default. Expect long waits and monitor intermittently.
- Do not intervene just because jobs are pending in queue with legitimate scheduler reasons.
- Accept that some failures are natural in sweeps (for example large sequence length + large batch size causing OOM).
- Intervene only when failure is systemic or projected learning value has collapsed.
- When intervention is required, intervene decisively: diagnose, kill scoped jobs, clean up aggressively, fix, resubmit, and continue monitoring.

## Scope and identity (must establish first)

Determine and record:
- `project_root`: current repo root.
- `project_name`: inferred from repo basename unless overridden by explicit user instruction.
- `cluster_user`: from env/config/project scripts, falling back only when high confidence.
- `job_prefix` or batch identifiers: from project scripts, submitted job IDs, or naming conventions.
- `cluster_host`: from project cluster wrappers/env/ssh config.

Always scope monitoring, cancellation, and cleanup to the current project and cluster user.

## Intervention thresholds (default policy)

Use these defaults unless user/project policy says otherwise:
- Expected failure watch band: up to `10%` failures in a sweep can be acceptable.
- Escalation band: `>10%` similar failures triggers deeper diagnosis and tighter monitoring.
- Intervention band: `>=15%` similar failures (OOM/timeouts/crashes) or strong evidence of low learning value triggers intervention workflow.

Interpret thresholds at batch/sweep level, not per single job.

Projected learning value gate (use with failure thresholds):
- Continue monitoring if expected remaining successful jobs will still produce meaningful coverage of the experiment space.
- Trigger intervention if projected informative coverage has clearly collapsed (for example most remaining jobs share the same fatal pattern and results will be low-yield).
- Prefer evidence-based projection from current state + config pattern, not guesswork.

Intervene earlier than thresholds only if any hard-stop condition appears:
- configuration bug affecting most jobs,
- invalid outputs (NaNs/empty artifacts/corrupt metrics) across the batch,
- deterministic crash pattern indicating the run cannot produce useful results.

Expected-failure policy:
- Treat isolated OOM/timeouts in aggressive sweep corners as expected unless they repeat systemically.
- Do not kill a batch for a few natural failures.
- When similar failures cross intervention band (`>=15%` by default), treat the batch as structurally misconfigured and intervene.

## Workflow

### 1) Preflight and monitoring contract

- Confirm `pwd`, repo root, branch, and required tools.
- Prefer project-native cluster wrappers/scripts; fall back to `ssh + squeue/sacct/scontrol` only when needed.
- Confirm what job group/batch is being monitored.
- Set expected failure posture explicitly: "allow some failures, intervene only when systemic."
- Choose the monitoring horizon (hours/day) and continue until completion or intervention decision.

### 2) Choose low-token waiting mechanism

Use either approach and prefer the lower-token option for the current context:
- direct intermittent monitoring loop (status + selective log/output checks), or
- `wait-for-job` for bounded quiet waits between checkpoints.

Prefer `wait-for-job` for long waits:
- Use its poller in regex mode with `--quiet`.
- Poll status summaries, not full logs, on each interval.
- Keep one wait cycle bounded to 8 hours, then resume with another cycle for day-long monitoring.

Cadence defaults:
- only pending jobs with legitimate reasons: poll every `600-900s`.
- active running jobs: poll every `180-300s`.
- degraded/suspect state: poll every `60-120s` until classified.

To minimize token/command noise:
- capture only state deltas and new failures since last poll,
- tail logs only for jobs with state changes or failure signals,
- avoid repeatedly printing unchanged queue tables.
- keep a compact running state snapshot (counts, ratios, new anomalies, current decision state) and update it in-place.

### 3) Intermittent health checks during run

At each poll:
- gather queue/sacct snapshot for scoped jobs,
- compute cumulative counts by state (`RUNNING`, `PENDING`, `COMPLETED`, `FAILED`, `CANCELLED`, `TIMEOUT`, `OOM`),
- inspect new error signals from stdout/stderr tails,
- inspect whether expected output artifacts/metrics are being produced.

Classify current batch health:
- `healthy`: failures within expected band and learning signal intact,
- `degraded`: failures rising or suspicious outputs, but still likely salvageable,
- `systemic`: high repeated failure or low expected learning value.

### 4) Intervention decision logic

Do not intervene when:
- queue delays are legitimate scheduler behavior,
- isolated failures are expected in exploratory sweeps,
- failure ratio remains below intervention band and successful runs still provide learning.

Intervene when:
- failure ratio reaches intervention band (`>=15%`) for similar root cause, or
- batch shows strong low-learning outcome (for example widespread invalid outputs), or
- repeated crashes indicate current configuration is fundamentally broken.

Do not intervene on uncertainty alone:
- if signals are mixed and learning value is still plausible, keep monitoring with tighter cadence until confidence increases.

### 5) Intervention workflow (when warranted)

1. Diagnose first:
- identify root cause and exact fix candidates,
- verify intervention is justified by evidence, not single-job noise,
- define the fix plan before canceling the batch.

2. Stop failing run cleanly:
- cancel the whole affected batch (scoped to project/user) when systemic failure is confirmed.

3. Clean up aggressively:
- remove partial/broken artifacts for canceled/failed jobs,
- reconcile remote/local outputs to avoid polluted downstream analysis.

4. Fix and verify:
- implement high-confidence fixes,
- run the smallest relevant checks/smoke run before full resubmission.

5. Resubmit and resume monitoring:
- submit updated jobs,
- record new job IDs and what changed,
- return to patient monitoring loop.

### 6) Completion workflow (required)

As soon as monitored jobs finish:
- sync all relevant outputs back to local,
- analyze outcomes deeply (metrics, anomalies, failure patterns, surprising behavior, expected-vs-actual outcomes),
- aggregate learnings across successful and failed jobs,
- extract what was learned from every experiment segment (including failed segments where informative),
- capture durable insights/decisions in docs,
- prepare next-step experiment framing only if the user asked for it.

## Reporting format (required)

Report in this order:
1. Scope and monitored batch/job IDs.
2. Monitoring timeline (poll cadence and key state transitions).
3. Failure distribution and threshold assessment.
4. Intervention decision (`no intervention`, `watch`, or `intervened`) with rationale.
5. If intervened: fixes applied, cleanup done, and resubmission IDs.
6. Completion status and synced artifact integrity.
7. Key learnings, anomalies, and confidence.
8. Evidence runbook (commands, logs, outputs inspected).

## Practical heuristics

- Optimize for learning throughput, not zero failures.
- Treat OOMs in aggressive hyperparameter corners as expected until they become systemic.
- Distinguish queue pain from run-quality pain; queue pain alone is not a reason to kill jobs.
- Prefer conservative intervention over trigger-happy cancellation.
- If systemic failure is clear, intervene quickly and thoroughly.
- Reuse `wait-for-job` rather than ad-hoc tight loops to reduce token/tool overhead.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you fix an issue, make a change that resolves an issue, or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your report, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing docs when they have a clear home, but create new focused docs/subdirectories when it improves navigability (and link them from related docs or indexes).
- Persist short-term monitoring notes in `plan/` and promote durable runbook guidance/learnings to `docs/`.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Repeat invocations

- Resume from existing monitored batch state; do not restart analysis from zero.
- Focus on new state transitions, new failures, and new outputs since last check.
- If no meaningful changes occurred, report "no material change" and keep waiting with the same or slower cadence.
