# Pre-registration — E8: Volatility-compression breakout ("squeeze")

**Written 2026-07-10, BEFORE any runner code exists. This document is the
experiment. Committed doc-only; the commit hash of this file predates the
runner, per program discipline.**

## Motivation and provenance

Sourced from the r/swingtrading thread Evan supplied 2026-07-10 (record
Appendix AL): the OP's own TTM-squeeze setup. This is a genuinely NEW family
for this program — E1–E7/E3 covered mean reversion, trend rotation, and
cross-sectional momentum; **breakout / volatility-expansion was never
tested.** That novelty is the only reason this runs: it is information, not
parameter fishing. A priori prior: POOR (program base rate 0/8; breakout
systems on liquid indices post-2000 are historically weak).

## Universe and data

- Frozen 29-ETF universe (`swing_bot/universe.py`, frozen 2026-07-08),
  coverage-gated: a ticker is eligible once its `data_start` + warmup allows
  indicator computation. Liquidity floor inherited from the frozen universe.
- Data: yfinance `auto_adjust=False` → split-adjusted, dividend-UNADJUSTED
  (program convention). Fetched LIVE from ticker inception; **no writes to
  swing.db** (protects the frozen-regression refs).
- EOD only: signal at close t, execute next open (t+1). Hard rule.

## Exact rules (all fixed a priori — no tuning after results)

Indicators (daily):
- SMA20 = 20-day simple mean of close; σ20 = **population** std of last 20
  closes; Bollinger = SMA20 ± 2.0·σ20.
- EMA20 of close (α = 2/21, seeded with SMA of first 20 closes).
- TR_t = max(high−low, |high−prev_close|, |low−prev_close|);
  ATR20 = 20-day simple mean of TR; Keltner = EMA20 ± 1.5·ATR20.
- **Squeeze ON** at t: upperBB < upperKC AND lowerBB > lowerKC.

Entry (long-only; shorting excluded a priori — small account, and all prior
research says the short side of US equities is structurally worse):
- Signal at close t when: squeeze was ON for ≥5 consecutive sessions ending
  t−1, squeeze is OFF at t, and close_t > SMA20_t (breakout is upward).
- Buy next open. Max K=3 concurrent positions (concentrated per goal), one
  position per ticker. If signals exceed free slots, rank by
  (close_t/SMA20_t − 1) descending.

Exit:
- Signal at close t when close_t < EMA20_t, OR hold ≥ 40 trading days since
  fill. Sell next open. Positions open at data end are marked to last close
  and flagged.

Sizing and costs:
- Initial capital $1,000; position size = min(cash, NAV/3) at entry
  (NAV-compounding, engine-v2 convention — the economically meaningful one
  for a CAGR gate). Costs 5 bps/side (program standard).

## Windows and gates (kill-criteria — any miss = FAIL)

- **Gate window: 2000-01-01 → 2013-12-31** (the hostile regimes decide).
  - CAGR ≥ 15%  AND  NAV maxDD ≤ 60%.
  - Interpretability floor: n_trades ≥ 30 in the gate window; fewer →
    INCONCLUSIVE (not PASS, not FAIL).
- **Secondary window: 2014-01-01 → data end.** Reported always. An overall
  PASS additionally requires CAGR ≥ 15% and maxDD ≤ 60% here too.
- No parameter may be changed after seeing any result. A FAIL closes the
  squeeze family for this program absent a new dated Evan decision.

## Disclosed limitations

- Dividend-UNADJUSTED closes understate long-hold returns slightly
  (consistent across the whole program; biases against the strategy and the
  benchmark equally).
- Universe inception staggering means the early gate window trades fewer
  tickers (~20 eligible in 2000 vs 29 by 2018) — disclosed, not corrected.
