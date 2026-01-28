---
name: setup
description: Initialize docs/plan/decisions conventions in a repo; create structure if missing; no-op if already set up.
---

# Setup

## Overview

Set up a consistent, agent-focused documentation and planning structure in any repo. The setup is idempotent: if everything is already in place, do nothing.

## Behavioral guardrails (must follow)

- State assumptions explicitly; if repository intent or constraints are unclear, ask.
- Prefer the minimal change set that satisfies the setup definition; avoid extra structure or features.
- Keep changes surgical and scoped to setup requirements only.

## Scope and permissions

- Apply changes in the current working directory (repo root), unless explicitly directed otherwise.
- Proceed with file/dir edits by default. If the user explicitly forbids edits or creation, do not modify the repo and report that setup was skipped.

## Restricted environments

If edits are not permitted (policy, permissions, or explicit user instruction), do not attempt setup. Report which required elements are missing and note that other skills must fall back to in-memory plan notes and local rationale capture (code comments or tests) until setup is allowed.

## Definition of "already set up"

Consider the repo set up only if all of the following are true:
- `docs/README.md` exists and states that `docs/` is long-term, agent-focused, committed, and evergreen.
- `docs/decisions.md` exists and defines a decision-capture policy with a template.
- `plan/` exists (subfolders as defined below are preferred).
- `.gitignore` ignores `plan/`.
- `AGENTS.md` documents `docs/`, `plan/`, and decision-capture policy usage.

If any element is missing, perform setup.

## Workflow

1. Inspect repository state:
   - Locate `AGENTS.md`, `.gitignore`, and check for `docs/` and `plan/` directories.
   - Verify whether the required docs and policy already exist.

2. If already set up:
   - Make no changes.
   - Report that setup was already present.

3. If setup is needed, apply the following changes (minimal edits only):
   - **AGENTS.md**: add or update sections that define:
     - `docs/` as long-term, agent-focused docs committed to git, evergreen, and kept lean.
     - `plan/` as short-term, disposable scratch space for agents, not committed.
     - decision capture policy location at `docs/decisions.md`.
     - recommended `plan/` subdirectories:
       - `plan/current/`
       - `plan/backlog/`
       - `plan/complete/`
       - `plan/experiments/`
       - `plan/artifacts/`
       - `plan/scratch/`
   - **docs/**:
     - Create `docs/README.md` with an evergreen description of `docs/` usage and its relationship to `plan/`.
     - Create `docs/decisions.md` with the decision-capture policy and template.
     - If these files already exist but are missing the required content, add the missing content without deleting unrelated material.
   - **plan/**:
     - Create `plan/` and the recommended subdirectories listed above.
   - **.gitignore**:
     - Ensure `plan/` is ignored (add a `plan/` entry if missing). Do not remove existing ignore rules.

4. Validate:
   - Confirm files and directories exist.
   - Confirm required content is present.

## Canonical templates

Use these templates when creating new files.

**docs/README.md**
```
# Docs Directory

This directory holds long-term, agent-focused documentation for this repo. It is not intended for human readers and is committed to git.

Principles:
- Keep content evergreen and aligned with the codebase.
- Avoid time- or date-dependent language.
- Prefer updating existing docs over adding new files unless the content is clearly distinct.
- Use docs for cross-cutting context or rationale that does not belong in code comments or tests.
- Keep entries concise and high-signal.

Relationship to `/plan/`:
- `/plan/` is a short-term, disposable scratch space for agents and is not committed to git.
- `/docs/` is long-lived; only stable guidance should live here.
```

**docs/decisions.md**
```
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

## Template
```
Decision:
Context:
Rationale:
Trade-offs:
Enforcement:
References:
```
```

## Notes

- Make the smallest change needed; do not rewrite unrelated content.
- Keep wording simple and evergreen; avoid timestamps unless the repo already uses dated decisions.
