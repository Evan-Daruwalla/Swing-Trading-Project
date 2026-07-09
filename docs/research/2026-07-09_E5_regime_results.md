# E5 results — E4 rotation across hostile regimes: VERDICT = FAIL (2026-07-09)

Per pre-registration `09a3a31`. **No tuning.** This test attacked E4's
regime-flattery directly by reaching the 2000–2013 era (dot-com + 2008) that
E4's 2014–2026 data excluded. It caught a real problem.

## Validation gate — the synthetic is trustworthy (PASS)

Synthetic daily-rebalanced 3× Nasdaq, drag calibrated to real TQQQ over
2014–2026:
- Calibrated drag **4.00%/yr** (expense + financing; sane for a 3× fund).
- Synthetic CAGR 38.31% vs **real TQQQ 38.36%** — 0.05 pp apart.
- Daily-return correlation **0.9989** (needed ≥0.99).

The synthetic faithfully reproduces real TQQQ, so the 2000–2013 extension is a
legitimate test, not an artifact.

## The verdict (2000–2013 UNSEEN window)

| criterion | got | result |
|---|---|---|
| rotation CAGR > 0 | **−3.37%** (−0.28%/mo) | **FAIL** |
| maxDD ≤ 65% AND ≥25pp below buy-hold-3× | **92.7%** vs BH-3× 100.0% | **FAIL** |
| rotation CAGR ≥ buy-hold-QQQ (1×) | −3.37% vs −0.53% | **FAIL** |

### E5 VERDICT: FAIL (all three gates)

## Full picture

| window | rotation CAGR (%/mo) | rotation maxDD | buy-hold-3× CAGR / maxDD | buy-hold-QQQ CAGR |
|---|---|---|---|---|
| **2000–2013 (unseen)** | **−3.37% (−0.28)** | **92.7%** | −28.87% / 100.0% | −0.53% |
| 2014–2026 (seen) | +34.31% (+2.49) | 60.1% | 38.31% / 81.6% | 18.30% |
| 2000–2026 (full) | +12.77% (+1.01) | 92.7% | −2.74% / 100.0% | 7.92% |

## What actually happened

**The 200-day MA did NOT protect in 2000–2013 — a 92.7% drawdown.** The
failure mode is whipsaw: in choppy secular bear markets (2000–2002, 2008),
violent counter-trend rallies push QQQ back above its 200-day MA, the strategy
re-enters 3× leverage, and the next leg down destroys it — repeatedly. Buy-and-
hold 3× was mathematically wiped out (−100%: a 3× fund cannot survive an ~−83%
underlying decline). The rotation "only" lost 92.7% — nominally better, but
still catastrophic and untradeable.

**E4's +2.45%/mo was entirely a 2014–2026 regime artifact.** Across the full
quarter-century the strategy made ~1%/mo *with a 93% drawdown* — the exact
"leverage rode a secular bull" outcome I flagged when E4 passed. The
pre-registered regime test converted that suspicion into proof.

The one honest point in the strategy's favor: over the full window it did beat
buy-and-hold 3× (+12.77% vs −2.74% CAGR, 92.7% vs 100% maxDD) — the timing
adds *some* value over blindly holding 3×. But "better than a total wipeout"
is not tradeable, and it underperformed even unlevered QQQ in the hostile era.

## Disposition

Per prereg §5: **E5 FAIL → E4 is regime-dependent → do NOT deploy to paper on
2014–2026 evidence.** E4 is de-authorized as a live-paper candidate. No
tuning; the result stands.

This is the hardening test doing precisely its job: it stopped a strategy that
looked like a 33%-CAGR winner but would have lost 93% in a different decade,
*before* any capital or months of attention were committed. That caught-it-
before-deploying outcome is the highest-value thing the rigor process can
produce.
