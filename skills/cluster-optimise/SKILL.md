---
name: cluster-optimise
description: Iteratively optimize cluster job throughput and resource efficiency for minimum total wall-clock completion time by running staged experiment rounds, analyzing Slurm statuses/logs/outputs, and tuning job shape/resources across pipeline stages (data fetching, preprocessing, caching, training, eval). Use when planning, submitting, monitoring, or refining cluster runs while avoiding crashes and OOM failures.
---

# cluster-optimise

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

Run autonomous, evidence-driven optimization rounds that start with small, low-risk trial jobs and expand only when results justify scaling.

Default to stage-based analysis unless the user specifies otherwise:
- `data_fetching`
- `preprocessing`
- `caching`
- `training`
- `eval`

Treat the primary objective as shortest total wall-clock completion time for the target workload, including queue time, runtime, and retries.
Treat each experiment as a learning step: capture what changed, what improved, and what should be tried next.

## Objectives (priority order)

1. Minimize total wall-clock completion time.
2. Maximize throughput within current cluster constraints.
3. Prevent job failures (OOM, timeout, repeated crashes, bad dependencies).
4. Right-size resource requests by workload type (CPU-only vs GPU).
5. Prefer a higher number of smaller jobs when this improves scheduling fit and safe concurrency.

## Behavioral guardrails (must follow)

- Use project-native cluster scripts/wrappers before ad-hoc commands.
- Keep filtering scoped to the current project/user; avoid cross-project interference.
- Run optimization in rounds and complete evidence collection for each round before moving to the next.
- Use the `wait-for-job` skill to block for completion whenever downstream analysis depends on finished jobs.
- Distinguish queue delay from runtime delay; optimize for total wall-clock, not runtime alone.
- Fail fast on repeated OOM/crash patterns; do not continue scaling unstable configurations.
- Separate CPU and GPU optimization paths when bottlenecks differ.
- Assume CPU capacity is typically more abundant than GPU capacity unless current cluster evidence shows otherwise.
- Ask for clarification only when constraints are ambiguous or a risky decision cannot be inferred.

## Workflow

### 1) Establish scope and success criteria

- Identify project root, cluster user, queue/partition constraints, and target workload definition.
- Confirm whether to optimize the full pipeline or a subset of stages.
- Define success metrics up front:
  - wall-clock to complete target work
  - jobs completed per hour
  - failure rate
  - queue wait vs runtime split

### 2) Build stage baseline

- Map the pipeline into explicit stages (`data_fetching`, `preprocessing`, `caching`, `training`, `eval`).
- For each stage, capture current job shape and baseline metrics from recent runs:
  - requested resources (cpu, mem, gpu, walltime)
  - queue wait
  - elapsed runtime
  - completion state/exit code
  - key utilization signals (cpu/memory/gpu when available)
- Mark the current bottleneck stage(s).

### 3) Design iterative experiment rounds

Start small and scale deliberately:
- Round 0: smoke tests for correctness and obvious failures.
- Round 1: small parameter sweep per stage/job type.
- Round 2+: scale candidate configurations that improve total wall-clock and stability.

Vary only a small number of factors per round:
- resource shape (`cpus`, `mem`, `gpus`, walltime)
- parallelism (array size/concurrency cap)
- job granularity (many small jobs vs fewer large jobs)
- stage placement (CPU offload vs GPU use)

### 4) Submit trials autonomously

- Submit representative trials for CPU-only and GPU paths as needed.
- Prefer many smaller independent jobs when this increases scheduling opportunities and keeps failure blast radius low.
- Keep GPU requests conservative and purposeful when GPU capacity is scarce.
- Bias scalable preprocessing/caching/data work toward CPU lanes when feasible, preserving GPU slots for truly GPU-bound training/eval work.
- Record exact submitted job IDs and tested hypotheses.

### 5) Wait and monitor

- Invoke `wait-for-job` to poll job completion before dependent analysis.
- Monitor Slurm state transitions and detect early failure signals:
  - OOM kills
  - timeout/cancel patterns
  - dependency deadlocks
  - repeated node/environment faults

### 6) Analyze evidence per stage

For each completed trial, inspect:
- Slurm metadata (`squeue`, `sacct`, `scontrol`, or project wrappers)
- stdout/stderr logs
- produced outputs/artifacts
- utilization summaries where available

Compute decision signals:
- total wall-clock impact (`queue + runtime + retries`)
- throughput per stage
- resource efficiency (allocated vs used)
- failure risk profile

### 7) Tune and choose next iteration

- Promote only high-confidence configurations.
- Apply targeted fixes for failures before scaling:
  - OOM: reduce memory pressure (for example smaller batch/chunk) or increase memory request if justified.
  - underutilized resources: reduce requests or raise parallelism.
  - long queue for large jobs: split into smaller jobs and increase count.
  - GPU contention: move eligible work to CPU stages and reserve GPU for true GPU-bound work.
- Continue rounds until improvements plateau or constraints are reached.

### 8) Capture learnings and checkpoint work

- Invoke `organise-docs` after each substantial round to preserve durable learnings, constraints, and winning configurations.
- Invoke `git-commit` at commit-eligible milestones (checks green, policy permits) to keep progress granular and reversible.
- Clean up temporary `plan/` artifacts that no longer add value.

### 9) Report required output

Always report in this order:
1. Optimization objective and scope.
2. Round-by-round experiment table (hypothesis, config, job IDs, outcome).
3. Stage-level findings (`data_fetching`, `preprocessing`, `caching`, `training`, `eval`).
4. Resource-fit recommendations (CPU and GPU separated).
5. Failure/OOM analysis and mitigations.
6. Chosen next configuration and expected wall-clock impact.
7. Documentation and commit checkpoints completed.
8. Remaining risks and next trial plan.

## Practical heuristics

- Optimize for `queue + runtime`, not runtime alone.
- Favor smaller jobs when cluster fragmentation and idle capacity make them faster to start.
- Keep experiments short and informative early; avoid expensive large runs before bottlenecks are clear.
- Treat repeated OOMs as a hard signal to redesign job shape before retrying.
- Prefer stable, reproducible configurations over fragile peak-speed settings.
