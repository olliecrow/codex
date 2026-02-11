---
name: setup
description: Initialize docs/plan/decisions conventions plus note-routing and orchestration defaults in a repo; create structure if missing; no-op if already set up.
---

# Setup

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
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Set up a consistent, agent-focused operating model in any repo. The setup is idempotent: if everything required is already in place, do nothing.

The setup must work for both:
- new repos with little or no structure
- existing repos that already have conventions and need minimal, additive updates

Primary outcomes:
- durable docs that compound knowledge over time
- disposable scratch space for active work
- explicit routing from scratch notes to durable docs
- clear multi-workstream tracking for orchestrated/subagent workflows
- a spartan default setup that stays lightweight and maintainable

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm the expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- State assumptions explicitly; if repository intent or constraints are unclear, ask.
- Prefer the minimal change set that satisfies the setup definition; avoid extra structure or features.
- Keep changes surgical and scoped to setup requirements only.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Scope and permissions

- Apply changes in the current working directory (repo root), unless explicitly directed otherwise.
- Proceed with file/dir edits by default. If the user explicitly forbids edits or creation, do not modify the repo and report that setup was skipped.
- Preserve existing conventions where they already satisfy required behavior; prefer additive updates over rewrites.

## Restricted environments

If edits are not permitted (policy, permissions, or explicit user instruction), do not attempt setup. Report which required elements are missing and note that other skills must fall back to in-memory plan notes and local rationale capture (code comments or tests) until setup is allowed.

## Productivity bootstrap model (must follow)

`setup` is responsible for bootstrapping the operating workflow, not just creating folders.

Baseline model to install:
- `docs/` stores durable, evergreen guidance and decisions.
- `plan/` stores disposable, task-scoped scratch notes and execution artifacts.
- Decisions are captured in the smallest durable place, with policy in `docs/decisions.md`.
- Notes are routed by purpose:
  - active notes and scratch logs in `plan/current/`
  - long-lived guidance in `docs/`
- Parallel/subagent work has explicit status tracking and handoff conventions to prevent "lost work" across streams.

## Definition of "already set up"

Consider the repo set up only if all of the following are true:
- `docs/README.md` exists and states that `docs/` is long-term, agent-focused, committed, and evergreen.
- `docs/decisions.md` exists and defines a decision-capture policy with a template.
- `docs/workflows.md` exists (or an equivalent workflow doc is referenced from `AGENTS.md`) and defines note routing, promotion, and parallel-work tracking conventions.
- `plan/` exists (subfolders as defined below are preferred).
- `.gitignore` ignores `plan/`.
- `AGENTS.md` documents `docs/`, `plan/`, decision-capture policy usage, and where workflow conventions live.

If any element is missing, perform setup.

## Workflow

1. Inspect repository state:
   - Locate `AGENTS.md`, `.gitignore`, and check for `docs/` and `plan/` directories.
   - Verify whether required docs and policy already exist.
   - Detect whether equivalent workflow guidance already exists under a different doc name; if yes, prefer updating that file and reference it in `AGENTS.md`.

2. If already set up:
   - Make no changes.
   - Report that setup was already present.

3. If setup is needed, apply the following changes (minimal edits only):
   - If `AGENTS.md` is missing, create it with concise sections for docs, plan, and workflow conventions.
   - **AGENTS.md**: add or update sections that define:
     - `docs/` as long-term, agent-focused docs committed to git, evergreen, and kept lean.
     - `plan/` as short-term, disposable scratch space for agents, not committed.
     - decision capture policy location at `docs/decisions.md`.
     - workflow conventions location at `docs/workflows.md` (or equivalent).
     - note routing expectations:
       - active notes in `plan/current/notes.md`
       - multi-workstream index in `plan/current/notes-index.md`
       - orchestration status in `plan/current/orchestrator-status.md`
     - recommended `plan/` subdirectories:
       - `plan/current/`
       - `plan/backlog/`
       - `plan/complete/`
       - `plan/experiments/`
       - `plan/artifacts/`
       - `plan/scratch/`
       - `plan/handoffs/`
   - **docs/**:
     - Create `docs/README.md` with an evergreen description of `docs/` usage and its relationship to `plan/`.
     - Create `docs/decisions.md` with the decision-capture policy and template.
     - Create `docs/workflows.md` with the operating workflow for note routing, promotion, and orchestration.
     - If these files already exist but are missing the required content, add the missing content without deleting unrelated material.
   - **plan/**:
     - Create `plan/` and the recommended subdirectories listed above.
   - **.gitignore**:
     - Ensure `plan/` is ignored (add a `plan/` entry if missing). Do not remove existing ignore rules.

4. Validate:
   - Confirm files and directories exist.
   - Confirm required content is present.
   - Confirm workflow doc and AGENTS references agree on the same routing and orchestration conventions.

## Canonical templates

Use these templates when creating new files.

**AGENTS.md (minimum scaffold)**
```
# Repository Guidelines

## Docs, Plans, and Decisions (agent usage)
- `docs/` is long-lived and committed.
- `plan/` is short-lived scratch space and is not committed.
- Decision capture policy lives in `docs/decisions.md`.
- Operating workflow conventions live in `docs/workflows.md`.

## Plan Directory Structure (agent usage)
- `plan/current/`
- `plan/backlog/`
- `plan/complete/`
- `plan/experiments/`
- `plan/artifacts/`
- `plan/scratch/`
- `plan/handoffs/`
```

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
- `/plan/handoffs/` is used for sequential workflow handoffs between automation scripts when needed.
- Active notes should be routed into `/plan/current/` and promoted into `/docs/` only when they become durable guidance.
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

**docs/workflows.md**
```
# Operating Workflow

This document defines how work is tracked so progress compounds without context bloat.

## Core mode
- Keep active, disposable notes in `/plan/current/`.
- Promote durable guidance into `/docs/`.
- Capture important rationale in the smallest durable place (code comments, tests, or docs).
- Keep the workflow spartan: short notes, clear routing, minimal ceremony.

## Note routing
- `/plan/current/notes.md`: running task notes, key findings, and next actions.
- `/plan/current/notes-index.md`: compact index of active workstreams and pointers to detailed notes.
- `/plan/current/orchestrator-status.md`: packet/status board for parallel or subagent work.
- `/plan/handoffs/`: sequential handoff summaries for staged automation workflows.

## Parallel and subagent workflows
- Use isolated worktrees or dedicated working directories when streams are independent.
- Track each stream with owner, scope, status, blocker, and last update.
- Require each stream to produce a concise handoff summary before merge.

## Promotion cycle
- During execution: write concise notes to `/plan/current/`.
- At meaningful milestones: consolidate and de-duplicate active notes.
- Before finishing: promote durable learnings to `/docs/` and trim stale `/plan/` artifacts.

## Stop conditions
- Stop when acceptance checks pass, risks are documented, and no unresolved blockers remain.
- If no new evidence appears, avoid repeating the same loop; report completion instead.
```

## Notes

- Make the smallest change needed; do not rewrite unrelated content.
- Keep wording simple and evergreen; avoid timestamps unless the repo already uses dated decisions.
