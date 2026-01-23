---
name: battletest
description: Proactively battle-test recent code changes across many configurations and perspectives. Use when asked to validate changes, run broad test coverage, or stress the codebase beyond the obvious checks.
---

# battletest

## Overview

Run many test perspectives and configurations, starting small and scaling up, then summarize outcomes, red flags, and next steps. Conduct a deep, thorough validation that maps coverage to all relevant changes and decisions, and reason through the results.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Rationale capture

When you fix an issue, make a change that resolves an issue, or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded.

## Workflow

1. Establish baseline:
- Identify the change scope.
- Ensure coverage maps to every relevant change, assumption, and risk area; do not leave gaps.
- Run fast, small checks first (lint, unit tests, targeted suites).
   - Proactively create and run small, isolated experiments or standalone tests when useful.
   - Stop early if basics fail; fix before scaling up.
   - After any fixes or changes, rerun the fast checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing); keep it untracked and never commit it.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

2. Expand test coverage:
   - Vary configs (feature flags, env vars, build modes).
   - Vary environments (OS, versions, dependencies) when feasible.
   - Vary perspectives (unit, integration, e2e, performance, security, UX, accessibility, API contract, data migration).
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
