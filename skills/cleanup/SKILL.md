---
name: cleanup
description: Review recent code changes and simplify/clean them without breaking behavior or performance. Use when asked to tidy up or lightly refactor work from the current branch or conversation.
---

# Cleanup

## Overview

Identify recent changes, then simplify, tidy, and de-over-engineer while preserving behavior and performance. Conduct a deep, thorough review of all relevant changes and reason through every cleanup decision.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- State assumptions explicitly; if cleanup scope is unclear, stop and ask.
- Prefer the simplest change that solves the problem; avoid speculative refactors.
- Keep changes surgical: do not touch adjacent code, comments, or formatting unless required.
- Define success criteria and verify after cleanup; do not assume no regressions.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you fix an issue, make a change that resolves an issue, or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Identify scope of changes:
- Compare current branch to its base (or main/master) to find what changed.
- Include changes made during the current conversation.
- Review every changed file and hunk; do not skip any relevant area.

2. Find cleanup opportunities:
   - Remove redundancy, simplify logic, reduce over-engineering.
   - Improve readability and maintainability.
   - Keep changes focused on tidying up, not feature work.

3. Investigate and validate:
   - Proactively create and run isolated tests or experiments to understand behavior.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

4. Apply cleanup changes:
   - Make small, safe simplifications.
   - Prefer clarity and minimalism.
   - Keep edits localized to changed areas unless a broader cleanup is clearly safe.
   - Do not break existing features.
   - Do not regress runtime or memory performance.
   - Avoid making code more complex.

5. Verify after changes:
   - Rerun relevant tests/experiments (small before large) to confirm no functional or performance regressions.
   - Clean up temporary test scripts unless they are needed to track a discovered issue.

6. Summarize results:
   - List areas cleaned up and why.
   - Call out any risky areas avoided.
   - Note possible next cleanup steps.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue finding new cleanup opportunities and avoid repeating prior summaries unless there are no new changes.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.