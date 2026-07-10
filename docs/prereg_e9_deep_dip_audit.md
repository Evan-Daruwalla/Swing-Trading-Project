# Pre-registration — E9: "Never book a loss" deep-dip audit

**Written 2026-07-10, BEFORE any runner code exists. Committed doc-only; the
commit hash of this file predates the runner, per program discipline.**

## Motivation and provenance

The most-upvoted strategy in the r/swingtrading thread Evan supplied
2026-07-10 (record Appendix AL): *"buy large caps at major support (≥20%
correction), sell at 15–20% profit, I have never booked losses."* E9
codifies that claim and runs it through 2000–2013 to measure what the
anecdote hides. This is an **audit with a dual readout**, pre-stated:

**A-priori predictions (written before any run):**
1. The "never book a loss" property will be (nearly) TRUE in realized terms
   — that is the seductive statistic.
2. The NAV will nonetheless show a LARGE unrealized drawdown and a CAGR well
   below the 15% bar, because capital idles waiting for rare 20%
   corrections, winners are capped at +15%, and losers are held uncapped
   through 50%+ crashes.

Either prediction failing is informative. Single stocks are excluded a
priori — a stock version is survivorship-poisoned (E3 lesson); ETFs are the
honest, survivorship-free reading of "large caps that won't death-spiral."

## Universe and data

- broad_us (SPY, QQQ, DIA, IWM) + the 11 SPDR sector funds from the frozen
  universe = 15 tickers, each eligible from its `data_start` (XLRE 2015,
  XLC 2018 → mostly absent from the gate window; disclosed).
- Data: yfinance `auto_adjust=False` (split-adjusted, dividend-UNADJUSTED),
  fetched LIVE from inception; **no writes to swing.db**. EOD only: signal
  at close, execute next open.

## Exact rules (fixed a priori)

- ATH_t = maximum close from series inception through t.
- **Entry** signal at close t: close_t ≤ 0.80 × ATH_t ("major correction"),
  no open position in that ticker, free slot. Buy next open. Max K=5
  concurrent positions (the commenter's "4–5"); if signals exceed slots,
  rank by close_t/ATH_t ascending (deepest correction first).
- **Exit** signal at close t: close_t ≥ 1.15 × entry fill (+15%, midpoint of
  the claimed 15–20%). Sell next open. **NO stop-loss, NO max hold** — that
  is the claim under test. Re-entry after exit allowed if conditions recur.
- Sizing: initial capital $1,000; size = min(cash, NAV/5). Costs 5 bps/side.
- Positions open at data end are marked to last close and flagged.

## Windows, gates, and audit metrics

- **Gate window 2000-01-01 → 2013-12-31** (high-return relevance):
  CAGR ≥ 15% AND NAV maxDD ≤ 60%. Any miss = FAIL for the program's
  high-return goal. Interpretability floor: n_closed_trades ≥ 10 in the
  gate window; fewer → INCONCLUSIVE.
- **Secondary window 2014-01-01 → data end**, reported always.
- **Audit metrics, reported regardless of verdict:** % of closed trades
  realized at a loss; worst per-position unrealized drawdown; longest hold
  (trading days); % of days with idle cash > 50% of NAV; open positions at
  data end and their unrealized P/L.
- No parameter changes after results. A FAIL closes the family absent a new
  dated Evan decision.

## Disclosed limitations

- Dividend-UNADJUSTED closes materially understate this strategy's returns
  (multi-year holds forfeit dividends in the accounting) — disclosed;
  direction of bias is AGAINST the strategy and stated up front.
- ATH from series inception: tickers born mid-bull (e.g. QQQ 1999) hit the
  −20% trigger relative to a young ATH — faithful to how a real trader using
  chart history would see it.
