# E6 results — de-leveraged 200-MA rotation: VERDICT = PASS (2026-07-09)

Per pre-registration `0526ea2`. **No tuning.** After E4/E5 showed the 3×
rotation is a regime-flattered mirage (92.7% drawdown in 2000–2013), E6 tests
whether the SAME timing rule at 1× is a robust drawdown-management overlay —
across all three regimes at once.

## Results (per window)

| window | strategy | CAGR | %/mo | maxDD | Sharpe | MAR |
|---|---|---|---|---|---|---|
| **2000–2013** (crashes) | **1× rotation** | +2.66% | +0.22% | **52.2%** | **0.24** | 0.05 |
| | buy-hold QQQ | −0.53% | −0.04% | 83.0% | 0.14 | −0.01 |
| **2014–2026** (bull) | **1× rotation** | +14.47% | +1.13% | **24.6%** | **0.92** | 0.59 |
| | buy-hold QQQ | +18.30% | +1.41% | 35.6% | 0.89 | 0.51 |
| **2000–2026** (full) | **1× rotation** | +8.04% | +0.65% | **52.2%** | **0.54** | 0.15 |
| | buy-hold QQQ | +7.92% | +0.64% | 83.0% | 0.42 | 0.10 |

2× synthetic (drag calibrated to real QLD at 2.00%/yr, synth CAGR 30.97% vs
real 31.11% — validated) is SECONDARY context: full-period CAGR 12.05%
(+0.95%/mo) but 80.0% maxDD and Sharpe 0.51 — **below 1×'s 0.54.** More
leverage adds drawdown faster than return; the rotation's value is at LOW
leverage.

## Kill criteria (1× cell)

| # | criterion | result |
|---|---|---|
| 1 | maxDD ≥10pp below buy-hold-QQQ in both crash windows | 52.2% vs 83.0% (−31pp) PASS |
| 2 | Sharpe ≥ buy-hold-QQQ in ALL 3 windows | 0.24≥0.14, 0.92≥0.89, 0.54≥0.42 PASS |
| 3 | CAGR > 0 in all 3 windows | +2.66 / +14.47 / +8.04 PASS |

### E6 VERDICT: PASS — the first robust, regime-spanning result in the project.

## Honest interpretation

1. **This IS a real, robust effect** — and it passes the exact regime test E4
   failed. The 200-MA overlay improves risk-adjusted return (Sharpe) in EVERY
   regime and roughly HALVES the worst drawdown (83%→52%) by sitting in cash
   through the dot-com and 2008/2022 declines. At 1×, whipsaws cost a little
   but never compound into ruin — the opposite of the 3× case.
2. **But it is NOT the high-return goal, and that must be stated plainly.**
   Full-period CAGR is 8.04% — essentially identical to buy-and-hold QQQ's
   7.92%. **The value is almost entirely drawdown reduction, not return.** At
   +0.65%/mo (full) / +1.13%/mo (bull), this does not meet "high percent
   return over a short time." It is a risk-managed equity core, not a
   return engine.
3. **In the bull it gave up return** (14.47% vs 18.30% CAGR, 2014–2026) to
   whipsaws — the honest, documented cost of trend-timing overlays. It is
   compensated by lower drawdown and a marginally higher Sharpe, not by more
   money.
4. **2× is not worth it:** it does not beat 1× on risk-adjusted return and
   reintroduces an 80% drawdown. The sweet spot is 1×.

## Disposition

E6 PASSES. De-leveraged 200-MA rotation is a **legitimate, robust,
deployable drawdown-management overlay** — the first thing the project has
produced that survives a regime-spanning pre-registered test. It is a
candidate for eventual paper as a *risk-managed core* (Evan-gated: Alpaca
account + go), explicitly **NOT** as the high-return objective, which remains
unmet. Per prereg §5 this is the last rotation-family experiment; next is the
write-up of the full program (Evan's option 1).

**The clean two-line summary of the whole rotation arc:** the high-return
version (3×, E4) is a bull-market artifact that loses 93% in a real bear; the
risk-managed version (1×, E6) is real but modest — it buys you half the
drawdown for roughly the same long-run return as just holding the index.
