# Pre-registration — X9: pairs / relative-value (market-neutral rule family)

**Written 2026-08-02 (CDT) by Claude, directed by Evan. Attempt #37.**
**COMMITTED DOC-ONLY BEFORE ANY RUNNER CODE EXISTS** — this file's commit hash
predates `scripts/run_x9_pairs.py`.

## 1. Why this experiment exists

Evan (2026-08-02), after X8 failed: test a **different rule family**. The
200-DMA trend family is exhausted — six one-window deaths (E6-downgrade, C7,
X6, X7, M10-2, X8a) across US equity, non-US equity, crypto, credit and gold.
Asking it new questions is no longer informative.

Re-reading the project's own survey (`docs/research/2026-07-12_swing_method_full_survey.md`)
and removing everything since tested (C1 residual reversal, C3 breakout, C6
FOMC, X1 vol-targeting, X3 RegSHO), the remaining untested candidates are
mostly **1–12 month horizons** — outside this project's days-to-weeks swing
scope — or data-gated.

**Pairs / relative value is the one structurally different family left**, and
it is the only one that is **market-neutral by construction**. That matters
because the driving goal (record DN) is decorrelation: every strategy this
program has deployed is "long QQQ or cash," so its correlation to equity beta
is ~1 whenever invested. A market-neutral spread has no such structural beta.

## 2. Hypothesis

**H1 (working):** A distance-based pairs strategy on liquid ETFs produces a
return stream that is profitable after costs and structurally uncorrelated with
the three live QQQ sleeves.

**H0 (null / rival, AND THE FAVORED PRIOR):** The pairs edge documented by
Gatev-Goetzmann-Rouwenhorst (2006) has **decayed to approximately nil net of
costs post-2002** (Do & Faff 2010). Under H0, X9 produces a low-or-negative
Sharpe in the modern window and deploys nothing.

**I expect H0 to win.** This is stated before running, so a FAIL cannot later
be dressed up as a surprise, and a PASS cannot be claimed as if it were
predicted. The reason to spend attempt #37 on a family with a bad prior:
(a) it is the last structurally-decorrelating family available, (b) confirming
a documented decay on this project's own data and cost model is a legitimate
result, and (c) the alternative candidates fail the horizon constraint outright.

## 3. Universe, formation, and rule (fixed — no tuning after results)

**Universe:** the frozen 29-ETF universe (`swing_bot/universe.py`) — liquid,
long-history, and the same basket every other experiment uses. Leveraged
members (TQQQ/UPRO/SPXL/SOXL/TNA) are EXCLUDED: their embedded decay breaks the
mean-reverting-spread premise. Pairs are formed only between ETFs whose
`data_start` precedes the formation window.

**Formation (Gatev's canonical distance method — chosen because it is what
Do-Faff measured the decay ON; a fancier cointegration test would change two
things at once):**
- Rolling **252-session formation window**, re-formed every **63 sessions**.
- Normalize each member's close to 1.0 at window start.
- For every eligible pair, compute the **sum of squared deviations (SSD)**
  between the two normalized series.
- Select the **K = 3 lowest-SSD pairs** to trade in the following 63 sessions.

**Trading rule:**
- Track the spread `s = normA - normB` (normalized at the formation-window end)
  and its formation-window standard deviation `sigma`.
- **OPEN** when `|s| > 2.0 * sigma` at a close: long the underperformer, short
  the outperformer, **equal dollar** on each leg.
- **CLOSE** on the first close where the spread crosses zero (convergence), OR
  at a **20-session time stop**, OR at the end of the trading window.
- Signal at close, **execute next open**. EOD only (project hard rule).
- **Cost: 5 bps per side per leg** (a round trip therefore pays 4 legs ×
  5 bps). Deliberately not the 1 bp broad-ETF tier — a pairs round trip is four
  executions and understating that is how this family is usually flattered.
- Capital: CAP0 $1,000, split evenly across up to K=3 open pairs.

## 4. Windows

Project-standard dual window, on the common data range:
- **GATE:** window start → 2013-12-31
- **SEC:** 2014-01-01 → present

## 5. Verdict criteria (pre-declared)

A market-neutral spread has no beta, so D1's `CAGR ≥ 15%` is the wrong
instrument — the same reasoning as X8 §6, declared BEFORE results for the same
reason. Market-neutral strategies are judged on **Sharpe**.

**X9 CLEARS only if ALL FOUR hold:**

1. **Annualised Sharpe ≥ 0.50 in BOTH windows.** (Gatev reported ~1.0+
   pre-2002; Do-Faff report ~nil after. 0.50 is deliberately set between them:
   low enough that a real-but-decayed edge could clear, high enough that noise
   cannot.)
2. **Net CAGR > 0 in BOTH windows** (after the 4-leg cost model).
3. **maxDD ≤ 60% in BOTH windows** (project ruin guard, unchanged).
4. **|correlation of daily returns to the e6_1x rule| ≤ 0.30** (the
   decorrelation purpose — same threshold X8 used).

**Failing ANY of the four = FAIL. No tuning, no window shopping, no threshold
changes after seeing results.** D1 numbers reported regardless for
comparability with the other 36 attempts.

## 6. Pre-committed next steps

- **If X9 CLEARS:** it is eligible as forward-paper sleeve #4, **added
  alongside** the untouched existing three — subject to the deployment
  feasibility check in §7, which may still block it.
- **If X9 FAILS:** deploy nothing; record that the last structurally
  decorrelating family also fails, and that the three live sleeves remain
  ~one strategy. Combined with X8 that is a substantive program-level finding,
  not merely a second miss.

## 7. Deployment feasibility — declared NOW, not after a convenient result

Even a CLEARING result may be **undeployable at this account size**, and that
must not be discovered late:
- Pairs requires **shorting**. Alpaca paper supports short sales, **but not
  fractional shorts** — short legs need whole shares.
- At **$1,000** split across 3 pairs (~$333/pair, ~$167/leg), most universe
  members trade well above $167/share, so the short leg cannot be sized
  correctly. **The backtest is therefore a test of the FAMILY, not a
  deployable configuration at $1,000.**
- If X9 clears, the honest options are: deploy DB-ledger-only (fractional,
  no broker mirror), deploy at a larger notional, or record it as
  "validated but undeployable at this capital." **This is reported, never
  worked around, and never faked with a stub claimed live.**

## 8. Rigor constraint (unchanged from X8 §8)

The three running sleeves are **not modified**. Their preregs (`0526ea2`,
`f32b008`, `prereg_m10_1_nagel_switch.md`) and accumulated forward evidence
remain intact. Decorrelation comes from ADDING a pre-registered sleeve, never
from mutating the running three.

## 9. Known limitations, declared up front

- **Survivorship:** the ETF universe is frozen as of 2026-07-08 and contains
  only funds that still exist. Pairs formed on survivors flatter the strategy —
  the same asymmetric-falsification caveat that applies to M11's 39 large-caps:
  **only a FAIL is clean; a PASS is forward-only.**
- **Dividend-unadjusted prices** (project convention) inject a small spurious
  spread between members with different yields — a real, declared bias for a
  spread strategy specifically.
- **In-sample formation:** SSD selection uses the formation window only and
  trades the following window, so there is no look-ahead — but the 252/63/2σ/20
  parameters are Gatev's published defaults, adopted wholesale precisely so they
  are not tuned here.

## Sources

- Gatev, Goetzmann & Rouwenhorst (2006), *Pairs Trading: Performance of a
  Relative-Value Arbitrage Rule*, RFS 19(3).
- Do & Faff (2010), *Does Simple Pairs Trading Still Work?* — documents the
  post-2002 decay that motivates H0.
