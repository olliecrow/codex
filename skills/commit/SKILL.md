---
name: commit
description: Create small, well-described git commits and do not push. Use when asked to commit changes, split work into logical units, craft commit messages, or provide commit commands.
---

# Git Commit

## Overview

Create local commits only and do not push, preferring small, focused commits with clear messages.
If committing is prohibited by project or system instructions, state that you cannot commit and always provide the exact git commands needed; do not ask the user whether they want commands or a summary.

## Workflow

1. Inspect the repo state first:
   - Check `git status -sb` for tracked and untracked files.
   - Review `git diff` and `git diff --staged` to understand changes.
   - Do this before any other steps.
   - If git operations can be executed here, run them directly; otherwise, output explicit commands and wait for results before continuing.

2. Run pre-commit checks first:
   - If the repo defines pre-commit checks (config or standard script), run them before committing.
   - If no pre-commit checks are defined, skip this step.
   - Ensure pre-commit checks pass before committing.
   - If failures are small and reasonable to fix, fix them before committing.
   - This requirement applies even when you cannot commit and must output copy-pasteable git commands.

3. Run tests (or the most relevant subset) before providing git commands:
   - Prefer the smallest relevant test target(s) when full test suites are too heavy.
   - Ensure tests pass before committing.
   - If tests cannot be run here, say so and request the user to run them and confirm results before you provide any git commands.

4. Split changes into logical units:
   - Prefer more, smaller commits over fewer large ones.
   - Keep each commit focused on a single purpose or area.
   - Treat unrelated untracked files as separate commits unless clearly part of the same change.
   - Ensure commit order and packaging make sense (foundational changes first, dependent changes after).
   - It is fine (and encouraged) to spend time reasoning, investigating, and considering the change set before deciding what each commit should encapsulate and what the best commit messages should be.

5. Stage and commit each unit:
   - Primarily use/return/print explicit `git add <paths>` commands (avoid interactive staging by default).
   - Primarily use/return/print `git commit -m "..."` commands with concise, descriptive, bespoke messages (imperative, present tense) tailored to the exact change.
   - Each commit should stand on its own as a logical, best-practice change that can be understood and reverted independently.
   - Order commits so they read as a coherent sequence with minimal backtracking or cross-dependencies.
   - Do not push.
   - If git operations can be executed here, run them directly; otherwise, provide explicit commands and pause until the user reports back.

6. Verify nothing remains unstaged that should be committed:
   - Re-check `git status -sb` at the very end and explicitly confirm the working tree is clean.
   - Ensure there are no unstaged or uncommitted files at the end of the commit sequence.
   - If any files that should have been committed remain unstaged or uncommitted, include them in a follow-up commit (or add the missing commands to the provided block).

7. Fallback when you must not commit:
   - If committing is disallowed (e.g., project instructions forbid any git writing), explicitly state you cannot commit here.
   - Then output a single copy-pasteable block of git commands, without asking the user whether they want commands or a summary.
   - The block must contain only commands, one per line, in execution order, with no extra text between them.
   - Prefer `git add <paths>` and `git commit -m "..."` commands in that block.

8. If there are no changes to commit:
   - State that the working tree is clean and stop.
   - If called repeatedly, you may follow prior suggested next steps or start fresh; both are fine. Re-check the repo and continue only if new changes exist.
