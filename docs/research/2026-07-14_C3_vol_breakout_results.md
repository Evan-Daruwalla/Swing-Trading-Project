# C3 — Consolidated volatility-breakout kill-shot: RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_c3_vol_breakout.md` (doc-only, predates runner). **Runner:**
`scripts/run_c3_vol_breakout.py`. **Verdict: FAIL — the breakout/chart-pattern family
is closed.** Frozen tripwire GREEN.

## TL;DR

The consolidated Donchian/squeeze construct (20d-high entry after a sub-median-vol
squeeze, 10d-low or 40d exit, K=5, 29 ETFs, 5 bps) delivers gate 2000–13 **3.62% CAGR /
Sharpe 0.37** and secondary **1.37% / 0.19** — nowhere near either D1 tier, with 607
gate entries (well-powered). As pre-registered, this was a kill-shot and it killed: the
canonical retail chart-pattern construct has no deployable edge on liquid ETFs, exactly
as Sullivan-Timmermann-White / Bajgrowicz-Scaillet predict and consistent with E8/E11.
**The instructive detail: the time-stop-only arm BEATS the channel exit** (gate 6.19%
vs 3.62%) — the 10-session-low exit systematically sells whipsaws at their bottom. The
"exit discipline" that defines the pattern is what destroys it, validating the
template's time-stop-baseline requirement.

## Results

| arm | gate 2000–13 | secondary 2014– |
|---|---|---|
| **C main (next-open, 5bps)** | **3.62% / DD 31.7% / Sh 0.37** (n=607) | 1.37% / 26.6% / 0.19 |
| B (next-open, 0bps) | 4.51% / 30.6% / 0.44 | 2.44% / 24.4% / 0.31 |
| A (c2c, 0bps) | 4.28% / 32.3% / 0.43 | 2.10% / 26.9% / 0.27 |
| C stress 15bps | 1.85% / 33.8% / 0.22 | −0.73% / 30.8% / −0.03 |
| time-stop-only (C) | **6.19%** / 35.7% / 0.47 (n=350) | 3.23% / 22.9% / 0.31 |

Ladder: A≈B (no gap component; the edge isn't overnight-loaded) and B→C −0.89 pp
(turnover cost, ~600 round-trips). But the headline is that **both are dwarfed by the
exit-rule damage** (channel exit −2.57 pp vs time-stop in the gate).

**D1:** PASS-HR fail (3.62% ≪ 15%); PASS-RA fail (Sharpe 0.37 < 0.80). **FAIL.**

## Interpretation

Compression → breakout has no directional content on ETFs (E8's finding, now with the
full entry/exit construct); what little long-drift the entries capture is then eroded
by the channel-low exit selling every shakeout. Chart-pattern trading's core loop —
"cut losses at the recent low" — is, measured honestly, a whipsaw tax. Family closed;
with E8 + E11 + C3 the breakout family has three consistent kills.

## Reproduction
`.venv\Scripts\python.exe scripts/run_c3_vol_breakout.py`; tripwire GREEN (12 refs d=0).

## Sources
Sullivan-Timmermann-White (1999, JF); Bajgrowicz-Scaillet (2012, JFE);
Moskowitz-Ooi-Pedersen (2012, JFE); E8/E11 results (2026-07-10).
