# Pre-registration — E14: Diversified sector momentum

**Written 2026-07-12, BEFORE any runner code. Committed doc-only; this hash
predates the runner. M7 task 29; D1 dual-bar verdict.**

## Provenance and why this one matters

Moskowitz & Grinblatt (1999, *J. Finance*): industry/sector momentum is a
robust driver of returns, partly subsuming individual-stock momentum. E3
already FAILED *concentrated single-stock* momentum — but that test was
survivorship-flattered (only a FAIL was clean). **E14 is different: the 11
SPDR sector ETFs are survivorship-CLEAN** (all 11 exist today; the two late
launches were genuinely unavailable early, which is availability, not
survivorship). So **a PASS here would be the program's first fully-
interpretable pass of any tier** — that is the point of running it.

## Universe, data

- The 11 SPDR sector funds from the frozen universe: XLE XLF XLK XLV XLI XLY
  XLP XLU XLB XLRE XLC. Data from `.e8e9_cache` (split-adjusted,
  dividend-UNADJUSTED). No swing.db writes. EOD: signal at close, execute
  next open.
- Availability: XLRE from 2015, XLC from 2018; the other 9 from 1998. At each
  rebalance only sectors with ≥ 126 sessions of history are eligible — so the
  2000–2013 gate ranks among the original 9. Disclosed, not corrected.

## Exact rules (fixed a priori)

- **Rebalance every 21 trading sessions.** At the rebalance decision (close of
  session i), rank all eligible sectors by trailing **126-session** total
  return (close_i / close_(i−126) − 1). Hold the **top 3, equal-weight**
  (NAV/3 each). Execute a full rebalance at the next open (liquidate all,
  buy the new top-3), 5 bps/side. $1,000 start.
- Between rebalances, hold. No stop, no intra-period exit (a clean momentum
  test).

## Windows and D1 verdict (all three labels fixed here)

- **Gate 2000-01-01 → 2013-12-31.** **Secondary 2014-01-01 → end.**
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60% in the gate window, confirmed
  in secondary.
- **PASS-RA:** net Sharpe ≥ 0.80 in the gate window AND Sharpe > SPY buy-hold
  in BOTH windows AND positive net CAGR in both.
- **FAIL:** neither. Interpretability floor: ≥ 30 rebalance-entries in the
  gate window.
- Benchmarks reported: SPY buy-hold and equal-weight-all-available-sectors
  buy-hold. No parameter changed after results.

## Disclosed limitations

- Dividend-UNADJUSTED closes understate sector returns and the benchmarks
  equally (~2%/yr); direction of bias is neutral across the comparison.
- 126/21/top-3 are the a-priori knobs (medium-term momentum, monthly rebal,
  concentrated per the project's K=1–3 goal); no grid search (that would be
  post-hoc tuning).
- Survivorship-clean on the ETF side; this is the interpretability advantage.
