# Research brief — Alternative & premium data: cost-benefit for a $100–1,000 swing bot

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Question:** if Evan spent a modest data budget, which specific blocked/untested
experiments become testable, at what cost, and is the documented edge worth it at
$100–1,000 — across options-derived, short-side/positioning, fundamental/estimate/
event, and exotic alt-data feeds? **Audience:** the operator + any future model
executing the PRD.

---

## TL;DR (verdict first)

**Two findings dominate. (1) The E17 "wall" is real for *deep* history but
overstated: FINRA now publishes FREE, official, exchange-listed consolidated short
interest from June 2021 — so E17 days-to-cover is runnable *free, right now* as a
~5-year modern out-of-sample test.** (2) **Almost every genuinely strong alt-data
edge is either institutional-priced, borrow-fee-illusory, or concentrated in illiquid
names the liquidity floor forbids** — and one satellite study literally documents
retail investors as the *harvested counterparty*. The single most decisive cross-cut:
Muravyev-Pearson-Pollet (2025, JFE) show the classic option-implied signals (IV
spread, skew) predict returns mostly because **they proxy the stock borrow fee** —
exclude hard-to-borrow names and predictability drops **≥ two-thirds**, i.e. the edge
lives exactly where a floored small account can't trade. If Evan spends one budget
dollar on data, it should be **Ortex Advanced (~$129/mo, one month)** — the only
retail feed that proxies *both* short-interest (E17) and the strongest short-side
signal, the **loan-fee anomaly** (Engelberg et al.: 4.01%/mo long-short, the single
best return predictor vs 102 anomalies). But prove the concept **free first**.

---

## Method
4 parallel agents (options-derived, short-side/positioning, fundamental/estimate/
event, exotic panels), primary-source-graded, every feed tagged FREE vs PAID with
$/mo, mapped to the liquidity floor + EOD + K=1–3 constraints and the specific
FAIL/BLOCKED items (E10/E15/E17). Budget framing: "$100–1,000" is *trading* capital,
so any $/mo feed is scoped as "buy one month, validate the backtest, cancel" — a
research cost, never a standing operating cost until capital is 10–50× larger.

---

## Findings

### Short-side & positioning (AD2) — the highest-value family, and it's partly free
- **E17 is partially unblocked FREE.** FINRA's own note: pre-June-2021 free short
  interest is OTC-only, **but exchange-listed consolidated short interest is free from
  June 2021 onward** (biweekly). → ~5 years of real settlement-date SI to run E17
  days-to-cover as a modern OOS test at zero cost (thin cadence, short window).
- **Reg SHO daily short-volume (free, 2009+)** supports a *different* test — a
  Diether-Lee-Werner / Boehmer-Jones-Zhang daily-short-flow drift — with real [PR]
  backing (BJZ: heavily-shorted underperform ~1.16%/20d). Caveats: it's *executed
  short volume* (contaminated by market-maker hedging), off-exchange unless you
  consolidate each exchange's file, and ≠ short interest.
- **Borrow-fee / loan-fee is the strongest short-side edge** (Engelberg-Evans-
  Leonard-Reed-Ringgenberg: **4.01%/mo long-short, Sharpe 0.66, 42% unique** vs 102
  anomalies) — but true Markit/S3 data is institutional-priced. **Ortex Advanced
  (~$129/mo)** is the only retail route to a *proxied* (estimated) version, and it
  bundles estimated SI + cost-to-borrow + utilization — one feed covers E17 *and* the
  loan-fee bet.
- 13F (free, 45-day lag → too slow), failures-to-deliver (free, niche/small-cap),
  COT (free, index-level only → out of scope for single-name K=1–3).

### Options-derived (AD1) — mostly gated, illusory, or vendor hype
- **Governing debunk:** Muravyev-Pearson-Pollet (2025, JFE) — IV-spread/skew signals
  are ~2/3 a **borrow-fee proxy**; exclude hard-to-borrow names → predictability
  drops ≥ two-thirds. The edge is in the illiquid names the floor excludes.
- The real single-name signals need **paid, gated data**: Pan-Poteshman signed
  put/call requires Cboe Open-Close (**$24k/yr**); Xing-Zhang-Zhao skew needs
  OptionMetrics/ORATS (paid). **O/S ratio** (Johnson-So, ~0.34%/wk) is the one
  *plausibly* free-buildable single-name signal at swing horizon — but free option-
  volume is snapshot-quality (point-in-time risk) and the edge is borrow-fee-loaded.
- **Free but redundant/wrong-shape:** aggregate Cboe put/call (weak sentiment gauge);
  VIX term structure = E18 already; variance risk premium (Bollerslev-Tauchen-Zhou —
  real but *quarterly, market-level*).
- **Vendor hype — do not pay:** unusual options flow (Unusual Whales/FlowAlgo — no
  peer-reviewed support, intraday by nature); GEX/dealer positioning (a *volatility*
  modifier mis-sold as directional; academic support is intraday); 0DTE (balanced
  flow, no next-day propagation).

### Fundamental / estimate / event (AD3) — the cheapest real unblock is a $22 feed
- **Analyst recommendation-CHANGE drift (Womack)** beats numeric estimate-revision
  drift *as a first cheap test*, purely because a rating change is an **event with a
  date** (no point-in-time consensus snapshot needed). **FMP Starter ($22/mo, one
  month)** gives event-dated grades cleanly — the cheapest clean event-driven test
  available.
- **Estimate-revision drift (Gleason-Lee)** is better-documented and *still alive*
  (Mill Street: 7.6 pp/yr spread, t=2.93, through Jan-2023) — but the numeric version
  needs a **timestamped consensus history**; cheap feeds (FMP/Finnhub) backfill and
  restate silently → look-ahead contamination. Clean PIT consensus = I/B/E/S (4–5
  figures / WRDS-academic-only).
- **The E15 look-ahead fix is free with discipline:** use FMP's *confirmed*
  earnings-date endpoint and freeze the date as-of the pre-event decision; don't trust
  a projected date that could be backfilled.
- **PIT-fundamentals trap:** yfinance serves only current/restated data for the
  currently-listed universe → survivorship *and* look-ahead. Prefer event-dated
  signals; never build a fundamentals-time-series signal on yfinance and call the
  backtest honest.
- **Escalation path (a relationship, not a purchase):** a **university WRDS login**
  (I/B/E/S + Compustat PIT, free to a student) is the only clean way to properly
  unblock this family — worth flagging for Evan.

### Exotic panels (AD4) — institutional-only, retail is the exit liquidity
- The strongest, cleanest edges are the *most* unaffordable: **credit-card/
  transaction panels** ($100k–1M+/yr — the best documented alt-data edge) and
  **satellite parking lots** ($50k–500k/yr + a geospatial team). The Berkeley/RS
  Metrics satellite study explicitly documents **retail investors as the losing
  counterparty** being harvested by the funds that own the data.
- "Retail tiers" (SimilarWeb ~$125–199/mo, Sensor Tower) are still 1.5–24× the whole
  account *and* aren't the point-in-time feeds that produced the peer-reviewed alpha —
  **vendor-hype for return prediction.** RavenPack's cheap tool is a chat product, not
  the tradable feed.
- The only genuinely $0 sources are the two weakest/most-hazardous: **self-scraped
  e-commerce data** (soft, slow, US-evidence-thin, heavy plumbing) and **social
  sentiment** (manipulation-laden, mostly intraday, strongest in the illiquid meme
  names the floor excludes — same trap as the already-probed Google-Trends/FEARS).

---

## Ranked recommendation

| Priority | Action | Cost | Why |
|---|---|---|---|
| 1 | **Run E17 days-to-cover FREE** on FINRA official exchange-listed SI, 2021→2026 | $0 | The wall is partly gone; prove the concept before paying |
| 2 | **Free Reg SHO daily short-volume drift** test (BJZ lineage) | $0 | Deep (2009+), daily, single-name, real academic backing |
| 3 | **Analyst recommendation-change drift** via FMP Starter (one month) | ~$22 | Cheapest clean *event-dated* test; also fixes the E15 confirmed-date concern |
| 4 | **If 1–3 promising: Ortex Advanced** (one month) for the loan-fee/utilization signal | ~$129 | The strongest short-side edge (4.01%/mo), higher-alpha than raw SI |
| — | **Do not pay:** options-flow vendors, GEX, SimilarWeb/exotic panels | — | No peer-reviewed edge / intraday / illiquid-concentrated / unaffordable |
| — | **Escalate (free-via-relationship):** university WRDS for I/B/E/S + Compustat PIT | $0* | The only clean unblock of the estimate-revision + PIT-fundamentals family |

**The honest caveat on all of it:** every documented edge here concentrates in
**low-coverage, small, illiquid, hard-to-borrow** names — exactly where the mandatory
liquidity floor forbids trading. A clean test on a *liquid* universe may simply show
the edge already arbitraged, same family as the E10/E15 kills. Pre-register with that
prior.

## What would change the conclusion
- A free/cheap test (E17-2021+, Reg SHO, or FMP recommendation drift) clearing the
  gate on a liquid universe after 5 bps.
- Access to a university WRDS login (unblocks I/B/E/S estimate revisions + PIT
  fundamentals cleanly).
- Capital scaling 10–50× so a $22–129/mo feed becomes a rational standing cost.

## Sources (dated)
- Muravyev, Pearson, Pollet — *Why Does Options Market Information Predict Stock Returns?* (2025, JFE) — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304405X25001618)
- Engelberg, Evans, Leonard, Reed, Ringgenberg — *The Loan Fee Anomaly* — [SSRN 3707166](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3707166)
- Boehmer, Jones, Zhang — *Which Shorts Are Informed?* (2008, JF); Diether, Lee, Werner — *Short-Sale Strategies and Return Predictability* (2009, RFS) — [PDF](https://diether.org/papers/short_strategies.pdf)
- FINRA — [Equity Short Interest](https://www.finra.org/finra-data/browse-catalog/equity-short-interest/files) · [Reg SHO daily volume](https://www.finra.org/finra-data/browse-catalog/short-sale-volume-data/daily-short-sale-volume-files) (accessed 2026-07-13)
- Pan & Poteshman — *The Information in Option Volume for Future Stock Prices* (2006, RFS); Johnson & So — *The Option to Stock Volume Ratio* (2012, JFE); Xing, Zhang, Zhao — *IV Smirk* (2010, JFQA)
- Womack — *Do Brokerage Analysts' Recommendations Have Investment Value?* (1996, JF) — [SSRN 5639](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5639); Gleason & Lee — *Analyst Forecast Revisions and Market Price Discovery* (2003, Acct Rev) — [SSRN 370425](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=370425); Mill Street Research (2023)
- Katona, Painter, Patatoukas, Zeng — satellite parking-lot study (RS Metrics) — [Haas](https://newsroom.haas.berkeley.edu/how-hedge-funds-use-satellite-images-to-beat-wall-street-and-main-street/); Gupta, Leung, Roscovan — card-transaction study (2022, JPM)
- Ortex pricing — [public.ortex.com](https://public.ortex.com/a-new-pricing-structure-for-ortex/); FMP pricing — [site](https://site.financialmodelingprep.com/pricing-plans) (accessed 2026-07-13)
