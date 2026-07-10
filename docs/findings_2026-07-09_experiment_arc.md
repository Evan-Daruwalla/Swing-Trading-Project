# Findings — A Falsification Program for a Small-Account Swing Trader (E1→E7)

**Swing Trading project · written 2026-07-09, updated 2026-07-10 · Evan Daruwalla**

A complete synthesis of the project's first research program: eight
pre-registered strategies across **three** families — index mean reversion,
leveraged trend rotation, and concentrated stock momentum — closed out with
an international out-of-sample test and a survivorship-aware stock test. All
EOD data, small capital ($100–1,000), Alpaca paper target. Every number
traces to a committed backtest; this reads from the append-only record
(Appendices A–AI) and the per-experiment result docs. Point-in-time
deliverable, not a live document.

---

## Abstract

I tried to build a systematic swing trader for a small account with the goal
of a high percentage return over short holds. I did not find one — and the
*way* I failed to find one is the result. Three strategy families were
tested under strict pre-registration. The first two:

- **Mean reversion** (IBS on ETFs and leveraged ETFs) failed because over
  half its edge lives in the overnight gap an end-of-day bot cannot capture,
  and what remains does not survive transaction costs.
- **Leverage rotation** (200-day-MA timing on 3× Nasdaq) *looked* like the
  winner — a 33%/yr, all-gates-pass backtest — until a pre-registered regime
  test on synthetic data back to 2000 showed it would have **lost 93%** in
  the dot-com and 2008 crashes. Its return was a 2014–2026 bull-market
  artifact.

A final pre-registered test settled the leverage question on **genuinely
unseen data** — five non-US indices back to 1985, including the 1990s–2000s
Japan secular bear, the most hostile trend regime in modern history. Even an
a-priori-volatility-gated 3× rotation (knobs fixed from first principles, no
fitting) **failed every gate** across those markets: 4.55% mean return, 83–97%
drawdowns, and the Hong Kong 3× was *mathematically wiped to zero* by the
single-day 1987 crash. The high-return-AND-robust question is therefore
closed not with "I ran out of data" but with "I found clean data and the idea
failed on it."

Finally, the last plausible route to high return — **concentrated single-
stock momentum** — was tested with the survivorship problem confronted head-on
(a stock backtest omits the companies that went bankrupt, biasing it upward).
Even on a bias-*flattered* universe of survivor large-caps, momentum
**failed** the return gate (6% vs 15%) and, damningly, **underperformed simply
buying and holding the same stocks**. All three families are now falsified.

The single robust, deployable result to emerge is a **de-leveraged (1×)
version of the trend rotation** — but it is a *risk-management* tool
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
| E6 | **1× MA rotation** | 2000–26 all regimes | +0.65% | **PASS** (risk-mgmt; later downgraded) |
| E7-A1 | E6 1× across 5 non-US markets | intl out-of-sample | — | **FAIL** 3/5 → E6 market-dependent |
| E7-A2 | a-priori vol-gated 3× rotation | intl out-of-sample | +0.36% (mean) | **FAIL** all gates → leverage closed |
| E3 | concentrated stock momentum (top-3) | 2000–13 gate, bias-flattered | +0.51% | **FAIL** (6% vs 15%; < buy-hold) → stocks closed |

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

## Family 2, continued — E7: the international out-of-sample close

A pressure-test exposed that the US market only offers two independent crash
regimes (2000–02, 2008), both now used — so further US backtesting is
hindsight-contaminated. E7 reached for **genuinely unseen data**: five non-US
indices back to 1985 (Nikkei, DAX, FTSE, Hang Seng, ASX), with the vol-gate
threshold (30%) and leverage drag (5%/yr) **fixed a priori** so the non-US
data was a true first test.

- **Arm 1 (does E6's 1× overlay generalize?) — FAIL, 3/5.** It works
  spectacularly in Japan (cuts the Nikkei's 82% buy-hold drawdown to 34%),
  Germany, and Hong Kong; it *fails* in the UK and Australia, where the
  timing whipsaw lowered risk-adjusted return. **E6 is downgraded from
  "robust" to "market-dependent"** — real, but not a universal law.
- **Arm 2 (a-priori vol-gated 3× — the last high-return candidate) — FAIL,
  every gate.** Mean CAGR 4.55% (bar: 15%), drawdowns of 83–97%, the vol
  gate barely improving on ungated leverage. And the Hong Kong 3× was
  **mathematically wiped to zero by the single-day 1987 crash** (>33% in a
  day destroys any 3× daily fund) — a mathematical, not statistical, verdict
  on extreme leverage.

E7 is the clean close for leverage: the one credible untested high-return
idea, tested a priori on five independent unseen regimes, failed everything.

## Family 3 — Concentrated stock momentum (E3): the survivorship trap, confronted

Single stocks are the natural home for high return — but a stock backtest on
freely-available data is quietly rigged: it omits the companies that went
bankrupt or delisted (Enron, Lehman, WorldCom…), and those deaths cluster in
the very crash regimes that decide robustness. So the backtest is *most*
flattered exactly where honesty matters most.

E3 confronted this with an **asymmetric-falsification** design: run
concentrated momentum (hold the top 3 large-caps by trailing 3-month return,
rebalanced fortnightly) on a universe of *survivor* stocks — a universe whose
biases can only inflate the result — and treat only a FAILURE as meaningful.
It failed, decisively: **6.3% CAGR in 2000–2013 versus the 15% bar**, and —
the tell — it **underperformed simply equal-weight buying and holding the same
39 stocks** in every window (4.8% vs 14.9% in 2014–2026). The momentum
*selection itself destroyed value*. Because the biases could only have helped,
the failure is interpretable in a way a pass never could have been. Stocks are
closed for a backtested high-return claim; only forward live paper
(survivorship-free) could say more, on a poor prior.

---

## Honest limitations

- All results are **simulated fills**; the live divergence logger (built into
  the plan) is what would validate real costs. Nothing has traded.
- E6's US windows are partly **seen** (2000–2013 was viewed at 3× in E5);
  the E7 international test is the cleaner out-of-sample check, and it
  downgraded E6 to market-dependent. Live paper remains the only clean
  *forward* test.
- The synthetic 3×/2× series, though validated against real TQQQ on overlap,
  **understate pre-2014 financing costs** and use an a-priori drag for non-US
  (no deep-history international 3× fund exists to calibrate) — flagged in the
  preregs; it biases mildly against the buy-hold benchmarks, not the
  conclusions. International results use local-currency price indices
  (dividend-excluding → returns understated ~2–3%/yr).
- **Survivorship bias** is eliminated for all ETF/index work but is inherent
  to any stock test; E3 handled it by asymmetric falsification (a
  bias-flattered universe that still failed), and only a live forward test is
  truly survivorship-free.
- E6 at 1× is **not** the stated high-return goal; that goal is unmet.

---

## Conclusion

No robust, regime-independent, cost-surviving *high-return* EOD strategy was
found across **all three** plausible families — index mean reversion,
leveraged trend, and concentrated stock momentum. That conclusion is backed by
out-of-sample evidence from five independent international regimes and a
survivorship-*flattered* stock test that still failed; it is the base-rate
outcome at this scale, not a symptom of too few ideas.

Three through-lines explain why:

1. **Execution and regime are where retail edges die.** Every mean-reversion
   result died on the overnight-execution gap and costs; the leverage winner
   died on regime-dependence, confirmed on five independent international
   markets. Neither failure was visible in a naive in-sample backtest — both
   required a purpose-built test (the fill ablation; the international
   out-of-sample reconstruction) to expose.
2. **What partly survived is risk management, not return — and even it is
   market-dependent.** Low-leverage trend-timing reduces drawdown in some
   markets but not universally, and never adds return. The one partly-
   deployable result — the 1× 200-MA rotation — is worth having as a
   *market-dependent* risk-management overlay, not as the return engine the
   goal asked for. That is the honest, well-documented shape of this problem.
3. **Extreme leverage is tail-fatal, not merely risky.** A single >33% day
   (Hong Kong, 1987) drives any 3× daily fund to a permanent zero. No amount
   of timing recovers from a one-day wipeout — an argument from arithmetic,
   not from a backtest.

Eight pre-registered experiments; one false positive caught by an out-of-
regime test; one refused p-hack; a self-pressure-test that retracted my own
over-claim; and a final international out-of-sample test that closed the
question on data never used to design anything. The headline is not a return
number — it is a **process that falsified its own best-looking idea before
risking a dollar**. For an engineering portfolio that is the harder, more
valuable thing to show than a curve-fit equity curve: the ability to be
rigorously, checkably wrong, and to know the difference between a real effect
and a regime artifact. A rigorous process correctly told the builder his goal
was unreachable with these tools — before the market charged tuition for the
same lesson.

---

## Reproducibility

- Code: `swing_bot/` (`prices`, `universe`, `coverage_gate`, `signals`,
  `backtest`, `rotation`, `test_frozen`); `scripts/` (per-experiment runners,
  incl. `run_e5_regime.py` / `run_e6_deleveraged.py` / `run_e7_international.py`
  synthetic + out-of-sample studies).
- Data: `swing.db` (34 ETFs, split-adjusted / dividend-unadjusted, 2014–26);
  E5/E6/E7 fetch QQQ/TQQQ/QLD + non-US indices to 1985 live (not pinned).
- Pre-registrations: E1 `8963e49`, E1b `0126ce3`, E2 `865c09e`, E4 `313d88a`,
  E5 `09a3a31`, E6 `0526ea2`, E7 `70ed2a1`, E3 `87bc8d9`.
- Result docs: `docs/research/2026-07-09_*` and `2026-07-10_*` (E7, E3).
- Full chronology with commit hashes: the project record, Appendices A–AI.
- Tripwire: `python -m swing_bot.test_frozen` (12 refs, d = ±0.0000pp).

**Status:** program complete — all three strategy families falsified (mean
reversion, leveraged trend, stock momentum), closed on out-of-sample and
survivorship-aware evidence. Nothing live. Open, Evan-gated options: deploy
E6 (1×) to paper as a market-dependent risk-managed overlay; or close the
project on this write-up.
