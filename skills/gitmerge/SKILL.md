---
name: gitmerge
description: Prepare the current branch to merge cleanly into main by ensuring a clean working tree, syncing with remote, understanding diffs and intent, planning safe changes, resolving conflicts, and verifying with battle tests.
---

# gitmerge

## Overview

Get the current branch to a merge-ready state with main by understanding differences, planning safely, merging without conflicts, and validating thoroughly.

## Workflow

1. Require a clean working tree:
   - Check `git status -sb` first.
   - If there are unstaged or uncommitted changes, stop and ask the user to address them.

2. Sync with remote:
   - Fetch latest refs.
   - Update main and the current branch from remote (pull or fast-forward) so both are up to date.
   - If remote update fails, stop and ask for guidance.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands for the user to run and wait for their results before continuing.

3. Understand diffs before merging:
   - Compare current branch vs main (`git diff main...HEAD` and `git log main..HEAD`).
   - Read key files to understand intent, behavior, and risk.
   - Understand what main is doing and why before making any merge decisions.

4. Plan the merge approach:
   - Identify conflicts, risky areas, and order of operations.
   - Develop a clear plan to address changes safely.
   - Think deeply and verify the plan is correct and low risk.
   - If there are critical open questions or unclear intent, stop and ask only the necessary clarifying questions.
   - Use a `plan/` directory as scratch space if needed; keep it untracked and never commit it.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

5. Execute the merge:
   - Apply the plan step by step.
   - Resolve conflicts carefully with reasoning aligned to main’s intent and the branch’s intent.
   - Keep changes minimal and avoid introducing new behavior unless required by the plan.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, provide explicit commands and pause until the user reports back.

6. Verify and battle test:
   - Validate that the merge completed cleanly and the working tree is consistent.
   - Run relevant checks/tests, starting small and expanding to broader coverage.
   - Battle test to catch regressions, edge cases, or integration issues.
   - After any fixes, re-run the smallest relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - If failures appear, fix and re-test until green.

7. Summarize:
   - Confirm merge readiness and note any remaining risks or follow-ups.
   - Write in plain, concise, and intuitive language with brief context.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- If called multiple times, avoid repeating the same probes or tests unless verifying a fix.
- Expand coverage gradually: re-check diffs after updates, deepen review of conflicted areas, or add broader tests if risk warrants it.
- Keep a lightweight log in `plan/gitmerge.md` (untracked) of decisions, conflicts, and fixes to avoid rework.
