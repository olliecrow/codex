---
name: gitmerge
description: Prepare the current branch to merge cleanly into main by ensuring a clean working tree, syncing with remote, understanding diffs and intent, planning safe changes, resolving conflicts, and verifying with battle tests.
---

# gitmerge

## Overview

Get the current branch to a merge-ready state with main by understanding differences, planning safely, merging without conflicts, and validating thoroughly. Conduct a deep, thorough review of all diffs and decisions, and ensure functionality from main still works after the merge.

## Behavioral guardrails (must follow)

- State assumptions explicitly; if intent or requirements are unclear, stop and ask.
- Prefer the simplest merge resolution that preserves intent on both sides; avoid extra refactors.
- Keep changes surgical and limited to merge needs; do not "improve" unrelated code.
- Define success criteria and verify after each meaningful step.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.

## Git safety and permissions

- Follow the current repo's git policy and the session's environment restrictions; if git writes or pushes are disallowed, do not perform them and provide commands instead.
- Never rewrite git history or force push. Do not use `git rebase`, `git commit --amend`, `git reset --hard`, `git reset --soft`, `git reset --mixed`, `git push --force`, `git push --force-with-lease`, or `git filter-branch`, or `git clean -fdx`.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Rationale capture

When you resolve a conflict, fix an issue, or make an important merge decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Require a clean working tree:
   - Check `git status -sb` first.
   - If there are unstaged or uncommitted changes, stop and ask the user to address them.

2. Sync with remote:
   - Fetch latest refs.
   - Update main and the current branch from remote (pull or fast-forward) so both are up to date.
   - If remote update fails, stop and ask for guidance.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands for the user to run and wait for their results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Understand diffs before merging:
   - Compare current branch vs main (`git diff main...HEAD` and `git log main..HEAD`).
   - If diffs are large, start with `git diff --stat main...HEAD` or `git diff --name-only main...HEAD` and then review per-file diffs to keep output manageable.
- Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat main...HEAD`, `git diff --name-only main...HEAD`, or per-file diffs instead of unbounded commands.
- Read key files to understand intent, behavior, and risk.
- Understand what main is doing and why before making any merge decisions.
- Review every changed file and hunk; ensure no main functionality is removed or degraded without explicit intent.

4. Plan the merge approach:
   - Identify conflicts, risky areas, and order of operations.
   - Develop a clear plan to address changes safely.
   - Think deeply and verify the plan is correct and low risk.
   - If there are critical open questions or unclear intent, stop and ask only the necessary clarifying questions.
   - Use a `plan/` directory as scratch space if needed; create it only if permitted, keep it untracked, and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

5. Execute the merge:
   - Apply the plan step by step.
   - Resolve conflicts carefully with reasoning aligned to main’s intent and the branch’s intent.
   - Keep changes minimal and avoid introducing new behavior unless required by the plan.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, provide explicit commands and pause until the user reports back.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

6. Verify and battle test:
- Validate that the merge completed cleanly and the working tree is consistent.
- Run relevant checks/tests, starting small and expanding to broader coverage.
- Battle test to catch regressions, edge cases, or integration issues.
- Explicitly confirm that functionality present on main still works; flag any regressions or removals.
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
- Keep a lightweight log in `plan/gitmerge.md` (untracked) of decisions, conflicts, and fixes to avoid rework. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
