---
name: git-commit
description: Commit all current uncommitted changes into small, logical commits with clear messages. Do not push. Use when asked to commit everything in the working tree.
---

# Gitcommit

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
- Do not create any commit until all applicable pre-commit checks, tests, and CI checks have been run and passed.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- Treat active-PR title/body updates as in-scope for this skill: if the branch has an active PR and metadata drift is detected, update it.
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
   - If `origin/main` does not exist, detect alternate mainline refs (`origin/master`, upstream default branch, or local mainline) and continue; ask only if no valid baseline can be established.
   - If git operations can be executed here, run them directly; otherwise, output explicit commands, continue prep/analysis, and mark command-result-dependent steps as pending.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Inspect repo state:
   - Check `git status -sb`.
   - Review `git diff`, `git diff --staged`, and `git diff --name-only` to understand all changes (tracked and untracked).
   - If diffs are large, start with `git diff --stat` and then review per-file diffs.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue packaging logical commit units, and mark any unresolved staging status as pending.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Run pre-commit checks first:
   - If the repo defines pre-commit checks (config or standard script), run them before committing.
   - If any skill definitions or skill scripts changed (for example `skills/*/SKILL.md` or `skills/*.py`), run `python3 "${CODEX_HOME:-$HOME/.codex}/skills/validate_skills.py"` and require a passing result before committing.
   - If no pre-commit checks are defined, skip this step.
   - Ensure pre-commit checks pass before committing.
   - If failures are small and reasonable to fix, fix them before committing.
   - This requirement applies even when you cannot commit and must output copy-pasteable git commands.

4. Run tests (or the most relevant subset) before committing:
   - Prefer the smallest relevant test target(s) when full test suites are too heavy.
   - Ensure tests pass before committing.
   - If tests cannot run here due hard blockers, capture exact blocker evidence and provide exact commands for later execution; commit only when verification evidence is available per policy.

5. Run CI checks before committing:
   - If CI scripts or workflow equivalents are available locally, run them.
   - If CI can only run remotely, trigger it and wait for success before committing; if triggering is impossible here, provide exact commands and mark commit as blocked pending CI evidence.
   - Ensure CI checks pass before committing.
   - This requirement applies even when you cannot commit and must output copy-pasteable git commands.

6. Split changes into logical units:
   - Prefer many small commits over fewer large ones.
   - Keep each commit focused on a single purpose or area with a clear rationale.
   - Treat unrelated untracked files as separate commits unless clearly part of the same change.
   - Ensure commit order and packaging make sense (foundational changes first, dependent changes after).
   - If a simpler split achieves the same clarity, choose the simpler split.

7. Stage and commit each unit:
   - Use explicit `git add <paths>` commands (avoid interactive staging by default).
   - Use `git commit -m "..."` with concise, descriptive, imperative messages tailored to each change.
   - Each commit should stand on its own as a logical, best-practice change that can be understood and reverted independently.
   - Order commits so they read as a coherent sequence with minimal backtracking or cross-dependencies.
   - If git operations can be executed here, run them directly; otherwise, provide explicit commands and continue with the remaining actionable preparation/reporting steps without waiting.
   - Do not push.

8. Ensure nothing appropriate is left uncommitted:
   - Re-check `git status -sb` and confirm the working tree is clean.
   - If any files that should be committed remain, create additional commits until the tree is clean.

9. Refresh active PR metadata:
   - Check whether the current branch has an active PR.
   - If yes, compare PR title/body against the current branch intent and the actual delta.
   - If title/body are stale or incomplete after additional changes, update them (for example with `gh pr edit --title ... --body-file ...`).
   - If the active PR is draft and the branch is review-ready, promote it (for example with `gh pr ready <pr-number-or-url>`).
   - If no active PR exists, state that explicitly and continue.

10. If committing is disallowed:
   - State that you cannot commit here.
   - Provide a single copy-pasteable block of git commands that will stage and commit all changes in logical units.
   - The block must contain only commands, one per line, in execution order, with no extra text between them.
   - Do not ask the user whether they want commands or a summary.

11. If there are no changes to commit:
   - State that the working tree is clean and stop.
   - In repeated invocations, re-check the repo and continue autonomously when new commit-eligible changes exist.

## Repeat invocations

- If called multiple times, only commit newly added changes.
- Avoid recombining prior commits; do not rewrite history.
- Continue committing eligible new changes in small logical batches until no commit-eligible changes remain.
