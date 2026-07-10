# Pre-registration — E6: de-leveraged 200-MA rotation as a drawdown overlay

**Committed 2026-07-09 (PRD M2d, "risk-management" branch), BEFORE the E6
runner exists. Parameters FIXED. This is Evan's option 2: after E4/E5 showed
200-MA rotation at 3× is regime-dependent (92.7% drawdown in 2000–2013,
record Appendix AB), test whether the SAME timing rule at LOWER leverage is a
robust drawdown-management overlay.**

## 0. Honesty disclosures (read first)

1. **This is NOT the high-return goal.** 1× rotation cannot produce
   "high %/mo." E6 tests a different, humbler claim: does 200-MA timing
   improve RISK-ADJUSTED return across regimes enough to be a legitimate
   deployable overlay? Return gates are floors (don't destroy capital), not
   the objective.
2. **2000–2013 is now SEEN.** E5 already looked at that window (at 3×). E6
   changes the leverage, but the window is contaminated — E6 is
   confirmatory-on-seen-data testing a different leverage, NOT clean OOS.
   Live paper / other markets remain the only clean forward test.
3. **1× is the clean core** (real QQQ, zero synthesis assumptions). The 2×
   variant uses a synthetic and is SECONDARY context only, flagged.

## 1. Hypothesis

The 200-day-MA rotation (hold the instrument while QQQ > its 200-day SMA,
else cash) is, at 1× (QQQ itself), a ROBUST drawdown-management overlay: it
delivers a better risk-adjusted return than buy-and-hold QQQ in EVERY regime
(the two crash-containing windows and the bull window), primarily by cutting
drawdown, without destroying return.

## 2. Instrument & rules (fixed)

- **PRIMARY: 1× — signal = QQQ, position = QQQ** (real data, 1999→2026, no
  synthesis). Rotation rule identical to E4/E5: close > SMA(200) → hold, else
  cash; switch at next open; 5 bps/side.
- **SECONDARY (context, not a gate): 2× synthetic** (daily-rebalanced 2×
  QQQ, drag calibrated to real QLD 2× Nasdaq ETF over its overlap by the E5
  method). Flagged as synthetic-dependent.
- Benchmark: buy-and-hold QQQ (1×).

## 3. Windows

- **2000-01-01 .. 2013-12-31** (dot-com + 2008; seen at 3× in E5)
- **2014-01-02 .. 2026-07-08** (bull)
- **2000-01-01 .. 2026-07-08** (full)

## 4. Kill criteria — E6 PASSES only if ALL (fixed), on the PRIMARY 1× cell

1. **Crash protection:** 1×-rotation maxDD ≤ buy-hold-QQQ maxDD − 10 pp in
   BOTH the 2000–2013 and 2000–2026 windows (the core claim).
2. **Risk-adjusted improvement everywhere:** 1×-rotation annualized Sharpe ≥
   buy-hold-QQQ Sharpe in ALL THREE windows. (An overlay that only helps in
   one regime is not robust — this is the discriminating gate.)
3. **Return floor:** 1×-rotation CAGR > 0 in all three windows (does not
   destroy capital in any regime).

If ANY fails → **E6 FAILS.** No tuning. A FAIL means even de-leveraged, 200-MA
timing is not a robust improvement over buy-and-hold — a clean, publishable
result (the classic "MA timing costs you in bulls, helps in bears, no free
lunch" finding).

**Reported alongside (not gates):** per-window CAGR / %/mo / maxDD / Sharpe
for 1×-rotation, 2×-synth-rotation, and buy-hold QQQ; the MAR ratio
(CAGR/maxDD) per window.

## 5. Disposition

- **E6 PASS** → de-leveraged rotation is a legitimate risk-managed overlay
  (modest return, robust). A candidate for eventual paper as a
  drawdown-managed core — still Evan-gated, and explicitly NOT the
  high-return objective.
- **E6 FAIL** → 200-MA timing adds no robust risk-adjusted value even
  de-leveraged; the rotation idea is closed. Proceed to write up the full
  falsification program (Evan's option 1).

Either outcome, this is the last rotation-family experiment before the
write-up.

## 6. No-change clause

§§2–4 frozen as of this commit. Ambiguities resolve to the most literal
reading, recorded, never toward better numbers. Any change is a new dated
pre-registration.
