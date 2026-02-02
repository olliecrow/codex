---
name: decisions
description: Deep, thorough decision support. Use when the conversation presents decisions to be made and requires background research, options analysis, and a consolidated recommendation report.
---

# Decisions

## Overview

This skill is for decision points in a conversation. Conduct deep and thorough background research for each decision, including investigations and considerations, then deliver a single, consolidated decision report. If the research shows there is no longer a decision to be made, omit that decision from the decision list and explain why a decision is no longer needed.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- State assumptions explicitly; if multiple interpretations exist, surface them before deciding.
- Prefer the simplest viable option when it satisfies requirements; push back on unnecessary complexity.
- Keep scope surgical: only include decisions that are actually required.
- Define clear success criteria for decisions and how they will be validated.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Shared principles (must follow)

- Use the smallest set of skills that fully covers the request; if multiple skills apply, state the order.
- Treat the `description` in this file as the primary trigger signal; do not expand scope beyond it.
- Use progressive disclosure for context: read only the files you need and summarize, do not bulk-load unrelated material.
- Prefer skill-provided scripts/templates or existing repo assets over retyping or reinventing workflows.
- Keep context tight and reduce noise; ask questions only when requirements are ambiguous or blocking.
- Write summaries in plain, concise language with brief context; avoid analogies and define technical terms when needed.

## Decision framing (must follow)

For every decision that still exists after research, include:
- Background context that fully equips a new reader to understand the topic and make an educated decision.
- Concrete examples (not analogies) that illustrate the options, impact, or tradeoffs.
- Options that are actually viable, with clear pros and cons for each.
- Your recommendation, including the reasoning and logic behind it.
- A confidence level and the key assumptions that drive the recommendation.
If no decisions remain, say so explicitly and explain why.

## Rationale capture

When a decision is made or a recommendation is adopted, record the "why" in a durable place (docs, ADR, code comments, or tests) according to `docs/decisions.md`. In the report, state where the rationale was captured or call out if it is missing.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place and call out the missing decision doc in the report.

## Workflow

1) Identify the decisions.
   - Enumerate each decision that must be made.
   - Clarify scope, constraints, and success criteria.
   - If the decision list is ambiguous, ask a minimal clarifying question.
2) Research deeply.
   - Perform deep, thorough background research for each decision, including investigations and considerations.
   - Gather evidence from the codebase, docs, logs, and relevant external sources.
   - Prefer primary sources and record versions or dates.
   - Validate any facts that could have changed recently.
3) Build decision context.
   - Explain the current state, the problem, and why it matters.
   - Include concrete examples (not analogies) that make the situation tangible.
   - Call out risks, dependencies, and non-negotiable constraints.
4) Analyze options.
   - List viable options; exclude non-viable ones explicitly.
   - Provide pros and cons for each option.
   - Include evidence for why each option is viable and why excluded options were rejected.
   - Note implementation effort, operational impact, and long-term maintenance.
5) Recommend.
   - Provide a clear recommendation with reasoning and logic.
   - State confidence and the assumptions behind the recommendation.
6) Consolidate the report.
   - Deliver one consolidated report that covers all decisions.
   - If any decisions are resolved by the research itself, remove them from the decision list and explain why a decision is no longer needed.

## Output expectations

- Provide a single consolidated report with clear sections per decision.
- Use plain, concise language; avoid analogies.
- Use absolute dates when referencing timelines.
- Distinguish facts, inferences, and uncertainties.
- Call out critical risks or red flags; if none exist, say so explicitly.
- Include examples for each decision.
- Include pros and cons for each viable option.
- Always include a recommendation with reasoning.
- If no decision remains, say so explicitly and explain why a decision is no longer needed.

## Repeat invocations

- Reuse prior research and expand with new evidence.
- Highlight what changed since the last report.
- Reissue the full consolidated report, not a delta.