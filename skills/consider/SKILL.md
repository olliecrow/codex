---
name: consider
description: Consider new evidence or reviews about recent work, investigate and reason deeply, and decide what (if anything) to integrate or change. Use when asked to evaluate new information and determine next actions.
---

# Consider

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
- Never squash commits; always use merge commits when integrating branches.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Evaluate new evidence or reviews about current work (for example, an independent review of a branch or codebase) without treating them as gospel. Investigate, research, and reason deeply to determine whether any points are valid, whether changes or further investigation are warranted, and what to do next. It is acceptable to conclude that nothing should change and to ignore suggestions that are not supported by evidence.

## Shared principles (must follow)

- Use the smallest set of skills that fully covers the request; if multiple skills apply, state the order.
- Treat the `description` in this file as the primary trigger signal; do not expand scope beyond it.
- Use progressive disclosure for context: read only the files you need and summarize, do not bulk-load unrelated material.
- Prefer skill-provided scripts/templates or existing repo assets over retyping or reinventing workflows.
- Keep context tight and reduce noise; ask questions only when requirements are ambiguous or blocking.
- Write summaries in plain, concise language with brief context; avoid analogies and define technical terms when needed.
- Prefer the simplest viable approach and call out overcomplication or speculative scope.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- State assumptions explicitly; if evidence scope or intent is unclear, ask before proceeding.
- Do not treat evidence as authoritative; validate with independent checks.
- Prefer the smallest investigation that establishes confidence; avoid scope creep.
- Keep changes surgical and within the evidence scope; do not introduce unrelated refactors.
- Define success criteria for accepting, modifying, deferring, or rejecting each point.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

## Rationale capture

When you accept, reject, or defer a point from the evidence and it results in a change or durable behavior, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your summary, mention where the rationale was recorded or call out the gap.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

1. Scope the evidence:
   - Identify the evidence source(s), date(s), and scope (files, subsystems, behavior).
   - Note whether it is an independent review, audit, or internal feedback.
   - Extract each claim, suggestion, or finding; list them explicitly.
   - Clarify what is in or out of scope for this consideration.

2. Assess evidence quality:
   - Evaluate methodology, coverage, recency, and potential bias.
   - Note any missing context, incomplete coverage, or assumptions.
   - Record uncertainties and risk of false positives/negatives.

3. Validate independently:
   - Read relevant code, docs, and tests.
   - Research external sources or specs when relevant to validate claims.
   - Run targeted checks or small experiments as needed to validate claims.
   - Keep a lightweight log in `plan/current/consider.md` (untracked) with probes and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
   - Prefer minimal probes that directly validate each claim; avoid unnecessary broad testing.

4. Evaluate each point:
   - Classify each claim: **accept**, **accept with modifications**, **defer**, or **reject**.
   - Provide reasoning and evidence for each classification.
   - If more data is required, specify the minimal investigation needed.

5. Decide next actions:
   - If changes or follow-up work are warranted, produce a highly detailed plan of change with steps, risks, and verification.
   - If nothing should change, say so explicitly and explain why the evidence does not warrant action.

6. Report:
   - Summarize the evidence considered, the validation performed, and the conclusions.
   - Call out accepted items and rejected items with rationale.
   - Include a plan only when changes are warranted; otherwise state that no plan is needed.
   - Write in plain, concise, and intuitive language with brief context.
   - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Output expectations

- A concise summary of evidence sources and scope.
- A per-point disposition (accept/modify/defer/reject) with reasoning.
- Explicit callout of whether any changes are warranted.
- If changes are warranted, a detailed, step-by-step plan with verification.
- If no changes are warranted, a direct statement that no action is needed.

## Repeat invocations

- Carry forward prior evidence and validation results; avoid repeating the same probes.
- Highlight what changed since the last consideration.
- Expand investigation only when new evidence or unresolved uncertainty justifies it.
