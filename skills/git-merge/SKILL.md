---
name: git-merge
description: Prepare the current branch to merge cleanly into main by ensuring a clean working tree, syncing with remote, understanding diffs and intent, planning safe changes, resolving conflicts, and verifying with battle tests.
---

# git-merge

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

Get the current branch to a merge-ready state with main by first understanding both branches in depth, then planning a careful integration that preserves functionality from each side. Do not rush into a merge: fully map how main has progressed and how the current branch diverges before changing anything. Treat integration as a potentially difficult, long‑thinking task; reason and plan deeply before executing any state‑changing git commands. Once the plan is validated, perform the required git operations to reach a fully merged state. Conduct a deep, thorough review of all diffs and decisions, and ensure functionality from both branches is preserved after the merge.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm you are at the repo root, verify `git`/required tools with `command -v`, and verify expected refs/remotes before state-changing commands.
- State assumptions explicitly; resolve intent from code/tests/docs/history first, and ask only when ambiguity remains materially risky.
- Prefer the simplest merge resolution that preserves intent on both sides; avoid extra refactors.
- Keep changes surgical and limited to merge needs; do not "improve" unrelated code.
- Define success criteria and verify after each meaningful step.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- At the end of the merge workflow, check whether the branch has an active PR and update title/body when metadata no longer matches the merged branch delta.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- Perform the merge when required without asking for permission; only stop to ask if there is ambiguity, missing information, or a risky decision that cannot be inferred.
- Never blindly accept default merge resolutions; inspect every conflict and ensure functionality from both branches is preserved.
- If the merge requires a commit, ensure pre-commit checks, relevant tests, and CI checks pass before committing.
- Default to preserving main’s functionality and changes; if there is a core functional conflict, prefer the current branch’s intent and document why.
- Treat doc merges as subjective: reconcile structure and wording carefully to produce the clearest, most accurate docs, not just a mechanical merge.
- Do not execute state‑changing git commands until a deep integration plan is complete and validated; once validated, execute the necessary commands to fully merge.
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

When you resolve a conflict, fix an issue, or make an important merge decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing docs when they have a clear home, but create new focused docs/subdirectories when it improves navigability (and link them from related docs or indexes).
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Sync remote main before anything else:
   - Run preflight checks first (`git rev-parse --show-toplevel`, `git remote -v`, and required tool availability).
   - Fetch the most recent `origin/main` before any other steps (do not checkout, merge, or rebase).
   - If the repo uses a different mainline (for example, `master`), fetch that instead.
   - If the update cannot be fetched, run bounded retries and mainline fallbacks (`origin/master`, local mainline refs); ask only if no valid merge base can be established.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue with read-only planning/analysis, and mark command-dependent merge actions as pending.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Require a clean working tree:
   - Check `git status -sb` next.
   - If there are unstaged or uncommitted changes, preserve them autonomously first (prefer checkpoint commit via `git-commit`; fallback to explicit non-destructive stash/branch safety step).
   - Ask only if safe preservation strategy is truly ambiguous or blocked by policy.

3. Sync the current branch with remote:
   - Fetch latest refs for the current branch.
   - Update the current branch from remote (pull or fast-forward) so it is up to date.
   - If remote update fails, retry with bounded backoff and explicit refspec fallback; ask only if branch state cannot be recovered safely.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue conflict-risk analysis, and mark branch-sync status as pending.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

4. Build a two‑sided understanding before merging:
   - Map main’s progression: what changed, why, and which functionality it introduces or modifies (`git diff HEAD..main`, `git log HEAD..main`).
   - Map the current branch: what changed, why, and which functionality it introduces or modifies (`git diff main...HEAD`, `git log main..HEAD`).
   - If diffs are large, start with `git diff --stat`/`--name-only` for both directions, then review per-file diffs.
   - Read key files to understand intent, behavior, and risk on both sides.
   - Produce an explicit mental (or `plan/`) map of overlapping areas, potential conflicts, and ownership.
   - Review every changed file and hunk; ensure no functionality from either branch is removed or degraded without explicit intent.

5. Plan the merge approach (before any state‑changing git commands):
   - Identify conflicts, risky areas, and order of operations.
   - Decide upfront how to preserve main’s changes and where branch intent must override due to core functional differences.
   - Call out doc-heavy areas and plan for editorial reconciliation rather than mechanical conflict resolution.
   - Develop a clear plan to address changes safely.
   - Think deeply and verify the plan is correct and low risk.
   - If there are critical open questions or unclear intent, attempt resolution from existing evidence first; ask only the minimal necessary clarifying questions when still blocked.
   - Use a `plan/` directory as scratch space if needed; create it only if permitted, keep it untracked, and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

6. Execute the merge:
   - Apply the plan step by step.
   - Before running merge commands, run pre-commit checks, tests, and CI checks on the current branch to establish a clean baseline; fix failures before proceeding.
   - Resolve conflicts carefully with reasoning aligned to main’s intent and the branch’s intent, preserving behavior from both.
   - Keep changes minimal and avoid introducing new behavior unless required by the plan.
   - Perform the merge directly when git operations can be executed here; do not ask for permission.
   - If git operations cannot be executed here, provide explicit commands and continue with any remaining non-state-changing validation/planning/reporting steps.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

7. Verify and battle test:
   - Validate that the merge completed cleanly and the working tree is consistent.
   - Run relevant checks/tests, starting small and expanding to broader coverage.
   - Run CI checks (or their local equivalents) and wait for success before completing the merge.
   - If the merge results in a commit, ensure pre-commit checks, tests, and CI checks pass before committing.
   - Battle test to catch regressions, edge cases, or integration issues.
   - Explicitly confirm that functionality present on both branches still works; flag any regressions or removals.
   - After any fixes, re-run the smallest relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - If failures appear, fix and re-test until green.

8. Summarize:
   - Confirm merge readiness and note any remaining risks or follow-ups.
   - Write in plain, concise, and intuitive language with brief context.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

9. Refresh active PR metadata:
   - Check whether the current branch has an active PR.
   - If yes, compare PR title/body against the merged branch intent and actual delta.
   - If title/body are stale or incomplete, update them (for example with `gh pr edit --title ... --body-file ...`).
   - If the active PR is draft and the branch is review-ready, promote it (for example with `gh pr ready <pr-number-or-url>`).
   - If no active PR exists, state that explicitly and continue.

## Repeat invocations

- If called multiple times, avoid repeating the same probes or tests unless verifying a fix.
- Expand coverage gradually: re-check diffs after updates, deepen review of conflicted areas, or add broader tests if risk warrants it.
- Keep a lightweight log in `plan/current/git-merge.md` (untracked) of decisions, conflicts, and fixes to avoid rework. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
