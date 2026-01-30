---
name: gitreview
description: Deep review of a branch vs main to find critical issues before merge. Use when asked to assess readiness to merge or to audit differences for red flags.
---

# gitreview

## Overview

Compare the current branch against main, analyze each change's intent and risk, and hunt for critical red flags before merge. Conduct a deep, thorough review that covers every change and decision end-to-end.

## Behavioral guardrails (must follow)

- Do not assume intent; if multiple interpretations exist, state them explicitly.
- Prefer the simplest explanation for a change and verify it against evidence.
- Keep review scope surgical: every comment should trace to a specific change.
- Define explicit readiness criteria and verify them before concluding.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Git safety and permissions

- Follow the current repo's git policy and the session's environment restrictions; if git writes or pushes are disallowed, do not perform them and provide commands instead.
- Never rewrite git history or force push. Do not use `git rebase`, `git commit --amend`, `git reset --hard`, `git reset --soft`, `git reset --mixed`, `git push --force`, `git push --force-with-lease`, or `git filter-branch`, or `git clean -fdx`.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you recommend or make a fix, or reach an important decision, ensure the "why" is captured in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded or call out gaps.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Sync remote main before anything else:
   - Pull the most recent `origin/main` before any other steps.
   - If the repo uses a different mainline (for example, `master`), sync that instead.
   - If the update cannot be applied safely, stop and ask for guidance.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Establish diff scope:
   - Compare current branch to main (or the branch it diverged from).
   - Enumerate all changed files and hunks.
   - Always conduct a full review of every changed file and hunk.
   - If diffs are large, start with `git diff --stat` or `git diff --name-only` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Understand intent:
   - For each change, identify the rationale, intent, and expected impact.
   - Flag unclear or unjustified changes for deeper scrutiny.

4. Deep risk review:
   - Look for critical red flags, regressions, security risks, data loss, perf issues, or correctness bugs.
   - Consider long-term maintainability and hidden coupling.
   - Ensure anything that worked on main still works here; flag removed or degraded functionality and verify intended parity.

5. Investigate thoroughly:
   - Proactively create and run experiments, trial runs, or tests as needed.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - After any changes or fixes, rerun relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

6. Handle huge diffs without skipping coverage:
   - Still review all changes end-to-end; do not sample or skip files.
   - Break the review into batches (by directory, feature, or risk area) and track progress in `plan/current/gitreview.md`. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - Use tooling to manage scale (e.g., `git diff --stat`, `git diff --numstat`, per-file diffs, and focused searches) but ensure every file and hunk is covered.
   - If time or compute constraints make a full review impractical, ask the user for a time budget or additional constraints, but keep the full-review requirement explicit.

7. Summarize readiness:
   - List critical issues or red flags.
   - Note required fixes before merge.
   - Provide a merge readiness assessment and next steps.
   - Use a concise verdict template: Ready / Needs fixes / Blocked.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue deeper review and append new findings rather than repeating prior summaries.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
