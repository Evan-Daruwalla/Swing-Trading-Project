# X6 — Crypto BTC/ETH time-series trend (paper-first): RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_x6_crypto_trend.md` (doc-only, predates runner). **Runner:**
`scripts/run_x6_crypto_trend.py`. **Verdict: FAIL (PROMISING-capped).** Frozen tripwire
GREEN. The program's first crypto-domain experiment (attempt 31 = 30 equity + 1 crypto).

## TL;DR

A BTC/ETH dual-MA trend sleeve (SMA20 > SMA100, long-or-flat, next-bar, 25 bps/side)
**crushes buy-and-hold in the bear-heavy 2018–2022 gate** — combined 29.6% CAGR vs
HODL 4.3%, Sharpe 0.76 vs 0.43, drawdown cut 82% → 61% — but **loses to HODL's raw
Sharpe in the 2023+ bull** (0.76 vs **1.01**), so it fails the pre-registered
beat-HODL-on-Sharpe-in-**both**-windows bar. Two findings matter more than the FAIL:
(1) it is **cost-robust** — 33 regime toggles over 5 years means 25 bps barely bites
(gate CAGR 30.3% at 10 bps → 28.6% at 50 bps), refuting the a-priori "crypto fees kill
it" worry *for a slow trend overlay*; (2) crypto trend is a **drawdown-control overlay,
not a return-enhancer over HODL in bull regimes — the same conclusion as equity E6, now
confirmed in a new asset class.** Stepping outside equities did not escape the program's
structural finding.

## Results (BTC 2014-09+, ETH 2017-11+; dual-MA SMA20>SMA100, 25 bps/side)

| sleeve | window | trend CAGR / DD / Sharpe | HODL CAGR / DD / Sharpe |
|---|---|---|---|
| BTC | gate 2018–22 | 23.07% / 64.4% / 0.67 | 3.91% / 81.5% / 0.43 |
| BTC | sec 2023– | 23.26% / 41.1% / 0.76 | 46.67% / 53.1% / **1.05** |
| ETH | gate | 26.85% / 71.5% / 0.70 | 9.14% / 94.0% / 0.58 |
| ETH | sec | 19.79% / 44.4% / 0.64 | 13.29% / 67.6% / 0.51 |
| **COMBINED K=2** | **gate** | **29.61% / 60.6% / 0.76** | 4.34% / 82.3% / 0.43 |
| **COMBINED K=2** | **sec** | **23.09% / 41.5% / 0.76** | 44.31% / 53.7% / **1.01** |

**Cost stress (combined):** 10 bps gate 30.26% / Sh 0.77 → 25 bps 29.61% / 0.76 →
50 bps 28.55% / 0.75 — **essentially flat** (low turnover). **Sensitivity (100-day
single MA, NOT the pre-registered primary):** looked *better* (BTC-100d gate Sharpe
0.90, sec 0.95) but still loses HODL's 1.05 in the bull — the FAIL is robust across
specs; I do not switch the verdict to the better-looking arm (that is tuning a FAIL).

**Verdict:** combined sleeve beats HODL Sharpe in the gate (0.76 > 0.43) but **not the
secondary (0.76 < 1.01)** → fails the both-windows bar → **FAIL**. (33 gate toggles ≫
10 floor; DD cut 21.8 pp ✓; +CAGR both ✓ — it fails *only* on the bull-market Sharpe.)

## Interpretation

- **Trend timing is regime-dependent, exactly as documented.** It triples HODL's return
  and cuts an 82% drawdown to 61% across the 2018/2022 bears — genuinely valuable
  drawdown control — then gives back the edge in the 2023–25 bull, where simply holding
  wins on Sharpe (you're flat during the pullbacks that immediately recover). This is
  the Grayscale/Moskowitz-Ooi-Pedersen trend signature, and the prereg pre-registered
  the choppy-tape underperformance as an *expected* mode.
- **The fee worry was misplaced for THIS strategy.** The crypto feasibility brief's
  governing concern — 25 bps/side (5× equity) — assumed a taker-heavy cadence. A
  slow 20/100 MA overlay toggles ~6×/yr, so fees are a rounding error (28.6% even at
  50 bps). The fee wall is real for high-frequency crypto, not for trend.
- **Same terminal lesson, new domain.** In equities the only survivor was E6 — a 1×
  MA rotation that is a *market-dependent risk-management overlay, not a high-return
  engine*. Crypto reproduces this precisely: MA trend = drawdown control that loses to
  buy-and-hold in bulls. The program's structural conclusion generalizes beyond
  equities.
- **Honest caveat on the gate "win":** BTC/ETH are the two survivor majors — their
  long-run compounding is survivorship-flattered. The *sleeve-vs-HODL delta* is the
  survivorship-robust read, and it says "better in bears, worse in bulls," i.e. a
  timing overlay, not alpha.

## Routing

Per the prereg, a PROMISING would have routed to **paper only**; this is a FAIL, so
even that does not apply. Crypto trend is not a high-return engine at 25 bps; its
drawdown-control value is real but is the same non-goal E6 already occupies.
**Live-money crypto remains Evan-gated regardless** (custody = the deciding,
undiversifiable risk). No live or paper deployment authorized here.

## Honest caveats

- **Single crypto domain, modified window** (2018–2025), PROMISING-capped by design.
- **Survivor majors** → absolute CAGR upper-bound-biased (delta is the honest read).
- **Spot long-or-flat only** — no funding/perp/borrow leg; yfinance daily close is an
  exchange blend (adequate for daily trend, not tick-precise).
- **2022–23 whipsaw** was pre-registered as expected; the FAIL is driven by the 2023+
  *bull* (HODL Sharpe), not the 2022 bear (where the sleeve won).

## Reproduction
`.venv\Scripts\python.exe scripts/run_x6_crypto_trend.py` (yfinance BTC-USD/ETH-USD,
`.crypto_cache/`, gitignored). Tripwire GREEN (12 refs d=0, unaffected — new domain).

## Sources
Liu & Tsyvinski — *Risks and Returns of Cryptocurrency* (2021 RFS); Grayscale — *The
Trend Is Your Friend*; crypto feasibility brief `docs/research/2026-07-13_crypto_feasibility.md`;
equity E6/E7 rotation results.
