# M10-2 — Gap-Amortized Stress IBS: RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_m10_2_gap_amortized_ibs.md` (committed doc-only, predates runner).
**Runner:** `scripts/run_m10_2_gap_amortized_ibs.py`. **Verdict: FAIL** — and it closes
the E2 "c2c mirage" permanently. Frozen tripwire GREEN.

## TL;DR

The design fixed the overnight-gap problem *and that is exactly how it fails.* Holding
2× QQQ mean-reversion for 5 sessions after a stress-oversold trigger makes the c2c and
next-open results nearly identical (gate 3.18% vs 2.99% — the gap is neutralized, unlike
E2's 1-day hold where it was ~half the edge). But with the gap removed, the underlying
trade is exposed for what it is: **buying 2× QQQ into the 2000–02 and 2008 cascades and
holding it 5 days — a drawdown catastrophe (gate 2.99% CAGR / 83.3% DD), not hidden
alpha.** The E2 c2c 18.15% was a 1-day-hold artifact; a properly-held, properly-costed
version reveals the reversion does not survive the crash drawdowns. **The overnight gap
was never hiding treasure — it was hiding a falling 2× knife.** Secondary is strong
(28.95% / Sharpe 1.08, the 2014+ V-shaped snapbacks + trend fallback) but both windows
are required → FAIL. PASS-RA fails too (gate Sharpe 0.28).

## Results (gate 2000–13 / secondary 2014–; 255 gate MR entries)

| arm | gate CAGR / DD / Sharpe | secondary CAGR / DD / Sharpe |
|---|---|---|
| **C — next-open, 1 bp (MAIN)** | **2.99% / 83.3% / 0.28** | 28.95% / 40.1% / 1.08 |
| B — c2c, 0 bp (E2-gap upper bound) | 3.18% / 82.9% / 0.29 | 37.53% / 29.1% / 1.30 |
| C — 5 bp stress | 1.06% / 83.7% / 0.24 | 26.91% / 41.6% / 1.02 |
| QQQ buy-hold | −0.53% / — / 0.14 | 18.39% / — / 0.90 |
| SPY buy-hold | 1.72% / — / 0.19 | 11.97% / — / 0.74 |

**Verdict:** gate CAGR 2.99% ≪ 15% AND gate DD 83.3% ≫ 60% → **PASS-HR FAIL** (secondary
passes in isolation but both windows are required). Gate Sharpe 0.28 < 0.80 → **PASS-RA
FAIL**.

## Interpretation — the program value is in the FAIL

- **The gap fix worked; that is the point.** c2c (3.18%) ≈ next-open (2.99%) in the gate:
  the 5-session hold amortized the lost first night to ~irrelevance (E2's 1-day hold made
  the gap ~half the edge). This *isolates* the reversion's true, gap-free economics — and
  they are terrible in the gate.
- **The E2 "c2c mirage" is closed.** E2's tantalizing c2c 18.15% (vs its executable
  7.98%) had left open the question: *was there real alpha behind the gap we just
  couldn't reach?* M10-2 answers no. Concentrate the trade in stress (where the per-trade
  edge is largest), remove the gap (multi-day hold), remove costs (1 bp index) — the very
  best case — and the gate still returns 2.99% on an **83% drawdown**. Buying 2× into
  2000–02/2008 oversold prints and holding 5 days catches more cascade than bounce. The
  gap was hiding the drawdown, not the alpha.
- **Leverage + index-timing is the killer, and it localizes the M10-1 contrast.** M10-1
  (Nagel Switch) passed HR with *unlevered, cross-sectional* reversal on survivors;
  M10-2 fails with *2× index* MR. Same VIX-stress conditioning, opposite outcome — the
  difference is 2× leverage into index crashes (83% DD) vs 1× dispersed survivor names.
  That sharpens the read on M10-1: its "pass" is a cross-sectional-survivor effect, not a
  general stress-reversion edge (M10-2 shows the index version is a drawdown engine).
- **Secondary looks great and means little here.** 28.95% / Sharpe 1.08 in 2014–26 is the
  2× MR riding V-shaped snapbacks (2018/2020/2022) plus the trend fallback capturing the
  QQQ bull — a one-window, bull-regime artifact, exactly the pattern every prior
  one-window "pass" showed.

## Honest caveats
- IN-SAMPLE-COMPOSED (M10 disclosure); QQQ-only (E7 market-dependence).
- The gate 83% DD is the pre-registered hazard realized — 2× long into cascading stress.
- Synthetic-2× drag QLD-calibrated (2.00%/yr, overlap CAGR 31.11% real vs 30.97% synth) —
  faithful to E5/E6; leverage is QQQ-only. No look-ahead (signal close → next-open;
  the c2c arm fills at the observed signal close, an explicit upper bound).

## Program status
M10-2 = attempt 33 (FAIL). Tally unchanged in substance: **1 IN-SAMPLE-COMPOSED PASS-HR
(M10-1, forward-paper-required) + 1 weak PASS-RA (E18) / 0 clean OOS high-return edges /
33 attempts.** The M10 synthesis arc is complete: of the two panel survivors run, the
Nagel Switch (M10-1) is the sole forward-paper candidate and M10-2 cleanly closes the E2
gap question. The only untested lever left that could validate M10-1 is **M3 forward
paper (Evan-gated)**.

## Reproduction
`.venv\Scripts\python.exe scripts/run_m10_2_gap_amortized_ibs.py`. Reuses E6 `synth`/
`calib`, `swing_bot.signals.ibs`, VIX `macro_close`. Tripwire GREEN (12 refs d=0).

## Sources
E2 leveraged-IBS results (the c2c mirage); EX-DECOMP (the overnight-gap killer); Nagel
(2012); M10 design panel (record Appendix CH).
