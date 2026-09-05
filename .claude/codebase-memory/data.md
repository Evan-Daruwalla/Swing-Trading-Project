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

## M3 paper ledger (added 2026-09-05, record FK/FL)
- **`paper_nav`'s primary key is `(sleeve, date)`.** Never aggregate it to a bare
  date set for a completeness check - see gotchas.md 2026-09-05. Coverage
  questions are per-sleeve questions.
- **The three sleeves do NOT have equal-length NAV series.** As of 2026-09-05:
  `e18_vixts` 36 marks, `m10_1_nagel` 36, **`e6_1x` 31** (2026-07-15 -> 09-03,
  103 rows total). Holes: 2026-07-30 across all three (record EI), plus
  2026-08-25, 08-26, 08-27, 08-28 and 08-31 for `e6_1x` only (record FJ).
  **All are ACKNOWLEDGED AS PERMANENT, not backfilled** (Evan, 2026-09-05,
  record FL) - forward evidence is not reconstructed after the fact. They live
  as `(sleeve, date)` pairs in `ACKNOWLEDGED_NAV_HOLES`
  (`scripts/daily_swing_paper.py`), still PRINTED every run but no longer
  failing it. **Consequence: any cross-sleeve return or NAV comparison MUST
  align on dates and must never assume equal series.**
- **Provenance caveat on the forward-paper evidence (record FL):** one
  unattributed write to the live ledger after 2026-09-01, bounded to two
  provably synthetic rows a landing-check agent left on 2026-08-25 (the fake
  `paper_nav` row implied a QQQ close of 812.00 against the same day's real
  ~710.7; the `ZZZZ` position had no matching transactions). The deletions match
  `clean_ledger_2026-08-25.py` exactly and the row arithmetic reconciles
  (86 + 17 marks over 08-26..09-03 = the 103 rows on disk). What happened is
  known and surgical; who ran it and when is not.
- **The liquidity floor now FAILS CLOSED** (2026-09-05, record FK): unmeasurable
  volume excludes the name rather than skipping the check. The INDEX invariant
  "liquidity floor is MANDATORY" was previously unenforceable on exactly the
  names most likely to need it.
