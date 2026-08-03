# M12 — constraint-relaxation factorial: **HORIZON binds, breadth does not**

**Swing Trading · 2026-08-03 (CDT) · attempt #38 · DIAGNOSTIC, no PASS/FAIL issued**
Prereg: `docs/prereg_m12_constraint_factorial.md`, committed doc-only as **`43e4d42`**,
before `scripts/run_m12_factorial.py` existed.
Universe: `swing_bot/universe_m12.py` — 142 large-caps, frozen `b2a421a`.

## TL;DR

**Horizon was the binding constraint; concentration was not — and the program's
own stated explanation was wrong.** Lengthening the hold from 10 → 63 sessions
adds **+8.0 pp (GATE) / +5.8 pp (SEC)** of CAGR at 5 bps, and **+12.3 / +10.8 pp
at 15 bps** — the effect *grows with cost*, which is the mechanical signature of a
turnover problem (turnover falls 50.5× → 8.3× per year). Widening K from 3 → 20
adds only +1.3 pp in GATE and **subtracts 7.3 pp in SEC**, and the interaction is
**negative (≈ −8 pp)**: breadth actively destroys the horizon gain.

**But the winner still would not pass this project's own bar**, and it is
survivor-flattered — see §4. Nothing is deployed.

## 1. Results — 5 bps/side

| cell | hold | K | GATE (2000–2013) | SEC (2014→) | turnover |
|---|---|---|---|---|---|
| ① BASELINE | 10 | 3 | +6.26% / DD 71.3% / Sh 0.35 | +21.19% / DD 59.3% / Sh 0.71 | 50.5×/yr |
| **② H (horizon)** | **63** | **3** | **+14.24% / DD 63.8% / Sh 0.56** | **+27.04% / DD 37.8% / Sh 0.85** | **8.3×/yr** |
| ③ C (breadth) | 10 | 20 | +7.53% / DD 53.3% / Sh 0.42 | +13.91% / DD 31.6% / Sh 0.70 | 50.4×/yr |
| ④ H+C (both) | 63 | 20 | +7.50% / DD 59.9% / Sh 0.41 | +12.80% / DD 35.2% / Sh 0.65 | 8.1×/yr |
| *EW buy-hold (bench)* | — | 142 | +10.42% / DD 51.2% / Sh 0.59 | +9.41% / DD 37.0% / Sh 0.59 | — |

**Effects (CAGR, pp vs baseline):**

| effect | GATE | SEC |
|---|---|---|
| horizon alone | **+7.98** | **+5.84** |
| breadth alone | +1.28 | **−7.28** |
| interaction | **−8.01** | **−6.95** |

## 2. Results — 15 bps/side (the stress leg)

| cell | GATE | SEC |
|---|---|---|
| ① BASELINE | +1.04% / Sh 0.20 | +15.24% / Sh 0.57 |
| **② H** | **+13.33% / Sh 0.53** | **+26.01% / Sh 0.82** |
| ③ C | +2.26% / Sh 0.21 | +8.32% / Sh 0.47 |
| ④ H+C | +6.65% / Sh 0.38 | +11.89% / Sh 0.62 |

| effect | GATE | SEC |
|---|---|---|
| horizon alone | **+12.29** | **+10.77** |
| breadth alone | +1.21 | −6.92 |
| interaction | −7.90 | −7.19 |

**The horizon effect grows ~50–85% when costs triple, while the breadth effect is
unchanged.** That is the decisive mechanistic evidence: the short-hold cells were
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
+13.91% drifting toward EW's +9.41%, while cell ② stays at +27.04%).

The real binding constraint was **turnover**: rebalancing every 10 sessions paid
~50× annual turnover, and the momentum signal's edge could not clear that toll.
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
  cell ②'s +27% SEC is *uninterpretable as evidence of edge*, which is exactly why
  the prereg forbade deploying any cell off this run.
- **Diagnostic, not a gate.** Per prereg §6, M12 issues no PASS/FAIL and no cell
  becomes a sleeve here. Picking the best of four and deploying it is in-sample
  composition — the M10-1 mistake, already documented and capped.
- **Not decorrelated.** corr(cell ④, e6 rule) = **+0.587** over 6,668 sessions, so
  these momentum cells are *moderately correlated* with the live trend sleeves —
  they would not solve the standing decorrelation problem either.
- **Drawdowns are brutal everywhere.** Every cell exceeds 30% DD in SEC and three
  of four exceed 59% in GATE. Baseline hits 71.3%.
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
- All 142 tickers pre-cached, so the run was fully offline and reproducible.
- No `swing.db` writes; frozen tripwire GREEN (d = ±0.0000pp); the three live M3
  sleeves were **not modified**.
