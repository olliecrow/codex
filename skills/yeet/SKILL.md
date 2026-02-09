---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
---

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Prerequisites

- Require GitHub CLI `gh`. Check `gh --version`. If missing, ask the user to install `gh` and stop.
- Require authenticated `gh` session. Run `gh auth status`. If not authenticated, ask the user to run `gh auth login` (and re-run `gh auth status`) before continuing.

## Naming conventions

- Branch: `olliecrow/{description}` when starting from main/master/default.
- Commit: `{description}` (terse).
- PR title: `{description}` summarizing the full diff.

## Workflow

- If on main/master/default, create a branch: `git checkout -b "olliecrow/{description}"`
- Otherwise stay on the current branch.
- Confirm status, then stage everything: `git status -sb` then `git add -A`.
- Run pre-commit checks, tests, and CI checks before committing.
  - If pre-commit config exists, run it.
  - Run the smallest relevant test targets; all tests must pass.
  - Run CI checks or local equivalents; if CI can only run remotely, trigger it and wait for success before proceeding.
  - If checks fail due to missing deps/tools, install dependencies and rerun once.
- Commit tersely with the description: `git commit -m "{description}"`
- Push with tracking: `git push -u origin $(git branch --show-current)`
- If git push fails due to workflow auth errors, pull from master and retry the push.
- If the branch has no active PR (open draft or ready-for-review), open one: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`.
- If the branch already has an active PR (open draft or ready-for-review), do not create a duplicate; edit the existing PR instead.
- Write the PR description to a temp file with real newlines (e.g. pr-body.md ... EOF) and run pr-body.md to avoid \\n-escaped markdown.
- PR description (markdown) must be detailed prose covering the issue, the cause and effect on users, the root cause, the fix, and any tests or checks used to validate.
- At the end, always compare the active PR title/body to the final branch delta and update stale metadata with `gh pr edit`.
