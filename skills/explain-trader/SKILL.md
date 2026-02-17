---
name: explain-trader
description: Explain the current topic in HFT/quant/trader terms (PnL, risk, exposure, execution, microstructure, latency, liquidity, limits, failure modes) while preserving all important details and nuances. Use for quant/trading projects when the user wants a trader-perspective explanation of technical work (code, model/ML components, math/stats, infrastructure, incidents, experiments, research results, design decisions), especially when live-trading step-by-step behavior matters (inflight fills, cancel/replace races, queue position), or to translate non-trading terminology into what matters for running a book.
---

# Explain Trader

## Overview

Translate whatever the team is discussing into the language of trading: what it means for alpha, PnL, risk, costs, and operational reality.

Optimize for fidelity: keep all the details, but frame them as a trader would evaluate them (edge cases, constraints, failure modes, and the practical implications for a strategy/book).

## Multi-agent collaboration

- Encourage use of multiple agents/subagents when it is likely to improve speed, quality, or confidence.
- Split work into clear packets with owners, inputs, acceptance checks, and a synthesis step when parallelizing.
- Use single-agent execution when scope is small or coordination overhead outweighs gains.

## Proactive autonomy and knowledge compounding

- Be proactive: immediately take the next highest-value in-scope action when it is clear.
- Default to autonomous execution: do not pause for confirmation between normal in-scope steps.
- Request user input only when absolutely necessary: ambiguous requirements, material risk tradeoffs, missing required context that would make the explanation wrong, or destructive/irreversible actions outside policy.
- Treat iterative execution as the default for non-trivial work; run adaptive loop passes until completion criteria are met.
- Keep looping until actual completion criteria are met: all material details from the source topic have a clear trader framing (or are explicitly marked as unmapped/unknown), and the explanation is internally consistent.
- Run `organise-docs` frequently during execution to capture durable decisions and learnings, not only at the end.
- Create small checkpoint commits frequently with `git-commit` when changes are commit-eligible, checks are green, and repo policy permits commits.
- Never squash commits; always use merge commits when integrating branches.
- Prefer simplification over added complexity: aggressively remove bloat, redundancy, and over-engineering while preserving correctness.

## Long-task checkpoint cadence

- For any non-trivial task, run recurring checkpoint cycles instead of waiting for a single end-of-task wrap-up.
- At each meaningful milestone: (1) update durable docs when warranted (`organise-docs`), (2) checkpoint with a small commit when eligible (`git-commit`).

## Workflow (Always Follow)

### 0) Build a detail inventory (do not lose information)

Before translating, extract a complete inventory of the source content:
- terms of art, variables, components, and claims
- assumptions (explicit and implicit)
- constraints and invariants
- edge cases and failure modes mentioned
- any numbers/thresholds/units that matter

Use the inventory to ensure every item gets translated or explicitly marked as unmapped/unknown.

### 0.1) Route the topic (pick the trader lens that preserves causality)

Choose the primary topic type(s). This determines which parts of the book-impact pass must be most explicit.

- signal/model/research result: prioritize alpha quality, decay, costs/turnover, and regime fragility
- execution/microstructure: prioritize slippage/adverse selection, fill probability, and capacity constraints
- hft/latency-critical live behavior: prioritize event timelines, order-state races (ack/fill/cancel), inflight exposure, and matching-engine realities
- risk/limits/sizing: prioritize exposures, tail scenarios, and limit consumption / breaches
- data pipeline/backtest plumbing: prioritize fake-PnL risks (leakage, timestamps), staleness, and reproducibility
- infra/reliability: prioritize operational failure modes (duplicate/stale orders, missing data) and kill-switch/monitoring
- incident/postmortem: prioritize worst-case book impact, blast radius, detection, prevention controls, and recovery steps

If multiple apply, say so and cover the union of required audits.

### 1) Lock the trading frame (state assumptions explicitly)

If the user did not specify these, assume generic “systematic trading” and state the assumptions you chose.

Cover, at minimum:
- instrument/asset class + venue (if known)
- horizon/holding period and how often decisions are made (if known)
- objective (e.g., market-neutral alpha, directional, carry, stat-arb, MM)
- constraints: leverage, liquidity/ADV, borrow/shorting constraints, risk limits, latency/throughput, capital allocation
- what “good” looks like: PnL distribution, drawdown tolerance, turnover and costs, tail behavior, stability across regimes

Ask at most 3 clarifying questions only if the explanation would otherwise be materially wrong (e.g., the difference between HFT execution constraints vs daily rebal).

### 1.1) If latency matters: do a live timeline replay (step-by-step)

Trigger this step when any of the following are true:
- the system is HFT-ish (sub-second decisions, market making, latency-sensitive execution), or
- the topic mentions latency/throughput, order router behavior, cancels, partial fills, acks, or “inflight”.

Write a concrete timeline as if running live. Include the order state transitions and the race conditions:
- data arrival -> signal decision -> order placement -> exchange/broker ack -> fills (partial/full) -> cancels -> cancel acks
- what can arrive out of order (fill before cancel ack, late acks, duplicate events)
- what is “inflight” at each step (open orders + pending cancels + unacknowledged orders)
- how exposure can temporarily exceed intent (partial fills during cancel, stale cancels, hedges lagging)

Translate the implications:
- PnL: adverse selection / slippage when you are late; phantom PnL when marks lag fills
- risk: transient gross/net spikes, limit breaches, unhedged legs, inventory drift
- ops: what monitoring catches it (fill/ack latency distributions, cancel reject rate, order state divergence)

### 2) Identify what the thing “is” in trading terms

Restate the subject in trader vocabulary, using the frame above:
- if it’s a model/signal: what information edge it’s trying to capture; what position/exposure it induces
- if it’s infrastructure: what part of the pipeline it protects (data integrity, latency, uptime) and what kind of trading risk it reduces
- if it’s research/experiment: what hypothesis about alpha/cost/risk it tests
- if it’s a bug/incident: what could have happened to the book (wrong risk, wrong sizing, missed fills, stale prices, phantom PnL, bad hedges)

### 3) Do a full “book impact” pass (do not skip details)

Explain impact across the stack a trader cares about:
- alpha: expected edge, decay, regime dependence, feature leakage, crowding/arb risk
- PnL: what moves the mean and what moves the variance; where PnL can be illusory (marking, stale prices)
- risk: factor exposures, tail risk, correlation spikes, gap risk, concentration, hidden leverage
- costs: spread, fees, slippage, market impact, borrow/financing, turnover
- liquidity: participation, ADV constraints, fill probability, partial fills, outage behavior
- sizing: how it affects notional, risk parity, constraints, and limit consumption
- execution: order types, latency sensitivity, adverse selection, queue position (if relevant)
- ops: monitoring, alerting, kill-switch triggers, fallbacks, manual intervention playbooks
- governance: “what could go wrong” controls, limits, and how to detect it early

If the topic includes “minor” implementation details, translate each into a trading implication, even if it is small (e.g., a timestamp bug is “stale signal risk”; a retry loop is “duplicate orders risk” unless idempotent).

When helpful, consult:
- `references/translations.md` for common ML/stat/infra term mappings
- `references/checklist.md` for a second-pass trader completeness audit
- `references/examples.md` for concrete translation patterns

### 4) Preserve fidelity with an explicit term-mapping appendix

End with a short appendix that maps the original terms to trader terms so no detail is lost.

Rules:
- Keep the main explanation in trader terms.
- The appendix can mention original terms, but must be a true correspondence (no hand-waving).
- If something does not map cleanly, say so and describe the nearest trading analogue plus what is missing.

Preferred appendix format (table is best when there are many terms):
- original term / component
- trader translation
- book impact (PnL/risk/cost/ops)
- failure mode if wrong

## Output Template

Use this structure unless the user asks otherwise:

1) Trading frame (assumptions + constraints)
2) What this is (in trading terms)
3) What it does to the book:
   - alpha / signal quality
   - pnl distribution (mean/var) and where pnl can be fake
   - risk (including tail + regime)
   - costs/turnover/liquidity
   - execution and operational failure modes
   - controls/limits/monitoring that matter
4) Edge cases and “how this breaks”
5) Term-mapping appendix (original -> trader)

## Heuristics (Use Trader Defaults)

- Prefer concrete “if X then the book experiences Y” statements over abstract theory.
- When uncertain, bound the outcome: best case, base case, and worst case for PnL/risk/ops.
- Always call out hidden assumptions (e.g., stable borrow, stable correlations, continuous liquidity).
- Avoid “math first” explanations; translate math into what it means for edge stability, limits, and failure modes.
- Spend time thinking: consider multiple trader framings and choose the one that best preserves the true causal story.
- When numbers exist, keep them: translate units into bps, dollars, risk units, participation, and limit usage (not “metric improved”).
- If you have to speculate, label it and keep it bounded; never present unknowns as certain.
- For HFT/latency-sensitive topics, always include a live step-by-step replay with order-state races and inflight exposure; do not compress this into “execution risk”.

## Completeness Gate (Run a Second Pass)

After writing the first draft, run a second pass:
- re-check the detail inventory and ensure every item is represented
- audit with `references/checklist.md` to catch missing book-relevant impacts
- tighten any vague mappings in the term-mapping appendix
