# Pre-registration — E4: 200-day-MA leverage rotation (TQQQ/QQQ)

**Committed 2026-07-09 (PRD M2d), BEFORE the E4 robustness-battery runner
(`swing_bot/rotation.py` / `scripts/run_e4_rotation.py`) exists. Parameters
FIXED; a change requires a new dated pre-registration.**

## 0. Honesty disclosure — what is and is NOT clean here

The B4 screen (record Appendix Y) ALREADY measured the primary cell
(TQQQ held while QQQ > 200-day SMA, next-open switch, 5bps/side): full-window
CAGR 33.75%, holdout +2.15%/mo. **That cell is contaminated — I have seen it.**
So E4 does NOT claim git-ordering purity on the primary number the way E1
could. Instead E4's kill-criteria target what is UNSEEN:

1. **Fragility** across an MA-length / execution-lag / cost grid I have not
   run (only the single MA200/lag0/5bps cell was screened).
2. **Benchmark-relative value:** does the 200-MA TIMING actually add value
   over just buy-and-holding TQQQ (leverage) or QQQ (equity)? — never
   measured.
3. **Live paper** is named as the ONLY truly clean out-of-sample test; a
   backtest PASS authorizes nothing but a paper deployment (Evan-gated).

## 1. Hypothesis

Rotating a 3× Nasdaq fund by its underlying's 200-day trend (a) delivers a
high absolute return, (b) with a drawdown materially below buy-and-hold 3×,
and (c) is NOT a knife-edge artifact of the exact MA length / execution
timing / cost assumed — i.e. the effect is robust across a neighborhood.

## 2. Instrument & rules (fixed)

- **PRIMARY: signal = QQQ, position = TQQQ.** Long-only, K=1 (full capital in
  one instrument — the extreme of the goal's K=1–3 concentration).
- **Rule:** at the CLOSE of day T compute the signal ETF's N-day simple
  moving average. If close > SMA(N) → target = 100% position fund; else →
  100% cash. When the target differs from the current state, switch at the
  OPEN of day T+1 (execution lag 0 = next open). One position, no fractional
  ambiguity (whole-dollar via fractional shares in backtest).
- **Cost:** applied to each switch fill, per side.
- **Data:** `swing.db`, split-adjusted / dividend-UNADJUSTED, full window
  2014-01-02 .. 2026-07-08 (TQQQ data_start 2010, QQQ 1999 — full coverage).

## 3. Robustness battery (the gate grid — UNSEEN until the run)

Cartesian grid, PRIMARY signal=QQQ / fund=TQQQ:
- **MA length N ∈ {150, 175, 200, 225, 250}**
- **execution lag ∈ {0 (next open), +1 (open after)}**
- **cost ∈ {5, 10} bps per side**

= 20 cells. Evaluated on the FULL window (holdout is contaminated, so the
full window is the honest basis and the doc says so). Also computed for
context (SECONDARY, not gates): fund=SPXL/signal=SPY; fund=SOXL/signal=SOXL-
self; buy-and-hold TQQQ and buy-and-hold QQQ benchmarks.

## 4. Kill criteria — E4 PASSES only if ALL (fixed)

Evaluated on the PRIMARY cell (QQQ→TQQQ, N=200, lag 0, 5bps) unless a grid
statement is given:

1. **Return:** primary-cell full-window CAGR ≥ 15% (≈ +1.17%/mo).
2. **Ruin guard:** primary-cell max drawdown ≤ 65%. (Loosened for 3× per the
   accepted-risk goal, but present — a 3× fund can approach zero in a fast
   crash; 65% is the "painful but not wipeout" line.)
3. **Timing adds value (the real test):**
   (a) primary-cell max drawdown ≤ buy-and-hold-TQQQ max drawdown − 15
       percentage points (the rotation must demonstrably cut leverage
       drawdown), AND
   (b) primary-cell CAGR ≥ buy-and-hold-QQQ CAGR (you are compensated for the
       leverage + timing with at least equity-like return).
4. **Non-fragility (grid):** ≥ 80% of the 20 grid cells have full-window
   CAGR > 0, AND the median grid-cell CAGR ≥ 10%, AND no MA-length's cells
   are negative while an adjacent MA-length's are strongly positive (no
   cliff).

If ANY fails → **E4 FAILS.** No tuning; the grid and thresholds are frozen
here.

## 5. Live gate (unchanged, BLOCKED-ON-EVAN)

Even on PASS, live paper (M3) requires Evan's explicit go + an Alpaca paper
account. Live paper is the true out-of-sample test; the backtest only decides
whether it is worth deploying paper capital and attention.

## 6. No-change clause

§§2–4 are frozen as of this commit. Implementation ambiguities resolve to the
most literal reading, recorded, never toward better numbers. Any change is a
new dated pre-registration.
