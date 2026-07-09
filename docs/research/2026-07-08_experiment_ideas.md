# Experiment ideas — Swing Trading project (2026-07-08, pre-council)

> **OUTCOME (2026-07-08):** /llm-council selected the program from this list —
> see record Appendix B. Wave 0: #29/#30/#28 (infra). Wave 1 (backtest):
> pre-registration for #1, then #15+#13 fill-timing ablation, then #1 with
> #27 side-check. Wave 2 (live, gated): #1 + #15-residual + #28. Deferred:
> #17/#18/#20/#2/#4/#11/#5. Dropped: the other 16.

Brainstorm feeding an /llm-council selection. Context: systematic swing bot
(days–weeks holds), $100–1,000 capital, EOD yfinance price_cache (~5,200 US
tickers, split-adjusted/dividend-UNadjusted), Alpaca PAPER, infra portable
from `D:\ClaudeCode\Trading`. Evidence base: research brief
`2026-07-08_small-account-swing-strategies.md` (IBS/RSI mean reversion on
ETFs ranked #1; trend-filtered pullback on mega-caps #2; bull flag rejected;
PDT rule eliminated 2026-06-04; Alpaca fractional = DAY-TIF only).

## A. Strategy-edge experiments

1. **ETF IBS mean reversion** — buy liquid index/sector ETF when IBS < 0.2,
   exit IBS > 0.8 or time stop. Direct Pagonidis replication on our data.
2. **RSI(2)/R3-style oversold ETF entries** — RSI(2) stacked-decline entry
   above the 200-day MA, exit on RSI strength (Connors family).
3. **Cumulative RSI(2)** — 2-day cumulative RSI below threshold; fewer,
   deeper signals than #2.
4. **IBS × RSI double filter** — require both oversold; tests whether signal
   intersection beats either alone.
5. **Trend-filtered pullback on mega-caps** — close > 200MA, close < 20MA,
   RSI(5) < 45; exit RSI(5) > 65. The codified merge of Evan's trend-pullback
   + mean-reversion candidates.
6. **Large-cap weekly short-term reversal** — buy prior-week losers within
   S&P-500-class names only (de Groot cost finding), hold ~1 week.
7. **Bollinger %B extreme + up-day confirmation** — enter only after the
   first positive close following a %B < 0 day; tests confirmation value.
8. **Gap-down reversion in uptrending large caps** — overnight gap ≤ −X% with
   close > 200MA; buy next open (or near close), exit N days.
9. **N-consecutive-down-days washout** — e.g. 4+ red days in an uptrend;
   simplest possible MR signal as a baseline.
10. **Multi-day RSI ladder scaling** — add a tranche each extra oversold day
    (tests scaling-in vs all-at-once).
11. **VIX-regime gate on MR** — same entries, skip when VIX above threshold
    (or size down); practitioner sources claim it removes worst drawdowns.
12. **Sector-relative pullback** — MR entries only in stocks/ETFs of
    top-momentum sectors; hybrid of pullback + sector rotation.
13. **Overnight-premium harvest** — buy close / sell next open on ETFs after
    low-IBS days; isolates the overnight component the literature says
    carries the effect.
14. **Country-ETF IBS** — replicate arXiv 2306.12434 basket; diversifies away
    from US-only regime.

## B. Execution experiments

15. **Execution-timing A/B** — identical signals run as two paper sleeves:
    next-open fills vs ~3:55pm near-close fills (Alpaca real-time quote
    approximation). Directly prices the overnight-component haircut.
16. **Limit-at-signal vs market entry** — resting limit at signal-day close
    vs market at open: fill rate vs per-fill edge.
17. **Exit-rule ablation** — time stop (N days) vs signal exit (IBS > 0.8 /
    RSI > 65) vs first-up-close, same entries.
18. **Stop-loss ablation on MR** — with vs without hard stops; literature
    suggests stops structurally hurt mean reversion — measure it.
19. **Fractional vs whole-share tracking error** — same sleeve mirrored both
    ways at $500; quantifies how load-bearing fractionability really is.

## C. Risk & sizing experiments

20. **Equal-weight vs ATR-volatility-targeted sizing** at $100–1,000.
21. **Concurrency sweep** — max 1 vs 3 vs 5 simultaneous positions at $500;
    concentration vs opportunity cost at tiny capital.
22. **Capital-floor stress** — same strategy at $100 vs $1,000 sleeves; finds
    where minimum-notional/whole-share rounding destroys the edge.

## D. LLM-overlay experiments (three-arm design ported from Trading)

23. **LLM veto on MR entries** — control vs cash-veto vs cascade arms at
    daily cadence; does an LLM reading the chart/context improve entries?
24. **LLM regime classifier** — daily market-state call (trend/chop/stress)
    gating which strategy family trades.
25. **LLM news-check on crash buys** — MR buys panicking stocks; LLM checks
    headlines for the *reason* (bankruptcy/fraud/dilution = veto, sympathy
    panic = allow). Highest-plausibility LLM edge since MR's known failure
    mode is catching justified knives.
26. **Mechanical earnings-date filter** — skip entries within N days of
    earnings (no LLM; needs an earnings calendar source). Baseline for #25.

## E. Infrastructure / methodology experiments

27. **Survivorship-bias bound** — same stock strategy on (a) full current
    universe vs (b) ETFs-only vs (c) mega-caps-always-listed; brackets how
    much the bias flatters stock results.
28. **DB-sim vs Alpaca-paper divergence tracking** — run the mirror from day
    one and log fill-price divergence per trade; produces a real slippage
    estimate instead of an assumption.
29. **Frozen-regression tripwire port** — pin 2 short windows × N strategies
    to reference numbers (d=±0.0000pp pattern) before any strategy iteration
    begins.
30. **Same-day coverage gate** — port Trading's publication-count gating to
    the daily loop before any signal fires on partial data.
