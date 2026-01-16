---
name: techdebt
description: Review the codebase with fresh eyes to find and reduce technical debt without breaking behavior. Use when asked to assess or clean technical debt, especially after recent changes.
---

# techdebt

## Overview

Review the project holistically, investigate debt with tests or experiments as needed, and apply safe simplifications.

## Workflow

1. Establish scope:
   - Scan the whole project, with extra focus on recent changes.
   - Minimize bias from earlier conversation; reevaluate assumptions.

2. Identify tech debt:
   - Look for over-engineering, duplication, confusing structure, unnecessary complexity.
   - Scan for TODO/FIXME, deprecated APIs, and stale or misleading docs.
   - Prioritize debt that hurts maintenance or clarity.

3. Prioritize and log:
   - Rank debt by impact (maintainability, risk, churn) and effort.
   - Track a lightweight debt log in `plan/techdebt.md` (untracked) with found items, fixes, and deferred items plus the reason.
   - For each planned change, state the intent as "no behavior change" (and note any exception that would require explicit user approval).

4. Investigate safely:
   - Proactively create and run targeted experiments or standalone tests to confirm behavior.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing); keep it untracked and never commit it.
   - If touching hot paths, capture a baseline or avoid micro-optimizations without evidence.

5. Apply improvements:
   - Make simplifying, low-risk changes.
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
