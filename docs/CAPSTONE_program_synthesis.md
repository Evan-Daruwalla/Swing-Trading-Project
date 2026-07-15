# Swing-Trading Falsification Program — Capstone Synthesis

**Evan Daruwalla · synthesis dated 2026-07-14 (CST) · repo:
https://github.com/Evan-Daruwalla/Swing-Trading-Project**

> This is the standing capstone: the single-document account of what the program set
> out to do, how it was run, what it found, and why. The append-only
> `docs/Project Record — Full Chronological History.md` remains ground truth for
> dated detail; this synthesizes it. **Standing counts (2026-07-14): 0 CLEAN PASS-HR /
> 1 IN-SAMPLE-COMPOSED PASS-HR (M10-1 Nagel Switch, forward-paper-only) / 1 weak PASS-RA
> (E18) / 34 pre-registered attempts — 33 equity across 9 strategy families + a
> state-conditioned synthesis arc, plus 1 crypto pilot.** The fixed-single-strategy space
> (E/C/X families) is exhausted and the M10 synthesis arc (composing the evidence into
> state-conditioned strategies) is complete — but **the program is NOT concluded.** M10 found
> the one design that clears PASS-HR *in-sample* (the Nagel Switch), a forward-paper
> hypothesis rather than a refutation of the terminal claim; and the last untouched mechanism
> family — **algorithmic chart-pattern detection** — has now been run and **FAILED** (M11,
> the 9th family; §3, §8), signal-dead on the deployable long side. The one untested
> *evidence* lever that remains is **M3 forward paper**. This reads as a progress report,
> not an obituary.

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

**Scope of the claim — and what it does NOT cover.** The claim is bounded by what was
tested: fixed-rule strategies over price/volume, factor, event, seasonality, regime,
informed-positioning, and crypto data. Two things sit outside it. (1) The M10 synthesis
arc showed that *state-conditioning* a losing fixed strategy on a causal regime variable
(VIX, per Nagel 2012) can clear PASS-HR **in-sample** — the Nagel Switch (§3, M10-1) — but
that pass is composed after seeing 31 results and buys known survivors in crashes, so it
is a forward-paper hypothesis, not a live edge. (2) One classical mechanism family has
**never been tested here:** algorithmic detection of the chart *shapes* retail traders are
taught (head-and-shoulders, double tops/bottoms, triangles, flag breakouts). Its prior is
weak (§8), but it is genuinely untested — so the honest statement is "no edge found in what
was tested," not "no edge exists." The program continues.

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
   GREEN across all 34 attempts.

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

## 3. Results ledger — 9 equity families + a synthesis arc + 1 crypto pilot, 34 attempts, 0 clean high-return passes

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
| Crypto pilot *(new domain)* | X6 | FAIL — BTC/ETH dual-MA trend @ 25 bps **crushes HODL in the 2018–22 bears** (29.6% vs 4.3%, DD 82%→61%) but **loses HODL's Sharpe in the 2023+ bull** (0.76 < 1.01); cost-robust (slow overlay). Reproduces E6's lesson: trend = drawdown control, not a return-enhancer over buy-and-hold. Paper-first; nothing live |
| *(closed on probe)* | C2 dividend-initiation | Only 3 first-ever initiations in 26 years among the survivors → insufficient event flow, no runner |
| Evidence synthesis *(state-conditioned)* | M10-1, M10-2 | **M10-1 Nagel Switch = the program's FIRST PASS-HR, but IN-SAMPLE-COMPOSED / forward-paper-only** (VIX>20 → C1 residual reversal, VIX≤20 → E6 trend; Nagel-2012 mechanism; gate 17.87% CAGR / DD 59.95% / Sh 0.66, sec 15.94% / 39.68% / 0.78) — composed after 31 results, survivor-flattered (buys known survivors in crashes), DD clears by 0.05 pp, breaks at VIX>18 (14.83%) and at 15 bps, fails PASS-RA (Sh 0.66) → **not clean, per the M10 data-snooping cap.** **M10-2** (2× QQQ stress mean-reversion, 5-day hold) = FAIL (gate 2.99% CAGR / **83.3% DD**) and **closes the E2 "c2c mirage"**: the 5-day hold neutralized the overnight gap (c2c 3.18% ≈ next-open 2.99%), proving the gap was hiding a *falling 2× knife into 2000–02/2008*, not alpha |
| Chart-pattern geometry *(shape, not a number)* | M11 | **FAIL — signal-dead** (attempt 34, the 9th family). Rule-based (NOT LLM) causal detection of long-side reversal shapes (double-bottom + inverse-H&S), fresh neckline break → next open, on the 39 survivors: gate **−0.14% CAGR / 50.4% DD / Sh 0.09**, loses SPY *and* survivorship-clean EW-39; frictionless Rung B ≈ 0 → the shape carries no directional edge. **Payload:** the survivor universe *destroys* the one documented (bearish) pattern edge — fwd-20 after a bearish top/H&S is +1.70% (> unconditional +1.15%), the opposite of Savin (2007), because survivorship removed exactly the names a bearish pattern predicts. Closes the last untested mechanism gap |

**Tally: 0 CLEAN PASS-HR, 1 IN-SAMPLE-COMPOSED PASS-HR (M10-1 Nagel Switch —
forward-paper-only), 1 weak PASS-RA (E18 VIX-TS), 34 pre-registered attempts (33 equity
across 9 families + a state-conditioned synthesis arc + 1 crypto pilot).** Full
per-experiment detail: the append-only record and `docs/research/`.

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
corrects — its own errors. **Thirty-four pre-registered attempts across nine equity
families, a state-conditioned synthesis arc, and a crypto pilot — zero CLEAN high-return
passes**, and a terminal claim that is *stronger* for being negative: the retail-EOD,
K=1–3, liquidity-floored swing-trading space does not contain a robust fixed-strategy
high-return edge — and it does not appear in crypto either, where trend timing reduces to
the same drawdown-control-not-alpha role as in equities. The tell is in the near-misses —
the program's most tempting numbers (C1's in-window 19% CAGR, C7's 26%, X6's 30%
crypto-gate CAGR, C4's drawdown cuts) were each produced *and then killed* by the
pre-registered both-windows / risk-adjusted / era-honest / vs-buy-hold bars. **The
sharpest demonstration is M10-1: the one design that actually CLEARED PASS-HR — and the
program still refused to call it a win**, because it was composed after seeing 31 results
and buys known survivors in crashes (the in-sample-composed cap). A weaker process would
have shipped C1, or crowned M10-1 the answer. This one labeled both as hypotheses for
forward paper and kept going.

## 8. The open frontier — what has NOT been tested, and what might still work

The program is a living falsification record, not a closed book. Three things could still
move the needle; only one is a genuinely new mechanism, and its prior is stated honestly.

**(a) Algorithmic chart-pattern detection (PRD M11) — RAN 2026-07-14 → FAIL (signal-dead).**
*Result:* gate −0.14% CAGR / Sharpe 0.09, loses SPY and survivorship-clean EW-39; frictionless
(Rung B) ≈ 0 → the shape carries no long-side directional edge (the E14 category). **Payload:**
the survivor universe *destroyed* the one documented pattern edge — fwd-20 after a bearish
top/H&S is +1.70% vs unconditional +1.15% (the OPPOSITE of Savin 2007), because survivorship
removed exactly the names a bearish pattern predicts. The prior below held exactly. Results:
`docs/research/2026-07-14_M11_chart_patterns_results.md`. The rationale, now confirmed:
every strategy above trades a *number* (an IBS value, a residual rank, a moving-average
cross, a short-interest ratio). None trades *shape* — the head-and-shoulders, double
top/bottom, triangle, and flag-breakout patterns retail traders are taught to read off a
chart. Detecting these algorithmically (rule-based geometry on daily OHLC, **not** an LLM)
is a real gap in "trying everything," and it is full-window testable (price-only, no data
wall → it can reach a true D1 tier, unlike every post-2000 experiment). **The prior is
weak but not zero.** The one rigorous academic detector — Lo, Mamaysky & Wang (2000,
*J. Finance*): kernel-smoothing + local extrema over ten classic patterns — found patterns
carry *modest incremental statistical information* (their conditional return distributions
differ from the unconditional) yet explicitly did **not** show it survives transaction
costs. Against that: Sullivan-Timmermann-White (1999) and Bajgrowicz-Scaillet (2012) show
technical-rule profits largely vanish after data-snooping / FDR correction and realistic
costs, and McLean-Pontiff decay applies with force — a pattern *taught publicly for
decades* is the definition of a published, arb-eligible signal. This program can even
predict its own result mechanistically: continuation patterns (flags, triangles,
breakouts) ARE breakouts, and the breakout family already died three times here
(E8/E11/C3 — C3 showed the channel exit is a whipsaw tax); reversal patterns (double
bottoms, inverse-H&S) are cousins of the reversal near-miss that cleared then decayed
(E16/C1). **Honest expectation: FAIL, extending the terminal claim to "even the shapes
don't trade at retail EOD" — with a small chance of a forward-paper 'PROMISING.'** The
disciplined build: adopt LMW's *published* detector parameters (externally anchored, not
fit), commit to ONE consolidated spec or a small pre-declared set with a snoop-adjustment
(the C3 kill-shot model), full-window D1, survivor-universe asymmetric framing, next-open
execution — was the plan, and it ran (FAIL, above). *(M11.1 brief,
`docs/research/2026-07-14_chart_pattern_detection_brief.md`: evidence is mixed, and the
best-supported pattern — head-and-shoulders — is a SHORT signal not profitable standalone
(Savin et al. 2007), the same no-shorting wall as X2; so the deployable lead is the
LONG-side reversal — inverse-H&S / double-bottom — and the detector must be causal, since
LMW's kernel smoother is look-ahead.)*

**(b) M3 forward paper — the only lever that produces UNCONTAMINATED evidence.** Every
number in this document is upper-bound-biased (survivorship) or in-sample (M10). The one
way to generate evidence that is neither is to deploy the forward-paper candidates —
E6-1× / E18 VIX-TS, and now the M10-1 Nagel Switch — to Alpaca **paper** and grade
implementation fidelity against a shadow backtest over a pre-committed 6–12-month window.
This does not "prove" an edge (the horizon is too short for statistical power on slow
signals — claiming otherwise would break the program's own rules), but it is the only
forward, look-ahead-free test available. **BLOCKED-ON-EVAN:** needs an Alpaca paper
account + the go.

**(c) Genuinely-untested levers, lower priority.** *Pairs / statistical arbitrage* on the
survivor universe (cointegration-based, market-neutral) is a mechanism never tried here —
but market-neutral at $100–1,000 with no fractional shorting is the same wall that made
X2/X2b's real short-interest anomaly uncapturable. *LLM-forward overlays* (the standing
`e1_llm_veto` design) are forward-only by construction — they cannot be backtested without
training-cutoff look-ahead — so they attach to M3, not to a backtest. *Short-interest done
right* (the one real anomaly, X2) needs paid point-in-time borrow-fee data (Ortex ~$129)
and a shorting account. *Intraday / MOC execution* — the only fill that captures the ~54%
overnight component the program keeps losing — is blocked until an intraday data source
exists (the EOD-only hard rule).

**What this section is not.** It is not a claim that any of these will work — the base
rate says they won't, and the honest prior on (a) is FAIL. It is the explicit statement
that the search is not finished, and that the next honest experiment is M11.

## 9. Reproducibility & artifacts

- Engine + tripwire: `swing_bot/` (`prices`, `universe`, `coverage_gate`, `signals`,
  `backtest`, `rotation`, `test_frozen`). Every runner: `scripts/run_*.py`; every
  prereg: `docs/prereg_*.md`; every result: `docs/research/`.
- Live snapshot: `HANDOFF.md`. Ground-truth history:
  `docs/Project Record — Full Chronological History.md`. Standing plan:
  `PRD_ROADMAP.md`. Prereg discipline: `docs/prereg_TEMPLATE.md`.
- This capstone supersedes the earlier partial write-up
  (`docs/findings_2026-07-09_experiment_arc.md`, E1–E7) as the complete synthesis.

*Status (2026-07-14): ONGOING — finalized THROUGH the M10 synthesis arc, not closed. The
fixed-single-strategy space (E/C/X families) is exhausted, M10 is complete (M10-1 Nagel
Switch = in-sample PASS-HR / forward-paper-only; M10-2 closed the E2 "c2c mirage"), and
**M11 — the last free backtestable mechanism (chart-pattern geometry) — ran 2026-07-14 →
FAIL** (signal-dead; the survivor universe destroyed the one documented pattern edge). **What
remains open:** no free autonomously-runnable backtest remains — the one untested *evidence*
lever is M3 Alpaca paper deploy of the three forward-paper candidates (E6-1× / E18-VIX-TS /
M10-1), the sole source of uncontaminated evidence (Evan-gated: account + go); the
lower-priority untested levers need new capital/data (pairs/stat-arb — shorting; LLM-forward —
M3; short-interest-done-right — paid borrow data; intraday/MOC — an intraday feed); X5
analyst-revision drift (**BLOCKED — $22 FMP feed**); live-money crypto (custody gate).
Standing at **34 attempts / 0 clean PASS-HR / 1 in-sample PASS-HR / 1 weak PASS-RA.** **The
research phase is NOT declared done — M3 forward paper is the open lever.***
