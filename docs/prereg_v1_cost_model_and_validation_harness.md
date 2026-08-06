# Pre-registration — V1: measured cost model + CPCV/DSR validation harness

**Written 2026-08-06 (CDT) by Claude, directed by Evan.**
**COMMITTED DOC-ONLY BEFORE ANY HARNESS CODE EXISTS** — this file's commit hash
must predate `swing_bot/costs.py` and `swing_bot/validation.py`.

This is **not an attempt**. It builds no strategy and claims no edge, so it does
**not** increment the attempt tally (38). It is infrastructure whose entire
purpose is to make *future* claims falsifiable.

Inputs that shaped it: the cold literature brief
`docs/research/2026-08-06_ta-swing-trading-ai-agent.md` (F4, F8) and its
reconciliation against the record (annotation dated 2026-08-06), plus
`docs/trial_log.json` / `docs/trial_log_notes.md`.

---

## 1. What is being built, and the one thing it must do

Two components:

- **A cost model** that reports round-trip friction as a **measured** quantity.
- **A validation harness**: purged K-fold with embargo, combinatorial purged
  cross-validation (CPCV), deflated Sharpe ratio (DSR), and probability of
  backtest overfitting (PBO).

**The success condition is that the harness REJECTS things.** A validation layer
that passes noise is not a weak tool, it is a *harmful* one — it manufactures
false confidence in exactly the situation it was built to prevent. Section 6
therefore pre-registers rejection of a worthless signal as the acceptance test,
before any of it is written.

## 2. Cost model

### 2.1 Measured, never assumed

Round-trip friction `r` (basis points) = entry-side + exit-side, each measured as
the signed gap between the price the simulation assumed and the price actually
obtained.

**Primary data source: `fill_divergence` in `swing.db`** — built 2026-07-28
(audit finding #2), already populated by the live M3 paper loop. Per fill it
holds `sim_price`, `alpaca_price`, `alpaca_qty`, `alpaca_status`. Friction per
fill is `(alpaca_price − sim_price) / sim_price × 10,000`, signed so that a cost
is positive on a buy and negative on a sell.

**DATA CONVENTION (mandatory header on anything touching prices):** all prices
here are **split-adjusted, dividend-UNADJUSTED** (`auto_adjust=False`), matching
`swing_bot/prices.py` and every other consumer. `fill_divergence.sim_price` is a
next-open fill from that same convention.

### 2.2 What it does when measurement is unavailable — FAIL LOUD

This is the part that must not be softened later:

- If **fewer than `MIN_FILLS_FOR_ESTIMATE` fills** exist for the requested
  instrument class, `estimate_friction()` **raises**. It does not fall back to a
  constant, does not interpolate, and does not return a default with a warning.
- A caller that wants to proceed anyway must pass an **explicit**
  `assumed_bps=<n>` — and every downstream artifact then carries
  `friction_source="ASSUMED"` so no report can present an assumption as a
  measurement.
- **`MIN_FILLS_FOR_ESTIMATE = 20` per instrument class**, pre-registered now.

### 2.3 Stated up front: the model CANNOT be calibrated today

`fill_divergence` currently holds **4** resolved fills: **+0.0, +0.0, +1.3,
−85.7 bps**. Three are the same ticker (QQQ), same side; the −85.7 bps outlier is
a documented discipline break (an intraday fire, record DE), **not spread**.

**n=4 cannot estimate a friction distribution.** Under §2.2 the model will
therefore **raise** on today's data — and that is the correct, pre-registered
behaviour, not a bug to be worked around. This prereg builds the *instrument*;
calibration waits for the live loop to accumulate fills. **Any future number
presented as "measured friction" must cite the fill count behind it.**

## 3. Validation harness

### 3.1 Purged K-fold with embargo

Financial series overlap: a label built from a forward window leaks into folds
that touch that window. Standard K-fold therefore reports skill that does not
exist.

- **Purge**: drop training observations whose label window overlaps any test
  observation's label window.
- **Embargo**: additionally drop training observations within
  `EMBARGO_PCT = 1%` of total sample length *after* each test block.
- `K_FOLDS = 6`.

### 3.2 Combinatorial purged cross-validation (CPCV)

Single train/test splits yield one path and therefore one Sharpe — no
distribution, no way to see variance across paths.

- `N_GROUPS = 6`, `N_TEST_GROUPS = 2` → **15 combinations**, each purged and
  embargoed as in §3.1. Output: a **distribution** of out-of-sample Sharpe.
- Reporting the distribution is mandatory. Bessembinder (brief F4) is the reason:
  with concentrated books the **median and mean diverge sharply**, so a mean-only
  report measures luck.

### 3.3 Deflated Sharpe ratio (DSR)

DSR adjusts an observed Sharpe for (a) the number of trials, (b) skew and
kurtosis of returns, (c) sample length.

- **The trial count is a HARD INPUT read from `docs/trial_log.json`.** The
  harness **raises** if the file is missing, unreadable, or older than the newest
  `docs/prereg_*.md` — a stale log under-counts trials in exactly the direction
  that flatters the result.
- **Trial count used = `max(max_attempt_number_in_record, declared_variant_total)`**,
  i.e. the **larger** figure, per `trial_log_notes.md`. The 37-vs-38 discrepancy
  is unresolved; the rule is to err toward *more* trials, never fewer.
- The harness must print the trial count and its source **in the same output
  block as the DSR value**, so a DSR can never be quoted without its N.

### 3.4 Probability of backtest overfitting (PBO)

Via CSCV over the CPCV paths: the fraction of splits in which the
in-sample-best configuration underperforms the **median** out-of-sample.
**PBO > 0.5 means the selection procedure is worse than random.**

## 4. Acceptance criteria — fixed now, before any code

The harness is **ACCEPTED** only if **all five** hold:

1. **Rejects a pure-noise control** (§6.2): DSR **not significant** at
   `DSR_ALPHA = 0.05` **and** `PBO ≥ 0.5`.
2. **Rejects a classical chart-pattern rule** (§6.1) on the same two criteria.
3. **Purging demonstrably bites**: mean CPCV Sharpe of the noise control is
   **lower** with purge+embargo enabled than with them disabled. If purging
   changes nothing, it is not wired in.
4. **Fails loud on missing cost data**: `estimate_friction()` raises on the
   current 4-fill `fill_divergence` (§2.3).
5. **Fails loud on a stale/absent trial log**: DSR raises when
   `docs/trial_log.json` is removed or predates the newest prereg.

**If the harness PASSES either §6 subject, that is the finding.** The harness is
reported broken, the result is recorded, and no strategy work proceeds on top of
it. **No tuning a FAIL** — thresholds in this section are not adjustable after
seeing output.

## 5. Falsification test — what would prove the harness worthless

A harness that rejects everything is as useless as one that accepts everything.
So, **as a REPORTED-not-gated diagnostic** (precedent: M11's short-side check,
X9's zero-cost run):

- Feed it a **synthetic signal with a known, planted edge** — a series
  constructed so future returns are genuinely predictable from the feature.
- **Expectation: the harness does NOT reject it.** If it rejects a planted edge
  too, its rejections carry no information and criteria 1–2 are satisfied
  trivially.
- This is **diagnostic, not gating**: a surprise here is reported, not silently
  fixed by loosening §4.

## 6. Test subjects

### 6.1 Classical chart-pattern rule — evidence-ranked LAST

The brief ranks classical pattern recognition **#6 of 6**, and this repo already
tested it: **M11 (2026-07-14) FAILED, signal-dead** (gate −0.14% CAGR / Sh 0.09).
It is the right subject precisely *because* both the literature and this project's
own experiment agree it has no edge.

**Reuse `scripts/run_m11_chart_patterns.py`'s existing causal pivot detector and
double-bottom / inverse-H&S logic.** Do not rebuild it.

### 6.2 Pure-noise control

A signal drawn from a seeded PRNG, independent of price by construction. Seed
pinned in the harness so the run is reproducible.

## 7. Hard constraints (inherited, restated so they cannot drift)

- **EOD only**: signal at close, execute next open. No intraday logic.
- **Trading's `price_cache` is READ-ONLY** from this project.
- **Split-adjusted / dividend-UNADJUSTED** stated in a header comment on every
  file touching prices.
- **Liquidity floor mandatory** in any universe filter.
- Frozen tripwire must hold at **d = ±0.0000pp**.
- No `swing.db` writes from the harness; open the ledger **read-only**.

## 8. Declared limitations

- **The cost model ships uncalibrated** (§2.3). It is an instrument, not a number.
- **The trial count is a lower bound** — it omits the ~90-method survey, the
  dropped-16 list, and pre-prereg parameter exploration, so DSR will be
  *optimistic*. Direction of error stated so it cannot be forgotten.
- **DSR assumes returns are IID-ish** after adjusting for skew/kurtosis; serial
  correlation in overlapping-label strategies violates that. Purging reduces but
  does not eliminate it.
- **This harness cannot fix survivorship.** Every universe here is survivor-biased;
  the standing rule still holds — **only a FAIL is clean**.
