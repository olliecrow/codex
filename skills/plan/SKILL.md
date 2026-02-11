---
name: plan
description: Create a comprehensive, high-conviction change plan that improves the codebase using all available context and decisions. Only include plan items you are highly confident in; if anything is unclear or low conviction, pause to request clarification or schedule targeted investigation before adding it.
---

# plan

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: immediately take the next highest-value in-scope action when it is clear.
- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material risk tradeoffs, missing required data/access, or destructive/irreversible actions outside policy.
- If blocked by command/tool/env failures, attempt high-confidence fallbacks autonomously before escalating (for example `rg` -> `find`/`grep`, `python` -> `python3`, alternate repo-native scripts).
- When the workflow uses `plan/`, ensure required plan directories exist before reading/writing them (create when edits are allowed; otherwise use an in-memory fallback and call it out).
- Treat transient external failures (network/SSH/remote APIs/timeouts) as retryable by default: run bounded retries with backoff and capture failure evidence before concluding blocked.
- On repeated invocations for the same objective, resume from prior findings/artifacts and prioritize net-new progress over rerunning identical work unless verification requires reruns.
- Drive work to complete outcomes with verification, not partial handoffs.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes. Example loops (adapt as needed, not rigid): issue-resolution `investigate -> plan -> fix -> verify -> battletest -> organise-docs -> git-commit -> re-review`; cleanup `scan -> prioritize -> clean -> verify -> re-scan`; docs `audit -> update -> verify -> re-audit`.
- Keep looping until actual completion criteria are met: no actionable in-scope items remain, verification is green, and confidence is high.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Create a single, consolidated, highly detailed plan spec that moves the codebase from its current state to a better state. This skill is intended for long, end-to-end work: produce a comprehensive spec so execution can proceed start-to-finish without additional questions, input, or decisions. Do not produce short or partial plans. Incorporate all available information (conversation, prior decisions, AGENTS.md, docs/, code, recent changes, tech debt notes, and any evidence gathered). Pack the questions, assumptions, investigation results, reasoning, and decisions up front. The plan must be high confidence: only include steps you strongly believe are correct and beneficial. If anything material is uncertain or low-conviction, resolve it via investigation or explicit assumptions before including it in the plan. If it cannot be resolved, state that planning is blocked and stop.

The spec must include empirical validation and battle testing, using real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces. Do not make the plan monolithic: build in step-by-step verification and testing throughout the phases, not only at the end. Always include a dedicated verification/validation plan immediately following the implementation plan; omission should be extremely rare and must be explicitly justified.

The spec is the primary working artifact for the task and should be saved in `plan/current/` as one or more Markdown files. It is still scratch and should not be committed. It should be comprehensive and execution-ready, with investigation results, assumptions, decisions, and validation plans captured in the spec itself.

## Shared principles (must follow)

- Use the smallest set of skills that fully covers the request; if multiple skills apply, state the order.
- Treat the `description` in this file as the primary trigger signal; do not expand scope beyond it.
- Use progressive disclosure for context: read only the files you need and summarize, do not bulk-load unrelated material.
- Prefer skill-provided scripts/templates or existing repo assets over retyping or reinventing workflows.
- Keep context tight and reduce noise; ask questions only when requirements are ambiguous or blocking.
- Write summaries in plain, concise language with brief context; avoid analogies and define technical terms when needed.
- When a plan can answer a question via investigation or reasonable assumptions, do so and make assumptions explicit; only ask questions that are truly blocking.
- Ensure the plan is executable end-to-end without further input or decisions; resolve all decisions up front.
- For long-running or parallel work, define a note hierarchy and routing strategy up front (scratch vs durable notes) to reduce context bloat.
- Define explicit stop criteria and iteration limits so optimization does not turn into open-ended churn.
- For experiment-driven work, optimize for learning yield and throughput, not just task completion.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- State assumptions explicitly and surface alternate interpretations; do not pick one silently.
- Prefer the simplest viable approach and call out overcomplication or speculative scope.
- Keep the plan surgical: only include work that directly serves the request; mention unrelated opportunities without adding them.
- Define success criteria and verification for each step; avoid vague goals.
- If there is nothing left to plan, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
- Explicit confidence level and key assumptions.
If no decision is required, say so explicitly and continue.

## Rationale capture

If the plan introduces or recommends a decision that should be durable, capture the "why" in the smallest durable place (code comments, docs, ADR/tests) and note where it was captured. Do not rely only on `plan/` scratch notes.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it. Store the plan spec in `plan/current/` as the working artifact for the task.
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
- Investigate unknowns early and capture evidence needed for confident planning.
- When feasible, run targeted empirical probes (real data, real runs) to validate key assumptions before finalizing the plan.
- Capture notes in `plan/current/plan.md` if scratch space is needed.
- For long or multi-workstream plans, also define where to capture running notes, worker status, and handoff summaries.

### 2) Resolve immediate, low-risk items

- If there are items that can be safely worked through now (small investigations, quick validations, low-risk fixes), do them immediately.
- Capture results, evidence, and any changes made, then fold the outcomes into the plan.
- Keep scope tight; do not begin large refactors or multi-step implementations during this phase.

### 3) Establish current state

- Summarize how the system works today (key flows, dependencies, boundaries).
- Call out pain points, risks, and places where behavior must remain unchanged.
- List any missing information and decide if it blocks planning.

### 4) Define the target state

- Specify the desired end state in concrete terms (behavior, structure, quality).
- List invariants that must not be violated.
- Define acceptance criteria and success signals.

### 5) Identify candidate changes

- List possible improvements and map them to goals.
- Filter aggressively: keep only high-confidence, high-conviction items.
- For any candidate with uncertainty or low conviction, schedule investigation or ask for clarification before committing it to the plan.

### 6) Make required decisions

- For each decision, provide the required framing (context, options, pros/cons, recommendation).
- Prefer decisions that reduce complexity and future maintenance burden.
- Avoid introducing tech debt; if unavoidable, justify and record mitigation.

### 7) Build the plan spec (single consolidated spec)

- Organize into phases (for example: Preparation, Changes, Cleanup, Verification, Rollout).
- For each step include:
  - Goal and rationale (why it improves the codebase).
  - Scope (files, modules, APIs, data).
  - Ordered tasks and dependencies.
  - Risks and mitigations.
  - Validation steps (tests, checks, manual verification) that use real data and real runs when relevant.
  - Rollback/exit criteria when relevant.
- Include empirical battle tests where relevant, with concrete commands, datasets, and expected signals.
- Avoid end-only testing; embed verification after each meaningful phase.
- Include contingencies and mitigation steps tied to likely failure modes.
- For multi-step work, present step -> verify checks explicitly.
- Include execution budget guardrails (for example max passes/retries or explicit "re-open only with new evidence" criteria).
- For cluster/experiment plans, include clear criteria for autonomous submission when confidence is high and escalation rules when confidence is low.
- Keep the plan extremely detailed and explicit; no hand-wavy steps.

### 8) Validation and experimentation phase (required)

- Always include an extensive validation/experimentation phase after implementation.
- Specify real runs, empirical checks, and experiments with concrete commands and expected signals.
- Use real data and production-like conditions when relevant and possible; if not, justify why and note risks.
- Include a coverage matrix (configs, environments, perspectives) and a plan to expand it if issues appear.
- Define exit criteria for the validation phase and escalation steps for failures.

### 9) Quality gate

- Confirm every item is high confidence and improves the codebase.
- Remove or defer anything ambiguous; ask questions only when necessary.
- Ensure the plan is consistent with repo guidelines and constraints.
- Confirm the verification/validation plan is present and follows the implementation plan; only allow omission with explicit justification.
- Confirm the validation/experimentation phase is present, extensive, and uses real data when feasible.

### 10) Output

- Write the spec into `plan/current/` as one or more Markdown files (for example: `plan/current/spec.md` and `plan/current/spec-*.md`).
- Deliver a single, verbose, consolidated plan with sections:
  - Context and constraints
  - Current state summary
  - Target state
  - Evidence and investigations (what was tested, learned, and assumed)
  - Note hierarchy and routing plan (scratch notes, status tracking, and durable promotion path)
  - Decisions (with pros/cons and recommendations)
  - Phased plan with detailed steps
  - Verification/validation plan (required; follows implementation plan and is omitted only with explicit justification)
  - Validation/experimentation phase (required; extensive, empirical, and uses real data when feasible)
  - Risks and mitigations
  - Contingencies and mitigation playbook
  - Stop criteria and re-entry triggers (what ends the cycle and what justifies another cycle)
  - Open questions (only if truly blocking; if any exist, state that execution cannot proceed without input)

## Repeat invocations

- Reuse prior notes and decisions; avoid rehashing unchanged sections.
- If invoked multiple times in a row, perform further investigation on any items that still need clarification or evidence before finalizing updates.
- Treat repeat calls as a signal to keep fleshing out the current plan: dig deeper, clarify assumptions, and add missing detail rather than restart from scratch.
- Incorporate new information and reissue a fully consolidated plan and updated spec files.
- Always return the full, final consolidated plan of change (not a delta).
- State what changed since the last plan and why.
