# Pre-registration — C6: Even-week FOMC-cycle overlay

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M8 task 41 (free-sweep authorization 2026-07-14). Written
against `docs/prereg_TEMPLATE.md`. OVERLAY → PASS-RA realistic tier; D1 stated.**

## Provenance and prior

Cieslak-Morse-Vissing-Jorgensen (2019 JF, *Stock Returns over the FOMC Cycle*): since
1994 the equity premium is earned almost entirely in **even weeks of FOMC-cycle time**
(weeks 0, 2, 4, 6 after a scheduled announcement). **H1:** long-SPY-in-even-weeks
beats SPY buy-hold risk-adjusted. **H0:** post-publication (2019) the pattern is
decayed/arbitraged (McLean-Pontiff), and ~50% exposure forfeits too much drift.
**Prior: FAIL/weak.** Distinct from the killed E13 (calendar-day turn-of-month rule);
this is a meeting-cycle rule.

## Data (in hand; provenance committed)

- **FOMC calendar:** `data/fomc_announcement_dates.json` — 260 scheduled announcement
  dates 1994–2026, compiled 2026-07-14 from federalreserve.gov primary sources
  (fomchistorical{YEAR}.htm 1994–2020; fomccalendars.htm 2021+), unscheduled/emergency
  meetings excluded, spot-checked against press releases. **No lookahead:** the
  schedule is published ~a year in advance, so cycle position is known at signal time.
- SPY OHLCV from `.e8e9_cache` (split-adjusted, dividend-UNADJUSTED). No swing.db writes.

## Exact rules (fixed a priori)

- **Cycle time:** t = number of SPY trading sessions since (and including) the most
  recent scheduled announcement date ⇒ announcement day is t=0. If the announcement
  date is a non-session, t=0 is the first session after it.
- **Even weeks:** t ∈ [0,4] ∪ [10,14] ∪ [20,24] ∪ [30,34]. **Exposure = 1 in even
  weeks, 0 otherwise** (t ∈ odd weeks or t > 34 — the latter handles the long
  cancelled-meeting gap of 2020 conservatively as flat).
- Signal at close (tomorrow's t is deterministic from the public calendar), execute
  **next open**; **1 bp/side** (broad ETF tier); 5/15 bp stress legs.
- No sizing/leverage; long-or-flat SPY only.

## Windows and verdict [D1]

- **Gate 2000-01-01 → 2013-12-31**; **secondary 2014→** (calendar covers 1994+; SPY
  cache floor governs). Floor ≥ 30 gate exposure toggles.
- **PASS-HR:** CAGR ≥ 15% AND maxDD ≤ 60% both windows (stated; realistically
  unreachable for a ~50%-exposure unlevered SPY subset). **PASS-RA:** gate Sharpe ≥
  0.80 AND > SPY-BH both windows AND +CAGR both. **FAIL:** neither. No post-hoc
  changes.

## Results-doc requirements
Both windows vs SPY-BH; exposure %; even-week vs odd-week mean daily return (the
CMVJ signature, descriptive); cost ladder 1/5/15 bp; tripwire GREEN.

## Disclosed limitations
Post-publication decay expected; single-index; the 2020 cancelled-meeting gap handled
by the t>34→flat rule (pre-registered, not tuned); CMVJ's mechanism (informal Fed
communication) is not directly observable here.
