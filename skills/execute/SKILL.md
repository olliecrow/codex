---
name: execute
description: Execute the current plan end-to-end, verifying completion; use when asked to run or carry out an existing plan and report results.
---

# execute

## Overview

Execute an existing plan step by step until it is fully complete and verified. Follow the plan spec's validation checkpoints and contingencies, using real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Rationale capture

When you fix an issue, make a change that resolves an issue, or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your report, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Locate the plan:
   - Use the current plan from conversation context when available.
   - If a plan file exists in `plan/`, read the relevant one.
   - If no plan exists, state that there is nothing to execute and stop.

2. Validate readiness:
   - Confirm prerequisites, constraints, and required inputs are present.
   - If critical information is missing, ask only the necessary questions and pause execution.
   - Use `plan/` as scratch space when needed; create it only if permitted, keep it untracked, and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

3. Execute relentlessly:
   - Perform each step in order, without skipping.
   - Track progress in `plan/execute.md` (untracked) with actions taken and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - If a step fails, diagnose, fix, and retry before moving on.
   - Run the step-specific validation checks from the plan as you go; do not defer all testing to the end.
   - Do not stop until all steps are complete.

4. Verify completion:
   - Run the relevant checks/tests, starting small and expanding to broader coverage as needed.
   - Prefer production-like configurations and real datasets when feasible; document data sources and constraints.
   - After any fixes, re-run the smallest relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - If verification fails, fix issues and re-verify until green.

5. Report:
   - State that execution is complete and verified, or explain what remains if blocked.
   - Write in plain, concise, and intuitive language with brief context.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- If called multiple times, continue from the latest progress log and avoid redoing completed steps unless verification requires it.
- Update `plan/execute.md` with new actions, fixes, and re-verification results. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
