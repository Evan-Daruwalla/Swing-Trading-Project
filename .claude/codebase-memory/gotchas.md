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
- 2026-08-13 (record EO, measured — the trap this project keeps setting for
  itself): **a `raise` added to a shared helper is inert until you check what
  CATCHES it.** `_note_vintage` was changed on 2026-08-12 to raise on a stale or
  mixed-vintage cache, and was proven to fire 5/5 in isolation — yet it was
  swallowed at three of its reachable sites. Worst was `cache_fetch`'s OWN retry
  loop: the `_note_vintage` call sat inside the `try:` that guards
  `prices.fetch`, so a vintage verdict was printed as `"{ticker} attempt N
  error"`, slept 20/40/60/80s, refetched 4x, and died as `"could not fetch"`.
  `run_m12_factorial` and `run_v1_harness_check` caught it per-ticker and
  `continue`d, so a uniformly stale cache EXCLUDED every name in turn — the
  guard turned "refuse to run" into "run on a silently emptied universe", which
  is strictly worse than the printing it replaced. Fixed by naming the error
  (`StaleCacheError(RuntimeError)`), moving the call out of the fetch `try`, and
  re-raising it in both consumers. **Rule: a broad `except Exception` around a
  call that can now raise a VERDICT must re-raise that verdict explicitly.**
  Residual: any FUTURE broad handler around `cache_fetch` re-opens this — the
  standing check is `scripts/prove_cache_guard.py` (8/8), which feeds the guard
  its trigger at every swallow site.
- 2026-08-13 (record EQ, proven by identity not assumption): **`scripts/` has no
  `__init__.py` and the repo root is on `sys.path`, so it is an implicit
  NAMESPACE PACKAGE — `import run_e8_squeeze` and `import scripts.run_e8_squeeze`
  both succeed and produce TWO DIFFERENT module objects with two different
  `StaleCacheError` classes.** `except StaleCacheError` then silently does not
  match and the guard is swallowed again. Today's consumers are safe (`m12` and
  `v1` both catch the identical class object — `is` returns True; zero hits
  repo-wide for the dotted form, confirmed by `grep -rn` and `git grep`). This
  applies to EVERY cross-script `except` in `scripts/`, not just the cache
  guard. Rule: import sibling scripts as bare `run_x`, never `scripts.run_x`.
- 2026-09-05 (record FK, measured): **the same "guard that cannot fire" family,
  in a new shape - AGGREGATION COLLAPSE.** `daily_swing_paper.py`'s
  missed-session detector read `SELECT DISTINCT date FROM paper_nav`, but that
  table's primary key is `(sleeve, date)`. Collapsing a composite key to one of
  its columns made a date count as covered when ANY ONE sleeve had written it,
  so the detector printed clean for 11 nights while `e6_1x` recorded nothing for
  2026-08-25, 08-26, 08-27, 08-28 and 08-31 and both peers recorded normally.
  The one real vanish it has ever had to catch was the one kind it structurally
  could not see. Fixed as a per-sleeve set difference over `ps.SLEEVES` reporting
  `(sleeve, date)` pairs. **Rule: never `DISTINCT` one column of a composite key
  and then treat presence as coverage - the aggregate is true when ANY member
  is, which is the opposite of what a completeness check needs.** Second half of
  the same fix: `ACKNOWLEDGED_NAV_HOLES` had to become pairs too, because a
  date-scoped acknowledgement forgives that date for every sleeve, re-creating
  the blindness inside the acknowledgement path.
- 2026-09-05 (record FK, measured): **a fail-open guard can be written INTO a
  docstring, and then the call site is bug-compatible with its own contract.**
  `median_dollar_volume()` returns None when fewer than `max(5, n//2)` sessions
  carry usable close AND volume, and its docstring instructed callers not to
  treat that as illiquid. The one caller obeyed - `if adv is not None and adv <
  FLOOR` - so a data-starved name (feed gap, halt, thin history) skipped the
  liquidity floor entirely and could enter the live K=4 stress basket. Both were
  fixed together; fixing only the call site would have left the next caller
  reading instructions to re-introduce it. Standing check:
  `scripts/prove_liquidity_floor.py` (6/6), which includes two cases asserting
  the OLD branch ranked those names. **Rule: when a helper returns "unknown",
  its docstring must say FAIL CLOSED, or the next caller will fail open with a
  clear conscience.**
- 2026-09-05 (record FK): **one malformed record heading silently blocks EVERY
  append to a project, and nothing surfaces it until a session tries to write.**
  `# Appendix BR-note - ...` (written 2026-07-13) does not match
  `^# Appendix ([A-Z]+)<dash>`, so `append-record-entry.js` refused every append
  for **54 days** - which is why the 2026-09-05 scheduled audit left no trace at
  all. The refusal is correct (an unparseable heading is invisible to the letter
  scan, so a duplicate could be written), but it is only visible at write time.
  Fixing it exposed a SECOND wedge behind it: the checker's TOC invariant then
  refused with `TOC lines (36) != appendix headings (167)`, because the record's
  Table of Contents had stopped at Appendix AI. **The shared checker still
  refuses `<LETTERS>-note` in all six repos that use it; this project no longer
  has one, but the next repo to write one wedges the same way.**
- 2026-09-05 (F3, record FN, measured): **a filter can destroy a verdict without
  changing a single return -- by starving the sample.** Adding the liquidity
  floor cut E11's gate sample from 46 closed trades to 24, under its own
  pre-registered `n>=30` minimum, so E11 stopped returning FAIL and started
  returning INCONCLUSIVE. Not better, not worse: the experiment lost the right
  to a verdict. **Rule: when adding any screen to a closed experiment, check the
  post-screen n against that experiment's own minimum BEFORE reading its
  metrics** -- otherwise a sample-size failure gets read as a performance result.
- 2026-09-05 (F3, record FN, measured): **candidate SUPPLY, not strategy
  mechanics, governs how much a universe screen moves a backtest.** Three
  pre-registered predictions reasoned from mechanics -- hold duration (E9 holds
  longest so should move most), selection style (E20 has no ranking so should
  move least), pool size (X9 should trade less) -- and all three were wrong. E9
  moved LEAST (-1.9%), E20 moved -14%, and X9 traded MORE (2,196 -> 2,502
  opens), because removing names changes WHICH pairs are the K=3 lowest-SSD and
  the replacements converge more often. A screen's impact tracks how many
  candidates a strategy had to begin with.
- 2026-09-05: **`.py` files in this repo are NOT uniformly LF.**
  `run_e8_squeeze.py`, `daily_swing_paper.py`, `backtest.py`, `universe.py` and
  `run_x9_pairs.py` are LF; `run_e11_volgated_breakout.py`,
  `run_e12_confirmed_capitulation.py`, `run_e9_deepdip.py`,
  `run_c3_vol_breakout.py`, `run_e20_dividend_capture.py` and
  `run_e1_backtest.py` are CRLF. A patch script that inserts LF newlines into a
  CRLF file creates mixed endings silently -- and a multi-line search pattern
  written with LF simply does NOT MATCH a CRLF file, which reads like the code
  having changed. Detect the file's EOL and convert patterns to it.
- 2026-09-05 (record FP, measured): **a detector whose clock comes from the
  feed it is checking cannot see that feed lag.** `daily_swing_paper.py` sets
  `today = qdates[-1]` from `series("QQQ")`. From 2026-09-02 the 19:00 run
  found no same-day bar and silently processed the previous session — three
  runs in a row, after a 17-run same-day streak (34 of 40 logged runs same-day) — so `paper_nav` has no 2026-09-04 row
  and the 09-02/09-03 rows were written a day late. The per-sleeve missed-session
  detector (fixed that very morning) excludes `today` by design and its `today`
  is the same lagged value, so it reported clean. **Rule: the expected session
  date must come from an INDEPENDENT source (broker clock, exchange calendar),
  and a feed that is behind it is a refusal, not a substitution.** Fix is PRD
  M13.1. Eighth variant of the guard-that-cannot-fire family.
- 2026-09-05 (M13.1, record FQ): **the feed-clock guard converts a silent
  wrong-date mark into a HARD STOP.** If yfinance keeps publishing the current
  bar after 20:00 ET, `daily_swing_paper.py` now REFUSES (exit 1, nothing
  marked or decided) on every 19:00 CT run instead of marking yesterday. That
  is correct, and it means the forward series stops accumulating rather than
  accumulating wrong. **No override env var exists on purpose** -- an override
  would let a human re-create the exact bug. The lever is the scheduled task's
  start time, not a flag.
- 2026-09-05 (M13.1, record FQ): **`test_frozen`'s convention guard counts a
  file as price-touching if the bare word `yfinance` appears ANYWHERE in it**,
  prose included -- `_price_scripts_missing_convention_header` greps the whole
  source but requires the convention string in the first 40 lines. A new module
  that merely *mentions* yfinance goes RED. Fix by stating the convention
  truthfully in the header, never by editing the invariant.
- 2026-09-05 (M13.1, record FQ): **`swing_bot/prices.py:92-136` `fetch()` has
  NO cache** -- a bare `yf.download` per call with a retry ladder. The
  permanent on-disk cache is `run_e8_squeeze.cache_fetch`, which the M3 loop
  never uses, and `swing.db bars` is frozen at 2026-07-08. So M3 feed staleness
  is always the vendor, never a local cache.
