---
name: prime
description: Prime any conversation at session start by familiarizing with available project docs and repo state, then establishing cross-project operating principles, autonomy defaults, verification posture, and recurring execution loops. Use when the user asks to prime the session or wants proactive/autonomous behavior with minimal unnecessary questions, frequent docs updates, frequent checkpoint commits, and regular cleanup.
---

# Prime

## Overview

Prime the conversation before substantial execution so work stays proactive, autonomous, and completion-driven across any project.

Start with a fast familiarization sweep of docs and current repo state, then set a clear session operating contract, activate recurring loops (`organise-docs`, `git-commit`, `cleanup`, verification), and keep enforcing the contract for the rest of the conversation.

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
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes until completion criteria are met.
- Compound knowledge aggressively over time: capture notes/findings continuously, then promote durable learnings/decisions into long-lived docs as soon as confidence is high.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Aggressive knowledge compounding (must follow)

- Keep a running findings log during execution; do not rely on end-of-task memory reconstruction.
- Route notes by durability:
  - short-lived scratch notes, experiments, and command artifacts -> `plan/`
  - durable principles, decisions, invariants, and high-value lessons -> `docs/`
- Promote durable knowledge early and repeatedly, not only in final summaries.
- Update existing docs first when possible; avoid fragmentation and duplication.
- When a non-obvious decision is made, capture `Decision`, `Context`, `Rationale`, `Trade-offs`, and `Enforcement` in the most local durable place.
- Prune stale scratch artifacts after promotion so `plan/` stays navigable.

## Priming outcomes

After priming, the session should have all of the following:

- A clear operating contract for autonomy, escalation boundaries, and completion criteria.
- A concise familiarity snapshot of the project/repo, based on available docs and current git/worktree state.
- A concrete execution loop for the current objective (adapted, not rigid).
- Explicit recurring hygiene loops:
  - documentation compounding loop (`organise-docs`)
  - checkpoint commit loop (`git-commit`)
  - cleanup loop (`cleanup` / `tech-debt` style passes)
  - verification loop (`verify` / targeted tests / `battletest` when risk warrants)
- A startup checklist showing what was confirmed and what assumptions are active.
- A live note-routing setup for this session:
  - ephemeral working notes in `plan/current/` (or in-memory fallback when plan writes are unavailable)
  - durable decisions/findings promoted into `docs/` during execution

## Workflow

### 1) Run startup preflight

- Confirm working directory/repo root and read project instructions (for example `AGENTS.md`, relevant docs/decision records).
- Confirm current git state (`git status -sb`) and identify whether the tree is clean or dirty.
- Confirm available tools and immediate constraints needed for likely work.

### 2) Run a familiarization sweep

- Discover and read high-signal docs that exist in the repo (for example `README*`, `AGENTS*`, `CLAUDE*`, `docs/`, architecture/runbook files, and relevant decision records).
- Build a concise project-state snapshot:
  - branch and divergence context when relevant
  - local working tree status and active diffs
  - obvious build/test entrypoints and workflow constraints
- If the project is unfamiliar or complex, run a short familiarize pass using `/Users/oc/repos/me/codex/skills/familiarize/SKILL.md` before deep execution.

### 3) Establish session operating contract

- State and apply the default behavior for this session:
  - proactive + autonomous execution
  - ask only when absolutely necessary
  - loop until completion criteria are met
  - keep scope tight and verification explicit
- If user constraints conflict with default contract, adopt user constraints and record the override.

### 4) Define the active execution loop

- Choose an adapted loop for the current objective. Example patterns:
  - issue-resolution: `investigate -> plan -> implement -> verify -> battletest -> organise-docs -> git-commit -> re-review`
  - cleanup-heavy: `scan -> prioritize -> clean -> verify -> organise-docs -> git-commit -> re-scan`
  - docs-heavy: `audit -> update -> verify -> organise-docs -> re-audit`
- Treat examples as templates, not rigid sequences.

### 5) Activate recurring hygiene loops

- `organise-docs` loop:
  - run after substantial findings, non-obvious decisions, or behavior changes.
  - promote durable knowledge from `plan/` to `docs/` during execution, not only at the end.
- `git-commit` loop:
  - run at commit-eligible milestones and at least once per major phase when checks are green and policy permits.
  - keep commits small, logical, and easy to review.
- `cleanup` loop:
  - run regular lightweight cleanup passes to remove redundant or dead additions introduced during work.
  - keep cleanup scoped; avoid speculative refactors unless clearly justified.
- note-taking/knowledge loop:
  - keep a current session note file in `plan/current/` for findings, assumptions, experiments, and open questions.
  - periodically consolidate those notes and push durable items into docs via `organise-docs`.

### 6) Prime summary handoff

Provide a concise prime summary before deep execution:

- active objective and scope assumptions
- familiarity snapshot (docs reviewed + current repo state)
- operating contract in force
- selected execution loop
- planned cadence for docs/commit/cleanup/verification
- immediate first actions

Then proceed directly into execution.

### 7) Enforce throughout the session

- Re-apply the prime contract whenever drift appears (for example repeated low-value reruns, avoidable user questions, stale docs, or delayed checkpoint commits).
- Continue from prior artifacts and logs when re-invoked; do not reset progress unless required.
- If there is nothing left to do, say so explicitly and stop.

## Guardrails

- Do not let priming become overhead; keep startup concise and begin real execution quickly.
- Do not use priming as a reason to avoid verification, docs compounding, or checkpoint commits.
- Do not ask the user to re-confirm defaults that are already clear from policy or context.
- Do not force unnecessary commits or docs edits when there are no meaningful changes.
