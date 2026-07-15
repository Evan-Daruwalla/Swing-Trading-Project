# Pre-registration — M11: Algorithmic chart-pattern detection (long-side reversal)

**Written 2026-07-14 (CST), BEFORE any backtest runner code. Committed doc-only;
this hash predates the runner.** PRD M11.2 (Evan's direction 2026-07-14); design
fixed by the M11.1 brief (`docs/research/2026-07-14_chart_pattern_detection_brief.md`).
D1 dual-bar verdict + asymmetric-falsification framing (survivor universe).

## Provenance and prior

Rule-based (NOT LLM/ML) detection of the classic reversal chart *shapes* — the one
mechanism family the program has never tested (all 33 prior attempts trade a *number*, not
a *shape*). Sources: Lo-Mamaysky-Wang (2000, *J. Finance*) — algorithmic kernel/extrema
pattern detection carries modest incremental statistical information but "informative ≠
profitable"; Savin-Weller-Zvingelis (2007, *J. Fin. Econometrics*) — head-and-shoulders
predicts ~5–7%/yr risk-adjusted **under**performance but a standalone strategy is "not
profitable … in rising markets" (a SHORT edge → the no-shorting wall); Sullivan-Timmermann-
White (1999) & Bajgrowicz-Scaillet (2012) — technical-rule profits vanish under
data-snooping correction + even low costs.

**Working hypothesis H1 (the prior):** no cost-surviving, out-of-sample, *long-only* K=1–3
retail-EOD chart-pattern edge exists on the survivor universe → **FAIL.** **Rival H0:**
long-side reversal patterns (double-bottom, inverse-H&S) carry tradeable predictive info
surviving costs → PROMISING. **Honest expectation: FAIL** — the deployable long side has the
weakest support; the tradeable evidence is short/hedged; and program-internally, continuation
patterns are breakouts (killed 3× — E8/E11/C3) and long reversals are cousins of the
reversal near-miss that decayed (E16/C1); next-open bleeds the overnight gap (EX-DECOMP).

**[STANDING] asymmetric-falsification clause:** the 39-name universe is survivor-biased →
survivorship can only HELP → **only a FAIL is clean**; a PASS is UNINTERPRETABLE and routes
to forward paper, never a live claim. (This IS a full-window test → D1 tiers are *reachable*
— not modified-window-capped — but survivorship still caps a pass to forward-only.)

## Data (probed 2026-07-14)

- **Source & access:** `.e8e9_cache` via `run_e8_squeeze.cache_fetch` (yfinance
  `prices.fetch`, from 1990), already populated for the 39-name universe by E10/E16/C1.
  No NEW data source (no probe needed). Cache gitignored; runner does **no swing.db writes**;
  Trading caches untouched.
- **Adjustment convention [STANDING]:** split-adjusted, dividend-UNADJUSTED
  (`auto_adjust=False`). Pattern pivots computed on **close** (b[5]); fills on **open**
  (b[2]); mark-to-market on close. Stated in the runner header.
- **Point-in-time / lookahead:** pivots are **causal** — a swing high/low at bar `j` is
  confirmed only at bar `j+w` (w bars of right-side confirmation), so at decision bar `i`
  only pivots with `j+w ≤ i` are used. The neckline break is evaluated on close[i] with the
  fresh-cross test using close[i−1]; entry executes at open[i+1]. **No two-sided smoother**
  (LMW's kernel is non-causal → look-ahead; explicitly avoided).
- **Universe & liquidity floor [STANDING]:** the 39 survivor mega-caps (E10 `UNIV`). Floor
  ADV ≥ $5M ∧ price ≥ $5 is satisfied by construction for this universe across 2000–2026
  (all large-caps; same as E16/C1). Participation cap non-binding at this AUM.

## Exact rules (fixed a priori)

- **Pivots (causal):** half-window **w = 5** sessions. Swing high at `j` iff
  `close[j] = max(close[j−5 … j+5])`; swing low iff `= min(...)`. Confirmed at `j+5`. Dedupe
  to a strictly alternating High/Low sequence, keeping the more-extreme bar on same-type runs.
- **Signal = long-side reversal pattern completion (ONE consolidated spec; C3-style collapse
  to avoid multi-pattern snooping).** Either sub-pattern, evaluated on the confirmed-pivot
  tail at bar `i`:
  1. **Double bottom** — pivots …L(T1) H(P1) L(T2): `|c[T2]−c[T1]| / min(c[T1],c[T2]) ≤ 0.04`
     (bottoms within 4%); `c[P1] ≥ 1.05·max(c[T1],c[T2])` (intervening peak ≥5% above the
     higher bottom); `10 ≤ T2−T1 ≤ 90` sessions. **Neckline = c[P1]** (flat).
  2. **Inverse head-and-shoulders** — pivots …L(ls) H(P1) L(head) H(P2) L(rs):
     `c[head] ≤ 0.97·min(c[ls],c[rs])` (head ≥3% below both shoulders);
     `|c[ls]−c[rs]| / min(c[ls],c[rs]) ≤ 0.06` (shoulders within 6%); each of `head−ls` and
     `rs−head` in `[10, 90]`. **Neckline = line through (P1,P2) evaluated at bar i.**
- **Entry trigger [STANDING EOD rule]:** a **fresh upward neckline cross on close** —
  `close[i] > neckline(i)` AND `close[i−1] ≤ neckline(i−1)` — with the most recent pattern
  trough (T2 / rs) within **30 sessions** of `i` (breakout recency; no crossing an ancient
  neckline). **Execute next open.**
- **Exit — time-stop baseline [STANDING]:** hold **N = 20 sessions**, exit at open.
  Descriptive-only sensitivity arms **N = 10 and 40** reported, NOT gated (any price/trailing
  stop would have to beat the time-stop-only arm; none is adopted here).
- **Sizing [STANDING defaults]:** **size = min(cash, NAV/K)** at entry; **K = 3** concurrent
  max; **no leverage**; **anti-martingale** (never average down). Oversubscription tie-break:
  rank simultaneous signals by breakout strength `close[i]/neckline(i) − 1` descending, fill
  top slots, **DROP the rest and report the dropped count** (no silent cap). Fixed-fraction,
  not Kelly (λ n/a); frozen here.
- **Costs [STANDING tiered]:** **5 bps/side** (single stocks) headline; **15 bps/side stress
  leg** reported alongside. Decomposition ladder A/B/C required (below).

## Windows and verdict [STANDING D1 dual-bar]

- **Gate 2000-01-01 → 2013-12-31** (hostile). **Secondary 2014-01-01 → end.** Floor: **≥ 30**
  gate entries, else INCONCLUSIVE. Full-window (price-only, no data wall) → D1 tiers reachable.
- **PASS-HR:** net CAGR ≥ **15%** AND maxDD ≤ **60%**, BOTH windows.
- **PASS-RA:** gate **Sharpe ≥ 0.80** AND > SPY buy-hold in BOTH windows AND positive CAGR
  both. Benchmarks: **SPY-BH and EW-39** (equal-weight survivor universe — the survivorship
  control).
- **FAIL:** neither. All three fixed here, before the run. **No parameter changes after
  results; a FAIL is never re-tuned into a pass.** A PASS (either tier) is capped
  UNINTERPRETABLE / forward-paper by the asymmetric clause.
- **Modified-window cap [STANDING]:** N/A — this is a full-window test.
- **LLM overlays forward-only [STANDING]:** N/A — this is rule-based, no LLM.

## Results-doc requirements [STANDING]

- **Decomposition ladder** on the headline: Rung A (c2c 0 bps) / Rung B (next-open 0 bps) /
  Rung C (next-open + 5 bps) — is any edge signal-real, gap-dwelling, or cost-gated.
- **Short-side diagnostic (reported, NOT gated):** detect the bearish mirrors (double-top,
  H&S) and report mean forward-20-session return after bearish-pattern completion vs bullish
  vs unconditional — to document the Savin (2007) short-side effect and confirm it is the
  **non-deployable** side (no fractional shorting at $100–1,000; the X2 lesson). Explicitly
  outside the D1 verdict.
- D1 verdict with criteria echoed; benchmark comparison; entry count vs floor; and the
  **frozen tripwire GREEN** (`.venv\Scripts\python.exe -m swing_bot.test_frozen`, 12 refs
  d=±0.0000pp) run AFTER — the standing done-check.

## Disclosed limitations

- **Survivorship (load-bearing):** the 39 names survived to today; a long reversal detector
  buys *dips in known survivors* → a pass is UNINTERPRETABLE (asymmetric clause). Only a FAIL
  is clean.
- **Detector-parameter surface:** pivot w, tolerances, neckline heights, hold N, recency
  are a snooping surface. They are PINNED here from standard TA definitions a priori and NOT
  tuned after results; the single-consolidated-spec (no multi-pattern sweep) limits the
  surface further. Different-but-reasonable params could shift the numbers — the verdict is
  the pre-committed one regardless.
- **Close-based pivots** (LMW convention) miss intrabar highs/lows; a high/low-based detector
  might fire differently. Fixed choice, disclosed.
- **Next-open execution** bleeds the overnight component (EX-DECOMP) — the A/B ladder
  measures it; disclosed as an expected headwind, not a tuning target.
- **Short-side diagnostic is a measurement, not a strategy** — the bearish edge (if any) is
  non-deployable (shorting) and is reported only to close the "is the shape informative?"
  question, mirroring X2.
