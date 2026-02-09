---
name: tech-debt
description: Alias for `cleanup` with a tech-debt focus. Use when a user requests `$tech-debt`; delegate directly to the `cleanup` skill workflow.
---

# tech-debt

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: move the task forward without waiting when the next high-value action is clear.
- Act autonomously on high-conviction, in-scope actions and fixes; ask only when confidence is low or risk is meaningful.
- Drive work to complete outcomes with verification, not partial handoffs.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Overview

This is a thin alias for the `cleanup` skill, focused on technical debt reduction.

## Workflow

1. Load and follow `../cleanup/SKILL.md`.
2. Prioritize tech-debt, bloat, redundancy, and maintainability concerns as directed by `cleanup`.
3. If there is any mismatch, prefer the canonical `cleanup` skill instructions.
