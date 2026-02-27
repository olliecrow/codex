---
name: git-review
description: Deep review of a branch vs main with top-priority focus on critical red flags and serious issues before merge. Use when asked to assess readiness to merge or to audit differences for red flags.
---

# git-review

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

Compare the current branch against main, analyze each change's intent and risk, and hunt for critical red flags before merge. If the branch has an open PR, incorporate all PR comments and interactions into the review. PR comments are inputs, not gospel. Conduct a deep, thorough review that covers every change and decision end-to-end.
When PR feedback surfaces high-confidence issues worth action, investigate deeply, add them to the plan, execute fixes, and verify outcomes before finalizing the verdict.
Priority order for this skill is mandatory: identify and resolve critical red flags and serious issues first, then review secondary concerns.

## Scoped review mode (must support)

When the user requests a focused review (for example: `prewarm`, `normalization`, `eval`, or a specific module), run in scoped mode:

- Build a concrete scope map first (files, directories, symbols, tests, and config paths tied to the requested area).
- Review all in-scope files/hunks end-to-end with the same severity-first standard as full mode.
- Review boundary files where scoped code integrates with the rest of the system (callers, shared utilities, config wiring, and output consumers).
- Explicitly label findings as `in-scope` or `boundary`.
- Do not silently claim full branch coverage in scoped mode.
- If user requests full-branch review, use standard full mode.

## Trigger phrases

Use this skill when the user asks for review intents like:
- `review this branch`
- `critical red flags`
- `serious issues`
- `is this ready to merge`
- `review <area> specifically` (scoped mode)

Mode hinting:
- use `full` mode for whole-branch readiness.
- use `scoped` mode for targeted areas (for example `prewarm`, `normalization`, `eval`, `multiagent`).

## Prompt templates

Use these copy-paste templates:
- `[$git-review] full branch review vs main for critical red flags and serious issues. findings first by severity.`
- `[$git-review] scoped review: prewarm + boundary files only. focus on critical red flags/serious issues first.`
- `[$git-review] scoped review: normalization path + boundary wiring; explicitly list out-of-scope files not reviewed.`
- `[$git-review] full review then fix high-confidence issues, verify, and re-review until no material findings remain.`

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Default write scope is the current `cwd` and its subdirectories.
- Read-only inspection outside the current `cwd` is allowed when needed for context; do not modify outside the `cwd` tree unless the user explicitly requests it.
- Run a preflight before substantial work: confirm you are at the repo root, verify `git`/required tools with `command -v`, and verify expected refs/remotes before diff/review commands.
- Do not assume intent; if multiple interpretations exist, state them explicitly.
- Prefer the simplest explanation for a change and verify it against evidence.
- Keep review scope surgical: every comment should trace to a specific change.
- Treat critical red flags and serious issues as the top review objective; investigate them first and report them first.
- Define explicit readiness criteria and verify them before concluding.
- For public/open-source repos, run an explicit safety pass for secrets, sensitive data, and local system paths in code, docs, PR text, comments, and commit metadata.
- If a PR exists, treat review comments and discussion as required inputs (not gospel); investigate each item deeply and determine whether it is addressed, out of scope, or worth action.
- At the end of the review, check whether the branch has an active PR and update title/body when metadata no longer matches the branch delta.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
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

When you recommend or make a fix, or reach an important decision, ensure the "why" is captured in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded or call out gaps.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing docs when they have a clear home, but create new focused docs/subdirectories when it improves navigability (and link them from related docs or indexes).
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Select review mode:
   - Determine whether this is `full` or `scoped` from the user request.
   - For scoped mode, write a scope map before diff analysis (requested area, mapped files, boundary files).
   - If scope is ambiguous, infer the smallest defensible scope and state assumptions clearly.
   - Keep severity bar identical to full mode.

2. Sync remote main before anything else:
   - Run preflight checks first (`git rev-parse --show-toplevel`, `git remote -v`, and required tool availability).
   - Fetch the most recent `origin/main` before any other steps (do not checkout, merge, or rebase).
   - If the repo uses a different mainline (for example, `master`), fetch that instead.
   - If the update cannot be fetched, run bounded retries and mainline fallbacks (`origin/master`, local mainline refs); proceed with local refs if needed and only ask if no valid comparison base exists.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue with available evidence, and mark dependent checks as pending until command results are available.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Gather PR context when applicable:
   - Determine whether the current branch has an open PR (prefer `gh pr view --json number,url,comments,reviews,reviewDecision`).
   - If the preferred JSON query fails due unsupported fields/version drift, retry with a minimal query (`gh pr view --json number,url`) and gather comments/reviews via additional supported calls (`gh pr view --comments`, `gh pr view --json reviews`).
   - If `gh` is unavailable or unauthenticated, continue branch-vs-main review without PR context, then request PR URL/number only if unresolved PR-specific risk remains.
   - Collect all PR interactions: review comments, review summaries, issue comments, and relevant status-check notes.
   - Treat PR feedback as inputs to investigate, not instructions to blindly apply.

4. Establish diff scope:
   - Compare current branch to main (or the branch it diverged from).
   - Enumerate all changed files and hunks.
   - In full mode, always conduct a full review of every changed file and hunk.
   - In scoped mode, review every in-scope and boundary hunk from the scope map; explicitly list out-of-scope files not reviewed.
   - If diffs are large, start with `git diff --stat` or `git diff --name-only` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue analysis on available local context, and mark any blocked verification explicitly.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

5. Understand intent:
   - For each change, identify the rationale, intent, and expected impact.
   - Flag unclear or unjustified changes for deeper scrutiny.

6. Deep risk review:
   - Top priority: aggressively hunt for critical red flags and serious issues (correctness, security, data loss, severe regressions) before anything else.
   - Look for critical red flags, regressions, security risks, data loss, perf issues, or correctness bugs.
   - Consider long-term maintainability and hidden coupling.
   - Ensure anything that worked on main still works here; flag removed or degraded functionality and verify intended parity.

7. Investigate thoroughly:
   - Proactively create and run experiments, trial runs, or tests as needed.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - After any changes or fixes, rerun relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

8. Triage PR feedback:
   - Enumerate every PR comment and interaction; for each, decide one of: addressed, not worth addressing (with rationale), or needs action.
   - For each item that needs action, investigate deeply to confirm root cause and expected impact.
   - Build a plan that preserves intent, minimizes risk, and links back to the specific feedback.
   - Flesh out the plan with concrete steps, dependencies, and verification.
   - Execute high-confidence, in-scope fixes and run relevant verification checks before closing the review.
   - Re-classify each acted-on item as addressed only after evidence-backed verification.

9. Handle huge diffs without skipping coverage:
   - In full mode, still review all changes end-to-end; do not sample or skip files.
   - In scoped mode, still review all in-scope and boundary changes end-to-end; do not sample or skip mapped scope files.
   - Break the review into batches (by directory, feature, or risk area) and track progress in `plan/current/git-review.md`. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - Use tooling to manage scale (e.g., `git diff --stat`, `git diff --numstat`, per-file diffs, and focused searches) but ensure every file and hunk in the active review scope is covered.
   - If time or compute constraints appear, continue autonomously with phased full-coverage passes and explicit progress checkpoints; ask the user only if hard environment limits prevent completion.

10. Produce a full change plan:
   - Investigate each potential change one by one and state whether it is high‑confidence/conviction, optional, or not worth doing.
   - Consolidate all items that should change into a final, ordered plan (even if the verdict is Ready).
   - For each plan item, include scope, rationale, dependencies, and verification steps.
   - Summarize PR comment triage with dispositions and link each planned and executed item to the originating comment when applicable.
   - Distinguish executed-and-verified fixes from deferred items, and justify any deferrals.
   - Note required fixes before merge and provide a merge readiness assessment and next steps.
   - In the final review output, present findings first and order them by severity with critical red flags and serious issues at the top.
   - Use a concise verdict template: Ready / Needs fixes / Blocked.
   - On repeated passes, continue deeper review and append net-new findings; avoid repeating prior summaries unless needed for traceability.
   - Write the report in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

11. Refresh active PR metadata:
   - Check whether the current branch has an active PR.
   - If yes, compare PR title/body against the reviewed branch intent and actual delta after any fixes.
   - If title/body are stale or incomplete, update them (for example with `gh pr edit --title ... --body-file ...`).
   - If the active PR is draft and the branch is review-ready, promote it (for example with `gh pr ready <pr-number-or-url>`).
   - If no active PR exists, state that explicitly and continue.

12. Repeat review-fix-verification passes until complete:
   - Re-run review passes after each batch of fixes.
   - Continue looping until no material findings remain unaddressed, verification is green, and merge readiness is clearly supported by evidence.
   - Only stop early when an explicit blocker is outside scope or requires user input under the "absolutely necessary" policy.
