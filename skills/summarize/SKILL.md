---
name: summarize
description: Summarize complex information from any source into concise, decision-ready briefs. Use when asked to "summarize" work, discussions, research, plans, tickets, incidents, meetings, audits, reviews, or project status while preserving background context, evidence when available, reasoning, pros/cons, and critical red flags.
---

# Summarize

## Goal

Produce a clear, concise, direct summary that fully equips the reader to understand what happened, why it happened, and what decisions or actions are needed next.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Rationale capture

When summarizing fixes, changes, or key decisions, confirm the "why" is captured in a durable place (docs, notes, tickets, ADRs, code comments, or tests). If it is missing, call out the gap in the summary.

## Workflow

1. Identify the scope.
   - Clarify the time window, sources, and what is in/out of scope.
   - If scope is ambiguous, ask a brief clarifying question before summarizing.
2. Extract background and context.
   - Explain the starting point, why it matters, and constraints.
3. Surface critical issues first.
   - Lead with red flags, blockers, or urgent risks that require immediate attention.
4. Summarize key findings.
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
- Avoid analogies; use simple, direct explanations and define any necessary technical terms.
- Use absolute dates when referencing timelines.
- Distinguish facts, inferences, and uncertainties.
- When applicable, include key evidence (tests, logs, artifacts) and a confidence level.
- Call out remaining risks or unknowns.
- If no critical red flags exist, say so explicitly.

## Repeat invocations

- Carry forward unresolved items and prior decisions.
- Highlight new findings, reversals, or changes since the last summary.
- Avoid repeating unchanged detail unless it is needed for context.

## Common Pitfalls

- Omitting context that explains why findings matter.
- Burying urgent risks below routine details.
- Presenting recommendations without pros/cons or reasoning.
- Over-summarizing and removing essential decision context.
