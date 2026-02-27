---
name: investigate
description: Deep, meticulous investigation of a problem, issue, or topic by forming hypotheses, gathering evidence, and testing empirically. Use when the user asks to investigate, deep dive, research, debug complex behavior, understand a codebase thoroughly, or build high confidence in an explanation or solution.
---

# Investigate

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
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.
- Compound knowledge continuously: keep `docs/` accurate and up to date, and promote durable learnings and decisions from work into docs.

## Long-task checkpoint cadence

- For any non-trivial task (including long efforts), run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone with commit-eligible changes, and at least once per major phase, invoke `git-commit` to create a small logical checkpoint commit once relevant checks are green and repo policy permits commits.
- At the same cadence, invoke `organise-docs` whenever durable learnings/decisions appear, and prune stale `plan/` scratch artifacts.
- If either checkpoint is blocked (for example failing checks or low-confidence documentation), resolve or record the blocker immediately and retry before expanding scope.

## Overview

Deep dive into a topic or issue by exploring hypotheses, validating them with evidence, and iterating until confidence is high. First build confidence in the current state, then confirm the proposed change is the right thing to change. Be relentless and keep going until you reach the bottom of the topic or problem, even if it takes a long time. Conduct a deep, thorough investigation that reviews all relevant changes, decisions, and assumptions and reasons through them explicitly.

Prefer empirical investigation with real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.
For experiment-heavy work, prioritize maximizing learning throughput: focus on high-information findings and actionable next experiments.

## Required output contract (must follow)

Always deliver the final report with all sections below, in this order:

1. Findings summary.
2. Source ledger.
3. Coverage gaps and explicit unknowns.
4. Ship/no-ship recommendation with risks.
5. Evidence runbook (commands/tests/artifacts).
6. Next steps.

Apply these requirements:
- Do not make a material claim without a corresponding source-ledger entry.
- Keep source-ledger entries concrete and auditable with fields:
  - `where_found`: exact location (file path, system, channel, or artifact name).
  - `link`: clickable URL or workspace path.
  - `confidence`: `high`, `medium`, or `low` plus brief reason.
  - `relevance`: why the source matters to the central question.
- List unresolved questions explicitly under coverage gaps and unknowns.
- End with a binary recommendation: `ship` or `no-ship`.
- For `ship`, list residual risks and mitigation/monitoring actions.
- For `no-ship`, list blocking risks and what evidence is required to flip to `ship`.

## Behavioral guardrails (must follow)

- Proceed without permission for standard in-scope steps (read/scan/summarize/plan/tests/edits/analysis). Ask clarifying questions only when requirements are ambiguous, missing inputs, or a risky decision cannot be inferred. Require explicit approval only for destructive/irreversible actions, executing untrusted code or installers, remote-state changes (push/deploy/publish), or changes outside the repo environment.
- Default write scope is the current `cwd` and its subdirectories.
- Read-only inspection outside the current `cwd` is allowed when needed for context; do not modify outside the `cwd` tree unless the user explicitly requests it.
- Run a preflight before substantial work: confirm the expected `cwd`, verify required tools with `command -v`, and verify referenced files/directories exist before reading or searching them.
- State assumptions explicitly; if multiple interpretations exist, list them instead of picking one silently.
- Prefer the simplest explanation and test it first; avoid speculative detours.
- Keep any code changes or experiments minimal and scoped to the investigation.
- Define clear success criteria for what would confirm or falsify a hypothesis.
- For public/open-source repos, include checks for secrets, sensitive data, and local system paths in affected outputs and files.
- Prefer quoted paths and explicit path checks when running shell commands to reduce avoidable glob/path failures.
- If an environment variable is required, check whether it is already set before asking for it or stating it is missing.
- If there is nothing left to do, say so explicitly and stop.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Evidence that the proposed change is the correct lever (and why alternatives were rejected).
- Your recommendation and the reasoning behind it.

## Rationale capture

When you fix an issue, make a change that resolves an issue, or reach an important decision, capture the "why" in a durable place (code comments, docs, ADR, or tests). Do not rely only on `plan/` scratch notes. In your report, mention where the rationale was recorded.

## Plan/docs/decisions robustness

- Treat `plan/` as short-term scratch and never commit it.
- If `plan/` is missing, create it (and any needed subdirs) only when edits are permitted; otherwise keep a lightweight in-memory log and state in the report that plan logging was not persisted.
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing docs when they have a clear home, but create new focused docs/subdirectories when it improves navigability (and link them from related docs or indexes).
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

### 1) Frame the investigation

- Identify the central question, scope boundaries, and success criteria.
- Establish the current-state baseline (observed behavior, metrics, reproducible steps).
- Run preflight checks first (`pwd`, required tools, and path existence for any targeted files/directories).
- Enumerate known facts, uncertainties, and potential risks.
- State what is expected to change vs what must remain stable.
- If the problem definition is weak or mismatched to evidence, re-scope early.
- Ask minimal clarifying questions only when requirements are ambiguous.
- Assume the investigation continues until the core questions are fully resolved or every reasonable avenue is exhausted.

### 2) Build a hypothesis map

- List plausible explanations or models; rank by likelihood and impact.
- Note what evidence would confirm or falsify each hypothesis.
- Track a lightweight investigation log in `plan/current/investigate.md` (untracked) with hypotheses, probes, and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
- For parallel investigations, maintain `plan/current/notes-index.md` and `plan/current/orchestrator-status.md` so hypotheses, owners, and evidence pointers stay synchronized.
- Use `plan/` as scratch space for ad-hoc experiments; create it only if permitted, remove any that are no longer needed, and never commit it. If you cannot create it, keep temporary notes in memory and call it out in the report.
- Keep `plan/` untracked and never commit it.
- For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

### 3) Gather evidence

- Read code, logs, configs, and docs relevant to each hypothesis.
- Collect direct evidence of the current behavior (tests, logs, metrics, traces, repro steps).
- Use external sources when needed (specs, papers, vendor docs, standards).
- Prefer primary sources and record versions/dates in the investigation log.

### 4) Test empirically

- Create independent, standalone probes and experiments where relevant.
- Prefer small, isolated tests first; stop early and fix if basics fail.
- Reproduce the baseline before testing changes; compare control vs treated when possible.
- Record commands, configs, and outcomes; re-run minimal probes after any fixes.

### 5) Synthesize and iterate

- Compare evidence against the hypothesis map; mark supported, weakened, or falsified.
- If gaps remain, design new probes or broaden the search.
- Avoid repeating the same probes across invocations; add new angles instead.
- If evidence is inconclusive or conflicting, state uncertainty and seek additional data.
- Do not conclude early; keep iterating until the investigation is genuinely exhausted or the root cause is fully understood.
- If evidence suggests the proposed change is not the right target, pivot and update the plan.
- When confidence is high, recommend concrete follow-up experiments/actions immediately; if confidence is low, explicitly call out what is needed before acting.

### 6) Report

- Provide a concise summary of findings, confidence level, and remaining risks.
- Call out critical red flags or regressions discovered during the investigation.
- List evidence (tests run, steps, outputs, artifacts) and what they show.
- Explicitly answer whether the proposed change is the right thing to change, backed by evidence.
- Provide the report using the required output contract sections and order.
- Include next steps and open questions.
- Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
- Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- Continue from prior logs; carry forward unresolved items and evidence.
- Expand coverage gradually: vary configs, environments, or perspectives when risk warrants it.
- Always provide a summary of all investigations completed so far, including confirmations or reversals.
- If re-invoked, follow prior suggested next steps or take a fresh angle; both are acceptable.
- Treat repeat invocations as a mandate to push deeper until the topic is fully understood.
- If a repeat pass has no new evidence, stop and report that further investigation would be low-yield until new inputs appear.
