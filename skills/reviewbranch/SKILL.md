---
name: reviewbranch
description: Alias for `gitreview`. Use when a user requests `$reviewbranch`; delegate directly to the `gitreview` skill workflow.
---

# reviewbranch

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

This is a thin alias for the `gitreview` skill.

## Workflow

1. Load and follow `../gitreview/SKILL.md`.
2. Apply the `gitreview` workflow end-to-end without adding a second, conflicting process.
3. If there is any mismatch, prefer the canonical `gitreview` skill instructions.
