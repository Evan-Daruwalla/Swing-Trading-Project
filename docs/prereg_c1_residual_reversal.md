# Pre-registration — C1: Short-term residual reversal (FF3-stripped)

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M8 task 36 (free-sweep authorization 2026-07-14). Written
against `docs/prereg_TEMPLATE.md`. D1 dual-bar + asymmetric framing (survivor
universe → only a FAIL is clean).**

## Provenance and prior

Blitz-Huij-Lansdorp-Verbeek (2013): ranking on **residual** (factor-stripped) returns
roughly doubles reversal's Sharpe and cuts its factor-driven risk vs raw reversal.
Direct refinement of **E16** (raw weekly reversal: gate CAGR 16.76% — the only
experiment to clear the 15% return bar — but on a 65.9% drawdown + survivorship).
**H1:** stripping FF3 exposure from the formation return keeps the return while
cutting the DD below the 60% ceiling. **H0 (expected):** the "reversal" in this
survivor universe is beta-to-dip-buying, not idiosyncratic mean reversion — stripping
factors strips the return too; and Nagel (2012) says reversal is close-anchored
liquidity provision that next-open execution bleeds (EX-DECOMP measured E16 gap-bleed
−4.96 pp). **Prior: FAIL** (E16's return was survivorship-flattered; the DD fix and
the return come from the same factor loading).

## Data (in hand + one free fetch)

- 39 survivor large-caps (E10 `UNIV`), OHLCV via `.e8e9_cache` (split-adj, div-UNADJ).
- **Fama-French 3-factor DAILY** (Mkt-RF, SMB, HML) from Ken French's library
  (Dartmouth, free CSV zip), fetched once and cached (gitignored, like price caches).
  No swing.db writes.

## Exact rules (fixed a priori)

- **Betas:** per name, OLS (with intercept) of daily returns on [Mkt-RF, SMB, HML]
  over the **trailing 126 aligned sessions** ending at the formation date.
- **Formation signal:** residual return = **sum of the last 21 daily OLS residuals**
  (the factor-stripped trailing-month return).
- **Portfolio:** each week-end (ISO-week change, as E16), rank the 39 by residual;
  **buy the bottom K=4** (most negative residual) at next open, full weekly rebalance
  — deliberately E16's exact engine with only the ranking variable changed, so any
  difference is attributable to the residual construction. **5 bps/side**; NAV/4;
  $1,000 start.
- Names need ≥ 147 aligned sessions to rank; SPY excluded from selection.

## Windows and verdict [D1 dual-bar]

- **Gate 2000-01-01 → 2013-12-31**; **secondary 2014→**. Floor ≥ 30 gate entries.
- **PASS-HR:** CAGR ≥ 15% AND maxDD ≤ 60% both windows. **PASS-RA:** gate Sharpe ≥
  0.80 AND > SPY both windows AND +CAGR both. **FAIL:** neither. Benchmarks: SPY-BH +
  EW-39. **Asymmetric:** survivor universe — a PASS is UNINTERPRETABLE (forward
  only); only a FAIL closes cleanly. Explicit comparison vs E16 (raw ranking) required
  in the results doc.

## Results-doc requirements
Decomposition ladder A/B/C + 15 bp stress; side-by-side vs E16's recorded numbers;
tripwire GREEN.

## Disclosed limitations
Survivorship (39 current large-caps) — flatters any dip-buying rule; FF3 factors are
market-wide (no industry factor — BHLV also strip industries; disclosed
simplification); 126d beta window and 21d formation fixed a priori, not tuned;
weekly cadence inherits E16's turnover cost profile.
