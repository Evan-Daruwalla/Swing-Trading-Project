# testing — Swing Trading

Last updated 2026-08-06. **The suite EXISTS and is the required done-check.**
(This file said "no test suite exists yet" until 2026-08-06 — stale since the
tripwire went green on 2026-07-09, found by audit #3.)

## The contract

```
.venv\Scripts\python.exe -m swing_bot.test_frozen
```
Must print **`FROZEN TESTS: GREEN (all d=0)`**. Run it after ANY change to
`swing_bot/` or to `scripts/daily_swing_paper.py`. A non-zero d is a FAIL, not
a discussion — the reference numbers are pinned precisely so drift is loud.

Two kinds of case, one file (`swing_bot/test_frozen.py`, no framework, own
`__main__` — Trading's pattern; pytest is not installed and is not required):

- **12 pinned references** — E1/E1b/E2 total-PnL and closed-trade counts on
  fixed swing.db windows, plus E4 rotation. Declared precision is ±0.0000pp.
  These run the real engine against the real `bars` table, opened READ-ONLY.
- **19 invariants** (17 until 2026-09-06; audit FX added `e18_zero_vix_refuses` and `e18_negative_vix_refuses`) — pure-function assertions needing no fixtures: `signals.ibs`
  edge cases; the three live sleeve decisions (`ps.decide_e6_1x`,
  `decide_e18_vixts`, `decide_m10_1`); since 2026-08-06, the pure helpers of
  the live orchestrator (`qty_reconcile_orders` drift band + pending suppression,
  `median_dollar_volume` thin-sample refusal, `isoweek_str`); and, since
  2026-08-11 (audit #4 F13), `price_scripts_state_adjustment_convention` — every
  `scripts/*.py` that imports `swing_bot.prices` or mentions `cache_fetch` must
  state the adjustment convention in its FIRST 40 LINES. Adding a price-touching
  script without that header FAILS the suite; that is the intended behaviour.
  (This bin said "16" from 2026-08-11 to 2026-08-13 — corrected in record EO.)
- **Standalone check, NOT part of the suite**: `scripts/prove_cache_guard.py`
  (8/8) feeds the `.e8e9_cache` freshness guard its own trigger at every site
  that can swallow it. Run it after ANY change to `_note_vintage`,
  `cache_fetch`'s retry loop, or a consumer's `except` around `cache_fetch`.

## What it does NOT cover

`scripts/` experiment runners (no frozen refs), the M3 paper tables
(`paper_sleeves` schema is orthogonal to `bars`), `alpaca_client` (network),
`costs`, `validation`, `universe_m12`, `coverage_gate`. There is no coverage
tool installed, no CI, and no git hooks — the suite is run by hand.

Discipline (independent of risk appetite): prereg before results; NEVER tune a
FAIL.

## Added 2026-09-05 (record FK)

- **Standalone check, NOT part of the suite**: `scripts/prove_liquidity_floor.py`
  (**6/6**) pins the fail-closed liquidity floor at `daily_swing_paper.py`.
  Pure in-memory - no DB, no network, no orders. Two of its six cases assert
  that the PRE-FIX branch ranked the data-starved names, so the check would
  still catch a silent revert. Run it after any change to
  `median_dollar_volume()` or to the stress-basket screen that calls it.
- **CORRECTION to "no git hooks" above:** this project HAS a native git
  pre-commit hook (`core.hooksPath` -> `scripts/git-hooks`, see security.md). It
  runs a secret scan AND the record's append-only + TOC-balance invariants, and
  it BLOCKS the commit on failure. It fired for real on 2026-09-05 -
  `APPEND-ONLY VIOLATION: a previously committed line was modified or removed` -
  and the commit went through only with a disclosed `--no-verify` on Evan's
  explicit call (record FM). The "no CI, no coverage tool, run by hand" half of
  that sentence still holds.

## Updated 2026-09-05 (F3, record FN)

- `scripts/prove_liquidity_floor.py` is now **11/11**, adding `liquidity_mask`
  cases: fail-closed over the first 9 indices of any series, PAST-ONLY masking
  (recomputing on a truncated prefix must give the identical answer), and a
  mid-series feed death returning False rather than coasting on an old median.
- **Its pass counts are DERIVED, not written.** The first version printed
  "GREEN (12/12)" while 11 cases ran, because the total was a literal. A checker
  that miscounts itself is not a checker.
- **Determinism is part of the F3 protocol:** every experiment arm is run twice
  and the two outputs must be byte-identical before any comparison is believed.
  All 16 runs (8 experiments x 2 arms) passed. (This bullet belongs to the F3
  section above; a 2026-09-06 edit inserted a heading directly on top of it and
  filed it under the torn-write section. Restored here.)

## Added 2026-09-06 (audit FX MED 4, record GA)

- `scripts/prove_torn_write.py` -> **`PROVEN: 32 checks`**. Proves
  `realize_pending`'s ledger writes are atomic PER PHASE.
- **It kills a real child process, it does not raise.** An in-process `raise`
  only shows `with conn:` unwinds cleanly; it does not model
  ExecutionTimeLimit or a reboot. Each kill arm re-execs the file as a child
  that monkeypatches one `paper_sleeves` function to `os._exit(137)` -- no
  `__exit__`, no `atexit`, no `close()` -- then the parent reopens the DB and
  lets SQLite's rollback journal decide. The child's return code is asserted
  to be exactly 137 so a child that merely errored cannot pass as a kill.
- **Arms A and F are what make it a proof.** A reproduces the PRE-FIX shape and
  requires the harness to DETECT the tear (without it, a harness that can
  detect nothing would pass). F is an `ast` walk asserting all 5 ledger calls
  carry `commit=False` inside a `with conn:` and that there are exactly TWO
  transactions -- so a later edit cannot silently un-defer a write.
- **Arm G pins a fact about the toolchain, not the code:** an inner
  `conn.commit()` ENDS a transaction opened by `with conn:`, so wrapping
  self-committing writes is a no-op. That is why FX's own prescribed fix would
  not have worked, and it is now a runnable check rather than prose.
- The assertion is a LEDGER REPLAY, not row counts: replay every
  `paper_transactions` row from the opening state and require the result to
  equal stored cash and positions to 1e-9.


## Added 2026-09-05 (M13.1, record FQ)

- `scripts/prove_feed_clock.py` -> **`PROVEN: 18 checks`**, exit 0. No DB, no
  network, no clock dependence: every case pins an explicit `now`. It calls
  `trading_calendar.check_feed_clock` -- **the same function the live loop
  calls**, not a copy of the branch, so the proof cannot drift away from the
  shipped guard (`prove_liquidity_floor.py` had to duplicate its branch).
- Coverage: the real incident replayed (feed 2026-09-03 at Fri 09-04 19:00 CT
  -> REFUSE), the Labor Day run, a before-close run, Good Friday, the
  Jul-4-observed-Friday shift, a 4-session stall, feed-ahead, and three
  observance shifts including Dec 31 2021 still TRADING. The derived 2026
  closure list is PRINTED for eyeballing rather than asserted from memory.
- **Call-site landing check** (scratchpad only, not committed): `_run()` on a
  throwaway DB with `series()` monkeypatched returned exit 1 and wrote 0
  `paper_nav` / 0 `paper_transactions` rows. Proving the function is not
  proving the call site.

## Added 2026-09-05 (M13.2, record FS)

- `scripts/probe_feed_publication.py --selftest` -> **`SELFTEST: PASS
  (4 cases)`**, no network, no DB. The verdict logic was lifted into a pure
  `verdicts(raw_last, filtered_last, expected)` for exactly one reason: the
  **"our filter dropped it"** state has never occurred live, and a branch that
  only a future bug can exercise is an untested branch. Pinning it offline is
  cheaper than waiting for the bug.
- The probe's `expected_session` comes from `swing_bot/trading_calendar.py` -
  the SAME clock `daily_swing_paper.py`'s feed guard uses. The probe and the
  live refusal are therefore independent measurements that must agree; a
  disagreement between them is a real finding, not noise.
- It refuses to mislead: run on a non-trading day it prints that it is measuring
  nothing about publication timing before sampling anyway.

## Added 2026-09-05 (M13.3, record FT)

- `scripts/prove_divergence_census.py` -> **`PROVEN: 16 checks`**. Seeds a
  throwaway DB with the live `fill_divergence` table's exact shape; `swing.db`
  is never opened and no network is touched.
- **Part B is the pattern worth reusing:** it parses `daily_swing_paper.py` with
  `ast`, walks `_run`, and asserts `print_divergence_census` is NOT nested under
  any `if args.execute:` -- while asserting `backfill_divergence` still IS. A
  "this line must appear on a dry run" requirement is otherwise checkable only
  by running the live loop, which this project forbids in a dev session.
- Part C captures the real printed line and pins the fragments an operator
  reads, so a reword that drops the denominator fails the check.
