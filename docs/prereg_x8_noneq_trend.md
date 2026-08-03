# Pre-registration — X8: non-equity trend sleeve (decorrelation candidate)

**Written 2026-08-02 (CDT) by Claude, directed by Evan. Attempt #36.**
**COMMITTED DOC-ONLY BEFORE ANY RUNNER CODE EXISTS** — the commit hash of this
file predates `scripts/run_x8_noneq_trend.py`. That ordering is the project's
core rigor claim; do not write the runner until this is committed.

## 1. Why this experiment exists

Evan (2026-08-02): "make the sleeves less correlated." Measured first (record
Appendix DN):

- Live (n=11 daily returns, 12 sessions): pairwise correlation **+0.95 / +0.94
  / +0.86**; 7–9 of 11 days have byte-identical returns.
- Structural (4,226 sessions, 2009-09→2026-07): **m10_1_nagel runs the
  IDENTICAL e6 rule on 69.7% of days** (its stress arm engages only 30.3%);
  e6 vs e18 hold the same position **84.0%** of days; **all three are
  effectively long simultaneously 65.3%** of days. All three trade QQQ.

The three sleeves therefore deliver roughly ONE sleeve's worth of independent
forward evidence — which matters because M3's product is EVIDENCE, not returns.

**The correlation is not sloppiness; it is the honest consequence of the
program's own results.** 35 attempts produced exactly one survivor: 200-DMA
trend gating (E6 — and E6 is explicitly *drawdown control, not a return
enhancer*). Applied to other EQUITY regimes it is market-dependent (E7: works
3/5 non-US regions) and to crypto it failed one-window (X6). There is no
validated uncorrelated candidate on the shelf. You cannot diversify into
strategies you do not have — you have to test a new one.

**The gap this targets:** the tradeable universe (`swing_bot/universe.py`) is
100% equity — US indices, 11 SPDR sectors, country ETFs, leveraged equity.
`IEF` appears in the project only as the *denominator* of X7's HYG:IEF credit
ratio, never as a traded instrument. **The surviving rule has never been tested
on a non-equity asset.**

## 2. Hypothesis

**H1 (working):** The 200-DMA trend gate generalizes beyond equities. A
trend-gated position in a non-equity asset produces a return stream that is
(a) not value-destroying, and (b) structurally uncorrelated with the three
live QQQ sleeves — making it worth spending forward-paper evidence on.

**H0 (null / rival):** The trend gate carries no edge outside equities; a
trend-gated non-equity sleeve either destroys value versus simply holding the
asset, or its correlation to the existing sleeves is not low enough to add
independent evidence. Under H0 the correct action is to deploy NOTHING and
record that the program has no uncorrelated candidate.

H0 is the honest default given E7 (market-dependent across equity regions) and
X6 (crypto FAIL). **A FAIL here is a fully acceptable, publishable outcome.**

## 3. Arms (pre-declared, fixed before any data is pulled)

| arm | instrument | why |
|---|---|---|
| **(a)** | **GLD** (SPDR Gold Shares) | Deepest-liquidity gold ETF; return stream driven by real rates / risk-aversion, not equity earnings. Inception 2004-11. |
| **(b)** | **TLT** (20+yr Treasuries) | Long-duration rates — the other classic non-equity diversifier. Inception 2002-07. |

**MULTIPLE-COMPARISON DISCLOSURE:** testing 2 arms roughly doubles the chance
that one clears by luck alone. This is declared BEFORE running (precedent: E18
pre-declared 4 gates). If exactly one arm clears and the other misses badly,
that asymmetry is reported as a weakness, not smoothed over.

## 4. Rule (fixed — no tuning after results)

Identical in form to E6, deliberately, so this tests the ASSET, not a new rule:

- **Signal:** at the close of day T, long the asset iff `close > SMA200(close)`;
  else cash.
- **Execution:** next open (T+1). EOD only — no intraday logic (project hard rule).
- **Cost:** 1 bp per side (broad, liquid ETF tier — the same tier E18/X7/m10
  use for QQQ). GLD and TLT are both top-decile-liquidity US ETFs.
- **Sizing:** K=1, full capital in the single instrument. CAP0 = $1,000.
- **Data:** split-adjusted, dividend-UNADJUSTED (`auto_adjust=False`), matching
  every other consumer in this project. **Dividend-unadjusted materially
  understates TLT** (a coupon-bearing asset); this is a KNOWN, DECLARED bias
  against arm (b) and must be restated in the results, not discovered later.

## 5. Windows

Per-asset, from the asset's first available bar (each asset's real inception,
fetched empirically — never an invented date):

- **GATE window:** inception → 2013-12-31 (contains the 2008 GFC).
- **SEC window:** 2014-01-01 → present.

Both windows are reported for every arm. This is the project's standard
GATE/SEC dual-window convention (E18: 2000–13 / 2014+; X7: 2007–13 / 2014+).

## 6. Verdict criteria — **a DIVERSIFIER bar, not the D1 return bar**

**Stated plainly and BEFORE results, because it differs from D1 and that
difference must not look retrofitted:** this sleeve is not a high-return
candidate and will not be claimed as one. Its justification is
evidence-independence. Using D1's `CAGR ≥ 15%` here would be the wrong
instrument — gold and long bonds have no plausible 15%/yr trend-gated CAGR, so
D1 would reject on a criterion this sleeve was never meant to satisfy.

An arm **CLEARS** only if ALL FOUR hold:

1. **DECORRELATION (the actual purpose):** |correlation of daily returns to the
   e6_1x rule| **≤ 0.30**, measured over the full common window.
2. **NOT VALUE-DESTROYING:** net CAGR **> 0%** in **BOTH** windows.
3. **RUIN GUARD:** max drawdown **≤ 60%** in **BOTH** windows (the project's
   standing ceiling, unchanged).
4. **THE GATE MUST EARN ITS KEEP:** annualised Sharpe **>** the same asset's
   buy-and-hold Sharpe in **BOTH** windows. This is exactly the bar E6 and X6
   were judged on — if trend-gating does not beat simply holding the asset,
   there is no edge, only exposure.

**Any arm failing ANY of the four = FAIL for that arm. No tuning, no window
shopping, no threshold moves after seeing results.**

D1 numbers (CAGR/DD/Sharpe both windows) are REPORTED for every arm regardless,
so the result is comparable with the other 35 attempts.

## 7. What happens next, pre-committed

- **If an arm CLEARS:** it becomes forward-paper sleeve #4, added ALONGSIDE the
  existing three, which are **not modified** (their preregs `0526ea2`,
  `f32b008`, `prereg_m10_1_nagel_switch.md` remain intact and their forward test
  uncontaminated — see §8).
- **If BOTH arms FAIL:** deploy nothing. Record that the program has no
  uncorrelated candidate and that the three live sleeves remain ~one strategy.
  That is a legitimate result, not a failure of the exercise.

## 8. Rigor constraint — the running sleeves are NOT touched

The three live sleeves are a pre-registered forward test. Editing what a
RUNNING sleeve trades would (1) break its pre-registration, (2) destroy the
accumulated forward evidence, and (3) be exactly "changing the strategy after
seeing results," which project CLAUDE.md forbids: *"Risk appetite changes gate
NUMBERS, never rigor DISCIPLINE (prereg before results; no tuning a FAIL)."*
The forward-paper record is this project's single uncontaminated evidence lever.
**Decorrelation is achieved by ADDING a newly pre-registered sleeve, never by
mutating the running three.**

## 9. Known limitations, declared up front

- **Dividend-unadjusted prices understate TLT** (§4). Declared bias against arm (b).
- **2 arms = multiple comparisons** (§3).
- **A trend gate on any asset is a drawdown-control device** (E6's finding);
  expect modest returns, and do not re-frame that as a disappointment later.
- **Low measured correlation is not a guarantee of future independence** —
  cross-asset correlations spike in crises (the moment diversification is most
  wanted). If an arm clears, this caveat rides with it into the sleeve docs.
- **Broker mirroring for a 4th sleeve needs a 4th Alpaca paper account**, which
  only Evan can create. **BLOCKED-ON-EVAN — reported, never worked around.**
  Until then a cleared sleeve runs DB-ledger-only, which is explicitly
  sufficient: the DB ledger IS the forward-paper evidence, independent of
  whether a sleeve is broker-mirrored (`daily_swing_paper.py` docstring, pt 3).
