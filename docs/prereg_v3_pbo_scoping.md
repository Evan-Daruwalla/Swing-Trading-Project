# Pre-registration — V3: scope PBO to configuration sets where selection is real

**Status:** DOC-ONLY. Written and committed BEFORE any change to
`swing_bot/validation.py` or `scripts/run_v1_harness_check.py`, and before any
re-run. Nothing in this document has been executed.

**Date written:** 2026-08-13 (record Appendix ET).

**Supersedes nothing.** V1 (`prereg_v1_cost_model_and_validation_harness.md`)
and V2 (`prereg_v2_harness_acceptance_amendment.md`) stand as written; the runs
they governed keep their verdicts. This amends how ONE axis is applied going
forward.

---

## 0. Why this is not a retrofit

V2 §6 pre-registered this exact next step **before** the amended harness was
run, as the pre-committed handling of an outcome V2 §4 predicted in advance:

> "**PBO is only meaningful when the configuration set represents a genuine
> selection choice**, not when configs are independent draws or trivial
> variants. Do **not** respond by loosening `PBO_FAIL_AT`, and do **not** drop
> the falsifier. If this occurs, the recommended next step is a V3 that computes
> PBO only over configuration sets where selection is real — pre-registered
> separately, never patched in after seeing output."

The predicted outcome occurred (planted edge rejected via PBO 0.514). So the
DIRECTION of this amendment was fixed before the number existed. **The specific
classification rule in §2 was not** — it is written by an author who has seen
V2's outputs. That contamination is real, is not cured by V2 §6, and is
disclosed in §7 with a cap on what a V3 pass may claim.

---

## 1. The defect, stated structurally rather than by outcome

`validation.pbo_cscv` (Bailey et al. 2016 CSCV) answers one question: **when I
pick the in-sample-best configuration out of a set, does that choice hold up
out-of-sample?** It splits the series into blocks, takes every half-split, picks
the IS winner, and asks where that winner ranks OOS. PBO is the fraction of
splits where the IS winner lands at or below the OOS median.

That question presupposes that **choosing between the configurations is a
decision with content.** The harness feeds it three sets, and only one of them
satisfies that presupposition:

| subject | how the config set is built | is choosing between them a real decision? |
|---|---|---|
| 6.1 chart-pattern | `cfgs = [(10,0.0),(20,0.0),(20,0.01),(40,0.0),(40,0.02)]` — hold × min-strength swept over the SAME panel (`run_v1_harness_check.py:271-278`) | **YES.** Different hyperparameters, one dataset. This is the thing PBO was designed for. |
| 6.2 pure noise | `[noise_signal(n_min, SEED + i, cost_bps) for i in range(len(cfgs))]` (`:286`) | **NO.** Five i.i.d. draws from one generator. |
| §5 planted edge | `[planted_edge(n_min, SEED + 100 + i) for i in range(len(cfgs))]` (`:300`) | **NO.** Five i.i.d. draws from one generator. |

For an **exchangeable** set — configurations that are independent realisations
of a single process, differing only by random seed — the IS-best is by
construction *the draw with the luckiest in-sample noise*, and out-of-sample it
regresses toward the set's median. PBO then measures the reproducibility of a
luck-based ranking. It is a property of the sampling, not of the strategy: a
process with a large genuine edge and a process with none can both produce a
mid-range PBO, because the common component that constitutes the edge is shared
by every member of the set and therefore cancels out of the *relative* ranking
PBO is built on.

**So `PBO ≥ 0.5 ⇒ overfit`, applied to an exchangeable set, is a category
error.** It is not a weak test of overfitting; it is a test of something else.
The planted-edge false positive is the visible symptom, not the defect.

---

## 2. The rule — fixed now, before any code

**2.1 Every configuration set presented to the harness MUST be declared, at the
call site, as exactly one of:**

- **`SELECTION`** — the members differ by a *parameter or design choice applied
  to the same underlying data*, and a researcher would in practice pick among
  them. PBO is computed and **gated**.
- **`EXCHANGEABLE`** — the members are independent realisations of one process
  (different seeds, resamples, or bootstrap draws). PBO is computed and
  **REPORTED, never gated**.

**2.2 The declaration is made a priori, per subject, in this document, and is
not derived from output.** The declarations are: 6.1 chart-pattern =
`SELECTION`; 6.2 pure noise = `EXCHANGEABLE`; §5 planted edge = `EXCHANGEABLE`.

**2.3 A set with fewer than 2 members remains `pbo = None`** — unchanged from
V1; `pbo_cscv` already returns `{"pbo": None, "reason": "need >= 2
configurations"}`.

**2.4 An `EXCHANGEABLE` subject is rejected on the DSR axis alone.** The OR-rule
from V2 becomes, per subject: `SELECTION` → reject if DSR fires **or** PBO
fires; `EXCHANGEABLE` → reject if DSR fires.

**2.5 NO THRESHOLD MOVES.** `PBO_FAIL_AT = 0.5` and `DSR_ALPHA = 0.05` are
unchanged and are not adjustable after seeing output. V3 changes *where* an
axis applies, never *how hard* it bites. Any V3 implementation that also edits a
threshold is out of compliance with this prereg.

**2.6 The declaration and the PBO value are REPORTED for every subject**,
including the ungated ones, carrying V2 §5's requirement forward: a bare
"rejected"/"accepted" is not acceptable output, and an `EXCHANGEABLE` subject
must print its PBO with the reason it was not gated.

---

## 3. Pre-registered predictions, written before running

Stated now so the re-run cannot be read as confirmation of whatever happens.

- **6.2 pure noise:** still **REJECTED**, via DSR (V2 measured 0.0001). High
  confidence. Its PBO (V2: 0.900) becomes reported-not-gated and the verdict
  must not change.
- **6.1 chart-pattern:** still **REJECTED**. Its set is `SELECTION`, so both
  axes remain live and DSR alone already fired in V2 (0.0168). High confidence.
- **§5 planted edge:** expected to become **NOT REJECTED** — the outcome the
  falsifier wants — because the axis that rejected it (PBO 0.514) no longer
  gates an `EXCHANGEABLE` set. **Moderate confidence only.** If DSR also fires
  on the planted edge, it stays rejected and V3 does not fix the falsifier; see
  §5.
- **Criteria 3/4/5 of V1:** unchanged and still passing. High confidence.

---

## 4. Acceptance criteria for V3 — fixed now

V3 is **ACCEPTED** only if all hold:

1. **Pure noise is still rejected.** (Non-negotiable — see §5.)
2. **Chart-pattern rule is still rejected.**
3. **V1 criteria 3, 4, 5 still pass unchanged.**
4. **Every subject reports its declared class, its DSR value, its PBO value, and
   which axis fired.**
5. **No threshold in the harness differs from its V1/V2 value.** Verified by
   diff, not by assertion.

---

## 5. The trap this creates, named in advance

**Scoping an axis away is indistinguishable, in outcome, from loosening it —
unless the thing it was catching is still caught by something else.** The entire
risk of V3 is that "PBO only applies to selection sets" is a disguised
weakening that lets a bad subject through.

**Pre-committed handling, binding:**

- **If pure noise is ACCEPTED under V3, V3 FAILS.** The change is reverted in
  full, the failure is recorded, and the honest conclusion is that the PBO axis
  was load-bearing for noise rejection and the harness needs a different
  selection-level test — not that the noise control should be re-specified.
  **No tuning a FAIL.**
- **If the planted edge is still rejected under V3** (DSR fires on it), V3 has
  *not* repaired the falsifier. That is reported as a V3 partial result, and the
  next step is a V4 examining the DSR axis — **not** a further loosening here.
- **The planted-edge falsifier is not dropped and its threshold is not moved.**

---

## 6. Hard constraints (inherited, restated so they cannot drift)

- Prereg before results. This document is committed before the runner changes.
- No tuning a FAIL.
- EOD only; paper only; `swing.db` and Trading's repo read-only.
- Prices split-adjusted, dividend-UNADJUSTED (`auto_adjust=False`).
- `.e8e9_cache` must be at ONE vintage for the run, and the vintage is recorded
  in the results doc. As of 2026-08-13 it is uniform at 2026-08-12 (record ER).
- The frozen tripwire must be GREEN before and after any harness change.

---

## 7. Disclosed limitations

1. **HINDSIGHT CONTAMINATION OF THE RULE, NOT THE DIRECTION.** V2 §6 fixed the
   direction in advance (§0), but §2's classification rule was authored with
   V2's four numbers already known (noise DSR 0.0001 / PBO 0.900; pattern DSR
   0.0168; planted PBO 0.514). **Therefore: a V3 pass may NOT be reported as
   evidence that the harness is well-specified.** The most it can support is
   "the harness no longer rejects a known edge via an axis that did not apply to
   it." Any stronger claim requires a subject this author has not seen scored.
2. **The exchangeable/selection distinction is a judgement about construction,
   not a measured quantity.** It is declared per call site by a human and can be
   declared wrongly. It is deliberately placed at the call site, in the open,
   rather than inferred — an inferred version would be a guard nobody can audit.
3. **N=5 configurations is small for CSCV** in every subject. V3 does not change
   this; it is inherited from V1 and remains a limitation of all PBO values this
   harness produces, gated or not.
4. **This repairs a falsifier; it produces no evidence about any strategy.** No
   sleeve, no attempt, and no entry in `docs/trial_log.json` follows from V3.
   The attempt tally does not move.
5. **The planted edge remains a synthetic control.** Passing it says the harness
   does not reject a large, clean, artificial edge. It says nothing about
   sensitivity to a small, noisy, real one.
