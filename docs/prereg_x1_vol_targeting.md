# Pre-registration — X1: Conditional volatility targeting (E6 × E18 interaction)

**Written 2026-07-13 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M9 task 45. Written against `docs/prereg_TEMPLATE.md`.
OVERLAY test → PASS-RA is the only reachable tier, and per the low-effective-N caveat
ANY verdict is labelled DESCRIPTIVE (forward paper is the real grade).**

## Provenance and prior

Moreira-Muir (FAJ 2017/2020) volatility-managed portfolios: scaling exposure inverse
to volatility adds ~0.16 Sharpe / cuts drawdown on momentum/market factors. The
project's own results motivate a *conditional* form: E6 (200-DMA rotation) cuts
drawdown but is market-dependent; E18's VIX-TS gate cleared a *weak* PASS-RA but has
**worse drawdown than buy-hold in bull markets** because it de-risks on *any* vol
spike, including spikes inside an intact uptrend. **Working hypothesis (H1):** a
conditional rule that de-risks **only when volatility is elevated AND trend is broken**
— staying invested when vol spikes inside an uptrend — beats *both* E6-alone and
E18-alone on risk-adjusted return. **Null (H0):** the interaction adds nothing beyond
the plain 200-DMA overlay (consistent with E18's finding that no gate beats the 200-DMA
on the robust both-windows criterion). **Honest prior: FAIL/weak** — a single gate
window with essentially one crash (2008) means low effective N; even a "pass" is
descriptive.

## Data (in hand)

- SPY OHLCV from `.e8e9_cache` (split-adjusted, dividend-UNADJUSTED). No swing.db writes.
- `^VIX`, `^VIX3M` daily close via `macro_close` (yfinance, cached; VIX3M starts 2006).
- No new data; no probe needed.

## Exact rules (fixed a priori)

- **Instrument:** SPY only, exposure ∈ {0, 1} (long or flat). Signal at close, execute
  **next open**. **1 bp/side** (broad-index ETF, tiered-cost model); 5 bp and 15 bp
  stress legs reported.
- **Three arms** (arms a/b are SPY re-baselines, not the exact E6/E18 runs which were
  QQQ):
  - **(a) E6-alone:** exposure = 1 iff SPY close > SPY 200-DMA, else 0.
  - **(b) E18-alone:** exposure = 1 iff VIX/VIX3M < 1, else 0.
  - **(c) Conditional (the test):** exposure = 0 iff (VIX/VIX3M > 1 **AND** SPY close <
    200-DMA), else 1. (De-risk only when BOTH vol elevated and trend broken.)
- **Benchmark:** SPY buy-hold. **Time-stop / sizing:** N/A (binary exposure overlay,
  no leverage).

## Windows and verdict [OVERLAY → DESCRIPTIVE]

- **Gate 2006–2013** (VIX3M floor; disclosed — one major crash → low effective N).
  **Secondary 2014→.** Floor: the overlay must actually toggle (≥ 10 exposure changes
  in gate).
- **PASS-HR is not reachable** (exposure ≤ 1 → return ≤ SPY; a leverage-free overlay
  cannot clear a 15% high-return bar in these windows). **Reachable tier = PASS-RA:**
  arm (c) Sharpe ≥ 0.80 AND > SPY buy-hold Sharpe in BOTH windows AND positive CAGR
  both AND maxDD cut ≥ 10 pp vs buy-hold in the gate — **AND** arm (c) beats BOTH arm
  (a) and arm (b) on gate Sharpe (the interaction must earn its keep). **FAIL**
  otherwise.
- **DESCRIPTIVE label [STANDING low-N]:** with ~3–5 independent stress episodes in the
  whole sample, ANY verdict here is descriptive — **forward paper is the real grade**;
  a PASS-RA is a forward-paper candidate only, never a live claim. PASS-HR stays 0
  regardless.

## Results-doc requirements

- The three arms + SPY buy-hold, both windows, with CAGR / maxDD / Sharpe / exposure-%
  / toggle count; the 5 bp and 15 bp stress legs; the decomposition is trivial here
  (overlay, no cross-sectional selection) so report next-open vs the 1/5/15 bp ladder.
- Frozen tripwire GREEN after.

## Disclosed limitations

- **Low effective N** — one gate window, ~one crash → descriptive only.
- **Single index (SPY)** — no cross-market generalization (E7 showed 200-DMA overlays
  are market-dependent); this is a US-only interaction test.
- **VIX3M floor 2006** — the gate is 2006–2013, not the full 2000–2013 hostile window.
- Overlay class → **risk-management, not the high-return goal**; a pass routes to the
  same forward-paper bucket as E6/E18, not to a live high-return claim.
