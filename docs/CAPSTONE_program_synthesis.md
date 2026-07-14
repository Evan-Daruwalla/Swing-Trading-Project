# Swing-Trading Falsification Program — Capstone Synthesis

**Evan Daruwalla · synthesis dated 2026-07-13 (CST) · repo:
https://github.com/Evan-Daruwalla/Swing-Trading-Project**

> This is the standing capstone: the single-document account of what the program set
> out to do, how it was run, what it found, and why. The append-only
> `docs/Project Record — Full Chronological History.md` remains ground truth for
> dated detail; this synthesizes it. **Final counts: 0 PASS-HR / 1 weak PASS-RA /
> 30 pre-registered attempts / 8 strategy families.** The M8 full-method-survey sweep
> (C1/C3/C4/C6/C7 run, C2 closed on probe) and the M9 free experiments
> (X1/X2/X2b/X3) are all complete — the entire documented, evidenced swing-method
> space is exhausted.

---

## 1. What this project is

A search for a **high-percent-return, concentrated (K=1–3), end-of-day swing-trading
edge** deployable at **$100–1,000** of real capital — and, when no such edge survived,
an honest, fully-documented **falsification program** proving the search space was
exhausted under discipline. Losses were explicitly accepted; the gates are
return-centric with loosened-but-present drawdown ceilings. The project is deliberately
**separate** from the author's other (factor-sleeve) trading repo and reads its price
caches read-only.

**The terminal claim (what the evidence supports):** *no robust, high-return,
cost-surviving, out-of-sample EOD edge exists in the documented, evidenced
swing-strategy space at retail scale, K=1–3 concentration, and a mandatory liquidity
floor.* The one strategy that partly survives (E6, 1× moving-average rotation) is a
**market-dependent risk-management overlay, not a high-return engine**. The one strong,
correctly-signed anomaly the program surfaced (short-interest / days-to-cover) is
**real but structurally uncapturable** within these constraints. **Nothing ever went
live.**

**The deliverable is the discipline, not a winning strategy.** The value of this work —
and the reason it is written this way — is that it demonstrates rigorous, honest,
self-correcting quantitative research: pre-registration, asymmetric falsification, a
frozen regression tripwire, cost/execution decomposition, and an unbroken dated record
including the program's own mistakes and corrections.

---

## 2. Methodology — the actual contribution

Every experiment obeyed the same machinery. This is the part worth reading.

1. **Pre-registration before code.** Each experiment's rules, windows, and the full
   PASS/FAIL criteria are written to a `docs/prereg_*.md` and **git-committed
   doc-only, before the runner exists** — the commit hash provably predates the
   analysis. No criterion is ever relaxed after seeing results; a FAIL is never
   re-tuned into a pass. A standing `docs/prereg_TEMPLATE.md` now binds every future
   prereg to these rules.

2. **Asymmetric falsification on a survivor universe.** The single-stock experiments
   run on 39 large-caps that *survived* to today — a universe biased *in the
   strategy's favor*. Therefore **only a FAIL is clean**: survivorship (and any
   lookahead) can only help, so a strategy that still fails has genuinely failed, while
   a "pass" is uninterpretable and would route to forward paper, never a live claim.

3. **D1 dual-bar verdict.** Two pre-registered pass tiers: **PASS-HR** (net CAGR ≥ 15%
   AND maxDD ≤ 60%, both a hostile 2000–2013 gate window and a 2014→ secondary) and
   **PASS-RA** (gate Sharpe ≥ 0.80 AND > benchmark both windows AND positive CAGR
   both). FAIL = neither. All three outcomes fixed before each run.

4. **Frozen-regression tripwire.** `swing_bot/test_frozen.py` pins 12 deterministic
   reference numbers to **exact** values (d = ±0.0000pp). It runs GREEN after every
   experiment; a silent drift from an "unrelated" change fails loud. It has stayed
   GREEN across all 23 attempts.

5. **Execution/signal decomposition ladder.** Every result is decomposed **Rung A**
   (frictionless close-to-close) → **Rung B** (next-open, 0 bps) → **Rung C**
   (next-open + tiered cost), isolating whether a nominal edge is signal-real,
   gap-dwelling, or cost-gated. Costs are tiered by instrument (1 bp broad ETF / 5 bp
   single stock / 15–25 bp or exclude below the floor) with a 15 bp stress leg.

6. **Mandatory liquidity floor + honest window caps.** ADV ≥ $5M ∧ price ≥ $5 is
   enforced (at this capital, spread/slippage dominate). Data that cannot cover
   2000–2013 (short interest 2018+, etc.) is capped at a "PROMISING" verdict — it may
   never claim PASS-HR/RA.

7. **An append-only record.** Every step — including dead ends, a mis-scoped cost
   model caught and fixed, and one over-enthusiastic finding later corrected — is dated
   and preserved. Prior entries are never edited; corrections are appended.

---

## 3. Results ledger — 8 families, 30 attempts, 0 high-return passes

| Family | Experiments | Verdict |
|---|---|---|
| Index mean-reversion (IBS) | E1, E1b, E2, E12 | FAIL — best OOS Sharpe 0.4961 (near-miss); >½ the edge is in the overnight gap next-open can't enter → **family shelved by pre-committed stop** |
| Leveraged trend rotation | E4, E5, E7 | E4 passed 2014–26 backtest, **E5 killed it** (92.7% DD in unseen 2000–13); E7 closed it OOS on 5 non-US regimes |
| De-leveraged trend (1×) | E6, E7 | **PASS then downgraded** — robust in US, market-dependent (3/5 regions); a risk-management overlay, *not* high-return |
| Single-stock momentum | E3 | FAIL — 6.27% gate CAGR, underperformed equal-weight buy-hold of its own survivor universe |
| Breakout / volatility | E8, E11, C3 | FAIL — compression predicts expansion, not direction; volume gating adds nothing; **C3** consolidated kill-shot confirms it, and shows the "cut at the recent low" exit is a whipsaw tax (time-stop beats it) |
| Deep-dip accumulation | E9 | FAIL — the "never book a loss" claim is literally true (0/53 realized losses) and still bad (3.46% CAGR, −79.7% unrealized) |
| Event-driven (earnings) | E10, E15 | FAIL — a real but small effect (only experiment to beat both benchmarks in 2000–13) that **decayed post-2010** |
| Seasonality / cross-sectional / overlay | E13, E14, E16, E18, E20, X1, C1, C4, C6, C7 | FAIL, except **E18 VIX-TS cleared the program's only (weak) PASS-RA**. **C1** residual reversal is the *closest-ever HR near-miss* — gate 19.08% CAGR / DD 57.7% clears both HR legs in-window, then dies post-2014 (survivorship + regime); **C7** SVXY carry posts the highest CAGR ever (26.45%) and still FAILs (Sharpe < SPY; rides the dead −1× instrument); **C4** vol-sizing is a real DD-cutter that misses the 0.80 bar; **C6** FOMC even-week replicates the published effect then *inverts* post-2014; **X1** confirms no vol gate beats the plain 200-DMA |
| Informed positioning | E19, X2, X2b, X3 | FAIL — insider opportunistic-buys close cleanly; short-**interest** days-to-cover is real on the *short* side but **uncapturable** (see §5); short-**volume** (X3) carries no cross-sectional signal at all (executed-flow MM-hedging noise — the clean X2/X3 contrast) |
| *(closed on probe)* | C2 dividend-initiation | Only 3 first-ever initiations in 26 years among the survivors → insufficient event flow, no runner |

**Tally: 0 PASS-HR, 1 weak PASS-RA (E18 VIX-TS, forward-paper candidate only), 30
pre-registered attempts, 8 families.** Full per-experiment detail: the append-only
record and `docs/research/`.

---

## 4. Why nothing passed — the structural conclusion

This is not bad luck; it is what an honest retail-EOD program *should* produce, for
reasons the literature predicts and this program observed directly:

- **Concentration destroys diversified edges.** Documented anomalies are
  value-weighted decile spreads across hundreds of names (Hou-Xue-Zhang: 65–82% fail
  under value-weighting). K=1–3 cannot reconstruct them.
- **The edges live where the floor forbids.** Anomaly alpha concentrates in **small,
  illiquid, hard-to-borrow** names (Avramov-Cheng-Metzker; Muravyev-Pearson-Pollet).
  A mandatory liquidity floor at $100–1,000 excludes exactly those names.
- **Post-publication decay.** McLean-Pontiff: anomalies decay 26–58% after publication.
  The program's one real effect (event-driven, E10/E15) faded post-2010 in-sample.
- **Two recurring executioners — the overnight gap and cost — measured directly.** The
  EX-DECOMP diagnostic (running every closed FAIL through the A/B/C ladder) found the
  IBS/mean-reversion family loses >½ its edge to the **overnight gap** a next-open EOD
  fill cannot capture, and that **turnover cost** independently sinks the rest
  (Chen-Velikov: ~93% of anomaly alpha dies under costs — observed in-repo). Only 1 of
  5 decomposed FAILs was truly signal-dead; the others had real gross structure that
  died to gap + cost + decay.

---

## 5. The one real anomaly — and why it is uncatchable

The program's most instructive single result. Using free FINRA consolidated short
interest (2018–2026), **days-to-cover is a real, correctly-signed anomaly**: the
most-shorted large-caps underperformed, and a frictionless long-short spread showed
+18.4% / Sharpe 0.98. It was briefly, and wrongly, called "the program's strongest
edge."

**Properly costed (X2b), it is a FAIL.** Real short accounting + a borrow-fee sweep +
fair turnover collapse the spread to 9.2% / Sharpe 0.56 at a realistic 5% borrow, with
only 5 of 9 years positive; the **pure short is negative at every borrow level**
(the "most-shorted" basket is a mix — several names rallied — plus volatility drag in a
bull tape). The long-only deployable leg loses to SPY on a risk-adjusted basis. The
edge is real, market-neutral, lumpy, and requires **shorting** — impossible at
$100–1,000 with no fractional shorting. **The program's one genuine anomaly is one it
structurally cannot trade**, and the honest test found that with a $0 borrow sweep
before any account was funded. *(This paragraph reflects a correction: the initial
X2 write-up over-weighted the frictionless number; X2b corrected it, and the record
preserves both.)*

---

## 6. What is deployable, and what went live

- **Deployable-ish:** E6, a 1× moving-average rotation, survives a US regime-spanning
  test as a **drawdown-control overlay** (cuts a 83% drawdown to ~52% with
  roughly market-level return) — market-dependent (works in 3/5 non-US regimes) and
  explicitly **not** the high-return goal. It, plus the weak E18 VIX-TS PASS-RA, are
  the only forward-paper candidates.
- **Live:** **nothing.** No strategy passed the M2→M3 gate; live deployment remains
  blocked on the author's decision + a broker account, by design.

---

## 7. What the program demonstrates

A working model of honest quantitative research at small scale: falsifiable
pre-registration, bias-aware experiment design, a regression tripwire, direct
cost/execution decomposition, and a documentation trail that records — and
corrects — its own errors. **Thirty pre-registered falsifications across eight
strategy families, zero high-return passes**, and a terminal claim that is *stronger*
for being negative: the retail-EOD, K=1–3, liquidity-floored swing-trading space
does not contain a robust high-return edge, and the discipline to prove that
cleanly is the result. The tell is in the near-misses — the program's most tempting
numbers (C1's in-window 19% CAGR, C7's 26%, C4's drawdown cuts) were each produced
*and then killed* by the pre-registered both-windows / risk-adjusted / era-honest
bars. A weaker process would have shipped one of them.

## 8. Reproducibility & artifacts

- Engine + tripwire: `swing_bot/` (`prices`, `universe`, `coverage_gate`, `signals`,
  `backtest`, `rotation`, `test_frozen`). Every runner: `scripts/run_*.py`; every
  prereg: `docs/prereg_*.md`; every result: `docs/research/`.
- Live snapshot: `HANDOFF.md`. Ground-truth history:
  `docs/Project Record — Full Chronological History.md`. Standing plan:
  `PRD_ROADMAP.md`. Prereg discipline: `docs/prereg_TEMPLATE.md`.
- This capstone supersedes the earlier partial write-up
  (`docs/findings_2026-07-09_experiment_arc.md`, E1–E7) as the complete synthesis.

*Status (2026-07-14): COMPLETE. All M8 survey candidates (C1/C3/C4/C6/C7 run, C2 closed
on probe) and all M9 free experiments (X1/X2/X2b/X3) are finished — 30 attempts, all
FAIL/closed. The remaining PRD items are Evan-gated only: M3 Alpaca paper deploy of the
E6-1× / E18-VIX-TS forward-paper candidates (the sole path to genuinely new,
out-of-sample evidence), and the paid/scope-gated probes (X5 analyst-revision $22, X6
crypto pilot). No free autonomous experiment remains; the documented method space is
exhausted.*
