---
name: git-summary
description: Analyze current branch vs main, understand all diffs and intent, and produce a concise lower-case bullet list suitable for a PR summary, including nuances and gotchas.
---

# git-summary

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

## Overview

Produce a precise, lower-case PR summary by fully understanding how the current branch differs from main. Conduct a deep, thorough review of all diffs so every change and decision is understood and reasoned through before summarizing.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Do not assume intent or fill gaps; call out uncertainty if needed.
- Prefer the simplest summary that covers the actual changes; avoid speculative detail.
- Keep scope surgical: every bullet must map to a specific change.
- At the end of the workflow, check whether the branch has an active PR and update title/body if metadata is stale.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Git safety and permissions

- Follow the current repo's git policy and the session's environment restrictions; if git writes or pushes are disallowed, do not perform them and provide commands instead.
- Never rewrite git history or force push. Do not use `git rebase`, `git commit --amend`, `git reset --hard`, `git reset --soft`, `git reset --mixed`, `git push --force`, `git push --force-with-lease`, or `git filter-branch`, or `git clean -fdx`.

## Rationale capture

If changes include issue fixes or key decisions, confirm the rationale is captured in a durable place (code comments, docs, ADR, or tests). If it is missing, call that out as a gap in the PR summary.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Sync remote main before anything else:
   - Fetch the most recent `origin/main` before any other steps (do not checkout, merge, or rebase).
   - If the repo uses a different mainline (for example, `master`), fetch that instead.
   - If the update cannot be fetched, run bounded retries and fallback to local mainline refs; ask only if no valid comparison base can be established.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue with available local context, and mark any missing upstream evidence explicitly.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

2. Establish baseline:
   - Confirm repo root and current branch.
   - Determine the main branch name (main/master) and verify it exists locally.

3. Gather diffs and context:
   - Compare branch vs main (e.g., `git diff main...HEAD` and `git log main..HEAD`).
   - If diffs are large, start with `git diff --stat main...HEAD` or `git diff --name-only main...HEAD` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat main...HEAD`, `git diff --name-only main...HEAD`, or per-file diffs instead of unbounded commands.
   - Review file-level changes and key hunks to understand intent.
   - Review every changed file and hunk; do not skip any relevant changes.
   - Read related docs or comments if they explain why changes were made.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands, continue summarization from available diffs, and note which parts depend on pending command output.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

4. Understand intent and impact:
   - Map changes to user-facing behavior, APIs, data, config, or ops.
   - Note any risk areas, edge cases, or migration considerations.
   - Identify tests added/updated and gaps if any are missing.
   - Call out removed or degraded functionality compared to main when relevant.

5. Summarize for PR:
   - Output a very concise bullet list suitable for a PR summary.
   - Use lower-case text only.
   - Use very simple language; avoid complex words and jargon.
   - Return the summary as a copy-pasteable block of bullets with no extra commentary.
   - End every bullet with a full stop.
   - Never use semicolons; keep punctuation simple.
   - Wrap relevant identifiers in backticks (paths, files, branches, commands, flags, test names, and config keys) so they render cleanly in pr comments.
   - Include important nuances, gotchas, and details others should know.
   - Write in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

6. Refresh active PR metadata:
   - Check whether the current branch has an active PR.
   - If yes, compare PR title/body against the actual branch delta and generated summary.
   - If title/body are stale or incomplete, update them (for example with `gh pr edit --title ... --body-file ...`).
   - If the active PR is draft and the branch is review-ready, promote it (for example with `gh pr ready <pr-number-or-url>`).
   - If no active PR exists, state that explicitly and continue.
