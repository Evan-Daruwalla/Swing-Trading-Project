# C6 — Even-week FOMC-cycle overlay: RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_c6_fomc_cycle.md` (doc-only, predates runner; calendar dataset
`data/fomc_announcement_dates.json`). **Runner:** `scripts/run_c6_fomc_cycle.py`.
**Verdict: FAIL.** Frozen tripwire GREEN.

## TL;DR

The Cieslak-Morse-Vissing-Jorgensen even-week pattern **was real and is dead** — the
cleanest McLean-Pontiff decay exhibit the program has produced. In the 2000–2013 gate
the published signature is unmistakable: SPY earned **+5.62 bps/day in even FOMC-cycle
weeks vs −3.15 bps/day in odd weeks**. Post-2014 it **inverts** (+3.69 even vs +6.60
odd) — the pattern vanished around publication. The tradeable overlay (long SPY in even
weeks, 51.7% exposure, 1 bp) beats SPY in the gate (4.11%/Sharpe 0.34 vs 1.72%/0.19)
but is nowhere near PASS-RA (0.34 ≪ 0.80), trails badly in the secondary
(4.47% vs 11.98%), and its 1,585 toggles make it violently cost-sensitive
(15 bps/side → **negative** CAGR). FAIL; the FOMC-cycle overlay is closed.

## Results

**CMVJ signature (mean daily close-to-close, bps):**

| window | even weeks | odd weeks |
|---|---:|---:|
| gate 2000–2013 | **+5.62** (1878d) | **−3.15** (1643d) |
| secondary 2014– | +3.69 (1672d) | **+6.60** (1475d) |
| full 1994– | +5.89 | +2.01 |

**Overlay (1 bp/side, exposure 51.7%, 1585 toggles):**

| window | C6 CAGR/DD/Sh | SPY CAGR/Sh |
|---|---|---|
| 2000–2013 | 4.11% / 31.6% / 0.34 | 1.72% / 0.19 |
| 2014– | 4.47% / 19.3% / 0.42 | 11.98% / 0.74 |

Stress: 5 bp → gate 2.10%/0.21; 15 bp → **−2.77%/−0.11** (a ~biweekly-toggle overlay
pays the toll ~48×/year).

**D1:** PASS-HR fail; PASS-RA fail (gate Sharpe 0.34). **FAIL.**

## Interpretation

This is what a genuine-then-arbitraged anomaly looks like in this framework: strong,
correctly-signed in-sample effect (the gate replicates CMVJ's published result on
independent code and a primary-source calendar), full inversion out-of-sample after
publication (2019 JF; effect visibly gone from ~2014), and an execution profile
(hundreds of toggles) that eats what little marginal edge might remain. Together with
E13 (turn-of-month) and E15 (earnings premium), the program now holds three
independent decayed-calendar/event exhibits — consistent, and closing the
seasonality-overlay direction.

## Reproduction
`.venv\Scripts\python.exe scripts/run_c6_fomc_cycle.py`; tripwire GREEN. Calendar
provenance: `data/fomc_announcement_dates.json` (federalreserve.gov, compiled
2026-07-14).

## Sources
Cieslak, Morse, Vissing-Jorgensen — *Stock Returns over the FOMC Cycle* (2019 JF);
McLean-Pontiff (2016 JF); E13/E15 results.
