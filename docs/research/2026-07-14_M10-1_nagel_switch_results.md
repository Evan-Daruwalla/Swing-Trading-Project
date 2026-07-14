# M10-1 — Nagel Switch (VIX-gated reversal/trend): RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_m10_1_nagel_switch.md` (committed doc-only, predates runner).
**Runner:** `scripts/run_m10_1_nagel_switch.py`. **Verdict: numerical PASS-HR — the
program's FIRST — but IN-SAMPLE-COMPOSED, survivor-flattered, and razor-thin;
FORWARD PAPER REQUIRED, not a clean or deployable pass.** Frozen tripwire GREEN.

## TL;DR — read the caveats before the number

For the first time in 32 attempts a strategy clears **PASS-HR** (net CAGR ≥ 15% AND
maxDD ≤ 60% in BOTH windows): gate 2000–13 **17.87% CAGR / DD 59.95% / Sharpe 0.66**,
secondary 2014– **15.94% / DD 39.68% / Sharpe 0.78**. The mechanism is the Nagel Switch
— trade C1 residual-reversal when VIX > 20, E6 QQQ-trend when VIX ≤ 20 — which escapes
the proven fixed-weight impossibility because it routes on a *causal* variable (Nagel
2012: reversal alpha scales with VIX). **But this is not a win, and the discipline is
what says so:** (1) it is **IN-SAMPLE-COMPOSED** — designed after seeing all 31 prior
results on these exact windows; (2) it is **survivor-flattered** — the reversal leg buys
the worst-residual names among 39 *known survivors* precisely in the 2000–02/2008
crashes, and C1's own prereg already declared such passes **UNINTERPRETABLE**; (3) the
gate DD clears the 60% ceiling by **0.05 pp** (59.95%); (4) it is **threshold-fragile**
— at VIX > 18 the gate CAGR drops to 14.83% and PASS-HR **fails**; (5) it **fails
PASS-RA** (gate Sharpe 0.66 < 0.80); (6) at 15 bps it collapses to 12.40% (FAIL). Per
the pre-registered M10 cap this is recorded **"PROMISING / forward paper REQUIRED,"**
never a clean pass or a live claim. It is simultaneously the best candidate the program
has produced and a textbook case of why in-sample composition cannot be trusted.

## Results (gate 2000–13 / secondary 2014–; 333 gate stress-weeks)

| arm | gate CAGR / DD / Sharpe | secondary CAGR / DD / Sharpe |
|---|---|---|
| **C — next-open, 5bps stk / 1bp QQQ (MAIN)** | **17.87% / 59.95% / 0.66** | **15.94% / 39.68% / 0.78** |
| B — next-open, 0 bps | 20.77% / 57.7% / 0.74 | 17.73% / 39.5% / 0.85 |
| A — c2c stocks, 0 bps | 22.82% / 53.3% / 0.79 | 16.76% / 38.6% / 0.80 |
| C — 15 bps stocks (stress) | 12.40% / 64.0% / 0.52 | 12.59% / 40.1% / 0.65 |
| SPY buy-hold | 1.72% / — / 0.19 | 11.98% / — / 0.74 |
| EW-39 buy-hold | −0.47% / — / 0.13 | 13.97% / — / 0.78 |

**D1 verdict:** PASS-HR (both windows clear 15% CAGR / 60% DD). PASS-RA **fails** (gate
Sharpe 0.66 < 0.80). **VIX-threshold sensitivity (report-only):** VIX>18 → gate
**14.83% (HR FAIL)**; VIX>20 → 17.87% (PASS); VIX>22 → 15.64% (PASS).

## Why this is NOT a clean pass (the load-bearing section)

1. **IN-SAMPLE-COMPOSED.** M10 designs were composed *after* 31 results on the same two
   windows; the components (C1 gate-alive, E6 secondary-alive) were chosen because they
   were the survivors. That is severe multiple-testing. The one honest defense — the VIX
   switch is a published pre-2012 mechanism, not a fitted date — does not remove the
   snooping, only the worst form of it.
2. **Survivorship is concentrated exactly where the pass comes from.** The gate return is
   dominated by the reversal leg buying bottom-residual names in the 2000–02 and 2008
   crashes — among 39 names *known to have survived*. Delisted crashers (the reversal's
   real losses) are absent. C1's prereg declared its survivor passes uninterpretable;
   this composite inherits that ceiling verbatim. **This alone caps the result at
   forward-paper-only.**
3. **Gate DD passes by 0.05 pp** (59.95% vs the 60% ceiling). The prereg predicted this
   knife-edge ("reversal stays ON through crashes; one bad stress week busts PASS-HR").
   A pass this thin on a survivor universe is not robust.
4. **Threshold-fragile.** The one free parameter (VIX 20, the long-run mean, pre-fixed)
   is load-bearing: at 18 it FAILS HR. A real edge should not flip on a ±2 VIX move.
5. **Execution- and cost-fragile.** c2c 22.82% → next-open 17.87% (≈5 pp of the edge is
   in the overnight gap C1 always leaked), and 15 bps breaks it (12.40%). The pass lives
   only in the 5 bps / next-open corner.
6. **PASS-RA fails** (Sharpe 0.66) — the return clears but the risk-adjusted bar does
   not; the "pass" is a high-return/high-variance profile riding a ~60% drawdown.
7. **Nagel's sample (1998–2010) overlaps the gate** — the switching mechanism is partly
   in-sample to the very window it's rewarded in. The genuine OOS question is whether
   secondary reversal profit truly concentrates in the 2020/2022 VIX spikes; the 15.94%
   secondary is encouraging on this but is trend-carried, not reversal-carried.

## What it would take to believe it

**Forward paper, live, at 5 bps, for a pre-committed horizon** — the only evidence not
contaminated by in-sample composition or survivorship. Per D1 and the M10 cap, a
PASS-HR here is a forward-paper candidate exactly like E18's PASS-RA, not a deployment
authorization. A clean test would also need a **survivorship-free universe** (the
reversal leg's true crash losses) — which the project's data cannot provide. Until then
the honest label is: **the first strategy to clear the return bar, on paper, under
maximal favorable bias — promising enough to forward-test, nowhere near trustworthy
enough to fund.**

## Program status

Terminal tally updates to **1 IN-SAMPLE-COMPOSED PASS-HR (forward-paper-required,
uninterpretable) + 1 weak PASS-RA (E18) / 0 clean OOS high-return edges / 32 attempts /
8 equity families + crypto + M10 synthesis.** The structural claim is unchanged and
arguably *reinforced*: the only way to numerically clear HR was to compose two known
survivors on a survivor universe with hindsight — and even then it passes by 0.05 pp and
fails at a nearby threshold. No robust, clean, out-of-sample high-return edge has been
found; M10-1 is the closest, and it is a forward-paper hypothesis, not a result.

## Reproduction
`.venv\Scripts\python.exe scripts/run_m10_1_nagel_switch.py`. Reuses C1's
`residual_series`/`ff3_daily` verbatim + E6 trend + VIX (`macro_close`, 1990+). Tripwire
GREEN (12 refs d=0). Fixed a mark-to-market carry-forward bug (QQQ cache ends one
session before some stocks; a held QQQ was marked 0 on the boundary date — corrected to
carry the last close; no look-ahead).

## Sources
Nagel — *Evaporating Liquidity* (RFS 2012); prior C1 / E6 / E18 results; M10 design panel
(record Appendix CH).
