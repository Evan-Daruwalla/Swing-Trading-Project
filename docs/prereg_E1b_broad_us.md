# Pre-registration — E1b: IBS mean reversion on broad-US index ETFs (out-of-sample test)

**Committed 2026-07-09 (PRD fallback branch after E1 FAIL, record Appendix O),
BEFORE running E1b or viewing any broad_us-specific holdout result. Every
parameter is FIXED; a change requires a new dated pre-registration.**

## 0. Honesty disclosure (why this experiment is shaped this way)

E1 (full 29-ETF universe) FAILED its kill criteria (record Appendix O). In
the per-group breakdown, `broad_us` alone cleared all four criteria
FULL-SAMPLE (Sharpe 0.60). **That selection is in-sample-informed** — I chose
broad_us because it looked best after seeing results, so its full-sample
number is contaminated and is NOT evidence. The ONLY clean test is
out-of-sample: a holdout period whose broad_us-specific performance has not
been observed. **Stated prior (pre-results): I expect decay** — the full
universe's 2022–2026 Sharpe was 0.01, so broad_us likely weakened too. E1b
exists to convert that prior into a pre-registered, falsifiable result.

## 1. Hypothesis

IBS mean reversion has an *executable* edge on broad US equity-index ETFs
that PERSISTS out-of-sample (into 2022–2026), clearing the same bar E1 was
held to.

## 2. Universe (fixed)

- **PRIMARY: `broad_us` = SPY, QQQ, DIA, IWM** (4 ETFs, from the frozen
  `swing_bot/universe.py`).
- **SECONDARY (reported, NOT a gate): broad_us + spdr_sector** (15 ETFs) —
  pre-declared here so it cannot be cherry-picked later. Sectors were
  marginal in E1 (Sharpe 0.31); including them is expected to dilute, not
  help.

## 3. Rules (IDENTICAL to E1 `8963e49` — only universe + eval protocol differ)

IBS<0.20 entry at close (skip high==low); exit first close IBS>0.80 OR 5-day
time stop; long-only; K=5 concurrent at capital/5 each ($500 nominal);
lowest-IBS-first selection, ties alphabetical; next-open PRIMARY fill
(c2c reported); 5 bps/side (=10 bps round-trip) primary cost. No parameter
is re-tuned — reusing E1's exact engine (`swing_bot/backtest.py`).

## 4. Evaluation protocol (the new part)

- **Train / context window: 2014-01-02 .. 2021-12-31** — reported to confirm
  the in-sample signal is genuinely present in broad_us. NOT the gate.
- **HOLDOUT / decisive window: 2022-01-01 .. 2026-07-08** — broad_us-specific
  performance here is UNSEEN as of this commit. **This is the gate.**

## 5. Kill criteria — E1b PASSES only if the HOLDOUT clears ALL (fixed)

Evaluated on the HOLDOUT window, PRIMARY universe (broad_us), next-open, net
of 10 bps round-trip:

1. **N:** ≥ 100 closed trades. (Floor set to 100, not E1's 200, because the
   holdout is ~4.5 yr on 4 ETFs — adjusted NOW, pre-results, by window length
   only, not by any observed outcome.)
2. **Expectancy:** net mean return per trade > 0.
3. **Risk-adjusted:** net annualized Sharpe ≥ 0.50.
4. **Drawdown:** max drawdown ≤ 25%.

If ANY fails → **E1b FAILS.** No tuning; a FAIL is the result (and would be
strong evidence the IBS edge has decayed even in its best subset).

**Reported alongside (context, NOT gates):** train-window metrics; the
secondary broad_us+sectors universe on the holdout; c2c and 0/20 bps
sensitivities on the holdout.

## 6. Live gate (unchanged)

Even on an E1b PASS, live paper (M3) still requires Evan's explicit go + an
Alpaca paper account (BLOCKED-ON-EVAN). A backtest PASS authorizes nothing
live by itself.

## 7. No-change clause

Parameters in §§2–5 are frozen as of this commit. Implementation ambiguities
resolve to the most literal reading, noted in the record, never toward better
results. Any change is a new dated pre-registration.
