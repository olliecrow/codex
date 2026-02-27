---
name: familiarize
description: Meticulously familiarize with a codebase to understand structure, purpose, and workflows; use when asked to get the lay of the land, orient in a repo, summarize architecture, or assess current branch changes vs main.
---

# Familiarize

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
- In shared repositories, assume concurrent edits from humans/agents are normal and avoid reverting unknown changes by default.
- When commits are in scope, stage only intentionally changed files for the current task and exclude unrelated concurrent edits.
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

Build a clear, accurate mental model of the codebase: layout, purpose, key flows, and current change state. When reviewing changes, conduct a deep, thorough review so every relevant change and decision is understood.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Default write scope is the current `cwd` and its subdirectories.
- Read-only inspection outside the current `cwd` is allowed when needed for context; do not modify outside the `cwd` tree unless the user explicitly requests it.
- State assumptions explicitly; if something is unclear or has multiple interpretations, ask.
- Prefer the simplest explanation supported by evidence; avoid speculative conclusions.
- Keep scope surgical and read-only unless explicitly asked to edit.
- For public/open-source repos, call out any discovered secrets, sensitive data exposure risk, or local system path leakage as explicit findings.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Git safety and permissions

- Follow the current repo's git policy and the session's environment restrictions; if git writes or pushes are disallowed, do not perform them and provide commands instead.
- Never rewrite git history or force push. Do not use `git rebase`, `git commit --amend`, `git reset --hard`, `git reset --soft`, `git reset --mixed`, `git push --force`, `git push --force-with-lease`, or `git filter-branch`, or `git clean -fdx`.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you fix an issue, make a change that resolves an issue, or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing docs when they have a clear home, but create new focused docs/subdirectories when it improves navigability (and link them from related docs or indexes).
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Establish scope and constraints:
   - Identify repo root and primary language/tooling.
   - Clarify any time constraints or areas of focus if the user is vague.
   - Prefer read-only exploration; do not modify files unless explicitly asked.

2. Map the repository layout:
   - Scan top-level structure and key directories.
   - Read the primary docs (README, docs/, CONTRIBUTING, ARCHITECTURE) if present.
   - Identify entrypoints, build/test scripts, and configuration files.

3. Understand how the system works:
   - Locate main modules, services, or packages and their responsibilities.
   - Trace high-level data flows or request paths through the code.
   - Note external dependencies and integrations.
   - Identify any conventions (naming, folder roles, patterns).

4. Capture developer workflows and interfaces:
   - Build/run/test map: capture canonical commands and where they live (scripts, Makefile, CI).
   - Config and environment: list required env vars, config files, secrets expectations, and local dev setup.
   - Interfaces: enumerate public APIs/CLIs or entrypoints for users/services.
   - Note similar onboarding essentials when present (e.g., CI/CD, release flow, data stores).

5. Inspect current working tree state:
   - Check `git status -sb`.
   - Review `git diff` and `git diff --staged` for local changes.
   - If diffs are large, start with `git diff --stat` or `git diff --name-only` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue with non-git repo familiarization, and mark git-dependent findings as pending.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

6. Compare against main when relevant:
   - If the current branch is not main, review diffs vs main (e.g., `git diff main...HEAD` and relevant logs).
   - If diffs are large, start with `git diff --stat main...HEAD` or `git diff --name-only main...HEAD` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat main...HEAD`, `git diff --name-only main...HEAD`, or per-file diffs instead of unbounded commands.
   - Summarize how the current branch diverges (scope and intent) and which areas are affected.
   - Review every changed file and hunk when comparing against main; do not skip relevant areas.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue architecture/workflow familiarization, and call out any branch-diff uncertainty explicitly.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

7. Optional deeper dives (as needed):
   - Read critical modules or hot paths to validate understanding.
   - Skim tests to understand expected behavior and coverage.
   - Identify any missing or outdated documentation.

8. Summarize findings:
   - Provide a concise, intuitive summary of the repo structure, purpose, and key workflows.
   - Include brief context for a new reader (what the system does, how parts fit together).
   - Summarize current git status, local diffs, and branch-vs-main diffs if applicable.
   - Note open questions, uncertainties, or areas that need deeper review.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
