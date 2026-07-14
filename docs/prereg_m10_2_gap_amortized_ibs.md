# Pre-registration — M10-2: Gap-Amortized Stress IBS

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. M10 synthesis arc (Evan "do 1"). Written against
`docs/prereg_TEMPLATE.md`. D1 dual-bar verdict.**

## DATA-SNOOPING DISCLOSURE [binds every M10 prereg]
Composed after seeing 32 prior results on these windows. Every parameter is inherited
from E2/E6 or a canonical constant; exactly one conditioning variable (VIX>20, the Nagel
mechanism). **Any in-window pass is recorded "IN-SAMPLE-COMPOSED — forward paper
REQUIRED," never clean or live.**

## Provenance and prior
EX-DECOMP found the overnight **gap** (A→B) is a recurring edge-killer; E2 (leveraged IBS
mean-reversion) measured >half its edge in the signal-close→next-open gap — its next-open
CAGR was 7.98% but c2c would have been 18.15%. M10-2 attacks that gap with two mechanical
levers, neither a tune: **(a)** hold **5 sessions** so the captured open-to-exit window
contains days 2–5 of the reversion, amortizing the lost first night (E2's 1-day hold made
the gap ~100% of the capture window; a 5-day hold ~20%); **(b)** enter only in **STRESS
(VIX>20)**, where Nagel (2012) documents liquidity-provision compensation is largest —
concentrating trades where the per-trade edge is big enough to survive losing the first
gap. Index-level (QQQ) at 1 bp so the cost (B→C) killer is also structurally absent.
**H1:** the reachable share of the E2 edge clears the tiers. **H0 (judges' base case):**
reversion completes mostly on night 1 → hold-extension recovers little → gate ~7–11%
(HR FAIL). **Honest prior: FAIL/PROMISING most likely; program value high either way —
it directly measures how much of the E2 gap edge is reachable at all.**

## Data (in hand)
QQQ daily OHLC (`swing_bot.prices.fetch`, split-adj/div-UNADJ, from 1999 → 200-DMA from
~2000); **^VIX** daily close (`macro_close`, 1990+ → full gate, no window cap); QLD
(2007+, for the synthetic-2x drag calibration). Synthetic-2x = E6's validated `synth`/
`calib` (daily 2× QQQ return − drag, drag QLD-calibrated ≈ 2.0%/yr). No swing.db writes.

## Exact rules (fixed a priori)
Signals at close t, execution at open t+1, cash = 0%. **State machine, evaluated
top-down at each close:**
1. **IN-TRADE (holding 2× MR):** exit at next open when **IBS_t ≥ 0.80** OR **5 sessions
   elapsed since entry open**, whichever first (time-stop per C3's time-stop-beats-channel
   finding). No other exit; exit → cash (no same-day re-entry).
2. **ENTRY (when not holding MR):** if **VIX close_t > 20.00 AND IBS_t ≤ 0.20** → buy
   **100% synthetic-2× QQQ** at next open. IBS = (Close−Low)/(High−Low) of QQQ
   (`swing_bot.signals.ibs`; High=Low → undefined → no signal).
3. **FALLBACK (not in MR, VIX ≤ 20):** hold 100% QQQ if QQQ close > 200-session SMA, else
   cash. Re-evaluated each close.
4. **(not in MR, VIX > 20, not oversold):** cash (stand aside — stress alone de-risks;
   deliberately not X1's failed AND-gate).
- **Costs:** 1 bp/side on QQQ and the 2× (broad-ETF tier); 5 bps stress arm reported. One
  position at a time; no pyramiding. **Leverage 2× is E2's own, permitted because the
  5-session time-stop + IBS exit IS the pre-committed regime stop.**

## Windows and verdict [D1 dual-bar]
Gate 2000-01-01→2013-12-31; secondary 2014-01-01→end. Floor ≥ 20 MR entries in the gate.
**PASS-HR:** CAGR ≥ 15% AND maxDD ≤ 60%, both windows. **PASS-RA:** gate Sharpe ≥ 0.80 AND
> QQQ-BH both windows AND +CAGR both (QQQ is the honest benchmark for a QQQ sleeve; SPY-BH
also reported). Benchmarks QQQ-BH + SPY-BH. **No tuning a FAIL** (no post-hoc widening of
IBS/VIX thresholds or hold length). **M10 cap:** a pass = forward-paper-required.

## Results-doc requirements
Both windows (CAGR/DD/Sharpe/MR-entry count/time-in-2x %) vs QQQ-BH + SPY-BH; a c2c-vs-
next-open comparison (the gap-amortization measurement — how much of the E2 c2c edge the
5-day hold recovers); 5 bps stress; frozen tripwire GREEN.

## Disclosed limitations
- **The 5-day-hold reachability is the load-bearing assumption** — if reversion completes
  night 1, the hold recovers little and this lands ~7–8% gate (a FAIL that still usefully
  quantifies the reachable E2 edge).
- **2× long into a cascading stress week** is the drawdown engine; a 2008-style repeated
  entry sequence could approach/breach the 60% ceiling.
- **IN-SAMPLE-COMPOSED** + QQQ-only market-dependence (E7). Synthetic-2× drag calibrated
  vs QLD (2007+) — fine, leverage is QQQ-only.
- Overlaps M10-1's VIX-regime logic; if both "pass" they are not independent evidence.
