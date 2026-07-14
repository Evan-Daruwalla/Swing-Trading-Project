# Pre-registration — M10-1: Nagel Switch (VIX-gated reversal / trend)

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. M10 synthesis arc (Evan: "using all the data... come up with
strategies to see if they meet both criteria"). Written against
`docs/prereg_TEMPLATE.md`. D1 dual-bar verdict.**

## DATA-SNOOPING DISCLOSURE [binds this and every M10 prereg]

This design is composed AFTER seeing 31 prior results on these exact two windows. It
reuses components (C1, E6) chosen *because* they were the gate-alive / secondary-alive
survivors. That is severe multiple-testing. The mitigations: (a) the switching variable
(VIX level) is set by a **published, pre-2012 mechanism** (Nagel 2012), not fit to our
windows; (b) every parameter is inherited verbatim from an already-committed prereg or
is a canonical constant, with exactly ONE new number (VIX threshold 20.0); (c) **any
in-window pass is recorded "IN-SAMPLE-COMPOSED — forward paper REQUIRED," never a clean
PASS or a live claim.** C1's own prereg already declared its survivor-universe results
UNINTERPRETABLE; this composite inherits that ceiling.

## Provenance and prior

Program fact: the two real edges are window-disjoint — C1 residual reversal is
gate-alive/secondary-dead (19.08% → 2.92% CAGR), trend rotation is secondary-alive/
gate-weak (E6 2.66% → 14.47%). Fixed-weight blends are arithmetically infeasible for
PASS-HR (gate forces C1-weight ≥ 0.66, secondary ≤ 0.29 — empty). **Nagel (2012,
"Evaporating Liquidity", RFS):** short-term reversal profit is compensation for
liquidity provision and **scales with VIX** — when VIX is high, arbitrage capital
withdraws and the reversal premium spikes; when low, it is competed to ~zero. This
predicts *both* C1's gate success (high-VIX 2000-02/2008-11) and its post-2014 death
(structurally low VIX). **H1:** routing to reversal only when VIX > 20 and to trend
otherwise clears both tiers (or comes closest). **Rival/null H0 (the judges' consensus
flag):** C1's reversal died *temporally* (McLean-Pontiff arbitrage crowding), not by
VIX-state — then conditioning cannot resurrect it post-2014 and the secondary CAGR lands
~10-13% (HR FAIL). **Honest prior: gate-HR plausible, secondary-HR likely near-miss →
most probable outcome PROMISING, not a clean double-pass.**

## Data (in hand)

- 39-survivor daily OHLCV cache (`run_e10_earnings_drift.UNIV`, split-adjusted,
  dividend-UNADJUSTED, READ-ONLY); FF3 daily factors (cached French lib); QQQ; **^VIX
  daily close (cached via `macro_close`, 1990+ — full gate coverage, no VIX3M/2006
  floor, so NO modified-window cap)**. No swing.db writes.

## Exact rules (fixed a priori)

- **Regime (weekly):** at each ISO-week-end close, read ^VIX close. **VIX > 20.0 →
  STRESS (reversal mode) next week; VIX ≤ 20.0 → CALM (trend mode) next week.** Mode
  applies from the next session's open through the following week's decision. Signals at
  close, execution next open, cash earns 0% (program convention).
- **STRESS = C1 verbatim:** for each survivor with ≥ BETA_N(126) FF3-aligned sessions
  passing the floor (close ≥ $5, 20-day dollar ADV ≥ $5M), OLS of daily returns on
  (Mkt-RF, SMB, HML, const) over trailing 126 sessions; rank by sum of last 21 daily
  residuals; **buy bottom K=4** (most negative) equal-weight at next open; hold one week;
  full weekly rebalance; **5 bps/side**.
- **CALM = E6 trend verbatim:** long QQQ iff QQQ close > 200-session SMA of QQQ close,
  else 100% cash; **1 bp/side**.
- **Mode switch:** liquidate outgoing at the next open, enter incoming at the same open;
  each leg pays its own side's cost. Never simultaneous (≤ 4 stocks OR 1 ETF; K ≤ 5 ok).
- **No leverage anywhere.** Long-only.

## Windows and verdict [D1 dual-bar]

- **Gate 2000-01-01 → 2013-12-31; secondary 2014-01-01 → end.** Floor ≥ 30 stress-mode
  entries in the gate. **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60%, both windows.
  **PASS-RA:** gate Sharpe ≥ 0.80 AND > SPY-BH both windows AND +CAGR both. Benchmarks
  SPY-BH + EW-39. **No parameter changes after results; a FAIL is never re-tuned.**
- **Snooping cap:** a numerical PASS is reported "IN-SAMPLE-COMPOSED — forward paper
  REQUIRED," not a clean pass. The honest reachable ceiling is PROMISING.
- **Sensitivity (report-only, NOT verdict):** VIX threshold 18 and 22.

## Results-doc requirements
Both windows (CAGR/DD/Sharpe/stress-week %/switch count) vs SPY-BH + EW-39; the A/B/C
decomposition ladder on the reversal leg; 15 bps cost stress on the stock sleeve; the
18/22 VIX sensitivity; **frozen tripwire GREEN**.

## Disclosed limitations
- **Survivorship**: C1's reversal leg buys bottom-residual names among 39 known
  survivors — inflates the gate reversal return by an unknown amount; a pass is
  survivor-flattered (the reason for the "forward paper required" cap).
- **Gate DD razor-thin**: reversal stays ON through crashes by construction (VIX high in
  2008) → gate maxDD inherits ~C1's 57.7% vs the 60% ceiling; one bad stress week busts
  PASS-HR. **No post-hoc crash de-risk bolt-on if it fails** (that would be tuning).
- **Nagel's sample (1998-2010) overlaps the gate** → the mechanism is partly in-sample
  to the gate; the true OOS test is whether secondary reversal profit concentrates in the
  2020-22 VIX spikes.
- **One new parameter (VIX 20.0)** = long-run VIX mean / canonical "elevated" line;
  18/22 reported not to tune but to bound.
- Micro-capital K=4 at $100 ⇒ ~$25/slot ⇒ needs fractional shares or ≥ $500 (flagged).
