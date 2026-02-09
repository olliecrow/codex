---
name: organise-docs
description: Autonomously maintain repository documentation from the active conversation across any project. Use when the user asks to update docs from chat context, capture explicit or inferred high-confidence decisions, consolidate contradictions, reduce ambiguity, reorganize doc structure, and preserve durable knowledge for future contributors.
---

# Organise Docs

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: move the task forward without waiting when the next high-value action is clear.
- Act autonomously on high-conviction, in-scope actions and fixes; ask only when confidence is low or risk is meaningful.
- Drive work to complete outcomes with verification, not partial handoffs.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Overview

Extract durable knowledge from the current conversation and convert it into high-signal repository documentation. Focus on decisions, principles, invariants, constraints, and rationale that remain useful over time.

## Continual compounding mode (must follow)

Run a compounding cycle after each substantial task.
- Treat a task as substantial when it includes multi-step debugging/investigation, meaningful code edits, non-trivial design decisions, or repeated back-and-forth that produced reusable knowledge.
- Keep a lightweight "write it down now" habit during execution so useful details are not reconstructed from memory later.
- Capture ephemeral exploration notes in `plan/` while working.
- Promote durable learnings into `docs/` before finishing the task.
- Consolidate duplicated scratch notes and prune stale `plan/` artifacts after promotion.
- Keep `docs/` evergreen and high-signal; keep `plan/` disposable and short-lived.

## Operating Mode

Apply documentation edits autonomously when confidence is high.
- Auto-apply doc edits without asking for permission when evidence is strong.
- Create, merge, split, move, rename, reorganize, and delete docs when this improves clarity and maintainability.
- If confidence is not high, do not invent facts. Leave content unchanged or call out the uncertainty in the final summary.

## Notes hierarchy and routing (must follow)

- Treat notes and snippets as flexible raw material; organization can evolve as understanding improves.
- Route ephemeral notes to `plan/current/` and keep them concise, task-linked, and disposable.
- Route durable guidance to `docs/` only after de-duplication and contradiction checks.
- Keep per-workstream notes near the workstream context (for example in its worktree/cwd notes file) and reflect only compact pointers in shared indexes.
- For multi-workstream/subagent efforts, keep a compact shared index (for example `plan/current/notes-index.md`) that links workstream notes and latest status.
- If `plan/` cannot be created, keep an in-memory index and call it out in the report.

## Workflow

1. Build the evidence set.
- Read the relevant conversation turns, edited files, and test outcomes before writing docs.
- Use only evidence-backed statements.
- Prefer concrete facts over interpretations.
- Keep temporary extraction notes in `plan/current/` while building the evidence set.
- Gather relevant notes and snippets from active workstreams before consolidation so nothing important is dropped.

2. Filter for durable knowledge.
- Keep: decisions, trade-offs, rules, invariants, failure modes, and stable process guidance.
- Drop: one-off status, temporary debugging traces, timestamps, and short-lived implementation trivia.
- Rewrite relative time phrasing into evergreen language.
- Mark every retained item as either `promote to docs` or `keep ephemeral in plan`.

3. Consolidate contradictions and ambiguity.
- Detect conflicting statements and collapse them into a single canonical statement.
- Use this tie-break order: current code/tests, explicit user instructions, then older docs.
- Replace vague wording with explicit terms, units, and constraints.

4. Route and reorganize docs.
- Prefer updating existing relevant docs first.
- Create new docs when the existing structure cannot hold content clearly.
- Merge fragmented docs when they duplicate scope.
- Split overloaded docs when mixed topics reduce clarity.
- Reorganize notes into a clear hierarchy when raw notes have grown large or hard to navigate.

5. Write concise, structured updates.
- Use explicit sections or bullet entries that are easy to scan.
- For decisions, include: `Decision`, `Context`, `Rationale`, `Trade-offs`, `Enforcement`.
- Capture inferred decisions only when conviction is high and evidence supports the inference.
- Reference concrete enforcement points such as tests, modules, or invariants when known.
- Avoid duplicating existing text; tighten or replace stale wording instead.

6. Apply preservation checks before destructive edits.
- Never destroy potentially valuable information.
- Before deleting or heavily consolidating a doc, migrate all unique valuable content into a retained destination.
- Treat rationale, constraints, invariants, risk notes, and behavioral contracts as valuable by default.
- If value is uncertain, preserve the content in a compact retained section rather than deleting it.

7. Validate consistency before finishing.
- Check that new documentation matches current code and tests.
- Fail fast on contradictions: do not publish a doc update that conflicts with known behavior.
- Remove low-confidence speculative claims.

8. Report what changed.
- Summarize files updated and the durable knowledge captured.
- Call out removed or consolidated docs and where preserved content was moved.
- Include a preservation map for destructive edits: `source_doc -> destination_doc/section`.
- List remaining ambiguity only when confidence was not high enough to resolve it safely.
- Include a `What got faster next time` section with concrete workflow improvements unlocked by the updated docs.
- Include a `Plan consolidation and prune` section listing which `plan/` artifacts were retained, merged, or deleted.

## Quality Bar

- Keep docs evergreen and stable; avoid date-anchored wording unless dates are required for correctness.
- Preserve fail-fast intent and do not document silent fallback behavior unless it is explicitly desired.
- Prefer simple language and explicit statements over abstract summaries.
- Ensure every added line helps future contributors make better decisions faster.
- Default to high-confidence autonomous changes; do not block on avoidable questions.

## Decision Entry Template

Use this structure when recording a new decision:

```text
Decision:
Context:
Rationale:
Trade-offs:
Enforcement:
```
