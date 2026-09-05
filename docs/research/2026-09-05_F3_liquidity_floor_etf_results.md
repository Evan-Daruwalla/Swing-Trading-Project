# F3 results — enforcing the liquidity floor in the ETF experiments

**Run 2026-09-05, ~18:00–18:18 CDT.** Pre-registration:
`docs/prereg_f3_liquidity_floor_etf_scope.md` (committed doc-only `6a23a9a`)
plus `docs/prereg_f3_amendment_cache_vintage.md` (doc-only `2f0a8a4`). Both
predate every line of runner code changed for this run — that ordering is
visible in `git log`, which is the only reason the predictions below are worth
anything.

**DATA CONVENTION:** split-adjusted, dividend-UNADJUSTED (`auto_adjust=False`)
throughout.

**VINTAGE:** the `.e8e9_cache` runs (E8, E9, E11, E12, C3, E20, X9) are pinned
at **2026-08-17** via `SWING_ALLOW_STALE_CACHE=1`; all 181 price-series files
share that single end date, so both arms read a byte-identical snapshot. **E1 is
different**: it reads `swing.db bars`, which spans **2014-01-02 → 2026-07-08**.
E1's arms are comparable to each other and NOT to the others.

## Headline

**No verdict flipped FAIL → PASS. One moved FAIL → INCONCLUSIVE.** Every
affected experiment changed its picks, so the floor is not a guard that cannot
fire — which is what the stock-universe scope would have been (record FG).

| experiment | verdict OFF → ON | trade count OFF → ON | the number that moved most |
|---|---|---|---|
| E1 IBS | FAIL → FAIL | 3,559 → 3,534 (−0.7%) | Sharpe 0.23 → 0.21 |
| E8 squeeze | FAIL → FAIL | 341 → 276 (−19%) | gate CAGR −1.43% → −2.21% |
| E9 deep-dip | FAIL → FAIL | 53 → 52 (−1.9%) | gate CAGR 3.46% → 3.00% |
| **E11 vol-gated** | **FAIL → INCONCLUSIVE** | 61 → 39 (−36%) | **gate n 46 → 24, under the pre-registered n≥30** |
| E12 capitulation | FAIL → FAIL | 130 → 106 (−18%) | gate maxDD 55.0% → 45.5% |
| C3 vol breakout | FAIL → FAIL | 607 → 488 (−20%) | **gate maxDD 31.7% → 17.1%** |
| E20 dividend capture | FAIL → FAIL | 2,345 → 2,011 (−14%) | gate CAGR 0.62% → 0.49% |
| X9 pairs | FAIL → FAIL | 2,196 → **2,502 (+14%)** | gate CAGR −2.50% → −4.68% |

Every arm was run twice and every pair was byte-identical, so no comparison here
rests on a non-deterministic runner.

## The two results that are actually interesting

**1. The floor can destroy a verdict by starving the sample.** E11's gate
sample fell from 46 closed trades to 24, below its own pre-registered n≥30
minimum, so E11 no longer returns FAIL — it returns INCONCLUSIVE. That is not a
better outcome and it is not a worse one; it is the experiment losing the right
to a verdict. E11 is E8's rules plus one added entry condition (RVOL≥1.5), so it
was already the thinnest sample in the set; the floor removed the illiquid names
that were supplying a third of what was left. **This was not among the five
pre-registered predictions.** The parent prereg's §4 anticipated the shape of it
("if the floor removes so many names that an experiment can no longer form a
full K-basket on a material share of dates, that is reported as a coverage
result") but predicted it as a basket-formation problem, not a sample-size one.

**2. The illiquid names were carrying half of C3's drawdown.** C3's gate maxDD
fell from 31.7% to 17.1% — a 46% reduction — while its gate CAGR fell only 3.62%
→ 3.20% and its Sharpe barely moved (0.37 → 0.36). The floor removed risk almost
without removing return. C3 still FAILs both its bars, so nothing is banked, but
this is the clearest evidence in the set that the floor is doing real work rather
than trimming noise. E12 shows the same direction (maxDD 55.0% → 45.5%).

## Pre-registered predictions — 2 held, 3 falsified

Recorded as they were written, not as they turned out.

| prediction | outcome |
|---|---|
| **P1** — at least one of E1/E8/E9/E11/E12/C3 changes at least one pick | **CONFIRMED.** All six changed. F3 has teeth on the ETF universe, unlike the stock scope. |
| **P2** — no verdict flips FAIL → PASS | **HELD.** None did. §4's central protection was never needed. |
| **P3** — E9 is the most affected of the K-selection set, because K=5 with no stop and no max hold holds an illiquid name longest | **FALSIFIED.** E9 moved LEAST of that set (−1.9%). E11 moved most (−36%). The reasoning was about hold duration; what actually governs is how many candidates a strategy has to begin with. |
| **P4** — E20 moves least of the eight, because ex-dates drive its selection rather than a cross-sectional ranking | **FALSIFIED.** E20 moved −14%, against E1's −0.7% and E9's −1.9%. Having no ranking does not protect a strategy — it means every screened-out name is a capture simply not taken. |
| **P5** — X9's tradeable-pair count drops | **FALSIFIED, and in the opposite direction.** X9 opened MORE trades with the floor on: 2,196 → 2,502. Removing illiquid names from the formation pool changes *which* pairs are the K=3 lowest-SSD, and the replacements open and converge more often. The candidate pool shrinks; the resulting activity rises. |

Three of five wrong is the return on writing them down. P3, P4 and P5 were all
reasoned from strategy mechanics; in every case the answer turned on candidate
supply instead.

## What changed in the code

- `swing_bot/universe.py` — `median_dollar_volume` **moved here** from
  `scripts/daily_swing_paper.py` (required: that module imports two runner
  scripts above the function's old definition, so a runner importing it back hit
  a partially-initialised module, record FG.4). Added `is_liquid` and
  `liquidity_mask`. The `MIN_MEDIAN_DOLLAR_VOL` comment claiming "every current
  member clears it by a wide margin" is corrected in place.
- `scripts/run_e8_squeeze.py` — `simulate(data, liq=None)` screens candidates
  **before** the ranking sort; `f3_masks` / `f3_masks_for` / `f3_masks_by_date`
  and the `SWING_F3_FLOOR` switch live here and are shared.
- `run_e11_volgated_breakout.py`, `run_e12_confirmed_capitulation.py`,
  `run_e9_deepdip.py`, `run_c3_vol_breakout.py`, `run_e20_dividend_capture.py`,
  `run_x9_pairs.py` — same screen at each runner's own chokepoint.
- `swing_bot/backtest.py` — `run_backtest(..., liq=None)`. **Default None is the
  pre-F3 path byte-for-byte**, which is why `swing_bot/test_frozen.py`'s 12
  pinned references stayed at d=±0.0000pp: the tripwire calls the function
  without the argument. That is by design, not by luck, and it is stated in the
  docstring so the next person does not "tidy up" the default.
- `scripts/prove_liquidity_floor.py` — now **11/11**, covering fail-closed on
  short history, past-only masking (a prefix recompute must match), and a
  mid-series feed death.

**Threshold untouched:** `MIN_MEDIAN_DOLLAR_VOL = 20_000_000` and the 20-session
window are exactly as set at M0.4.

## Two counts that look like contradictions and are not

- **"27 of 29 names" here vs FG's "26 of 29".** FG swept from 2000-01-01
  (179,055 ticker-sessions); `liquidity_mask` covers each series in full, so EWJ
  (listed 1996) enters this count and not FG's. Sub-floor bars: 38,573 here,
  28,776 in FG, same reason.
- **"29 of 29 blocked" — a number that was almost published and is wrong.** The
  first version of the run banner counted the unmeasurable warm-up prefix (the
  first 9 bars of every series, 261 bars total, where the mask fails closed
  because there is nothing yet to measure) together with real sub-floor bars.
  That reads as every name being blocked. The banner now reports the two
  separately. The substantive figure is 27 names / 38,573 bars.

## Not covered

- **E14** (top-3 of the 11 SPDR sectors) — the prereg scoped it as a reported
  count, not a verdict test, because its sub-universe is not the 29-ETF set. Two
  of its 11 names (XLY, XLP) are breachers. **Not run.** It is the one in-scope
  item this pass did not measure.
- **M12** — no PASS/FAIL to move; FG's figure (floor removes ~5.2% of
  gate-window picks at K=3) stands unre-measured.
- **E1b and E2** — measured OUT of scope by FG and unchanged: E1b trades
  broad-US only with zero breaches; E2's only breacher is SOXL, entirely
  pre-2017, inside its train window and outside its 2022+ gate.
- **The 39-name stock set** — 0 of 260,363 ticker-sessions breach. Not run, and
  deliberately so: wiring the floor there installs a guard that cannot fire.

## Gates

`swing_bot.test_frozen` → **`FROZEN TESTS: GREEN (all d=0)`**, run after every
change to `swing_bot/`, including `backtest.py` itself.
`scripts/prove_liquidity_floor.py` → **GREEN (11/11)**.
No writes to `swing.db` (E1 opens it through `prices.connect_ro`);
`scripts/daily_swing_paper.py` and every `.bat` never executed.
