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
   - Prioritize debt that hurts maintenance or clarity.

3. Investigate safely:
   - Proactively create and run targeted experiments or standalone tests to confirm behavior.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing); keep it untracked and never commit it.

4. Apply improvements:
   - Make simplifying, low-risk changes.
   - Preserve functionality and performance.
   - Avoid introducing new complexity while "cleaning."

5. Verify after changes:
   - Rerun relevant tests/experiments (small before large) to confirm no functional or performance regressions.
   - Clean up temporary test scripts unless they are needed to track a discovered issue.

6. Summarize results:
   - List debt addressed and key changes.
   - Call out any remaining risky areas or deferred debt.
   - Note possible next steps.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue hunting for new debt and append new findings rather than repeating prior summaries.
