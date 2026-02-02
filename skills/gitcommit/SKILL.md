---
name: gitcommit
description: Commit all current uncommitted changes into small, logical commits with clear messages. Do not push. Use when asked to commit everything in the working tree.
---

# Gitcommit

## Overview

Commit all appropriate uncommitted changes (including relevant untracked files) into many small, logical commits with descriptive messages. Do not push. End with no changes that should be committed left uncommitted.
If committing is prohibited by project or system instructions, state that you cannot commit and always provide the exact git commands needed; do not ask the user whether they want commands or a summary.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- State assumptions explicitly; choose a reasonable grouping without asking and note assumptions in the summary.
- Keep commits minimal and directly tied to the request; do not include unrelated changes.
- Prefer the simplest commit structure that preserves logical separation; avoid bundling unrelated changes.
- Keep changes surgical: do not add unrelated edits just to "clean up."
- Define success criteria (clean working tree) and verify before finishing.
- If multiple interpretations of how to split commits exist, pick the simplest split that preserves logical separation and state why.
- Do not add new features, refactors, or formatting changes solely to "make the commit nicer."
- If you must adjust code to capture rationale or fix small issues discovered during review, keep it minimal and directly tied to the request.
- Do not create any commit until all applicable pre-commit checks and tests have been run and passed.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Git safety and permissions

- Follow the current repo's git policy and the session's environment restrictions; if git writes or commits are disallowed, do not perform them and provide commands instead.
- Never rewrite git history or force push. Do not use `git rebase`, `git commit --amend`, `git reset --hard`, `git reset --soft`, `git reset --mixed`, `git push --force`, `git push --force-with-lease`, or `git filter-branch`, or `git clean -fdx`.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

Before committing, ensure that any issue fixes or key decisions are documented in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. If rationale is missing, add it before committing and mention where it was captured.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Sync remote main before anything else:
   - Fetch the most recent `origin/main` before any other steps (do not checkout, merge, or rebase).
   - If `origin/main` does not exist, stop and ask for guidance.
   - If git operations can be executed here, run them directly; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Inspect repo state:
   - Check `git status -sb`.
   - Review `git diff`, `git diff --staged`, and `git diff --name-only` to understand all changes (tracked and untracked).
   - If diffs are large, start with `git diff --stat` and then review per-file diffs.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Run pre-commit checks first:
   - If the repo defines pre-commit checks (config or standard script), run them before committing.
   - If no pre-commit checks are defined, skip this step.
   - Ensure pre-commit checks pass before committing.
   - If failures are small and reasonable to fix, fix them before committing.
   - This requirement applies even when you cannot commit and must output copy-pasteable git commands.

4. Run tests (or the most relevant subset) before committing:
   - Prefer the smallest relevant test target(s) when full test suites are too heavy.
   - Ensure tests pass before committing.
   - If tests cannot be run here, say so and request the user to run them and confirm results before proceeding.

5. Split changes into logical units:
   - Prefer many small commits over fewer large ones.
   - Keep each commit focused on a single purpose or area with a clear rationale.
   - Treat unrelated untracked files as separate commits unless clearly part of the same change.
   - Ensure commit order and packaging make sense (foundational changes first, dependent changes after).
   - If a simpler split achieves the same clarity, choose the simpler split.

6. Stage and commit each unit:
   - Use explicit `git add <paths>` commands (avoid interactive staging by default).
   - Use `git commit -m "..."` with concise, descriptive, imperative messages tailored to each change.
   - Each commit should stand on its own as a logical, best-practice change that can be understood and reverted independently.
   - Order commits so they read as a coherent sequence with minimal backtracking or cross-dependencies.
   - If git operations can be executed here, run them directly; otherwise, provide explicit commands and pause until the user reports back.
   - Do not push.

7. Ensure nothing appropriate is left uncommitted:
   - Re-check `git status -sb` and confirm the working tree is clean.
   - If any files that should be committed remain, create additional commits until the tree is clean.

8. If committing is disallowed:
   - State that you cannot commit here.
   - Provide a single copy-pasteable block of git commands that will stage and commit all changes in logical units.
   - The block must contain only commands, one per line, in execution order, with no extra text between them.
   - Do not ask the user whether they want commands or a summary.

9. If there are no changes to commit:
   - State that the working tree is clean and stop.
   - If called repeatedly, you may follow prior suggested next steps or start fresh; both are fine. Re-check the repo and continue only if new changes exist.

## Repeat invocations

- If called multiple times, only commit newly added changes.
- Avoid recombining prior commits; do not rewrite history.
