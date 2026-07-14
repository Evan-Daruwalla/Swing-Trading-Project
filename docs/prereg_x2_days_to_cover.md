# Pre-registration — X2: Days-to-cover / short-interest drift (FINRA, modern OOS)

**Written 2026-07-13 (CST), BEFORE any backtest runner code. Committed doc-only;
this hash predates the runner. PRD M9 task 46 (Evan authorized "do 1" =
X2/X3, 2026-07-13). First prereg written against the new
`docs/prereg_TEMPLATE.md` (M9 #43). D1 dual-bar verdict, but under the
MODIFIED-WINDOW CAP — see Windows.**

## Provenance and prior

Boehmer-Huszar-Jordan (*The Good News in Short Interest*, JFE 2010) and
Asquith-Pathak-Ritter (JFE 2005): **high short interest predicts negative
abnormal returns; low short interest predicts positive** — days-to-cover
(shares short / ADV) is the canonical normalization. Working hypothesis (H1):
a long book of the LOWEST-days-to-cover survivor large-caps beats passive; the
long-short (low − high DTC) spread carries the documented positive sign. Null
(H0): no exploitable dispersion among 39 liquid mega-caps. **Honest prior:
near-certain FAIL / at most weak-PROMISING.** The documented edge concentrates
in **small, illiquid, hard-to-borrow** names the mandatory liquidity floor
excludes (data-sources brief 2026-07-13; Muravyev-Pearson-Pollet 2025 — most
short-side predictability is a borrow-fee proxy living in unfloorable names).
The modern window is also a post-publication, likely-arbitraged regime
(McLean-Pontiff). This is the data-unblocked descendant of the BLOCKED-ON-DATA
E17 (record Appendix BA).

## Data (probed 2026-07-13)

- **Source & access:** FINRA consolidated exchange-listed short interest via the
  public REST API (no auth; scout-verified, record Appendix BU). Ingested by
  `scripts/ingest_finra_short_interest.py` → `.finra_cache/short_interest.json`
  (gitignored). **205 biweekly settlement dates 2017-12-29 → 2026-06-30, 39/39
  name coverage on every date.** `daysToCoverQuantity` is PRECOMPUTED (verified
  consistent with currentShortPositionQuantity / averageDailyVolumeQuantity).
- **Adjustment convention:** prices from `.e8e9_cache` (split-adjusted,
  dividend-UNADJUSTED, `auto_adjust=False`). No swing.db writes.
- **Point-in-time / lookahead guard [load-bearing]:** short interest for
  settlement date *S* is not publicly disseminated until ~8–9 **business** days
  after *S*. To guarantee no lookahead, the runner enters **10 trading sessions
  AFTER the settlement date** (conservative buffer past dissemination), never on
  *S* itself. Acting on ~2-week-old short interest is the realistic live case.
- **Universe & liquidity floor:** the 39 survivor large-caps (as E10/E15/E16/
  E19). All clear the ADV ≥ $5M ∧ price ≥ $5 floor trivially (mega-caps) — which
  is exactly why the prior is weak: the floor keeps us out of the names where
  the effect lives. Survivor universe → **asymmetric framing: only a FAIL is
  clean.**

## Exact rules (fixed a priori)

- **Signal:** at each settlement date, rank the 39 names by precomputed
  days-to-cover.
- **Deployable long-only leg (the tradeable falsification):** hold the **K = 5
  LOWEST-DTC** names, equal-weight. Enter 10 sessions after the settlement date
  at the next open; hold until the next cycle's entry fires (~biweekly ≈ 10–11
  sessions); full rebalance each cycle. 5 bps/side; $1,000 start; size = NAV/K.
- **Existence spread (reported, NOT deployable):** the long-short (K lowest-DTC
  minus K highest-DTC) equal-weight return, to test whether the documented sign
  exists in this universe/window. **Flagged non-deployable** — no fractional
  shorting at this capital, and the anomaly's alpha concentrates in the SHORT
  (high-DTC) leg. Existence-only; never a live claim.
- **Time-stop baseline:** exit is the biweekly time stop (next rebalance). No
  price stop (would need a separate arm that beats this; not tested here).
- **Costs:** headline 5 bps/side (single stocks); **15 bps/side stress leg
  reported alongside** per the template.

## Windows and verdict [MODIFIED-WINDOW CAP]

- **Single window 2018-2026** (short-interest data floor 2017-12-29). No
  2000–2013 gate is possible → per the standing modified-window rule, **the best
  achievable verdict is "PROMISING — needs forward confirmation"; X2 may NOT
  claim PASS-HR or PASS-RA.** Floor: ≥ 20 rebalance cycles (205 settlements →
  far exceeded).
- **PROMISING** iff the deployable long-only leg beats **both** SPY buy-hold AND
  EW-39-universe on **CAGR AND Sharpe** over the window, AND the existence spread
  shows the documented positive (low−high DTC) sign. **FAIL** otherwise.
- Reference tiers (descriptive only, cannot be claimed given one window): CAGR ≥
  15% / maxDD ≤ 60% (HR-shaped); Sharpe ≥ 0.80 (RA-shaped).
- **Asymmetric overlay:** survivorship can only help → a FAIL is clean and closes
  the days-to-cover long idea for this universe; a PROMISING routes to forward
  paper only. No parameter changed after results.

## Results-doc requirements

- **Decomposition ladder** (Rung A c2c 0bps / B next-open 0bps / C next-open
  5bps) on the long-only leg, per the template.
- Long-only leg vs SPY-BH and EW-39; the existence-spread sign and magnitude;
  the 15 bps stress leg; entry/cycle count vs floor; **frozen tripwire GREEN**
  (`.venv\Scripts\python.exe -m swing_bot.test_frozen`, 12 refs d=±0.0000pp).

## Disclosed limitations

- **Single 2018–2026 window** (one covid crash + one 2022 bear) — thin regime
  coverage; PROMISING-capped by design.
- **Survivorship** (39 current large-caps) — the reason for FAIL-only reading.
- **The floor excludes where the edge lives** — a liquid-universe test may
  simply confirm the effect is unreachable at this capital (the E10/E15 pattern).
- **10-session dissemination lag is a fixed approximation**, not the exact
  per-date FINRA publication date (the API exposes no dissemination field);
  chosen conservative to eliminate lookahead, at the cost of some signal
  freshness.
- **Long-only leg tests the WEAK side** of the anomaly (the alpha is on the
  short/high-DTC leg, which is not deployable here) — a FAIL of the long leg does
  not falsify the short-side effect, only its long-only tradability.
