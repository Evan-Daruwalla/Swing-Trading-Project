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
