# EX-DECOMP — Execution/signal decomposition of the closed FAILs (M9 #44)

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Type:** diagnostic (no D1 verdict, no tuning). **Runner:** `scripts/run_ex_decomp.py`.
**Regression:** GREEN — Rung C reproduces every recorded FAIL exactly. Frozen
tripwire GREEN (12 refs, d=±0.0000pp).

---

## TL;DR

Ran a three-rung execution ladder on five closed FAILs (E13, E14, E15, E16, E20)
to locate *where* each one's benchmark-relative alpha dies. Rung **A** = frictionless
close-to-close, 0 bps (raw signal); **B** = next-open, 0 bps (removes the overnight
gap); **C** = next-open + 5 bps/side (as-run). The PRD expected "most land
SIGNAL-DEAD" — **that's wrong; only E14 is signal-dead.** The others carry real gross
structure that dies for *different, now-named* reasons: **E13 is COST-GATED** (real
timing edge beats SPY frictionless *and* at next-open, killed only by turnover cost),
**E15 SURVIVES its null in the gate but decays out-of-sample**, **E16 SURVIVES its
null in the gate but that is survivorship, and it fails the null post-2014**, and
**E20 is a real-but-subscale, gap-loaded overnight edge** (its ex-date deficiency
lives in the close→open move) that goes **negative after cost post-2014**. Unifying
result: **no closed FAIL yields a robust, cost-surviving, out-of-sample high-return
edge — but the decomposition shows the program's failures are heterogeneous, not one
flat "no signal," and cost + the overnight gap are the two recurring killers.**

---

## Method

- **Rungs.** A = frictionless close-to-close (act at the signal-day close you
  observed), 0 bps; B = next-open, 0 bps; C = next-open + 5 bps/side (the committed
  run). A→B isolates the **overnight gap**; B→C isolates the **cost/turnover** drag.
- **Zero execution-logic edits.** Rung A is obtained by wrapping the price feed so
  each bar's `open := prior close`; the runner's unchanged "fill at next open" then
  transacts at the signal-day close = frictionless c2c. B/C differ only by `COST`
  (monkeypatched to 0 for A/B). Benchmarks read closes, so they are **identical across
  rungs**. Each runner got one additive `return` (behavior unchanged; `__main__`
  ignores it). **E20** (its entry is already a close, so the transform degenerates) is
  computed directly from its documented per-trade formula, reusing its `divs()` loader.
- **Null (honest benchmark) per strategy:** SPY buy-hold for E13 (a SPY timing
  overlay); EW-sectors for E14 (does momentum beat equal-weighting the 11 sectors);
  EW-survivor-universe for E15/E16 (does the event/dip *selection* beat holding all 39
  survivors); absolute mean-net-per-trade sign for E20 (an overnight overlay).
- **Classification (gate 2000–2013 primary):** SIGNAL-DEAD (A ≤ null) / GAP-DWELLER
  (beats null at A, dies A→B) / COST-GATED (beats null at B, dies B→C) / SURVIVES-NULL
  (still beats null at C — real benchmark-relative alpha; the D1 FAIL is then about the
  15% bar / DD, *not* the signal).
- **Regression gate.** Rung C must reproduce the recorded numbers: E13 gate 1.41% (rec
  1.40% ✓), E16 gate 16.76% (rec 16.76% ✓), E20 full-sample mean-net weighted from the
  gate/secondary split = +9.2 bps ≈ recorded +0.10%/trade ✓. **GREEN.**

---

## Results

**Gate 2000–2013 (CAGR; primary window):**

| strategy | null | A (c2c) | B (open) | C (+cost) | null CAGR | class |
|---|---|---:|---:|---:|---:|---|
| E13 turn-of-month | SPY-BH | 3.40% | 2.64% | 1.41% | 1.72% | **COST-GATED** |
| E14 sector-momentum | EW-sectors | 4.06% | 3.65% | 2.42% | 4.13% | **SIGNAL-DEAD** |
| E15 earnings-premium | EW-univ | 5.45% | 7.90% | 6.36% | −0.47% | **SURVIVES-NULL** |
| E16 weekly-reversal | EW-univ | 27.97% | 23.01% | 16.76% | −0.47% | **SURVIVES-NULL** |

**Secondary 2014– (CAGR; context):**

| strategy | A | B | C | null |
|---|---:|---:|---:|---:|
| E13 | 2.25% | 2.68% | 1.44% | 11.98% |
| E14 | 8.38% | 8.28% | 6.99% | 10.53% |
| E15 | 6.27% | 4.24% | 2.50% | 13.97% |
| E16 | 15.22% | 16.62% | 10.68% | 13.97% |

**E20 dividend-capture (overnight overlay; mean NET per-trade, bps):**

| window | n | A (c2c) | B (open) | C (+cost) | read |
|---|---:|---:|---:|---:|---|
| gate | 1067 | +16.9 | +34.5 | +24.5 | real, gap-loaded (B≫A), survives cost |
| 2014– | 1151 | −5.7 | +5.0 | −5.0 | dead after cost |

---

## Interpretation (per strategy)

- **E13 turn-of-month → COST-GATED.** Frictionless it *beats* SPY (3.40% vs 1.72%) and
  still beats it at next-open (2.64%); the 5 bps/side turnover cost (−1.23 pp) is what
  drags it below SPY to the recorded 1.41%. So there is a **real gross calendar edge**,
  killed by cost at this turnover — not "matched SPY by luck." Actionable only in
  principle (a lower-turnover variant); it's a ~1.4% SPY-timing overlay at 19%
  exposure, nowhere near the 15% goal, so low-value to chase.
- **E14 sector-momentum → SIGNAL-DEAD.** Even frictionless c2c (4.06%) it does **not**
  beat equal-weighting the sectors (4.13%). No alpha to execute; cost is irrelevant.
  The program's cleanest true negative (confirms the record's "lost to EW every
  window").
- **E15 earnings-premium → SURVIVES-NULL in gate, decays OOS.** In 2000–13 it beats the
  survivor basket at every rung (C 6.36% vs −0.47%) — real gate alpha, consistent with
  "beat both benchmarks in 2000–13." Note A→B *gains* (+2.45 pp): the run-up is partly
  an overnight-gap phenomenon that next-open captures. But post-2014 (C 2.50% vs null
  13.97%) it falls below the null — **real-but-decayed**, the McLean-Pontiff pattern.
- **E16 weekly-reversal → SURVIVES-NULL in gate (survivorship), fails null OOS.** The
  huge gross gate number (A 27.97%) is the **survivorship artifact** flagged at run
  time: "buy the biggest 5-day losers" on a *survivor* universe systematically buys
  dips in names we already know recovered. The decomposition can't launder that — and
  the tell is post-2014, where C 10.68% falls **below** EW-univ 13.97%: once the
  survivorship tailwind weakens, dip-selection loses to just holding the basket. Cost
  (−6.25 pp gate) and gap (−4.96 pp gate) both bite hard because of weekly turnover.
- **E20 dividend-capture → REAL-BUT-SUBSCALE, gap-loaded.** The ex-date "price drops by
  less than the dividend" edge is an **overnight** effect: B (close→open, +34.5 bps)
  ≫ A (close→close, +16.9 bps) — by the close the deficiency has largely mean-reverted
  away. It survives cost in the gate (+24.5 bps/trade) but is too small to compound
  (0.62% CAGR) and goes **negative after cost post-2014** (−5.0 bps). Pre-tax; a
  taxable-event overlay in reality.

## Cross-strategy pattern (the payload)

1. **Two recurring killers, not one.** Overnight **gap** (A→B) and **cost/turnover**
   (B→C) each independently sink edges; which one dominates depends on holding period
   and direction. Momentum/timing (E13, E16) *lose* to the gap; mean-reversion/event
   overnight trades (E15, E20) *gain* from it (their edge lives in the gap next-open
   still captures) but then pay it back in cost.
2. **Cost scales with turnover and is decisive.** The two heaviest-turnover strategies
   (E16 weekly rebalance −6.25 pp; E20 2×5 bps/overnight-trade −10 bps) take the
   largest B→C hits. This is the Chen-Velikov "~93% of anomaly alpha dies under costs"
   mechanism, observed directly in-repo.
3. **Only one strategy is truly signal-dead (E14).** The rest have real gross structure
   — but "real gross structure" converts to *zero deployable high-return edge* once you
   pass it through the gap, the cost, and out-of-sample decay. That is a **stronger and
   more honest** terminal statement than "no signal anywhere."

## Honest caveats

- **SURVIVES-NULL ≠ passes D1.** It means "beats the passive basket," not "clears the
  15% high-return bar / DD ceiling." E15 and E16 are still clean D1 FAILs.
- **The decomposition does not remove survivorship.** E16's gate SURVIVES-NULL is a
  survivorship artifact, stated as such — not evidence of a real edge.
- **Classified on CAGR** (the program's return metric); Sharpe not used for the bucket
  decision. Single deterministic path per strategy, no error bars.
- **E13/E15's "real gross edge" is sub-scale** (1–6% CAGR) — naming it COST-GATED /
  SURVIVES-NULL characterizes *why it fails*, it does not resurrect it as a candidate.

## What would change / follow from this

- A **low-turnover E13 variant** (hold the whole TOM block, minimize round-trips) is the
  only mechanically-implied follow-up; expected value low (a ~1.4% overlay). Not queued.
- The gap/cost decomposition **generalizes the M3 forward-paper rationale**: any live
  deployment must be judged at Rung C, and the gap is uncapturable at EOD — reconfirms
  E6-1× (a low-turnover overlay) as the only sane deploy candidate.

## Reproduction

- `.venv\Scripts\python.exe scripts/run_ex_decomp.py` → prints both windows + E20 +
  the regression check.
- Runner edits are additive `return {...}` hooks (E13/E14/E15/E16) tagged
  `EX-DECOMP hook (M9 #44)`; default `__main__` behavior unchanged (verified: each
  Rung C reproduces the recorded FAIL; frozen tripwire GREEN).
