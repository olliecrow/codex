---
name: gitsummary
description: Analyze current branch vs main, understand all diffs and intent, and produce a concise lower-case bullet list suitable for a PR summary, including nuances and gotchas.
---

# gitsummary

## Overview

Produce a precise, lower-case PR summary by fully understanding how the current branch differs from main. Conduct a deep, thorough review of all diffs so every change and decision is understood and reasoned through before summarizing.

## Behavioral guardrails (must follow)

- Do not assume intent or fill gaps; call out uncertainty if needed.
- Prefer the simplest summary that covers the actual changes; avoid speculative detail.
- Keep scope surgical: every bullet must map to a specific change.
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

1. Establish baseline:
   - Confirm repo root and current branch.
   - Determine the main branch name (main/master) and verify it exists locally.

2. Gather diffs and context:
   - Compare branch vs main (e.g., `git diff main...HEAD` and `git log main..HEAD`).
   - If diffs are large, start with `git diff --stat main...HEAD` or `git diff --name-only main...HEAD` and then review per-file diffs to keep output manageable.
   - Account for large git output; prefer bounded output like `git log --oneline -n 20`, `git diff --stat main...HEAD`, `git diff --name-only main...HEAD`, or per-file diffs instead of unbounded commands.
   - Review file-level changes and key hunks to understand intent.
   - Review every changed file and hunk; do not skip any relevant changes.
   - Read related docs or comments if they explain why changes were made.
   - If git operations can be executed here, run them directly using the user's git identity; otherwise, output explicit commands and wait for results before continuing.
   - When providing git commands, output a single copy-pasteable block with only commands and no commentary; place explanations above or below the block.

3. Understand intent and impact:
   - Map changes to user-facing behavior, APIs, data, config, or ops.
   - Note any risk areas, edge cases, or migration considerations.
   - Identify tests added/updated and gaps if any are missing.
   - Call out removed or degraded functionality compared to main when relevant.

4. Summarize for PR:
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