---
name: reviewbranch
description: Deep review of a branch vs main to find critical issues before merge. Use when asked to assess readiness to merge or to audit differences for red flags.
---

# Review Branch

## Overview

Compare the current branch against main, analyze each change's intent and risk, and hunt for critical red flags before merge.

## Workflow

1. Establish diff scope:
   - Compare current branch to main (or the branch it diverged from).
   - Enumerate all changed files and hunks.

2. Understand intent:
   - For each change, identify the rationale, intent, and expected impact.
   - Flag unclear or unjustified changes for deeper scrutiny.

3. Deep risk review:
   - Look for critical red flags, regressions, security risks, data loss, perf issues, or correctness bugs.
   - Consider long-term maintainability and hidden coupling.

4. Investigate thoroughly:
   - Proactively create and run experiments, trial runs, or tests as needed.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - After any changes or fixes, rerun relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing); keep it untracked and never commit it.

5. Summarize readiness:
   - List critical issues or red flags.
   - Note required fixes before merge.
   - Provide a merge readiness assessment and next steps.
   - Use a concise verdict template: Ready / Needs fixes / Blocked.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue deeper review and append new findings rather than repeating prior summaries.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
