---
name: review-branch
description: Alias for `git-review`. Use when a user requests `$review-branch`; delegate directly to the `git-review` skill workflow.
---

# review-branch

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

This is a thin alias for the `git-review` skill.

## Workflow

1. Load and follow `../git-review/SKILL.md`.
2. Apply the `git-review` workflow end-to-end without adding a second, conflicting process.
3. If there is any mismatch, prefer the canonical `git-review` skill instructions.
4. This includes checking active PR metadata (open draft or ready-for-review) and updating title/body when stale.
