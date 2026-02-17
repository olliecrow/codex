# Explain-Trader Translations (Trader Vocabulary Map)

Use this as a lookup when the topic includes ML/stat/infra terms. Prefer translating into:
- book outcomes (PnL mean/variance, drawdown, tail risk)
- constraints (limits, liquidity/capacity, execution)
- failure modes (ways you lose money or violate risk/controls)

Do not force a mapping when it is not faithful. If unmapped, say so and explain the nearest trading analogue and what is missing.

## Modeling / ML

- "model" -> "signal / forecast used to size or select trades"
- "features" -> "information inputs; what you think predicts returns/costs/risk"
- "labels" -> "what you define as the payoff you're trying to capture"
- "regularization" -> "penalize fragile edges; reduce overfit paper alpha"
- "hyperparameters" -> "how aggressive/complex the signal is; affects stability vs responsiveness"
- "overfitting" -> "edge that disappears when the tape changes; drawdowns after regime shift"
- "underfitting" -> "missing an edge; low hit-rate / weak separation"
- "train/val/test split" -> "paper trading on past data vs out-of-sample reality"
- "cross-validation" -> "repeated out-of-sample checks across different tapes/regimes"
- "online learning" -> "signal adapts during trading; risk of chasing noise / feedback loops"
- "batch training" -> "periodic retrain; risk of stale model between retrains"

## Common Metrics (Translate to Book Impact)

- "accuracy" -> "how often you classify a trade correctly; often misleading for trading"
- "AUC" -> "ranking power: whether high-score trades are better than low-score trades"
- "precision" -> "how many trades you take are actually good (avoids overtrading cost drag)"
- "recall" -> "how many good trades you capture (avoids leaving edge unused)"
- "false positives" -> "bad trades you take (cost + drawdown)"
- "false negatives" -> "good trades you miss (opportunity cost)"
- "calibration" -> "does score map to realized edge; matters for position sizing and limits"

## Data / Backtesting Pitfalls (Translate as Fake PnL Risks)

- "data leakage" -> "using information you wouldn't have live; fake backtest PnL"
- "lookahead bias" -> "same as leakage; trading with tomorrow's info"
- "survivorship bias" -> "removing losers; overstated PnL and understated drawdowns"
- "timestamp misalignment" -> "stale/early signals; can create leakage or missed fills"
- "stale prices" -> "phantom alpha; you cannot actually trade those marks"
- "label drift / concept drift" -> "edge decays as market changes; rising drawdowns"
- "distribution shift" -> "regime change; correlations/vol change; hedges stop working"

## Infrastructure / Systems (Translate to Operational and Trading Risk)

- "latency" -> "how long you wait while price moves away; slippage/adverse selection risk"
- "throughput" -> "can you keep up with the decision rate; missed trades / backpressure"
- "retries" -> "duplicate orders risk unless idempotent"
- "timeouts" -> "stale actions risk; cancel/replace storms; missed hedges"
- "inflight" -> "orders/cancels in motion; exposure you may not fully see yet"
- "ack" / "acknowledgement" -> "confirmation of order state; late acks create state divergence"
- "fill" -> "real inventory change; can arrive before your local state updates"
- "partial fill" -> "inventory drifts while you still have remaining exposure; impacts hedges/limits"
- "cancel/replace race" -> "you think you pulled risk, but you can still get hit"
- "idempotency key" -> "prevent duplicate orders during retries; limits duplicate-exposure risk"
- "eventual consistency" -> "temporary position/account mismatch; limit breaches if not guarded"
- "cache" -> "faster but can go stale; stale signal risk"
- "backfill" -> "fix historical data; can silently change research conclusions"
- "schema change" -> "silent feature break; can flip signal sign or scale"
- "precision/rounding" -> "pennies become bps at scale; sizing and limits drift"
- "clock skew" -> "wrong sequencing; can create leakage or stale orders"

## Research / Experimentation (Translate to Tradeability)

- "statistical significance" -> "is the edge likely real vs noise; but still must survive costs"
- "ablation" -> "which info input actually drives the edge"
- "robustness" -> "does it survive different regimes, venues, and cost assumptions"
- "paper trading" -> "simulated live; check that execution + data pipeline behave"
