# Pre-registration — F2: align E5 and E7 to the 200-DMA convention of the rule they test

**Status:** DOC-ONLY. Written and committed BEFORE any change to
`scripts/run_e5_regime.py` or `scripts/run_e7_international.py`, and before any
re-run. Nothing here has been executed.

**Date written:** 2026-08-19 (record Appendix FD).

**Authorised by Evan 2026-08-19**, choosing "align E5/E7 to E6 and re-run" over
document-only and over making the whole repo uniform.

---

## 1. The defect, stated structurally

E6 is the strategy: **hold QQQ while its close is above its own 200-day moving
average, else cash; switch at next open.** E5 (regime test on 2000-2013) and E7
(international validation on five non-US markets) exist to test *that rule* out
of sample.

They do not implement it. The moving average is computed differently:

| site | slice | includes today's close? |
|---|---|---|
| `swing_bot/paper_sleeves.py` `sma()` + `decide_e6_1x()` — **LIVE** | `series[-200:]` | **YES** |
| `scripts/run_e6_deleveraged.py` `rotation_nav()` | `closes[i - ma + 1:i + 1]` | **YES** |
| `scripts/run_e5_regime.py` `rotation_nav()` | `closes[i - ma:i]` | **NO** |
| `scripts/run_e7_international.py` `rotation()` | `closes[i-MA:i]` | **NO** |

The signal in all four is `closes[i] > m`. Under the exclusive form today's close
is compared against a mean that excludes it; under the inclusive form, against a
mean that contains it. These are different rules, and they disagree on real data
— the 2026-08-06 alignment of E6 itself moved its numbers (maxDD 52.2% to 54.3%,
Sharpe 0.24 to 0.22 on 2000-2013).

**So E5 and E7 currently report the out-of-sample behaviour of a rule the project
does not run.** That is the defect. It is not a bug in either script — each is
internally consistent — it is a mismatch between a test and its subject.

## 2. The change — fixed now, before any code

**2.1** In `scripts/run_e5_regime.py` `rotation_nav()`, replace
`m = sum(closes[i - ma:i]) / ma` with `m = sum(closes[i - ma + 1:i + 1]) / ma`.

**2.2** In `scripts/run_e7_international.py` `rotation()`, replace
`m = sum(closes[i-MA:i])/MA` with `m = sum(closes[i-MA+1:i+1])/MA`.

**2.3** The boundary guard (`if i >= ma` / `if i >= MA`) is COPIED FROM E6
UNCHANGED. E6 uses `if i >= ma`, which is one bar more conservative than the
inclusive slice strictly needs; matching it exactly is the point of an
alignment, so no guard is retuned.

**2.4 NOTHING ELSE CHANGES.** Not the cost model, not the windows, not the
universes, not the execution lag, not `MA`/`ma` itself, not the verdict bars.

**2.5 `swing_bot/rotation.py` IS NOT TOUCHED.** It is the E4 engine and is PINNED
by the frozen tripwire's 12 reference numbers; changing it turns the tripwire RED
and moves E4's recorded results. E4 keeps the exclusive convention and that
divergence is documented, not silently inherited. **The frozen tripwire must be
GREEN before and after this change** — if it goes RED, the change escaped its
intended scope and is reverted.

**2.6** The remaining exclusive sites (`pt_volgate.py`, `screens_20260709.py`)
are NOT touched: both are explicitly in-sample, hypothesis-generating, and
carry no verdict.

## 3. Pre-registered predictions, written before running

- **Direction unknown, magnitude small.** E6's own alignment moved Sharpe by
  0.02 and maxDD by 2.1pp. I predict E5's and E7's headline metrics move by a
  similar order (single-digit percentage points of drawdown, <=0.10 of Sharpe)
  and that the sign is not predictable a priori.
- **E5 verdict: still FAIL.** Its recorded failure is a 92.7% drawdown on the
  3x rotation in 2000-2013 against a 60% ceiling. A convention change of this
  size cannot close a 32.7pp gap. **High confidence.**
- **E7 verdict: still FAIL, both arms.** Arm 1's recorded finding is that E6's
  overlay generalises to 3 of 5 markets; Arm 2's is mean CAGR 4.55% with 83-97%
  drawdowns. **High confidence for Arm 2. MODERATE for Arm 1**, because "3 of 5"
  is a count of per-market pass/fail and a single market sitting near its
  threshold could flip the count without any headline number moving much.
- **The frozen tripwire stays GREEN.** High confidence — neither file is
  imported by it.

## 4. What this is, and what it is NOT

**This is a RESTATEMENT of two already-recorded attempts, not a new attempt.**
E5 and E7 keep their attempt numbers; `docs/trial_log.json`'s trial count does
not move; no new prereg-per-attempt is created. The corrected numbers SUPERSEDE
the old ones in the record by dated entry, and the old ones are not deleted.

## 5. The trap this creates, named in advance

**A re-run under a changed convention is not an out-of-sample test, and a
verdict that improves must not be banked as if it were.** E5 and E7 were
selected, designed and run under the old convention against data already seen.
Re-running them on the same data under a new convention is a RESTATEMENT.

**Pre-committed handling, binding:**

- **If a verdict FLIPS from FAIL to PASS on either arm, it is reported as
  `PROVISIONAL — CONVENTION-FLIP` and is NOT recorded as a program PASS.** The
  program's PASS-HR count stays 0 until such a result is re-tested under a fresh
  pre-registration on data not used to select it. **No exceptions**: a flip is
  the single most suspicious outcome available here, because the change was made
  by someone who knew the old verdicts.
- **If a verdict stays FAIL, that is the expected outcome and buys nothing** —
  it does not strengthen the original finding, it merely removes an
  inconsistency between a test and its subject.
- **Both the OLD and NEW numbers are reported side by side**, with the delta.
  Reporting only the new ones would erase the evidence that anything changed.
- **NO TUNING.** If the aligned run produces something unattractive, the fix is
  not adjusted. The one-line change in section 2 is the entire intervention.

## 6. Hard constraints (inherited, restated so they cannot drift)

- Prereg before results; this document is committed before the code changes.
- EOD only; paper only; `swing.db` and Trading's repo read-only.
- Prices split-adjusted, dividend-UNADJUSTED (`auto_adjust=False`).
- `.e8e9_cache` at ONE vintage for the run; the vintage is recorded with the
  results. As of 2026-08-19 it is uniform at 2026-08-17 (record EZ).
- Frozen tripwire GREEN before and after (section 2.5).

## 7. Disclosed limitations

1. **The author knew the old verdicts.** The direction of section 2 is forced by
   the structural argument in section 1 — a test must implement its subject —
   and not by any number, but the section 3 predictions were written by someone
   who has read the recorded results. Section 5's flip-handling exists precisely
   because that contamination cannot be undone.
2. **This does not make the repo uniform.** Four exclusive sites remain
   (`swing_bot/rotation.py`, `pt_volgate.py`, `screens_20260709.py`, and E4's
   consumers). The split is narrowed from "tests disagree with their subject" to
   "a pinned legacy engine and two in-sample screens use the other form", which
   is a defensible boundary but is still a split.
3. **Neither convention is claimed to be correct in general.** The inclusive
   form is chosen ONLY because it is what the live sleeve runs. If the live rule
   ever changes, this alignment must follow it.
4. **No new evidence about any strategy is produced.** E5 and E7 were and remain
   falsification tests; the best outcome here is that they test the right thing.
