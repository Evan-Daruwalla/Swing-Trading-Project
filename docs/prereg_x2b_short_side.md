# Pre-registration — X2b: Short-side / long-short days-to-cover, borrow-costed

**Written 2026-07-13 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. Follow-on to X2 (Evan authorized "do 1" = pursue the
short-side, 2026-07-13). Written against `docs/prereg_TEMPLATE.md`. MODIFIED-WINDOW
CAP + market-neutral pivot — see Windows.**

## Provenance and prior

X2 (record Appendix BU) found the short-interest anomaly **real and correctly
signed** on the modern liquid large-cap tape, but concentrated **entirely on the
short (high-DTC) leg** (high-DTC −2.63%/yr vs SPY +12.53%; long-short existence
spread +18.39%, Sharpe 0.98) — and therefore non-deployable long-only. X2b asks the
**deployability question honestly**: does the edge survive **realistic shorting
costs** — 5 bps/side trading AND stock-borrow fees? Working hypothesis (H1): the
long-short net of trading + a *realistic large-cap borrow* (≤ ~5%/yr) stays positive
with Sharpe ≥ 0.80. Null / rival (H0): **borrow eats it** — Muravyev-Pearson-Pollet
(JFE 2025) show short-side predictability is largely a **borrow-fee proxy**, so a
properly-costed short may be flat-to-negative. **Honest prior: genuinely uncertain,
leaning FAIL/marginal** — single window, market-neutral pivot away from the stated
high-return-long goal, and the borrow question is the whole ballgame.

## Data (in hand)

- Short interest: the X2 FINRA cache (`.finra_cache/short_interest.json`, 205
  biweekly settlement dates 2017-12-29→2026-06-30, 39/39 coverage, precomputed DTC).
- Prices: `.e8e9_cache` (split-adjusted, dividend-UNADJUSTED). No swing.db writes.
- **Borrow fees: NOT available free** (real per-name cost-to-borrow is paid — Ortex
  ~$129/mo, Evan-gated). **Handled by a BORROW-COST SWEEP** (0 / 2 / 5 / 10 / 20%
  annualized, accrued daily on short notional) to find the breakeven and bracket the
  unknown. This is the load-bearing honesty move: an un-borrow-costed short backtest
  would be dishonest.
- Lookahead guard: enter **10 trading sessions after the settlement date** (as X2).

## Exact rules (fixed a priori)

- **Signal:** rank the 39 by precomputed days-to-cover at each settlement date.
- **Two strategies, both next-open, 5 bps/side trading, biweekly rebalance, K=5:**
  1. **Pure short** — short the K highest-DTC names, equal-weight. Short P&L = −(price
     return) − borrow − trading.
  2. **Long-short (market-neutral)** — $1 long the K lowest-DTC + $1 short the K
     highest-DTC (2× gross on $1 net capital; dollar-neutral). Borrow accrues on the
     short $1 notional only.
- **Sizing:** equal-weight within each leg; NAV-proportional; no leverage beyond the
  1×/1× market-neutral gross (declared). Whole-share shorting (Alpaca has no
  fractional shorting) is NOT modeled — backtest assumes fractional shorts, an
  **upper bound**; the whole-share haircut at $1,000 is a disclosed limitation.
- **Time-stop baseline:** biweekly time stop (next rebalance); no price stop.
- **Costs:** 5 bps/side trading on every leg turnover; borrow swept as above; report a
  15 bps/side trading stress leg alongside.

## Windows and verdict [MODIFIED-WINDOW CAP + market-neutral bar]

- **Single window 2018–2026** (SI floor) → best achievable = **PROMISING**, never
  PASS-HR/RA. Floor ≥ 20 cycles (204 available).
- **Market-neutral bar** (SPY buy-hold is the wrong benchmark for a dollar-neutral
  sleeve): **PROMISING** iff, at a **realistic large-cap borrow of 5%/yr**, the
  long-short net has **positive CAGR AND Sharpe ≥ 0.80 AND** the yearly spread sign is
  **positive in ≥ 70% of calendar years** (robustness). **FAIL** otherwise. Report the
  full borrow breakeven (the borrow rate at which net CAGR → 0).
- **Asymmetric note:** survivorship works AGAINST the short leg (delisted
  shorted-crashers excluded) → results are a **lower bound** on the short-side edge;
  a FAIL here is therefore a strong close, a PROMISING is forward-only.

## Results-doc requirements

- **Cost ladder:** gross (0 trading, 0 borrow) → +5 bps trading → +borrow sweep
  (0/2/5/10/20%), for both the pure-short and long-short. The **borrow breakeven**
  (net CAGR = 0) stated explicitly.
- **Robustness:** per-calendar-year long-short return (stability); the short-leg
  **name concentration** (which high-DTC names drive the −2.63% — is it broad or a few
  blowups?); turnover.
- Frozen tripwire GREEN after (`.venv\Scripts\python.exe -m swing_bot.test_frozen`).

## Disclosed limitations

- **Borrow is swept, not measured** — real per-name cost-to-borrow (paid) would
  replace the sweep; the honest read is "survives iff borrow < breakeven."
- **Market-neutral pivot** from the stated high-return-long goal — a different
  strategy class (lower absolute return, higher Sharpe, needs shorting infra); the
  verdict informs, but does not itself authorize, that pivot (Evan-gated).
- **Single 2018–2026 window**, survivor universe (lower-bounds the short leg),
  fractional-short assumption (whole-share haircut real at $1,000), no borrow-supply
  constraint modeled (a heavily-shorted name can be hard-to-borrow / recalled — the
  exact tail the sweep's high end proxies).
- **Shorting itself is Evan-gated** — margin/borrow-capable account; nothing live
  without Evan + account.
