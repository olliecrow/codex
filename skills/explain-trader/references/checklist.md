# Explain-Trader Checklist (Trader Completeness Audit)

Use this as a second-pass audit to avoid dropping "minor" but book-relevant details.
Apply only the sections relevant to the topic; do not invent facts when inputs are missing.

## A) Trading Frame

- Instrument/asset class and venue clear (or explicitly unknown)?
- Horizon and decision frequency stated (or explicitly unknown)?
- Strategy objective stated (market-neutral alpha, directional, carry, stat-arb, MM)?
- Primary constraints stated:
  - capital/leverage
  - liquidity/capacity (ADV, participation)
  - borrow/shorting constraints (if relevant)
  - risk limits (gross/net, factor, sector, duration, vega, etc.)
  - latency/throughput (if relevant)
- Definition of "good" stated:
  - expected PnL distribution and drawdown tolerance
  - turnover and costs
  - tail behavior
  - regime stability / robustness

## B) Alpha / Signal Quality

- What is the edge hypothesis in plain trading terms?
- What exposures does it induce (directional beta, sectors, rates, vol, FX, commodities)?
- What is the decay profile (minutes/hours/days)? What breaks it?
- Is there crowding/arb risk? Is it easily replicable?
- Is there leakage/contamination risk (lookahead, survivorship, timestamp alignment, stale marks)?
- Are "paper alpha" sources explicitly addressed (bad marking, unrealistic fills, missing fees)?

## C) PnL Mechanics (Where Mean/Variance Comes From)

- What pushes expected returns up/down?
- What increases variance (vol regimes, correlation spikes, jump risk)?
- What makes PnL illusory:
  - stale prices / wrong marks
  - smoothed signals that hide turnover
  - using mid when you cross the spread
  - ignoring borrow/financing
  - ignoring partial fills
- Is PnL decomposed at least conceptually:
  - alpha vs beta
  - carry/roll (if relevant)
  - execution / slippage drag
  - fees / financing / borrow

## D) Risk (Explicit + Hidden)

- Factor risk called out (beta, sector, size, value, momentum, rates, FX, vol)?
- Concentration risk (names, sectors, countries, single venues) called out?
- Tail risk scenarios:
  - gap risk, limit moves, trading halts
  - correlation going to 1
  - liquidity vanishing
- Hidden leverage sources called out (options convexity, leveraged products, correlated books)?
- Hedging assumptions stated (if any) and what happens when hedges fail?

## E) Costs, Turnover, Capacity

- Spread/fees/commissions included?
- Slippage and market impact explained as capacity limiter?
- Borrow/financing explicitly handled (if relevant)?
- Turnover implications tied to costs and risk limit usage?
- Capacity story stated:
  - what breaks first as you scale (impact, borrow, liquidity, limits)?

## F) Execution / Microstructure (If Relevant)

- Execution style implied:
  - cross vs passive
  - TWAP/VWAP/POV
  - order types and risk controls
- Adverse selection risk explained (getting filled when you're wrong)?
- Partial fills / queue position / cancel-replace behavior considered (if relevant)?
- Latency sensitivity stated (or explicitly not relevant)?

## F.1) HFT / Latency-Critical Live Behavior (If Relevant)

- Is there a step-by-step live timeline (data -> decision -> place -> ack -> fill -> cancel -> cancel ack)?
- Are order-state races covered:
  - fill arrives before cancel ack
  - partial fill during cancel
  - late ack or duplicate events
  - cancel reject / post-only reject handling
- Is “inflight” exposure accounted for:
  - open orders + unacknowledged orders + pending cancels
  - how risk/limits should treat inflight (worst-case fill assumptions)
- Are the main latency distributions named (even qualitatively):
  - market data latency
  - decision latency
  - gateway/router latency
  - exchange ack/fill latency
- Are the monitoring hooks specified:
  - fill/ack latency percentiles
  - order state divergence / reconcile loop health
  - cancel reject rate / replace churn
  - unexpected fill rate after cancel

## G) Operational Reality (Infra + Controls)

- Data integrity risks translated:
  - missing/late data -> stale signals / missed trades
  - duplicate data -> duplicate orders risk
  - timestamp bugs -> wrong sequencing / lookahead / stale alpha
- Idempotency addressed for:
  - retries
  - reconcilers
  - order placement and cancellations
- Monitoring/alerts:
  - what metrics would warn of decay or broken pipeline?
  - what triggers a kill-switch?
- Fallback modes:
  - if a component fails, do you stop trading or degrade safely?
- Governance:
  - which limits prevent worst outcomes?
  - which logs/audits allow postmortem reconstruction?

## H) Incident/Bug-Specific Audit (If Topic Is an Incident)

- Worst-case book impact bounded (PnL, risk, positions, missed fills)?
- Blast radius stated (which strategies/venues/accounts)?
- Detection: how would you notice live (PnL shape, exposure drift, fill anomalies)?
- Prevention: which control would have prevented it (limit, idempotency, validation, monitoring)?
- Recovery: how to unwind or freeze without making things worse?
