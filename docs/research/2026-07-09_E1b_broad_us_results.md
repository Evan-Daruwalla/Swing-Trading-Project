# E1b results — broad_us out-of-sample: VERDICT = FAIL (near-miss) (2026-07-09)

Per pre-registration `0126ce3`. Gate = broad_us HOLDOUT (2022-01-01 ..
2026-07-08), next-open, 5bps/side. **No tuning.**

## Kill criteria (broad_us HOLDOUT, next-open, 5bps)

| criterion | threshold | got | result |
|---|---|---|---|
| closed trades | ≥ 100 | 560 | PASS |
| mean net return/trade | > 0 | +17.77 bps | PASS |
| annualized Sharpe | ≥ 0.50 | **0.4961** | **FAIL** |
| max drawdown | ≤ 25% | 9.77% | PASS |

### E1b VERDICT: FAIL — by 0.0039 of Sharpe (0.4961 vs 0.50)

Three of four criteria pass, two of them decisively (drawdown 9.8% is less
than half the ceiling; expectancy +17.8 bps is strong). The gate is the
Sharpe bar, and 0.4961 < 0.50, so **E1b fails as pre-registered.** The value
was NOT rounded up — the threshold was strict and committed before the run.

## Full holdout table

| run | n | exp/trade | Sharpe | maxDD | CAGR |
|---|---|---|---|---|---|
| **broad_us HOLDOUT next-open 5bps (GATE)** | 560 | +17.77 bps | **0.4961** | 9.8% | 3.96% |
| broad_us HOLDOUT 0bps | 560 | +27.8 bps | 0.76 | 8.9% | 6.07% |
| broad_us HOLDOUT 10bps/side | 560 | +7.8 bps | 0.23 | 10.7% | 1.69% |
| broad_us HOLDOUT c2c 5bps | 572 | +20.1 bps | 0.60 | 9.3% | 4.65% |
| broad_us+sectors HOLDOUT 5bps (secondary) | 1097 | −3.0 bps | −0.05 | 24.9% | −1.78% |

Train/context window (2014–2021, broad_us): n=914, +26.4 bps, Sharpe 0.66,
maxDD 14.2%.

## Honest interpretation

1. **My pre-results prior was WRONG (in broad_us's favor).** I expected decay
   to ~0 (the full universe was Sharpe 0.01 in this window). Instead broad_us
   held Sharpe 0.66 (train) → 0.496 (holdout) — the edge substantially
   PERSISTED out-of-sample in the 4 broad US index ETFs, even through the
   2022 bear market (holdout maxDD only 9.8%). This is a real, if modest,
   decayed-but-alive effect — categorically different from E1's decisive fail.
2. **It still fails the bar.** 0.496 is below 0.50 out-of-sample at the
   pre-registered conservative cost. Not a green light.
3. **Cost is the swing factor.** 0bps → Sharpe 0.76; 5bps/side → 0.496;
   10bps/side → 0.23. The verdict hinges entirely on the cost assumption.
   The pre-reg's 5bps/side is CONSERVATIVE for SPY/QQQ/DIA/IWM — the four
   deepest US ETFs, typical spreads ~1 bp. (This is an observation, NOT a
   licence to re-run at a lower cost to force a pass — see below.)
4. **Sectors confirmed dead weight.** The secondary broad_us+sectors is
   net-negative on the holdout (−3.0 bps, Sharpe −0.05). Pre-declaring it as
   non-gate was correct; it is not the vehicle.

## Disposition and the multiplicity caveat

E1b FAILED. Two pre-registered tests have now run (E1 fail, E1b near-miss).
A THIRD pre-registration that lowers the cost assumption would be defensible
ONLY on independent liquidity grounds (real SPY/QQQ spreads ~1 bp, so 5bps/
side overstates cost) — NOT because E1b happened to just miss. To avoid
fishing-by-multiplicity, any such E1c must (a) justify its cost number from
measured/quoted spreads set before the run, and (b) carry a PRE-COMMITTED
STOP: if E1c fails, ETF IBS mean reversion is shelved. That is the honest way
to take one final swing; endless re-pre-registration is p-hacking with extra
steps.

Alternative, equally defensible: accept that broad_us IBS is a real but
sub-0.50-Sharpe, cost-sensitive effect that does not clear the pre-registered
tradeability bar, write it up as the conclusion, and pivot to a different
strategy family. Evan's call.

No live trading — E1b did not pass the gate.
