---
name: summarize
description: Summarize complex information from any source into concise, decision-ready briefs. Use when asked to "summarize" work, discussions, research, plans, tickets, incidents, meetings, audits, reviews, or project status while preserving background context, evidence when available, reasoning, pros/cons, and critical red flags.
---

# Summarize

## Goal

Produce a clear, concise, direct summary that fully equips the reader to understand what happened, why it happened, and what decisions or actions are needed next.

## Behavioral guardrails (must follow)

- State assumptions explicitly; if the source is ambiguous, call it out instead of guessing.
- Prefer the simplest summary that meets the need; avoid speculative or extra detail.
- Keep scope surgical: include only what is supported by the source material.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Rationale capture

When summarizing fixes, changes, or key decisions, confirm the "why" is captured in a durable place (docs, notes, tickets, ADRs, code comments, or tests). If it is missing, call out the gap in the summary.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Identify the scope.
   - Clarify the time window, sources, and what is in/out of scope.
   - If scope is ambiguous, ask a brief clarifying question before summarizing.
2. Extract background and context.
   - Explain the starting point, why it matters, and constraints.
3. Surface critical issues first.
   - Lead with red flags, blockers, or urgent risks that require immediate attention.
   - Label any critical red flags, serious concerns, and immediate next steps explicitly and explain them clearly.
4. Summarize key findings.
   - Summarize all findings, even if brief.
   - Focus on outcomes, evidence, and implications; avoid low-value detail.
5. Capture decisions and rationale.
   - For each decision made or needed, include:
     - Options considered
     - Pros and cons
     - Recommendation (with reasoning)
6. List open questions and next steps.
   - Make them specific, actionable, and prioritized if possible.

## Output Expectations

- Be concise and direct; prefer short paragraphs or bullets.
- Include enough background context so a reader can understand the situation without prior knowledge.
- Tailor depth and emphasis to the stated audience (executive, technical, operational) when specified.
- Write in plain, concise, and intuitive language with brief context.
- Clearly highlight and explain any critical red flags, serious concerns/issues, or immediate next steps.
- Avoid analogies; use simple, direct explanations and define any necessary technical terms.
- Use absolute dates when referencing timelines.
- Distinguish facts, inferences, and uncertainties.
- When applicable, include key evidence (tests, logs, artifacts) and a confidence level.
- Call out remaining risks or unknowns.
- If no critical red flags exist, say so explicitly.
- Ensure all findings are summarized, even if brief.

## Repeat invocations

- Carry forward unresolved items and prior decisions.
- Highlight new findings, reversals, or changes since the last summary.
- Avoid repeating unchanged detail unless it is needed for context.

## Common Pitfalls

- Omitting context that explains why findings matter.
- Burying urgent risks below routine details.
- Presenting recommendations without pros/cons or reasoning.
- Over-summarizing and removing essential decision context.
