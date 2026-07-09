# E1 backtest results — VERDICT: FAIL (2026-07-09)

**PRD task M2.10.** E1 (ETF IBS mean reversion) run on the full `swing.db`
window (2014-01-02..2026-07-08) per the frozen pre-registration
`docs/prereg_E1_ibs.md` (`8963e49`). **Parameters were NOT tuned; a FAIL is
recorded as-is.**

## Kill criteria (primary: next-open, 5bps/side = 10bps round-trip, full universe)

| criterion | threshold | got | result |
|---|---|---|---|
| closed trades | ≥ 200 | 3559 | PASS |
| mean net return / trade | > 0 | +4.7 bps | PASS |
| annualized Sharpe | ≥ 0.50 | **0.23** | **FAIL** |
| max drawdown | ≤ 25% | **36.0%** | **FAIL** |

### E1 VERDICT: FAIL (2 of 4 criteria missed)

## Full result table

| run | n | exp/trade | Sharpe | maxDD | CAGR | hold |
|---|---|---|---|---|---|---|
| **PRIMARY next-open 5bps** | 3559 | +4.7 bps | **0.23** | **36.0%** | 2.31% | 3.2 |
| next-open 0bps | 3559 | +14.7 bps | 0.56 | 24.3% | 5.89% | 3.2 |
| next-open 10bps/side | 3559 | −5.3 bps | −0.04 | 68.4% | −3.78% | 3.2 |
| c2c 5bps (reference) | 3761 | +8.5 bps | 0.37 | 22.5% | 4.00% | 3.0 |
| c2c 0bps (reference) | 3761 | +18.5 bps | 0.74 | 17.3% | 7.21% | 3.0 |

### Per-group (next-open, 5bps)

| group | n | exp/trade | Sharpe | maxDD | CAGR |
|---|---|---|---|---|---|
| broad_us | 1478 | +23.1 bps | 0.60 | 14.2% | 4.22% |
| spdr_sector | 2849 | +8.0 bps | 0.31 | 31.7% | 2.97% |
| country_intl | 2996 | −2.2 bps | 0.05 | 57.5% | −1.13% |

### Split-sample (next-open, 5bps, full universe)

| window | n | exp/trade | Sharpe | maxDD | CAGR |
|---|---|---|---|---|---|
| 2014..2021 | 2313 | +8.0 bps | 0.32 | 36.0% | 3.97% |
| 2022..2026 | 1241 | −1.7 bps | 0.01 | 22.5% | −1.14% |

## Why it failed (diagnostic — NOT a basis for tuning)

1. **Cost-fragile.** Gross (0bps) the edge is real: Sharpe 0.56, +14.7 bps/
   trade. At the realistic 10bps round-trip it decays to Sharpe 0.23; at
   20bps round-trip it is outright negative. The M1.8 ablation's warning
   (+7.5bps/signal thin vs 10bps cost) was correct — the multi-day hold
   raised gross expectancy to +14.7bps but not enough to clear cost + the
   Sharpe/DD bars.
2. **Country ETFs drag it down.** country_intl is net negative (−2.2 bps,
   Sharpe 0.05, 57.5% maxDD) — the executable IBS edge there is an overnight/
   stale-NAV artifact (M0.3, M1.8), forfeited by next-open fills.
3. **Recent-era decay.** 2014–2021 Sharpe 0.32 → 2022–2026 Sharpe 0.01,
   negative expectancy. A public, well-known signal decaying over time — the
   research brief's crowding caveat, realized.
4. **Drawdown.** 36% peak-to-trough far exceeds the 25% ceiling, driven by
   the sector/country legs.

## What this is NOT: a broad_us pass

broad_us alone clears all four criteria (n=1478, Sharpe 0.60, maxDD 14.2%,
+23.1 bps). **This does not rescue E1.** The pre-registered experiment was
the full 29-ETF universe, and it FAILED. Selecting broad_us after seeing the
results is post-hoc universe-narrowing, explicitly forbidden by pre-reg §10.
"broad_us IBS mean reversion" is a NEW hypothesis the data suggests — it must
be tested under its OWN dated pre-registration ("E1b"), ideally with a real
out-of-sample holdout (its 2022–2026 behavior is unknown and the full-
universe recent period already shows decay). It is a lead, not a result.

## Disposition

Per pre-reg + PRD M2.13, E1 FAIL → STOP, do not tune, await Evan's direction.
The engine is pinned by the frozen-regression test (M2.11) so this result is
tamper-evident. Candidate next directions (Evan's call): (a) pre-register
E1b on broad_us (+ maybe sectors) with a holdout; (b) pre-register a
lower-cost / different-signal variant; (c) shelve E1 and move to a deferred
idea. No live trading — E1 did not pass the M2→M3 gate.
