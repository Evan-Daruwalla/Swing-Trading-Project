# Research brief — Exhaustive catalog of swing-trading ideas with genuine merit

**Swing Trading project · 2026-07-10 · Evan Daruwalla**

**Question this answers:** what is the *complete* space of swing-trading
strategies with real (academic or robustly-documented) merit, and — cross-
referenced against this project's 13 pre-registered experiments (E1–E12) —
which are already falsified here versus **genuinely untested with merit**?
**Decision it feeds:** whether any remaining idea is worth a new
pre-registration, or whether the search space is exhausted.

Scope filter applied throughout: swing horizon (holds days–weeks), EOD-
codifiable, retail-scale ($100–1,000), long-biased (short side noted but
deprioritized per prior program findings). "Merit" = ≥1 peer-reviewed source
OR a robustly-replicated effect; vendor/blog backtests are tagged as such and
discounted.

---

## TL;DR (verdict first)

Across ~40 documented swing ideas, **the vast majority are already falsified
here, already decayed in the literature, out of the EOD/retail scope, or
income-overlays rather than return engines.** After removing those, **five
ideas are genuinely untested in this project AND carry real evidence AND fit
the horizon** — but note honestly that *four of the five are cross-sectional
diversified constructs, not the concentrated high-return single-name bets the
project's goal wanted, and the project's own fill-timing ablation (54% of
mean-reversion edge lives in the overnight gap) is direct counter-evidence
against the reversal-family candidates.* Ranked shortlist:

1. **Cross-sectional short-term reversal** (weekly, large-cap, cost-optimized) — de Groot/Huij/Zhou.
2. **Earnings-announcement premium** (buy *before* scheduled earnings) — Frazzini/Lamont; distinct from the FAILED E10 (post-earnings).
3. **Short-interest / days-to-cover** screen (avoid/short high-DTC) — Hong/Li/Ni.
4. **Diversified cross-sectional / sector momentum** (not the FAILED concentrated E3) — Jegadeesh-Titman / Moskowitz-Grinblatt.
5. **Turn-of-the-month overlay** — small but robust and nearly free — McConnell/Xu.

The high-return-AND-robust-AND-retail-EOD cell remains empty; these are
"real but small / diversified / risk-managed" edges, consistent with the
program's 0/13 conclusion.

---

## The full catalog (grouped; each tagged)

Tags: **[KILLED-HERE]** already falsified by an experiment · **[ADJACENT-KILLED]**
a near-variant was falsified · **[DECAYED]** literature says the edge is gone ·
**[OUT-OF-SCOPE]** not EOD / not retail / wrong horizon · **[OVERLAY]** risk or
income tool, not a return engine · **[UNTESTED-MERIT]** genuinely open here.

### A. Mean-reversion family
1. **IBS (internal bar strength)** — buy close near low, exit on reversion.
   **[KILLED-HERE: E1/E1b/E2]** Sharpe 0.23, and the fill-timing ablation
   proved 54% of the edge is in the un-catchable overnight gap.
2. **RSI(2) with 200-day trend filter (Connors)** — buy RSI2<5 above the
   200-DMA, exit above 5-DMA. Vendor backtests claim ~9–27%/yr on SPY but
   these are un-cost-realistic and in-sample
   ([QuantifiedStrategies](https://www.quantifiedstrategies.com/rsi-2-strategy/)).
   **[ADJACENT-KILLED]** — same short-term-index-MR family as E1/E12; our
   ablation is direct counter-evidence. The *only* untested wrinkle is the
   explicit 200-DMA regime filter, which E1 lacked. Low-priority retest.
3. **Bollinger-band mean reversion** — buy lower band, exit mid. **[ADJACENT-KILLED]** same family.
4. **Confirmed-capitulation MR ("right side of the V")** — **[KILLED-HERE: E12]** −4.71%; confirmation surrenders the overnight pop.
5. **Deep-dip "never book a loss"** (buy ≤0.80×ATH, +15% target, no stop) — **[KILLED-HERE: E9]** claim literally true, still 3.5%/yr with a −80% unrealized tail.
6. **Cross-sectional short-term reversal (weekly)** — long past-week losers,
   short winners, in **large caps** with turnover/cost optimization. De Groot,
   Huij & Zhou (2012, *J. Banking & Finance*) show **30–50 bps/week net of
   costs** once you avoid small caps
   ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963131)).
   **[UNTESTED-MERIT]** — genuinely distinct from E1 (cross-sectional, weekly,
   large-cap-cost-aware, not single-name daily IBS). Strongest reversal
   candidate; caveat: it's a long-short market-neutral construct in the paper.
7. **Short-term residual reversal** — reversal on factor-residual returns;
   Blitz, Huij & Martens report it is stronger and more stable than raw
   reversal ([EFMA PDF](https://www.efmaefm.org/0EFMSYMPOSIUM/2012/papers/017_update.pdf)).
   **[UNTESTED-MERIT]** but needs a factor model → heavier build.

### B. Trend / momentum family (time-series)
8. **200-day-MA leverage rotation (3×)** — **[KILLED-HERE: E4/E5/E7]** 93% drawdown out-of-regime.
9. **1× MA rotation** — **[KILLED-HERE→OVERLAY: E6]** works as a market-dependent drawdown overlay, ≈ index return, not high-return.
10. **Time-series momentum, 12-month (Moskowitz-Ooi-Pedersen 2012)** — SR ≈1.28,
    but across **58 futures** (equities/bonds/FX/commodities), and shines in
    2008 via short + cross-asset legs
    ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304405X11002613)).
    **[OUT-OF-SCOPE]** equity-only = E6; the edge that makes it great needs
    futures/shorting we don't have.
11. **MA crossover (EMA 9/13/50)** — **[ADJACENT-KILLED]** trend timing adds no return (E4/E6 lesson).
12. **Dual momentum / GEM (Antonacci)** — absolute+relative, 12-mo lookback,
    monthly ([Optimal Momentum](https://www.optimalmomentum.com/dual-relative-absolute-momentum/)).
    **[OUT-OF-SCOPE (horizon)]** — monthly rebalance is position-trading, not
    swing; and it's a risk-managed core, not high-return.

### C. Cross-sectional stock-selection
13. **Concentrated stock momentum (top-3, 63-day)** — **[KILLED-HERE: E3]** 6.3% vs 15%, lost to buy-hold even survivorship-flattered.
14. **Diversified cross-sectional momentum (Jegadeesh-Titman)** — the classic
    3–12mo winners-minus-losers. **[UNTESTED-MERIT (with caveat)]** — E3
    killed the *concentrated* version; a *diversified* long-only decile is
    untested here, but the horizon (3–12mo hold) is position-trading and the
    factor has decayed/crashed post-2000. Marginal.
15. **52-week-high momentum (George-Hwang 2004)** — rank by price/52wk-high;
    0.60–0.94%/mo, robust in 18/20 markets, doesn't reverse
    ([J. Finance](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00695.x)).
    **[UNTESTED-MERIT (horizon caveat)]** — 6–12mo hold, borderline swing.
16. **Residual momentum (Blitz-Huij-Martens 2009)** — ~2× risk-adjusted vs
    total-return momentum ([Robeco](https://www.robeco.com/en-us/about-us/key-strengths/quant/our-most-important-quant-papers)).
    **[UNTESTED-MERIT]** but factor-model build + position horizon.
17. **Industry/sector momentum (Moskowitz-Grinblatt 1999)** — rotate into
    strongest sectors. **[UNTESTED-MERIT]** — distinct from E4/E6 (those were
    single-index time-series timing, not cross-sectional sector selection).
    Codifiable on the 11 SPDR sectors already in the universe.
18. **Low-volatility anomaly (Blitz-van Vliet 2007)** — ~12%/yr alpha spread,
    but a multi-year holding-period effect ([ResearchGate](https://www.researchgate.net/publication/4781460_The_Volatility_Effect_Lower_Risk_without_Lower_Return)). **[OUT-OF-SCOPE (horizon)]**.
19. **Short-interest / days-to-cover** — high DTC predicts low returns; Hong,
    Li & Ni report a long-short **Sharpe ≈1.3**, monthly
    ([NBER w21166](https://www.nber.org/system/files/working_papers/w21166.pdf));
    Asquith et al. corroborate ([NBER w10434](https://www.nber.org/system/files/working_papers/w10434.pdf)).
    **[UNTESTED-MERIT]** — data is free (FINRA bi-monthly short interest);
    retail angle = avoid/short high-DTC names or long low-SI. Weeks horizon.

### D. Event-driven / catalyst
20. **Post-earnings-announcement drift (PEAD)** — **[KILLED-HERE: E10]** 5.9% vs 15%; real-but-small and decayed after ~2010.
21. **Earnings-announcement premium (Frazzini-Lamont 2007)** — stocks rise
    *around scheduled* earnings; buy a few days before, exit after; driven by
    attention-buying, hard to arb ([NBER w13090](https://www.nber.org/papers/w13090)).
    **[UNTESTED-MERIT]** — genuinely distinct from E10 (this is *pre*-
    announcement, PEAD is *post*), swing-horizon, and buildable on the same
    earnings-date infra E10 already fetched. Caveat: it's a small diversified
    premium, not a concentrated bet.
22. **Index reconstitution (S&P add/delete front-run)** — **[DECAYED]**
    Greenwood & Sammon: the effect fell from 7.4% (1990s) to **<1%** last
    decade — "the disappearing index effect"
    ([J. Finance 2025](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13410)).
23. **Merger arbitrage** — collect the deal spread. Real but **4.4%/yr
    1998–2022, ~200bp over risk-free**, with a fat left tail on breaks
    ([Return Stacked](https://www.returnstacked.com/merger-arbitrage/)).
    **[OUT-OF-SCOPE / LOW-RETURN]** — deal-data-gated, not high-return.
24. **Buyback / insider-buying / analyst-revision / spinoff / lockup drifts** —
    each has documented drift but all are **data-gated** (need corporate-action
    or estimate feeds) and mostly diversified/small. **[OUT-OF-SCOPE (data)]**.
25. **Biotech/FDA binary events** — **[OUT-OF-SCOPE]** not systematically EOD-codifiable; lottery risk.

### E. Seasonality / calendar
26. **Turn-of-the-month (McConnell-Xu 2008)** — returns concentrate in the
    ~4-day month-turn; **0.45%/mo alpha**, robust in 31/35 countries, strongest
    in the *recent* sub-sample ([FAJ](https://www.tandfonline.com/doi/abs/10.2469/faj.v64.n2.11)).
    **[UNTESTED-MERIT]** — trivially EOD-codifiable, nearly free (in-market
    ~20% of days). Small alone; best as a filter/overlay.
27. **Sell-in-May / Halloween, Santa rally, day-of-week, holiday** —
    documented but small and mostly **[OVERLAY]**; weak standalone.

### F. Overnight / microstructure
28. **Overnight return anomaly (buy close, sell open)** — nearly all equity
    gains accrue overnight; intraday ≈ flat
    ([Lou-Polk-Skouras "Tug of War"](http://www.econ.yale.edu/~shiller/behfin/2015-04-11/lou_polk_skouras.pdf)).
    **[ADJACENT-KILLED / COST-FATAL]** — our A3 screen (overnight-only IBS)
    was dead; two real overnight ETFs (NSPY/NIWM, 2022) died within a year;
    "probably would not cover transaction costs" ([Falkenblog](https://efalken.substack.com/p/the-equity-overnight-anomaly-etfs)).

### G. Sentiment / flow
29. **Sentiment extremes (AAII, put/call)** — contrarian overlay, weak alone. **[OVERLAY]**.
30. **Short-squeeze setups** (high SI + catalyst) — the retail face of #19; discretionary, hard to codify cleanly. **[UNTESTED but low-confidence]**.
31. **Google-Trends / options-flow / alt-data** — **[OUT-OF-SCOPE (data / not EOD)]**.

### H. Volatility / options structures
32. **Covered calls / short-vol (volatility risk premium)** — real premium but
    an **[OVERLAY]** that reshapes the distribution (caps upside for income),
    not a directional swing return engine; options-gated.
33. **Earnings vol crush (short straddle into earnings)** — options, not EOD-directional. **[OUT-OF-SCOPE]**.

---

## Ranked shortlist — genuinely untested here, with merit, in-scope

| # | Idea | Evidence | Horizon | Build cost | Honest caveat |
|---|---|---|---|---|---|
| 1 | **X-sectional short-term reversal** (weekly, large-cap, cost-opt) | de Groot 2012: 30–50bps/wk net | ~1 wk | Medium (rank+cost model) | Long-short in the paper; retail long-only differs; MR family that died on the gap here |
| 2 | **Earnings-announcement premium** (buy pre-earnings) | Frazzini-Lamont 2007 | days | Low (reuse E10 earnings infra) | Small diversified premium, not concentrated; distinct from FAILED E10 |
| 3 | **Short-interest / days-to-cover** screen | Hong-Li-Ni SR≈1.3 | weeks | Medium (FINRA SI data) | Best as short/avoid; long side weaker |
| 4 | **Diversified sector momentum** (11 SPDRs) | Moskowitz-Grinblatt 1999 | 1–3 mo | Low (universe in hand) | Position-horizon; concentrated version already FAILED (E3) |
| 5 | **Turn-of-the-month overlay** | McConnell-Xu 2008: 0.45%/mo | 4 days/mo | Trivial | Small; a filter, not a standalone engine |

Everything else is **KILLED-HERE, ADJACENT-KILLED, DECAYED, OUT-OF-SCOPE, or
OVERLAY** — see tags above.

## What would change the conclusion
- If candidate #1 or #2 **passes** a pre-registered 2000–2013 gate *after*
  realistic costs and next-open execution — that would be the program's first
  survivor. Prior is low: #1 is a reversal (the family that died on the gap),
  #2 is a small diversified premium unlikely to clear a 15% CAGR bar
  concentrated.
- If a **data source** opens (point-in-time estimates, corporate actions,
  intraday) several **[OUT-OF-SCOPE (data)]** ideas become testable.
- The honest base rate after 13 pre-registered failures argues these will
  also fall short of the *high-return* bar, though #1/#3/#4 could plausibly
  clear a *risk-adjusted* (Sharpe) bar the goal never asked for.

## Sources (dated)
- de Groot, Huij, Zhou — *Another Look at Trading Costs and Short-Term Reversal Profits* (2012, JBF) — [SSRN 1963131](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963131)
- Blitz, Huij, Martens — *Short-Term Residual Reversal* (2012) — [EFMA](https://www.efmaefm.org/0EFMSYMPOSIUM/2012/papers/017_update.pdf); *Residual Momentum* (2009) — [Robeco](https://www.robeco.com/en-us/about-us/key-strengths/quant/our-most-important-quant-papers)
- Frazzini, Lamont — *The Earnings Announcement Premium and Trading Volume* (2007) — [NBER w13090](https://www.nber.org/papers/w13090)
- George, Hwang — *The 52-Week High and Momentum Investing* (2004, J. Finance) — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00695.x)
- Moskowitz, Ooi, Pedersen — *Time Series Momentum* (2012, JFE) — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304405X11002613)
- Hong, Li, Ni — *Days to Cover and Stock Returns* (2015) — [NBER w21166](https://www.nber.org/system/files/working_papers/w21166.pdf); Asquith et al. — *Short Interest and Stock Returns* — [NBER w10434](https://www.nber.org/system/files/working_papers/w10434.pdf)
- Greenwood, Sammon — *The Disappearing Index Effect* (2025, J. Finance) — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13410) / [NBER w30748](https://www.nber.org/system/files/working_papers/w30748.pdf)
- McConnell, Xu — *Equity Returns at the Turn of the Month* (2008, FAJ) — [T&F](https://www.tandfonline.com/doi/abs/10.2469/faj.v64.n2.11)
- Lou, Polk, Skouras — *A Tug of War: Overnight vs Intraday Expected Returns* — [PDF](http://www.econ.yale.edu/~shiller/behfin/2015-04-11/lou_polk_skouras.pdf); Falkenstein — *The Equity Overnight Anomaly ETFs* — [Falkenblog](https://efalken.substack.com/p/the-equity-overnight-anomaly-etfs)
- Antonacci — *Dual Momentum / GEM* — [Optimal Momentum](https://www.optimalmomentum.com/dual-relative-absolute-momentum/)
- Merger-arb return figures — [Return Stacked](https://www.returnstacked.com/merger-arbitrage/)
- Connors RSI(2) (vendor backtest, discounted) — [QuantifiedStrategies](https://www.quantifiedstrategies.com/rsi-2-strategy/)
