# Research brief — Full in-depth survey of every swing-trading method with claimed merit

**Swing Trading project · 2026-07-12 (CST) · Evan Daruwalla**

**Question this answers:** across the *entire* documented universe of swing-trading
methods — mean-reversion, trend/momentum, chart-pattern TA, event/catalyst,
seasonality/overnight, sentiment/flow/alt-data, volatility/options, and
factor/ML construction — what is each method's real mechanism, evidence
quality, data requirement, and testability under THIS project's hard
constraints (EOD-only, next-open fills, $100–1,000 capital, K=1–3 concentrated,
mandatory liquidity floor, 5 bps/side)? And, cross-referenced against the
project's **20 pre-registered experiments (0 high-return passes / 1 weak
risk-adjusted pass)**, which methods are already falsified here versus
**genuinely still open**?

**Decision it feeds:** whether any remaining idea justifies a new
pre-registration, or whether the search space is exhausted.

**Audience:** the operator of this bot (Evan) and any future model executing
the PRD. It is also a portfolio artifact — the *reasoning trail* is a
deliverable, so kills and out-of-scope verdicts are stated as explicitly as
the survivors.

---

## TL;DR (verdict first)

**The high-return AND robust AND retail-EOD cell is empty, and this survey —
built from ~90 methods across 8 families, primary-source-graded — is a
stronger, better-sourced confirmation of the program's own 0-for-20 result
than the 2026-07-10 catalog was.** Three findings dominate:

1. **Most "untested" ideas the literature points to are already killed *here*.**
   Reconciling the eight family surveys against the project's own experiment
   ledger removes the top candidates outright: diversified sector momentum
   (**E14 FAIL**), turn-of-the-month (**E13 FAIL**), earnings-announcement
   premium (**E15 FAIL**), raw cross-sectional weekly reversal (**E16 FAIL**,
   and it hit 16.76% gate CAGR only on a **65.9% drawdown**), dividend capture
   (**E20 FAIL**). The project has now tested a representative of nearly every
   family.

2. **The genuine edges are structurally the wrong shape for this mandate.**
   Nearly every method with peer-reviewed merit is a *diversified long-short
   decile premium* whose documented profit is disproportionately located in
   **microcap / illiquid / distressed / high-turnover** names. Hou-Xue-Zhang
   (2020): 65–82% of 452 anomalies fail once you value-weight and drop
   microcaps. McLean-Pontiff (2016): a further ~26% out-of-sample / ~58%
   post-publication haircut, largest for low-liquidity anomalies. Avramov-
   Cheng-Metzker (2023): even ML alpha "evaporates" once microcaps/distress
   and realistic costs are removed. Collapsing any of these to **K=1–3 liquid
   names** discards the diversification that *is* the edge and keeps only the
   shrunken, decayed, cost-eroded mean plus the idiosyncratic noise.

3. **After reconciliation, only a short list is genuinely open — and all of it
   carries a strong prior of failing the 15% bar.** The honest survivors are
   refinements of already-killed families (short-term *residual* reversal after
   raw-reversal E16), overlays not engines (vol-targeting sizing, even-week
   FOMC), a strong-FAIL-prior kill-shot (one consolidated volatility-breakout
   spec), a free-data catalyst (dividend-*initiation* drift), and a degraded-
   proxy sentiment signal (free Reg SHO daily short-volume). None is a
   plausible standalone high-return engine.

**Working hypothesis H1** ("a swing method with real merit exists that this
project simply hasn't tried yet") is **rejected in its strong form**: the
untried methods are either refinements of local kills, overlays, or carry
published strong-FAIL priors. **Rival/null H0** ("the residual search space is
exhausted of high-return, retail-EOD, robust engines; what remains are
risk-adjusted overlays and honest kill-shots") **survives.** This is consistent
with the program reaching its autonomous wall.

---

## Method (stage-4 design + limitations)

- **Design:** 8 parallel desk-research agents, one per method family, each
  instructed to grade every method by evidence tier (**[PEER-REVIEWED]** /
  **[WORKING-PAPER]** / **[VENDOR-BLOG low-confidence]** / **[FOLKLORE]**),
  report effect size + net-of-cost + decay, state data requirements, and issue
  a testability verdict against the project constraints. Sources favor primary
  literature (SSRN, NBER, journals); every source dated.
- **Reconciliation layer (added at compile):** each family's "genuinely
  untested" claims were cross-checked against the project's **E1–E20** ledger,
  because the agents did not all know which experiments had already run. This
  is where several top-line candidates were reclassified from "open" to
  "already killed here."
- **Limitations:** (1) This is *desk research* — no new backtests were run in
  producing it (the running E19 ingestion is separate); every "testability"
  verdict is a scoping judgment, not a result. (2) Effect sizes are as
  reported by the cited studies; where a figure could not be independently
  verified it is labeled unverified. (3) Vendor/blog backtests are catalogued
  for completeness but discounted. (4) Coverage is broad but not literally
  exhaustive — novel niche variants surely exist; the families are the
  standard partition of the documented space.

---

## The reconciliation that matters — families vs the project's own ledger

This is the load-bearing table. It maps each family to the experiment(s) that
already probed it here and the resulting D1 verdict, so "merit in the
literature" is never confused with "open for this project."

| Family | Literature's best idea | Tested here? | Verdict here |
|---|---|---|---|
| Mean-reversion | IBS / oscillator reversion | **E1/E1b/E2, E8, E9, E11, E12** | FAIL (Sharpe 0.23; 54% of edge in un-catchable overnight gap) |
| Mean-reversion | Raw cross-sectional weekly reversal | **E16** | FAIL (16.76% gate CAGR **but 65.9% DD**) |
| Trend/momentum | Concentrated single-name momentum | **E3** | FAIL (6.3% vs 15%) |
| Trend/momentum | Diversified sector momentum (11 SPDRs) | **E14** | FAIL (2.4% gate, Sharpe 0.22) |
| Trend-timing | 200-DMA leverage / MA rotation | **E4/E5/E7, E6** | FAIL (93% DD levered; 1× ≈ index overlay) |
| Event/catalyst | PEAD (post-earnings) | **E10** | FAIL (5.9%; decayed post-2010) |
| Event/catalyst | Earnings-announcement premium (pre) | **E15** | FAIL (6.4%) |
| Event/catalyst | Opportunistic insider buying | **E19 (LIVE, ingesting)** | pending; strong-FAIL prior |
| Seasonality | Turn-of-the-month | **E13** | FAIL (1.4%/yr) |
| Sentiment/flow | VIX term-structure regime gate | **E18** | **weak PASS-RA** (2006–13 dodges 2008; forward-paper only) |
| Sentiment/flow | Short interest / days-to-cover | **E17 (blocked)** | BLOCKED (FINRA free SI OTC-only pre-2021) |
| Vol/income | Dividend capture | **E20** | FAIL (0.6%/yr) |
| Factor/ML | Diversified factor / ML deciles | not run | structurally void at K=1–3 (see §Findings-H) |
| Chart-pattern TA | Breakout / MA rules | not run directly | strong-FAIL prior (STW 1999; Bajgrowicz-Scaillet 2012) |

Reading: representatives of every family except chart-pattern TA and
factor/ML have been directly tested, and every one failed the high-return bar.
The two untested families are precisely the two with the *worst* priors — TA
rules die under data-snooping correction, and factor/ML edges die when
concentrated to K=1–3 liquid names.

---

## Findings by family

Tiering tags below: **[PR]** peer-reviewed · **[WP]** working paper · **[V]**
vendor/blog low-confidence · **[F]** folklore/no rigorous source. Testability:
IN-SCOPE-UNTESTED · ADJACENT-TO-A-KILL · OUT-OF-SCOPE · DECAYED · DATA-GATED ·
OVERLAY-not-engine.

### A. Mean-reversion & short-term reversal

Splits into single-name daily oscillators (IBS, RSI2, Bollinger/%B, Williams
%R, oversold-bounce, gap-fade) — one method in six costumes, all close→next-open
and all inside the project's overnight-gap kill — and cross-sectional/spread
reversal (weekly, residual, pairs). The project already killed the oscillator
cluster (E1/E2/E8/E9/E11/E12) and raw weekly reversal (E16).

| Method | Tier | Testability here |
|---|---|---|
| IBS / RSI2 / Bollinger / %R / oversold-bounce | V (on PR reversal anomaly) | ADJACENT-TO-A-KILL (E1/E2; 54% of edge in overnight gap) |
| Gap-down fade / gap-fill | V + adverse academic | ADJACENT / partly OUT-OF-SCOPE(intraday) |
| Opening-range reversal, ETF-vs-NAV | V / PR | OUT-OF-SCOPE(intraday) |
| Raw cross-sectional weekly reversal (de Groot 2012) | PR (30–50 bps/wk net, large-cap) | **KILLED HERE (E16)** as raw; long-short/scale mismatch |
| **Short-term RESIDUAL reversal (Blitz et al. 2013)** | **PR (~2× raw reversal Sharpe; net-positive in large-caps)** | **IN-SCOPE-UNTESTED** (distinct from E16's raw version) |
| Pairs / cointegration-OU stat-arb (Gatev 2006) | PR but **DECAYED** (Do-Faff: ~nil net post-2002) | IN-SCOPE-UNTESTED but decayed; needs shorting |

Synthesis: the only genuinely-open candidate is **residual reversal** — it
strips the factor betas that drove E16's 65.9% drawdown and claims lower
variance, so it is the logical next refinement after E16. Honest caveat: Nagel
(2012) shows reversal returns *are* close-anchored liquidity provision, so
next-open execution bleeds the same gap that killed the oscillators.

### B. Trend / momentum (time-series & cross-sectional)

**Scope hazard:** the swing horizon (days–weeks) sits inside the short-term
*reversal* window, not the momentum window (which is 3–12mo formation, 1–6mo
hold). Gutierrez-Kelley (2008) and Novy-Marx (2012) show a strict days–weeks
hold captures the *reversal* leg, wrong sign. The project killed concentrated
momentum (E3) and diversified sector momentum (E14).

| Method | Tier | Testability here |
|---|---|---|
| TSMOM 12-mo (Moskowitz-Ooi-Pedersen) | PR, **contested** (Huang 2020) | OUT-OF-SCOPE(horizon) + ADJACENT-TO-A-KILL (E4/E6) |
| Diversified J-T decile / sector momentum | PR, decayed | **KILLED HERE (E3, E14)** |
| 52-week-high anchor (George-Hwang 2004) | PR (~0.45%/mo, no reversal) | IN-SCOPE-UNTESTED as a *signal* variant, 1–6mo hold |
| Residual momentum (Blitz-Huij-Martens 2011) | PR (~2× risk-adj) | IN-SCOPE-UNTESTED; addresses crash tail; monthly formation |
| Frog-in-the-pan continuity (Da-Gurun-Warachka 2014) | PR | IN-SCOPE-UNTESTED **overlay** (not standalone) |
| Donchian / 20-day-high / MA-crossover / MACD | F / V; PR-negative (STW) | ADJACENT-TO-A-KILL / FOLKLORE |
| CANSLIM / Minervini / Darvas breakout | V / F (marketing, contest survivorship) | LIKELY-DECAYED / hard-to-systematize |
| GEM / dual momentum (Antonacci) | V | OUT-OF-SCOPE(horizon) + ADJACENT-TO-A-KILL |

Synthesis: sector momentum was the literature's "only real opening" — and it
is **already E14 FAIL**. What remains untested are *refinements* of a family
that is 0-for-2 here (52-wk-high anchor, residual momentum, frog-in-the-pan as
a continuity filter), all documented at 1–12mo holds. Marginal.

### C. Chart-pattern & price-action technical analysis

The largest and lowest-merit family. Governing anchors: Lo-Mamaysky-Wang
(2000) found modest *information* content (≠ profit); Park-Irwin (2007) survey
found early profits vanish in later rigorous work; Sullivan-Timmermann-White
(1999) + Bajgrowicz-Scaillet (2012) overturned the classic Brock (1992)
breakout/MA result under data-snooping + costs; Marshall et al. (2006/2008)
and Horton (2009) killed candlesticks on liquid equities.

| Method | Tier | Testability here |
|---|---|---|
| Flags, pennants, cup-and-handle, trendlines | F | HARD-TO-CODIFY (discretionary) |
| Fibonacci retracement / Elliott Wave | PR-negative / F (unfalsifiable) | OUT-OF-SCOPE / null |
| Candlesticks (engulfing, hammer, doji…) | **PR — decisively negative** (Marshall 2006/08) | codifiable but a replicated FAIL on liquid equities |
| Head-and-shoulders, double-top/bottom | PR (info content, but "dominated by simpler filters") | HARD-TO-CODIFY; standalone edge absent |
| Round-number support/resistance (Osler 2003) | PR (FX order-flow mechanism) | IN-SCOPE-UNTESTED but you can't observe the driver |
| **Volatility/channel breakout (Donchian≈Bollinger-squeeze≈ATR≈Keltner)** | PR as *futures* trend factor (MOP 2012); PR-negative on stocks | **IN-SCOPE-UNTESTED as ONE consolidated kill-shot; strong-FAIL prior** |
| VWAP / anchored-VWAP | PR as an *execution benchmark*, not a signal | OUT-OF-SCOPE(no predictive claim) |

Synthesis: the one rigorously-supported, cleanly EOD-codifiable idea the
project hasn't isolated is **volatility breakout as trend-following** — but its
merit lives in *futures*, and on single equities under 5 bps + next-open the
STW/Bajgrowicz/Marshall trilogy predicts it dies. Correct move if run at all:
**one** pre-registered volatility-breakout specification (all four variants
collapsed to avoid multiple-testing), entered as an honest kill-shot.

### D. Event-driven / catalyst

| Method | Tier | Testability here |
|---|---|---|
| PEAD | PR, **decayed** post-2010 | **KILLED HERE (E10)** |
| Earnings-announcement premium (pre) | PR (~7%/yr, turnover-hostile) | **KILLED HERE (E15)** |
| Opportunistic insider buying (CMP 2012) | PR (~82 bps/mo, but pre-2007/small-cap/pre-SOX-speed) | **LIVE (E19)**; free EDGAR data; strong-FAIL prior |
| **Dividend-initiation drift (Michaely-Thaler-Womack 1995)** | **PR (+7.5%/12mo initiations)** | **IN-SCOPE-UNTESTED (long-only, free data); distinct from E20 capture** |
| 13D activist filings (Brav-Jiang 2008) | PR (~7% at filing, no reversal) | IN-SCOPE-UNTESTED but timing-fragile (next-open forfeits the pop) |
| Buybacks / spinoffs / SEO / lockup / stock-split | PR but multi-year or short-side | OUT-OF-SCOPE(horizon / shorting) |
| Analyst revisions / guidance / merger-arb | PR | DATA-GATED (I/B/E/S, deal data = paid) |
| Index adds / Russell reconstitution | PR — **decayed to <1%** (Greenwood-Sammon 2025) | DECAYED |
| FDA / biotech binary | V / F | OUT-OF-SCOPE(no sign-predictable edge; gap risk) |

Synthesis: after E10 and E15, the only free-data + EOD + long-only + untested
catalyst is **dividend-initiation drift** (distinct from E20's dividend
*capture*), plus the live E19 insider work. Everything else is decayed,
data-gated, short-side, or multi-year.

### E. Seasonality / calendar & overnight / microstructure

Governed by Sullivan-Timmermann-White (2001): calendar effects lose
significance under a full-universe bootstrap. Turn-of-month is **E13 FAIL**.

| Method | Tier | Testability here |
|---|---|---|
| Turn-of-the-month (McConnell-Xu 2008) | PR (~15 bps/day, 4-day window) | **KILLED HERE (E13)** |
| **Even-week FOMC cycle (Cieslak-Morse-Vissing-Jorgensen 2019)** | **PR (~whole equity premium in even weeks)** | **IN-SCOPE-UNTESTED overlay** (pure date math, live mechanism) |
| Pre-FOMC drift (Lucca-Moench 2015) | PR then **decayed** (Kurov 2021, gone post-2016) | LIKELY-DECAYED |
| Sell-in-May, Santa, day-of-week, pre-holiday, January | PR but small / **decayed** / illiquid | OUT-OF-SCOPE(horizon) / OVERLAY / DECAYED |
| Overnight return anomaly (tug-of-war) | PR — **cost-fatal** (Berkman: open-buy cost > half-spread) | ADJACENT-TO-A-KILL (the project's own 54%-gap finding) |
| Triple-witching / intraday seasonality | PR but intraday | OUT-OF-SCOPE(intraday) |

Synthesis: the only calendar effect that is robust + EOD-codifiable + live-
mechanism + not-yet-killed-here is the **even-week FOMC cycle** — as an
overlay, never an engine. TOM is already E13 FAIL; the overnight family is
cost-fatal.

### F. Sentiment / flow / alternative data

Best free+EOD+point-in-time signals are already claimed: VIX-TS is **E18**
(the weak pass) and opportunistic insider is **E19**. Short interest is
**E17-blocked** (FINRA free SI OTC-only pre-2021).

| Method | Tier | Testability here |
|---|---|---|
| VIX term structure | WP/V | **PARTIALLY TESTED (E18 weak pass; forward-paper)** |
| Short interest / days-to-cover (Hong-Li-Ni; Boehmer 2008) | PR/WP (~1.2%/mo; 15.6% ann) | **DATA-BLOCKED (E17)** for clean history; thin forward-only from 2021 |
| **Free Reg SHO daily short-volume drift** | **PR lineage (Boehmer 2008), free 2009+ proxy** | **IN-SCOPE-UNTESTED** (single-name, EOD, PIT; overlay-grade) |
| Google-Trends / FEARS (Da-Engelberg-Gao 2015) | PR (short-horizon reversal) | IN-SCOPE-UNTESTED w/ real point-in-time renormalization hazard |
| Put/call ratio (aggregate, free) | PR-strong only for *signed* (paid) | OVERLAY-not-engine (free version weak) |
| Baker-Wurgler, fund flows | PR but monthly + illiquid-concentrated | OUT-OF-SCOPE(horizon) |
| IV skew, single-name signed option volume, news/social | PR/WP | PAID-DATA-GATED / look-ahead-prone |
| AAII, NAAIM, COT, breadth, margin debt | V / F / negative | OVERLAY-not-engine, weak |

Synthesis: the genuinely-untested free candidate is the **Reg SHO daily
short-volume** proxy (a degraded stand-in for the paid Boehmer order-flow
signal) — framed honestly as overlay-grade, not a high-return engine. Every
robust cross-sectional sentiment anomaly concentrates alpha in illiquid names
the floor excludes.

### G. Volatility & options-structured

**~80% is OUT-OF-SCOPE:** the project has no options chain, no IV surface, no
VIX-futures feed, and at $100–1,000 the 100-share multiplier makes most
structures infeasible. The whole family is one economic bet — the variance
risk premium (Carr-Wu 2009; Bakshi-Kapadia 2003) — and Israelov-Nielsen (2015)
show the "income" framing (covered calls) is mostly repackaged equity beta,
risk transfer not alpha.

| Method | Tier | Testability here |
|---|---|---|
| Covered calls, CSPs, straddles, calendars, dispersion, collars | PR | OUT-OF-SCOPE(no options data) + retail-infeasible |
| **Vol-targeting sizing overlay (Moreira-Muir 2017)** | **PR, contested OOS (Cederburg 2020)** | **IN-SCOPE-UNTESTED overlay (zero new data)** |
| **SVXY short-vol carry gated by free VIX/VIX3M** | PR blowup risk (Volmageddon 2021) | **PROXY-TESTABLE-VIA-ETP; fat tail; overlaps E18** |
| Leveraged/inverse-ETF decay harvesting | PR (Cheng-Madhavan 2009) | PROXY-TESTABLE but borrow-cost is the whole ballgame |

Synthesis: three EOD-equity-proxy paths are testable — the **Moreira-Muir
inverse-vol sizing overlay** (cleanest; zero new data; but Cederburg predicts
OOS FAIL), the **SVXY carry** (only real VRP harvest at retail scale, but a
Feb-2018-style −90% tail demands a hard kill-switch), and LETF-decay harvesting
(contingent on honest borrow modeling). None is an alpha source; all are
compensated-risk or risk-control.

### H. Multi-factor / systematic construction / ML

**This family structurally cannot help this project.** The merit-bearing edges
(value+momentum "everywhere", QMJ quality, Gu-Kelly-Xiu ML) are diversified
long-short decile premia. Their profit lives in microcap/illiquid/high-turnover
names (Avramov-Cheng-Metzker 2023); 65–82% of anomalies fail once value-weighted
and microcaps dropped (Hou-Xue-Zhang 2020); McLean-Pontiff strips a further
26–58%. **Collapsing any of these to K=1–3 liquid names re-injects the
idiosyncratic variance the deciles were built to cancel.**

| Method | Tier | Testability here |
|---|---|---|
| Value+momentum+quality blend, QMJ, factor momentum | PR (survive OOS as *deciles*) | TENSION-WITH-K=1–3 + NEEDS-PIT-FUNDAMENTALS |
| Betting-against-beta | PR but needs leverage; contested (2022) | OUT-OF-SCOPE(leverage) |
| ML classifiers (Gu-Kelly-Xiu 2020) | PR (Sharpe ~1.35 deciles) but illiquid-driven | OVERFIT-RISK-HIGH + TENSION-WITH-K=1–3 |
| Factor timing / ensembles / technical-ML features | WP / V / F | OVERFIT-RISK-HIGH |
| **Vol-targeting, fractional (≤½) Kelly sizing** | PR (risk control, not alpha) | IN-SCOPE-UNTESTED as **risk overlays** |
| Purged/combinatorial CV; Deflated-Sharpe / PBO / factor-zoo t>3 | PR/WP methodology | **IN-SCOPE — adopt as mandatory scoring/validation discipline** |

Synthesis: worth pre-registering only as (1) a static value+momentum(+quality)
composite *rank* used as a candidate-generation **screen** feeding a small
liquid book (pre-registered to FAIL net-of-cost high-return), and (2) cheap
low-degrees-of-freedom **risk overlays** (fractional Kelly, inverse-vol). All
ML/technical/timing = OVERFIT-RISK-HIGH; with 20 experiments already run, the
multiple-testing correction (Harvey-Liu-Zhu demand t>3.0) alone likely
disqualifies any marginal future "pass."

---

## Ranked shortlist — genuinely still open after reconciliation

Everything below is **long-only-capable, EOD-codifiable, free-data, and not yet
falsified in this project.** All carry a strong prior of missing the 15%
high-return bar (0-for-20 base rate + the §H structural reason). Ranked by
merit × in-scope-ness × novelty-here.

| # | Idea | Family | Evidence | Honest tradeoff / prior |
|---|---|---|---|---|
| 1 | **Short-term residual reversal** (strip FF betas, then reversal) | A | Blitz et al. 2013 [PR]: ~2× raw-reversal Sharpe, net-positive large-caps | The logical fix for E16's 65.9% DD, but Nagel: reversal is close-anchored → next-open bleeds the gap that killed the oscillators. Needs a diversified book (K=1–3 tension) |
| 2 | **Dividend-initiation drift** (long on first-ever initiation) | D | Michaely-Thaler-Womack 1995 [PR]: +7.5%/12mo | Free EDGAR/dividend data, long-only, no shorting. But ~months horizon (long edge of "swing"), low base rate → thin signal stream for K=1–3 |
| 3 | **One consolidated volatility-breakout kill-shot** (Donchian≈Bollinger-squeeze≈ATR≈Keltner as a single spec) | B/C | MOP 2012 [PR] as *futures* trend | Native swing horizon, cleanest EOD rule — but STW/Bajgrowicz/Marshall predict it dies on stocks after snoop+cost. Run as an honest kill-shot, one spec only |
| 4 | **Vol-targeting sizing overlay** (inverse realized vol) on the best existing sleeve | G/H | Moreira-Muir 2017 [PR], Cederburg 2020 [PR-rebuttal] | Zero new data, clean falsifiable A/B. Prior: Cederburg says it FAILS OOS. Risk-control, not alpha — best-case improves DD, not CAGR |
| 5 | **Free Reg SHO daily short-volume drift** (single-name) | F | Boehmer-Jones-Zhang 2008 [PR] lineage; free 2009+ proxy | Free/EOD/point-in-time/swing-horizon, but a *degraded* proxy for the paid signed-flow signal; overlay-grade, not a high-return engine |
| 6 | **Even-week FOMC-cycle overlay** | E | Cieslak-Morse-Vissing-Jorgensen 2019 [PR] | Pure date math, live mechanism, distinct from the killed E13 TOM. Overlay-not-engine; shrinks under Sullivan-Timmermann-White |
| 7 | **SVXY short-vol carry** gated by free VIX/VIX3M term structure | G | Volmageddon 2021 [PR] documents the tail | Only real VRP harvest reachable at retail scale, but a Feb-2018-style −90% single-day tail; overlaps E18; needs a hard drawdown kill-switch |

Below the line (do NOT re-run): sector momentum (E14), turn-of-month (E13),
earnings-announcement premium (E15), raw weekly reversal (E16), dividend
capture (E20), PEAD (E10), the oscillator MR cluster (E1/E2/E8/E9/E11/E12), MA
rotation (E4/E5/E6/E7), concentrated momentum (E3) — all locally killed. Merger
arb / analyst revisions / guidance / short interest / IV skew — data-gated
(paid or FINRA-walled). Options structures, dispersion, intraday, index
reconstitution — out-of-scope or decayed.

---

## The structural reason the high-return cell is empty

The survey converges on one explanation, stated four ways by four independent
literatures:

- **Concentration destroys the edge.** Real anomalies are diversified
  long-short deciles. K=1–3 keeps the mean, adds back the variance
  (Asness-Frazzini-Pedersen; the §H tables).
- **The edge lives where you can't trade.** Reversal, short interest, ML,
  Baker-Wurgler, PEAD — all concentrate alpha in microcap/illiquid/distressed
  names the mandatory liquidity floor excludes (Avramov-Cheng-Metzker 2023;
  Hou-Xue-Zhang 2020).
- **Publication kills it.** McLean-Pontiff (2016): ~26% OOS / ~58%
  post-publication decay, largest exactly for the low-liquidity anomalies
  above; index effect, day-of-week, pre-FOMC, PEAD all demonstrably decayed.
- **Costs and the overnight gap eat the rest.** The project's own 54%-of-edge-
  in-the-gap finding is corroborated in print (Berkman et al. 2012: buying near
  the open costs more than the half-spread); reversal net-of-cost survives
  only in large-cap turnover-managed *books*, not a K=1–3 next-open bot.

None of these is a defect of the project's search — they are properties of the
opportunity set. The 0-for-20 record is what an honest retail-EOD program
*should* produce.

---

## What would change this conclusion

- **A data source opens.** Paid point-in-time I/B/E/S (analyst revisions,
  guidance), clean historical exchange-listed short interest (unblocks E17), or
  intraday data (unblocks the overnight/microstructure family) would each move
  several DATA-GATED methods into scope.
- **The mandate loosens on concentration or horizon.** If K rises toward a
  diversified book, or the hold extends to weeks–months, then residual
  reversal, sector/residual momentum, and the factor blends become faithful to
  their evidence instead of caricatures of it.
- **A shortlist item passes its pre-registered gate.** If #1 (residual
  reversal) or #2 (dividend-initiation) clears the 2000–2013 gate net of costs
  at next open, that is the program's first genuine survivor. Prior is low —
  #1 is a reversal (the family that died on the gap and on E16's drawdown), #2
  is a small months-horizon premium unlikely to clear 15% concentrated.
- **E19 resolves.** The live insider test is the last catalyst with free,
  clean, point-in-time data; its result (near-certain FAIL under the
  asymmetric survivorship framing) either closes the catalyst family or, if it
  passes, routes to forward paper as uninterpretable rather than validated.

---

## Sources (deduplicated, dated; primary preferred)

**Mean-reversion / reversal**
- de Groot, Huij, Zhou — *Another Look at Trading Costs and Short-Term Reversal Profits* (2012, JBF) — [SSRN 1605049](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1605049)
- Blitz, Huij, Lansdorp, Verbeek — *Short-Term Residual Reversal* (2013, J. Financial Markets) — [SSRN 1911449](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1911449)
- Jegadeesh (1990), Lehmann (1990) reversal — via NY Fed [SR513](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr513.pdf)
- Nagel — *Evaporating Liquidity* (reversal = liquidity provision, 2012, RFS)
- Gatev, Goetzmann, Rouwenhorst — *Pairs Trading* (2006, RFS) — [OUP](https://academic.oup.com/rfs/article-abstract/19/3/797/1646694); Do & Faff (2010, decay) — [SSRN 1707125](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1707125)

**Trend / momentum**
- Moskowitz, Ooi, Pedersen — *Time Series Momentum* (2012, JFE); Huang, Li, Wang, Zhou — *Is it there?* (2020, JFE) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19301953)
- Jegadeesh & Titman (1993); Daniel & Moskowitz — *Momentum Crashes* (2016, JFE) — [NBER w20439](https://www.nber.org/papers/w20439)
- George & Hwang — *The 52-Week High and Momentum* (2004, JF)
- Blitz, Huij, Martens — *Residual Momentum* (2011) — [SSRN 2319861](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2319861)
- Moskowitz & Grinblatt — *Do Industries Explain Momentum?* (1999, JF)
- Da, Gurun, Warachka — *Frog in the Pan* (2014, RFS) — [PDF](https://www3.nd.edu/~zda/Frog.pdf); Gutierrez & Kelley (2008, JF)

**Chart-pattern TA**
- Lo, Mamaysky, Wang — *Foundations of Technical Analysis* (2000, JF) — [PDF](https://www.cis.upenn.edu/~mkearns/teaching/cis700/lo.pdf)
- Park & Irwin — *What Do We Know About the Profitability of Technical Analysis?* (2007, J. Econ. Surveys)
- Sullivan, Timmermann, White — *Data-Snooping, Technical Trading Rule Performance* (1999, JF) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00163); Bajgrowicz & Scaillet (2012, JFE) — [SSRN 1095202](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1095202)
- Marshall, Young, Rose — *Candlestick Technical Trading Strategies* (2006, JBF) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378426605002116); Marshall, Young, Cahan (2008, Japan); Horton (2009)
- Chang & Osler — *Methodical Madness: Head-and-Shoulders* (1999) — [SSRN 51421](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=51421); Savin, Weller, Zvingelis (2007, J. Fin. Econometrics)
- Osler — *Currency Orders and Exchange-Rate Dynamics* (2003, NY Fed) — [SR125](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf)
- Marshall, Cahan, Cahan — *Intraday TA on US equities* (2008) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927539807000588)

**Event / catalyst**
- Bernard & Thomas (PEAD, 1989/90); Martineau — *PEAD.txt / decay* — [Phila Fed WP21-07](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2021/wp21-07.pdf)
- Frazzini & Lamont — *Earnings Announcement Premium* (2007) — [NBER w13090](https://www.nber.org/papers/w13090)
- Cohen, Malloy, Pomorski — *Decoding Inside Information* (2012, JF) — [NBER w16454](https://www.nber.org/system/files/working_papers/w16454/w16454.pdf); Lakonishok & Lee (2001); Jeng-Metrick-Zeckhauser (2003); Tian et al. (2025 decay) — [SSRN 5237160](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5237160)
- Michaely, Thaler, Womack — *Dividend Initiations/Omissions* (1995, JF) — [NBER w4778](https://www.nber.org/papers/w4778)
- Brav, Jiang, Partnoy, Thomas — *Hedge Fund Activism* (2008, JF) — [SSRN 948907](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=948907)
- Greenwood & Sammon — *The Disappearing Index Effect* (2025, JF) — [NBER w30748](https://www.nber.org/system/files/working_papers/w30748/w30748.pdf)
- Mitchell & Pulvino — *Characteristics of Risk in Merger Arbitrage* (2001, JF) — [SSRN 268144](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=268144)

**Seasonality / overnight**
- McConnell & Xu — *Equity Returns at the Turn of the Month* (2008, FAJ)
- Cieslak, Morse, Vissing-Jorgensen — *Stock Returns over the FOMC Cycle* (2019, JF) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12818)
- Lucca & Moench — *The Pre-FOMC Announcement Drift* (2015, JF); Kurov et al. — *Disappearing* (2021, FRL)
- Lou, Polk, Skouras — *A Tug of War* (2019, JFE) — [PDF](https://personal.lse.ac.uk/polk/research/TugOfWar.pdf); Berkman et al. — *Paying Attention* (2012, JFQA)
- Sullivan, Timmermann, White — *Calendar Effects / Data-Driven Inference* (2001, J. Econometrics) — [SSRN 160330](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=160330)

**Sentiment / flow**
- Asquith, Pathak, Ritter — *Short Interest, Institutional Ownership, and Returns* (2005, JFE) — [PDF](https://site.warrington.ufl.edu/ritter/files/2015/04/Short-interest-institutional-ownership-and-stock-returns-2005-08.pdf)
- Hong, Li, Ni, Scheinkman, Yan — *Days to Cover* (2015) — [NBER w21166](https://www.nber.org/system/files/working_papers/w21166/w21166.pdf); Boehmer, Jones, Zhang — *Which Shorts Are Informed?* (2008, JF)
- Pan & Poteshman — *Information in Option Volume* (2006, RFS); Xing, Zhang, Zhao — *Skew* (2010, JFQA)
- Bollerslev, Tauchen, Zhou — *Variance Risk Premia* (2009, RFS) — [PDF](https://public.econ.duke.edu/~boller/Published_Papers/jfqa_14.pdf)
- Da, Engelberg, Gao — *Sum of All FEARS* (2015, RFS); Tetlock — *Giving Content to Investor Sentiment* (2007, JF); Baker & Wurgler (2006, JF) — [NBER w10449](https://www.nber.org/papers/w10449)

**Volatility / options**
- Carr & Wu — *Variance Risk Premiums* (2009, RFS); Bakshi & Kapadia — *Delta-Hedged Gains* (2003, RFS) — [PDF](https://people.umass.edu/~nkapadia/docs/Bakshi_and_Kapadia_2003_RFS.pdf)
- Israelov & Nielsen — *Covered Calls Uncovered* (2015, FAJ) — [SSRN 2444999](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2444999)
- Gao, Xing, Zhang — *Straddles around Earnings* (2018, JFQA) — [SSRN 2204549](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2204549)
- Moreira & Muir — *Volatility-Managed Portfolios* (2017, JF) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12513); Cederburg et al. (2020, JFE) — [PDF](https://www.lehigh.edu/~xuy219/research/COWY.pdf)
- Augustin, Cheng, Van den Bergen — *Volmageddon* (2021, FAJ) — [T&F](https://www.tandfonline.com/doi/abs/10.1080/0015198X.2021.1913040); Cheng & Madhavan — *Dynamics of Leveraged/Inverse ETFs* (2009) — [SSRN 1539120](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1539120)

**Factor / ML / construction**
- Asness, Moskowitz, Pedersen — *Value and Momentum Everywhere* (2013, JF) — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jofi.12021)
- Novy-Marx — *Gross Profitability Premium* (2013, JFE); Asness, Frazzini, Pedersen — *Quality Minus Junk* (2019, RAS) — [SSRN 2312432](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2312432)
- Frazzini & Pedersen — *Betting Against Beta* (2014, JFE); Novy-Marx & Velikov — *Betting Against BAB* (2022, JFE)
- Gu, Kelly, Xiu — *Empirical Asset Pricing via ML* (2020, RFS) — [PDF](https://dachxiu.chicagobooth.edu/download/ML.pdf); Avramov, Cheng, Metzker — *ML vs Economic Restrictions* (2023, Mgmt Sci) — [PDF](https://si-cheng.net/wp-content/uploads/2023/05/2023-ms-avramov_cheng_metzker-machine-learning-vs.-economic-restrictions.pdf)
- Harvey, Liu, Zhu — *…and the Cross-Section of Expected Returns* (2016, RFS) — [PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF); Hou, Xue, Zhang — *Replicating Anomalies* (2020, RFS); McLean & Pontiff — *Does Academic Research Destroy Predictability?* (2016, JF) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365)
- Bailey & López de Prado — *Deflated Sharpe Ratio* (2014) — [SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551); López de Prado — *Advances in Financial ML* (2018, purged/combinatorial CV)

**Prior project docs (superseded/extended by this brief):**
- `docs/research/2026-07-10_swing_strategy_catalog.md` (the ~40-idea catalog)
- `docs/research/2026-07-12_data_type_exploration.md` (data-type probes → E18/E19/E20)
- `docs/findings_2026-07-09_experiment_arc.md` (the E1–E12 arc write-up)
