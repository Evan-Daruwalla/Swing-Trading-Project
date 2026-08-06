# Research Brief — Technical-Analysis Swing Trading Executed by an AI Agent

- **Date:** 2026-08-06
- **Author:** Claude (Opus 5), `/research-brief` 10-stage process
- **Question:** Does chart-based technical analysis (support/resistance, trend lines,
  moving averages, breakouts, pullbacks, RSI/momentum), executed by an algorithm or
  LLM agent on a days-to-weeks holding period, produce a real net-of-cost edge at
  $100–1,000 of capital — and if any part of it does, which part, and how should the
  system be built and validated?
- **Audience:** Evan (sole engineer/decision-maker on this repo), deciding what the
  swing bot's signal layer should be and what validation discipline is mandatory
  before any number from it is believed.

---

> ## RECONCILIATION AGAINST THE PROJECT RECORD — added 2026-08-06 ~12:43 CDT
>
> This brief was written COLD (project files deliberately unread), so its
> conclusions were unreconciled. This note reconciles them. **The brief's findings
> below are NOT rewritten** — the record wins where they conflict, and this block
> records where that happens.
>
> **Nothing in the brief is REFUTED by the record.** Stated plainly because the
> honest answer is not "the brief was wrong": on every claim the repo has actually
> tested, the two agree. What follows is one scope mismatch and one internal
> tension, not a correction of fact.
>
> **AGREEMENTS — reached independently, which is the interesting part:**
>
> | brief claim | record result | where |
> |---|---|---|
> | F1: chart patterns fail net of cost | M11 **FAIL, signal-dead** (gate −0.14% CAGR / Sh 0.09; the survivor universe *destroyed* the documented bearish edge) | Appendix CO, 2026-07-14 |
> | F4: costs are the binding constraint | X9 pairs: **87.4% of trades converged** yet lost 70% of capital — the signal is real and smaller than four legs of cost; gross SEC Sharpe already −0.05 | Appendix DP, 2026-08-03 |
> | F2: MA-timing overstated, ≈ buy-and-hold | **six one-window deaths** of the 200-DMA family (E6-downgrade, C7, X6, X7, X8a) across US equity, non-US equity, crypto, credit, gold; E6 explicitly downgraded to *drawdown control, not return enhancement* | CV, DO, DP |
> | F2: short-horizon reversal is cost-bound | E1 FAIL — **more than half the edge sits in the overnight gap** next-open execution cannot enter | Appendix O, 2026-07-09 |
> | F7: LLM alpha is mostly beta | no LLM sleeve was ever deployed here; the e1_llm_veto design died with E1 | CP/CQ |
>
> **THE CRUX — is M12's "horizon binds" the same result as F2's "the surviving
> evidence is long-horizon"? NO. Same direction, different claims.** Three reasons:
> 1. **Different quantities.** M12 varied hold length with the signal held constant
>    and identified a **cost/turnover** mechanism — the tell is that the horizon
>    effect *grows* when cost triples (SEC +2.06 pp → +7.20 pp; turnover 50.4× →
>    8.2×/yr). That is an argument about **friction**. F2 is an argument about
>    **where the premium is documented**. Complementary, not redundant.
> 2. **M12 never reaches the literature's horizon.** Its winning cell is **63
>    sessions ≈ 3 months**; MOP-2012 and George/Hwang are **6–12 months**. M12's best
>    cell is still an extrapolation *below* the evidence, not an arrival at it.
> 3. **M12 cannot separate the two explanations.** Moving only hold length makes
>    "longer = cheaper" and "longer = more real signal" co-move. M12 measured the
>    first; F2 supplies the second. Neither alone establishes the other.
>
> **SCOPE MISMATCH (not a contradiction) — breadth.** F2 says the surviving evidence
> is *diversified*; M12 found K=20 **hurt** (breadth alone −9.60 pp SEC). These do
> not conflict: M12's K=20 of 142 is a **14% sort**, while academic momentum is a
> decile of thousands (**~1% sort**). The record holds both data points — the sister
> project's `momentum_v2` at **top-50 of ~5,200 (1% sort) VALIDATED** (IS +21.0%/yr,
> OOS +26.5%/yr). So M12 measured **sort strength inside a small universe**, not
> diversification, and its own results doc already discloses this. The brief's claim
> is about a construction M12 never tested.
>
> **INTERNAL TENSION IN THE BRIEF'S OWN RANKING.** Candidate #1 (52-week-high
> proximity) rests on George/Hwang — **monthly-rebalanced, long-short, top/bottom
> 30%, 6–12 month holds**. Recommending it *and* compressing it to K=3 / 5–20 days
> reintroduces exactly the extrapolation F2 warns against. The brief says the
> compression "is the untested part"; the record sharpens that: **E3 already tested
> concentrated single-stock momentum and it FAILED** (6.27% gate CAGR, lost to its
> own universe's equal-weight buy-hold — Appendix ~2026-07-10). The compression is
> not merely untested; its nearest tested neighbour failed.
>
> **CLAIMS THIS REPO HAS ALREADY TESTED** (so they need no re-testing):
> chart patterns → **M11 FAIL**; high-turnover cost death → **X9 FAIL**; MA/trend
> gating → **6 one-window deaths**; short-horizon reversal → **E1/E16/C1 FAIL**;
> PEAD, the brief's candidate #2 → **E10/E15 FAIL, decayed post-2010**;
> horizon-vs-concentration → **M12**. **Genuinely untested: the 52-week-high anchor**
> (the repo's own 2026-07-12 method survey already flagged it IN-SCOPE-UNTESTED).
>
> **BEARING ON THE PROPOSED COST-MODEL/HARNESS BUILD:** the measurement instrument
> F4 demands **already exists** — `fill_divergence` (built 2026-07-28, audit #2)
> holds **4 real sim-vs-broker fills: +0.0, +0.0, +1.3, −85.7 bps**. It should be
> the data source rather than a new one. But **n=4 cannot calibrate a friction
> distribution**: 3 of 4 are the same ticker (QQQ), same side, and the −85.7 bps
> outlier is a documented discipline break (an intraday fire, record DE), not
> spread. **The harness can be SPECIFIED now; it cannot be CALIBRATED yet.**

## TL;DR

**The baseline as stated is half-right, and the wrong half is the half most retail
material emphasizes.** The *pattern-recognition* component — head-and-shoulders,
double tops, candlestick patterns, "buy the breakout above resistance" as a
standalone rule — has repeatedly survived in-sample and died out-of-sample once
data-snooping is corrected for, and dies again to transaction costs even in-sample
([Sullivan/Timmermann/White 1999](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00163);
[Bajgrowicz/Scaillet 2012](https://www.sciencedirect.com/science/article/abs/pii/S0304405X1200116X);
[Marshall/Young/Rose 2006](https://www.sciencedirect.com/science/article/abs/pii/S0378426605002116)).
The *trend/momentum* component survives — but the surviving version is a
**cross-sectional, diversified, 6-to-12-month-horizon portfolio effect**
([Moskowitz/Ooi/Pedersen 2012](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf);
[George/Hwang 2004](https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf)), not a
single-chart, K=1–3, days-to-weeks trade. Support/resistance is the one classical
concept with a *verified order-flow mechanism* behind it
([Osler 2003](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf)),
but that evidence is FX dealer order books, not EOD equity bars.

**On the AI half: the published LLM-trading-agent literature is not yet evidence.**
A May-2026 audit of 77 studies found that of the 19 with closed-loop evaluation,
**2/19 disclosed a time-consistent train/test split, 1/19 specified a transaction-cost
model, 1/19 documented survivorship handling, and 0/19 reached full reproducibility**
([Xia et al. 2026](https://arxiv.org/abs/2605.19337)). When memorized market history
is masked out, frontier LLM agents' returns are *"largely explained by passive market
and style exposure, with limited evidence of persistent stock-selection alpha"*
([Zhu et al., KTD-Fin, 2026](https://arxiv.org/abs/2605.28359)).

**Verdict on the pre-registered hypotheses:** H1 (classical chart TA has a tradable
edge) **fails in strong form**, survives only weakly — some chart-derived state carries
*incremental distributional information*
([Lo/Mamaysky/Wang 2000](https://www.nber.org/system/files/working_papers/w7613/w7613.pdf)),
which is not the same as a net-of-cost strategy. **H2 (trend survives, patterns don't)
is the winner**, with the amendment that the surviving form is structurally
incompatible with K=1–3. **H3 (data-snooping null) survives specifically for
rule-mined chart patterns.** **H4 (LLM agents add nothing over coded rules; their wins
are leakage) survives** on the current evidence.

**The binding constraint at $100–1,000 is not signal quality — it's cost arithmetic
and validation discipline.** Build the cost model and the overfitting-resistant test
harness *first*; the signal is the cheap part.

---

## Method, scope, and limitations

**Design (stage 4).** Hypotheses were written before collection (see TL;DR and
`Hypotheses` below). Evidence was sought in four buckets: (a) peer-reviewed tests of
technical trading rules with explicit data-snooping correction; (b) the
momentum/trend/reversal anomaly literature and its post-2010 decay; (c) the
retail-trader cost and outcome base rate; (d) the 2024–2026 ML/LLM-agent trading
literature and its methodological audits. Preference given to primary sources
(journal papers, arXiv preprints, regulatory filings, law-firm regulatory alerts)
over blog rehashes.

**Limitations — read these before using any number here:**

1. **The project's own files were deliberately not read.** Evan's instruction was an
   explicit cold-sweep constraint ("without looking at the files in the folder"). This
   brief therefore does **not** reconcile against `HANDOFF.md`, the append-only record,
   or any prior work in this repo. Anything here that contradicts the record — the
   record wins. Reconciliation is an open follow-up task.
2. **Desk research only. No backtests were run for this brief.** Every performance
   number is quoted from a source, not produced here.
3. **Some numbers are single-source or could not be verified.** They are tagged
   inline as `[UNVERIFIED]`. Most notably: the headline Sharpe ratios for
   Jiang/Kelly/Xiu (2023) — secondary summaries report mutually inconsistent figures
   (equal-weight 1.2 vs. 2.4; value-weight 0.3 vs. 0.5) and the paper PDF would not
   parse. The *qualitative* finding is well-attested; treat the magnitude as unknown.
4. **No primary data collection was possible.** Questions that genuinely need it —
   e.g. "what is *your* broker's realized effective spread on *your* candidate
   universe at *your* order sizes?" — are scoped as open items, not estimated. The
   method a human would use: pull your broker's Rule 605 execution-quality reports
   and measure realized slippage on paper fills. Not simulated here.
5. **US-equity focus.** FX and futures evidence is used where it is the best available
   mechanism evidence and is labeled as such.

---

## Hypotheses (pre-registered, stage 3)

| # | Hypothesis | Verdict |
|---|---|---|
| H1 | Classical chart TA (S/R, trend lines, breakouts, pullbacks, RSI) has genuine predictive edge; an agent trading it beats buy-and-hold | **Fails in strong form.** Weak form (charts carry *some* incremental information) survives. |
| H2 | The trend/momentum component survives OOS, the pattern-recognition component does not; short-horizon mean reversion is real but too thin for retail costs | **Survives — the winner.** Amendment: the surviving trend evidence is cross-sectional and multi-month, not K=1–3 swing. |
| H3 | Any apparent edge is data-snooping; corrected for multiple testing it is indistinguishable from zero | **Survives for rule-mined chart patterns specifically.** Does not hold for momentum/52-week-high, which replicate across markets and decades. |
| H4 | LLM/vision agents add nothing over a coded rule set; reported wins are lookahead leakage | **Survives.** Strongest single result: alpha vanishes under memory-controlled evaluation. |

---

## Findings

### F1. The pattern-recognition half of the baseline is the weakest-evidenced half

- **The literature's "positive" tally is not what it looks like.**
  [Park & Irwin (2007, *J. Economic Surveys* 21:786–826)](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2007.00519.x)
  surveyed 92 modern studies: 58 positive, 24 negative, 10 mixed — and then stated
  that most of those studies are compromised by *data snooping, ex-post selection of
  trading rules, and difficulties estimating risk and transaction costs*. Their
  positive finding is time-boxed: technical rules generated economic profits in
  various speculative markets **at least until the early 1990s**. That is a survey of
  a *disappearing* effect, not a standing one.

- **The canonical data-snooping correction kills it out-of-sample.**
  [Sullivan, Timmermann & White (1999, *J. Finance* 54:1647–1691)](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00163)
  expanded Brock/Lakonishok/LeBaron's 26 rules into a full universe over 100 years of
  daily DJIA data and applied White's Reality Check bootstrap. Result: the best rule
  *does* survive data-snooping correction **inside BLL's original sample** — and does
  **not** deliver superior performance in the subsequent 10-year post-sample period,
  and shows **no evidence of outperformance on S&P 500 futures** once snooping is
  accounted for. This is the exact signature of an artifact.

- **The modern re-test kills it in-sample too, on costs.**
  [Bajgrowicz & Scaillet (2012, *JFE* 106:473–491)](https://www.sciencedirect.com/science/article/abs/pii/S0304405X1200116X)
  re-ran DJIA daily prices 1897–2011 using False Discovery Rate control. Two findings
  that matter more than any backtest you will ever run: (i) **persistence tests show
  an investor would never have been able to select the future best-performing rules
  ex ante**, and (ii) **even in-sample, performance is completely offset by the
  introduction of low transaction costs.** They conclude this "seriously calls into
  question the economic value of technical trading rules reported for early periods."

- **Candlestick patterns specifically: no value.**
  [Marshall, Young & Rose (2006, *JBF* 30:2303–2323)](https://www.sciencedirect.com/science/article/abs/pii/S0378426605002116)
  tested 14 candlestick patterns on DJIA component stocks 1992–2002 using a bootstrap
  that generates random OHLC prices. No statistically significant excess returns vs.
  random trading.

- **The strongest pro-pattern paper claims less than it is usually cited for.**
  [Lo, Mamaysky & Wang (2000, *J. Finance* 55:1705–1765)](https://www.nber.org/system/files/working_papers/w7613/w7613.pdf)
  built automated pattern recognition via nonparametric kernel regression over US
  stocks 1962–1996 and compared the *unconditional* return distribution to the
  distribution *conditioned* on patterns (head-and-shoulders, double bottoms, etc.).
  They found several indicators **do provide incremental information and "may have
  some practical value."** Note precisely what that is: a statement about conditional
  return *distributions*, not a demonstration of a net-of-cost tradable strategy. It
  is the best evidence for H1 and it is still a weak-form claim.

**Read of F1:** "Buy the breakout above resistance, sell the trendline break" is not
a null hypothesis you get to assume is true. It is a hypothesis that has been tested
adversarially for thirty years and has mostly lost.

### F2. The trend/momentum half has real evidence — at a structure incompatible with K=1–3

- **Time-series momentum.**
  [Moskowitz, Ooi & Pedersen (2012, *JFE* 104:228–250)](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf):
  58 futures and forward contracts (equity indices, currencies, commodities, sovereign
  bonds), 25+ years. Each instrument's **past 12-month excess return positively
  predicts its future return**; the effect persists ~12 months then partially reverses.
  A *diversified portfolio across all asset classes* delivers substantial abnormal
  returns with little exposure to standard factors and performs best in extreme
  markets. Every load-bearing word there — 58 instruments, 12 months, diversified —
  is a structural constraint, not decoration.

- **"Breakout to new highs," done rigorously, is the 52-week-high effect.**
  [George & Hwang (2004, *J. Finance* 59:2145–2176)](https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf):
  rank stocks monthly by (current price ÷ 52-week high); long the top 30%, short the
  bottom 30%, hold 6 or 12 months. **Nearness to the 52-week high dominates and
  improves on past returns as a predictor.** Average return **0.45%/month** across all
  months, rising to **1.23%/month** excluding January. Critically: these forecasts
  **do not reverse in the long run**, unlike conventional momentum. This is the
  academically defensible ancestor of "buy the breakout" — and it is a monthly-rebalanced
  cross-sectional long-short over 6–12 months.

- **Moving-average timing is substantially overstated.**
  [Zakamulin's](https://papers.ssrn.com/abstract=2242795) out-of-sample work
  (with realistic transaction costs, and explicitly re-running simulations that had
  contained look-ahead bias) found **no statistically significant evidence that MA
  timing strategies outperformed the market in the second half of his sample**, and
  that most of the time MA-strategy performance is **statistically indistinguishable
  from buy-and-hold**. If your system's core is "price above the 50-day MA," this is
  the paper that says the reported edge is mostly data-mining bias plus frictions.

- **Momentum has decayed but is not dead.** One recent practitioner review reports the
  momentum factor returning ~10%/yr in the 1990s versus **closer to 2% today**
  `[UNVERIFIED — single secondary source]`, while noting **2024 was momentum's best
  year among equity factors** and that a basic US-equity momentum strategy averaged
  ~9%/yr over 1866–2024
  ([Alpha Architect summary](https://alphaarchitect.com/momentum-factor-investing/);
  [van Vliet et al. 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5561720)).
  Directionally: real, decayed, and cyclical enough that a 2–3 year live sample tells
  you almost nothing.

- **Short-horizon mean reversion (the RSI half of the baseline) has decayed and is
  cost-bound.** Conventional reversal strategies showed weak post-1990 performance,
  with average returns rising only marginally from **0.18% to 0.26%/month**
  `[UNVERIFIED — quoted via search summary of Blitz/Huij et al.; not read in full]`,
  and researchers note reversal requires **frequent rebalancing in disproportionately
  high-cost securities**, which can prevent profitable execution
  ([Blitz/Huij et al.](https://www.efmaefm.org/0EFMSYMPOSIUM/2012/papers/017_update.pdf);
  [NY Fed SR-513](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr513.pdf)).
  A 0.26%/month gross signal traded through a retail spread is not an edge.

**Read of F2:** the evidence supports *trend* as a cross-sectional ranking signal over
a diversified book on multi-month horizons. Compressing that to 1–3 concentrated
positions over 5–20 days is an extrapolation well outside the evidence. That may
still be the right call given the stated risk appetite — but it must be
**pre-registered as an extrapolation and tested as one**, not inherited as if the
papers endorsed it.

### F3. Support/resistance has the best *mechanism* story in all of technical analysis

[Osler (2003, *J. Finance* 58:1791–1820)](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf)
examined actual stop-loss and take-profit orders at a large FX dealing bank and found:

- **Take-profit orders cluster strongly at round numbers** → prices tend to reverse at
  those levels (the "resistance/support holds" prediction).
- **Stop-loss orders cluster strongly just *beyond* round numbers** → prices tend to
  accelerate once the level is crossed (the "breakout runs" prediction).
- **96% of published FX support/resistance levels end in 0 or 5; 20% end in 00.**

This is the only place in the literature where a classical TA prediction is explained
by a *directly observed order-flow mechanism* rather than by curve-fitting. Two
caveats that keep it from being a green light: it is **FX dealer data, not US
equities**, and it explains *why price behaves that way*, not that a retail trader
nets a profit from it after crossing the spread. Testing it properly needs order-flow
or at least intraday data — which this project's EOD-only rule currently forbids.

### F4. Cost arithmetic and the retail base rate are the binding constraint

- **The base rate.** [Barber, Lee, Liu & Odean](https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf)
  used the *complete* trading records of the Taiwan Stock Exchange, 1992–2006:
  **more than 8 in 10 day traders lost money in the typical semiannual period**;
  **fewer than 1% were predictably profitable**; day traders lost an average of
  **23.9 basis points per day net of fees**; and aggregate day-trader performance was
  **reliably negative in 14 of the 15 years** studied. In the
  [follow-up cross-section-of-skill paper](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/The%20Cross-Section%20of%20Speculator%20Skill.pdf),
  predictably-profitable traders were **<3% of all day traders**. Swing trading is
  lower-turnover than day trading, which moves you along this distribution — it does
  not move you off it.

- **Costs are what killed the rules, repeatedly.** Bajgrowicz & Scaillet: in-sample
  TA performance **completely offset by low transaction costs**. The reversal
  literature: profits blocked by rebalancing in high-cost securities. This is the same
  failure mode showing up in two independent literatures.

- **Commission-free is not cost-free.** At $100–1,000 with concentrated positions,
  your cost is the **bid-ask spread plus slippage**, paid twice per trade.
  Practitioner guidance converges on small-cap spreads running several multiples of
  large-cap, with 0.5% spreads treated as disqualifying and limit orders mandatory
  below ~100k average daily volume
  ([Trade The Pool](https://tradethepool.com/fundamental/how-to-trade-small-cap-stocks-best-guide-for-traders/))
  `[practitioner sources, not peer-reviewed — treat as order-of-magnitude only]`.

- **The arithmetic you should run before writing any signal code** (this is derivation,
  not a sourced claim): a K=1–3 book with 5–20 day holds implies roughly 25–100 round
  trips per year at full deployment. At a total round-trip friction of *r* basis
  points, annual cost drag is ≈ (round trips) × *r*. At r=15bp and 50 round trips
  that's ~7.5% of capital per year — comparable to the entire long-run equity risk
  premium. **The cost model is therefore not a detail to add later; it determines
  whether any candidate strategy is even admissible.** Concretely: the strategy must
  clear its own friction before it clears the benchmark, and the friction estimate
  must come from measured paper fills, not an assumed constant.

- **Concentration is a skewness bet, and the base rate is brutal.**
  [Bessembinder (2018, *JFE* 129:440–457)](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301521):
  **57.4% of all CRSP common stocks had a lifetime buy-and-hold return below one-month
  T-bills**, and **4.3% of stocks account for the entire net wealth creation** of the
  US market. With K=1–3 you are drawing a very small sample from a distribution where
  the median draw loses to T-bills. This does not make K=1–3 wrong given an explicit
  high-variance mandate — but it means **median outcome and mean outcome will diverge
  sharply**, and any evaluation that reports only the mean of a small number of runs
  is measuring luck. Evaluation must report the full distribution.

### F5. The regulatory environment changed in 2026 — this removes an excuse, not the constraint

- **The Pattern Day Trader rule and the $25,000 minimum are gone.** The SEC approved
  FINRA's amendments to Rule 4210 on **2026-04-14**, effective **2026-06-04**,
  eliminating the "pattern day trader" definition, the **$25,000 minimum equity
  requirement**, and "day trading buying power" calculations. They are replaced by an
  **intraday margin standard** applying to all margin accounts: firms must either
  block trades that would create an intraday margin deficit in real time, or perform
  an end-of-day calculation and issue a margin call. Firms may **phase in over 18
  months, ending 2027-10-20**
  ([WilmerHale client alert, 2026-04-23](https://www.wilmerhale.com/en/insights/client-alerts/20260423-sec-approves-amendments-to-finra-rule-4210-replacing-day-trading-margin-requirements-with-a-modernized-intraday-margin-standard);
  [King & Spalding](https://www.kslaw.com/news-and-insights/finra-adopts-sweeping-changes-to-margin-requirements-for-day-trading);
  [FINRA Regulatory Notice 26-10](https://www.finra.org/rules-guidance/notices/26-10);
  [SEC order SR-FINRA-2025-017](https://www.sec.gov/files/rules/sro/finra/2026/34-105226.pdf)).
  **Caveat:** because of the phase-in, *your specific broker may not have implemented
  this yet*, and brokers have historically been free to impose stricter house rules.
  Verify with the actual broker before designing around it.

- **Settlement is T+1**, effective **2024-05-28** under amended Rule 15c6-1(a)
  ([Davis Polk](https://www.davispolk.com/insights/client-update/sec-adopts-t-1-settlement-effective-may-2024);
  [FINRA technical notice](https://www.finra.org/filing-reporting/technical-notice/final-reminder-t-1-settlement-052224)).
  Cash-account capital recycles in one business day, not two.

**Read of F5:** the structural reason a sub-$25k account *had* to hold overnight is
gone as of mid-2026. That is a genuine change to the design space — but it cuts
against you as much as for you, because the strategies it unlocks (higher turnover)
are exactly the ones F4's cost arithmetic punishes hardest. Do not let a removed
regulatory constraint pull the design toward more trading.

### F6. "AI reading charts" has one strong result — and it isn't shaped like your system

[Jiang, Kelly & Xiu (2023, *J. Finance* 78:3193–3249)](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13268)
trained CNNs on **images** of price/volume charts (OHLC bars, volume, a moving
average) to predict the sign of forward returns. Findings:

- The key mechanism is **implicit rescaling**: rendering each stock's window as an
  image where the recent high/low span the image height puts every stock on the same
  scale, enabling powerful **cross-sectional** comparison. That is the actual source
  of the edge — not "the model learned head-and-shoulders."
- Patterns show **context independence** (short-horizon patterns work at longer
  scales) and **transfer to international markets** from US-trained models.
- The strategy is a **long-short decile spread**, with weekly rebalancing and
  **turnover reported at roughly 7×** `[UNVERIFIED — secondary summary]`.
- Headline Sharpe ratios: secondary summaries report **inconsistent** figures
  (equal-weight 1.2 *or* 2.4; value-weight 0.3 *or* 0.5). **Do not cite a number here
  without reading the paper.** `[UNVERIFIED]`

**Read of F6:** this is the best existing evidence that a machine can extract signal
from chart images. It is also a high-turnover, cross-sectional, long-short,
many-hundreds-of-names strategy — the structural opposite of a K=1–3 long-only
$500 account. It validates the *idea* while invalidating the *implementation shape*.

### F7. LLM trading agents: the literature is not yet evidence, and the controlled result is damning

- **The audit.** [Xia et al., "Agentic Trading: When LLM Agents Meet Financial
  Markets" (arXiv 2605.19337, 2026-05-19)](https://arxiv.org/abs/2605.19337) screened
  **77 studies** through 2026-03-09; **19** met the minimum bar of "action output plus
  closed-loop evaluation." Within those 19:
  - **2/19** disclose an extractable **time-consistent data split**
  - **1/19** specifies a **transaction-cost model**
  - **1/19** documents **universe/survivorship handling**
  - **11/19** report execution timing/semantics
  - **15/19** sit at reproducibility tier **R0**; **0/19** reach **R3**

  Their conclusion: architectural experimentation is expanding fast while *"comparable
  evaluation protocols, execution semantics, and reproducible artifacts remain the
  field's immediate bottlenecks."*

- **Parametric look-ahead is a real, measured effect.**
  [Li, Wang & Ma (arXiv 2605.24564, 2026-05-23)](https://arxiv.org/html/2605.24564)
  name the problem *parametric look-ahead bias*: an LLM trained after an event
  implicitly knows the outcome, and that knowledge lives in the weights where no
  train/test split can reach it. Their FinCAD decoding intervention, across five
  7–14B models and five mega-cap stocks, **reduced in-sample backtest returns by up to
  67.1% on memorized dates** while leaving 2025 out-of-sample returns within $8K and
  Sharpe within 0.10 of baseline. The size of that gap *is* the measurement of the
  contamination.

- **The controlled result: the alpha is beta.**
  [Zhu et al., KTD-Fin (arXiv 2605.28359, 2026-05-27)](https://arxiv.org/abs/2605.28359)
  built a memory-controlled benchmark that masks tickers and calendar information in
  every prompt and tool response, then ran **ten frontier LLM agents** on CSI300 over
  2024–2026 with Barra-style attribution. Finding: under leakage-controlled evaluation,
  agents' cumulative returns are **"largely explained by passive market and style
  exposure, with limited evidence of persistent stock-selection alpha."**

- **The most-cited positive LLM result is a *news-sentiment* result, and it decays.**
  [Lopez-Lira & Tang (arXiv 2304.07619)](https://arxiv.org/abs/2304.07619) found
  ChatGPT headline scores significantly predict out-of-sample daily returns,
  subsuming traditional methods, strongest in smaller stocks and after negative news
  — a self-financing long/short earning **~650% cumulative from 2021m10–2023m12**.
  But the annualized **Sharpe decays 6.54 (2021Q4) → 3.68 (2022) → 2.33 (2023)** as
  LLM adoption rises. Two readings are both consistent with the data: a real edge
  being arbitraged away, or progressively worse leakage in the early window. Either
  reading argues against building on it now. Note also: this is **text**, not charts.

- **[TradingAgents (arXiv 2412.20138)](https://arxiv.org/html/2412.20138v1)** and the
  FinMem/FinAgent line report strong backtests, but the TradingAgents evaluation window
  is **2024-06-19 to 2024-11-19** — a single five-month window falling inside frontier
  training data — and the authors themselves note performance varies with backbone
  model, temperature, trading period, and data quality. Treat these as **architecture
  references and code to read**, not as evidence of edge.

**Read of F7:** an LLM agent is currently defensible in exactly one role — a
**constrained overlay or veto** on top of a coded, independently-validated signal,
evaluated only on data strictly after the model's knowledge cutoff. As the primary
decision-maker it is, on present evidence, a beta machine with a narrative generator
attached.

### F8. The validation harness is the actual deliverable

Given F1/F3/F7, the thing that separates this project from the 92 studies Park &
Irwin found methodologically compromised is the test discipline, not the strategy.
Minimum bar, all sourced:

- **Deflated Sharpe Ratio** — [Bailey & López de Prado (2014, *JPM* 40(5):94–107)](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)
  corrects an observed Sharpe for **selection bias under multiple testing**, non-normal
  returns, sample length, skewness and kurtosis. It requires you to **honestly count
  the number of trials you ran** — which means logging every variant you test,
  including the ones you abandoned.
- **Probability of Backtest Overfitting (PBO)** — [Bailey, Borwein, López de Prado &
  Zhu (*J. Computational Finance* 20(4):39–70)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253).
- **Purged K-fold CV with embargo, and Combinatorial Purged Cross-Validation (CPCV)** —
  [purged CV](https://en.wikipedia.org/wiki/Purged_cross-validation) removes training
  samples whose label windows overlap the test set; CPCV builds many train/test
  combinations to yield a *distribution* of OOS estimates rather than one number.
  In a synthetic controlled comparison, [Arian, Norouzi & Seco](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4686376_code4361537.pdf?abstractid=4686376&mirid=1)
  found CPCV showed **lower PBO and better deflated-Sharpe statistics than K-fold,
  purged K-fold, and walk-forward**. Walk-forward remains the more realistic
  *trading simulation*; use both, for different questions.

This maps cleanly onto the project's existing frozen-regression discipline: pin the
reference numbers, fail loud on drift, and never tune a FAIL.

---

## Ranked candidates for the signal layer

Ranked by **evidence quality × implementability at $100–1,000**, given the stated
mandate (high % return, K=1–3, losses accepted, EOD-only).

| # | Candidate | Why it ranks here | The tradeoff you're accepting |
|---|---|---|---|
| **1** | **Cross-sectional trend/breakout rank, 5–20 day holds, K=3.** Signal = proximity-to-52-week-high (George/Hwang) + a 12-1 or shorter TS-momentum filter + a hard liquidity floor. | Best evidence-to-build-cost ratio here. Both parent effects replicate across decades, markets, and asset classes. Fits EOD-only and a tiny account. | The source evidence is a **diversified 6–12 month long-short**. Compressing to K=3 over 5–20 days is an extrapolation. Must be pre-registered as such and tested against the un-compressed version as a control. |
| **2** | **PEAD-timed swing entries** — enter on earnings surprise, hold 5–20 days. | The only well-documented anomaly whose **native horizon actually matches swing trading**, and it is event-driven, which makes pre-registration and point-in-time discipline natural. | Magnitude has **decayed substantially** — from ~18% annualized abnormal returns in Bernard & Thomas (1989) toward insignificance in some recent US samples ([Fink 2020 review](https://static.uni-graz.at/fileadmin/sowi/Working_Paper/2020-04_Fink.pdf)). Needs a **point-in-time earnings/estimates feed** you do not currently have free. |
| **3** | **Support/resistance + round-number rules, Osler-style.** | The only classical TA concept with a **directly observed order-flow mechanism**. Matches the baseline's core intuition most closely of anything that has real backing. | Evidence is **FX dealer order books, not US equities**. Testing it honestly wants intraday/order data, which the project's EOD-only hard rule forbids. Would require either a data-source decision or an explicit "we're testing a weaker EOD proxy" caveat. |
| **4** | **Image-CNN on chart images (JKX replication).** | Strongest existing evidence that a model can read charts. Highest engineering-portfolio value of anything on this list. | **Structurally incompatible** with the mandate: cross-sectional long-short, ~7× turnover, hundreds of names. Also a large build with real GPU/data requirements. Good as a research milestone, bad as *the* signal layer. |
| **5** | **LLM agent as decision-maker.** | Highest narrative value; lowest evidentiary support on this list. | **0/19 studies reproducible; alpha vanishes under memory control.** Only defensible as a **veto/context overlay** on a coded signal, evaluated strictly post-cutoff, with the coded signal alone as the mandatory control arm. |
| **6** | **Classical chart-pattern recognition (H&S, double tops, flags, candlesticks) as the primary signal.** | Matches the baseline description most literally and is what most retail material teaches. | **Weakest evidence of the six.** Fails OOS under Reality Check, fails to costs even in-sample under FDR, and candlesticks specifically show no value vs. bootstrap-random. Worth building only as a **falsification exercise** — which, honestly documented, is itself a legitimate portfolio artifact. |

**Recommendation: #1, with #5 strictly as a later overlay — and neither of them
first.** The first deliverable should be the **cost model plus the CPCV/DSR
validation harness**, with a deliberately dumb signal running through it, because F4
says the cost model determines admissibility and F8 says the harness is what makes
any subsequent number believable. Building the harness against a known-worthless
signal (#6 is a good choice) is the cheapest possible way to prove the harness
actually rejects things.

---

## What would change this conclusion

These are the untested falsifiers from stage 3 — the specific results that would move
the verdict:

1. **A CPCV-validated, cost-inclusive backtest in which a chart-pattern signal beats
   a matched trend/momentum signal on the same universe and horizon**, with an honest
   trial count fed into a deflated Sharpe. That would revive H1 and is exactly the
   experiment nobody in the surveyed literature ran cleanly.
2. **A measured round-trip friction materially below the practitioner estimates** on
   the actual candidate universe — from real paper fills, not assumptions. If total
   friction is genuinely ~5bp rather than ~15–30bp, F4's arithmetic loosens a lot and
   higher-turnover candidates (#3, #4) become admissible.
3. **An equities replication of Osler's order-clustering result** — even a weak EOD
   proxy showing round-number levels carry incremental predictive information in US
   equities would promote candidate #3 sharply.
4. **An LLM-agent result on a strictly post-cutoff window with a coded-signal control
   arm** showing the agent adds incremental return over the control. Nothing in the
   current literature does this; if you produce it, that's a genuinely novel artifact.
5. **Evidence that the 52-week-high effect survives compression** to K=3 and 5–20 day
   holds. The papers do not test this. If it doesn't survive, candidate #1 collapses
   into "just hold a diversified momentum sleeve," which contradicts the mandate and
   forces an explicit decision about which one wins.

### Open questions this brief could not answer

- **What is your broker's actual realized effective spread and slippage** on your
  candidate universe at your order sizes? Requires broker Rule 605 reports + measured
  paper fills. Not estimable from desk research.
- **Has your broker implemented the post-PDT intraday margin regime yet**, and does it
  impose stricter house rules? Requires asking the broker; the 18-month phase-in runs
  to 2027-10-20.
- **What do this project's existing docs already conclude?** Not read, by instruction.
  This brief must be reconciled against `HANDOFF.md` and the append-only record before
  any of it drives a build decision.

---

## Sources

**Technical analysis — tests and surveys**
- Park, C.-H. & Irwin, S.H. (2007). *What Do We Know About the Profitability of Technical Analysis?* Journal of Economic Surveys 21:786–826. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2007.00519.x
- Sullivan, R., Timmermann, A. & White, H. (1999). *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap.* Journal of Finance 54:1647–1691. https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00163 — PDF: https://www.kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf
- Bajgrowicz, P. & Scaillet, O. (2012). *Technical Trading Revisited: False Discoveries, Persistence Tests, and Transaction Costs.* JFE 106:473–491. https://www.sciencedirect.com/science/article/abs/pii/S0304405X1200116X
- Marshall, B.R., Young, M.R. & Rose, L.C. (2006). *Candlestick Technical Trading Strategies: Can They Create Value for Investors?* JBF 30:2303–2323. https://www.sciencedirect.com/science/article/abs/pii/S0378426605002116
- Lo, A.W., Mamaysky, H. & Wang, J. (2000). *Foundations of Technical Analysis.* Journal of Finance 55. NBER WP 7613: https://www.nber.org/system/files/working_papers/w7613/w7613.pdf
- Zakamulin, V. *The Real-Life Performance of Market Timing with Moving Average and Time-Series Momentum Rules.* https://papers.ssrn.com/abstract=2242795 — and *Market Timing with Moving Averages* https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2585056

**Momentum, trend, reversal, and the cross-section**
- Moskowitz, T.J., Ooi, Y.H. & Pedersen, L.H. (2012). *Time Series Momentum.* JFE 104:228–250. https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf
- George, T.J. & Hwang, C.-Y. (2004). *The 52-Week High and Momentum Investing.* Journal of Finance 59:2145–2176. https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf
- van Vliet, B., Baltussen, G., Dom, M.S. & Vidojevic, M. *Momentum Factor Investing: Evidence and Evolution.* https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5561720 — summary: https://alphaarchitect.com/momentum-factor-investing/
- Blitz, D., Huij, J. et al. *Short-Term Residual Reversal.* https://www.efmaefm.org/0EFMSYMPOSIUM/2012/papers/017_update.pdf
- FRBNY Staff Report 513, *Decomposing Short-Term Return Reversal.* https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr513.pdf
- Bessembinder, H. (2018). *Do Stocks Outperform Treasury Bills?* JFE 129:440–457. https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301521
- Fink, J. (2020). *A Review of the Post-Earnings-Announcement Drift.* https://static.uni-graz.at/fileadmin/sowi/Working_Paper/2020-04_Fink.pdf

**Microstructure / why support and resistance could work**
- Osler, C.L. (2003). *Currency Orders and Exchange Rate Dynamics: An Explanation for the Predictive Success of Technical Analysis.* Journal of Finance 58. FRBNY Staff Report 125: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf

**Retail outcomes and costs**
- Barber, B.M., Lee, Y.-T., Liu, Y.-J. & Odean, T. *Do Individual Day Traders Make Money? Evidence from Taiwan.* https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf
- Barber, Lee, Liu & Odean. *The Cross-Section of Speculator Skill: Evidence from Day Trading.* https://faculty.haas.berkeley.edu/odean/papers/day%20traders/The%20Cross-Section%20of%20Speculator%20Skill.pdf

**ML / AI on charts and LLM trading agents**
- Jiang, J., Kelly, B.T. & Xiu, D. (2023). *(Re-)Imag(in)ing Price Trends.* Journal of Finance 78. https://onlinelibrary.wiley.com/doi/10.1111/jofi.13268 — PDF: https://www.aidf.nus.edu.sg/wp-content/uploads/2022/02/Xiu-Re-Imagining-Price-Trends.pdf
- Xia, Y., You, P., Wang, T., Liu, F., Qi, H., Wu, X. & Zhang, S. (2026-05-19). *Agentic Trading: When LLM Agents Meet Financial Markets.* arXiv:2605.19337. https://arxiv.org/abs/2605.19337
- Li, W.W., Wang, M. & Ma, T. (2026-05-23). *Summoning the Oracle to Slay It: Mitigating Look-Ahead Bias in Financial Backtesting with LLMs.* arXiv:2605.24564. https://arxiv.org/html/2605.24564
- Zhu, T. et al. (2026-05-27). *From Knowing to Doing: A Memory-Controlled Benchmark for LLM Trading Agents on Stock Markets (KTD-Fin).* arXiv:2605.28359. https://arxiv.org/abs/2605.28359
- Lopez-Lira, A. & Tang, Y. *Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models.* arXiv:2304.07619. https://arxiv.org/abs/2304.07619
- Xiao, Y. et al. (2024-12). *TradingAgents: Multi-Agents LLM Financial Trading Framework.* arXiv:2412.20138. https://arxiv.org/html/2412.20138v1 — code: https://github.com/TauricResearch/TradingAgents

**Validation methodology**
- Bailey, D.H. & López de Prado, M. (2014). *The Deflated Sharpe Ratio.* JPM 40(5):94–107. https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- Bailey, D.H., Borwein, J., López de Prado, M. & Zhu, Q.J. *The Probability of Backtest Overfitting.* J. Computational Finance 20(4):39–70. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
- Arian, H.R., Norouzi M., D. & Seco, L.A. *Backtest Overfitting in the Machine Learning Era: A Comparison of Out-of-Sample Testing Methods in a Synthetic Controlled Environment.* https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4686376_code4361537.pdf?abstractid=4686376&mirid=1
- Purged cross-validation (López de Prado, 2017) overview: https://en.wikipedia.org/wiki/Purged_cross-validation

**Regulatory (verify against your broker before designing around these)**
- SEC order approving SR-FINRA-2025-017 (Rule 4210 amendments), 2026-04-14. https://www.sec.gov/files/rules/sro/finra/2026/34-105226.pdf
- WilmerHale client alert, 2026-04-23. https://www.wilmerhale.com/en/insights/client-alerts/20260423-sec-approves-amendments-to-finra-rule-4210-replacing-day-trading-margin-requirements-with-a-modernized-intraday-margin-standard
- King & Spalding, *FINRA Adopts Sweeping Changes to Margin Requirements for Day Trading.* https://www.kslaw.com/news-and-insights/finra-adopts-sweeping-changes-to-margin-requirements-for-day-trading
- FINRA Regulatory Notice 26-10. https://www.finra.org/rules-guidance/notices/26-10
- Davis Polk, *SEC adopts T+1 settlement effective May 2024.* https://www.davispolk.com/insights/client-update/sec-adopts-t-1-settlement-effective-may-2024
- FINRA, *Final Reminder — T+1 Settlement* (2024-05-22). https://www.finra.org/filing-reporting/technical-notice/final-reminder-t-1-settlement-052224

**Practitioner / infrastructure (lower evidentiary weight, used only for build options)**
- Alpaca Trading API docs (paper trading, fractional shares, historical data). https://docs.alpaca.markets/us/docs/trading-api
- Trade The Pool, small-cap spread and liquidity guidance. https://tradethepool.com/fundamental/how-to-trade-small-cap-stocks-best-guide-for-traders/
