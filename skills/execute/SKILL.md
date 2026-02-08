---
name: execute
description: Execute the current plan end-to-end, verifying completion; use when asked to run or carry out an existing plan and report results.
---

# execute

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Overview

Execute an existing plan step by step until it is fully complete and verified. Follow the plan spec's validation checkpoints and contingencies, using real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.

## Controller/worker orchestration mode (must follow for non-trivial plans)

Use a controller role to coordinate focused workers.
- Act as controller by default when the plan has parallelizable streams or mixed disciplines (research/code/data).
- Decompose the plan into scoped work packets with objective, inputs, constraints, and acceptance checks.
- When a packet can run independently and policy permits, assign it to an isolated worktree or dedicated `cwd` to reduce interference.
- Delegate focused packets to workers:
  - `research-worker`: gather evidence, constraints, and references.
  - `code-worker`: implement scoped code/config/doc changes.
  - `data-worker`: run analysis, measurements, and validation datasets/checks.
- Keep workers narrow; prevent cross-scope drift.
- Maintain a controller status board (`plan/current/orchestrator-status.md`, untracked) with packet, owner, `cwd`/worktree, status, blocker, and last update. If `plan/` cannot be created, keep an equivalent in-memory board and call it out in the report.
- Require each worker handoff to include concise outputs: what changed, evidence pointers, and unresolved risks.
- Keep a running notes file (`plan/current/notes.md`, untracked) with short updates after meaningful steps so findings can be reorganized and promoted later. If `plan/` cannot be created, keep in-memory notes and call it out in the report.
- Merge worker outputs in the controller pass.
- Run consistency checks before delivery:
  - requirements coverage across all work packets,
  - contradiction check across assumptions/findings,
  - implementation-to-evidence alignment,
  - validation completeness and pass/fail status.
- If consistency checks fail, route issues back to the relevant worker packet, then re-merge and re-check.
- Deliver only after controller consistency checks pass or blockers are explicitly documented.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm the expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- State assumptions explicitly; if anything is unclear or has multiple interpretations, stop and ask.
- Prefer the simplest implementation that satisfies the plan; avoid speculative features or extra flexibility.
- Keep changes surgical and within plan scope; do not refactor or "improve" adjacent code unless required.
- Define success criteria per step and verify before moving on.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

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
   - Check for existing execution logs and completion ledgers in `plan/current/` and load them before taking new actions.
   - If `docs/workflows.md` exists, align note routing and status tracking with it before execution starts.
   - If workflow conventions are missing and edits are allowed, prefer running `setup` before long-running or parallel execution.
   - For long or parallel execution, initialize note routing up front: scratch notes, status board, and the promotion path for durable learnings.
   - If critical information is missing, ask only the necessary questions and pause execution.
   - Use `plan/` as scratch space when needed; create it only if permitted, keep it untracked, and never commit it. If you cannot create it, keep a lightweight in-memory log and call it out in the report.
   - For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

3. Execute relentlessly:
   - Perform each step in order, without skipping.
   - Use controller/worker orchestration when plan streams can run independently.
   - Track progress in `plan/current/execute.md` (untracked) with actions taken and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - Maintain `plan/current/execute-ledger.md` (untracked) with each plan step's status (`pending`, `in_progress`, `done`), evidence pointer, and last verification result. If `plan/` cannot be created, keep a lightweight in-memory ledger and call it out in the report.
   - After each meaningful action, append a concise note with what was done, what changed, and what remains.
   - If a step fails, diagnose, fix, and retry before moving on.
   - Run the step-specific validation checks from the plan as you go; do not defer all testing to the end.
   - If the plan is ambiguous or would require scope expansion, stop and ask before proceeding.
   - Do not stop until all steps are complete.

4. Verify completion:
   - Run the relevant checks/tests, starting small and expanding to broader coverage as needed.
   - Prefer production-like configurations and real datasets when feasible; document data sources and constraints.
   - After any fixes, re-run the smallest relevant checks to confirm no regressions.
   - Remove ad-hoc experiments that are no longer needed; keep only those that revealed issues and should be preserved.
   - If verification fails, fix issues and re-verify until green.

5. Report:
   - State that execution is complete and verified, or explain what remains if blocked.
   - If no new inputs or code changes exist and the completion ledger is fully `done`, report that there is no remaining work and stop.
   - Include controller summary, worker packet outcomes, and consistency-check results.
   - Write in plain, concise, and intuitive language with brief context.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- If called multiple times, continue from the latest progress log and avoid redoing completed steps unless verification requires it.
- Update `plan/current/execute.md` and `plan/current/execute-ledger.md` with new actions, fixes, and re-verification results. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
- If the completion ledger shows all steps `done` and no new evidence is introduced, do not rerun the same loop; return a concise completion confirmation instead.
