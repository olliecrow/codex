---
name: gitsummary
description: Analyze current branch vs main, understand all diffs and intent, and produce a concise lower-case bullet list suitable for a PR summary, including nuances and gotchas.
---

# gitsummary

## Overview

Produce a precise, lower-case PR summary by fully understanding how the current branch differs from main.

## Workflow

1. Establish baseline:
   - Confirm repo root and current branch.
   - Determine the main branch name (main/master) and verify it exists locally.

2. Gather diffs and context:
   - Compare branch vs main (e.g., `git diff main...HEAD` and `git log main..HEAD`).
   - Review file-level changes and key hunks to understand intent.
   - Read related docs or comments if they explain why changes were made.

3. Understand intent and impact:
   - Map changes to user-facing behavior, APIs, data, config, or ops.
   - Note any risk areas, edge cases, or migration considerations.
   - Identify tests added/updated and gaps if any are missing.

4. Summarize for PR:
   - Output a very concise bullet list suitable for a PR summary.
   - Use lower-case text only.
   - End every bullet with a full stop.
   - Never use semicolons; keep punctuation simple.
   - Include important nuances, gotchas, and details others should know.
   - Write in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
