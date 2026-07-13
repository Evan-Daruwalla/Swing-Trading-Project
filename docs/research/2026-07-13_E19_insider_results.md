# E19 — Opportunistic insider-buy drift (SEC Form 4): RESULTS

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Prereg:** `ebf54a4` (doc-only, predates the runner `8b12932`). **Runner:**
`scripts/run_e19_insider.py`. **Verdict:** **FAIL (clean, robust to data
cleaning).** Frozen tripwire GREEN (12 refs, d=±0.0000pp) after the run.

---

## TL;DR (verdict first)

Opportunistic insider open-market buys (SEC Form-4, CMP routine-vs-opportunistic
classification, next-open entry, 40-session hold, K=5) on the 39-name survivor
large-cap universe produce a **sub-beta long-only equity sleeve**: gate-window
(2003–2013) CAGR **4.68%** / Sharpe **0.31**, secondary (2014→) CAGR **4.91%** /
Sharpe **0.35** — **underperforming SPY buy-hold on both CAGR and Sharpe in both
windows** (SPY 6.65%/0.42 and 11.98%/0.74). Both pre-registered pass tiers fail
(PASS-HR needs ≥15% CAGR; PASS-RA needs gate Sharpe ≥0.80). The dataset carried
**severe transactionCode-"P" contamination** (BAC alone = 2,851 of 6,435 P-buys =
44%, dominated by the issuer's own CIK, including 1-share sub-penny artifacts; the
CMP classifier passed 95% through as "opportunistic" — the Appendix-BQ prediction
that it would absorb them as "routine" was **falsified**). A post-hoc de-junk
sensitivity (price floors $1/$5, same-owner-same-day dedup that cuts entries
6,119→2,675) leaves the verdict and the stats unchanged — so **cleaning does not
reveal a masked edge; the FAIL is robust, not a contamination artifact.** Idea
closed. **Tally → 0 PASS-HR / 1 weak PASS-RA / 21 attempts / 8 families.**

---

## Method

- **Prereg (`ebf54a4`, committed before the runner):** trade only *opportunistic*
  buys — Cohen-Malloy-Pomorski: routine = the reporting owner bought in the same
  calendar month in each of the prior 3 years; everything else is opportunistic.
  Enter the first session **after** the filing date (`bisect_right` on the trading
  calendar), hold **40 sessions**, **K=5**, size on NAV/K, **5 bps/side**.
- **Universe:** the same 39 survivor large-caps as E3/E10 (`run_e10_earnings_drift.UNIV`).
  Survivorship + the fact that these names never delisted means every bias runs
  **in the strategy's favor** → per the standing asymmetric-falsification doctrine,
  only a FAIL is clean; any PASS would be uninterpretable and route to forward paper.
- **Data:** SEC EDGAR Form-4, full history, resumable per-ticker ingester
  (`scripts/ingest_edgar_form4.py`, 39/39 tickers, `.edgar_cache/` gitignored).
  Open-market buy = transactionCode "P" + acquired flag "A". Former-CIK map for
  XOM/DIS. Gate window starts 2003 (structured-XML floor).
- **Verdict:** D1 dual-bar (prereg `ebf54a4`, goal amendment Appendix AW), all three
  outcomes fixed before running. Done-check: D1 verdict + frozen tripwire GREEN.

---

## Results (as-run, per prereg)

```
P-buys 6435; opportunistic 6138; tradeable entries 6138; gate entries 279 (≥20 ok)

window        E19 CAGR   maxDD  Sharpe  |  SPY CAGR  SPY Sharpe
2003-2013        4.68%   53.6%    0.31  |     6.65%       0.42
2014-            4.91%   42.6%    0.35  |    11.98%       0.74
```

- **PASS-HR** (CAGR ≥15% AND maxDD ≤60%, both windows): **FAIL** — 4.68%/4.91% CAGR.
- **PASS-RA** (gate Sharpe ≥0.80 AND > SPY both windows AND +CAGR both): **FAIL** —
  gate Sharpe 0.31 < 0.80, and E19 Sharpe < SPY Sharpe in both windows.
- **VERDICT: FAIL** — the insider opportunistic-buy idea is closed under
  pre-registration.

---

## Data-quality finding (carries + corrects Appendix BQ)

The per-ticker P-buy distribution is pathological:

| ticker | P-buys | | ticker | P-buys |
|---|---:|---|---|---:|
| **BAC** | **2851** | | C | 178 |
| **GS** | **728** | | T | 165 |
| **ABT** | **388** | | WMT | 133 |
| **JPM** | **353** | | AXP | 118 |
| **GE** | **310** | | (34 others) | ≤98 each |

- **BAC = 44% of all P-buys**, dominated by a single "owner" CIK `0000070858` —
  which is **Bank of America's own issuer CIK**, not an insider — and includes
  **1-share lots priced $0.01–0.02**, physically impossible as real open-market BAC
  purchases (DRIP/fractional/accounting artifacts mis-coded as transactionCode "P").
- **The CMP classifier did NOT absorb these.** 6,138 of 6,435 (95%) were classified
  *opportunistic*. Appendix BQ predicted the same-calendar-month-3-years routine rule
  would catch DRIP as "routine" and exclude it — **that prediction is falsified**
  (DRIP cadence + duplicate line-items don't map cleanly onto the same-month-each-year
  pattern, so they leak through as opportunistic).
- **Appendix BQ also claimed contamination "can only inflate a spurious PASS."** That
  is imprecise: mechanical (signal-free) buys pull the sleeve **toward market beta**,
  which is **bidirectional** — it could equally *mask* a real edge by diluting it.
  That is the genuine threat to a FAIL, and the reason for the sensitivity below.

## Post-hoc de-junk sensitivity (NOT the prereg result)

To resolve whether the FAIL is a contamination artifact, the existing cache was
re-run with junk filters (no re-ingestion). **Per doctrine, any pass here would be
"PROMISING / needs a fresh prereg," never a claimed PASS** — but none flipped:

| filter | kept buys | entries | gate entries | gate CAGR / DD / Sh | 2014- CAGR / DD / Sh | verdict |
|---|---:|---:|---:|---|---|---|
| as-run (prereg) | 6435 | 6138 | 279 | 4.68% / 53.6% / 0.31 | 4.91% / 42.6% / 0.35 | FAIL |
| price ≥ $1 | 6410 | 6119 | 279 | 4.66% / 53.7% / 0.31 | 4.96% / 42.6% / 0.36 | FAIL |
| price ≥ $1 + same-owner/day dedup | 2775 | 2675 | 279 | 4.54% / 53.7% / 0.30 | 4.91% / 42.6% / 0.35 | FAIL |
| price ≥ $5 + dedup | 2655 | 2562 | 277 | 3.66% / 55.8% / 0.27 | 4.67% / 42.6% / 0.34 | FAIL |

Only 25 records are sub-$1, but **dedup nearly halves the entry set** (6,119→2,675),
confirming heavy same-owner/same-day line-item duplication. Yet every variant stays
flat and sub-beta (gate Sharpe 0.27–0.31). Gate *entries used* is stable at ~279
across all variants because a K=5 / 40-session book **saturates** — throughput, not
raw signal count, sets the trade rate. **Cleaning does not reveal a masked edge.**

---

## Interpretation

E19 is what an honest retail-EOD insider-drift test *should* produce, and it matches
the program's structural conclusion (Hou-Xue-Zhang / McLean-Pontiff / survey
2026-07-12): a **K-concentrated, liquidity-floored, survivor-universe** sleeve of a
diversified anomaly collapses to a slightly-worse-than-market long-only book. The
documented insider-buy alpha lives in **small, illiquid** names (Lakonishok-Lee;
Cohen-Malloy-Pomorski's own effect is strongest in small caps) — exactly the names
the mandatory liquidity floor excludes — and next-open EOD execution surrenders any
announcement pop. The survivor large-caps here (all of which *did* fine long-term)
give the sleeve market beta and nothing more.

**Asymmetric close:** survivorship could only *help*; the contamination *could* have
hurt (masking), and the sensitivity ruled that out. So the FAIL is clean in both
directions — the strongest negative the program can produce on a survivor universe.

---

## What would change the conclusion (untested falsifiers)

- A **survivorship-free, delisting-inclusive** universe (the bias currently favors
  the strategy and it *still* fails — but a clean universe is the honest next build).
- A **liquidity-floor-respecting small/mid-cap** universe where the documented effect
  actually lives (contradicts the floor mandate at $100–1,000 → not runnable here).
- A **clean P-code build** (footnote-parsed to exclude DRIP/ESPP, owner≠issuer, real
  open-market only) — but the sensitivity already brackets this and it does not flip.

None of these are worth building against a 0-PASS-HR / 20-prior base rate; E19 is
closed. If revisited, it would need a fresh prereg, not a re-run.

## Reproduction

- Ingest: `.venv\Scripts\python.exe scripts/ingest_edgar_form4.py` (resumable; writes
  `.edgar_cache/{ticker}.json`, gitignored).
- Run: `.venv\Scripts\python.exe scripts/run_e19_insider.py`.
- Tripwire: `.venv\Scripts\python.exe -m swing_bot.test_frozen` → GREEN, 12 refs d=0.
- Sensitivity script is scratch-only (post-hoc, not committed); table above is the record.

## Sources (dated)

- Cohen, Malloy, Pomorski — *Decoding Inside Information* (2012, JF) — routine vs
  opportunistic insiders; opportunistic buys predict returns, effect strongest in
  small caps.
- Lakonishok & Lee — *Are Insiders' Trades Informative?* (2001, RFS) — insider-buy
  informativeness concentrated in small firms.
- SEC EDGAR Form-4 full-text + structured XML (`data.sec.gov`), accessed 2026-07-13.
- Prior project docs: survey `docs/research/2026-07-12_swing_method_full_survey.md`;
  D1 amendment record Appendix AW; contamination flag record Appendix BQ.
