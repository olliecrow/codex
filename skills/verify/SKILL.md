---
name: verify
description: Verify correctness of recent code changes, decisions, plans, or outputs by running checks/tests and gathering evidence. Use when the user asks to confirm, validate, double-check, or prove that recent work (including plans) is correct, complete, or meets requirements, especially after edits, bug fixes, refactors, or discussions.
---

# Verify

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

Verify recent work by collecting evidence that it is correct, complete, and matches requirements, prioritizing targeted checks over broad stress testing unless risk demands it. Conduct a deep, thorough verification that reviews all relevant changes, decisions, and assumptions end-to-end and reasons through the evidence.

Prefer empirical verification with real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Run a preflight before substantial work: confirm the expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- State assumptions explicitly; if requirements are unclear or have multiple interpretations, ask before verifying.
- Prefer the simplest verification that proves the claim; do not add speculative tests or scope.
- Keep changes surgical if you must modify code or tests; avoid refactors unrelated to verification.
- Define explicit success criteria and map each to a concrete check.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.

When a current plan is the subject, use **plan verification mode**: review, critique, and refine the plan; run small investigations if needed; then return a fresh, improved plan.
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

### 1) Establish scope and criteria

- Identify the recent changes or claims to verify.
- Extract acceptance criteria, expected behavior, invariants, and risk areas.
- Ensure every relevant change, decision, and assumption is explicitly reviewed; do not leave gaps.
- Run preflight checks first (`pwd`, required tools, path existence, and test entrypoints).
- Ask minimal clarifying questions only when requirements are ambiguous.
- Note what would constitute proof of correctness vs. "good enough."
- If verifying a plan: capture the current plan, its goals, constraints, and why it is being proposed now.

### 2) Plan verification probes

- Map each criterion to a concrete check (tests, manual steps, logs, queries, static analysis).
- Prefer fast, focused probes first; include regression checks around touched areas.
- Prefer `uv run pytest` over bare `pytest` unless the repo explicitly uses another test runner flow.
- For long-running checks, use explicit timeouts and capture logs to a temporary artifact path for later review.
- Treat "no tests collected" as a coverage signal that requires adjustment, not as a pass.
- If basics fail, stop early and fix before scaling the verification effort.
- Prefer production-like configurations and real datasets when feasible; document data sources and constraints.
- Keep a lightweight verification log in `plan/current/verify.md` (untracked) with probes and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
- Track a minimal verification matrix of configs/perspectives already covered to avoid repeats.
- Use `plan/` as scratch space for ad-hoc experiments; create it only if permitted, remove any that are no longer needed, and never commit it. If you cannot create it, keep temporary notes in memory and call it out in the report.
- Keep `plan/` untracked and never commit it.
- For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

### 2b) Plan verification mode (when the subject is a plan)

- Review the plan for completeness, ordering, dependencies, and feasibility.
- Challenge assumptions against prior conversation context and known constraints.
- Identify missing steps, risky leaps, vague items, or unclear ownership/exit criteria.
- Run small investigations or experiments when they materially reduce uncertainty.
- Produce a refreshed plan with explicit steps, dependencies, and verification points.

### 3) Execute and gather evidence

- Run the smallest checks that validate each claim.
- Add targeted tests or reproducible steps when gaps exist.
- Create small, isolated experiments or standalone tests when they give clearer evidence.
- Record commands, configs, and results in the verification log.
- After any fixes, re-run the smallest relevant probes to confirm no regression.

### 4) Evaluate and close gaps

- Compare outcomes to criteria; mark verified, failed, or unknown.
- If unknown, design an additional probe or request missing context.
- If failures appear and the user wants fixes, fix and re-run relevant probes.

### 5) Report

- Summarize verified items, remaining risks, and confidence level.
- Call out critical red flags and any regressions introduced during verification.
- List evidence (tests run, steps, outputs, artifacts).
- Note follow-up items and any limitations.
- If plan verification mode was used, include the refreshed plan as a full replacement copy.
- Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
- Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- Avoid repeating the same probes; add new perspectives or deeper edge cases.
- Update the verification log and carry forward unresolved items.
- Re-run the minimal subset needed to confirm no regression when new changes land.
- Expand only as needed: vary configs, environments, or perspectives when risk warrants it.
- If re-invoked, follow prior suggested next steps or take a fresh angle; both are acceptable.
