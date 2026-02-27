---
name: checkpoint
description: "Alias for a checkpoint cycle: run `organise-docs`, then `cleanup`, then `git-commit` to keep docs and commits current during long tasks."
---

# checkpoint

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

This is a thin alias for the standard checkpoint cycle used in long or multi-step tasks:
1) run `organise-docs` to promote durable knowledge, then
2) run `cleanup` to simplify and de-risk recent changes, then
3) run `git-commit` to checkpoint verified changes.

## Trigger phrases

Use this skill when the user asks for:
- `checkpoint`
- `commit/docs checkpoint`
- `organise docs and commit`
- `organise docs, cleanup, and commit`
- `run milestone checkpoint`
- `do docs + commit now`

If the request is the combined docs-promotion and commit cycle, prefer `checkpoint` over invoking separate skills.
If the user explicitly asks to push in the same request, run the checkpoint cycle first and then push. Do not push by default.

## Prompt templates

Use these copy-paste templates:
- `[$checkpoint] run docs promotion + small logical commits for work completed so far.`
- `[$checkpoint] milestone checkpoint now: organise durable findings, cleanup, then commit verified changes.`
- `[$checkpoint] run one checkpoint cycle and report what was documented and committed.`
- `[$checkpoint] run checkpoint and then push (explicitly requested).`

## Workflow

1. Load and follow `../organise-docs/SKILL.md`.
2. Promote durable findings/decisions and keep `plan/` scratch uncommitted.
3. Load and follow `../cleanup/SKILL.md`.
4. Apply high-confidence cleanup and verify no regressions.
5. Load and follow `../git-commit/SKILL.md`.
6. Commit in small logical units after relevant checks pass.
7. Push only when explicitly requested by the user in the same instruction.
8. If there is any mismatch, prefer canonical `organise-docs`, `cleanup`, and `git-commit` instructions.
