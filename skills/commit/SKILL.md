---
name: commit
description: Create small, well-described git commits and do not push. Use when asked to commit changes, split work into logical units, craft commit messages, or provide commit commands.
---

# Git Commit

## Overview

Create local commits only and do not push, preferring small, focused commits with clear messages.
If committing is prohibited by project or system instructions, state that you cannot commit and always provide the exact git commands needed; do not ask the user whether they want commands or a summary.

## Behavioral guardrails (must follow)

- State assumptions explicitly; if commit grouping or intent is unclear, ask.
- Keep commits minimal and directly tied to the request; do not include unrelated changes.
- Prefer the simplest commit structure that preserves logical separation.
- Do not create any commit until all applicable pre-commit checks and tests have been run and passed.
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

Before committing, ensure that any issue fixes or key decisions are documented in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. If the rationale is not captured yet, add it before creating commits and mention where it was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Sync remote main before anything else:
   - Pull the most recent `origin/main` before any other steps.
   - If `origin/main` does not exist or the update cannot be applied safely, stop and ask for guidance.
   - If git operations can be executed here, run them directly; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Inspect the repo state:
   - Check `git status -sb` for tracked and untracked files.
   - Review `git diff` and `git diff --staged` to understand changes.
   - If diffs are large, start with `git diff --stat` or `git diff --name-only` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - Do this before any commit operations.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Run pre-commit checks first:
   - If the repo defines pre-commit checks (config or standard script), run them before committing.
   - If no pre-commit checks are defined, skip this step.
   - Ensure pre-commit checks pass before committing.
   - If failures are small and reasonable to fix, fix them before committing.
   - This requirement applies even when you cannot commit and must output copy-pasteable git commands.

4. Run tests (or the most relevant subset) before providing git commands:
   - Prefer the smallest relevant test target(s) when full test suites are too heavy.
   - Ensure tests pass before committing.
   - If tests cannot be run here, say so and request the user to run them and confirm results before you provide any git commands.

5. Split changes into logical units:
   - Prefer more, smaller commits over fewer large ones; uncommitted changes can (and often should) be split into multiple commits when it makes sense.
   - Keep each commit focused on a single purpose or area with a clear rationale.
   - Treat unrelated untracked files as separate commits unless clearly part of the same change.
   - Ensure commit order and packaging make sense (foundational changes first, dependent changes after).
   - It is fine (and encouraged) to spend time reasoning, investigating, and considering the change set before deciding what each commit should encapsulate and what the best commit messages should be.

6. Stage and commit each unit:
   - Primarily use/return/print explicit `git add <paths>` commands (avoid interactive staging by default).
   - Primarily use/return/print `git commit -m "..."` commands with concise, descriptive, bespoke messages (imperative, present tense) tailored to the exact change.
   - Each commit should stand on its own as a logical, best-practice change that can be understood and reverted independently.
   - Order commits so they read as a coherent sequence with minimal backtracking or cross-dependencies.
   - Do not push.
   - If git operations can be executed here, run them directly; otherwise, provide explicit commands and pause until the user reports back.

7. Verify nothing remains unstaged that should be committed:
   - Re-check `git status -sb` at the very end and explicitly confirm the working tree is clean.
   - Ensure there are no unstaged or uncommitted files at the end of the commit sequence.
   - If any files that should have been committed remain unstaged or uncommitted, include them in a follow-up commit (or add the missing commands to the provided block).

8. Fallback when you must not commit:
   - If committing is disallowed (e.g., project instructions forbid any git writing), explicitly state you cannot commit here.
   - Then output a single copy-pasteable block of git commands, without asking the user whether they want commands or a summary.
   - The block must contain only commands, one per line, in execution order, with no extra text between them.
   - Prefer `git add <paths>` and `git commit -m "..."` commands in that block.

9. If there are no changes to commit:
   - State that the working tree is clean and stop.
   - If called repeatedly, you may follow prior suggested next steps or start fresh; both are fine. Re-check the repo and continue only if new changes exist.
