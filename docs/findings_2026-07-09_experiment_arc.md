# Findings — A Falsification Program for a Small-Account Swing Trader (E1→E6)

**Swing Trading project · written 2026-07-09 · Evan Daruwalla**

A complete synthesis of the project's first research program: six
pre-registered strategies across two families, all EOD data, small capital
($100–1,000), Alpaca paper target. Every number traces to a committed
backtest; this reads from the append-only record (Appendices A–AC) and the
per-experiment result docs. Point-in-time deliverable, not a live document.

---

## Abstract

I tried to build a systematic swing trader for a small account with the goal
of a high percentage return over short holds. I did not find one — and the
*way* I failed to find one is the result. Two strategy families were tested
under strict pre-registration:

- **Mean reversion** (IBS on ETFs and leveraged ETFs) failed because over
  half its edge lives in the overnight gap an end-of-day bot cannot capture,
  and what remains does not survive transaction costs.
- **Leverage rotation** (200-day-MA timing on 3× Nasdaq) *looked* like the
  winner — a 33%/yr, all-gates-pass backtest — until a pre-registered regime
  test on synthetic data back to 2000 showed it would have **lost 93%** in
  the dot-com and 2008 crashes. Its return was a 2014–2026 bull-market
  artifact.

The single robust, deployable result to emerge is a **de-leveraged (1×)
version of that same rotation** — but it is a *risk-management* tool
(roughly halves the index's worst drawdown for about the same long-run
return), **not** the high-return strategy the goal asked for. That goal
remains unmet, and the evidence now argues it is genuinely hard to meet with
simple public EOD tools at retail scale.

The deliverable is not a profitable bot. It is a **falsification program**
that caught a curve-fit before it cost a dollar.

---

## Method — the discipline that makes these results trustworthy

Every strategy followed the same protocol:

1. **Pre-registration before code.** Exact rules, sizing, costs, evaluation
   windows, and pass/fail kill-criteria were committed to git *before* the
   runner existed (e.g. E1 prereg `8963e49` predates the engine `415c527`;
   E4 `313d88a`, E5 `09a3a31`, E6 `0526ea2`). "It passed" is verifiable, not
   asserted.
2. **Kill-criteria, not vibes.** "Survives" = a conjunction of thresholds.
   Any miss = FAIL, recorded as-is. **No parameter was ever re-tuned to
   rescue a failed run.**
3. **Out-of-sample and out-of-regime.** Parameters set on one window, judged
   on an unseen one; and — the decisive step — a synthetic reconstruction
   back to 2000 to test regimes the modern data excludes.
4. **A frozen-regression tripwire** (`swing_bot/test_frozen.py`, 12 pinned
   references at ±0.0000pp) so an unrelated code change can't silently alter
   a past result.
5. **Refused temptations, logged.** When a data-suggested subset (broad-US)
   passed, redefining the experiment around it was refused as p-hacking and
   spun into its own pre-registration instead.

---

## The results, in one table (%/mo = monthly-compounded equivalent)

| Experiment | What | Basis | %/mo | Verdict |
|---|---|---|---|---|
| E1 | IBS MR, 29 ETFs | 2014–26 net | +0.19% | **FAIL** (Sharpe 0.23, DD 36%) |
| E1b | IBS MR, broad-US | 2022–26 holdout | +0.32% | **FAIL** near-miss (Sharpe 0.496) |
| E2 | IBS MR, 3× ETFs | 2022–26 holdout | +0.64% | **FAIL** (CAGR 8% < 15%, DD 61%) |
| A3 | Overnight-only IBS | screen | −0.11%…+0.56% | dead |
| B1 | Gap-down at open | screen | +0.23% | dead |
| E4 | 3× MA rotation | 2014–26 | +2.45% | **PASS** (then killed by E5) |
| E5 | E4 across 2000–13 | unseen regime | **−0.28%** (DD 92.7%) | **FAIL** → E4 regime-dependent |
| E6 | **1× MA rotation** | 2000–26 all regimes | +0.65% | **PASS** (robust, but risk-mgmt) |

---

## Family 1 — Mean reversion (E1 → E1b → E2 → A3/B1)

Buy oversold (IBS < 0.20), exit on reversion. The full 29-ETF version failed
on cost and drawdown; the broad-US subset persisted out-of-sample but landed
0.004 of Sharpe under the bar; the 3× version failed its return/drawdown
gates. A pre-registered **execution ablation** found the cause: **54% of the
IBS edge is in the close→next-open gap**, which the EOD bot forfeits, and the
non-executable close-to-close version would have passed everything the
executable one failed. Two follow-up screens (harvest the overnight piece
directly; execute at the open to zero the gap) were both dead — the overnight
edge is real but not *separately* harvestable at retail cost. **Family
verdict: no executable edge.**

## Family 2 — Leverage rotation (E4 → E5 → E6): the instructive subplot

**E4 — the false positive.** Hold 3× Nasdaq (TQQQ) while QQQ is above its
200-day MA, else cash. On 2014–2026 it passed all five pre-registered gates:
CAGR 33.8% (+2.45%/mo), and a 20-cell robustness grid was 100% positive. It
looked like the answer.

**E5 — the regime test that killed it.** I reconstructed a synthetic
daily-rebalanced 3× Nasdaq from QQQ back to 1999 (validated against real
TQQQ: drag 4%/yr, daily-return correlation 0.9989) and ran the *same* rule
across the 2000–2013 window the modern data excludes. Result: **−3.4% CAGR
and a 92.7% drawdown.** In choppy secular bears, counter-trend rallies push
QQQ back above its MA, the strategy re-enters 3× right before the next leg
down, and leverage turns whipsaw into ruin. **E4's return was entirely a
2014–2026 artifact.** De-authorized for paper.

**E6 — the honest survivor.** The same rotation at **1×** (real QQQ) passes a
regime-spanning pre-registered test E4 failed: it cuts QQQ's worst drawdown
from **83% to 52%**, improves Sharpe in *every* regime (0.24/0.92/0.54 vs
0.14/0.89/0.42), and stays positive throughout. **But** its full-period CAGR
(8.04%) is essentially identical to just buying and holding QQQ (7.92%) — the
value is drawdown reduction, not return. At +0.65%/mo it is a risk-managed
equity core, **not** a high-return strategy. (2× is worse risk-adjusted than
1×; the sweet spot is no leverage.)

---

## The two through-lines

1. **Execution and regime are where retail edges die.** Every mean-reversion
   result died on the overnight-execution gap and costs; the leverage winner
   died on regime-dependence. Neither failure was visible in a naive
   in-sample backtest — both required a purpose-built test (the fill ablation;
   the synthetic regime reconstruction) to expose.
2. **The one thing that survived is risk management, not return.** Low-
   leverage trend-timing robustly reduces drawdown but does not add return.
   That is the honest, well-documented shape of this problem — and it is the
   opposite of what the "high percent return" goal wanted.

---

## Honest limitations

- All results are **simulated fills**; the live divergence logger (built into
  the plan) is what would validate real costs. Nothing has traded.
- E6's clean windows are partly **seen** (2000–2013 was viewed at 3× in E5),
  so E6 is confirmatory-on-seen-data at a new leverage; live paper / other
  markets remain the only truly clean forward test.
- The synthetic 3×/2× series, though validated on overlap, **understate
  pre-2014 financing costs** (rates were higher then) — flagged in the E5/E6
  preregs; it biases mildly against the buy-hold benchmarks, not the
  conclusions.
- **Survivorship bias** is eliminated for all ETF work but returns the moment
  single stocks (the never-run E3) are tested.
- E6 at 1× is **not** the stated high-return goal; that goal is unmet.

---

## What this program demonstrates

Six pre-registered experiments; one false positive caught by an
out-of-regime test; one refused p-hack; one honest, modest survivor. The
headline is not a return number — it is a **process that falsified its own
best-looking idea before risking capital**. For an engineering portfolio that
is the harder and more valuable thing to show than a curve-fit equity curve:
the ability to be rigorously, checkably wrong, and to know the difference
between a real effect and a regime artifact.

**Bottom line for the stated goal:** no robust, regime-independent, cost-
surviving *high-return* EOD strategy was found, and the accumulated evidence
argues that is the base-rate outcome at this scale. The project's one
deployable result — 1× 200-MA rotation — is worth having as risk management,
not as the return engine that was asked for.

---

## Reproducibility

- Code: `swing_bot/` (`prices`, `universe`, `coverage_gate`, `signals`,
  `backtest`, `rotation`, `test_frozen`); `scripts/` (per-experiment runners,
  incl. `run_e5_regime.py` / `run_e6_deleveraged.py` synthetic studies).
- Data: `swing.db` (34 ETFs, split-adjusted / dividend-unadjusted, 2014–26);
  E5/E6 fetch QQQ/TQQQ/QLD history to 1999 live (not pinned).
- Pre-registrations: E1 `8963e49`, E1b `0126ce3`, E2 `865c09e`, E4 `313d88a`,
  E5 `09a3a31`, E6 `0526ea2`.
- Result docs: `docs/research/2026-07-09_*` (E1/E1b/E2/screen/E4/E5/E6).
- Full chronology with commit hashes: the project record, Appendices A–AC.
- Tripwire: `python -m swing_bot.test_frozen` (12 refs, d = ±0.0000pp).

**Status:** program complete. Nothing live. Open, Evan-gated options: deploy
E6 (1×) to paper as a risk-managed core; open a genuinely new family (stocks/
events); or close the project on this write-up.
