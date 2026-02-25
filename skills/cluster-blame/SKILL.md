---
name: cluster-blame
description: "Audit active or recent Slurm queue state to find likely job-shape misconfigurations that strand shared cluster capacity (CPU, memory, GPU) and block scheduling for others. Use when users ask why resources appear idle, who may be blocking allocation, which jobs/users look misconfigured, or when preparing evidence for neutral outreach. Keep the workflow strictly read-only: inspect and report only, never cancel, edit, reprioritize, or otherwise mutate jobs or cluster state."
---

# Cluster Blame

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

Inspect Slurm scheduler state and node packing to identify probable resource-stranding job submissions while avoiding false accusations.

Treat output as evidence-backed candidate attribution, not certainty: label findings by impact and confidence, separate policy effects from user-level misfit, and produce neutral follow-up language.

## Cross-skill principles integrated

- From `cluster-check`: default to quick-scan first for operational questions, return concrete units and timestamps, and make scope/identity explicit.
- From `cluster-monitor`: treat legitimate queue waiting (`Priority`, `Resources`, dependencies) as normal scheduler behavior until fit/fragmentation evidence shows avoidable stranding.
- From `investigate`: build explicit hypotheses, try to falsify attribution, and report coverage gaps and uncertainty instead of overstating certainty.
- From `summarize`: lead with high-impact findings and clearly separate facts, inferences, and unknowns.

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

## Quick-scan mode (must support)

When the user asks for a fast status answer (for example `who is blocking compute right now`), run quick-scan mode first.

Quick-scan mode requirements:
- Keep it read-only and fast; avoid deep history unless required.
- Prefer live scheduler evidence (`squeue`, `sinfo`, `scontrol show node`, `scontrol show job -d`, `sprio`).
- Return concrete timestamps and units (for example `CPU used/total`, `GPU used/total`, `mem used/total`).
- Distinguish `likely blocker`, `possible blocker`, and `policy-driven` explicitly.

## Trigger phrases

Use quick-scan mode for prompts like:
- `who is blocking resources right now`
- `why are gpus idle`
- `which users are stranding capacity`
- `check current cluster blockers`

Use deep-attribution mode for prompts like:
- `deeply research why resources are not fully allocated`
- `separate policy effects from misconfiguration`
- `rank top blockers with confidence`
- `draft outreach messages`

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- Keep all operations read-only. Never run `scancel`, `scontrol update`, `scontrol hold`, `scontrol release`, `srun`, `sbatch`, `salloc`, or any command that mutates scheduler or job state.
- Never alter any job, including current user jobs.
- Never infer intent from a single snapshot. Capture an initial timestamped snapshot and one refresh snapshot before final attribution.
- Never treat queue waiting alone as misconfiguration; require fit/fragmentation evidence on CPU+memory+GPU dimensions.
- Separate likely submission misconfiguration from scheduler policy effects (QoS weights, partition defaults, fair-share, dependencies, reservations).
- Test at least one disconfirming hypothesis for every high-confidence attribution candidate.
- Use neutral language (`candidate`, `possible`, `likely`) and include confidence levels.
- Prefer quoted paths and explicit path checks in shell commands to reduce avoidable failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.
- If cluster access is blocked, report concrete blocker evidence and exact commands needed to unblock.

## Scope and identity (must establish first)

Determine and record:
- `cluster_user`: analyst identity for command scope.
- `cluster_host`: cluster endpoint used for evidence.
- `partition_scope`: analyzed partitions (for example `training`, `gpu`).
- `analysis_window`: live snapshot time and any historical range.

Unless explicitly asked otherwise, analyze all users in scope because the goal is shared-capacity attribution, not only self-jobs.

## Workflow

### 0) Mode selection

- Select `quick-scan` mode for fast answers (for example `who is blocking resources right now`).
- Select `deep-attribution` mode for root-cause separation, confidence scoring, and outreach-ready evidence.
- In ambiguous cases, start with quick-scan and escalate only if the answer remains unclear.
- If `quick-scan` mode is selected, run only quick-scan workflow and report; do not run deeper steps unless asked.

### 0.5) Quick-scan workflow (quick-scan mode only)

- Run preflight/light wiring from step 1.
- Collect minimum data needed to answer the question:
  - queue snapshot (`squeue`),
  - node fit snapshot (`sinfo` + `scontrol show node`),
  - candidate job `ReqTRES`/`AllocTRES` (`scontrol show job -d`),
  - priority/QoS context (`sprio`, `sacctmgr show qos`) only if attribution depends on it.
- Keep it read-only and return quick-scan report; stop unless user requests deep-attribution.

### 1) Preflight and evidence snapshot

- Confirm `pwd`, identity, and connectivity to Slurm host.
- Prefer project-native cluster wrappers/scripts when available; fall back to raw `ssh + squeue/sacct/scontrol`.
- Validate required commands (`ssh`, `squeue`/`sacct` via remote if local tools absent, `rg`, `python3`).
- Capture timestamped scheduler snapshots:
  - `squeue` for running/pending jobs with user, partition, reason, and allocated node list.
  - `sinfo` and `scontrol show node` for node states and free/allocated CPU, memory, GPU.
  - `scontrol show job -d` for suspected jobs to get `ReqTRES`, `AllocTRES`, and constraints.
  - `sprio` and `sacctmgr show qos` when priority policy may explain waiting.
- If needed, collect recent `sacct` records for trend confirmation.

### 2) Confirm cluster health before blaming users

- Rule out infrastructure issues first: down/drain/fail nodes, reservations, or scheduler outage.
- If infra is healthy, continue to attribution.
- If infra is unhealthy, report that as primary blocker and do not over-attribute to user misconfiguration.

### 3) Build fit and fragmentation view

- Compute node-level fit constraints: a pending job must fit CPU + memory + GPU simultaneously.
- Identify stranded leftovers by node:
  - idle GPUs with insufficient free CPU or memory to place queued jobs,
  - idle CPUs with memory exhausted,
  - idle resources caused by shape mismatch rather than true free capacity.
- Highlight the specific resource dimension that prevents placement per blocked job class.

### 4) Detect candidate misconfiguration patterns

Flag only with evidence. Common high-signal patterns:
- `gpu=0` jobs on GPU nodes requesting near-full node memory and stranding multiple GPUs.
- Jobs with oversized CPU requests relative to GPU count that leave orphaned GPUs on busy nodes.
- Jobs with very high memory requests that make residual GPUs/CPUs unschedulable.
- Oversized single-job shapes that cannot be packed despite substantial fragmented free capacity.

For each candidate, capture:
- job ID, user, job name, partition, node(s), state, reason,
- `ReqTRES` and `AllocTRES`,
- what becomes stranded (for example `7 GPUs idle on node X while mem free is 0`).

### 5) Separate policy effects from submission effects

Before attributing to user misconfiguration, test policy explanations:
- QoS priority weights and fair-share differences.
- Partition defaults (`DefMemPerGPU`, `DefCpuPerGPU`) that inflate allocations.
- Hyperthread/core accounting behavior.
- Explicit dependencies (`afterany`, arrays) and reservation constraints.

Apply explicit falsification checks:
- If pending jobs are blocked mainly by priority deltas and not by fit on available nodes, downgrade submission blame confidence.
- If stranded capacity can be explained by partition defaults alone, classify as `policy-likely` unless job-specific evidence contradicts.
- If evidence is mixed, classify as `mixed` and avoid single-user blame language.

Classify each finding as one of:
- `submission-likely`: likely user-level request misfit.
- `policy-likely`: mostly scheduler/QoS/defaults behavior.
- `mixed`: both policy and submission shape contribute.

### 6) Rank top blockers by impact and confidence

Use an explicit score:
- `impact`: amount of stranded capacity and expected queue delay contribution.
- `confidence`: strength of attribution after policy checks.

Confidence rubric:
- `high`: direct node/job evidence plus failed falsification checks.
- `medium`: strong indicators but at least one unresolved policy confounder.
- `low`: plausible but not well-separated from policy or transient effects.

Prioritize only high-impact findings. Avoid naming low-confidence users as primary blockers.

### 7) Prepare neutral follow-up actions (no mutations)

- Recommend non-destructive next actions only:
  - verify intent with job owner,
  - suggest resource-shape checks,
  - suggest partition/QoS discussions with admins if policy-driven.
- Provide optional outreach draft text that asks for confirmation and context without blame.

## Report format (required)

Return sections in this order:
1. Findings summary.
2. Source ledger.
3. Timestamp and scope.
4. Cluster health status (infra vs scheduling policy vs job shape).
5. Top candidate blockers by user/job (impact + confidence + evidence).
6. Policy-vs-submission classification table.
7. Why resources appear idle (fragmentation explanation).
8. Coverage gaps and explicit unknowns.
9. Recommended follow-up actions (read-only, neutral outreach).
10. Evidence runbook (commands and artifacts inspected).

Source ledger entry requirements:
- `where_found`: exact system/file/output location.
- `link`: workspace path or command context.
- `confidence`: `high`, `medium`, or `low` with brief reason.
- `relevance`: why this source supports the attribution.

Quick-scan report (short form):
1. Snapshot timestamp and question answered.
2. Scope and identity.
3. Direct answer with impact/confidence labels.
4. Key evidence lines (`ReqTRES`, node free/used, pending reason).
5. Any blockers and exact unblock command.

## Prompt templates

- `[$cluster-blame] quick-scan: identify likely users/jobs currently stranding CPU/GPU/memory, with evidence and confidence.`
- `[$cluster-blame] deep-attribution: explain why resources are idle despite pending jobs, separate policy effects from likely submission misconfiguration, and rank top blockers.`
- `[$cluster-blame] deep-attribution: generate a neutral outreach draft for the top 3 high-confidence blocking candidates.`

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you establish an important attribution rule, threshold, or classification convention, capture the rationale in a durable place (docs, runbooks, or tests for parser/analysis logic). Do not rely only on `plan/` scratch notes.

## Repeat invocations

- Resume from prior snapshots/findings and prioritize net-new evidence.
- Recheck only changed jobs/nodes unless verification requires a full refresh.
- If no material changes occurred, report `no material change` and keep prior ranking with updated timestamp.
