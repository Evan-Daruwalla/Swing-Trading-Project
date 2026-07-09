# Findings — From IBS Mean Reversion to Leverage Rotation (Experiment Arc E1→B4)

**Swing Trading project · written 2026-07-09 · Evan Daruwalla**

A synthesis of the project's first experimental arc: five pre-registered or
screened strategies, all EOD data, small capital ($100–1,000), Alpaca paper
target. This report reads from the append-only record
(`docs/Project Record — Full Chronological History.md`, Appendices A–Y) and
the per-experiment result docs; every number here traces to a committed
backtest. It is a point-in-time deliverable, not a live document.

---

## Abstract

I set out to build a systematic swing trader for a small account. Starting
from a literature-ranked signal (Internal Bar Strength mean reversion on
liquid ETFs), I ran three fully **pre-registered** experiments and one
screening round. The mean-reversion family **failed** — not randomly, but for
a single, identifiable reason: **over half the edge lives in the overnight
gap between the signal (at the close) and the fill (at the next open), which
an end-of-day bot cannot capture.** After exhausting that family under a
pre-committed stop, a screening round surfaced a different mechanism —
**200-day-moving-average leverage rotation (hold TQQQ while QQQ is in an
uptrend, else cash)** — that returned **~2.15%/month out-of-sample** because
it trades ~4 times a year and is therefore immune to the execution problem
that killed everything else. That candidate (E4) is not yet confirmed; the
next stage is a pre-registered robustness battery and live paper.

The deliverable is not a profitable bot. It is a **falsifiable research
program**: rules fixed in git before results existed, negative results
recorded honestly, and one temptation to p-hack explicitly refused.

---

## Method — why this is more than "backtesting until something works"

Every strategy tested against real capital rules followed the same
discipline:

1. **Pre-registration before code.** The exact entry/exit rules, sizing,
   fill model, cost, evaluation window, and pass/fail kill-criteria were
   written to a doc and **committed to git before any backtest engine code
   existed.** Git history is the proof: the E1 pre-registration is commit
   `8963e49` (132 lines, one file, no engine); the engine arrived later at
   `415c527`. This makes "the strategy passed" a credible claim rather than a
   number I could have reverse-engineered.
2. **Out-of-sample holdout.** Parameters were set on 2014–2021; the verdict
   was rendered on a 2022–2026 holdout not used to choose anything.
3. **Kill-criteria, not vibes.** Each experiment defined "survives" as a
   conjunction of thresholds (trade count, expectancy, risk-adjusted return,
   drawdown ceiling). A miss on any one = FAIL, recorded as-is. **No
   parameter was ever re-tuned to rescue a failed run.**
4. **A frozen-regression tripwire** (`swing_bot/test_frozen.py`) pins each
   engine's output on fixed windows to ±0.0000 percentage points, so an
   unrelated code change that silently altered a past result trips loudly.
5. **Data honesty.** Prices are split-adjusted, dividend-unadjusted; a
   coverage/quality gate caught 19 corrupt bars before they could poison a
   backtest; ETFs (not single stocks) were chosen specifically to eliminate
   survivorship bias from the first four experiments.

---

## The experiments

Returns are net of a 10 bps round-trip cost unless noted, on the executable
(next-open) fill model. "%/mo" is the monthly-compounded equivalent of the
annualized figure.

### E1 — IBS mean reversion, 29-ETF universe · VERDICT: FAIL

- **Hypothesis:** buy oversold liquid ETFs (IBS < 0.20 at close), exit on
  reversion (IBS > 0.80) or a 5-day stop.
- **Result:** 3,559 trades, expectancy +4.7 bps (positive), but **Sharpe
  0.23** (needed ≥0.50) and **max drawdown 36%** (needed ≤25%). CAGR 2.31%
  = **+0.19%/mo.**
- **Why it failed:** cost-fragile (the same strategy at zero cost had Sharpe
  0.56; at a 20 bps round-trip it went negative), the country-ETF leg was
  net-negative, and the edge decayed to nothing after 2021.
- **The integrity moment:** the broad-US subset *alone* passed all four
  criteria. Redefining "E1 = broad-US" after seeing that would be
  post-hoc universe-narrowing — p-hacking. It was refused; broad-US became a
  *new* hypothesis (E1b) with its own pre-registration.

### E1b — IBS on broad-US indices, true out-of-sample · VERDICT: FAIL (near-miss)

- **Hypothesis:** the effect isolated to SPY/QQQ/DIA/IWM persists on an
  unseen 2022–2026 holdout.
- **Result:** 560 trades, expectancy +17.8 bps, drawdown a clean 9.8%, but
  **Sharpe 0.4961 — below the 0.50 bar by 0.004.** CAGR 3.96% = **+0.32%/mo.**
- **Verdict:** FAIL, *not rounded up*. But informative: my pre-registered
  prior (decay to zero, like the full universe) was **wrong** — the edge
  genuinely persisted out-of-sample (train Sharpe 0.66 → holdout 0.496)
  through the 2022 bear market. Real, but just under tradeable, and entirely
  hostage to the cost assumption.

### E2 — IBS on 3× leveraged ETFs, return-centric gates · VERDICT: FAIL

- **Context:** after the goal was redefined toward *high percent return with
  risk accepted*, the natural amplifier was leveraged wrappers of the exact
  underlyings where the edge had persisted (TQQQ/UPRO/SPXL/SOXL/TNA),
  concentrated to 2 positions, gated on CAGR ≥ 15% with a loosened 60%
  drawdown ceiling.
- **Result:** 351 trades, expectancy +31 bps, but **CAGR 7.98%** (+0.64%/mo,
  needed ≥15%) and **drawdown 60.6%** (just over the 60% ceiling). FAIL.
- **The decisive observation:** the **non-executable** close-to-close version
  of this exact strategy would have **passed everything** — CAGR 18.15%
  (+1.40%/mo), drawdown 52%. The entire gap between success and failure is
  the overnight component the EOD bot cannot enter.

### Screening round (in-sample, hypothesis-generating)

With the mean-reversion family shelved under a pre-committed stop, three
cheap screens tested new mechanisms:

- **A3 — harvest the overnight component directly** (buy close, sell next
  open): DEAD. On broad ETFs it is net-negative — the 6.3 bps/night gross
  effect cannot pay a 10 bps round-trip. The overnight edge is real but not
  *separately* harvestable at retail cost.
- **B1 — gap-down reversion executed at the open** (zero signal-to-fill gap
  by construction): DEAD. Best variant +0.23%/mo; the execution advantage
  came with no edge.
- **B4 — 200-day-MA leverage rotation** (hold TQQQ while QQQ closes above its
  200-day average, else cash): **STANDOUT.**

### B4 — leverage rotation · the surviving lead (NOT yet confirmed)

| window | %/mo | CAGR | maxDD | Sharpe | switches/yr |
|---|---|---|---|---|---|
| train 2014–21 | +2.59% | 35.9% | 57.7% | 0.89 | ~4 |
| holdout 2022–26 | **+2.15%** | 29.0% | 48.2% | 0.79 | ~4 |

Roughly 3–4× the return of anything the mean-reversion family produced, and
its mechanism **sidesteps the execution problem entirely**: at ~4 switches
per year, the overnight gap and bid-ask spread are rounding errors. It also
matches an independent published construct (Gayed, "Leverage for the Long
Run") rather than being mined from noise.

---

## The through-line

Every mean-reversion result — E1, E1b, E2, A3 — failed or fell short for the
**same reason**, and the leverage-rotation result succeeded for the
**inverse** of that reason:

> Short-horizon mean-reversion edges are concentrated in the overnight move
> immediately after the signal. An end-of-day bot that signals at the close
> and fills at the next open forfeits over half of them, and what remains
> does not survive transaction costs. A low-frequency trend-timing strategy
> holds positions for weeks, so it never pays that overnight tax.

That is a genuine, reusable finding about this problem class — arguably more
valuable than a marginal passing backtest would have been.

---

## Honest limitations

- **B4 is not confirmed.** The screen looked at 2022–2026, so that window is
  now contaminated for a follow-up pre-registration. Confirmation requires a
  *new* pre-registered robustness battery (MA lengths 150–250, signal-source
  and execution-lag variants, doubled costs) and, ultimately, **live paper
  as the only truly unseen test.**
- **Variant selection.** TQQQ/QQQ was the stronger of two rotation variants
  seen (UPRO/SPY was much weaker out-of-sample). Partly mitigated because
  TQQQ/QQQ is the a priori literature choice and QQQ carried the edge in
  every prior experiment.
- **Drawdowns of ~50–58% are real** and will happen; that is the accepted-
  risk contract of a leveraged strategy, stated up front.
- **B4 stretches the "swing" label** — holds run weeks to months between
  crossings; it is leverage *timing*, not classic multi-day swing trading.
- **Survivorship bias** is eliminated for the ETF work but will return the
  moment single stocks (the deferred E3) are tested; the plan requires a
  liquidity-defined universe and an explicit caveat there.
- **Paper-fill realism:** all results are simulated fills; the live divergence
  logger (built into the plan, not yet run) is what will validate real costs.

---

## What the process demonstrates

Five strategies, four honest FAILs (or near-fails), one live lead — and,
critically:

- rules committed to git *before* results existed (verifiable, not asserted);
- a data-suggested "winner" (broad-US) **refused** because taking it would
  have been p-hacking;
- a **pre-committed stop** that ended the mean-reversion family instead of
  letting it spawn endless re-tuned variants;
- in-sample screens explicitly labeled hypothesis-generating, with their
  contamination of any future holdout flagged in advance.

The bot is not finished and may never trade a passing strategy. The
**experimental discipline** — the thing that separates research from
curve-fitting — is the deliverable, and it is intact and reproducible.

---

## Reproducibility

- Code: `swing_bot/` (`prices`, `universe`, `coverage_gate`, `signals`,
  `backtest`, `test_frozen`), `scripts/` (per-experiment runners).
- Data: `swing.db`, 34 ETFs, split-adjusted / dividend-unadjusted,
  backfilled from yfinance 2014–2026.
- Pre-registrations: `docs/prereg_E1_ibs.md` (`8963e49`),
  `docs/prereg_E1b_broad_us.md` (`0126ce3`),
  `docs/prereg_E2_leveraged_ibs.md` (`865c09e`).
- Result docs: `docs/research/2026-07-09_E1_backtest_results.md`,
  `..._E1b_broad_us_results.md`, `..._E2_leveraged_results.md`,
  `..._screen_results.md`; power and ablation studies alongside.
- Full chronology with commit hashes: the project record, Appendices A–Y.
- Tripwire: `python -m swing_bot.test_frozen` (10 pinned references,
  d = ±0.0000pp).

**Status:** experiment arc closed at the B4 lead. Next stage (E4 confirmation)
is pre-registration + robustness battery + live paper, on Evan's direction.
