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
Decision: Skills default to proactive, autonomous execution for high-conviction, in-scope work, with end-to-end completion and verification.
Context: Repeated skill invocations were spending avoidable cycles on partial handoffs and delayed follow-through.
Rationale: Proactive autonomy improves throughput and reduces coordination overhead while preserving quality through explicit verification requirements.
Trade-offs: Slightly less human checkpointing on routine decisions; mitigated by requiring escalation when confidence is low or risk is meaningful.
Enforcement: Shared principles in `docs/skills.md`, repo guidance in `AGENTS.md`, and per-skill `Proactive autonomy and knowledge compounding` sections in `skills/*/SKILL.md`.
References: `docs/skills.md`, `AGENTS.md`, `skills/organise-docs/SKILL.md`.

## Template
```
Decision:
Context:
Rationale:
Trade-offs:
Enforcement:
References:
```
