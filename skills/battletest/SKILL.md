---
name: battletest
description: Proactively battle-test recent code changes across many configurations and perspectives. Use when asked to validate changes, run broad test coverage, or stress the codebase beyond the obvious checks.
---

# battletest

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
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Run many test perspectives and configurations, starting small and scaling up, then summarize outcomes, red flags, and next steps. Conduct a deep, thorough validation that maps coverage to all relevant changes and decisions, and reason through the results.

Prefer empirical testing with real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm the expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- State assumptions about scope and coverage; if multiple interpretations exist, surface them.
- Prefer the simplest tests that meaningfully increase confidence before scaling up.
- Avoid unrelated code changes; keep any fixes or test additions strictly in scope.
- Define success criteria and map each to a test or check.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

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
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Establish baseline:
- Identify the change scope.
- Ensure coverage maps to every relevant change, assumption, and risk area; do not leave gaps.
- Run preflight checks first (`pwd`, required tools, path existence, and test entrypoints).
- Run fast, small checks first (lint, unit tests, targeted suites).
  - Prefer `uv run pytest` over bare `pytest` unless the repo explicitly uses another test runner flow.
  - For long-running checks, use explicit timeouts and capture logs to a temporary artifact path for later review.
  - Treat "no tests collected" as a coverage signal that requires adjustment, not as a pass.
   - Proactively create and run small, isolated experiments or standalone tests when useful.
   - Stop early if basics fail; fix before scaling up.
   - After any fixes or changes, rerun the fast checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

2. Expand test coverage:
   - Vary configs (feature flags, env vars, build modes).
   - Vary environments (OS, versions, dependencies) when feasible.
   - Vary perspectives (unit, integration, e2e, performance, security, UX, accessibility, API contract, data migration).
   - Prefer production-like configurations and real datasets when feasible; document data sources and constraints.
   - Prefer smaller probes before long-running suites, but still run large tests when warranted.
   - If any code changes are made during testing, rerun relevant probes and suites (small before large) to confirm no regressions.
   - Maintain a lightweight test matrix of configs/environments/perspectives already covered to avoid repeats.

3. Be proactive:
   - Keep exploring reasonable new angles and edge cases.
   - Create new investigations without extra prompting.
   - On repeated passes, prioritize net-new high-value coverage and avoid repeating the same tests unless regression confirmation requires it.

4. Summarize results:
   - List tests/checks executed.
   - Provide conclusions and confidence level.
   - Call out critical red flags or issues.
   - Confirm whether any changes during testing introduced regressions in functionality or performance.
   - Track and append to the running list of known issues if re-invoked.
   - Note obvious next steps or follow-up investigations.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

5. Repeat passes until complete:
   - Re-enter Steps 1-4 until no material untested risk areas remain and confidence is high.
   - If testing reveals issues, route through an issue-resolution loop (`investigate -> plan -> fix -> verify -> battletest -> organise-docs -> git-commit -> re-review`) before declaring completion.
