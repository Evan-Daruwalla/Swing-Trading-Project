# Pre-registration — E16: Cross-sectional weekly reversal

**Written 2026-07-11 (CST), BEFORE any runner code. Committed doc-only; this
hash predates the runner. M7 task 31; D1 dual-bar verdict + asymmetric
framing.**

## Provenance, prior, and disclosed counter-evidence

De Groot, Huij & Zhou (2012, *J. Banking & Finance*): short-term reversal
earns 30–50 bps/week **net of costs** when confined to large caps. This is
the catalog's strongest untested candidate — but two disclosures up front:
1. **Counter-evidence from our own work:** the M1 fill-timing ablation found
   54% of the mean-reversion edge lives in the close→next-open gap an EOD bot
   forfeits. The paper's construct is close-based and long-short; our
   next-open long-only version should capture materially less. Prior: modest.
2. **Universe bias:** run on E3's 39 survivor large-caps → survivorship;
   asymmetric framing (only a FAIL is clean) layered on the D1 tiers.

## Universe, data

- E3's 39 survivor large-caps, from `.e8e9_cache` (split-adjusted,
  dividend-UNADJUSTED). No swing.db writes. EOD.

## Exact rules (fixed a priori)

- **Weekly signal** on the last trading session of each calendar week
  (detected via weekday: session d is a week-end if the next available
  session falls in a different ISO week). Rank all 39 by **trailing 5-session
  return** (close_d / close_(d−5) − 1).
- **Enter** the **bottom 4** (largest 5-session losers → reversal bet) at the
  next session's open, equal-weight (NAV/4). **Full weekly rebalance:**
  liquidate the prior basket and buy the new bottom-4 at that same next open;
  so each basket is held ≈ 1 week (to the next weekly rebalance). 5 bps/side.
  $1,000 start.

## Windows and verdict

- **Gate 2000-01-01 → 2013-12-31.** **Secondary 2014 → end.**
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60% in the gate window, confirmed
  in secondary. **PASS-RA:** net Sharpe ≥ 0.80 in the gate window AND
  Sharpe > SPY buy-hold in BOTH windows AND positive net CAGR in both.
  **FAIL:** neither.
- **Asymmetric overlay:** because of survivorship, a PASS is reported
  UNINTERPRETABLE (forward only); a FAIL is clean and closes the weekly-
  reversal idea. Floor: ≥ 30 weekly rebalances in the gate window (trivially
  met). Benchmarks: equal-weight-39 and SPY. No tuning after results.

## Disclosed limitations

- Next-open execution forfeits the overnight component the paper captures
  (our own ablation) — the central reason the prior is modest.
- Long-only bottom-4 vs the paper's long-short deciles — a different, more
  retail-realistic construct; not a replication.
- Survivorship (39 current large-caps); dividend-UNADJUSTED closes.
