---
name: cluster-check
description: Check and deeply analyze recent cluster jobs for the current project and cluster user, sync artifacts, extract learnings, apply high-confidence fixes, and submit clear follow-up experiments when warranted.
---

# cluster-check

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

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
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Investigate the latest cluster activity for the current project and cluster user end-to-end: queue state, recent jobs, logs, outputs, sync integrity, failures, and experiment learnings. This skill is Slurm-only.

Use the findings to either:
- apply high-confidence code/config fixes immediately, and/or
- design and submit clear follow-up experiments that maximize learning.

Prioritize maximizing learning and experiment throughput efficiency. If no clear follow-up experiments or fixes are justified, say so explicitly.

## When to use

Use this skill when the user asks to:
- check in on cluster jobs,
- analyze completed experiment batches,
- triage logs/errors/issues from cluster runs,
- sync cluster outputs back to local,
- decide what to run next and submit jobs,
- turn cluster learnings into code/config improvements.

Do not use this skill for non-Slurm schedulers.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm the expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- Prioritize project/user isolation: only inspect and act on jobs relevant to the current project and cluster user.
- Always cancel lingering/stuck jobs for the current project/user and perform safe remote cleanup for their artifacts.
- Never cancel, modify, or clean up jobs/files that belong to other users or unrelated project prefixes.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- For transient cluster connectivity failures (SSH timeouts, banner/host-key issues, temporary Slurm RPC errors), run bounded retry + reconnect attempts before declaring a hard blocker.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Scope and identity (must establish first)

Determine and record:
- `project_root`: current repo root.
- `project_name`: infer from repo basename (for example `gigaplay` or `mercantile`).
- `cluster_user`: prefer environment/user config, fallback to `ollie` only when no stronger source is available.
- `job_prefix`: project-specific prefix from env/config/scripts when available.
- `ssh_host`: cluster host alias from env/config/scripts.

Use the most specific available source in this order:
1. Project cluster env loader (for example `tools/cluster/env.sh`).
2. `.env` values in the project root.
3. Existing project cluster scripts that expose host/user/prefix.
4. Explicit user instruction.
5. Conservative default (`cluster_user=ollie`) when unambiguous.

If `.env` is missing:
- Attempt high-confidence reconstruction from `.env.example`, project cluster scripts, and existing project conventions.
- If reconstruction confidence is not high, try additional local evidence (`ssh` config aliases, recent job artifacts/logs, wrapper defaults, and conservative read-only probes) before asking the user for only the minimal missing detail.

## Workflow

### 1) Preflight and project wiring

- Confirm `pwd`, repo root, and current branch.
- Detect cluster tooling and choose the best interface:
  - `tools/cluster/*.sh` (preferred when present),
  - `scripts/cluster/*.sh` and `scripts/cluster/*.py`,
  - raw `ssh + squeue/sacct/scontrol` fallback.
- If a cluster env loader exists, load it with explicit env-file context when needed (for example `CLUSTER_ENV_FILE="$PWD/.env"`).
- Validate required commands (`ssh`, `squeue`/`sacct` availability via remote if local tools are absent, `rg`, `python`/`uv` as needed).
- If connectivity checks fail transiently, retry with short backoff and then continue preflight once connectivity is restored.
- Enforce Slurm scope. If Slurm tooling cannot be reached and no project Slurm wrapper works, stop and report the blocker.

### 2) Build a recent job inventory

Collect both live and recent history for the current project/user.

- Live queue:
  - running/pending states with IDs, names, runtime, reason/node, and array details when present.
- Recent history:
  - `sacct` for recent jobs (state, exit code, elapsed, start/end, resources), filtered to project-relevant names/prefixes.
- Batch segmentation:
  - identify the most recent batch(es) by shared prefix/search id/time window.
  - prefer the batch currently being discussed in this conversation when identifiable.
  - otherwise use the most recent run/completed batch on the cluster.

### 3) Cancel lingering/stuck jobs and clean up

- Detect lingering/stuck jobs for current project/user (for example stale pending, hung runtime, failed dependencies).
- Cancel them automatically when confidence is high they are stale or non-progressing.
- Perform safe remote cleanup for canceled/failed partial artifacts belonging to current project/user only.
- Record what was canceled and cleaned, with reasons.

### 4) Sync and reconcile artifacts

- Sync cluster outputs relevant to the identified recent batch back to local.
- Use project-provided sync scripts when available (for example `fetch_runs`, `resync_results`, `sync_repo` flows).
- Reconcile remote vs local:
  - missing locally,
  - stale locally,
  - failed/partial remote outputs,
- manifest inconsistencies.
- Confirm local paths for each batch before analysis.

### 5) Deep investigation of logs and outputs

For each recent batch/job (prioritize failed/slow/anomalous jobs first):

- Extract scheduler diagnostics:
  - state transitions,
  - exit codes,
  - runtime vs requested limits,
  - allocation/resources.
- Inspect logs:
  - stdout/stderr tails and targeted grep for `Traceback`, `ERROR`, `Exception`, OOM, timeout, cancellation, container/env failures.
- Inspect produced outputs:
  - run directories, metrics files, summaries, checkpoints/manifests.
- Verify lifecycle completeness:
  - run execution,
  - aggregation,
  - cleanup/finalization,
  - post-run sync integrity.
- Classify each issue by root-cause bucket:
  - env/config wiring,
  - resource mismatch,
  - scheduler dependency/array behavior,
  - code/runtime exception,
  - data/path/sync corruption.

### 6) Extract learnings and decision signals

Convert raw evidence into decision-quality findings:

- What worked reliably.
- What failed and why.
- Throughput/cost/resource insights (CPU vs GPU, concurrency, runtime bottlenecks).
- Quality/performance insights from experiment results.
- Changes that will most improve reliability and learning velocity next.

Prioritize high-confidence, high-leverage findings.

### 7) Apply high-confidence fixes when justified

If a fix is clearly justified by evidence and scoped to current project work:
- implement it immediately,
- run relevant checks/tests,
- record rationale in a durable place (code comments/tests/docs).
- Keep code/config changes limited to the current project/repo only.

Do not apply speculative fixes. If confidence is low, document and defer.

### 8) Autonomously submit follow-up experiments

If clear follow-up experiments are warranted:
- define hypotheses and expected learning outcome,
- choose minimal, representative experiment set,
- configure resources/concurrency explicitly,
- submit jobs using project-native tooling when confidence is high,
- record submitted job IDs and what each job is testing.
- default to autonomous submission when confidence is high.
- if submission confidence is not high, ask before submitting.

If no clear follow-up experiments are justified, state that explicitly and do not submit more jobs.

### 9) Report (required)

Always report with these sections in order:
1. Findings summary.
2. Scope and identity (project, cluster user, prefix, host).
3. Recent batch inventory (running/completed/failed/cancelled).
4. Logs and errors analysis (root causes + evidence).
5. Output/sync integrity status.
6. Learnings and decisions.
7. Fixes applied (or why none).
8. Follow-up experiments submitted (or explicit no-submit decision).
9. Durable findings updated in docs.
10. Coverage gaps and unknowns.
11. Evidence runbook (commands/artifacts).

## Strong defaults and practical heuristics

- Prefer project-provided cluster wrappers/scripts before raw ad-hoc shell pipelines.
- When shell quoting becomes brittle, switch to small Python helpers for parsing.
- For long-running checks, poll at practical intervals (for example 60-180s) and avoid noisy loops.
- Use `wait-for-job` when the task explicitly requires waiting for completion before next analysis.
- Keep job filtering strict (`project + user + prefix`) to avoid cross-project contamination.
- Optimize for learning throughput: favor high-information experiments and avoid low-yield reruns.

## Common failure patterns to check first

- Missing or wrong env wiring (`.env`, `CLUSTER_ENV_FILE`, host/user/prefix unset).
- Local shell lacks `squeue/sacct` (must execute remotely or via project wrappers).
- SSH/auth/connectivity timeouts.
- Fragile shell quoting in nested `ssh` commands.
- Branch/worktree drift causing wrong code version on cluster.
- Sync gaps between remote results and local runs directories.

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
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- Persist short-term investigation details in `plan/` and promote durable findings/learnings to `docs/`.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Repeat invocations

- Continue from prior run artifacts and notes; avoid redoing settled analysis.
- Focus on new cluster events, newly completed jobs, and unresolved failures.
- If no meaningful new evidence exists, report that further investigation would be low-yield until new jobs complete or new inputs are provided.
