# gotchas — Swing Trading

All inherited 2026-07-08 from Trading's battle scars (source: Evan's
infrastructure inventory + Trading's `.claude/codebase-memory/gotchas.md`);
they apply to any yfinance-based pipeline built here:

- yfinance split-misapplication: a >1000% single-day move is the tell for a
  misapplied split, not a real return.
- Incomplete same-day publication: same-day coverage can sit at ~4,400/5,200
  tickers and never settle — gate freshness on coverage COUNT, not on "ran
  today".
- Friday-spike corruption and multi-year cache-gap phantom-ranking: both
  produce fake winners in rankings; universe quality filters
  (`factors/universe.py` in Trading) exist because of these.
- Survivorship bias: yfinance carries currently-listed names only — every
  backtest is upper-bound-biased. Short-horizon mean reversion is worst hit
  (delisted crashers are exactly what an RSI<30 buyer catches). No fix
  exists in the current stack; state it in every result.
- price_cache convention: SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED
  (`auto_adjust=False`). Every consumer must honor it or returns are
  silently wrong.
- Small-capital edges: Alpaca fractionability/minimum-order-size — the
  whole-share fallback in Trading's `fractionability.py` is load-bearing at
  $100–1,000, not an edge case.
- 2026-07-09 (E2, K=1 context run): `swing_bot/backtest.py` sizes positions
  at FIXED initial-capital/K dollars, NOT current-NAV/K — after losses it
  keeps buying full-size (implicit leverage; cash can go negative). At K=1
  on 3x funds NAV crossed zero (maxDD 104%). Immaterial for diversified 1x
  runs (E1/E1b); does NOT invalidate pinned refs (all experiments shared
  these semantics). Any FUTURE engine or live loop MUST size on current NAV.
- 2026-07-08 (M0.4, measured on our swing.db): XLRE has 19 zero-range bars
  (High==Low) in 2015-10..2016-02, its first ~5 months post-launch
  (illiquid early trading, not a split error). IBS=(close-low)/(high-low)
  DIVIDES BY ZERO on these. E1 signal code MUST skip any ticker on a day
  where high==low (treat IBS as undefined → no signal), not crash. All other
  28 universe tickers were clean in the M0.4 sanity scan (no OHLC-order
  violations, no |daily ret|>35%, no zero-range). Detector:
  `swing_bot/coverage_gate.sanity_scan`.
