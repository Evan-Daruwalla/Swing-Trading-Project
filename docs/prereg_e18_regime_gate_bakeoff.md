# Pre-registration — E18: Regime-gate bake-off

**Written 2026-07-11 (CST), BEFORE any runner code. Committed doc-only; this
hash predates the runner. M7b task 33; D1 dual-bar verdict.**

## Provenance and prior

The data-type brief (`docs/research/2026-07-12_data_type_exploration.md`)
found the available non-OHLCV data types skew to regime gates, not return
engines. E18 pits four a-priori risk-on/off gates against each other as
**drawdown overlays** on a 1× equity sleeve (the E6 idea), to see if any
newer signal beats the plain 200-DMA gate E6 already uses. **Honest prior:**
overlays cannot clear PASS-HR (they hold cash part-time → sub-15% CAGR); the
only reachable pass is PASS-RA, and the real question is *risk-adjusted
improvement vs buy-hold and vs the 200-DMA benchmark*. If D1 had been
declined this task would be pointless — D1 was approved (Appendix AW).

## Base sleeve, gates, data

- **Base equity: QQQ** (E6's instrument), from `.e8e9_cache`. Risk-ON = hold
  QQQ; risk-OFF = cash. Signal at close, execute next open, 5 bps/side, full
  in/out, $1,000.
- **Four gates (risk-ON condition), all a-priori knobs:**
  - **(a) VIX term structure:** VIX / VIX3M < 1.00 (contango = calm).
    `^VIX`/`^VIX3M` via yfinance; **VIX3M starts 2006** → this arm evaluated
    2006→ only (disclosed).
  - **(b) HY credit spread:** BAMLH0A0HYM2 (FRED, keyless CSV, from 1996) <
    its trailing **252-trading-day median** (spreads below normal = risk-on).
    Forward-filled to trading days; publication is daily, no revision issue
    for OAS.
  - **(c) Breadth:** ≥ 50% of the available 29-ETF frozen universe trading
    above their own 200-DMA (self-computed from `.e8e9_cache`).
  - **(d) 200-DMA (benchmark):** QQQ close > its 200-DMA — the E6 gate, the
    line every other gate must beat.

## Evaluation and verdict

- Each gate run as its own overlay; compared head-to-head against **QQQ
  buy-hold** and against gate (d).
- **Overlay success (E6 criteria):** maxDD reduced by ≥ 10 pp vs QQQ-BH AND
  Sharpe ≥ QQQ-BH — required in BOTH the gate window (2000–2013, or 2006–2013
  for the VIX arm) and the secondary (2014→).
- **D1 tiers** also reported per gate: PASS-HR (CAGR ≥ 15% & maxDD ≤ 60% both
  windows — expected unreachable for overlays); **PASS-RA** (gate Sharpe ≥
  0.80 AND > SPY buy-hold both windows AND +CAGR both).
- **Bake-off verdict:** the winning gate is the one meeting the overlay
  criteria in both windows AND beating (d) on gate-window Sharpe; if none
  beats (d), the conclusion is "no new regime signal improves on the plain
  200-DMA overlay." No parameter changed after results. Interpretability
  floor: ≥ 20 risk-off episodes per gate in its evaluation window.

## Disclosed limitations

- VIX arm loses the 2000–02 crash (VIX3M from 2006) — weaker regime coverage;
  disclosed, not corrected.
- Breadth universe is 29 ETFs (fewer pre-2004), not the full market tape.
- Overlays by construction cannot pass PASS-HR; PASS-RA / the E6 overlay
  criteria are the operative bars. QQQ dividend-UNADJUSTED (biases the
  overlay/BH comparison neutrally).
