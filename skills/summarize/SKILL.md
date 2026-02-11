---
name: summarize
description: Summarize complex information from any source into concise, decision-ready briefs. Use when asked to "summarize" work, discussions, research, plans, tickets, incidents, meetings, audits, reviews, or project status while preserving background context, evidence when available, reasoning, pros/cons, and critical red flags.
---

# Summarize

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

## Goal

Produce a clear, concise, direct summary that fully equips the reader to understand what happened, why it happened, and what decisions or actions are needed next.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- State assumptions explicitly; if the source is ambiguous, call it out instead of guessing.
- Prefer the simplest summary that meets the need; avoid speculative or extra detail.
- Keep scope surgical: include only what is supported by the source material.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.
If no decision is required, say so explicitly and continue.

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
