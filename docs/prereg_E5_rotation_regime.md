# Pre-registration — E5: E4 rotation across hostile regimes (2000–2013, unseen)

**Committed 2026-07-09 (PRD M2d hardening), BEFORE the E5 synthesis/runner
code exists. Parameters FIXED. Purpose: attack E4's single biggest weakness —
that its +2.45%/mo is 3× Nasdaq over the best tech decade (2014–2026) — by
testing the SAME rotation rule across the regimes most hostile to leveraged
tech: the 2000–2002 dot-com crash and 2008 GFC.**

## 0. Why this is genuinely unseen

E4 (record Appendix AA) was measured only on 2014–2026. The 2000–2013 window
— including a ~−83% Nasdaq dot-com bust and 2008 — has NEVER been looked at
for this strategy, and TQQQ did not exist then. E5 constructs a synthetic 3×
series to reach it. If the 200-MA rotation's value survives here, the
regime-flattery objection is substantially answered; if it fails, E4 is
regime-dependent and must NOT go to paper on the strength of 2014–2026 alone.

## 1. Hypothesis

The 200-day-MA rotation (hold 3×-Nasdaq while QQQ > 200-day SMA, else cash)
delivers, over the UNSEEN 2000–2013 window, (a) positive CAGR, (b) a max
drawdown far below buy-and-hold 3×-Nasdaq (the crash protection is the point),
and (c) at least unlevered-QQQ-equivalent return — i.e. the timing adds real
value in bad regimes, not just good ones.

## 2. Data & synthetic construction (fixed)

- Fetch QQQ full history (1999→2026) and real TQQQ (2010→2026) via the own
  fetcher (`auto_adjust=False`), into a SEPARATE analysis store — do NOT
  touch `swing.db` or the frozen universe.
- **Synthetic daily-rebalanced 3× Nasdaq:** `syn[t] = syn[t-1] × (1 + 3·r[t]
  − d)`, where `r[t]` = QQQ daily close-to-close return and `d` = daily drag.
  Daily rebalancing means ×3 of DAILY returns (correct model for a leveraged
  ETF), NOT ×3 of cumulative. Drag `d = D_annual/252`.
- **Drag calibration (fixed method):** choose `D_annual` so the synthetic's
  2014-01-02..2026-07-08 CAGR best matches REAL TQQQ's over the same window
  (grid search to nearest 0.25%/yr). Report the calibrated value.

## 3. Validation gate (synthetic must be trustworthy BEFORE any verdict)

Over the 2014–2026 overlap, the calibrated synthetic vs real TQQQ must show:
- daily-return Pearson correlation ≥ 0.99, AND
- |synthetic CAGR − real TQQQ CAGR| ≤ 3 percentage points.

If validation FAILS, E5 is inconclusive (synthetic untrustworthy) — reported
as such, NOT forced. **Honest caveat pinned now:** pre-2014 real leveraged
financing costs were materially higher than the near-zero-rate 2014–2021 era,
so a drag calibrated on 2014–2026 UNDERSTATES pre-2014 drag → the synthetic
is OPTIMISTIC for buy-and-hold pre-2014. This biases AGAINST the rotation's
relative case only mildly (protection is about being in CASH during crashes),
and is acceptable for a drawdown-protection test. Reported, not hidden.

## 4. Kill criteria — E5 (E4-regime-robustness) PASSES only if ALL (fixed)

Validation gate (§3) passes, AND on the UNSEEN **2000-01-01 .. 2013-12-31**
window (signal QQQ, position synthetic-3×, next-open switch, calibrated drag,
5 bps/side):

1. **Survives positive:** rotation CAGR (2000–2013) > 0.
2. **Crash protection:** rotation maxDD (2000–2013) ≤ 65% AND at least 25
   percentage points below buy-and-hold-synthetic-3× maxDD over the same
   window.
3. **Beats unlevered equity in the bad era:** rotation CAGR (2000–2013) ≥
   buy-and-hold-QQQ (1×) CAGR over the same window.

If ANY fails → **E5 FAILS** → E4 is judged regime-dependent; do NOT deploy to
paper on 2014–2026 evidence; record honestly. No tuning; drag METHOD and
gates are frozen here (the calibrated drag VALUE is data-derived per §2, not a
free parameter).

**Reported alongside (context, not gates):** full 2000–2026 rotation vs
buy-hold-3× vs buy-hold-QQQ; per-year return decomposition; drag sensitivity
at D_annual ∈ {calibrated, 1%, 5%}; the 2000–2013 vs 2014–2026 split.

## 5. Disposition

E5 PASS → the regime concern is materially addressed; E4 becomes a
defensible paper-deployment candidate (still Evan-gated for the Alpaca
account + go). E5 FAIL → E4 stays a 2014–2026-only artifact; no paper.
Live paper remains the only true forward OOS regardless.

## 6. No-change clause

§§2–4 frozen as of this commit. Ambiguities resolve to the most literal
reading, recorded, never toward better numbers. Any change is a new dated
pre-registration.
