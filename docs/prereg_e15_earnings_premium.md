# Pre-registration — E15: Earnings-announcement premium

**Written 2026-07-12, BEFORE any runner code. Committed doc-only; this hash
predates the runner. M7 task 30; D1 dual-bar verdict + E3/E10 asymmetric
framing.**

## Provenance and framing

Frazzini & Lamont (2007, NBER w13090): stocks rise *around scheduled*
earnings announcements — an attention-driven "earnings-announcement premium,"
distinct from PEAD (which is the *post*-announcement drift E10 already FAILED).
E15 tests the *pre/through*-announcement premium. Universe = E3's 39 survivor
large-caps + cached earnings dates → **two biases stack**: survivorship (E3
lesson) AND a mild lookahead (we use Yahoo's *today-known* announcement dates;
rescheduled dates correlate with news). So framing is asymmetric: **only a
FAIL is clean**; any PASS is uninterpretable and routes to forward paper.

## Universe, data

- E3's 39 survivor large-caps. Earnings dates via the E10 infra
  (`get_earnings_dates(limit=100)`, cached `.e8e9_cache/{t}_earn.json`,
  ~2001 on). OHLCV from `.e8e9_cache` (split-adjusted, dividend-UNADJUSTED).
  No swing.db writes. EOD.

## Exact rules (fixed a priori)

- For each announcement date E, let **a** = the first ticker session with date
  ≥ E. **Entry:** buy at the open of session **a−5** (5 sessions before the
  announcement). **Exit:** sell at the open of session **a+1** (the session
  after the announcement) — capture the run-up premium through the event,
  exit immediately after. Hold ≈ 6 sessions.
- Max **K=5** concurrent (earnings cluster in season → the cap binds).
  Process events by entry date; if a slot is free at the entry session, take
  it, else skip that event (no queueing). Size = min(cash, NAV/5); 5 bps/side.
  $1,000 start.

## Windows and verdict

- **Gate 2000-01-01 → 2013-12-31** (earnings data ~2001.5 on). **Secondary
  2014 → end.**
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60% in the gate window, confirmed
  in secondary. **PASS-RA:** net Sharpe ≥ 0.80 in the gate window AND
  Sharpe > SPY buy-hold in BOTH windows AND positive net CAGR in both.
  **FAIL:** neither.
- **Asymmetric overlay on D1:** because of survivorship+lookahead, a PASS-HR
  or PASS-RA is reported as **PASS (UNINTERPRETABLE — biases; forward only)**;
  a FAIL is clean and closes the earnings-premium idea. Floor: ≥ 20 gate
  entries. Benchmarks: equal-weight-39 buy-hold and SPY. No tuning after
  results.

## Disclosed limitations

- Survivorship (39 current large-caps) + scheduled-date lookahead — both can
  only flatter; hence FAIL-only interpretation.
- 100-row earnings cap → history starts ~2001–2002.
- Dividend-UNADJUSTED closes; ~6-session holds make the dividend omission
  negligible here.
