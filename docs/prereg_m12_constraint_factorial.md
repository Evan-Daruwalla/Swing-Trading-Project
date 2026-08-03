# Pre-registration — M12: constraint-relaxation factorial (horizon × concentration)

**Written 2026-08-03 (CDT) by Claude, directed by Evan. Attempt #38.**
**COMMITTED DOC-ONLY BEFORE ANY RUNNER CODE EXISTS** — this file's commit hash
predates `scripts/run_m12_factorial.py`.
Plan: `docs/M12_constraint_relaxation_plan.md`. Revert point: tag
`search-phase-closed-v1` (`6e8f431`). Universe frozen: `swing_bot/universe_m12.py`
(142 names, `b2a421a`).

---

## 1. Question

The search phase closed at 37 attempts with a terminal claim that is **explicitly
conditioned on the constraints**: no cost-surviving OOS edge *at K=1–3, holds of
days-to-weeks, retail costs, free EOD data*. The program never tested **which
constraint binds**. M12 tests exactly that, and nothing else.

The project already owns both endpoints, which is what makes this decisive:

| known result | hold | K | outcome |
|---|---|---|---|
| **E3** single-stock momentum (this project) | short | 1–3 | **FAIL** — 6.27% gate CAGR, lost to its own universe's EW buy-hold |
| **momentum_v2** (Trading project, read-only) | monthly | 50 | **VALIDATED** — IS +21.0%/yr, OOS +26.5%/yr, OOS Sharpe 0.87 |

Same factor family, opposite verdicts.

## 2. Hypotheses

- **H_K (concentration binds):** the premium is a cross-sectional spread needing
  breadth (Hou-Xue-Zhang); K=3 cannot express it. Predicts cell ③ ≫ ①.
- **H_H (horizon binds):** the failures are a turnover/cost problem — X9
  quantified ~16%/yr of drag from ~81 round trips. Predicts ② ≫ ①.
- **H_0 (neither binds):** the constraints were never the problem; the terminal
  claim is *stronger* than assumed. Predicts all four cells ≈ equal.

**H_0 is a genuine live possibility and is written here BEFORE running so it
cannot be quietly discarded if the cells come out flat.**

## 3. Design — 2×2 factorial

| | K=3 | K=20 |
|---|---|---|
| **10-session hold** | **① BASELINE** (today's constraint box) | **③ C** |
| **63-session hold** | **② H** | **④ H+C** |

Reported: all four cells, both **main effects** (② − ①, ③ − ①), and the
**interaction** (④ − ② − ③ + ①). Running only ④ could not attribute a result to
either relaxation — the factorial is the entire point.

## 4. Held constant across all four cells (fixed now, no tuning later)

- **Signal: 12-1 cross-sectional momentum** — rank by total return from t−252 to
  t−21 (skipping the most recent 21 sessions, the standard short-term-reversal
  skip). Chosen *because* it is the bridge between E3 and momentum_v2, not a new
  idea.
- **Selection:** top-K by rank, **equal-weight**, long-only.
- **Universe:** `swing_bot/universe_m12.py` — 142 US large-caps, frozen
  2026-08-03, every `data_start` empirical.
- **Execution:** rank at the close of day T, **fill at the open of T+1**. EOD
  only (project hard rule).
- **Rebalance:** every H sessions (10 or 63); full re-selection to the current
  top-K; names leaving the top-K are sold, names entering are bought.
- **Cost:** **5 bps per side** (single-stock tier), applied to every buy and
  sell. **Also reported at 15 bps per side** — the cost hypothesis is half of
  what is being tested, so it must not be flattered by a single optimistic tier.
- **Windows:** **GATE** = 2000-01-01 → 2013-12-31, **SEC** = 2014-01-01 → present.
- **Capital:** CAP0 $1,000, fractional shares, fully invested across K names.
- **Benchmarks reported in every cell:** equal-weight buy-and-hold of the same
  142-name universe (the survivorship-honest benchmark), QQQ buy-and-hold, and
  the e6 rule.

## 5. What is measured

Per cell, per window: net CAGR, max drawdown, annualised Sharpe, number of
rebalances, and turnover. Plus correlation of daily returns to the e6 rule
(the live sleeves' signal), since decorrelation is the standing secondary goal.

## 6. VERDICT DISCIPLINE — this is a DIAGNOSTIC, not a deployment gate

**Declared before any data is pulled, because it is the easiest rule to break
later.** M12 reports a 4-cell table plus main effects and the interaction. It
does **NOT** issue PASS/FAIL, and **no cell becomes a forward-paper sleeve on
the strength of this run.** Selecting the best of four cells and deploying it is
in-sample composition — precisely the M10-1 mistake this program already
documented and capped.

Pre-committed path:
1. M12 runs → reports the cells (diagnostic only).
2. If a relaxation shows a real effect, a **separate prereg** fixes that single
   configuration and gates it on the standard **D1 dual-bar**.
3. Only then does forward paper enter the conversation.

**M12 also cannot rewrite the search-phase terminal claim.** That claim is scoped
to the old constraints; a result here *extends* the map, it does not
retroactively un-falsify anything already killed.

## 7. Interpretation table, fixed in advance

| pattern | reading |
|---|---|
| ② ≫ ①, ③ ≈ ① | **horizon binds** — the failures were a cost/turnover problem |
| ③ ≫ ①, ② ≈ ① | **concentration binds** — confirms the Hou-Xue-Zhang explanation the program has been asserting |
| ④ ≫ ②, ③ | **interaction** — breadth only pays at long horizons; the premium needs both |
| all ≈ equal | **H_0: neither binds** — the terminal claim is stronger than assumed |

## 8. Declared limitations

- **Survivorship.** The 142 names still trade today; the universe is biased in
  the strategy's favour. Under the project's asymmetric-falsification rule
  **only a FAIL is clean**; any apparent success is uninterpretable and routes to
  forward paper. This applies to *every* cell, including a "winning" one.
- **K=20 at $1,000 ≈ $50/position.** Executable with fractional shares, but far
  from the project's original "concentrated, high-percent-return" intent — which
  is the point of relaxing the constraint, and part of why §6 forbids
  auto-deployment.
- **Partial convergence toward the Trading project.** Keeping cells ①/② at K=3
  and staying on this project's own data preserves the separation.
- **No total-return data path** (gap logged in record DO): dividends are not
  reinvested, which understates every cell and the EW benchmark roughly equally,
  but understates high-yield sectors (utilities, staples, REITs) most.
- **One signal only.** M12 tests constraints *given* 12-1 momentum. A different
  signal could bind differently; that is not claimed either way.
- **142 names is not 5,200.** A top-20 of 142 is a 14% sort; momentum_v2's top-50
  of ~5,200 is a 1% sort. So M12 tests the **direction** of the concentration
  effect, not its full magnitude.
