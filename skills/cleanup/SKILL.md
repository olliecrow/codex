---
name: cleanup
description: Review recent code changes and simplify/clean them without breaking behavior or performance. Use when asked to tidy up or lightly refactor work from the current branch or conversation.
---

# Cleanup

## Overview

Identify recent changes, then simplify, tidy, and de-over-engineer while preserving behavior and performance.

## Workflow

1. Identify scope of changes:
   - Compare current branch to its base (or main/master) to find what changed.
   - Include changes made during the current conversation.

2. Find cleanup opportunities:
   - Remove redundancy, simplify logic, reduce over-engineering.
   - Improve readability and maintainability.
   - Keep changes focused on tidying up, not feature work.

3. Investigate and validate:
   - Proactively create and run isolated tests or experiments to understand behavior.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing); keep it untracked and never commit it.

4. Apply cleanup changes:
   - Make small, safe simplifications.
   - Prefer clarity and minimalism.
   - Keep edits localized to changed areas unless a broader cleanup is clearly safe.
   - Do not break existing features.
   - Do not regress runtime or memory performance.
   - Avoid making code more complex.

5. Verify after changes:
   - Rerun relevant tests/experiments (small before large) to confirm no functional or performance regressions.
   - Clean up temporary test scripts unless they are needed to track a discovered issue.

6. Summarize results:
   - List areas cleaned up and why.
   - Call out any risky areas avoided.
   - Note possible next cleanup steps.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue finding new cleanup opportunities and avoid repeating prior summaries unless there are no new changes.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
