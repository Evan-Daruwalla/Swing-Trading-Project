# Pre-registration — E1: ETF IBS mean reversion

**Committed 2026-07-09 (PRD task M1.7), BEFORE any backtest-engine code
exists. This is the project's core rigor artifact: git history proves this
doc predates `swing_bot/backtest.py`. Every parameter below is FIXED. No
parameter may change after this commit — a changed rule requires a NEW dated
pre-registration doc that references this one and explains why. Results seen
in M2 must NOT feed back into these rules.**

Grounding: research brief `docs/research/2026-07-08_small-account-swing-
strategies.md`; power calc `docs/research/2026-07-09_E1_power.md` (E1 is
powerable — 19.6% signal rate, thousands of backtest trades). Parameters are
LITERATURE/CONVENTION-set (Pagonidis IBS thresholds, Connors-style time
stop), NOT fitted to our data — so full-sample evaluation is valid.

---

## 1. Universe (fixed)

The frozen 29-ETF universe in `swing_bot/universe.py` (4 broad US + 11 SPDR
sectors + 14 country/regional), FROZEN 2026-07-08. A ticker is eligible on a
date only if listed as of that date (`data_start <= date`) and its bar passes
the M0.4 quality gate (skip `high == low` zero-range bars — IBS undefined).

## 2. Signal (fixed)

At the CLOSE of day T, for each eligible ticker:
- IBS = (close − low) / (high − low).
- **Entry candidate iff IBS < 0.20.** (Skip if high == low.)

Long-only. No shorting.

## 3. Exit (fixed)

A held position exits on the FIRST of:
- **Mean-reversion exit:** the first day whose close has **IBS > 0.80**, OR
- **Time stop:** **5 trading days** after entry (hold ≤ 5 sessions).

**No hard stop-loss in E1.** (Literature indicates fixed stops structurally
hurt mean reversion; a stop-loss ablation is a SEPARATE later experiment,
PRD M5 #18 — not part of E1.)

## 4. Sizing & concurrency (fixed)

- Capital parameter: **$500 nominal** (parameterized; sizing scales linearly).
- **Max 5 concurrent positions (K=5).** Target size per position =
  capital / 5 (20% each); unused slots sit in cash.
- **Selection when signals > free slots:** take the LOWEST-IBS (most
  oversold) candidates first; ties broken alphabetically by ticker
  (deterministic).
- Fractional shares assumed in backtest. (Whole-share fallback and DAY-TIF
  order constraints are LIVE concerns handled in M3, not modeled in the
  backtest.)
- One position per ticker at a time (no pyramiding).

## 5. Execution / fill models (BOTH reported; primary = next-open)

- **Model A — next-open (PRIMARY, executable):** enter at the OPEN of day
  T+1; exit at the OPEN of the day after the exit signal fires. This is what
  the bot can actually do (signal at close, execute next open). Kill criteria
  in §7 are judged on Model A.
- **Model B — close-to-close (reference/idealized):** enter at the CLOSE of
  day T; exit at the CLOSE of the exit-signal day. This is the published
  measurement basis (Pagonidis). Reported to quantify the overnight/
  execution haircut (Model B − Model A). NOT a kill-criteria basis.

## 6. Cost model (fixed)

- **PRIMARY: 5 bps per side (10 bps round-trip)** — realistic for the liquid
  US members; applied to every entry and exit fill.
- Reported as sensitivity (not gates): **0 bps** and **10 bps/side (20 bps
  round-trip)** — the latter a conservative proxy for wider country-ETF
  spreads.
- No borrow cost (long-only). No commission (Alpaca commission-free).

## 7. Kill criteria — the definition of "E1 SURVIVES" (fixed)

Evaluated on the FULL window in `swing.db` (2014-01-02 .. 2026-07-08), on
**Model A (next-open) net of the primary 10 bps round-trip cost**. E1 PASSES
only if ALL hold:

1. **N:** ≥ 200 closed trades in the backtest (power floor).
2. **Expectancy:** net mean return per trade > 0 (strictly positive after
   cost).
3. **Risk-adjusted:** net annualized Sharpe ratio ≥ 0.50.
4. **Drawdown:** max drawdown ≤ 25%.

If ANY criterion fails → **E1 FAILS.** A failure is a valid, publishable
result: STOP, record it honestly, do NOT tune parameters to rescue it
(that needs a new pre-registration + Evan's sign-off).

**Reported alongside (context, NOT gates):** Model B results and the A−B
haircut; 0/20 bps sensitivity; per-group breakdown (broad_us / spdr_sector /
country_intl — the country group has a distinct stale-NAV/overnight
mechanism, record Appendix G, so it is reported separately); split-sample
stability (2014-01-02..2021-12-31 vs 2022-01-01..2026-07-08).

## 8. Live-trading gate (M2 → M3)

Live paper (M3) begins ONLY on: E1 backtest PASS (all of §7) **AND** Evan's
explicit go **AND** an allocated Alpaca paper account. All three are required;
this is the BLOCKED-ON-EVAN gate (PRD M2.13 / M3.15).

## 9. Overlay experiment pre-registration (E1-veto)

The LLM overlay is KEPT and LIVE-ACTING from M3 day one (Evan 2026-07-08) as
a controlled experiment, pre-registered here:

- **Arms:** `e1_control` (mechanical E1, always takes the pick) vs
  `e1_llm_veto` (treatment: LLM VETO → sit that entry out in cash; otherwise
  identical). **Cascade arm deferred** to the readout.
- **Overlay decision rule:** for each entry candidate, the LLM returns
  BUY/VETO with an invalidation price + rationale, logged UNIQUE(date,ticker)
  to `overlay_log`. VETO diverges ONLY the treatment sleeve; the control
  sleeve is provably unaffected (runtime assertion, PRD M3.14).
- **Readout point (fixed):** the FIRST of **100 logged overlay decisions**
  OR **6 months of live paper**. No conclusions before this point; interim
  numbers are descriptive-only.
- **Overlay kill criteria (at readout):** DROP the overlay if EITHER —
  (a) vetoed candidates' realized (paper) outcomes are NOT worse on average
  than taken candidates (veto adds no predictive value), OR
  (b) `e1_llm_veto` NAV ≤ `e1_control` NAV.
  Trading's kill-switch discipline: an overlay that doesn't beat the
  mechanical control by its own readout is dropped, not nursed.

## 10. No-change clause

The parameters in §§1–9 are frozen as of this commit. The executing model
implements exactly these in M2. If implementation reveals an ambiguity, it is
resolved in the MOST LITERAL reading and noted in the record — never by
choosing the variant that improves results. Any substantive change is a new
dated pre-registration doc.
