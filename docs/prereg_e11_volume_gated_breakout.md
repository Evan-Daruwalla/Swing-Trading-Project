# Pre-registration — E11: Volume-gated consolidation breakout

**Written 2026-07-10, BEFORE any runner code. Committed doc-only; this hash
predates the runner.**

## Provenance and the "is this retuning a FAIL?" question

Three article-set sources (SMB "RVOL ≥ 1.5 on the breakout," CapTrader "high
volume + high volatility breakout," the ex-Trillium trader's volume-climax
filter) all insist a breakout is only tradeable **with volume confirmation.**
E8 (squeeze breakout) FAILED with **no volume filter.** E11 tests exactly one
new hypothesis: *does requiring elevated volume on the breakout bar give
breakouts the directional edge E8 lacked?*

**Why this is a new experiment, not a retune of a FAIL:** the RVOL ≥ 1.5 gate
is specified **a priori by external sources**, NOT derived by inspecting E8's
losing trades and reverse-engineering a filter that would flip them. E8's
gates and exits are held **identical**; the ONLY change is the added entry
condition. Prior remains POOR (E8 failed at the family level; a volume gate is
a refinement). Disclosed.

## Universe, data, rules

- Frozen 29-ETF universe; data reused from the E8/E9 live-fetch cache
  (`.e8e9_cache/`, gitignored); **no swing.db writes**. EOD only.
- **Identical to E8** (prereg `9b49190`): BB(20, 2σ) inside Keltner(EMA20,
  1.5×ATR20) squeeze for ≥5 consecutive sessions, then squeeze OFF and
  close > SMA20 → breakout; K=3; exit close < EMA20 OR 40-bar max hold; buy
  next open; 5 bps/side; $1,000 NAV/3.
- **ADDED (the only change):** the breakout bar t must satisfy
  **RVOL_t = volume_t / mean(volume[t−20 … t−1]) ≥ 1.5.** Signals failing the
  gate are skipped.

## Windows and gates (unchanged from E8 — any miss = FAIL)

- **Gate 2000–2013:** CAGR ≥ 15% AND maxDD ≤ 60%. Interpretability floor
  n_trades ≥ 30 (the volume gate will thin trades; below 30 → INCONCLUSIVE).
- **Secondary 2014 → end:** overall PASS also needs CAGR ≥ 15% & maxDD ≤ 60%
  here.
- No tuning after results. A FAIL closes the volume-gated-breakout idea.

## Disclosed limitations

- ETFs only (single stocks = survivorship trap, E3). The pros apply this to
  single stocks; the ETF reading is the survivorship-clean, interpretable one.
- Dividend-UNADJUSTED closes; staggered ETF inception (fewer names early).
