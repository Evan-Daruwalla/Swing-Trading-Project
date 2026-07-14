# Pre-registration — X6: Crypto BTC/ETH time-series trend (paper-first)

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M9 task 50 (Evan authorized the crypto scope via "do 2",
2026-07-14). Written against `docs/prereg_TEMPLATE.md`. MODIFIED-WINDOW CAP +
new-domain (crypto) — see Windows. NON-EQUITY: extends, does not contradict, the
"equity method space exhausted at 30 attempts" terminal claim.**

## Provenance and prior

Liu-Tsyvinski (2021 RFS): 1–4 week crypto return predictability. Grayscale *The Trend
Is Your Friend* (survivorship-free BTC, 20/100 MA): Sharpe 1.7 vs 1.3 HODL. The crypto
feasibility brief (2026-07-13) recommended exactly this: a **liquid-only, paper-first,
time-series-trend** pilot on the majors, pre-registered at **crypto fees**. **H1:** a
dual-MA trend sleeve on BTC/ETH beats HODL on Sharpe and cuts the ~80% HODL drawdown.
**H0:** trend timing adds no risk-adjusted value net of 25 bps/side and whipsaws in
range-bound tape. **Honest prior: uncertain, leaning FAIL/PROMISING-weak** — the
documented edge is real but (a) 25 bps/side (5× the equity model) is the governing
economic fact, (b) TS-momentum went **negative in the choppy 2022–23** tape (pre-
registered as an EXPECTED drawdown, not a tuning target), (c) BTC/ETH are the two
survivor majors → survivorship-flattered *absolute* returns (the sleeve-vs-HODL delta
is the survivorship-robust read).

## Data (probed 2026-07-14)

- **BTC-USD** (4,319 bars from 2014-09-17) and **ETH-USD** (3,170 bars from 2017-11-09)
  daily via yfinance, `auto_adjust=False` (crypto has no splits/dividends → close is
  actual). **24/7 daily bars** (weekends included). Cached to `.crypto_cache/`
  (gitignored). No swing.db writes.
- **No overnight gap by construction:** a UTC daily bar is an arbitrary cut of a
  continuous market; signal at bar-close → execute next bar's open is mechanically
  clean (the one structural advantage over the equity EOD loop).

## Exact rules (fixed a priori)

- **Universe:** BTC, ETH (liquid majors only — the liquidity floor excludes the alt
  universe where survivorship/wash-trading inflate backtests 17–50%/yr).
- **Signal (PRIMARY):** per asset, **long when SMA(20) > SMA(100)** (Grayscale dual-MA
  trend), **flat** otherwise. Signal at daily close, **execute next bar's open**.
  Sensitivity arm (reported, not the verdict): single **100-day MA** long-or-flat.
- **Sleeves:** BTC sleeve, ETH sleeve, and an equal-weight **K=2 combined** book. Long-
  or-flat only (no shorting, no leverage). Size = full sleeve capital per asset.
- **Costs [crypto tier]:** **25 bps/side** (Alpaca crypto taker — the realistic live
  number). Report a 10 bps/side (aggressive-venue) and 50 bps/side (Coinbase-ish)
  stress. **Time-stop baseline:** the MA-cross IS the exit; no price stop.

## Windows and verdict [MODIFIED-WINDOW CAP + paper-first]

- **Gate 2018-01-01 → 2022-12-31** (two crypto bears — 2018 post-bubble + 2022 winter —
  plus the 2020–21 bull; a real regime mix). **Secondary 2023 → end.** Post-2000,
  crypto-only, single domain → **best achievable = PROMISING; PASS-HR/RA NOT
  claimable.** Floor: the sleeve must toggle (≥ 10 regime changes in gate).
- **Benchmark = HODL** (buy-and-hold each asset — the survivorship-robust comparison).
  **PROMISING** iff the K=2 combined trend sleeve, at **25 bps/side**, beats HODL on
  **Sharpe in BOTH windows** AND cuts gate maxDD by **≥ 20 pp** vs HODL AND has
  positive CAGR both. **FAIL** otherwise.
- **Paper-first [STANDING crypto]:** a PROMISING routes to **paper only** (Alpaca crypto
  paper sandbox); **live-money crypto is a separate Evan-gated decision** whose deciding
  risk is custody (100% of capital uninsured on an exchange). Nothing live here.

## Results-doc requirements
BTC/ETH/combined sleeves vs HODL, both windows (CAGR/maxDD/Sharpe/exposure%); the
25 bps verdict + 10/50 bps stress; the 100-day sensitivity arm; the 2022–23 drawdown
called out; frozen tripwire GREEN (unaffected — no swing.db/frozen-ref touch).

## Disclosed limitations
- **25 bps/side is the governing economics** — an edge that only clears at equity fees
  is a FAIL for a live crypto arm.
- **Survivor majors** (BTC/ETH) → absolute CAGR is upper-bound-biased; the sleeve-vs-
  HODL delta is the honest read.
- **Single crypto domain, modified window** → PROMISING-capped; paper-first.
- **2022–23 whipsaw drawdown is pre-registered as expected**, not a failure to tune away.
- yfinance crypto close quality (exchange-blend) is adequate for daily trend, not tick-
  precise; no borrow/funding/perp leg (spot long-or-flat only).
