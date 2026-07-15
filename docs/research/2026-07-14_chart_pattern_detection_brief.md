# Research Brief — Algorithmic Chart-Pattern Detection (feeds PRD M11)

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Question:** Can rule-based (NOT LLM) algorithmic detection of the chart *shapes* retail
traders are taught — head-and-shoulders, double top/bottom, triangles, flags — produce a
cost-surviving, out-of-sample, **long-only, K=1–3, retail-EOD** swing edge on the survivor
universe? And if run, how should M11 be designed so a pass is real and a fail is clean?

**Audience:** the M11 prereg (`prereg_m11_chart_patterns.md`, not yet written). This brief
is the stage-before-prereg survey; it does not run a backtest (that is M11 itself).

---

## TL;DR — verdict first

**Honest a-priori verdict for a *deployable* long-only retail-EOD pattern strategy: FAIL —
but the evidence is genuinely MIXED, and mapping it to this project's constraints is what
makes the FAIL prior sharp rather than lazy.** Three load-bearing facts:

1. **Patterns carry real but modest incremental *statistical* information** — Lo, Mamaysky &
   Wang (2000), the one rigorous algorithmic detector, established this on US stocks
   1962–96. But they were explicit: *informative ≠ profitable* ("patterns optimal for
   detecting statistical anomalies need not be optimal for trading profits").
2. **The single best-documented pattern is a SHORT signal this project cannot trade.**
   Savin-Weller-Zvingelis (2007), using LMW's own detector, found head-and-shoulders
   predicts ~5–7%/yr risk-adjusted **underperformance** (Russell 2000, 1990s) — but a
   standalone short strategy was **NOT profitable** ("the upward drift of the market
   overwhelms this underperformance"; "may work well … in hedged portfolios"). That is a
   short / market-neutral edge → the exact no-fractional-shorting wall that made the
   program's real short-interest anomaly (**X2/X2b**) uncapturable at $100–1,000.
3. **Snooping + costs are the executioners.** Sullivan-Timmermann-White (1999): best
   technical rules don't survive the data-snooping (Reality Check) adjustment and decay
   out-of-sample. Bajgrowicz-Scaillet (2012): on 1897–2011 Dow data, rule performance is
   "completely offset by … low transaction costs" *even in-sample*, and no method could
   pick the future-best rules ex ante.

**Net:** the tradeable evidence concentrates on the **side (short/hedged)** and **structure
(large diversified books)** this project structurally cannot use. The deployable **long-only**
side is where support is weakest — and where the program's own three breakout kills
(E8/E11/C3) already apply. **Run M11 as an honest kill-shot, not a hopeful engine** — its
job is to close the last untested mechanism gap ("even the *shapes* don't trade at retail
EOD"), with a small, honestly-disclosed chance of a forward-paper "PROMISING."

---

## Method

Desk research (an LLM can search/read, not run surveys or new experiments). Six web
searches across the academic + practitioner literature; targeted fetches for the two most
decision-critical primaries. **Limitations:** the two paywalled primaries (Savin et al.,
*J. Financial Econometrics*; Tsinaslanidis, *Expert Systems*) were read via an open
summary (CXO Advisory) and search abstracts respectively — the exact Savin caveat was
confirmed from the CXO summary, not the paper PDF. No new primary data (no backtest) was
generated; that is M11. **Hypotheses were fixed before collection** (below), per the
anti-confirmation gate.

**Hypotheses (pre-registered for this brief):**
- **H1 (working):** no cost-surviving, OOS, *long-only* deployable chart-pattern edge exists
  at retail EOD / K=1–3 on the survivor universe → FAIL.
- **H0 (rival / null-buster):** some patterns (esp. reversal H&S / double-bottom, in large
  liquid names) carry tradeable predictive info that survives costs → PROMISING.
- **H2 (method):** the outcome depends on the detection method and the snoop-adjustment; a
  poorly-pinned detector data-mines a false pass.

---

## Findings

**1. Patterns are informative, but "informative ≠ profitable" (LMW 2000).** Nonparametric
kernel-regression smoothing + local-extrema geometry over ~10 classic patterns, applied to
a large US cross-section 1962–96, found several patterns carry incremental information
(conditional return distribution ≠ unconditional), concentrated short-term. LMW did **not**
demonstrate a cost-surviving trading rule and flagged the anomaly-vs-profit gap directly.
*(Corroborated by finding 2's independent replication.)*

**2. The best-supported pattern (H&S) is short-side and non-deployable here (Savin et al.
2007).** Using LMW's algorithm (plus analyst filters) on S&P 500 + Russell 2000, 1990–99:
a standalone H&S short strategy was **not profitable**; the real result was **conditional
underperformance of ~5–7%/yr risk-adjusted** for Russell 2000 names in the 3 months after
the pattern — a genuine predictive signal, but bearish, small-cap, and only monetizable in
a **hedged / market-neutral** structure. **Direct map to this program:** this is the X2
lesson repeated — the one pattern with strong evidence is one the $100–1,000, long-only,
no-fractional-shorting mandate cannot trade. The *deployable* long-side analogues
(inverse-H&S, double-bottom, bullish breakouts) have materially weaker documented support.

**3. Data-snooping + transaction costs kill technical rules (STW 1999; Bajgrowicz-Scaillet
2012).** STW expanded Brock-Lakonishok-LeBaron's rule set to ~7,846 rules on 100 yrs of
Dow data under White's Reality Check: the best rule's edge largely vanishes after the
snooping adjustment and profitability is low in the 10-yr OOS period. Bajgrowicz-Scaillet
(FDR, 1897–2011) is blunter: performance is **offset by even low transaction costs in-sample**,
and persistence tests show no ex-ante way to pick the future winners. **Implication for
M11:** trying many patterns/parameters is the failure mode; the prereg must pin ONE
consolidated spec or snoop-adjust explicitly.

**4. Modern evidence is mixed / positive-leaning but snoop-caveated (Tsinaslanidis 2021,
et al.).** A 2021 *Expert Systems* study on 560 NYSE stocks reports 92.5% of experiments
profitable "if the analysis is reduced to the parameter values aligned with technical
analysis," costs reducing (not erasing) profit; DFDR studies on MSCI indices also report
some post-cost profitability. **Read skeptically:** "reduced to TA-aligned parameter
values" is precisely the ex-post parameter selection STW/Bajgrowicz-Scaillet warn about;
the abstract did not establish a clean OOS, single-pre-committed-spec result. Real
signal-of-life, not a clean deployable claim.

**5. Detection method matters, and LMW's smoother has a look-ahead trap.** Deployable
detectors: (a) causal rolling local-extrema / zig-zag geometry, (b) perceptually-important-
points (PIP), (c) LMW two-sided kernel regression. **Critical:** LMW's kernel smoother is
**non-causal** (each smoothed point uses future prices) — fine for their statistical study,
**look-ahead for trading.** A deployable M11 detector must use a **causal** smoother, or
confirm a pattern **only after the neckline/confirmation break** (no future bars).
Practitioners also note pattern presence is subjective/ambiguous — the detector's tolerance
parameters are a snooping surface and must be pinned a priori. *(ML/CNN chart-image
classifiers are a separate, ML-driven literature — out of scope for Evan's rule-based ask.)*

**6. Program-internal mechanistic prediction (the sharpest prior).** Continuation patterns
(flags, triangles, breakouts) ARE breakouts → inherit the breakout family's three kills
(E8/E11/C3; C3 showed the channel exit is a whipsaw tax). Long reversal patterns
(double-bottom, inverse-H&S) are cousins of the reversal near-miss that cleared then
decayed (E16/C1). And next-open execution bleeds the same overnight gap the program keeps
losing (EX-DECOMP). Every internal analogue points to FAIL.

**Hypothesis scorecard:** H1 **survives** (and is sharpened). H0 **partially survives but
in a non-deployable form** — the tradeable evidence is short-side/hedged/large-book, not
long-only-K=1–3. H2 **confirmed** — method + snoop-adjustment are decisive.

---

## Ranked design options for M11

1. **(RECOMMENDED) Causal LMW detector; ONE consolidated LONG-side reversal spec
   (inverse-H&S + double-bottom) as the deployable arm, WITH a reported short-only H&S /
   double-top measurement.** Full-window 2000–2013 gate + 2014→ secondary (D1); survivor
   universe (asymmetric — only a FAIL is clean); next-open fills; tiered costs +15 bps
   stress; parameters pinned from LMW; a single spec (no multi-pattern snooping). *Tradeoff:*
   cleanest honest kill-shot; tests the *deployable* side directly; the short-side readout
   documents (X2-style) that the best-supported pattern is uncapturable. This is the
   reversal-side analogue of C3's breakout kill-shot. **Lead with this.**
2. **Broad multi-pattern scanner (H&S, triangles, flags, double tops/bottoms, cup-handle)
   under an explicit FDR / Reality-Check adjustment.** *Tradeoff:* most "complete," but
   maximal snooping surface and heaviest build; the adjustment will very likely null it
   (that IS the demonstration, à la STW) — expensive for a near-certain null.
3. **Continuation / breakout patterns only (flags, triangles).** *Tradeoff:* lowest value —
   it is the breakout family already killed 3× (E8/E11/C3); near-certain FAIL, little new
   information. Skip unless Evan wants the explicit "breakouts, one more time as *shapes*"
   exhibit.

---

## What would change this conclusion (falsifiers to watch in M11)

- A **long-only** inverse-H&S / double-bottom spec clearing **PASS-HR full-window** on the
  survivor universe with the **causal** detector, a snoop-adjustment, AND realistic costs —
  that would be a genuine surprise → route to M3 forward paper (never a live claim on a
  survivor universe).
- Evidence the **deployable long side** (not just short H&S) carries post-cost OOS edge in
  liquid large-caps — the current literature does not support this.
- A **causal** detector materially outperforming the two-sided one — would suggest LMW's
  look-ahead is the whole story and the "signal" is an artifact.

---

## Sources (accessed 2026-07-14)

- Lo, Mamaysky & Wang (2000), "Foundations of Technical Analysis," *J. Finance* 55(4) —
  [NBER w7613](https://www.nber.org/papers/w7613),
  [SSRN 228099](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=228099).
- Savin, Weller & Zvingelis (2007), "The Predictive Power of Head-and-Shoulders Price
  Patterns in the US Stock Market," *J. Financial Econometrics* 5(2) —
  [SSRN 1145511](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1145511);
  precise caveat via
  [CXO Advisory summary](https://www.cxoadvisory.com/technical-trading/testing-the-head-and-shoulders-pattern/).
- Sullivan, Timmermann & White (1999), "Data-Snooping, Technical Trading Rule Performance,
  and the Bootstrap," *J. Finance* 54(5) —
  [SSRN 160330](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=160330).
- Bajgrowicz & Scaillet (2012), "Technical Trading Revisited: False Discoveries, Persistence
  Tests, and Transaction Costs," *J. Financial Economics* 106(3) —
  [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X1200116X).
- Tsinaslanidis (2021), "What makes trading strategies based on chart pattern recognition
  profitable?" *Expert Systems* —
  [Wiley exsy.12596](https://onlinelibrary.wiley.com/doi/abs/10.1111/exsy.12596) *(abstract
  only; paywalled)*.
- Detection-method practitioner references (secondary):
  [Alpaca — detecting/trading chart patterns in Python](https://alpaca.markets/learn/algorithmic-trading-chart-pattern-python),
  [QuantConnect — H&S detection](https://www.quantconnect.com/research/15603/head-amp-shoulders-ta-pattern-detection/).

*Program prior sources (in-repo): EX-DECOMP overnight-gap finding; E8/E11/C3 breakout kills;
E16/C1 reversal near-miss; X2/X2b short-side wall. See the append-only record + capstone §8.*
