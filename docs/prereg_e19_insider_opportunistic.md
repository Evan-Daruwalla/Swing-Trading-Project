# Pre-registration — E19: Opportunistic insider-buy drift (SEC Form 4)

**Written 2026-07-11 (CST), BEFORE any backtest runner code. Committed
doc-only; this hash predates the runner. M7b task 34 (Evan authorized the
full EDGAR build 2026-07-11); D1 dual-bar verdict + E3 asymmetric framing.**

## Provenance and prior

Cohen, Malloy & Pomorski (*Decoding Inside Information*, J. Finance 2012):
**opportunistic** insider trades (pattern-breaking) earn ~82 bps/mo abnormal
returns; **routine** trades (same-month-every-year) earn nothing. E19 tests
the long side — opportunistic insider **purchases** — on the 39 survivor
large-caps. Survivorship + the strategy only trading currently-listed names →
asymmetric framing: **only a FAIL is clean**; a PASS is uninterpretable and
routes to forward paper. Prior: near-certain FAIL vs a 0-PASS-HR/19 base rate.

## Data (probed 2026-07-11)

- SEC EDGAR Form 4, ingested per name via the submissions API + archive files,
  raw-XML parsed. **104,496 Form-4s across the 39** (fetch budget, ~hours).
- **Disclosed data limits:** (1) structured Form-4 XML begins ~**2003**
  (SEC mandatory e-filing) → the gate window is effectively **2003–2013**,
  not 2000 (the pre-2003 slice has no parseable insider data). (2) Two names
  (XOM, DIS) have pre-reorganization history under **former CIKs** — resolved
  via a manual former-CIK map (XOM 0000034088, DIS 0001001039); coverage
  still best-effort. (3) Filing date (not transaction date) is used for
  point-in-time entry — no lookahead (Form 4 is filed within 2 business days).
- Prices from `.e8e9_cache` (split-adjusted, dividend-UNADJUSTED). No
  swing.db writes.

## Exact rules (fixed a priori)

- **Transactions used:** open-market **purchases** only — Form-4
  `transactionCode == "P"` AND acquired/disposed `== "A"`. (Grants A/M, sells
  S/F ignored.)
- **Routine vs opportunistic** (per reporting-owner CIK, CMP-style): a
  purchase in calendar month *m* of year *y* is **ROUTINE** if that insider
  also made a purchase in month *m* in each of years *y−1, y−2, y−3*;
  otherwise **OPPORTUNISTIC**. E19 trades only OPPORTUNISTIC purchases.
- **Entry:** on any opportunistic purchase with filing date *F* in a stock,
  buy that stock at the next session's open. One position per stock (a second
  insider buy while already long is ignored). **Hold 40 trading sessions**,
  exit at open. **K = 5** concurrent; if oversubscribed, earliest-filing
  first. Size = min(cash, NAV/5); 5 bps/side; $1,000 start.

## Windows and verdict

- **Gate 2003-01-01 → 2013-12-31** (structured-data floor). **Secondary
  2014 → end.**
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60% both windows. **PASS-RA:** gate
  Sharpe ≥ 0.80 AND > SPY buy-hold both windows AND +CAGR both. **FAIL:**
  neither. Floor: ≥ 20 opportunistic-buy entries in the gate window.
- **Asymmetric overlay:** a PASS is reported UNINTERPRETABLE (forward only);
  a FAIL is clean and closes the insider idea. Benchmarks: equal-weight-39
  and SPY. No parameter changed after results.

## Disclosed limitations

- Survivorship (39 current large-caps) — the reason for FAIL-only reading.
- 2003 structured-data floor; best-effort former-CIK coverage (XOM/DIS).
- Filing-date entry (≈ transaction + 1–2 business days); no intra-month
  timing optimization (would be tuning).
