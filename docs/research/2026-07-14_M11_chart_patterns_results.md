# M11 — Algorithmic Chart-Pattern Detection: RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_m11_chart_patterns.md` (committed doc-only `9cb5ac5`, predates the
runner). **Runner:** `scripts/run_m11_chart_patterns.py`. **Verdict: FAIL** — as the
a-priori prior predicted, and SIGNAL-DEAD (not gap-dwelling, not cost-gated). Frozen
tripwire GREEN.

## TL;DR

Rule-based (NOT LLM) detection of the long-side reversal *shapes* retail traders are taught
— double-bottom + inverse-head-and-shoulders, causal detector, entered on a fresh neckline
break at close → next open — produces **no edge** on the 39 survivor mega-caps: gate
2000–13 **−0.14% CAGR / 50.4% DD / Sharpe 0.09**, secondary **1.67% / 0.19**. It fails both
D1 tiers, loses to SPY *and* to equal-weight buy-hold of its own survivor universe, and it
is **signal-dead** — even frictionless (Rung B) the gate is +0.61% ≈ 0, and Rung A ≈ Rung B
(no overnight-gap story to tell). The chart *shape* carries no directional information on
the long side. **The terminal claim upgrades: even the shapes don't trade at retail EOD.**
The payload is in the short-side diagnostic (below): the survivor universe doesn't just
flatter longs — it *destroys* the one documented pattern edge.

## Results — decomposition ladder (gate 2000–13 / secondary 2014–; 314 gate entries)

| rung / arm | gate CAGR / DD / Sharpe | secondary CAGR / DD / Sharpe |
|---|---|---|
| **C — next-open, 5 bps (MAIN)** | **−0.14% / 50.4% / 0.09** | 1.67% / 36.8% / 0.19 |
| B — next-open, 0 bps | 0.61% / 49.0% / 0.13 | 2.39% / 35.7% / 0.24 |
| A — c2c, 0 bps (upper bound) | −0.06% / 52.0% / 0.09 | 2.33% / 37.8% / 0.23 |
| C — stress 15 bps | −1.62% / 53.2% / 0.01 | 0.26% / 39.1% / 0.09 |
| SPY buy-hold | 1.72% / — / 0.19 | 11.98% / — / 0.74 |
| EW-39 (survivor, survivorship-clean) | −0.47% / — / 0.13 | 13.97% / 0.78 |

Hold sensitivity (descriptive, next-open 5 bps, NOT gated, NOT tuned): hold=10 → gate
−3.03% / Sh −0.15; hold=40 → gate −3.58%, sec +6.06% (a one-window bull artifact, the same
shape every prior one-window "pass" showed). None rescues the gate; the verdict stays the
pre-committed 20-session baseline.

**Verdict:** gate CAGR −0.14% ≪ 15% AND gate Sharpe 0.09 < 0.80 → **PASS-HR FAIL, PASS-RA
FAIL** (loses SPY's Sharpe in the gate, and loses both SPY and EW-39 in the secondary). 314
gate entries ≫ 30 floor → not inconclusive. Per the asymmetric clause a FAIL on this
survivor universe is **clean**.

## Interpretation — SIGNAL-DEAD, and a survivorship payload

- **Signal-dead, not executed by gap or cost.** Rung A (c2c) ≈ Rung B (next-open) ≈ 0% in
  the gate: unlike the IBS family (which lost >½ its edge A→B to the overnight gap) or E13
  (cost-gated), the long-reversal shape has **no gross edge to lose.** The completion of a
  double-bottom / inverse-H&S carries no usable directional information for these names. This
  is the E14 category (signal-dead), not the gap/cost category — the cleanest kind of
  negative.
- **It loses to its own survivorship-clean benchmark.** Gate EW-39 buy-hold is −0.47%; the
  pattern strategy's −0.14% is not an edge over simply holding the same names — it is noise
  around a flat, brutal 2000–13 tape for mega-caps.
- **The payload — the survivor universe DESTROYS the documented (short-side) pattern edge.**
  The reported forward-20-session diagnostic (never traded): after a **long-reversal**
  (double-bottom / iH&S) completion the mean fwd-20 return is **+0.82%**, *below* the
  unconditional **+1.15%**; after a **bearish** (double-top / H&S) completion it is **+1.70%**,
  *above* unconditional. That is the **opposite** of what retail TA teaches and the opposite
  in sign of Savin-Weller-Zvingelis (2007), who found H&S predicts *under*performance. Why
  the inversion here: **survivorship removed exactly the names that would validate a bearish
  pattern** — the stocks whose head-and-shoulders correctly foretold a decline are the ones
  that fell out of the universe. On a survivor mega-cap set, a "top" pattern is just a pause
  in a name that (by construction) kept rising. So the survivor bias does not merely inflate
  long dip-buying (E16/C1) — it *structurally erases* the one pattern edge the literature
  documents. A cleaner illustration of the asymmetric-falsification framing than the program
  has produced before.
- **Every internal prediction held.** The M11.1 brief predicted FAIL: LMW's "informative ≠
  profitable," the deployable long side is the weakest-supported side, and the program's own
  breakout kills (E8/E11/C3) + reversal decay (E16/C1) pointed here. Confirmed.

## Honest caveats

- Survivor universe → a PASS would have been UNINTERPRETABLE; only this FAIL is clean.
- Close-based pivots (LMW convention) + one consolidated spec + pinned parameters (never
  tuned post-result). Different-but-reasonable parameters could move the numbers; the verdict
  is the pre-committed one. Oversubscription drops (738 gate) are the K=3 cap on clustered
  signals — disclosed, not silent; a larger K would dilute toward EW-39 (already −0.47%).
- Next-open execution: the A≈B ladder shows the gap is not the story here (unlike IBS), so
  a close-entry (MOC) variant would not rescue it.

## Program status

M11 = attempt 34 (FAIL), and the **9th equity strategy family** (price-geometry
pattern-completion — the first family that trades *shape* rather than a *number*). Tally:
**1 IN-SAMPLE-COMPOSED PASS-HR (M10-1, forward-only) + 1 weak PASS-RA (E18) / 0 clean
high-return edges / 34 attempts.** The terminal claim upgrades to include the chart-pattern
family: *even the chart shapes retail traders are taught do not trade at retail EOD, K=1–3,
$100–1,000 scale* — and the survivor universe destroys the one documented (bearish) pattern
edge along the way. The one lever that could still validate M10-1 remains **M3 forward paper
(Evan-gated)**.

## Reproduction

`.venv\Scripts\python.exe scripts/run_m11_chart_patterns.py`. Reuses `cache_fetch`/`UNIV`
(39 survivors), close-based causal pivots (w=5). Tripwire GREEN (12 refs d=0).

## Sources

M11.1 brief (`docs/research/2026-07-14_chart_pattern_detection_brief.md`); Lo-Mamaysky-Wang
(2000); Savin-Weller-Zvingelis (2007); Sullivan-Timmermann-White (1999); Bajgrowicz-Scaillet
(2012). Program priors: E8/E11/C3 (breakout kills), E16/C1 (reversal decay), EX-DECOMP
(overnight gap), X2/X2b (the short-side wall).
