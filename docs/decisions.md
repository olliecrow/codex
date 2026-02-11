# Decision Capture Policy

This document defines how to record fixes and important decisions so future work does not re-litigate the same questions. It is written to stay accurate over time; avoid time-specific language.

## When to record
- Any fix for a confirmed bug, regression, or safety issue.
- Any deliberate behavior choice that differs from intuitive defaults.
- Any trade-off decision that affects modeling or behavior.
- Any change that affects external behavior, invariants, or public APIs.

## Where to record
Use the smallest, most local place that makes the decision obvious:
- **Code comments** near the behavior when the rationale is not obvious.
- **Tests** with names/assertions that encode the invariant.
- **Docs** (this file or another focused doc) when the decision is cross-cutting.

Prefer updating an existing note over creating a new file.

## What to record
Keep entries short and focused:
- **Decision**: what was chosen.
- **Context**: what problem or risk it addresses.
- **Rationale**: why this choice was made.
- **Trade-offs**: what we are not doing.
- **Enforcement**: which tests or code paths lock it in.
- **References** (optional): file paths, tests, or PRs that embody the decision.

## Recorded decisions
Decision: Skills default to proactive, autonomous execution for normal in-scope work, and user input is requested only when absolutely necessary.
Context: Repeated invocations were losing momentum due to avoidable check-ins and partial handoffs.
Rationale: Minimizing interruptions improves throughput while preserving safety by narrowing prompts to true blockers and risk decisions.
Trade-offs: Less routine human checkpointing; mitigated by strict escalation triggers for ambiguity, material-risk trade-offs, missing required access/data, and destructive/irreversible actions outside policy.
Enforcement: Shared principles in `docs/skills.md`, repo guidance in `AGENTS.md`, and per-skill `Proactive autonomy and knowledge compounding` sections in `skills/*/SKILL.md`.
References: `docs/skills.md`, `AGENTS.md`, `skills/organise-docs/SKILL.md`, `skills/git-commit/SKILL.md`.

Decision: Non-trivial skill workflows run adaptive loop passes until completion criteria are met.
Context: One-pass execution was leaving actionable issues unresolved between passes.
Rationale: Adaptive loops improve quality by repeatedly investigating, fixing, verifying, and re-checking until evidence shows completion.
Trade-offs: Additional execution cycles on complex tasks; mitigated by explicit stop criteria and scope discipline.
Enforcement: Shared principles in `docs/skills.md`, loop requirements in per-skill proactive sections, and explicit repeat-pass workflow steps in key skills.
References: `docs/skills.md`, `skills/cleanup/SKILL.md`, `skills/git-review/SKILL.md`, `skills/battletest/SKILL.md`.

Decision: For any non-trivial task, run recurring checkpoints with frequent `organise-docs` updates and small logical `git-commit` checkpoints.
Context: Durable rationale and reviewable progress were drifting when updates were deferred to end-of-task.
Rationale: Frequent docs + commit checkpoints improve recoverability, reduce risk, and compound reusable knowledge while context is fresh.
Trade-offs: Adds lightweight process overhead; mitigated by keeping checkpoints small and tied to meaningful milestones.
Enforcement: Shared checkpoint guidance in `docs/skills.md`, repo policy in `AGENTS.md`, and per-skill `Long-task checkpoint cadence` sections.
References: `docs/skills.md`, `AGENTS.md`, `skills/organise-docs/SKILL.md`, `skills/git-commit/SKILL.md`.

Decision: Skills should default to autonomous fallback/retry/resume behavior before reporting blockers.
Context: Recent sessions showed repeated transient failures (timeouts, SSH/remote transport issues, missing tools/paths) and repeated re-invocations of the same objectives.
Rationale: Explicit fallback/retry/resume rules reduce avoidable interruptions, improve progress continuity, and keep agents focused on net-new work.
Trade-offs: Slightly more autonomous retries can add extra command attempts; mitigated by bounded retries, backoff, and explicit failure evidence before escalation.
Enforcement: Shared proactive-autonomy bullets in `skills/*/SKILL.md`, plus explicit transient-failure handling in cluster and wait workflows.
References: `skills/wait-for-job/SKILL.md`, `skills/cluster-check/SKILL.md`, `skills/cluster-optimise/SKILL.md`.

Decision: Session startup should default to `prime` familiarization and contract setup before deep execution.
Context: Recent multi-repo sessions repeatedly spent early turns re-establishing autonomy expectations, local context, and hygiene cadence.
Rationale: A standardized prime pass improves first-pass quality by immediately grounding execution in repo docs/state and activating recurring `organise-docs`/`git-commit`/`cleanup`/verification loops.
Trade-offs: Adds lightweight startup overhead; mitigated by keeping prime preflight concise and immediately transitioning into execution.
Enforcement: `prime` skill workflow requirements, shared principles in `docs/skills.md`, and skill list routing in `AGENTS.md`.
References: `skills/prime/SKILL.md`, `docs/skills.md`, `AGENTS.md`.

## Template
```
Decision:
Context:
Rationale:
Trade-offs:
Enforcement:
References:
```
