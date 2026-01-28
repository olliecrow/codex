---
name: battletest
description: Proactively battle-test recent code changes across many configurations and perspectives. Use when asked to validate changes, run broad test coverage, or stress the codebase beyond the obvious checks.
---

# battletest

## Overview

Run many test perspectives and configurations, starting small and scaling up, then summarize outcomes, red flags, and next steps. Conduct a deep, thorough validation that maps coverage to all relevant changes and decisions, and reason through the results.

Prefer empirical testing with real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.

## Behavioral guardrails (must follow)

- State assumptions about scope and coverage; if multiple interpretations exist, surface them.
- Prefer the simplest tests that meaningfully increase confidence before scaling up.
- Avoid unrelated code changes; keep any fixes or test additions strictly in scope.
- Define success criteria and map each to a test or check.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

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
- Run fast, small checks first (lint, unit tests, targeted suites).
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
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Avoid repeating the same tests; add new variations and deeper angles.

4. Summarize results:
   - List tests/checks executed.
   - Provide conclusions and confidence level.
   - Call out critical red flags or issues.
   - Confirm whether any changes during testing introduced regressions in functionality or performance.
   - Track and append to the running list of known issues if re-invoked.
   - Note obvious next steps or follow-up investigations.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
