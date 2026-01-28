---
name: techdebt
description: Review the codebase with fresh eyes to find and reduce technical debt without breaking behavior. Use when asked to assess or clean technical debt, especially after recent changes.
---

# techdebt

## Overview

Review the project holistically, investigate debt with tests or experiments as needed, and apply safe simplifications. Conduct a deep, thorough review of all relevant areas and reason through every change and decision.

## Behavioral guardrails (must follow)

- State assumptions explicitly; if scope or intent is unclear, stop and ask.
- Prefer the simplest debt reduction that preserves behavior; avoid speculative improvements.
- Keep changes surgical and limited to the debt being addressed; mention unrelated issues without changing them.
- Define success criteria and verify after changes.

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

1. Establish scope:
- Scan the whole project, with extra focus on recent changes.
- Minimize bias from earlier conversation; reevaluate assumptions.
- Ensure every relevant area is reviewed; do not skip parts that affect behavior.

2. Identify tech debt:
   - Look for over-engineering, duplication, confusing structure, unnecessary complexity.
   - Look for explicitly redundant code that can be removed safely.
   - Scan for TODO/FIXME, deprecated APIs, and stale or misleading docs.
   - Prioritize debt that hurts maintenance or clarity.

3. Prioritize and log:
   - Rank debt by impact (maintainability, risk, churn) and effort.
   - Track a lightweight debt log in `plan/techdebt.md` (untracked) with found items, fixes, and deferred items plus the reason. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - For each planned change, state the intent as "no behavior change" (and note any exception that would require explicit user approval).
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

4. Investigate safely:
   - Proactively create and run targeted experiments or standalone tests to confirm behavior.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - If touching hot paths, capture a baseline or avoid micro-optimizations without evidence.
   - Capture before/after evidence for any performance-sensitive edits.

5. Apply improvements:
   - Make simplifying, low-risk changes.
   - Prefer a few well-done changes over many low-quality ones.
   - Preserve functionality and performance.
   - Keep "no behavior change" intent explicit; stop and ask if a change would alter behavior.
   - Avoid introducing new complexity while "cleaning."

6. Verify after changes:
   - Rerun relevant tests/experiments (small before large) to confirm no functional or performance regressions.
   - Clean up temporary test scripts unless they are needed to track a discovered issue.
   - Do a scope check: confirm changes stayed within tech-debt cleanup and did not drift into feature work.

7. Summarize results:
   - List debt addressed and key changes.
   - Call out any remaining risky areas or deferred debt.
   - Note possible next steps.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue hunting for new debt and append new findings rather than repeating prior summaries.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
