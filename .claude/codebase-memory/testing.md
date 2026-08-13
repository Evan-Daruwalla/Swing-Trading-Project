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
- **17 invariants** — pure-function assertions needing no fixtures: `signals.ibs`
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
