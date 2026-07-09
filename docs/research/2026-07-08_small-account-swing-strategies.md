# Research brief — Swing-trading strategies for a small account ($100–1,000)

**Date: 2026-07-08.** Feeds: strategy selection for `PRD_ROADMAP.md` in
`D:\ClaudeCode\Swing Trading` (systematic EOD bot; signal at close, execute
next open; yfinance price_cache ~5,200 US tickers; Alpaca PAPER).

**Question:** which swing strategies (days-to-weeks holds) have credible
published evidence of edge that survives (a) EOD-only OHLCV data, (b)
survivorship-biased backtest data, and (c) small-account frictions?

---

## TL;DR

Short-horizon mean reversion on **liquid index/sector ETFs** (IBS- and
RSI-family signals) has the strongest published, replicated evidence that fits
this stack — and trading ETFs sidesteps the project's worst limitation
(survivorship bias) entirely. Evan's "trend pullback" and "mean reversion"
candidates are best implemented as ONE strategy: buy short-term weakness
inside a long-term uptrend (trend filter + oversold trigger), the only version
of either with consistent quantified support. Bull-flag breakout should be
rejected — the academic literature could not establish profitability for
codified flag patterns. Sector rotation has solid academic backing but at
weeks-to-months horizons it duplicates what the Trading project already does.
A major friction disappeared mid-2026: the PDT rule was eliminated effective
2026-06-04, so same-day stop-outs are no longer a regulatory trap for
sub-$25k accounts.

---

## Findings

### 1. Short-horizon mean reversion — the best-evidenced family for EOD data

- **Academic base (stocks):** the short-term reversal anomaly (losers over
  ~1 week–1 month outperform next period) is long-documented. The key
  cost-aware study — [de Groot, Huij & Zhou, *Another Look at Trading Costs
  and Short-Term Reversal Profits* (2011/2012, J. Banking &
  Finance)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1605049) —
  finds reversal profits survive transaction costs **only when restricted to
  large caps**: 30–50 bps/week net, including post-decimalization
  ([EFMA copy](https://www.efmaefm.org/0efmameetings/efma%20annual%20meetings/2011-Braga/papers/0259.pdf);
  [Quantpedia summary](https://quantpedia.com/strategies/short-term-reversal-in-stocks)).
  Naive small-cap reversal dies on costs. Direct implication: trade this in
  liquid large caps or ETFs, never the broad 5,200-ticker universe.
- **IBS (Internal Bar Strength) on equity ETFs:** [Pagonidis, *The IBS
  Effect: Mean Reversion in Equity ETFs* (2013, NAAIM)](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
  — IBS = (close − low)/(high − low) on daily bars. Next-day close-to-close
  returns after IBS < 0.20 averaged +0.35% vs −0.13% after IBS > 0.80, across
  US and international index ETFs. Replicated/extended independently:
  [arXiv 2306.12434 (2023) on country ETFs](https://arxiv.org/pdf/2306.12434),
  [Kinlay (2019)](https://jonathankinlay.com/2019/07/the-internal-bar-strength-indicator/),
  [QuantifiedStrategies](https://www.quantifiedstrategies.com/internal-bar-strength-ibs-indicator-strategy/).
  Computable from OHLC alone — perfectly matched to the existing price_cache.
- **RSI(2)/Connors family (practitioner, weaker sourcing):** RSI(2)-below-
  threshold long entries above the 200-day MA, exit on strength. Practitioner
  backtests report the family still working years after publication — e.g.
  [R3 on 20 liquid ETFs, still profitable 12 years post-publication
  (QuantifiedStrategies)](https://www.quantifiedstrategies.com/larry-connors-r3-strategy/),
  [SPY RSI2 ~9%/yr invested ~28% of the time, 34% maxDD
  (algotr.substack)](https://algotr.substack.com/p/this-simple-mean-reversion-strategy),
  [cumulative-RSI variant (quantitativo)](https://www.quantitativo.com/p/squeezing-more-profits-with-cumulative).
  **Single-source practitioner numbers — treat each as unverified until
  reproduced on our own data.** Consistent direction across independent
  practitioners is the signal here, not any one CAGR.
- **Execution-timing caveat (applies to this whole family):** published
  effects are measured close-to-close. Our default loop (signal at close,
  execute next open) forfeits the overnight component, which is a large share
  of short-horizon equity returns (see e.g. [MDPI, overnight vs. daytime
  sector-ETF returns, 2026](https://www.mdpi.com/2227-9091/14/4/84)). Options:
  accept and measure the haircut in backtest (execute next open), or run the
  bot minutes before the close using Alpaca real-time quotes to approximate
  the closing bar. This is a design decision for the PRD, and the backtest
  must model whichever is chosen — with next-open fills, the cached
  `next_open` series already supports it.

### 2. Trend pullback — codifiable, but only as a mean-reversion hybrid

The discretionary description (20>50 EMA, dip to the 20 EMA, "buy the
reversal candlestick") has no direct academic literature. Its codified
cousin — long-term trend filter + short-term oversold trigger — is exactly
the Connors-family setup above and inherits its evidence. One representative
quantified version: close > 200-day MA, close < 20-day MA, RSI(5) < 45, exit
RSI(5) > 65 — reported CAGR 8.3%, 82% win rate, 30% maxDD
([QuantifiedStrategies pullback backtests](https://www.quantifiedstrategies.com/pullback-trading-strategy/);
**single practitioner source, unverified**). Reversal-candle confirmation and
intraday entries are not implementable EOD; the honest version enters at next
open after the signal day. **Recommendation: fold Evan's candidates #1 and #3
into one strategy family** — "buy weakness in an uptrend" — rather than build
two.

### 3. Bull-flag breakout — reject

[Lo, Mamaysky & Wang (2000, J. Finance)](https://www.sciencedirect.com/science/article/abs/pii/S0957417406001448)
found some chart patterns carry statistical information, but did not
establish profitability, and their kernel-smoothing detection uses
right-side (future) data — unusable for live trading. Follow-on template-
matching work (Leigh et al. 2002/2004) is fragile and thinly replicated
([survey](https://scholarworks.uno.edu/cgi/viewcontent.cgi?article=3850&context=td)).
No credible out-of-sample, costs-included evidence for a codified bull flag
was found. Detection is parameter-soup (what counts as a pole? a channel?),
so any backtest largely tests the detector, not the edge. Drop it.

### 4. Sector rotation — real evidence, wrong project

Industry momentum is well-established:
[Moskowitz & Grinblatt (1999)](https://www.anderson.ucla.edu/documents/areas/prg/asam/2019/Momentum.pdf)
documented ~0.43%/month (1963–95), and ETF-implementable versions tested
out-of-sample remain profitable
([Quantpedia sector-momentum](https://quantpedia.com/strategies/sector-momentum-rotational-system);
[TSX 60 out-of-sample validation, 2000–2025 (MDPI, 2026)](https://www.mdpi.com/1911-8074/19/1/70)).
But the effect lives at 1–6 month horizons — that's the Trading project's
territory (its factor library already has `sector_momentum.py`), not a
days-to-weeks swing bot. Including it here would duplicate the other repo
with a shorter label.

### 5. PEAD — conditional alternative, not a starter

Post-earnings-announcement drift is one of the oldest anomalies (Ball & Brown
1968; [review](https://www.sciencedirect.com/science/article/pii/S2214635020303750)),
with drift strongest in the first ~5–20 days — a genuine swing horizon. But
it has [decayed markedly in large caps in recent
decades](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/PEAD_Declined_over_time.pdf),
persists mainly in small/illiquid names where spreads are worst, and needs an
earnings-surprise data source beyond price_cache (Trading's `pead.py` is a
starting point). Park for a later milestone.

### 6. Small-account frictions (2026 state)

- **PDT rule: GONE.** SEC approved FINRA's Rule 4210 amendments 2026-04-14;
  effective 2026-06-04 the PDT designation and $25,000 minimum are eliminated,
  replaced by real-time intraday margin
  ([FINRA Regulatory Notice 26-10](https://www.finra.org/rules-guidance/notices/26-10);
  [SEC order](https://www.sec.gov/files/rules/sro/finra/2026/34-105226.pdf);
  [Schwab summary](https://www.schwab.com/learn/story/sec-approves-scrapping-25000-day-trader-minimum)).
  [Alpaca implemented the new framework 2026-06-04 and removes PDT API fields
  by 2026-07-06](https://alpaca.markets/blog/finra-retires-the-pdt-rule-introducing-alpacas-new-intraday-margin-framework/)
  — any ported code reading `daytrade_count`/`pattern_day_trader` will break.
  Same-day stop-outs no longer risk a regulatory lockout on a sub-$25k margin
  account. Cash accounts still face T+1 settlement / good-faith-violation
  rules ([FINRA on day trading](https://www.finra.org/investors/investing/investment-products/stocks/day-trading)).
- **Fractional shares on Alpaca:** market, limit, stop, and stop-limit orders
  now supported for fractional/notional quantities — but **time-in-force DAY
  only**; minimum $1 notional buys; up to 9 decimals
  ([Alpaca fractional docs](https://docs.alpaca.markets/us/docs/fractional-trading);
  [2024 limit-order announcement](https://alpaca.markets/blog/fractional-shares-trading-supports-limit-orders-and-extended-hours/)).
  DAY-only TIF means no GTC stop-losses on fractional positions — a daily
  loop must re-submit protective orders each morning, or manage exits in
  software. Not all assets are fractionable: the whole-share fallback logic
  in Trading's `fractionability.py` stays load-bearing.
- **Spread/slippage:** commission-free ≠ free. The de Groot result (§1) is
  the quantitative anchor: high-turnover strategies survive costs only in the
  most liquid names. At $100–1,000 position sizes market impact is nil, but
  crossing the spread 2×/trade at swing-trade frequency compounds fast in
  anything illiquid. Index/sector ETFs and mega-caps minimize this
  (spread magnitudes not independently sourced here — measure at build time).
  The existing MIN_DOLLAR_VOL=0 universe gap must be fixed before any stock
  strategy runs.
- **Survivorship bias:** ETFs mostly eliminate it (major index/sector ETFs
  alive throughout any realistic backtest window); stock mean reversion is
  the worst-affected strategy class since delisted crashers are precisely
  what oversold triggers buy ([Ernie Chan's standard advice: use ETFs to
  avoid survivorship bias](https://www.quantifiedstrategies.com/mean-reversion-trading-strategy/)).

---

## Ranked candidates

| # | Strategy | Verdict | One-line tradeoff |
|---|---|---|---|
| 1 | **IBS + RSI-family mean reversion on liquid index/sector ETFs** | Build first | Best replicated EOD evidence + kills survivorship problem; edge is small per trade, so execution timing (close vs next open) must be modeled honestly |
| 2 | **Trend-filtered pullback on mega-cap stocks** (close > 200MA + short-term oversold; merges Evan's #1 and #3) | Build second | Same evidence family as #1 with stock-level upside; reintroduces survivorship bias and spread cost — large-cap-only universe is mandatory |
| 3 | **PEAD swing variant** | Later milestone | Real anomaly at true swing horizons, but decayed in large caps and needs earnings data the stack doesn't cache yet |
| 4 | **Sector rotation** | Skip here | Evidence is solid but the horizon is monthly — it belongs to (and partly exists in) the Trading project |
| 5 | **Bull-flag breakout** | Reject | No credible codified, costs-included evidence; backtests would measure the pattern detector, not an edge |

## What would change this conclusion

- **Reproduction failure:** if IBS/pullback edges don't survive next-open
  execution and spread assumptions on our own price_cache backtest, the
  ranking collapses — that reproduction IS the first PRD milestone's job.
- **Practitioner-number fragility:** every CAGR quoted from
  QuantifiedStrategies/substacks is single-source; treat as hypotheses.
- **Regime dependence:** mean reversion on indices fails in sustained crashes
  without a regime/trend filter (2008-style); the 200-day-MA gate is not
  optional.
- **Broker behavior:** the intraday-margin framework is <5 weeks old
  (brokers may phase in until 2027-10-20 per FINRA 26-10) — verify actual
  Alpaca paper-account behavior before relying on it.
- **Crowding:** these are public, widely-known signals; the honest expectation
  is a modest, decaying edge — the project's value is the rigor loop, same as
  Trading.

## Sources (all accessed 2026-07-08)

- [de Groot, Huij & Zhou — Another Look at Trading Costs and Short-Term Reversal Profits (SSRN 2011 / JBF 2012)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1605049) · [EFMA PDF](https://www.efmaefm.org/0efmameetings/efma%20annual%20meetings/2011-Braga/papers/0259.pdf)
- [Quantpedia — Short-Term Reversal in Stocks](https://quantpedia.com/strategies/short-term-reversal-in-stocks)
- [NY Fed staff report 513 — Decomposing Short-Term Return Reversal](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr513.pdf)
- [Pagonidis — The IBS Effect: Mean Reversion in Equity ETFs (2013, NAAIM)](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- [arXiv 2306.12434 (2023) — IBS for trading country ETFs](https://arxiv.org/pdf/2306.12434)
- [Kinlay (2019) — The Internal Bar Strength Indicator](https://jonathankinlay.com/2019/07/the-internal-bar-strength-indicator/)
- [QuantifiedStrategies — IBS strategy](https://www.quantifiedstrategies.com/internal-bar-strength-ibs-indicator-strategy/) · [R3 strategy (2024)](https://www.quantifiedstrategies.com/larry-connors-r3-strategy/) · [Pullback backtests](https://www.quantifiedstrategies.com/pullback-trading-strategy/) · [Mean-reversion overview](https://www.quantifiedstrategies.com/mean-reversion-trading-strategy/)
- [algotr.substack — RSI2 SPY backtest](https://algotr.substack.com/p/this-simple-mean-reversion-strategy) · [quantitativo — cumulative RSI](https://www.quantitativo.com/p/squeezing-more-profits-with-cumulative)
- [Lo, Mamaysky & Wang (2000) context via pattern-recognition literature](https://www.sciencedirect.com/science/article/abs/pii/S0957417406001448) · [UNO dissertation surveying pattern predictability](https://scholarworks.uno.edu/cgi/viewcontent.cgi?article=3850&context=td)
- [Moskowitz & Grinblatt — industry momentum (UCLA copy)](https://www.anderson.ucla.edu/documents/areas/prg/asam/2019/Momentum.pdf) · [Quantpedia — sector momentum](https://quantpedia.com/strategies/sector-momentum-rotational-system) · [MDPI (2026) — TSX 60 sector rotation out-of-sample](https://www.mdpi.com/1911-8074/19/1/70)
- [MDPI (2026) — Overnight vs. daytime returns across sector ETFs](https://www.mdpi.com/2227-9091/14/4/84)
- [Columbia CEASA — Why Has PEAD Declined Over Time?](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/PEAD_Declined_over_time.pdf) · [PEAD review (2020, ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2214635020303750) · [Quantpedia — Post-Earnings Announcement Effect](https://quantpedia.com/strategies/post-earnings-announcement-effect)
- [FINRA Regulatory Notice 26-10 — PDT elimination, effective 2026-06-04](https://www.finra.org/rules-guidance/notices/26-10) · [SEC approval order 34-105226 (2026-04-14)](https://www.sec.gov/files/rules/sro/finra/2026/34-105226.pdf) · [Schwab explainer](https://www.schwab.com/learn/story/sec-approves-scrapping-25000-day-trader-minimum) · [Alpaca — new intraday margin framework](https://alpaca.markets/blog/finra-retires-the-pdt-rule-introducing-alpacas-new-intraday-margin-framework/)
- [FINRA — day trading / cash account settlement basics](https://www.finra.org/investors/investing/investment-products/stocks/day-trading)
- [Alpaca docs — fractional trading](https://docs.alpaca.markets/us/docs/fractional-trading) · [Alpaca blog — fractional limit orders & extended hours (2024)](https://alpaca.markets/blog/fractional-shares-trading-supports-limit-orders-and-extended-hours/)
