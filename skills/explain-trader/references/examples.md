# Explain-Trader Examples (Use As Patterns)

These are patterns, not scripts. Do not copy verbatim; adapt to the actual topic and preserve all real details.

## Example 1: Timestamp Alignment Bug (Data Pipeline)

Source-style statement:
"We found that feature timestamps were in local time, but price bars were UTC. We fixed it by normalizing to UTC before the join."

Trader framing:
- What this is: a data integrity bug that can create fake backtest PnL (implicit lookahead) or, live, stale/early signals depending on direction of skew.
- Book impact:
  - alpha: you might be “predicting” moves using information that wasn't actually available at decision time
  - pnl: paper Sharpe can be inflated; live PnL can mean-revert to zero and drawdowns appear “out of nowhere”
  - risk: exposures can drift because the signal is effectively shifted in time (wrong hedge timing)
  - ops: if monitoring is tied to expected hit-rate, you get false confidence until live performance breaks
- Failure mode if unfixed: you deploy a strategy sized off fake backtests; you hit risk limits during the first regime where timing matters (news/vol spikes).

Term-mapping appendix (example):
| original | trader translation | book impact | failure mode |
|---|---|---|---|
| "timestamp normalization" | "ensure the signal only uses information available before the trade" | prevents fake PnL | accidental lookahead, then live decay |
| "join" | "how the signal sees the tape at decision time" | changes signal timing | stale/early signal |

## Example 2: Model Metric Improvement (Research Result)

Source-style statement:
"AUC improved from 0.52 to 0.56 on validation; calibration got slightly worse."

Trader framing:
- What this is: the signal ranks trades better, but sizing confidence degraded.
- Book impact:
  - alpha: you may be better at selecting which trades to take (higher hit-rate or better payoff asymmetry), but not necessarily better at sizing
  - pnl: mean may improve if you keep trade frequency stable; variance may rise if miscalibration leads to oversizing losers
  - costs: if you “use” the extra ranking power by trading more, turnover and slippage can eat the gain
  - risk: worse calibration can concentrate risk unintentionally; you may breach per-name or factor limits faster
- What a trader asks next: what is the realized bps per trade after costs, and what happens to drawdown under stress regimes?

Term-mapping appendix (example):
| original | trader translation | book impact | failure mode |
|---|---|---|---|
| "AUC +0.04" | "better trade ranking / selection edge" | potential mean uplift | paper gain if costs dominate |
| "calibration worse" | "sizing confidence degraded" | risk/limit usage volatility | oversizing into losers |

## Example 3: Retry Logic in an Order Router (Infra/Reliability)

Source-style statement:
"We added retries around the order placement call to handle transient network errors."

Trader framing:
- What this is: reliability work that reduces missed trades, but can introduce duplicate/stale orders if not idempotent and bounded.
- Book impact:
  - execution: fewer missed fills in transient outages
  - risk: worst case is duplicate orders that blow through limits or create unintended net exposure
  - ops: you need monitoring for retry rate spikes and reconciliation to confirm broker/exchange state
- Controls that matter: idempotency keys, max retry budget, cancel-on-timeout behavior, hard risk limits enforced independently of the router.

Term-mapping appendix (example):
| original | trader translation | book impact | failure mode |
|---|---|---|---|
| "retries" | "avoid missed trades but risk duplicate orders" | reduces opportunity loss | double fills / limit breaches |
| "transient network error" | "uncertain order state" | needs reconcile | ghost orders / stale cancels |

## Example 4: Inflight Fill During Cancel (HFT Execution Nuance)

Source-style statement:
"We observed fills arriving after we sent cancels; sometimes the cancel ack was delayed. We added a reconcile loop and adjusted limit checks."

Trader framing:
- What this is: a normal microstructure race where you cannot assume cancel means risk is gone until you have the cancel ack (and even then, late fills/events can appear depending on venue/event ordering).
- Step-by-step live replay:
  - you place an order and it rests
  - you decide to cancel (signal changed or inventory limit)
  - before the cancel is acknowledged, you get partially (or fully) filled
  - your local system can briefly believe the risk is “pulled” while inventory actually increased
- Book impact:
  - PnL: if the market moved against you, these fills are adverse selection; if your hedging leg is delayed, you pay extra spread/impact
  - risk: transient gross/net spikes; breaches if limits ignore inflight worst-case fills
  - ops: without reconcile, you get persistent state divergence and repeated “mystery inventory”
- Controls that matter:
  - treat open + unacknowledged + pending-cancel quantity as inflight exposure for limits
  - reconcile against venue/broker truth; alert on divergence
  - measure cancel-to-ack and fill-to-report latencies; watch tails (p99/p999)

Term-mapping appendix (example):
| original | trader translation | book impact | failure mode |
|---|---|---|---|
| "cancel ack delayed" | "risk not actually pulled yet" | inflight exposure persists | limit breaches / inventory drift |
| "reconcile loop" | "position/order truth sync" | prevents ghost risk | repeated hidden exposure |
