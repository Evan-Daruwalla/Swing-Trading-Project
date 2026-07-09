# E2 results — leveraged-ETF IBS: VERDICT = FAIL → IBS family SHELVED (2026-07-09)

Per pre-registration `865c09e`. Gate = HOLDOUT (2022-01-01..2026-07-08),
K=2, next-open, 5 bps/side. **No tuning. The prereg's pre-committed stop
(§7) triggers: the IBS family — 1x and leveraged — is SHELVED.**

## Kill criteria (K=2 HOLDOUT, next-open, 5bps/side)

| criterion | threshold | got | result |
|---|---|---|---|
| closed trades | ≥ 100 | 351 | PASS |
| mean net return/trade | > 0 | +31.0 bps | PASS |
| net CAGR | ≥ 15% | **7.98%** | **FAIL** |
| max drawdown | ≤ 60% | **60.6%** | **FAIL** |

### E2 VERDICT: FAIL (2 of 4) — pre-committed stop executes

## Full table

| run | n | exp/trade | CAGR | maxDD | Sharpe | hold |
|---|---|---|---|---|---|---|
| K=2 train 2014–21 (context) | 635 | +100.7 bps | 19.63% | 46.4% | 0.77 | 2.8 |
| **K=2 HOLDOUT (GATE)** | 351 | +31.0 bps | **7.98%** | **60.6%** | 0.39 | 3.1 |
| K=1 HOLDOUT | 190 | +4.6 bps | −2.70% | 104.2% | −0.75 | 3.1 |
| K=3 HOLDOUT | 490 | +36.6 bps | 9.22% | 46.2% | 0.41 | 3.0 |
| K=2 HOLDOUT 0bps | 351 | +41.0 bps | 10.85% | 54.5% | 0.44 | 3.1 |
| K=2 HOLDOUT 10bps/side | 351 | +21.0 bps | 4.82% | 67.2% | 0.35 | 3.1 |
| K=2 HOLDOUT c2c 5bps | 371 | +60.0 bps | 18.15% | 52.4% | 0.60 | 3.1 |

## Honest findings

1. **The edge exists but decayed and the executable version can't clear the
   return bar.** Train CAGR 19.6% → holdout 7.98%. Same OOS decay pattern as
   E1b, amplified by leverage.
2. **The overnight gap is the killer — again.** The c2c (close-fill,
   NON-executable with EOD data) holdout would have PASSED every gate (CAGR
   18.15%, maxDD 52.4%). The executable next-open version earns less than
   half that. Fully consistent with M1.8 (54% of the IBS edge is overnight).
   The gap between "the effect is real" and "you can capture it at next
   open" is the story of this entire project.
3. **Drawdown at the edge of ruin.** 60.6% peak-to-trough on the gate run —
   crash-buying 3x funds through 2022 did exactly what the risk flags said.
4. **ENGINE PROPERTY exposed by K=1 (104% maxDD = NAV went negative):** the
   engine sizes positions at FIXED initial-capital/K dollars, not
   current-NAV/K — after losses it keeps buying full-size, which is implicit
   leverage; at K=1 in 3x funds NAV crossed zero. This was immaterial for
   E1/E1b (diversified 1x, small moves) and does not change the E2 gate
   verdict (K=2 gate run stands under the engine semantics all three
   experiments shared) — but any future engine must size on current NAV.
   Recorded as a known limitation, not silently fixed post-hoc.

## Disposition — the stop executes

Three pre-registered tests of the IBS family have now run and failed:
E1 (full universe: FAIL), E1b (broad_us OOS: near-miss FAIL), E2 (leveraged,
return-centric: FAIL). Per prereg `865c09e` §7, **the IBS family is
SHELVED** — no E2b, no E1c, no cost-shaved or execution-shaved re-runs.

**Information for Evan (not a recommendation to continue):** the c2c rows
suggest a near-close execution model (~3:55pm real-time quote approximation,
the council-flagged alternative) could capture much of the overnight
component. Testing that is still the IBS family → covered by the stop. Only
a NEW dated decision by Evan re-opens it; the executing model will not.

**What remains open:** E3 (different signal family, concentrated stocks,
survivorship caveat) per PRD M2c — design from scratch with its own
pre-registration. No live trading: nothing has passed.
