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

## Second data layer: `.e8e9_cache` (the research jungle; added to this bin 2026-08-13)
- `swing.db` is NOT the only store. `cache_fetch` in `scripts/run_e8_squeeze.py`
  is a permanent on-disk yfinance cache and is what the scripts/ runners
  actually read: **31** files import the module (30 runners + the standing
  proof script), 28 of them naming `cache_fetch`. `swing_bot/prices.py` →
  `swing.db` feeds the ENGINES and the live M3 loop; `cache_fetch` feeds the
  EXPERIMENTS. Same adjustment convention.
- Gitignored, 292 files in ONE filename namespace over THREE shapes: 181 bar
  lists (price series), 72 dicts (`*_div`, `ff3_daily`, `*_idx`, `fred_*`), 39
  lists of date strings (`*_earn`). Only the bar lists carry a vintage;
  `_last_bar_date` returns None for the other 111, so they are invisible to the
  freshness guard BY DESIGN.
- **FRESHNESS CONTRACT (2026-08-12, record EM/EO)**: entries are written on
  whatever day a ticker is first touched, so a universe assembled across
  sessions silently MIXES VINTAGES — that is what overstated M12's headline
  effect 3x. `_note_vintage` now raises `StaleCacheError` on a mixed vintage
  (≥2 distinct end-dates in one process) or a stale one (> `SWING_MAX_CACHE_
  STALE_DAYS`, default 5 calendar days, measured against the CLOCK). Mixed
  fires BEFORE stale.
- **Refreshing is all-or-nothing.** The write path is per-ticker and
  cache-miss-driven, no script enumerates the cache, and no refresh tool exists
  (none should be built). Deleting a subset and re-running one consumer just
  manufactures a NEW mixed vintage. Delete every price-series `*.json`, re-run
  every consumer in one sitting.

## Invariants
- **EOD data only**: signal at close, execute next open. No intraday logic until
  an intraday source exists.
- Trading's repo/DB is **READ-ONLY** from here; never run backtests concurrently
  against it. If reading Trading's price_cache, honor split-adj/div-unadj in
  every consumer.
- **Liquidity floor is MANDATORY** in any universe filter — at $100–1,000 capital,
  spread/slippage dominate.
