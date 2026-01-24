---
name: plan
description: Create a comprehensive, high-conviction change plan that improves the codebase using all available context and decisions. Only include plan items you are highly confident in; if anything is unclear or low conviction, pause to request clarification or schedule targeted investigation before adding it.
---

# plan

## Overview

Create a single, consolidated, highly detailed plan that moves the codebase from its current state to a better state. Incorporate all available information (conversation, prior decisions, AGENTS.md, docs/, code, recent changes, tech debt notes, and any evidence gathered). The plan must be high confidence: only include steps you strongly believe are correct and beneficial. If anything material is uncertain or low-conviction, pause and ask a clarifying question (or schedule a targeted investigation) before including it in the plan.

## Shared principles (must follow)

- Use the smallest set of skills that fully covers the request; if multiple skills apply, state the order.
- Treat the `description` in this file as the primary trigger signal; do not expand scope beyond it.
- Use progressive disclosure for context: read only the files you need and summarize, do not bulk-load unrelated material.
- Prefer skill-provided scripts/templates or existing repo assets over retyping or reinventing workflows.
- Keep context tight and reduce noise; ask questions only when requirements are ambiguous or blocking.
- Write summaries in plain, concise language with brief context; avoid analogies and define technical terms when needed.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
- Explicit confidence level and key assumptions.

## Rationale capture

If the plan introduces or recommends a decision that should be durable, capture the "why" in the smallest durable place (code comments, docs, ADR/tests) and note where it was captured. Do not rely only on `plan/` scratch notes.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it with the required subdirectories only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- Avoid time- or date-dependent language in `docs/`; prefer timeless, evergreen wording.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place and call out the missing decision doc in the report.

## Workflow

### 1) Gather full context

- Re-read the user request, conversation, and any decisions already made.
- Read AGENTS.md, docs/ (especially decisions), and relevant runbooks.
- Scan the repo structure, key modules, and recent changes (git diff/status if allowed).
- Identify known constraints (tests, environment, performance, security, release rules).
- Inventory tech debt signals (TODO/FIXME, duplication, brittle areas).
- Capture notes in `plan/current/plan.md` if scratch space is needed.

### 2) Establish current state

- Summarize how the system works today (key flows, dependencies, boundaries).
- Call out pain points, risks, and places where behavior must remain unchanged.
- List any missing information and decide if it blocks planning.

### 3) Define the target state

- Specify the desired end state in concrete terms (behavior, structure, quality).
- List invariants that must not be violated.
- Define acceptance criteria and success signals.

### 4) Identify candidate changes

- List possible improvements and map them to goals.
- Filter aggressively: keep only high-confidence, high-conviction items.
- For any candidate with uncertainty or low conviction, schedule investigation or ask for clarification before committing it to the plan.

### 5) Make required decisions

- For each decision, provide the required framing (context, options, pros/cons, recommendation).
- Prefer decisions that reduce complexity and future maintenance burden.
- Avoid introducing tech debt; if unavoidable, justify and record mitigation.

### 6) Build the plan (single consolidated plan)

- Organize into phases (for example: Preparation, Changes, Cleanup, Verification, Rollout).
- For each step include:
  - Goal and rationale (why it improves the codebase).
  - Scope (files, modules, APIs, data).
  - Ordered tasks and dependencies.
  - Risks and mitigations.
  - Validation steps (tests, checks, manual verification).
  - Rollback/exit criteria when relevant.
- Keep the plan extremely detailed and explicit; no hand-wavy steps.

### 7) Quality gate

- Confirm every item is high confidence and improves the codebase.
- Remove or defer anything ambiguous; ask questions only when necessary.
- Ensure the plan is consistent with repo guidelines and constraints.

### 8) Output

- Deliver a single, verbose, consolidated plan with sections:
  - Context and constraints
  - Current state summary
  - Target state
  - Decisions (with pros/cons and recommendations)
  - Phased plan with detailed steps
  - Validation strategy
  - Risks and mitigations
  - Open questions (only if truly blocking)

## Repeat invocations

- Reuse prior notes and decisions; avoid rehashing unchanged sections.
- If invoked multiple times in a row, perform further investigation on any items that still need clarification or evidence before finalizing updates.
- Incorporate new information and reissue a fully consolidated plan.
- Always return the full, final consolidated plan of change (not a delta).
- State what changed since the last plan and why.
