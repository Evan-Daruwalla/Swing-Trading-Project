# Screen results — A3 / B1 / B4 (2026-07-09)

**IN-SAMPLE SCREENS — hypothesis-generating, NOT verdicts.** Run per record
Appendix W (Evan's dated stop-override covers A3; B1/B4 stop-clear). Engine-
v2-style NAV-proportional sizing, 5 bps/side, K=2 where applicable. Train =
2014–2021, holdout = 2022–2026 — but see the contamination note: these
"holdout" columns are now SEEN, so they are not clean OOS for any follow-up
pre-registration.

## A3 — overnight-only IBS harvest (buy close on IBS<0.20, sell next open)

| variant | window | n | %/mo | CAGR | maxDD | Sharpe |
|---|---|---|---|---|---|---|
| broad K=2 | train | 980 | −0.07% | −0.83% | 23.2% | −0.09 |
| broad K=2 | holdout | 604 | −0.19% | −2.22% | 15.3% | −0.34 |
| lev K=2 | train | 1064 | +1.20% | 15.45% | 34.9% | 0.78 |
| **lev K=2** | **holdout** | 630 | **+0.56%** | 6.95% | 33.5% | 0.40 |

**Read:** broad is NET-NEGATIVE — the measured 6.3bps/signal gross overnight
component (M1.8) cannot pay a 10bps round-trip every night. Leveraged is
positive but its holdout (+0.56%/mo) is BELOW the already-failed E2
next-open (+0.64%/mo). **A3 is not the unlock. The overnight component is
real but not separately harvestable at retail cost.** Stop stays effectively
closed on IBS.

## B1 — gap-down reversion at the open (uptrend filter, exec at open)

Best variant: lev gap≤−2%, exit next open — holdout +0.23%/mo, maxDD 46.4%,
Sharpe 0.24. Everything else ≈ zero or negative (broad ≈ +0.01%/mo; same-day
close exits negative throughout).
**Read: hypothesis largely refuted** at these thresholds — no variant is
worth a pre-registration. The by-construction execution advantage did not
come with an edge.

## B4 — vol-regime leverage rotation (3x fund while 1x signal > 200d MA)

| variant | window | switches | %/mo | CAGR | maxDD | Sharpe |
|---|---|---|---|---|---|---|
| **TQQQ/QQQ** | train | 33 | +2.59% | 35.90% | 57.7% | 0.89 |
| **TQQQ/QQQ** | **holdout** | 19 | **+2.15%** | **29.01%** | 48.2% | 0.79 |
| TQQQ/QQQ | full | 51 | +2.45% | 33.75% | 57.7% | 0.86 |
| UPRO/SPY | train | 43 | +1.62% | 21.21% | 51.2% | 0.74 |
| UPRO/SPY | holdout | 33 | +0.61% | 7.58% | 56.1% | 0.39 |
| UPRO/SPY | full | 75 | +1.27% | 16.38% | 55.6% | 0.62 |

**Read: the standout by an order of magnitude.** TQQQ/QQQ held ~2.1–2.6%/mo
across BOTH periods (modest decay 2.59→2.15), Sharpe ~0.8, ~4 switches/year
(costs and the overnight mechanism are irrelevant at that frequency), maxDD
48–58% — inside Evan's accepted-risk class. Matches the literature prior
(Gayed "Leverage for the Long Run") rather than contradicting it. UPRO/SPY
is much weaker OOS — the effect concentrates in the Nasdaq wrapper, echoing
every earlier finding (QQQ/XLK carried E1's edge too).

## Honest caveats before anyone gets excited

1. **Holdout contamination:** these screens LOOKED at 2022–2026. A follow-up
   prereg cannot claim unseen-holdout purity on this data. Confirmation must
   come from (a) a pre-registered robustness battery (MA length 150/175/
   200/225/250, signal on QQQ vs TQQQ itself, execution-lag +1 day, cost
   ×2) where the CLAIM is "edge is not a knife-edge artifact of MA200", and
   (b) live paper as the only true OOS.
2. **Variant selection:** TQQQ/QQQ was the better of two variants seen —
   selection bias is present. Mitigation: TQQQ/QQQ is also the a priori
   choice (the literature construct; QQQ carried the edge in all prior
   experiments), and the prereg will name it primary with UPRO secondary.
3. **This is trend-following leverage timing, not "swing trading" strictly:**
   holds run weeks-to-months between MA crossings. It fits Evan's goal
   (high %/mo, few instruments, risk accepted) but stretches the holding-
   period identity of the project. Flagged, not hidden.
4. **maxDD ~50–58%** will really happen — that is the accepted-risk contract.

## Recommendation

Pre-register **E4 = TQQQ/QQQ 200d-MA leverage rotation** (primary; UPRO
secondary context) with: return-centric gates on the FULL window (since
holdout is contaminated, the gate basis must say so), the robustness battery
above as pass/fail criteria (e.g., all MA∈{150..250} variants positive and
within a band), and live paper as the true confirmatory stage. B1 dropped;
A3 closed (stop resumes in full).
