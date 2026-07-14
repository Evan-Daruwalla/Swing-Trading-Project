# Pre-registration — C4: Vol-targeting sizing overlay (Moreira-Muir)

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M8 task 39 (free-sweep authorization 2026-07-14). Written
against `docs/prereg_TEMPLATE.md`. OVERLAY → PASS-RA only; DESCRIPTIVE (low
effective N).**

## Provenance and prior

Moreira-Muir (2017 JF): scaling exposure inversely to realized variance raises Sharpe
on factor portfolios. **H1:** vol-managing the program's surviving overlays (E6
200-DMA; E18 VIX-TS — the lone weak PASS-RA) improves their gate Sharpe. **H0
(expected):** no improvement — Cederburg-O'Doherty-Wang-Yan (2020) show the effect
largely fails real-time out-of-sample; X1 already showed vol-conditioning adds nothing
to the 200-DMA. **Prior: FAIL.**

## Data (in hand)
QQQ from `.e8e9_cache` (split-adj, div-UNADJ); `^VIX`/`^VIX3M` via cached
`macro_close`. No swing.db writes.

## Exact rules (fixed a priori)

- **Bases:** (i) **E6:** long QQQ iff QQQ close > 200-DMA; (ii) **E18:** long QQQ iff
  VIX/VIX3M < 1. Exposure 0 when the gate is off.
- **Overlay:** when the gate is on, target weight **w = min(1, 0.15 / σ_ann)** where
  σ_ann = trailing 20-session realized vol, annualized (√252). 15% target fixed a
  priori (round-number, no tuning); **no leverage** (cap 1).
- **Execution:** signal at close, adjust at next open; **rebalance band** — trade only
  if |Δw| > 0.05 (avoids daily churn). **1 bp/side** (broad ETF tier); 5/15 bp stress.
- **Arms:** each base unmanaged vs vol-managed (4 arms) + QQQ buy-hold.

## Windows and verdict
- E6 base: gate 2000–2013 / secondary 2014→. E18 base: gate 2006–2013 (VIX3M floor).
- **PASS-RA (per base):** managed Sharpe ≥ 0.80 in gate AND > its unmanaged base in
  BOTH windows AND positive CAGR both. PASS-HR unreachable (exposure ≤ 1). **FAIL**
  otherwise. **DESCRIPTIVE label** (few independent stress episodes).

## Results-doc requirements
4 arms + buy-hold both windows; turnover/trade count; cost ladder 1/5/15 bp;
tripwire GREEN.

## Disclosed limitations
Low effective N; QQQ-only (market-dependence per E7); σ-target and band are single
a-priori constants; overlay = risk management, not the high-return goal.
