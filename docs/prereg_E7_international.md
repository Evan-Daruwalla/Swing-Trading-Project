# Pre-registration — E7: international validation (unseen regimes)

**Committed 2026-07-10 (PRD M2e), BEFORE the E7 runner exists. Parameters
FIXED. This is the clean-data unlock: US backtest regimes are exhausted
(record Appendix AE), so E7 tests on GENUINELY UNSEEN non-US indices — above
all the 1990s–2000s Japan secular bear, the most hostile trend-rotation
regime in modern history.**

## 0. Honesty disclosures

1. **The non-US data has never been examined for this project** — Nikkei,
   DAX, FTSE, Hang Seng, ASX are first looked at by the E7 runner, AFTER this
   commit. This is as close to a clean out-of-sample test as exists short of
   live paper.
2. **Arm 2's two free knobs are fixed A PRIORI, not fit to any data:**
   - Vol-gate threshold = **30% annualized**, from first principles: a 3×
     fund on a 30%-vol index runs ~90% position vol, the practical prudence
     ceiling; above it, 3× leverage is imprudent regardless of trend. NOT
     chosen to survive any observed crash.
   - Synthetic drag = **5%/yr** (no real deep-history international 3× fund
     exists to calibrate against; 5% is slightly more conservative than the
     4%/yr calibrated to real TQQQ in E5). Reported with 3%/7% sensitivity.
3. **Local-currency price indices** are used (returns in local terms):
   isolates the rotation MECHANICS from currency noise — the right choice for
   a robustness test, not a tradeable. Price indices EXCLUDE dividends, so
   all E7 returns UNDERSTATE total return by ~2–3%/yr (conservative). A real
   USD deployment would add currency + dividend effects; flagged, out of
   scope for E7.

## 1. Markets (fixed)

Non-US test set: **^N225 (Nikkei, from 1985), ^GDAXI (DAX), ^FTSE, ^HSI
(Hang Seng), ^AXJO (ASX 200)**. Cross-check (reported, not gated): ^GSPC
(S&P 500 index). Full available history each; **Nikkei is the make-or-break
market** (contains the 20-year post-1989 bear).

## 2. Two arms & rules (fixed)

Shared: signal = the index's own close vs its 200-day SMA; switch at next
open; 5 bps/side; identical rotation mechanics to E4/E6.

- **Arm 1 — confirm E6 (1× drawdown overlay):** position = the index itself
  (1×). Tests whether E6's US result generalizes.
- **Arm 2 — a-priori vol-gated 3× (high-return shot):** position = synthetic
  daily-rebalanced 3× of the index (drag 5%/yr). Hold 3× only when
  `close > SMA200` **AND** `20d annualized realized vol < 30%`; else cash.

Benchmarks per market: buy-and-hold 1× index (both arms); buy-and-hold
synthetic-3× and plain-3×-rotation-without-vol-gate (Arm 2 context).

## 3. Kill criteria (fixed)

**Arm 1 PASSES** if, in **≥ 4 of the 5** non-US markets, 1×-rotation shows
BOTH: maxDD ≤ buy-hold-index maxDD − 10 pp, AND annualized Sharpe ≥
buy-hold-index Sharpe. (E6's drawdown-overlay value generalizes globally.)

**Arm 2 PASSES** (the high-return-AND-robust test) only if ALL:
1. Positive CAGR in ALL 5 non-US markets (survives every regime).
2. maxDD ≤ 70% in ALL 5 markets (ruin guard for 3×).
3. **Nikkei CAGR > 0 AND Nikkei maxDD ≤ 70%** (the make-or-break: positive,
   bounded return through the worst secular bear on record).
4. Mean CAGR across the 5 markets ≥ 15% (the high-return bar, matching
   E2/E4).

If an arm misses any of its criteria → that arm FAILS. No tuning; thresholds
and the 30%/5% knobs are frozen here.

## 4. Disposition

- **Arm 2 PASS** → a leverage strategy that is high-return AND survives the
  most hostile unseen regime in equity history, on data never used to design
  it — the first genuine high-return-robust candidate the project has found.
  Promote to the M3 live-paper gate (Evan + Alpaca).
- **Arm 2 FAIL** → the high-return-AND-robust question is CLOSED with
  confidence; no leverage-timing strategy clears the bar.
- **Arm 1 PASS** → E6 (1×) is validated as a globally-robust drawdown
  overlay, strengthening it as the deployable risk-managed core.
- **Arm 1 FAIL** → E6 was US-specific; downgrade it.

Live paper remains the only true forward test regardless of E7 outcome.

## 5. No-change clause

§§1–3 frozen as of this commit. Ambiguities resolve to the most literal
reading, recorded, never toward better numbers. Any change is a new dated
pre-registration.
