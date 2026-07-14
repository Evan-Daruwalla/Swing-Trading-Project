# C1 — Short-term residual reversal (FF3-stripped): RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_c1_residual_reversal.md` (doc-only, predates runner). **Runner:**
`scripts/run_c1_residual_reversal.py`. **Verdict: FAIL** — but the program's closest
approach to PASS-HR, and the most instructive near-miss in the ledger. Frozen
tripwire GREEN.

## TL;DR

Swapping E16's raw 5-day ranking for a **FF3-residual trailing-month ranking** (same
engine, same universe, same costs) did exactly what Blitz-Huij-Lansdorp-Verbeek
promise: gate 2000–13 net **19.08% CAGR / maxDD 57.7% / Sharpe 0.69** — *more* return
than E16 (16.76%) with the drawdown pulled **under the 60% ceiling** (65.9% → 57.7%).
**For the first time in 28 attempts, both PASS-HR legs clear in the gate window.** It
is still a clean FAIL: PASS-HR requires both windows and the secondary collapses to
**2.92% CAGR / Sharpe 0.24** (vs SPY 11.98%/0.74) — the effect is dead post-2014. And
the asymmetric framing caps the meaning of the gate number regardless: on a survivor
universe, buying the biggest idiosyncratic losers among 39 names *known to have
survived* is upper-bound-biased by construction. Cost-fragility is severe (weekly
churn, 2,924 gate entries; 15 bps → 7.28% gate, **negative** secondary). Residual
reversal closed.

## Results

| arm | gate 2000–13 | secondary 2014– |
|---|---|---|
| **C main (next-open, 5bps)** | **19.08% / DD 57.7% / Sh 0.69** | 2.92% / 38.7% / 0.24 |
| B (next-open, 0bps) | 25.46% / 55.0% / 0.84 | 8.40% / 37.9% / 0.46 |
| A (c2c, 0bps) | 28.24% / 46.5% / 0.90 | 7.50% / 34.8% / 0.43 |
| C stress 15bps | 7.28% / 63.1% / 0.38 | −7.24% / 68.0% / −0.21 |
| E16 raw (recorded) | 16.76% / 65.9% / 0.61 | 10.68% / — / — |
| SPY-BH | 1.72% / — / 0.19 | 11.98% / — / 0.74 |
| EW-39-BH | −0.47% / — / 0.13 | 13.97% / — / 0.78 |

Ladder: A→B −2.78 pp (gap bleed, the Nagel close-anchoring cost, milder than E16's);
B→C −6.38 pp (weekly turnover × 5 bps); 15 bps kills it outright.

**D1:** PASS-HR — gate legs PASS (19.08% ≥ 15%, 57.7% ≤ 60%) but secondary fails
(2.92% < 15%) → **fail**. PASS-RA — gate Sharpe 0.69 < 0.80, secondary Sharpe < SPY →
**fail**. **FAIL** (floor: 2,924 gate entries).

## Interpretation

- **The BHLV mechanism is real:** factor-stripping the formation return raised return
  *and* cut drawdown vs E16's raw ranking, exactly as published — the rare case in
  this program where a literature refinement did what it says on the survivor tape.
- **But it is a regime artifact + survivorship stack:** all of the performance lives
  in 2000–2013 (crash-rebound decades where dip-buying survivors is maximally
  flattered) and vanishes in the modern regime (2.92% vs an EW basket at 13.97%). A
  strategy whose edge requires 2000-2013-style volatility *and* foreknowledge of
  survival is not deployable.
- **Program-level meaning:** the closest-ever HR approach came from the reversal
  family — consistent with EX-DECOMP (E16 was SURVIVES-NULL-gate, the strongest gross
  structure among the FAILs). The bar held: no tuning, no window-shopping, FAIL
  recorded. This is the discipline working as designed on the most tempting result
  the program has produced.

## Reproduction
`.venv\Scripts\python.exe scripts/run_c1_residual_reversal.py` (fetches + caches FF3
daily from Ken French's library on first run); tripwire GREEN (12 refs d=0).

## Sources
Blitz-Huij-Lansdorp-Verbeek (2013, J. Empirical Finance); Nagel (2012, RFS);
Ken French data library (accessed 2026-07-14); E16 results (2026-07-11);
EX-DECOMP (2026-07-13).
