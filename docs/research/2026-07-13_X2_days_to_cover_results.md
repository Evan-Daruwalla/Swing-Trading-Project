# X2 — Days-to-cover / short-interest drift (FINRA, modern OOS): RESULTS

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Prereg:** `prereg_x2_days_to_cover.md` (committed `4094889`, doc-only, predates
the runner). **Runner:** `scripts/run_x2_days_to_cover.py`. **Verdict:** **FAIL
(deployable long-only leg)** — but the short-interest anomaly is **real, correctly
signed, and strong on the non-deployable short leg.** Frozen tripwire GREEN.

---

## TL;DR

The deployable long-only lowest-days-to-cover leg (K=5, biweekly, next-open,
5 bps, 39 survivor large-caps, 2018–2026) returns net **13.32% CAGR / Sharpe 0.60**
— it beats SPY on raw CAGR (12.53%) and EW-39 (9.59%) but has **worse risk-adjusted
return than SPY** (0.60 < 0.71) and a 35% drawdown in a bull window. Against the
pre-registered "beat both benchmarks on CAGR **and** Sharpe" bar it is a clean
**FAIL**. **But the anomaly itself is alive and exactly as documented:** the
long-short spread is **+18.39% CAGR, Sharpe 0.98**, and it decomposes precisely as
theory predicts — low-DTC +15.77% vs **high-DTC −2.63%** (the most-shorted mega-caps
*underperformed SPY by ~15 pp/yr*). The alpha is **entirely on the short/high-DTC
leg**, which is **not deployable** at $100–1,000 (no fractional shorting; borrow).
This is *exactly* what the prereg predicted a priori ("the long-only leg tests the
weak side; the alpha is on the short leg, not deployable here") — a clean
falsification of the *tradeable* idea and a validation of the a-priori reasoning.

---

## Method

Per prereg: FINRA consolidated short interest (public REST API, no auth; 205 biweekly
settlement dates 2017-12-29→2026-06-30, 39/39 coverage; `daysToCoverQuantity`
precomputed). Each settlement date, rank the 39 by days-to-cover. **Deployable leg:**
long the K=5 lowest-DTC, equal-weight, rebalance each cycle. **Existence spread
(non-deployable):** low-K minus high-K. **Lookahead guard:** enter **10 trading
sessions after the settlement date** (past the ~8–9-business-day dissemination lag).
**Single 2018–2026 window → MODIFIED-WINDOW CAP: best achievable = PROMISING, never
PASS-HR/RA.** Decomposition ladder (A c2c 0bps / B next-open 0bps / C next-open 5bps)
+ a 15 bps stress leg, per the new template. Survivor universe → asymmetric framing
(only a FAIL is clean).

---

## Results (window 2018-01-16 → 2026-07-10; 2132 sessions, 204 cycles)

| leg | CAGR | maxDD | Sharpe |
|---|---:|---:|---:|
| long-only **A** (c2c, 0 bps) | 15.93% | 37.7% | 0.69 |
| long-only **B** (next-open, 0 bps) | 16.07% | 34.7% | 0.69 |
| long-only **C** (next-open, **5 bps** — as-run) | **13.32%** | 34.9% | **0.60** |
| long-only (15 bps stress) | 8.01% | 35.3% | 0.42 |
| SPY buy-hold | 12.53% | 34.1% | **0.71** |
| EW-39 buy-hold | 9.59% | 34.2% | 0.58 |
| spread: low-DTC basket (long) | 15.77% | 37.7% | 0.69 |
| spread: **high-DTC basket (short leg)** | **−2.63%** | 36.4% | −0.03 |
| **long-short SPREAD** | **18.39%** | 26.0% | **0.98** |

**Verdict:** long-only C beats SPY & EW on CAGR but **loses Sharpe to SPY (0.60 <
0.71)** → fails the pre-registered "CAGR **and** Sharpe vs both" bar → **FAIL**
(the pre-committed criterion is honored, not relaxed). Existence spread sign is
positive (+18.39%), as predicted. 204 cycles ≫ 20 floor.

---

## Interpretation

- **The tradeable idea fails, cleanly.** A long book of the least-shorted mega-caps
  is a higher-beta SPY tilt: +0.79 pp CAGR over SPY, but *worse* Sharpe and 35%
  drawdown, in a mostly-bull decade. After the honest 5 bps it clears no risk-adjusted
  bar; at 15 bps it collapses to 8%. Decomposition: **A→B is flat** (16.07 vs 15.93 —
  *not* a gap-dwelling edge, unlike the reversal family), so the erosion is **pure
  cost** (B→C −2.75 pp from biweekly turnover). But even gross (16%, Sharpe 0.69) the
  long side barely matches SPY — the long leg simply is not where the edge is.
- **The anomaly is real and correctly signed — on the short side.** The spread's
  Sharpe 0.98 / +18.4% is driven almost entirely by the **high-DTC leg underperforming
  by ~15 pp/yr** (−2.63% vs SPY +12.53%). This is the Boehmer-Huszar-Jordan /
  Asquith-Pathak-Ritter effect **alive in the modern liquid large-cap tape** — the
  first time this program has found a strong, documented, correctly-signed anomaly.
- **Survivorship makes the short-leg result a LOWER bound.** Our universe excludes
  names that were heavily shorted and then *delisted/crashed* — exactly the short
  seller's biggest wins. So the true short-side alpha is if anything larger than −2.63%
  measured. That cuts the usual direction: here survivorship works *against* the
  finding, strengthening "the anomaly is real." (It does flatter the long leg, the
  standard way — but the long leg failed anyway.)
- **It is not harvestable here.** The alpha lives in shorting high-DTC names:
  impossible with no fractional shorting at $100–1,000, and long-only cannot convert a
  short leg's −15 pp underperformance into profit. Avoiding high-DTC names (≈ the
  long-only low-DTC leg) does *not* recover it — that leg is the one that failed. So
  the correct routing is: **existence-confirmed, non-deployable.**

## Honest caveats

- **PROMISING-capped and FAILED anyway** — single 2018–2026 window (one covid crash,
  one 2022 bear); the deployable leg didn't even reach the capped bar, so window
  thinness isn't load-bearing for the FAIL.
- **The spread is an existence signal, not a validated tradeable edge:** 39 survivor
  names, one window, dollar-neutral, non-deployable; the −2.63% short leg may be
  concentrated in a few troubled mega-caps (GE-era, energy-2020, etc.). Not a live
  claim; not counted toward PASS-HR (which stays 0).
- **Long-only leg tests the weak side of the anomaly** (disclosed a priori) — this FAIL
  falsifies the *long-only tradability*, not the short-side effect.

## What would change the conclusion

- A route to the short leg within the constraints (whole-share shorting on a larger
  account; a short-biased inverse instrument) — an **Evan-gated capital/scope
  decision**, not an autonomous one.
- A longer/independent window confirming the high-DTC underperformance out-of-sample
  (the effect is post-publication and could decay).

## Reproduction

- Ingest: `.venv\Scripts\python.exe scripts/ingest_finra_short_interest.py`
  (public FINRA API; `.finra_cache/`, gitignored).
- Run: `.venv\Scripts\python.exe scripts/run_x2_days_to_cover.py`.
- Tripwire: `.venv\Scripts\python.exe -m swing_bot.test_frozen` → GREEN (12 refs d=0).

## Sources (dated)

- Boehmer, Huszar, Jordan — *The Good News in Short Interest* (JFE 2010).
- Asquith, Pathak, Ritter — *Short Interest, Institutional Ownership, and Stock
  Returns* (JFE 2005).
- FINRA consolidated short interest REST API (`api.finra.org`), accessed 2026-07-13
  (record Appendix BU); data-sources brief `docs/research/2026-07-13_data_sources.md`.
