# M12 — Constraint-Relaxation Factorial: experiment plan

**Swing Trading · planned 2026-08-03 (CDT) · Evan's direction**
**Status: PLAN ONLY — nothing has been run. No prereg is committed yet.**
Revert point for the whole phase: git tag **`search-phase-closed-v1`** (`6e8f431`).

---

## 1. Why this exists

The search phase closed at 37 attempts (record DQ) with a terminal claim:
*no robust, cost-surviving, out-of-sample EOD edge exists in the documented
swing-strategy space **at retail scale, K=1–3 concentration, days-to-weeks
holds, and a mandatory liquidity floor**.*

That claim is **conditioned on the constraints**, and the program has never
tested which constraint actually binds. Two are candidates:

- **CONCENTRATION.** The program's own explanation (Hou-Xue-Zhang) is that a
  factor premium is a decile spread across *many* names; K=1–3 cannot express it.
- **HORIZON.** Cost drag is the program's most repeated killer — X9 quantified
  it at ~16%/yr from ~81 round trips. Fewer, longer holds pay less toll.

The project already owns **both endpoints of the answer**, which is what makes
this cheap and decisive:

| known result | horizon | K | outcome |
|---|---|---|---|
| **E3** single-stock momentum (this project) | short | 1–3 | **FAIL** (6.27% gate CAGR, lost to its own universe's equal-weight buy-hold) |
| **momentum_v2** (Trading project, read-only) | monthly | 50 | **VALIDATED** — IS +21.0%/yr, OOS +26.5%/yr, OOS Sharpe 0.87 |

Same factor family, opposite verdicts. **Something between those two points is
doing the work, and nobody has isolated which.** A 2×2 answers it directly.

## 2. Design — a controlled 2×2 factorial

**Factors** (only these vary; everything else is held constant):

| factor | LOW (current constraint) | HIGH (relaxed) |
|---|---|---|
| **Horizon** `H` | hold/rebalance **10 sessions** (~2 weeks — inside the old swing scope) | hold/rebalance **63 sessions** (~3 months — mid-range of the 1–6 month relaxation) |
| **Concentration** `K` | **K = 3** | **K = 20** |

**Cells:**

| | K=3 | K=20 |
|---|---|---|
| **10-session hold** | **① BASELINE** — reproduces today's constraint box | **③ C** — concentration relaxed |
| **63-session hold** | **② H** — horizon relaxed | **④ H+C** — both |

Reporting the **two main effects** (H alone, C alone) and the **interaction**
(does breadth only pay off at long horizons?) is the entire point. Running only
④ would have told us nothing about *which* relaxation mattered — that was the
objection to "both at once," and the factorial removes it.

## 3. Held constant across all four cells

Deliberately identical so the only difference is the constraint:

- **Signal: 12-1 cross-sectional momentum** (rank by return from t−252 to t−21,
  skipping the last month). Chosen *because* both endpoints above used this
  family — it is the bridge between E3 and momentum_v2, not a new idea.
- **Selection:** top-K by momentum rank, equal-weight.
- **Execution:** signal at close, **fill next open** (project hard rule).
- **Cost:** 5 bps/side (single-stock tier). Also reported at **15 bps stress**,
  since the cost hypothesis is half of what is being tested and must not be
  flattered.
- **Windows:** GATE → 2013-12-31, SEC 2014-01-01 → present (project standard).
- **Capital:** CAP0 $1,000, fractional shares.
- **Benchmarks:** equal-weight buy-and-hold of the same universe, plus QQQ
  buy-and-hold and the e6 rule, in every cell.

## 4. OPEN DESIGN DECISION — the universe (needs Evan's pick)

K=20 is only meaningful if the universe is big enough for "top 20" to be a real
sort. Three options, each with a real cost:

| option | breadth | pros | cons |
|---|---|---|---|
| **(a) existing 39-name survivor universe** | 39 | self-contained; full OHLC via `cache_fetch`; already used by C1/M10-1/M11 | **top-20 of 39 is half the universe — a weak sort.** Tests *direction* (does breadth help?) not *magnitude* |
| **(b) expand to ~100 large-caps** (recommended) | ~100 | top-20 of 100 is a genuine sort; still self-contained, full OHLC, free | requires a **new frozen universe decision** (dated, per M0.3 rules); adds survivorship the same way the 39 does |
| **(c) Trading's `price_cache`, READ-ONLY** | 12,486 tickers | true breadth; matches momentum_v2's design | **verified problems:** `next_open` has only 1.1M rows vs 15.7M `close` (many ticker-days cannot be filled next-open); only **3 delistings** recorded, so it is still survivor-biased; median ticker has 636 rows; and it **couples two projects CLAUDE.md keeps separate**, with a concurrent-DB-access rule to respect |

**Recommendation: (b).** It buys a real sort without coupling the projects or
inheriting (c)'s fill-coverage gap. The new universe would be frozen with a
dated decision and the same survivorship disclosure the 39-name set carries.

## 5. Verdict discipline — this is a DIAGNOSTIC, not a deployment gate

**Stated before any data is pulled, because it is the easiest rule to break
later:** M12 is a *constraint diagnostic*. Its output is "which constraint
binds," reported as the 4-cell table plus main effects and interaction.

**A winning cell does NOT become a sleeve on the strength of this run.** Picking
the best of four cells and deploying it is in-sample composition — exactly the
M10-1 mistake the program already documented and capped. The pre-committed path:

1. M12 runs and reports the 4 cells (diagnostic; no PASS/FAIL claimed).
2. If a relaxation shows a real effect, **a separate prereg** fixes that
   configuration and gates it on the standard D1 dual-bar.
3. Only then does forward paper enter the conversation.

Also pre-committed: **M12 cannot change the search-phase terminal claim.** That
claim is explicitly scoped to the old constraints; a result here *extends* the
map, it does not retroactively rewrite what was already falsified.

## 6. What each outcome would mean

| pattern | reading |
|---|---|
| ② H ≫ ① and ③ C ≈ ① | **horizon binds** — the program's failures were a *cost/turnover* problem |
| ③ C ≫ ① and ② H ≈ ① | **concentration binds** — confirms the Hou-Xue-Zhang explanation the program has been asserting |
| ④ ≫ ②,③ (interaction) | breadth only pays at long horizons — the premium needs *both* |
| all four ≈ each other | **neither constraint was the binding problem** — the honest and most uncomfortable outcome, and it would mean the terminal claim is stronger than assumed, not weaker |

The fourth row is a real possibility and is written down *now* so it cannot be
quietly discarded later.

## 7. Declared limitations

- **Survivorship** under every universe option; only a FAIL is clean, a PASS
  routes to forward paper (standing project rule).
- **K=20 at $1,000** = ~$50/position. Fractional shares make it executable, but
  it sits far from the project's original "concentrated, high-percent-return"
  intent — which is the point of relaxing the constraint, and is why §5 forbids
  auto-deployment.
- **This converges partly toward the Trading project.** Keeping K=3 in cells ①/②
  and staying on this project's own data preserves the separation; option (c)
  would erode it.
- **No total-return data path** (gap logged in record DO) — dividend-heavy names
  remain mismeasured.

## 8. Execution order (once the universe is picked)

1. Freeze the universe decision (dated) if option (b).
2. **Commit the M12 prereg doc-only** — criteria, cells, and §5's
   diagnostic-not-deployment rule fixed before any runner exists.
3. Write `scripts/run_m12_factorial.py`; run all four cells + benchmarks + the
   15 bps stress leg.
4. Results doc + record entry; frozen tripwire must stay GREEN.
5. Separate prereg for anything that warrants deployment.
