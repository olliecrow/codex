---
name: git-review
description: Deep review of a branch vs main to find critical issues before merge. Use when asked to assess readiness to merge or to audit differences for red flags.
---

# git-review

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

Compare the current branch against main, analyze each change's intent and risk, and hunt for critical red flags before merge. If the branch has an open PR, incorporate all PR comments and interactions into the review. Conduct a deep, thorough review that covers every change and decision end-to-end.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm you are at the repo root, verify `git`/required tools with `command -v`, and verify expected refs/remotes before diff/review commands.
- Do not assume intent; if multiple interpretations exist, state them explicitly.
- Prefer the simplest explanation for a change and verify it against evidence.
- Keep review scope surgical: every comment should trace to a specific change.
- Define explicit readiness criteria and verify them before concluding.
- If a PR exists, treat review comments and discussion as required inputs (not gospel); investigate each item deeply and determine whether it is addressed, out of scope, or worth action.
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
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Sync remote main before anything else:
   - Run preflight checks first (`git rev-parse --show-toplevel`, `git remote -v`, and required tool availability).
   - Fetch the most recent `origin/main` before any other steps (do not checkout, merge, or rebase).
   - If the repo uses a different mainline (for example, `master`), fetch that instead.
   - If the update cannot be fetched, stop and ask for guidance.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Gather PR context when applicable:
   - Determine whether the current branch has an open PR (prefer `gh pr view --json number,url,reviewThreads,comments,reviews`).
   - If `gh` is unavailable or unauthenticated, ask the user for the PR URL/number or a comment dump; do not proceed without PR context if one exists.
   - Collect all PR interactions: review comments, review summaries, issue comments, and relevant status-check notes.
   - Treat PR feedback as inputs to investigate, not instructions to blindly apply.

3. Establish diff scope:
   - Compare current branch to main (or the branch it diverged from).
   - Enumerate all changed files and hunks.
   - Always conduct a full review of every changed file and hunk.
   - If diffs are large, start with `git diff --stat` or `git diff --name-only` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat`, `git diff --name-only`, or per-file diffs instead of unbounded commands.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

4. Understand intent:
   - For each change, identify the rationale, intent, and expected impact.
   - Flag unclear or unjustified changes for deeper scrutiny.

5. Deep risk review:
   - Look for critical red flags, regressions, security risks, data loss, perf issues, or correctness bugs.
   - Consider long-term maintainability and hidden coupling.
   - Ensure anything that worked on main still works here; flag removed or degraded functionality and verify intended parity.

6. Investigate thoroughly:
   - Proactively create and run experiments, trial runs, or tests as needed.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - After any changes or fixes, rerun relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

7. Triage PR feedback:
   - Enumerate every PR comment and interaction; for each, decide one of: addressed, not worth addressing (with rationale), or needs action.
   - For each item that needs action, build a plan that preserves intent, minimizes risk, and links back to the specific feedback.
   - Flesh out the plan with concrete steps, dependencies, and verification.

8. Handle huge diffs without skipping coverage:
   - Still review all changes end-to-end; do not sample or skip files.
   - Break the review into batches (by directory, feature, or risk area) and track progress in `plan/current/git-review.md`. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - Use tooling to manage scale (e.g., `git diff --stat`, `git diff --numstat`, per-file diffs, and focused searches) but ensure every file and hunk is covered.
   - If time or compute constraints make a full review impractical, ask the user for a time budget or additional constraints, but keep the full-review requirement explicit.

9. Produce a full change plan:
   - Investigate each potential change one by one and state whether it is high‑confidence/conviction, optional, or not worth doing.
   - Consolidate all items that should change into a final, ordered plan (even if the verdict is Ready).
   - For each plan item, include scope, rationale, dependencies, and verification steps.
   - Summarize PR comment triage with dispositions and link each planned item to the originating comment when applicable.
   - Note required fixes before merge and provide a merge readiness assessment and next steps.
   - Use a concise verdict template: Ready / Needs fixes / Blocked.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue deeper review and append new findings rather than repeating prior summaries.
   - Write the report in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
