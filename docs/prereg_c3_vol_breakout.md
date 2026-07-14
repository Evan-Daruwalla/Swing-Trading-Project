# Pre-registration — C3: Consolidated volatility-breakout kill-shot

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M8 task 38 (Evan authorized the free sweep 2026-07-14).
Written against `docs/prereg_TEMPLATE.md`. D1 dual-bar verdict.**

## Provenance and prior

Donchian channels / Bollinger squeeze / ATR breakouts are the canonical retail
chart-pattern family; Moskowitz-Ooi-Pedersen (2012) document time-series momentum in
*futures*. **One consolidated spec** is pre-registered here (squeeze → channel-high
entry → channel-low/time exit) to avoid multiple-testing snooping across the ~dozen
near-identical variants. **H1:** compression-then-breakout carries directional edge on
liquid ETFs. **H0 (expected):** it dies on equities after honest costs —
Sullivan-Timmermann-White (1999) and Bajgrowicz-Scaillet (2012) show technical rules
fail after snoop-correction + costs, and this program already killed the components:
E8 (squeeze alone: compression predicts expansion, not direction, gate CAGR −1.43%)
and E11 (volume-gated breakout adds nothing). **Honest prior: near-certain FAIL — this
is an explicit kill-shot to close the breakout/chart-pattern family, not a hopeful
engine.**

## Data (in hand)

- 29-ETF frozen universe (`swing_bot.universe`), OHLCV via `.e8e9_cache`
  (split-adjusted, dividend-UNADJUSTED). Later-inception ETFs (XLRE 2015, XLC 2018,
  some country ETFs) enter when their history exists — disclosed. No swing.db writes.

## Exact rules (fixed a priori)

- **Squeeze:** 20-session realized vol (stdev of daily returns) is **below its median**
  over the trailing 252 sessions, evaluated on the session *before* the breakout.
- **Entry signal:** close = highest close of the trailing 20 sessions AND the squeeze
  condition held on the prior session. Signal at close → **buy next open**.
- **Exit:** close < lowest close of the trailing 10 sessions → sell next open; OR
  **time stop 40 sessions**; whichever first. (Time-stop baseline: an arm with the
  time stop ONLY — no channel-low exit — is reported alongside; the channel exit must
  beat it to claim value.)
- **K = 5** concurrent; earliest-signal first, ties alphabetical; one position per
  ticker; size = min(cash, NAV/5); **5 bps/side** (conservative ≥ tiered model for the
  broad ETFs); $1,000 start.

## Windows and verdict [D1 dual-bar]

- **Gate 2000-01-01 → 2013-12-31**; **secondary 2014 →**. Floor ≥ 30 gate entries.
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60%, both windows. **PASS-RA:** gate Sharpe
  ≥ 0.80 AND > SPY-BH both windows AND +CAGR both. **FAIL:** neither. Benchmarks:
  SPY-BH and EW-29-universe. No parameter changes after results.

## Results-doc requirements

Decomposition ladder (A c2c 0bps / B next-open 0bps / C next-open 5bps) + 15 bps
stress + time-stop-only arm + frozen tripwire GREEN.

## Disclosed limitations

- Consolidated single spec (by design); parameters (20/10/40/K=5) fixed a priori from
  the canonical Donchian/turtle construct, not tuned.
- ETF universe is survivorship-light (ETFs don't delist like stocks) but
  later-inception names thin the early gate window.
- 5 bps flat is conservative for SPY/QQQ/DIA/IWM (tiered model would charge 1 bp).
