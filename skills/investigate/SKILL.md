---
name: investigate
description: Deep, meticulous investigation of a problem, issue, or topic by forming hypotheses, gathering evidence, and testing empirically. Use when the user asks to investigate, deep dive, research, debug complex behavior, understand a codebase thoroughly, or build high confidence in an explanation or solution.
---

# Investigate

## Overview

Deep dive into a topic or issue by exploring hypotheses, validating them with evidence, and iterating until confidence is high. First build confidence in the current state, then confirm the proposed change is the right thing to change. Be relentless and keep going until you reach the bottom of the topic or problem, even if it takes a long time. Conduct a deep, thorough investigation that reviews all relevant changes, decisions, and assumptions and reasons through them explicitly.

Prefer empirical investigation with real data and real runs when relevant. Avoid mock or stub data unless there is no alternative; if you must use non-real data, explain why and what risk it introduces.

## Behavioral guardrails (must follow)

- State assumptions explicitly; if multiple interpretations exist, list them instead of picking one silently.
- Prefer the simplest explanation and test it first; avoid speculative detours.
- Keep any code changes or experiments minimal and scoped to the investigation.
- Define clear success criteria for what would confirm or falsify a hypothesis.
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
- Treat `docs/` as long-lived, evergreen guidance; prefer updating existing entries over adding new files.
- If `docs/decisions.md` is missing, prefer using the `setup` skill to create it when allowed. If you cannot create docs, capture rationale in the smallest durable local place (code comments or tests) and call out the missing decision doc in the report.

## Workflow

### 1) Frame the investigation

- Identify the central question, scope boundaries, and success criteria.
- Establish the current-state baseline (observed behavior, metrics, reproducible steps).
- Enumerate known facts, uncertainties, and potential risks.
- State what is expected to change vs what must remain stable.
- If the problem definition is weak or mismatched to evidence, re-scope early.
- Ask minimal clarifying questions only when requirements are ambiguous.
- Assume the investigation continues until the core questions are fully resolved or every reasonable avenue is exhausted.

### 2) Build a hypothesis map

- List plausible explanations or models; rank by likelihood and impact.
- Note what evidence would confirm or falsify each hypothesis.
- Track a lightweight investigation log in `plan/current/investigate.md` (untracked) with hypotheses, probes, and outcomes. If `plan/` cannot be created, keep a lightweight in-memory log and call it out in the report.
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

### 6) Report

- Provide a concise summary of findings, confidence level, and remaining risks.
- Call out critical red flags or regressions discovered during the investigation.
- List evidence (tests run, steps, outputs, artifacts) and what they show.
- Explicitly answer whether the proposed change is the right thing to change, backed by evidence.
- Include next steps and open questions.
- Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
- Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- Continue from prior logs; carry forward unresolved items and evidence.
- Expand coverage gradually: vary configs, environments, or perspectives when risk warrants it.
- Always provide a summary of all investigations completed so far, including confirmations or reversals.
- If re-invoked, follow prior suggested next steps or take a fresh angle; both are acceptable.
- Treat repeat invocations as a mandate to push deeper until the topic is fully understood.