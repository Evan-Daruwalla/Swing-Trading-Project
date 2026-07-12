# E19 STEP-1 probe — insider Form-4 ingestion: FEASIBLE-BUT-DEFERRED

**2026-07-11 (CST) · M7b task 34, probe step per PRD (no prereg — the probe
gates the effort). No swing.db writes; no strategy run.**

## Question
Is SEC EDGAR Form-4 ingestion clean and feasible enough to build the
Cohen-Malloy-Pomorski opportunistic-insider-buy strategy (E19) over the
2000–2013 gate window for the 39-stock survivor universe?

## Probe results (2026-07-11)
- **CIK resolution: 39/39** tickers mapped via `company_tickers.json`. ✓
- **Submissions API works** (`data.sec.gov/submissions/CIK*.json`); recent
  Form-4 volume is healthy for active names — AAPL 42, JPM 132, WMT 215,
  GE 51 in the last ~year. ✓
- **Three real hazards for a HISTORICAL build:**
  1. **CIK changes over time.** XOM now resolves to CIK 0002115436 with only
     26 filings and **zero** Form-4s — its historical filings are under a
     prior CIK (0000034088). Clean 2000–2013 coverage requires a
     CIK-history map, or names silently lose their history.
  2. **`primaryDocument` is the XSL/HTML render** (`xslF345X06/form4.xml`),
     not raw XML — every parse must rewrite the URL to the raw document.
  3. **Recent-submissions API caps at ~1000 filings.** JPM has 25,342 total;
     reaching 2000–2013 requires paginating EDGAR's older submission archives
     or the quarterly full-index — i.e. tens of thousands of fetches across
     39 names, each raw-XML-parsed, under the 10 req/s limit.

## Verdict: FEASIBLE-BUT-DEFERRED (Evan-gated effort)
The data exists and parses, so this is **not** BLOCKED-ON-DATA. But the full
gate-window ingestion is the heaviest build the project would attempt (hours,
tens of thousands of HTTP fetches, plus the CIK-history and raw-XML hazards),
and E19 inherits E3's survivorship → asymmetric framing (only a FAIL is
clean). Against a program base rate of **0 PASS-HR / 19 attempts**, committing
that effort for a near-certain interpretable-FAIL is a poor trade to make
autonomously. Recorded as **deferred**, pending an explicit Evan decision to
authorize the ingestion (or a paid insider-data feed that sidesteps the three
hazards).

**Unblock/proceed conditions:** Evan authorizes the full EDGAR build (I'll
handle CIK-history + raw-XML + archive pagination), OR a clean vendor feed
appears. This is the M7b terminus: E18 done (weak PASS-RA), E20 done (FAIL),
**E19 deferred.**
