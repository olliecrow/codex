---
name: gitreview
description: Deep review of a branch vs main to find critical issues before merge. Use when asked to assess readiness to merge or to audit differences for red flags.
---

# gitreview

## Overview

Compare the current branch against main, analyze each change's intent and risk, and hunt for critical red flags before merge.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Rationale capture

When you recommend or make a fix, or reach an important decision, ensure the "why" is captured in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded or call out gaps.

## Workflow

1. Establish diff scope:
   - Compare current branch to main (or the branch it diverged from).
   - Enumerate all changed files and hunks.
   - Always conduct a full review of every changed file and hunk.
   - If diffs are large, start with `git diff --stat` or `git diff --name-only` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

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
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

5. Handle huge diffs without skipping coverage:
   - Still review all changes end-to-end; do not sample or skip files.
   - Break the review into batches (by directory, feature, or risk area) and track progress in `plan/gitreview.md`.
   - Use tooling to manage scale (e.g., `git diff --stat`, `git diff --numstat`, per-file diffs, and focused searches) but ensure every file and hunk is covered.
   - If time or compute constraints make a full review impractical, ask the user for a time budget or additional constraints, but keep the full-review requirement explicit.

6. Summarize readiness:
   - List critical issues or red flags.
   - Note required fixes before merge.
   - Provide a merge readiness assessment and next steps.
   - Use a concise verdict template: Ready / Needs fixes / Blocked.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue deeper review and append new findings rather than repeating prior summaries.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
