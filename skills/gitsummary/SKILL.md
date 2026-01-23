---
name: gitsummary
description: Analyze current branch vs main, understand all diffs and intent, and produce a concise lower-case bullet list suitable for a PR summary, including nuances and gotchas.
---

# gitsummary

## Overview

Produce a precise, lower-case PR summary by fully understanding how the current branch differs from main. Conduct a deep, thorough review of all diffs so every change and decision is understood and reasoned through before summarizing.

## Rationale capture

If changes include issue fixes or key decisions, confirm the rationale is captured in a durable place (code comments, docs, ADR, or tests). If it is missing, call that out as a gap in the PR summary.

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
