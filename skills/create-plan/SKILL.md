---
name: create-plan
description: Alias for `plan`. Use when a user requests `$create-plan`; delegate directly to the `plan` skill workflow.
---

# create-plan

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

This is a thin alias for the `plan` skill.

## Workflow

1. Load and follow `../plan/SKILL.md`.
2. Apply the `plan` workflow end-to-end without adding a second, conflicting process.
3. If there is any mismatch, prefer the canonical `plan` skill instructions.
