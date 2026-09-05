# Pre-registration — F3: enforce the liquidity floor in the ETF experiments

**Written 2026-09-05, ~18:00 CDT. Committed DOC-ONLY before any runner code
changes.** Supersedes the F3 scope Evan authorised on 2026-08-19
("prereg + re-run affected backtests" over the 39-name stock set), which record
FG showed to be provably immune. Evan authorised this redirect 2026-09-05.

## 0. Why this exists, stated as a gap rather than as a hypothesis

`CLAUDE.md:51` says the liquidity floor is **"mandatory in any universe
filter"**. As of 2026-09-05 that is true of exactly one place: the live M10-1
stress screen in `scripts/daily_swing_paper.py`, fixed to fail closed earlier
today (record FK). **No research runner enforces it at all.** The 29-ETF
universe in `swing_bot/universe.py` carries the constant
`MIN_MEDIAN_DOLLAR_VOL = 20_000_000` with the comment *"guard only; every
current member clears it by a wide margin"* — a present-tense snapshot that
record FG proved false as a statement about the history.

**This is a ROBUSTNESS RE-CHECK of closed FAILs, not a new experiment.** Every
affected experiment already has a recorded verdict, and every one of those
verdicts is FAIL. That asymmetry is the whole design of this prereg, and §4 is
where it is handled.

## 1. Scope — measured, not assumed

From record FG (2026-08-19), re-derived independently in FH.3:

| universe | ticker-sessions below the floor | names ever below |
|---|---|---|
| 39-name stock survivor set | **0 of 260,363 = 0.00%** | 0 of 39 |
| **29-ETF frozen universe** | **28,776 of 179,055 = 16.07%** | **26 of 29** |

Top breachers by session count: EWU 2,886, EWG 2,231, EWC 1,898, EWA 1,809,
EWH 1,677, EWW 1,468, XLY 1,453, XLP 1,416.

**IN SCOPE** — experiments that do cross-sectional selection over the 29-ETF
universe, so the floor can change which names they hold:

| experiment | selection | recorded verdict |
|---|---|---|
| E1 | IBS ranking, `swing_bot/backtest.py:129` | FAIL |
| E8 | squeeze breakout, K=3 | FAIL |
| E9 | deep-dip, K=5 | FAIL |
| E11 | volume-gated breakout, K=3 | FAIL |
| E12 | confirmed capitulation, K=3 | FAIL |
| C3 | vol breakout, K=5 | FAIL |
| X9 | pairs, K=3 lowest-SSD | FAIL |
| E20 | dividend capture, equal-weight same-day ex-dates | FAIL |

**OUT OF SCOPE, with the reason measured rather than assumed:**

- **E1b** — trades `broad_us` (SPY/QQQ/DIA/IWM) only; **zero breaches** (FG).
- **E2** — its only breaching name is SOXL, and every SOXL breach falls before
  2017: inside E2's train window and outside its 2022+ gate, so **E2's verdict
  cannot move** (FG).
- **E14** — selects top-3 of the 11 SPDR sectors, not the 29-ETF universe. Two
  of the 11 (XLY, XLP) are on the breacher list, so E14 is **IN SCOPE for a
  count but its own sub-universe must be measured separately**; treated as a
  reported number, not a verdict test.
- **M12** — 142 names, 2.69% of ticker-sessions; the floor removes ~5.2% of
  gate-window picks at K=3 (FG). **M12 issues no PASS/FAIL**, so what moves is
  a magnitude, not a verdict. Reported, not gated.
- **The 39-name stock set** — 0 breaches. Re-running it is pure compute for a
  guaranteed null, and wiring the floor in would install a guard that cannot
  fire for the fifth time (FG.2). **Explicitly not done.**

## 2. What will be changed in the code

1. **Move `median_dollar_volume` from `scripts/daily_swing_paper.py` into
   `swing_bot/universe.py`**, beside the constant it enforces, so threshold and
   enforcement are one unit. Required, not cosmetic: FG.4 showed
   `daily_swing_paper.py` imports `run_e10_earnings_drift` and
   `run_c1_residual_reversal` at module level ABOVE the function's definition,
   so a runner importing the function back would hit a partially-initialised
   module. `daily_swing_paper` re-imports it from its new home, so its call site
   and `test_frozen`'s `median_dollar_volume_refuses_thin_sample` invariant are
   unchanged in behaviour.
2. Add `swing_bot.universe.is_liquid(dates, close, vol, asof)` — the single
   eligibility predicate, **failing closed on unmeasurable volume** exactly as
   the live loop now does (record FK).
3. The in-scope runners stop discarding volume at load (it is index 7 of the
   cached bar, present in every path, 0 nulls across 105,396 `bars` rows) and
   screen candidates through `is_liquid` before ranking.
4. `swing_bot/universe.py:48`'s "every current member clears it by a wide
   margin" is corrected — it is a snapshot, and 26 of 29 members have breached.

**Threshold is NOT touched.** `MIN_MEDIAN_DOLLAR_VOL = 20_000_000` and the
20-session window were set at M0.4 and are used as-is. Changing either while
looking at results is the tuning this project forbids.

## 3. Pre-registered predictions

Written before any run. Each is falsifiable and is recorded whether it holds or
not.

- **P1 — picks move.** At least one of E1, E8, E9, E11, E12, C3 changes at
  least one held name on at least one date. *(If NO experiment changes a single
  pick, F3 has no teeth anywhere and the finding is closed as null — which
  would make the ETF redirect wrong in the same way the stock scope was.)*
- **P2 — no verdict flips FAIL to PASS.** All eight recorded verdicts stay FAIL.
- **P3 — E9 is the most affected of the K-selection set**, because it holds
  K=5 with no stop and no max hold, so an illiquid name it buys stays in the
  book longest.
- **P4 — E20 moves least of the eight**, because its selection is driven by
  ex-dates rather than by a cross-sectional ranking, so the floor removes names
  rather than reordering a queue.
- **P5 — X9's pair count drops.** Removing 26 of 29 names on some dates shrinks
  the formation-period candidate set, so the number of tradeable pairs falls in
  at least one formation window.

## 4. Pre-committed failure conditions — the asymmetry, handled

Every affected verdict is already FAIL. A filter added after a FAIL can only be
neutral or flattering, and a flattering result here would be indistinguishable
from tuning. So:

- **If any experiment flips FAIL to PASS, that is NOT a verdict change and is
  NOT banked.** It is recorded as a FLAG FOR RE-EXAMINATION: the experiment is
  reported as FAIL-with-a-liquidity-caveat, and any claim of a PASS requires its
  own fresh pre-registration written before looking further. Rationale: the
  floor was chosen at M0.4 for live-trading reasons, not selected to improve
  these backtests, but that intent is not verifiable from the result, and a
  PASS obtained this way would fail the "never tune a FAIL" rule in substance
  even if it passes it in form.
- **If the floor removes so many names that an experiment can no longer form a
  full K-basket on a material share of dates, that is reported as a coverage
  result, not silently backfilled** with the next-best illiquid name.
- **If `is_liquid` never returns False in a given experiment's run**, that
  experiment is reported as UNAFFECTED and its result is NOT re-stated as a new
  measurement — a guard that cannot fire gets named, not shipped (FG.2).
- **If the re-run does not reproduce the recorded FAIL numbers with the floor
  DISABLED**, everything stops: that means something else changed since the
  original run, and no floor conclusion can be drawn until it is explained.

## 5. Reporting

Each in-scope experiment reports, in one table: recorded verdict, floor-off
re-run (must reproduce), floor-on result, names removed, dates affected, and
whether the verdict moved. Results land in
`docs/research/2026-09-05_F3_liquidity_floor_etf_results.md` and a record entry.

## 6. Disclosed weakness of this pre-registration

This prereg is committed doc-only in its own commit, so git proves it predates
the runner changes. **But it is written and run in the same session**, which is
weaker than the V3 precedent, where Evan deliberately left the run for a later
sitting. That gap is disclosed here rather than glossed: the protection this
prereg actually provides is §4's pre-committed handling of a flattering result,
not temporal separation from the author.
