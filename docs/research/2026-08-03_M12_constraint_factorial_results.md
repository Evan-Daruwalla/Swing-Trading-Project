# M12 — constraint-relaxation factorial: **HORIZON binds, breadth does not**

**Swing Trading · 2026-08-03 (CDT) · attempt #38 · DIAGNOSTIC, no PASS/FAIL issued**
Prereg: `docs/prereg_m12_constraint_factorial.md`, committed doc-only as **`43e4d42`**,
before `scripts/run_m12_factorial.py` existed.
Universe: `swing_bot/universe_m12.py` — 142 large-caps, frozen `b2a421a`.

> ## ⚠ CORRECTED 2026-08-03 — the originally published SEC numbers were WRONG
>
> A cold audit found that `cache_fetch` had **no freshness check** and returned
> cached price files of mixed vintage: of these 142 tickers, **38 ended
> 2026-07-10 while 104 ran to 2026-07-31**. The date axis was a *union*, so the
> 38 short names read `None` for the final 15 sessions and were marked at **zero**
> — not a price. Every number in the **SEC** window was affected; the **GATE**
> window reproduces exactly and is unchanged.
>
> **The headline SEC horizon effect was overstated 3×: published +5.84 pp →
> actual +1.87 pp.** The qualitative conclusion survives (horizon helps, breadth
> hurts — breadth in fact hurts *more*), but the original magnitudes did not.
>
> Root cause fixed in `run_e8_squeeze.cache_fetch` (optional `through=` freshness
> contract) and `run_m12_factorial.load()` (date axis truncated to the earliest
> final bar, mixed vintage reported loudly). Every table below is the corrected
> re-run. Original values are preserved in record DU and its correction DV.

## TL;DR

**Horizon was the binding constraint; concentration was not — and the program's
own stated explanation was wrong.** Lengthening the hold from 10 → 63 sessions
adds **+8.0 pp (GATE) / +1.9 pp (SEC)** of CAGR at 5 bps, and **+12.3 / +7.1 pp
at 15 bps** — the effect *grows with cost*, which is the mechanical signature of a
turnover problem (turnover falls 50.2× → 7.7× per year). Widening K from 3 → 20
adds only +1.3 pp in GATE and **subtracts 10.2 pp in SEC**, and the interaction is
**negative** (−8.0 pp GATE, −3.3 pp SEC): breadth actively destroys the horizon gain.

**But the winner still would not pass this project's own bar**, and it is
survivor-flattered — see §4. Nothing is deployed.

## 1. Results — 5 bps/side

| cell | hold | K | GATE (2000–2013) | SEC (2014→) | turnover |
|---|---|---|---|---|---|
| ① BASELINE | 10 | 3 | +6.26% / DD 71.3% / Sh 0.35 | +26.66% / DD 36.9% / Sh 0.84 | 50.2×/yr |
| **② H (horizon)** | **63** | **3** | **+14.24% / DD 63.8% / Sh 0.56** | **+28.53% / DD 34.3% / Sh 0.89** | **7.7×/yr** |
| ③ C (breadth) | 10 | 20 | +7.53% / DD 53.3% / Sh 0.42 | +16.43% / DD 31.2% / Sh 0.82 | 50.3×/yr |
| ④ H+C (both) | 63 | 20 | +7.50% / DD 59.9% / Sh 0.41 | +14.96% / DD 35.2% / Sh 0.75 | 7.9×/yr |
| *EW buy-hold (bench)* | — | 142 | +10.42% / DD 51.2% / Sh 0.59 | +12.11% / DD 37.0% / Sh 0.77 | — |

**Effects (CAGR, pp vs baseline):**

| effect | GATE | SEC |
|---|---|---|
| horizon alone | **+7.98** | **+1.87** |
| breadth alone | +1.28 | **−10.23** |
| interaction | **−8.01** | **−3.34** |

## 2. Results — 15 bps/side (the stress leg)

| cell | GATE | SEC |
|---|---|---|
| ① BASELINE | +1.04% / Sh 0.20 | +20.45% / Sh 0.70 |
| **② H** | **+13.33% / Sh 0.53** | **+27.50% / Sh 0.87** |
| ③ C | +2.26% / Sh 0.21 | +10.72% / Sh 0.58 |
| ④ H+C | +6.65% / Sh 0.38 | +14.04% / Sh 0.71 |

| effect | GATE | SEC |
|---|---|---|
| horizon alone | **+12.29** | **+7.05** |
| breadth alone | +1.21 | −9.72 |
| interaction | −7.90 | −3.73 |

**The horizon effect grows ~54% in GATE and ~3.8x in SEC when costs triple, while
the breadth effect stays flat.** That is the decisive mechanistic evidence: the short-hold cells were
being eaten by turnover, exactly as X9 (~16%/yr of drag) predicted.

## 3. What this overturns

The program has been asserting — most explicitly in the cross-project comparison
(record CY) — that:

> *the problem is not that factors fail — it is that Swing's retail constraints
> (K=1–4, $1K, liquidity floor) forbid the breadth the premium requires.*

**M12 says that was wrong.** Breadth was not the binding constraint. Going from
K=3 to K=20 helped negligibly in GATE and *hurt materially* in SEC, because at
K=20 of 142 you hold 14% of the universe and the portfolio converges toward the
equal-weight benchmark — which is precisely what the numbers show (cell ③ SEC
+16.43% drifting toward EW's +12.11%, while cell ② stays at +28.53%).

The real binding constraint was **turnover**: rebalancing every 10 sessions paid
~50× annual turnover (50.2 vs 7.7 at the long hold), and the momentum signal's
edge could not clear that toll.
This is the same lesson X9 delivered ("the signal is smaller than the toll"),
now confirmed by direct experiment rather than inference.

## 4. What this does NOT establish — read before getting excited

- **Cell ② would still FAIL this project's D1 bar.** PASS-HR needs CAGR ≥ 15% AND
  maxDD ≤ 60% in **both** windows. Cell ② posts GATE **CAGR 14.24% (< 15%)** and
  **DD 63.8% (> 60%)**. It fails on *both* GATE criteria — narrowly on return,
  clearly on drawdown. At 15 bps GATE CAGR is 13.33%, still short. **The
  best cell in the factorial is not a passing strategy.**
- **Survivorship.** All 142 names still trade today; the universe is biased in the
  strategy's favour. Under the project's standing rule **only a FAIL is clean** —
  cell ②'s +28.5% SEC is *uninterpretable as evidence of edge*, which is exactly why
  the prereg forbade deploying any cell off this run.
- **Diagnostic, not a gate.** Per prereg §6, M12 issues no PASS/FAIL and no cell
  becomes a sleeve here. Picking the best of four and deploying it is in-sample
  composition — the M10-1 mistake, already documented and capped.
- **Not decorrelated.** corr(cell ④, e6 rule) = **+0.587** over 6,668 sessions, so
  these momentum cells are *moderately correlated* with the live trend sleeves —
  they would not solve the standing decorrelation problem either.
- **Drawdowns are brutal in GATE.** Three of four cells exceed 59% DD in GATE and
  the baseline hits 71.3%. (SEC drawdowns are milder, 31-37%.)
- **142 names is a 14% sort, not momentum_v2's 1%.** This tests the *direction* of
  the concentration effect, not its magnitude — a much wider universe could in
  principle behave differently.

## 5. Honest reading

The 2×2 did its job: it **attributed** the failure. The old constraint box was
losing to *transaction costs from over-trading*, not to a lack of breadth. That
resolves a question the program had been answering by assertion for weeks, and it
corrects the record.

It does **not** produce a deployable strategy. The single best configuration —
12-1 momentum, top-3, 63-session hold — clears neither D1 criterion in the GATE
window and sits on a survivor universe. The honest summary is: *we now know which
wall we were hitting, and the wall behind it is drawdown.*

## Provenance

- Prereg `43e4d42` (doc-only) → runner `scripts/run_m12_factorial.py`.
- Universe frozen `b2a421a` (142 names, empirical `data_start`s, survivorship
  disclosed in the module docstring).
- All 142 tickers pre-cached. NOTE: the cache was MIXED-VINTAGE at first run; the
  corrected run truncates the date axis to the earliest final bar (2026-07-10).
- No `swing.db` writes; frozen tripwire GREEN (d = ±0.0000pp); the three live M3
  sleeves were **not modified**.
