# Pre-registration — E20: Dividend capture

**Written 2026-07-11 (CST), BEFORE any runner code. Committed doc-only; this
hash predates the runner. M7b task 35; D1 dual-bar verdict.**

## Provenance and prior

Classic dividend-capture folklore: buy just before the ex-date to collect the
dividend, sell on the ex-date. The academic finding is that the ex-date price
drop ≈ the dividend (historically slightly less, tax-driven), so the gross
edge is tiny and costs/taxes eat it. **Prior: near-zero / negative net.** The
pedagogical value: the project's dividend-UNADJUSTED price convention is
finally exactly right for measuring an ex-date effect — but only if the
received dividend is credited to P&L (otherwise the ex-date drop looks like a
pure loss). This prereg fixes that accounting explicitly.

## Universe, data

- The 29 frozen-universe ETFs, from `.e8e9_cache` (split-adjusted,
  dividend-UNADJUSTED closes). Ex-dates + amounts from yfinance
  `Ticker(t).dividends` (cached). No swing.db writes. EOD.

## Exact rules (fixed a priori)

- For each ETF ex-date **E** (with dividend amount **D**): **buy at the close
  of the session before E** (price P0), **sell at the open of session E**
  (price P1). Holder of record across the ex-date **receives D**.
- **Per-trade net return** = (P1 − P0)/P0 + D/P0 − 2·(5 bps). (The D/P0 term
  is the dividend credit the dividend-UNADJUSTED prices omit.)
- Portfolio: each session, equal-weight across all ETFs whose ex-date is the
  next session; 1-session hold; compound NAV from $1,000. If N ETFs go ex on
  the same day, split capital N ways (cap N at 29).

## Windows and verdict

- **Gate 2000-01-01 → 2013-12-31.** **Secondary 2014 → end.**
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60% both windows. **PASS-RA:** gate
  Sharpe ≥ 0.80 AND > SPY buy-hold both windows AND +CAGR both. **FAIL:**
  neither. Floor: ≥ 30 capture trades in the gate window.
- Also reported (the real question): **mean net per-trade return** and win
  rate — is the ex-date effect > 0 after costs? No tuning after results.

## Disclosed limitations

- No tax modeling (dividends are taxed as income; capture is worse after tax —
  biases the real-world result below this backtest).
- yfinance dividend ex-dates are as-reported today; amounts are per-share,
  split-adjusted consistently with the price series.
- 1-session open-to-close-spanning-ex hold; no attempt to optimize the exit
  (that would be tuning).
