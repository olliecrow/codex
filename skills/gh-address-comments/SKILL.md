---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and address actionable comments autonomously, asking the user only for true blockers or ambiguous high-risk choices.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

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

## Preflight (must run first)

- Confirm repo context and branch state (`git rev-parse --show-toplevel`, `git symbolic-ref -q --short HEAD`).
- Confirm `gh` availability/auth (`command -v gh`, `gh auth status`).
- If detached HEAD or branch PR lookup fails, retry with explicit `--repo <owner>/<repo>` and current branch metadata before requesting a PR number/URL.
- Verify referenced paths exist before reading/writing helper outputs.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR
- If branch-based PR discovery fails, retry with explicit `--repo <owner>/<repo>` and PR identifier.
- If the script fails due to `gh` JSON schema drift, rerun with a reduced field set and continue.

## 2) Triage comments autonomously
- Number all review threads/comments and classify each as: `address now`, `already addressed`, `not worth addressing` (with rationale), or `blocked`.
- Default to addressing all high-confidence in-scope comments without waiting for user selection.
- Ask a minimal user question only when a comment implies an ambiguous high-risk behavior change that cannot be resolved from code/tests/docs.

## 3) Apply fixes and verify
- Apply fixes for all `address now` comments in focused batches.
- Run relevant checks/tests after each batch, then re-fetch comments to confirm dispositions.
- Keep looping until no actionable in-scope comments remain or a true blocker is identified.

## 4) Refresh active PR metadata (always)
- Check whether the current branch has an active PR.
- Compare PR title/body against the branch intent and actual delta after addressed comments.
- If title/body are stale or incomplete, update them (for example with `gh pr edit --title ... --body-file ...`).
- If the active PR is draft and the branch is review-ready, promote it (for example with `gh pr ready <pr-number-or-url>`).
- If no active PR exists, state that explicitly and continue.

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
- Treat `Unknown JSON field` as schema drift and reduce requested fields before failing.
- Treat `Not Found (404)` as repo/PR mismatch first; validate `--repo` and PR identity.
