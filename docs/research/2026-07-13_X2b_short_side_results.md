# X2b — Short-side / long-short days-to-cover, borrow-costed: RESULTS

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Prereg:** `prereg_x2b_short_side.md` (committed `e718f6f`, doc-only, predates the
runner). **Runner:** `scripts/run_x2b_short_side.py`. **Verdict:** **FAIL** — the
short-side edge does not survive honest costs + a robustness bar. Frozen tripwire
GREEN.

---

## TL;DR (and a correction)

X2 flagged the short-interest anomaly as "the program's strongest real edge"
(long-short existence spread +18.39%, Sharpe 0.98). **X2b properly costs it — and
that framing was too generous.** With a fair delta-turnover trading model (5 bps/side)
and a borrow-fee sweep, the dollar-neutral long-short decays from a **frictionless
17.1% / Sharpe 0.92** to **9.2% / Sharpe 0.56 at a realistic 5% borrow**, and it is
**lumpy — only 5 of 9 calendar years positive.** The **pure short of high-DTC mega-caps
loses at every borrow level** (−2.1% even at zero borrow): the "most-shorted" basket is
a *mix* (IBM/TXN/ORCL rallied hard) and volatility drag punishes shorting volatile
names in a bull tape. Against the pre-registered market-neutral bar (at 5% borrow:
+CAGR **and** Sharpe ≥ 0.80 **and** ≥ 70% positive years) it is a clean **FAIL** —
even the most generous realistic case (0% borrow, Sharpe 0.82) fails the robustness
leg. **The short-side lead is closed: honestly costed, it is not a deployable
market-neutral edge, and the pivot away from the high-return-long goal is not worth
making.**

---

## Method

Per prereg: same FINRA short-interest cache + 39-name universe as X2. Two strategies,
K=5, biweekly rebalance, next-open fills, **5 bps/side trading on delta turnover only**
(continuers keep their shares — the first cut of this runner over-charged by churning
the whole book; fixed). **Real short accounting** (proceeds, daily-marked liability)
with a **borrow-fee sweep 0/2/5/10/20%/yr** on short market value, since real per-name
cost-to-borrow is paid data (Ortex, Evan-gated). Single 2018–2026 window →
MODIFIED-WINDOW CAP (PROMISING max). Market-neutral bar (SPY is the wrong benchmark for
a dollar-neutral sleeve): Sharpe ≥ 0.80 + positive CAGR + ≥ 70% positive years, all at
a realistic 5% borrow.

---

## Results (window 2018-01-16 → 2026-07-10; 2132 sessions, 204 cycles)

**Cost ladder + borrow sweep:**

| strategy | borrow | CAGR | maxDD | Sharpe |
|---|---:|---:|---:|---:|
| long-short **gross** (0 trading, 0 borrow) | — | 17.13% | 25.8% | 0.92 |
| long-short | 0% | 14.81% | 26.6% | 0.82 |
| long-short | 2% | 12.55% | 27.4% | 0.71 |
| long-short | **5%** | **9.24%** | 30.0% | **0.56** |
| long-short | 10% | 3.92% | 35.2% | 0.30 |
| long-short | 20% | −5.98% | 62.9% | −0.22 |
| long-short (15 bps trading) | 5% | 4.93% | 33.7% | 0.35 |
| **pure short** | 0% | **−2.10%** | 54.4% | −0.00 |
| pure short | 5% | −6.90% | 63.9% | −0.25 |
| pure short | 20% | −19.98% | 87.0% | −1.00 |

**Borrow breakeven (LS net CAGR → 0): 13.8%/yr.** **Robustness — per-year LS @ 5%
borrow (5/9 positive):** 2018 −8.4%, 2019 +23.4%, 2020 +5.3%, 2021 −5.7%, 2022 −8.8%,
2023 +31.3%, 2024 −9.5%, 2025 +29.3%, 2026 +34.5%.

**Short-leg (high-DTC) name concentration** — mean forward biweekly return while held:

| name | cycles held | ~annualized while held |
|---|---:|---:|
| IBM | 171 | **+7.2%** |
| TXN | 111 | **+17.8%** |
| MMM | 94 | −12.5% |
| T | 60 | −8.3% |
| CVX | 57 | +2.1% |
| ABT | 46 | −9.6% |
| ORCL | 42 | **+23.7%** |
| HD | 39 | −15.6% |

**Verdict:** LS @5% borrow = 9.24% CAGR (>0 ✓), **Sharpe 0.56 (< 0.80 ✗)**, **5/9 =
55% positive years (< 70% ✗)** → **FAIL.**

---

## Interpretation

- **The gross edge is real but frictionless.** LS gross 17.13% / Sharpe 0.92 ≈ X2's
  +18.39% existence spread — the anomaly *exists*. But it is a **market-neutral
  factor bet**, and honest costs matter: fair trading (~2.3 pp) plus a realistic
  large-cap borrow (2–5%) pull it to Sharpe 0.56–0.71. Only the unrealistic 0%-borrow
  case clears Sharpe 0.80 — and it fails robustness anyway.
- **Borrow is *not* the sole killer here.** Breakeven borrow is 13.8%/yr — far above
  the ~0.3–3% GC borrow these liquid mega-caps actually carry. So, unlike the
  Muravyev-Pearson-Pollet borrow-fee-proxy story (which bites in *illiquid* names),
  X2b fails on **risk-adjusted return + lumpiness**, not on borrow supply. The edge is
  real but not *good enough* net of ordinary frictions, and too concentrated in a few
  years (2019/2023/2025/2026 carry it; 2018/2021/2022/2024 lose).
- **"Short the most-shorted" does not work standalone.** The pure short is negative at
  every borrow level. The high-DTC basket is a **mix**: IBM (+7.2%), TXN (+17.8%),
  ORCL (+23.7%) *rallied* while held — being heavily shorted did not make them fall.
  Add volatility drag (shorting volatile names compounds against you even when they end
  roughly flat) and a bull tape, and the short leg is a loser. The long-short only
  "works" gross because the *long* low-DTC leg carries it, hedged to market-neutral.
- **This corrects X2's headline.** Calling the spread "the program's strongest real
  anomaly" over-weighted a zero-cost, zero-borrow number. Properly costed and
  robustness-tested, it is a **FAIL** — a lumpy market-neutral factor that clears no
  deployable bar. Better to find that with a $0 borrow sweep than after funding an
  Ortex subscription and a margin account.

## What this means for the "pursue the short-side" decision

**Don't.** The rigorous test says the short-side days-to-cover edge is not a robust,
deployable, market-neutral sleeve at this universe/window, and the pure short is
outright negative. Sizing up to a shorting-capable account for it is not justified by
the evidence. The one residual that *could* change this is genuinely Evan-gated and
low-priority: real per-name borrow + a broader/independent window + the illiquid names
the floor excludes (where the effect is strongest and the borrow-fee-proxy story
actually lives) — i.e., not reachable within the project's constraints.

## Honest caveats

- **Single 2018–2026 window**, survivor universe (lower-bounds the short leg —
  strengthens the FAIL). PROMISING-capped and failed anyway.
- **Borrow is swept, not measured**; the FAIL holds across the whole realistic range
  (breakeven 13.8% ≫ actual large-cap borrow), so paid borrow data would not rescue it.
- **Fractional shorts assumed** (no whole-share haircut) — an upper bound; real
  $1,000-account execution is worse.
- **Vol-drag / mixed-basket mechanism** for the negative pure short is inferred from
  the per-name table + return math, not separately decomposed.

## Reproduction

- `.venv\Scripts\python.exe scripts/run_x2b_short_side.py` → ladder, sweep, breakeven,
  per-year robustness, name concentration, verdict.
- Tripwire: `.venv\Scripts\python.exe -m swing_bot.test_frozen` → GREEN (12 refs d=0).

## Sources (dated)

- Muravyev, Pearson, Pollet — *Why Does Options Market Information Predict Stock
  Returns?* (JFE 2025) — short-side predictability as a borrow-fee proxy.
- Boehmer, Huszar, Jordan — *The Good News in Short Interest* (JFE 2010).
- X2 results `docs/research/2026-07-13_X2_days_to_cover_results.md`; prereg
  `prereg_x2b_short_side.md`; record Appendix BV.
