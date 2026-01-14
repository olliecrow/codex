---
name: commit
description: Create small, well-described git commits and do not push. Use when asked to commit changes, split work into logical units, craft commit messages, or provide commit commands.
---

# Git Commit

## Overview

Create local commits only and do not push, preferring small, focused commits with clear messages.
If committing is prohibited by project or system instructions, state that you cannot commit and always provide the exact git commands needed; do not ask the user whether they want commands or a summary.

## Workflow

1. Inspect the repo state:
   - Check `git status -sb` for tracked and untracked files.
   - Review `git diff` and `git diff --staged` to understand changes.

2. Run pre-commit checks first:
   - If the repo defines pre-commit checks (config or standard script), run them before committing.
   - If no pre-commit checks are defined, skip this step.
   - Ensure pre-commit checks pass before committing.
   - If failures are small and reasonable to fix, fix them before committing.
   - This requirement applies even when you cannot commit and must output copy-pasteable git commands.

3. Split changes into logical units:
   - Prefer more, smaller commits over fewer large ones.
   - Keep each commit focused on a single purpose or area.
   - Treat unrelated untracked files as separate commits unless clearly part of the same change.

4. Stage and commit each unit:
   - Use `git add -p` or targeted `git add <paths>` to keep commits small.
   - Write concise, descriptive commit messages (imperative, present tense).
   - Do not push.

5. Fallback when you must not commit:
   - If committing is disallowed (e.g., project instructions forbid any git writing), explicitly state you cannot commit here.
   - Then output a single copy-pasteable block of git commands, without asking the user whether they want commands or a summary.
   - The block must contain only commands, one per line, in execution order, with no extra text between them.

6. If there are no changes to commit:
   - State that the working tree is clean and stop.
   - If called repeatedly, you may follow prior suggested next steps or start fresh; both are fine. Re-check the repo and continue only if new changes exist.
