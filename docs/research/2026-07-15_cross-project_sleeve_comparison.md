# Cross-Project Comparison — Swing (3 sleeves) vs Trading (momentum, 27 sleeves)

**Swing Trading project · 2026-07-15 (CST) · Evan Daruwalla**

How the three Alpaca paper sleeves this project just launched (M3, 2026-07-15) compare to
the longer-term momentum sleeves in the separate `D:\ClaudeCode\Trading` project. Trading
was inspected **READ-ONLY** (project hard rule); facts below are from its `momentum_v2.py`
(locked 2026-05-26) and `HANDOFF.md` (2026-07-11), read 2026-07-15. Not an experiment — no
verdict, no tally change.

## TL;DR

The two paper programs sit at **opposite ends of one spectrum** and are complements, not
competitors. Trading harvests a **validated, diversified momentum premium** (top-50, monthly,
~5,200-name universe, $100K) and exists to build a real forward track record. Swing runs
**three deliberately-concentrated, retail-scale ($1K), EOD hypotheses** — two of them beta
overlays, one a *reversal* strategy that is the literal opposite of Trading's momentum — none
of them a clean edge. **Trading is the control that proves Swing's 0-for-35 is about retail
constraints (K=1–4, $1K, liquidity floor), not about factors failing.** Their signals are
near-orthogonal (momentum vs reversal, broad vs QQQ, monthly vs daily), so running both is
genuinely diversifying.

## The facts

| | **Swing — 3 sleeves (this project)** | **Trading — momentum, 27 sleeves** |
|---|---|---|
| Core signal | **e6_1x**: QQQ 1× iff QQQ>200-DMA · **e18_vixts**: QQQ 1× iff VIX/VIX3M<1 · **m10_1_nagel**: VIX>20 → bottom-K=4 FF3-residual **reversal** (weekly) / else QQQ 200-DMA trend | 12-1 cross-sectional **momentum** (`momentum_v2`, factor `momentum_12_1`, equal-weight) |
| Direction | trend-time / **mean-revert** (m10 in stress) | **momentum** (opposite of reversal) |
| Universe | QQQ + 39 hand-picked survivor mega-caps | ~5,200 US stocks (min price $5, min history 252d) |
| Concentration | **K = 1** (e6/e18) to **4** (m10) | **top 50**, 2% NAV each |
| Horizon / cadence | days–weeks; **daily** EOD decision, next-open | ~1-month holds; **monthly** rebalance (validated vs W/Q) |
| Capital | **$1,000** / sleeve (retail floor binds) | **$100,000** / sleeve |
| Cost model | 1 bp/side QQQ (5 bp m10 stocks) | 5 bp half-spread (single stocks) |
| Validation | **0 clean edges** / 35 attempts — all in-sample or survivor-flattered | **validated & robust**: IS 2015-23 +21.0%/yr, OOS 2024-26 +26.5%/yr, OOS Sharpe 0.87 |
| Goal | high-% concentrated return, losses accepted; falsification program | build rigor + a track record before Evan turns 18 |
| Status | launched 2026-07-15 (3 isolated paper accounts) | Phase 2d, months live, full ops/backup/coverage infra |

## What actually matters

**1. Trading is the control for Swing's negative.** Swing's terminal finding
(Hou-Xue-Zhang) is that *concentration destroys diversified factor edges* — a premium is a
decile spread across many names, not K=1–4. Trading's `momentum_v2` does exactly the "right"
thing (top-50 equal-weight across breadth) and **validated** (IS +21%, OOS +26.5%, robust
both windows). Put together, the two projects say something neither says alone: **the problem
is not that factors fail — it is that Swing's retail constraints (K=1–4, $1K, mandatory
liquidity floor) forbid the breadth the premium requires.** Trading is the existence proof
that the machinery works when it is allowed to diversify.

**2. The signals are near-opposite — a feature, not a bug.** `m10_1_nagel` buys the
*bottom-K residual reversal* (recent losers snapping back, weekly horizon); Trading buys the
*top-50 by 12-month momentum* (recent winners continuing). Opposite sign, opposite horizon.
They exploit different, opposite-signed anomalies, so they are complementary rather than
redundant — and in a sharp bear-bottom reversal (a classic "momentum crash"), they behave
very differently.

**3. Overlay vs return-engine.** Trading's momentum is a **return engine** — alpha from
security selection. `e6_1x` and `e18_vixts` are **beta-timing overlays**: they decide *when*
to hold QQQ, not *what* to hold, and generate no selection alpha. Strictly, e6/e18 are the
kind of risk overlay you would bolt *onto* a return engine — including Trading's momentum,
which they would de-risk during a momentum unwind. Of Swing's three sleeves, only `m10` is a
genuine cross-sectional selection strategy (and it is momentum's mirror image).

**4. Validation asymmetry is stark.** Trading's sleeves harvest a *known, robust* premium
with a real forward track record. Swing's three are *hypotheses the program itself
distrusts*: `m10_1_nagel` is IN-SAMPLE-COMPOSED (built after seeing 31 results),
`e18_vixts` is a WEAK PASS-RA (largely "dodged 2008"), `e6_1x` is market-dependent
(works 3/5 non-US regimes). Side by side, the honest framing is: **Swing is a research
instrument; Trading is the track record.**

## Skeptical notes (both directions)

- **Don't over-rate Trading.** `momentum_v2`'s *in-sample* mean-yearly Sharpe is only **0.23**
  — the +21% CAGR carries large volatility and real **momentum-crash tail risk** (2009-style
  post-bear reversals savage momentum). Its headline **0.87 OOS Sharpe is a 2024-26 bull**
  with no momentum crash in the window — the same one-window flattery Swing kills experiments
  for. Ironically, Swing's e6/e18 overlays are precisely what would protect momentum through
  that crash (they'd be in cash when it unwinds).
- **Don't over-rate Swing.** All three sleeves are forward-paper hypotheses on a survivor /
  in-sample basis; the point of M3 is to see whether *any* of them survives contact with live
  paper, not to claim they will.

## Synthesis — a natural experiment across the retail/institutional divide

Because the two run on **separate broker accounts, in the same era, with near-orthogonal
signals**, together they form a clean natural experiment across three axes at once:
**concentration** (K=1–4 vs 50), **horizon** (daily-EOD swing vs monthly), and **capital
scale** ($1K retail-floored vs $100K). The most likely forward outcome, consistent with both
projects' priors: **Trading's diversified momentum compounds a real track record while
Swing's concentrated sleeves confirm — forward, out-of-sample — that the retail-EOD, K=1–4,
liquidity-floored corner does not contain a robust edge.** If instead a Swing sleeve holds up
forward, that is the genuinely new information the whole falsification program was built to
detect. Either way, the pair is more informative than either alone.

## Sources (read-only)

- `D:\ClaudeCode\Trading\trading_bot\strategies\momentum_v2.py` (SPEC + locked baseline
  metrics, locked 2026-05-26); `D:\ClaudeCode\Trading\HANDOFF.md` (2026-07-11, "27 sleeves
  live"); factor files `momentum.py`, `mom_roa_*`, `mom_quality_screen`, `mom_then_accruals`,
  `sector_momentum`, `residual_momentum` (the sleeve cohort). Read 2026-07-15, no writes.
- Swing sleeve specs: `swing_bot/paper_sleeves.py`, `docs/research/2026-07-15_M3_forward_paper_setup.md`,
  preregs E6 `0526ea2` / E18 / `prereg_m10_1_nagel_switch.md`.
