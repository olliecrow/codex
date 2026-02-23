---
name: git-sync
description: Sync local git state to the latest remote branch state (`main`, current branch, or explicit target branch) with safe fast-forward behavior and clear verification.
---

# git-sync

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
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Safely sync local git state with the most recent remote state for one of:
- the current branch,
- the mainline branch (`main`/`master`), or
- an explicitly requested branch.

Default behavior is fast-forward only. Do not introduce merge commits during sync.

## Trigger phrases

Use this skill when the user intent matches phrases like:
- `git pull`
- `pull branch`
- `pull most recent remote main`
- `sync with upstream`
- `switch to most recent version of branch`

If the request is only synchronization and branch-state verification, prefer `git-sync` over broader git skills.

## Prompt templates

Use these copy-paste templates:
- `[$git-sync] sync current branch with upstream (ff-only) and verify branch/upstream/ahead-behind.`
- `[$git-sync] pull most recent remote main (ff-only) and report new HEAD commit.`
- `[$git-sync] sync explicit branch olliecrow/<branch-name> to latest remote state (ff-only).`
- `[$git-sync] verify we are on most recent remote <branch-name>; if blocked, return exact unblock commands.`

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm repo root, verify `git` with `command -v`, and confirm remote availability.
- Prefer `git fetch` + explicit fast-forward operations over implicit merges.
- If worktree has local modifications that block pull/checkout, preserve user changes and provide the safest next step instead of forcing.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Git safety and permissions

- Follow the current repo's git policy and the session's environment restrictions; if git writes are disallowed, do not perform them and provide commands instead.
- Never rewrite git history or force push. Do not use `git rebase`, `git commit --amend`, `git reset --hard`, `git reset --soft`, `git reset --mixed`, `git push --force`, `git push --force-with-lease`, or `git filter-branch`, or `git clean -fdx`.
- Use `--ff-only` for pull/sync operations.

## Workflow

1. Preflight:
   - Run `git rev-parse --show-toplevel`, `git status -sb`, `git remote -v`.
   - Detect default mainline (`origin/main`, fallback `origin/master`).
   - Capture current branch and its tracking branch.

2. Determine sync target mode:
   - `current-branch` when user says `git pull` or `pull branch`.
   - `mainline` when user says `pull most recent remote main` or equivalent.
   - `explicit-branch` when user names a remote branch.
   - If ambiguous, choose `current-branch` and state the assumption.

3. Fetch fresh remote state:
   - Run `git fetch --prune origin` (bounded retries on transient failure).
   - If fetch fails after retries, report blocker with exact failing command/output.

4. Apply sync safely:
   - `current-branch`: if tracking branch exists, run `git pull --ff-only`.
   - `mainline`: switch to detected mainline branch if needed, then run `git pull --ff-only origin <mainline>`.
   - `explicit-branch`: fetch branch, switch/create local tracking branch if needed, then pull with `--ff-only`.
   - If local changes block checkout/pull, do not stash/reset automatically; report safe options and continue with read-only verification where possible.

5. Verify sync outcome:
   - Report branch, upstream, and ahead/behind status (`git status -sb`).
   - Report new HEAD commit (`git log --oneline -n 1`) and whether local is aligned with upstream.

6. Output contract:
   - State mode used, target branch, and exact sync result.
   - If blocked, give one concise reason and exact unblock commands.
   - If git writes were not allowed, provide one copy-pasteable command block and mark sync pending.

## Repeat invocations

- Reuse the previous target mode unless the user changes it.
- Continue from current repo state; do not re-run unrelated diagnostics.
- If already up to date, report that explicitly and stop.
