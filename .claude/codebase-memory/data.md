# data — Swing Trading

Last updated 2026-07-15. Canonical home for data/schema standards. The
Trading-read-only + EOD-only rules are also always-load INDEX invariants.

## Data layer (M0.2, DECIDED 2026-07-08 — own fetcher, NOT price_cache reuse)
- `swing_bot/prices.py` fetches full OHLCV (`auto_adjust=False`) into `swing.db`
  table `bars` (PK ticker,date; open/high/low/close/adj_close/volume). Decision
  rationale in architecture.md: Trading's price_cache stores only close+volume
  (no OHLC → IBS uncomputable) and lacks DIA/IWM + country ETFs. `swing.db` also
  holds positions/NAV/results (M3+).
- **Adjustment convention**: split-adjusted, dividend-UNadjusted (`auto_adjust=
  False`). Any script touching price data STATES its convention in a header comment.

## Invariants
- **EOD data only**: signal at close, execute next open. No intraday logic until
  an intraday source exists.
- Trading's repo/DB is **READ-ONLY** from here; never run backtests concurrently
  against it. If reading Trading's price_cache, honor split-adj/div-unadj in
  every consumer.
- **Liquidity floor is MANDATORY** in any universe filter — at $100–1,000 capital,
  spread/slippage dominate.
