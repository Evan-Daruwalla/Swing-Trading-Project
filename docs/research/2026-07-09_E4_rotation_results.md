# E4 results — 200d-MA leverage rotation: VERDICT = PASS (2026-07-09)

Per pre-registration `313d88a`. Full-window basis (holdout contaminated by
the B4 screen — prereg §0). **No tuning.** First strategy in the project to
clear a pre-registered gate — read the honest limitations below before
treating it as a green light.

## Kill criteria (primary cell: QQQ→TQQQ, N=200, lag 0, 5bps)

| # | criterion | got | result |
|---|---|---|---|
| 1 | CAGR ≥ 15% | 33.76% (+2.45%/mo) | PASS |
| 2 | max drawdown ≤ 65% | 57.7% | PASS |
| 3a | cuts buy-hold-TQQQ DD by ≥15pp | 57.7% vs 81.8% (−24pp) | PASS |
| 3b | CAGR ≥ buy-hold-QQQ | 33.76% vs 18.30% | PASS |
| 4 | non-fragile grid (≥80% cells +, median ≥10%, no cliff) | 100% +, median 32.5% | PASS |

### E4 VERDICT: PASS (all 5)

## Benchmarks (full window, the honest context)

| strategy | CAGR | %/mo | maxDD |
|---|---|---|---|
| buy-hold TQQQ | **38.36%** | +2.74% | **81.8%** |
| **E4 rotation** | 33.76% | +2.45% | **57.7%** |
| buy-hold QQQ | 18.30% | +1.41% | 35.6% |

**The rotation does NOT beat buy-and-hold TQQQ on return** (33.8% vs 38.4%).
Its entire value is drawdown reduction: it trades ~4.6 pp of CAGR to cut the
peak drawdown from 82% to 58%. This is risk-managed leverage, not return
enhancement. Sharpe 0.86 (vs a much lower implied Sharpe for 82%-DD buy-hold)
is where the value shows up — but a max-return-seeker could rationally just
hold TQQQ and accept the 82% drawdown. That trade-off is Evan's to make.

## Robustness battery (the genuinely un-peeked evidence — it held)

20 cells, QQQ→TQQQ, full window. ALL positive. CAGR range 21.3%–36.5%,
median 32.5%; maxDD 52.7%–68.3%.

- Mild gradient: longer MA → lower return / higher DD at lag 0 (N=250 lag0 =
  21.3% CAGR / 68% DD, the weakest cell but still well positive).
- +1-day execution lag generally REDUCES drawdown (52.7–62.7%) with little
  return cost — the effect is not timing-fragile; if anything a slower fill
  is slightly safer.
- Cost (5 vs 10 bps/side) barely matters (~0.3pp CAGR) — expected at ~4
  switches/year. This is the structural reason rotation survives where the
  IBS family died on costs.

Secondary (context, not gates): SPY→SPXL 16.1% CAGR / 55% DD (weaker, echoes
E1b/E2 — the S&P wrapper underperforms the Nasdaq one); SOXL-self 32.8% CAGR
/ 74% DD (semis: high return, uncomfortable drawdown).

## Honest limitations (do not skip)

1. **Regime-flattered.** 3× Nasdaq over 2014–2026 = leverage on the best tech
   decade in history. The 200-MA timing genuinely helped in the 2018/2022
   drawdowns, but the base engine is "leverage × a secular bull." A flat or
   bear forward decade would look materially worse. Discount the forward
   expectation hard — the +2.45%/mo is a backtest ceiling, not a forecast.
2. **Primary cell contaminated.** The B4 screen already saw QQQ→TQQQ/MA200.
   The battery (fragility) and benchmark tests are the new, un-peeked
   evidence that passed; the headline number is not clean OOS.
3. **Live validation is slow.** At ~4 switches/year, a year of live paper
   yields a handful of decisions — this strategy is nearly impossible to
   confirm quickly on paper. Its OOS proof is measured in years, or in
   further pre-registered backtests on other markets/eras.
4. **57.7% drawdown is real and brutal at small capital** — a $500 sleeve to
   ~$210 at the trough. That is the accepted-risk contract.
5. **Not classic swing trading** — holds run weeks to months between
   crossings; this is leverage regime-timing that fits the redefined
   high-return goal.

## Disposition

E4 PASSES its pre-registered backtest gate — the first strategy to do so, and
the fragility evidence is legitimately strong. Per prereg §5 this authorizes
consideration for LIVE PAPER only, which is BLOCKED-ON-EVAN (his explicit go +
an Alpaca paper account). It does NOT authorize live money, and the honest
case for it is "risk-managed leveraged Nasdaq exposure," not "beats buy-and-
hold." STOP at the M3 gate.
