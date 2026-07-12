# Research brief — Strategies from other data types (beyond daily OHLCV)

**Swing Trading project · 2026-07-12 · Evan Daruwalla**

**Question:** what strategy families become testable if the project uses data
*types* beyond its daily OHLCV (prices/volume) feed — and which of those are
actually retrievable free at retail, today, with enough history for the
program's regime-spanning discipline? **Decision it feeds:** whether M7
(E13–E17) gets additional candidates or a follow-on arc.

Every availability claim below was **probed live on 2026-07-12**
(`probe_datatypes.py` run against yfinance + FRED endpoints) or is sourced;
nothing is assumed.

---

## TL;DR

Six new data types are genuinely available free; three more are hard-blocked.
The available ones skew heavily toward **regime gates and overlays, not
return engines** — same shape as the OHLCV conclusion (0/13). The two
standouts: (1) the **VIX complex** (probed: VIX to 1990, VIX3M to 2006,
VVIX/SKEW too) enables a pre-registrable **term-structure regime gate** on
existing sleeves; (2) **EDGAR Form 4 insider filings** carry the strongest
*academic* anomaly of any new type (opportunistic insider buys ≈ 82 bps/mo,
Cohen-Malloy-Pomorski) but need a heavy parsing build and inherit a
price-side survivorship caveat. Breadth is self-computable from data already
cached. Options/IV history, short-interest history, and historical news
sentiment are **BLOCKED-ON-DATA** at $0 — the honest boundary of this
project's data budget.

---

## Probed availability (facts, 2026-07-12)

| Data type | Source | Probe result |
|---|---|---|
| VIX (30d IV) | yfinance `^VIX` | **1990-01-02 → present** (9,198 bars) |
| VIX3M (93d IV) | yfinance `^VIX3M` | **2006-07-17 → present** |
| VIX9D / VVIX / SKEW | yfinance | 2011+ / 2007+ / **1990+** |
| Dividend calendar | yfinance `.dividends` | SPY: 135 events, 1993→2026 |
| Yield curve (T10Y2Y) | FRED keyless CSV | **1976 → present** (13,074 rows) |
| Initial claims (ICSA) | FRED keyless CSV | 1967 → present |
| HY credit spread (BAMLH0A0HYM2) | FRED keyless CSV | endpoint works; default window ~3yr, full series (1996→) needs `cosd` date param |
| Market breadth | **self-computed** from own cache | 107 cached tickers → % above 200DMA / A/D computable: YES |
| Options chains / IV history | yfinance | **current chains only — NO history. BLOCKED at $0** |
| Short-interest history | yfinance | snapshot only (`shortRatio`) — history = E17's pending FINRA probe |
| Historical news / sentiment | — | no free point-in-time archive; forward-only (M3 LLM overlay) |
| Google Trends | free | exists, but normalized/sampled/rescaled per request — reproducibility hazard; not probed further |
| Insider Form 4 | SEC EDGAR | free, point-in-time by filing date; **build-heavy** (XML parsing, years of filings) |

## Strategy candidates by data type

### 1. VIX term-structure regime gate — best new candidate
Mechanism: implied-vol term structure (VIX/VIX3M) inverts (backwardation)
under near-term fear; contango = calm. Documented as a risk-on/off timing
signal by practitioners and an academic ML study
([Raven Quant](https://ravenquant.com/vix-term-structure/),
[PMC walk-forward study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11029606/),
[Cboe](https://www.cboe.com/tradable-products/vix/term-structure/)).
Testable here as: hold equity sleeve only while VIX/VIX3M < 1 (or < 0.95),
cash otherwise — an *a-priori-knob* regime gate in the E7 vol-gate spirit,
EOD, data in hand. **Honest limits:** VIX3M starts 2006 → the 2000-02 crash
is out of window (only 2008/2020/2022 available — weaker than the program's
usual gate window); and it's an **overlay** (defends drawdown), not a return
engine — the E6/E7 arc already showed how such gates fail to add return.
**Verdict: testable now; prior = risk-management value, not high return.**

### 2. Self-computed market breadth (regime filter / thrust)
% of universe above 200DMA and advance/decline computed from our own 107
cached series — zero new data risk. The Zweig Breadth Thrust claim (rare
signal, +20% avg 12mo after) is practitioner-sourced with **N < 30 signals
since 1950** — statistically fragile, position-horizon
([QuantifiedStrategies](https://www.quantifiedstrategies.com/zweig-breadth-thrust-indicator-strategy/),
[Investing.com skeptical take](https://www.investing.com/analysis/zweig-breadth-thrust-is-it-a-trustworthy-technical-indicator-for-stock-market-200660043)).
**Honest limits:** our breadth is 29 ETFs + 39 survivor stocks, not the NYSE
tape the folklore is built on; thrust N is tiny → any test is
INCONCLUSIVE-prone. **Verdict: cheap to build as a regime *feature*; not a
standalone experiment worth a prereg on its own.**

### 3. EDGAR Form 4 insider trades — strongest academic anomaly, heaviest build
Cohen, Malloy & Pomorski (*Decoding Inside Information*, J. Finance 2012):
**opportunistic** (pattern-breaking) insider buys → ~82 bps/mo value-weighted
abnormal returns; routine trades → nothing
([NBER w16454](https://www.nber.org/system/files/working_papers/w16454.pdf),
[AQR](https://www.aqr.com/Insights/Research/Journal-Article/Decoding-Inside-Information)).
Filing-date-stamped EDGAR data is point-in-time (no lookahead on the signal
side). **Honest limits:** multi-year Form 4 ingestion is the biggest build
this project would have attempted; pricing the signals through yfinance
reintroduces survivorship on the *price* side (delisted names unpriceable) →
asymmetric framing again; drift horizon is weeks-to-months (upper edge of
swing). **Verdict: the one new data type with a real shot at a return edge;
gate it behind a scoped data-probe task before any prereg.**

### 4. FRED macro/credit regime gates
HY OAS spread widening / curve inversion as risk-off gates. Free, decades of
history, EOD. **But:** publication-lag/revision nuance (ALFRED vintages exist
for honesty), and again an **overlay**, not a return engine. Worth folding
into the same experiment as #1 (one "regime-gate bake-off" prereg: VIX-TS vs
HY-OAS vs breadth vs the existing 200DMA, all a-priori knobs, judged on the
E6 overlay criteria) rather than five separate preregs.

### 5. Dividend capture (calendar data)
Buy before ex-date, sell after; yfinance has full dividend history and our
price convention (dividend-UNadjusted closes) is exactly right for measuring
it. Literature and practice say the drop ≈ the dividend and costs/taxes eat
the residue. **Verdict: cheap one-sitting falsification test; low prior;
pedagogically neat (the convention finally works *for* us).**

### 6. Blocked / rejected at $0 (recorded so nobody re-litigates)
- **Options flow / IV history** — no free historical chains; BLOCKED.
- **Short-interest history** — E17's probe (M7 task 32) still owns this.
- **News/social sentiment history** — no free point-in-time archive; honest
  path is FORWARD-ONLY = the already-planned M3 LLM-veto sleeve.
- **Google Trends** — data is resampled/renormalized per request →
  irreproducible backtests; rejected on rigor grounds.
- **13F holdings** — 45-day lag makes it position-trading, out of scope.
- **Crypto (24/7 OHLCV, Alpaca-tradable)** — a new *asset class*, not a new
  data type; would need its own goal decision from Evan; parked.

---

## Ranked additions (if M7 grows)

1. **E18 — Regime-gate bake-off** (VIX term structure vs HY-OAS vs breadth vs
   200DMA, all a-priori knobs, judged as overlays on the E6 criteria).
   Data in hand; one prereg; directly upgrades the project's one surviving
   artifact (the 1× overlay). *Recommended.*
2. **E19 — Insider opportunistic-buy drift** — gated behind an EDGAR
   ingestion probe (scoped: one year of Form 4s for the 39-stock universe
   first). Only attempt if the probe is clean.
3. **E20 — Dividend capture falsification** — one sitting, low prior, run
   whenever convenient.

## What would change this conclusion
- A free historical options/IV or short-interest source appearing (unblocks
  the vol-risk-premium and DTC families properly).
- Evan approving a paid data budget (even ~$30/mo unlocks options/SI
  history) — that is a **new decision**, not assumed.
- D1 (risk-adjusted tier) being declined — that guts E18's point too, since
  overlays by construction can't pass a pure return bar.

## Sources
- Probe: `probe_datatypes.py` run 2026-07-12 (results table above).
- VIX term structure — [Raven Quant](https://ravenquant.com/vix-term-structure/) · [Cboe](https://www.cboe.com/tradable-products/vix/term-structure/) · [PMC ML study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11029606/) · [Aptus](https://aptuscapitaladvisors.com/utilizing-volatility-expectations-to-guide-risk-taking/)
- Cohen, Malloy, Pomorski — *Decoding Inside Information* (2012) — [NBER w16454](https://www.nber.org/system/files/working_papers/w16454.pdf) · [AQR](https://www.aqr.com/Insights/Research/Journal-Article/Decoding-Inside-Information) · [Harvard corp-gov summary](https://corpgov.law.harvard.edu/2012/02/03/decoding-inside-information/)
- Zweig breadth thrust (practitioner, discounted) — [QuantifiedStrategies](https://www.quantifiedstrategies.com/zweig-breadth-thrust-indicator-strategy/) · [skeptical review](https://www.investing.com/analysis/zweig-breadth-thrust-is-it-a-trustworthy-technical-indicator-for-stock-market-200660043)
- FRED series probed keyless via `fredgraph.csv` (T10Y2Y, ICSA, BAMLH0A0HYM2).
