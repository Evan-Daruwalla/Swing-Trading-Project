# X9 — pairs / relative-value (market-neutral family): **FAIL**

**Swing Trading · 2026-08-03 (CDT) · attempt #37**
Prereg: `docs/prereg_x9_pairs_relative_value.md`, committed doc-only as
**`00c8c44`**, before `scripts/run_x9_pairs.py` existed.
**H0 was the pre-declared favored prior, and H0 won.**

## TL;DR

FAIL on 3 of 4 pre-registered criteria; only the correlation criterion passed
(**−0.057**). A post-hoc zero-cost diagnostic splits the failure cleanly in two:
**the gross edge is already ~nil in the modern window (Sharpe −0.05, 2014+),
and the 4-leg cost structure then destroys what little remains** (net −70% of
capital). This reproduces Do & Faff (2010) — the Gatev (2006) pairs edge decayed
to approximately nothing post-2002 — independently, on this project's own data
and cost model. Nothing deployed.

## Setup

Gatev's canonical distance method at his **published defaults, adopted
wholesale so nothing is tuned here**: 252-session formation, 63-session trading,
K=3 lowest-SSD pairs, entry when |spread| > 2·formation-σ, exit on spread sign
change (convergence) or a 20-session stop. Long the underperformer, short the
outperformer, equal dollar. Signal at close, execute next open.

Universe: the frozen 29-ETF universe, **leveraged members excluded** (embedded
decay breaks the mean-reverting premise). 6,927 sessions, 1998-12-22 → 2026-07-09.

Cost: **5 bps per side per leg** — a round trip pays **4 legs = ~20 bps**.
Deliberately not the 1 bp broad-ETF tier; understating the leg count is the
usual way this family gets flattered.

## Results — pre-registered (net of cost)

| | CAGR | maxDD | Sharpe |
|---|---|---|---|
| GATE (→2013-12) | **−2.50%** | 41.3% | **−0.47** |
| SEC (2014-01→) | **−6.71%** | 60.2% | **−1.40** |

- Trades: **2,196 opened · 1,920 converged (87.4%) · 274 time-stopped**
- Final NAV: **$294.16** from $1,000
- Correlation to the e6 rule: **−0.0571** over 6,674 sessions

| criterion | result |
|---|---|
| ① Sharpe ≥ 0.50 both windows | **FAIL** |
| ② CAGR > 0 both windows | **FAIL** |
| ③ maxDD ≤ 60% both windows | **FAIL** (60.2% in SEC) |
| ④ \|corr to e6\| ≤ 0.30 | **PASS** (−0.057) |

**VERDICT: FAIL → deploy nothing** (prereg §6).

## Diagnostic — zero cost (post-hoc, NOT part of the gated test)

Run only to separate *"no edge"* from *"edge eaten by costs"*. Labelled as a
diagnostic exactly as M11's short-side check was; it does not change the verdict.

| | CAGR | maxDD | Sharpe |
|---|---|---|---|
| GATE gross | +2.07% | 9.2% | **0.43** |
| SEC gross | −0.35% | 15.8% | **−0.05** |

Final gross NAV $1,273.57 (vs $294.16 net).

**Both failure modes are real and they compound:**

1. **The edge had already decayed before costs.** Gross Sharpe is 0.43 in the
   GATE window — below the 0.50 bar even for free — and **−0.05 in 2014+, i.e.
   literally nothing.** That is Do & Faff's decay, reproduced here independently.
2. **Then the cost structure kills it.** ~81 round trips/year × ~20 bps ≈ 16%/yr
   of drag, which converts a nil gross edge into −70% of capital.

The mechanism itself is *not* broken: **87.4% of trades converged.** Spreads do
mean-revert. The reversion is simply smaller than four legs of transaction cost.
That distinction matters — this is not "the signal doesn't exist," it is "the
signal is smaller than the toll."

## What this means for the program

**Decorrelation is not the scarce resource; edge is.** Three consecutive
attempts at a decorrelated sleeve produced near-zero correlations to the live
sleeves and no deployable edge:

| attempt | family | corr to e6 | outcome |
|---|---|---|---|
| X8a GLD | non-equity trend | **+0.089** | FAIL (3 of 4) |
| X8b TLT | non-equity trend | **−0.191** | FAIL |
| X9 pairs | market-neutral relative value | **−0.057** | FAIL |

Every one cleared the correlation bar comfortably. None cleared profitability.
The three live sleeves therefore remain **~one strategy** (record DN: m10 runs
the identical e6 rule on 69.7% of 4,226 sessions), and that is now a documented
consequence of the evidence rather than an oversight.

This also closes the last structurally different family the July-12 survey
identified as in-scope and untested. The remaining untested candidates are
1–12 month horizons (outside the days-to-weeks swing scope) or data-gated.

## Deployment feasibility (declared in prereg §7, restated)

Moot given the FAIL, but recorded as promised: even a clearing result would have
been **undeployable at $1,000** — Alpaca paper does not support fractional
shorts, and ~$167/leg cannot buy a whole share of most universe members. This
tested the **family**, never a deployable configuration.

## Limitations (declared before running)

- **Survivorship:** the ETF universe is frozen 2026-07-08 and holds only funds
  that still exist. Pairs formed on survivors *flatter* the strategy — so the
  FAIL is clean (a PASS would have been forward-only).
- **Dividend-unadjusted prices** inject a small spurious spread between members
  with different yields — a real declared bias for a spread strategy specifically.
- Gatev's parameters were adopted wholesale and **not** tuned; a tuned variant
  might do better, but tuning after a FAIL is what this project forbids.

## What would change this conclusion

- A cost model materially below ~20 bps/round-trip (institutional execution),
  which is exactly what this retail-constrained program cannot assume.
- Intraday or higher-frequency convergence, which needs a data source the
  project does not have.
- A different pair-selection method (cointegration tests rather than SSD
  distance) — but the *gross* SEC Sharpe of −0.05 suggests the problem is the
  decayed edge, not the selection rule.

## Provenance

- Prereg `00c8c44` (doc-only) → runner `scripts/run_x9_pairs.py`.
- Two self-caught bugs during the code-check, fixed **before** the run: the
  original draft double-charged costs (quantities already embedded the cost),
  and its spread logic compared a 1-day normalized difference against
  `σ/√252` while using *entry* rather than the *formation base* for the exit —
  neither was Gatev's rule. Both corrected before any result was generated.
- No `swing.db` writes. The three live sleeves were **not modified**.
