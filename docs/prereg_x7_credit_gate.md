# Pre-registration — X7: HYG:IEF credit-appetite regime gate

**Written 2026-07-15 (CST), BEFORE any backtest runner code. Committed doc-only;
this hash predates the runner.** Completeness kill-shot opened by Evan (2026-07-15)
after the BlackRock systematic-HY report (record Appendix CU). D1 dual-bar verdict,
**MODIFIED-WINDOW → capped at PROMISING** (data starts 2007). Not survivor-biased
(ETF market signal) → interpretable in both directions.

## Provenance and prior

The BlackRock "systematic approach to high yield credit" report (2025) argues credit
risk-appetite regimes drive returns. Credit markets are widely claimed to LEAD equities
into stress (spreads widen before equities break). **E18 already tried to test a credit
gate** — its HY-OAS arm (FRED BAMLH0A0HYM2) was INCONCLUSIVE because free FRED OAS history
only ran ~2023+. **X7's novelty: the HYG:IEF price ratio is a free, tradeable proxy for the
same credit-spread signal, available back to 2007-04-11** (probed 2026-07-15: HYG 2007-04-11→,
IEF 2002-07→; ratio collapses correctly in stress — 1.27 calm 2007 → 0.95 GFC Oct-2008 →
0.63 COVID Mar-2020). So X7 finally tests the credit-regime gate E18 could not.

**Working hypothesis H1:** a credit-appetite gate (long QQQ when HYG:IEF > its trailing
200-DMA, else cash) beats the plain QQQ 200-DMA overlay by de-risking EARLIER in credit
stress (esp. 2008) → cuts more drawdown at equal-or-better Sharpe. **Rival/null H0:** the
credit gate is just another risk-on/off proxy correlated with QQQ's own 200-DMA and adds
nothing incremental.

**Honest prior: FAIL / no improvement.** E18's whole finding was that NO regime gate
(VIX-TS, HY-OAS, breadth) beat the plain 200-DMA overlay on the robust both-windows
criterion; X1 (conditional vol-targeting) confirmed it. Credit-appetite and equity-trend are
both risk proxies, so the gate likely duplicates the 200-DMA signal. The one way H1 wins is
if credit genuinely leads — a real, falsifiable mechanism, which is why it is worth one
sitting. **This is an overlay → PASS-HR is unreachable (overlays can't clear 15% CAGR); the
substantive test is whether it BEATS the incumbent 200-DMA overlay.**

**[STANDING] asymmetric note:** unlike the survivor-stock experiments, this gate is a
market-wide ETF signal on QQQ — NOT survivor-biased → a pass is interpretable (not
auto-uninterpretable), though still **PROMISING-capped** by the post-2000 window and
forward-paper-routed, never a live claim on its own.

## Data (probed 2026-07-15)

- **Source & access:** HYG, IEF, QQQ, SPY via `.e8e9_cache` (`run_e8_squeeze.cache_fetch`,
  yfinance). Coverage confirmed: HYG 4,844 bars 2007-04-11→2026-07-13; IEF from 2002-07;
  QQQ from 1999. No NEW data source (no probe-blocker). Cache gitignored; runner does **no
  swing.db writes**.
- **Adjustment convention [STANDING]:** split-adjusted, dividend-UNADJUSTED
  (`auto_adjust=False`). NOTE: HYG/IEF are dividend-heavy (bond ETFs) → dividend-UNADJUSTED
  closes understate their total return, so the RATIO is a price-only credit-risk signal, NOT
  a total-return series — which is fine and CORRECT here (we use it only as a regime signal,
  never trade the bonds). Disclosed. QQQ is the traded instrument (also div-unadj, minor).
- **Point-in-time / lookahead:** ratio and its 200-DMA computed on closes through day t;
  gate decided at close t, QQQ executed at **next open t+1** [STANDING EOD rule]. Both ETFs
  are liquid and trade the same sessions as QQQ (no alignment gaps in-window).
- **Universe & liquidity floor [STANDING]:** the traded instrument is QQQ (broad ETF, far
  above ADV ≥ $5M ∧ price ≥ $5). HYG/IEF are signal-only. Floor satisfied by construction.

## Exact rules (fixed a priori)

- **Signal:** `ratio[t] = HYG_close[t] / IEF_close[t]`, aligned to QQQ session dates.
  `ma[t] = 200-session SMA of ratio` (200 pinned from the program's standing 200-DMA
  convention — E6/E18 — NOT tuned). **risk_on[t] = ratio[t] > ma[t]** (credit appetite ON →
  HY outperforming Treasuries). None before 200 valid ratio observations exist.
- **Sleeve / entry-exit:** long QQQ 1× when risk_on, else cash. Signal at close, **execute
  next open** [STANDING]. No K (single-index overlay, as E18). No leverage.
- **Sizing [STANDING]:** full-notional QQQ-or-cash (an overlay, not a sized book); no Kelly/
  fractional-risk parameter applies. Frozen here.
- **Time-stop [STANDING]:** N/A — a regime overlay holds until the gate flips (the honest
  baseline for an overlay is the gate itself; no price-stop arm).
- **Costs [STANDING tiered]:** QQQ = broad-index ETF → **1 bp/side** primary. Decomposition
  ladder required: Rung A (c2c, 0 bp) / Rung B (next-open, 0 bp) / Rung C (next-open, 1 bp).
  **15 bp/side stress leg** reported (overlays are low-turnover, so cost should barely bite —
  if 15 bp changes the verdict, that is itself the finding).

## Windows and verdict [STANDING D1 dual-bar, PROMISING-capped]

- **Gate 2007-04-11 → 2013-12-31** (the widest the HYG data supports; CONTAINS THE 2008 GFC,
  the premier credit-stress event — so the gate is meaningful even though it misses 2000-02).
  **Secondary 2014-01-01 → end.** Floor: gate spans ~6.7 yrs; report the gate switch count
  descriptively (an overlay's "N").
- **[STANDING] MODIFIED-WINDOW CAP:** the gate cannot cover 2000-2013 → **best achievable
  verdict = "PROMISING — needs forward confirmation."** X7 may NOT claim PASS-HR or PASS-RA.
- **Substantive test (the real question, since PASS-HR is unreachable for an overlay):**
  X7 = **PROMISING** iff it clears BOTH of the E6/E18 overlay criteria in BOTH windows —
  (i) maxDD cut ≥ 10 pp vs QQQ buy-hold, (ii) Sharpe ≥ QQQ buy-hold — **AND** its **gate
  Sharpe beats the plain QQQ 200-DMA overlay's** (E18 arm d, the incumbent to beat).
  Otherwise **FAIL**.
- **Also reported (capped):** PASS-RA-equivalent (gate Sharpe ≥ 0.80 AND > SPY-BH both
  windows AND +CAGR both) and PASS-HR-equivalent (expected fail). Benchmarks: QQQ-BH, SPY-BH,
  plain QQQ 200-DMA overlay.
- **No parameter changes after results; a FAIL is never re-tuned.** A faster ratio-MA (e.g.
  50-day) may be reported as a DESCRIPTIVE sensitivity only — it does NOT change the
  pre-committed 200-DMA verdict.

## Results-doc requirements [STANDING]

- The A/B/C decomposition ladder + 15 bp stress on the headline.
- The verdict with criteria echoed; the head-to-head vs the plain 200-DMA overlay and vs
  QQQ-BH/SPY-BH; the gate switch count; and **frozen tripwire GREEN**
  (`.venv\Scripts\python.exe -m swing_bot.test_frozen`, 12 refs d=±0.0000pp) run AFTER.

## Disclosed limitations

- **Modified window (load-bearing):** starts 2007 → misses 2000-02; verdict capped at
  PROMISING; a pass is forward-paper-routed, never live.
- **Correlated-signal risk:** credit-appetite and equity 200-DMA may be near-duplicates →
  the gate may add nothing over the incumbent (the null). Expected.
- **Dividend-UNADJUSTED bond ETFs:** the ratio is price-only (not total return) — correct for
  a regime signal, disclosed; not a tradeable HY return.
- **Overlay, not a return engine:** cannot clear PASS-HR by construction; this extends the
  E18/X1 "no gate beats 200-DMA" finding to the credit channel (or, if H1 wins, is the first
  gate that does — PROMISING, forward-paper only).
