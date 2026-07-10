# Pre-registration — E3: concentrated stock momentum (falsification-only)

**Committed 2026-07-10 (PRD M2c), BEFORE the E3 runner exists. Parameters
FIXED. Evan opened this family 2026-07-10 (record Appendix AH).**

## 0. THE BIAS DISCLOSURE — read before any result

A stock backtest on yfinance data carries TWO biases that both inflate
returns and cannot be removed with available data:

1. **Survivorship:** yfinance has only currently-listed names. Companies that
   went bankrupt/delisted (Enron, Lehman, WorldCom, WaMu, old GM, Kodak…) are
   ABSENT. These deaths cluster in the crash regimes (2000–02, 2008) — so the
   backtest is MOST flattered exactly in the periods that decide robustness.
2. **Lookahead:** the universe below is stocks that EXIST TODAY, i.e. the
   survivors that succeeded. Selecting them is implicitly picking winners.

No point-in-time constituent data is available to fix either. **Therefore E3
is interpreted ONLY by asymmetric falsification:**
- A **FAIL** (especially in 2000–2013) is a CLEAN result: if concentrated
  momentum fails even with survivorship + lookahead + a favorable tape ALL
  working in its favor, the stock avenue is closed too.
- A **PASS** is UNINTERPRETABLE — it cannot be distinguished from the biases,
  and routes to the only survivorship-free test: forward live paper
  (Evan/Alpaca-gated). A backtest PASS authorizes nothing.

## 1. Universe (fixed; disclosed as survivor-selected)

~35 large-cap US stocks that traded continuously since 2000 and still trade,
spread across sectors to limit single-sector lookahead: MSFT INTC CSCO ORCL
IBM AAPL QCOM TXN ADBE · JPM BAC WFC C GS AXP · XOM CVX COP SLB · PG KO PEP
WMT MCD HD NKE DIS · JNJ PFE MRK ABT UNH · GE CAT BA MMM HON · T VZ. This set
is EXPLICITLY biased (all survivors); see §0.

## 2. Signal & rules (fixed)

- **Momentum:** at each rebalance, rank the universe by trailing **63-trading-
  day** total return (skip the most recent 1 day). Hold the **top K = 3**,
  equal-weight (concentration per the goal). Short holds: **rebalance every 10
  trading days** (~2 weeks).
- **Execution:** next-open fills on rebalance days; 5 bps/side; fractional
  shares; NAV-proportional sizing (engine v2 semantics).
- Long-only.

## 3. Windows

2000-01-03 .. 2013-12-31 (crash regimes — the GATE window), 2014-01-02 ..
2026-07-08 (bull), full. Benchmarks: equal-weight buy-hold of the universe,
and buy-hold SPY.

## 4. Kill criteria (fixed) — the GATE is the crash window

E3 "survives-even-flattered" only if, on **2000–2013** (next-open, 5 bps):
1. CAGR ≥ 15% (the high-return bar, matching E2/E4/E7), AND
2. max drawdown ≤ 65%.

Interpretation per §0: if it MISSES either → **FAIL, clean** → concentrated
stock momentum is closed (fails even with the biases in its favor, in the
regime that matters). If it MEETS both → **uninterpretable PASS** → the only
valid next test is forward live paper; no backtest claim is made.

Reported alongside (context): all three windows; vs equal-weight-universe and
SPY buy-hold; per-window %/mo.

## 5. No-change clause

§§1–4 frozen as of this commit. Ambiguities resolve to the most literal
reading, recorded, never toward better numbers. Any change is a new dated
pre-registration.
