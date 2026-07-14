# X1 — Conditional volatility targeting (E6 × E18): RESULTS

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Prereg:** `prereg_x1_vol_targeting.md` (committed `07c22cb`, doc-only, predates the
runner). **Runner:** `scripts/run_x1_vol_targeting.py`. **Verdict:** **FAIL
(descriptive, overlay).** Frozen tripwire GREEN.

---

## TL;DR

The conditional rule — de-risk SPY only when volatility is elevated **and** trend is
broken (stay invested when vol spikes inside an uptrend) — **does not beat the plain
200-DMA overlay.** In the 2006–2013 gate the simple E6 200-DMA arm is the **best** risk
manager (Sharpe 0.58, maxDD 19.9% vs SPY's 0.32 / 56.5%); the conditional arm ties the
VIX-TS arm (Sharpe 0.42) and loses to E6. H1 rejected, null survives — **confirming
E18's finding that no vol gate beats the plain 200-DMA.** Conditioning on VIX just keeps
the sleeve invested more (89% exposure), diluting the drawdown protection. PASS-HR is
unreachable for a leverage-free overlay; the PASS-RA bar is failed. Descriptive (one
gate window ≈ one crash → low effective N).

---

## Results (SPY overlay, next-open, 1 bp/side)

**GATE 2006–2013:**

| arm | CAGR | maxDD | Sharpe | exposure | toggles |
|---|---:|---:|---:|---:|---:|
| **(a) E6 200-DMA** | 6.16% | **19.9%** | **0.58** | 70.0% | 58 |
| (b) E18 VIX-TS | 5.28% | 36.5% | 0.42 | 84.4% | 142 |
| **(c) conditional** | 5.48% | 37.3% | 0.42 | 88.7% | 92 |
| SPY buy-hold | 4.83% | 56.5% | 0.32 | 100% | 0 |

**SECONDARY 2014–:**

| arm | CAGR | maxDD | Sharpe | exposure |
|---|---:|---:|---:|---:|
| (a) E6 200-DMA | 7.47% | 22.1% | 0.68 | 82.2% |
| (b) E18 VIX-TS | 10.02% | 30.4% | 0.78 | 92.3% |
| (c) conditional | 10.44% | 30.3% | 0.77 | 95.3% |
| SPY buy-hold | 11.98% | 34.1% | 0.74 | 100% |

**Arm (c) cost stress:** 1 bp gate Sharpe 0.42 → 5 bp 0.39 → 15 bp 0.32 (cost-robust;
cost is not the issue).

**Verdict:** (c) gate Sharpe **0.42 < 0.80**, and (c) does **not** beat both plain
overlays (ties (b) at 0.42, loses to (a) at 0.58) → **FAIL** against the pre-registered
PASS-RA bar.

---

## Interpretation

- **The simple 200-DMA overlay (E6) is the best risk manager, again.** It cuts the
  gate drawdown from 56.5% to 19.9% (−36.6 pp) at Sharpe 0.58 — decisively better than
  either VIX-conditioned arm. This re-confirms E18's terminal finding and the program's
  standing conclusion: **1× 200-DMA rotation is the one deployable risk overlay, and
  volatility-timing embellishments do not improve it.**
- **Why the conditional rule fails its own hypothesis.** Requiring *both* vol-elevated
  AND trend-broken to de-risk means it stays invested far more (89% vs E6's 70%
  exposure), so it barely de-risks at all — its drawdown (37.3%) is close to buy-hold,
  not to E6. The "stay invested when vol spikes inside an uptrend" intuition is real,
  but in practice the binding drawdowns (2008) are exactly when trend *is* broken, so
  the extra condition mostly just removes E6's protective exits during choppy-but-
  down-trending stretches.
- **Secondary window:** all three overlays trail SPY buy-hold on CAGR in the 2014→ bull
  (as expected — de-risking costs return in a bull), and (c)'s Sharpe (0.77) edges SPY
  (0.74) but not enough, and the gate leg already failed.
- **Descriptive, as pre-registered:** one gate window with essentially one crash → low
  effective N; this is a directional read, not a validated edge. No new pass; PASS-HR
  stays 0, and the only weak PASS-RA in the program remains E18's VIX-TS (which X1
  shows is itself dominated by plain E6 on drawdown).

## Honest caveats

- **Low effective N** (~one gate crash) — descriptive only.
- **SPY only** — E7 showed 200-DMA overlays are market-dependent; no cross-market claim.
- **Gate is 2006–2013** (VIX3M floor), not the full 2000–2013 hostile window.
- Overlay class → risk-management, never the high-return goal.

## Reproduction

- `.venv\Scripts\python.exe scripts/run_x1_vol_targeting.py`
- Tripwire: `.venv\Scripts\python.exe -m swing_bot.test_frozen` → GREEN (12 refs d=0).

## Sources (dated)

- Moreira & Muir — *Volatility-Managed Portfolios* (JF 2017) / FAJ 2020 practitioner
  version.
- Prior project: E18 regime-gate bake-off (`docs/research/2026-07-11_E18_results.md`);
  E6/E7 rotation results; prereg `prereg_x1_vol_targeting.md`.
