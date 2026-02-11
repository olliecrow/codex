---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
---

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: immediately take the next highest-value in-scope action when it is clear.
- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material risk tradeoffs, missing required data/access, or destructive/irreversible actions outside policy.
- If blocked by command/tool/env failures, attempt high-confidence fallbacks autonomously before escalating (for example `rg` -> `find`/`grep`, `python` -> `python3`, alternate repo-native scripts).
- When the workflow uses `plan/`, ensure required plan directories exist before reading/writing them (create when edits are allowed; otherwise use an in-memory fallback and call it out).
- Treat transient external failures (network/SSH/remote APIs/timeouts) as retryable by default: run bounded retries with backoff and capture failure evidence before concluding blocked.
- On repeated invocations for the same objective, resume from prior findings/artifacts and prioritize net-new progress over rerunning identical work unless verification requires reruns.
- Drive work to complete outcomes with verification, not partial handoffs.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes. Example loops (adapt as needed, not rigid): issue-resolution `investigate -> plan -> fix -> verify -> battletest -> organise-docs -> git-commit -> re-review`; cleanup `scan -> prioritize -> clean -> verify -> re-scan`; docs `audit -> update -> verify -> re-audit`.
- Keep looping until actual completion criteria are met: no actionable in-scope items remain, verification is green, and confidence is high.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Never squash commits; always use merge commits when integrating branches.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Prerequisites

- Require GitHub CLI `gh`. Check `gh --version`. If missing, attempt a non-interactive install path available on the host (for example `brew`, `apt`, or existing repo bootstrap scripts), then re-check. Ask the user only if installation remains blocked.
- Require authenticated `gh` session. Run `gh auth status`. If unauthenticated, attempt token-based auth via `GH_TOKEN`/`GITHUB_TOKEN` when available, then re-check. Ask the user to run `gh auth login` only if auth remains blocked.

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
- If git push fails due to workflow auth errors, refresh from the tracked upstream (or the detected mainline branch) and retry the push once.
- If the branch has no active PR, open one in ready-for-review state: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --fill --head $(git branch --show-current)`.
- If the branch already has an active PR, do not create a duplicate; edit the existing PR instead.
- If the active PR is draft, promote it before finishing: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr ready $(git branch --show-current)`.
- Write the PR description to a temp file with real newlines (e.g. pr-body.md ... EOF) and run pr-body.md to avoid \\n-escaped markdown.
- PR description (markdown) must be detailed prose covering the issue, the cause and effect on users, the root cause, the fix, and any tests or checks used to validate.
- At the end, always compare the active PR title/body to the final branch delta and update stale metadata with `gh pr edit`.
