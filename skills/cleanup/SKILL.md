---
name: cleanup
description: Review recent changes and/or broader code to simplify or reduce technical debt without breaking behavior or performance. Use when asked to tidy up, lightly refactor, or address tech debt.
---

# Cleanup

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

Relentlessly search for tech debt, bloat, redundancy, unused code, and unnecessary complexity across the project, then simplify, tidy, and de-over-engineer while preserving performance. Conduct a deep, thorough review of all relevant areas and reason through every cleanup decision.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- State assumptions explicitly; if cleanup scope is unclear, stop and ask.
- Prefer the simplest change that solves the problem; avoid speculative refactors.
- Keep changes surgical: do not touch adjacent code, comments, or formatting unless required.
- Prioritize clarity and maintainability over strict backward compatibility when it materially improves the codebase.
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

1. Establish scope:
- For cleanup of recent work, compare current branch to its base (or main/master) to find what changed.
- For tech debt work, expand scope to the broader codebase and recent changes.
- Include changes made during the current conversation.
- Ensure every relevant area is reviewed; do not skip parts that affect behavior.

2. Identify cleanup and tech-debt opportunities:
   - Relentlessly search for tech debt, bloat, redundancy, unused code, dead paths, and unnecessary complexity.
   - Remove redundancy, simplify logic, reduce over-engineering.
   - Improve readability and maintainability.
   - Look for over-engineering, duplication, confusing structure, unnecessary complexity.
   - Scan for TODO/FIXME, deprecated APIs, and stale or misleading docs.
   - Keep changes focused on tidying up, not feature work.

3. Prioritize and log (when addressing tech debt):
   - Rank items by impact (maintainability, risk, churn) and effort.
   - Track a lightweight debt log in `plan/current/techdebt.md` (untracked) with found items, fixes, and deferred items plus the reason. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - For each planned change, state the intent (behavior-preserving or behavior-changing) and why the change is worth it.

4. Investigate and validate:
   - Proactively create and run isolated tests or experiments to understand behavior.
   - Start with small, fast checks before larger runs; large tests are still expected when relevant.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - Use a `plan/` directory as scratch space (create it if missing and edits are permitted); keep it untracked and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.
   - If touching hot paths, capture a baseline or avoid micro-optimizations without evidence.
   - Capture before/after evidence for any performance-sensitive edits.

5. Apply cleanup changes:
   - Make small, safe simplifications when possible; allow behavior-changing cleanups if they materially improve maintainability.
   - Prefer clarity and minimalism.
   - Keep edits localized to changed areas unless a broader cleanup is clearly safe.
   - Breaking changes are allowed; clearly call them out, justify them, and ensure the end state is cleaner and more maintainable.
   - Do not regress runtime or memory performance.
   - Avoid making code more complex.
   - Keep intent explicit; stop and ask only if a behavior change would be risky or unclear.

6. Verify after changes:
   - Rerun relevant tests/experiments (small before large) to confirm no functional or performance regressions.
   - Clean up temporary test scripts unless they are needed to track a discovered issue.
   - Do a scope check: confirm changes stayed within cleanup/tech-debt work and did not drift into feature work.

7. Summarize results:
   - List areas cleaned up and why.
   - Call out deferred debt or risky areas left untouched.
   - Call out any risky areas avoided.
   - Note possible next cleanup steps.
   - If called repeatedly, you may follow prior suggested next steps or take a fresh angle; both are fine. Continue finding new cleanup opportunities and avoid repeating prior summaries unless there are no new changes.
   - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.
