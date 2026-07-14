# Pre-registration — C7: SVXY short-vol carry gated by VIX term structure

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M8 task 42 (free-sweep authorization 2026-07-14). Written
against `docs/prereg_TEMPLATE.md`. MODIFIED-WINDOW CAP → best verdict = PROMISING.**

## Provenance and prior

The volatility risk premium (variance swaps / VIX futures roll-down in contango) is
among the best-documented premia; short-VIX ETPs harvest it and periodically blow up
doing so — XIV terminated in the 2018-02-05 "Volmageddon" (−>90% in a session;
Augustin-Cheng-Van den Bergen 2021). **H1:** holding SVXY only when the term structure
is in contango (VIX/VIX3M < 1 — E18's exact gate) harvests the carry while the gate +
a hard kill-switch cap the tail. **H0:** the tail cannot be gated at EOD — one
overnight cascade erases years of carry (the crypto-brief's gap-risk logic), and
post-2018 deleveraged SVXY (−0.5×) halves the carry. **Prior: FAIL/weak.**

## Data (probed 2026-07-14)

- **SVXY** OHLCV via `.e8e9_cache`: **2011-10-04 → present (3,713 bars)** — full
  history incl. Volmageddon. `^VIX`/`^VIX3M` via cached `macro_close`. SPY benchmark.
  No swing.db writes.
- **Instrument regime change (disclosed):** SVXY was **−1×** until 2018-02-27 and
  **−0.5×** after. Actual traded prices reflect this — the backtest experiences what a
  holder experienced; no synthetic splicing.

## Exact rules (fixed a priori)

- **Gate:** long SVXY iff VIX/VIX3M < 1 at close (contango), else flat. Signal at
  close → **next open**; **5 bps/side**; long-or-flat, no leverage, whole-NAV
  position; $1,000 start.
- **Hard kill-switch (mandatory):** if the held position's close-to-close return ≤
  **−20%** in one session, exit at next open and **stand down 21 sessions** (no
  re-entry regardless of gate). Modeled honestly: the exit eats the next-open gap.
- **Arms:** (a) gated + kill-switch (MAIN); (b) gated, no kill-switch (sensitivity);
  (c) SVXY buy-hold (reference); SPY-BH benchmark. 15 bps stress on (a).

## Windows and verdict [MODIFIED-WINDOW CAP]

- **Single window 2012-01-01 → present** (SVXY inception floor; includes Volmageddon,
  covid, 2022). **No 2000–2013 gate exists → best achievable = "PROMISING — forward
  confirmation required"; PASS-HR/RA may NOT be claimed.** Floor ≥ 20 gate toggles.
- **PROMISING** iff arm (a) beats SPY-BH on **CAGR AND Sharpe** over the full window
  AND maxDD ≤ 60%. **FAIL** otherwise. No post-hoc changes.

## Results-doc requirements
All arms + SPY; the Volmageddon episode traced day-by-day (did the gate/kill-switch
fire, what was eaten); cost ladder 5/15 bp; toggle count; tripwire GREEN.

## Disclosed limitations
Single window, one Volmageddon (effective N≈1 for the tail); −1×→−0.5× regime change
mid-sample; kill-switch threshold (−20%) and stand-down (21) fixed a priori, untuned;
overnight cascade risk is structurally uncapped at EOD (the honest reason this is
PROMISING-capped at best).
