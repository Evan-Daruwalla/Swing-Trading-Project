# X7 — HYG:IEF Credit-Appetite Regime Gate: RESULTS

**Swing Trading project · 2026-07-15 (CST) · Evan Daruwalla**

**Prereg:** `prereg_x7_credit_gate.md` (committed doc-only `f4a4d34`, predates the runner).
**Runner:** `scripts/run_x7_credit_gate.py`. **Verdict: FAIL** (PROMISING-capped window; it
did not reach PROMISING) — but the most interesting gate result since E18: **the first gate
in the program to beat the plain 200-DMA overlay in a window.** Frozen tripwire GREEN.

## TL;DR

Long QQQ when the HYG:IEF price ratio > its 200-day SMA (credit appetite on), else cash —
the free credit-spread proxy E18's HY-OAS arm couldn't test. **In the GFC gate (2007–13) it
is excellent and genuinely beats the 200-DMA: 9.60% CAGR / 12.9% DD / Sharpe 0.98 vs the
plain 200-DMA overlay's 8.30% / 20.3% / 0.61** (and QQQ buy-hold's 53.6% DD). Credit did
lead equities into 2008 and de-risked earlier — H1's mechanism is real *in crisis*. **But in
the 2014+ secondary it collapses: 3.81% CAGR / 47.6% DD / Sharpe 0.34**, a *worse* drawdown
than buy-hold and far behind the 200-DMA (0.93). It whipsaws on credit wobbles that never
become equity drawdowns (221 regime switches vs the 200-DMA's 172). **A crisis specialist
that self-destructs in bull markets** → fails the both-windows bar. The 200-DMA remains
undefeated as a robust overlay; X7 extends the E18/X1 finding to the credit channel with a
sharp nuance.

## Results (gate 2007-04→2013-12 / secondary 2014→; credit-gate switches 221, 200-DMA 172)

| arm | gate CAGR / DD / Sharpe | secondary CAGR / DD / Sharpe |
|---|---|---|
| **CREDIT next-open 1 bp (MAIN)** | **9.60% / 12.9% / 0.98** | 3.81% / 47.6% / 0.34 |
| credit next-open 0 bp (B) | 9.67% / 12.7% / 0.99 | 3.95% / 47.4% / 0.35 |
| credit c2c 0 bp (A, upper) | 8.93% / 15.1% / 0.92 | 3.39% / 44.0% / 0.31 |
| credit stress 15 bp | 8.57% / 15.5% / 0.88 | 1.78% / 50.2% / 0.20 |
| **PLAIN 200-DMA overlay** (incumbent) | 8.30% / 20.3% / 0.61 | 14.81% / 24.1% / 0.93 |
| QQQ buy-hold | 10.77% / 53.6% / 0.55 | 18.45% / 35.6% / 0.90 |
| SPY buy-hold | 3.77% / — / 0.27 | 11.98% / — / 0.74 |

Descriptive sensitivity (NOT gated, not a verdict input): a 50-day ratio-MA is *even better*
in the gate (12.41% / 14.8% / **1.01**) and *still* fails the secondary (5.58% / 42.0% /
0.46) — confirming the crisis-specialist pattern is not an artifact of the 200-day window.

**Verdict logic (prereg):** X7 = PROMISING iff it clears the E6/E18 overlay criteria (DD cut
≥ 10 pp vs QQQ-BH AND Sharpe ≥ QQQ-BH) in **both** windows AND beats the plain 200-DMA on
gate Sharpe. **Gate: passes (DD 12.9% ≪ 53.6%, Sharpe 0.98 > 0.55, and 0.98 > 200-DMA's
0.61 → beats the incumbent).** **Secondary: FAILS** (DD 47.6% > QQQ-BH 35.6%; Sharpe 0.34 ≪
0.90). Both windows required → **FAIL.** PASS-HR unreachable (overlay); PASS-RA-equiv fails
on the secondary. Modified window caps the ceiling at PROMISING regardless.

## Interpretation — a clean FAIL with the program's sharpest gate payload

- **The FIRST gate to beat the 200-DMA in a window.** E18 tested VIX-TS / HY-OAS / breadth
  and none beat the plain 200-DMA; X1 confirmed. X7's credit gate finally does — **in the
  GFC gate, Sharpe 0.98 vs 0.61.** The credit-leads-equities hypothesis (H1) is REAL: HYG:IEF
  collapsed ahead of / alongside the 2008 equity break, so the gate cut the drawdown to
  12.9% (vs the 200-DMA's 20.3%). This is a genuine, mechanistic in-crisis edge.
- **…and a crisis specialist that whipsaws to pieces in bulls.** In 2014–26 the credit ratio
  dips on every spread wobble (energy 2015-16, Q4-2018, COVID, 2022) — many of which the
  200-DMA rode through — so the gate sells low and buys back higher, netting 3.81% CAGR with
  a **47.6% drawdown, worse than simply holding QQQ.** 221 switches vs 172 = it is the
  noisier signal, and the noise is fatal in a trending bull.
- **Same one-window death as every prior near-miss, inverted.** C7 (26% gate CAGR), X6 (30%
  crypto gate), M10-2 (28% secondary) each passed one window and died in the other; X7 passes
  the *crisis* window and dies in the *bull*. The pre-registered both-windows bar killed it —
  exactly as designed. A weaker process would have shipped the 0.98 gate Sharpe.
- **It corroborates the BlackRock report against itself.** BlackRock's own Figures 2/3 show
  defensive credit tilts mitigate crisis downside then miss the snapback; X7 is that precise
  dynamic measured on QQQ — downside-mitigation-without-upside-capture, a THIRD-domain
  confirmation (equities E6/C4, crypto X6, credit X7) of the program's structural conclusion.

## Honest caveats

- **Modified window** (HYG starts 2007) → misses 2000-02; verdict PROMISING-capped anyway,
  and the 200-DMA warmup keeps the credit gate in cash ~2007-04→2008-01 (handicaps its early
  gate return — yet it still beats the 200-DMA, so the result is conservative).
- **Price-only ratio** (dividend-UNADJUSTED bond ETFs) — correct for a regime signal, never
  traded as a return series; disclosed.
- **Not survivor-biased** (market-wide ETF signal) → this FAIL is clean and interpretable in
  both directions; a pass would have been meaningful (but forward-paper-routed by the window).
- **Overlay, not a return engine** — cannot clear PASS-HR by construction.

## Program status

X7 = attempt 35 (FAIL), within the regime-gate/overlay family (E18 lineage). Tally: **1
IN-SAMPLE-COMPOSED PASS-HR (M10-1, forward-only) + 1 weak PASS-RA (E18) / 0 clean high-return
edges / 35 attempts.** The terminal claim stands and gains a credit-channel data point: the
plain 200-DMA remains the only robust overlay; a credit gate beats it *in a crisis* but not
across regimes. The completeness sweep now spans the credit domain.

## Reproduction

`.venv\Scripts\python.exe scripts/run_x7_credit_gate.py`. Reuses `cache_fetch` (HYG/IEF/QQQ/
SPY) + E18 `sma`/`stats`. Tripwire GREEN (12 refs d=0).

## Sources

BlackRock "A systematic approach to high yield credit" (2025, record Appendix CU); E18
regime-gate bake-off + X1 (the 200-DMA incumbent); prereg `prereg_x7_credit_gate.md`.
