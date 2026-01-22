---
name: investigate
description: Deep, meticulous investigation of a problem, issue, or topic by forming hypotheses, gathering evidence, and testing empirically. Use when the user asks to investigate, deep dive, research, debug complex behavior, understand a codebase thoroughly, or build high confidence in an explanation or solution.
---

# Investigate

## Overview

Deep dive into a topic or issue by exploring hypotheses, validating them with evidence, and iterating until confidence is high. Be relentless and keep going until you reach the bottom of the topic or problem, even if it takes a long time.

## Decision framing

When a decision is required, always provide:
- Background context sufficient to make the decision.
- Pros and cons for each viable option.
- Your recommendation and the reasoning behind it.

## Workflow

### 1) Frame the investigation

- Identify the central question, scope boundaries, and success criteria.
- Enumerate known facts, uncertainties, and potential risks.
- Ask minimal clarifying questions only when requirements are ambiguous.
- Assume the investigation continues until the core questions are fully resolved or every reasonable avenue is exhausted.

### 2) Build a hypothesis map

- List plausible explanations or models; rank by likelihood and impact.
- Note what evidence would confirm or falsify each hypothesis.
- Track a lightweight investigation log in `plan/investigate.md` (untracked) with hypotheses, probes, and outcomes.
- Use `plan/` as scratch space for ad-hoc experiments; remove any that are no longer needed.
- Keep `plan/` untracked and never commit it.
- For large or long tasks, heavy use of the `plan/` scratchpad is strongly recommended; it is for agent use (not human) and can be used however is most useful.

### 3) Gather evidence

- Read code, logs, configs, and docs relevant to each hypothesis.
- Use external sources when needed (specs, papers, vendor docs, standards).
- Prefer primary sources and record versions/dates in the investigation log.

### 4) Test empirically

- Create independent, standalone probes and experiments where relevant.
- Prefer small, isolated tests first; stop early and fix if basics fail.
- Record commands, configs, and outcomes; re-run minimal probes after any fixes.

### 5) Synthesize and iterate

- Compare evidence against the hypothesis map; mark supported, weakened, or falsified.
- If gaps remain, design new probes or broaden the search.
- Avoid repeating the same probes across invocations; add new angles instead.
- If evidence is inconclusive or conflicting, state uncertainty and seek additional data.
- Do not conclude early; keep iterating until the investigation is genuinely exhausted or the root cause is fully understood.

### 6) Report

- Provide a concise summary of findings, confidence level, and remaining risks.
- Call out critical red flags or regressions discovered during the investigation.
- List evidence (tests run, steps, outputs, artifacts) and what they show.
- Include next steps and open questions.
 - Write the summary in plain, concise, and intuitive language with brief context so a new reader can follow it.
 - Avoid analogies; use simple, direct explanations and define any necessary technical terms.

## Repeat invocations

- Continue from prior logs; carry forward unresolved items and evidence.
- Expand coverage gradually: vary configs, environments, or perspectives when risk warrants it.
- Always provide a summary of all investigations completed so far, including confirmations or reversals.
- If re-invoked, follow prior suggested next steps or take a fresh angle; both are acceptable.
- Treat repeat invocations as a mandate to push deeper until the topic is fully understood.
