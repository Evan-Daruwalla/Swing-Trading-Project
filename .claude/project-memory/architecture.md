# architecture — Swing Trading

- 2026-07-08: This project is SEPARATE from `D:\ClaudeCode\Trading` (Evan's
  decision 2026-07-08). Trading's repo and DB are read-only from here; never
  run backtests concurrently against Trading's DB.
- 2026-07-08 (M0.2, supersedes the earlier "OPEN — read price_cache read-only"
  entry): Data layer DECIDED = **own yfinance fetcher**, NOT price_cache
  reuse. `swing_bot/prices.py` fetches full OHLCV (`auto_adjust=False`) into
  `swing.db` table `bars` (PK ticker,date; open/high/low/close/adj_close/
  volume). Reason: Trading's `price_cache` (in `var/trades.db`) stores only
  `close`+`volume`+derived flags — NO high/low/open — so IBS is uncomputable
  from it; it also lacks DIA/IWM + all country ETFs and has zero `next_open`
  rows for ETFs. `swing.db` also holds positions/NAV/results (M3+).
- 2026-07-08: TOOLING — Grep/Glob tools do not reach `D:\ClaudeCode\Trading`
  (returns no matches despite files present). Access that repo's DB via
  venv-python sqlite (`file:...?mode=ro`) + PowerShell, not Grep/Glob.
  Trading DB path: `D:\ClaudeCode\Trading\var\trades.db`.
- 2026-07-08: Reuse targets identified (map, verify before use): Trading's
  `factor_backtest.py` harness, `paper_trader.py` DB schema (cadence-agnostic),
  `alpaca_client.py`/`alpaca_sync.py`/`fractionability.py` for the Alpaca
  PAPER mirror. NOT reusable: `paper_rebalance.py` monthly buy-top-N logic,
  the long-horizon factor set.
- 2026-09-05 (F3, record FN): **the liquidity floor and its enforcement are ONE
  unit, in `swing_bot/universe.py`.** `median_dollar_volume` MOVED there from
  `scripts/daily_swing_paper.py`, joined by `is_liquid` and `liquidity_mask`
  beside `MIN_MEDIAN_DOLLAR_VOL`. This was forced, not tidying:
  `daily_swing_paper.py` imports `run_e10_earnings_drift` and
  `run_c1_residual_reversal` at MODULE LEVEL, above where the function used to
  be defined, so any runner importing it back hit a partially-initialised module
  (record FG.4). `daily_swing_paper` re-binds both names so its own call site,
  `test_frozen`'s `median_dollar_volume_refuses_thin_sample` invariant, and
  `scripts/prove_liquidity_floor.py` all still reach them unchanged.
- 2026-09-05 (F3): **`SWING_F3_FLOOR` is the arm switch, defined once in
  `scripts/run_e8_squeeze.py` and shared** by every ETF runner, alongside
  `f3_masks` (index-keyed), `f3_masks_for` (raw bars) and `f3_masks_by_date`
  (date-keyed, for E20/X9 which key prices by date). Default ON. `=0` selects
  the pre-F3 path byte-for-byte. Every run prints which arm produced its
  numbers -- an unlabelled number from these engines is ambiguous against every
  result pinned before 2026-09-05.
- 2026-09-05 (F3): **`swing_bot/backtest.py` takes `liq=None` and None is the
  pinned path.** `test_frozen` calls `run_backtest()` without the argument, so
  the 12 references stay at d=+-0.0000pp BY DESIGN. Do not "simplify" that
  default away. `_load`'s SELECT still drops volume on purpose: widening its
  `(o,h,l,c)` tuple breaks every `bar[1]/bar[2]/bar[3]` index on the pinned
  paths, so E1's runner builds its mask from `swing.db` directly instead.
- 2026-09-05 (M13.1, record FQ): **`swing_bot/trading_calendar.py` is the M3
  loop's SECOND CLOCK** and the only module in the repo that deliberately reads
  no price data. `last_completed_session(now)` = the latest already-closed US
  session from the wall clock plus rule-derived NYSE closures (n-th weekday,
  Gregorian Easter for Good Friday, Sat->Fri / Sun->Mon observance, and the
  exception that Jan 1 on a Saturday does NOT close the prior Friday).
  `check_feed_clock(qdates[-1])` returns the refusal reason or None and is
  called at `daily_swing_paper.py:733-754`, BEFORE the VIX/VIX3M fetches, so a
  refusal costs no network. It refuses in BOTH directions (feed behind = the
  real bug; feed ahead = a partial row or a wrong calendar).
- **Why not Alpaca's calendar API** (asked and answered, do not "improve" it):
  the M3 DB ledger is independent of broker connectivity by design (the loop's
  docstring step 3) and a total credential outage is a logged real event
  (record FH). An Alpaca-sourced clock would turn that outage into a refusal to
  mark NAV, manufacturing the holes the guard exists to prevent.
- 2026-09-05 (M13.3, record FT): **the fidelity REPORT is split from the
  fidelity RESOLVING, on purpose.** `paper_sleeves.divergence_census(conn)`
  buckets every `fill_divergence` row (measured / resolved_no_price / dark /
  pending, mutually exclusive, summing to total) and lives beside
  `open_divergence_rows` -- the filter whose `alpaca_order_id IS NOT NULL`
  clause creates the darkness. `daily_swing_paper.print_divergence_census()`
  prints it and is called UNGATED at `:824`, beside the missed-session detector.
  **Do not "tidy" that call into `backfill_divergence`:** that function's only
  call site is inside `if args.execute:`, so the line would vanish from every
  dry run, which is precisely what M13.3 required it to survive.
