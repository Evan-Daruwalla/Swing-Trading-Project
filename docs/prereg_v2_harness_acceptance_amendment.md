# Pre-registration — V2: amended harness acceptance criterion

**Written 2026-08-06 (CDT) by Claude, directed by Evan.**
**COMMITTED DOC-ONLY BEFORE THE ACCEPTANCE LOGIC IS CHANGED** — this file's hash
must predate the edit to `scripts/run_v1_harness_check.py`.

**Not an attempt. Builds no strategy, claims no edge, does not increment the
tally (38).**

**This SUPERSEDES section 4 of `prereg_v1_cost_model_and_validation_harness.md`
(commit `ec51b91`) — it does NOT edit it.** V1 failed its own criterion 2 and
that failure stands on the record (Appendix EB, commit `3b346cb`). Amending a
criterion by rewriting the document it lives in would erase the evidence that it
was ever wrong, which is the whole reason this project pre-registers anything.

---

## 1. What was wrong with V1's criterion, stated before any re-run

V1 §4 defined rejection as:

> DSR **not significant** at α=0.05 **AND** PBO ≥ 0.5

That conjunction is **mis-specified**, and the V1 run demonstrated it:

| subject | DSR | PBO | V1 verdict |
|---|---|---|---|
| pure noise | 0.0001 | 0.900 | rejected |
| chart-pattern rule | 0.0168 | 0.429 | **not rejected** |
| planted edge | 1.0000 | 0.514 | not rejected |

**The two statistics answer different questions:**

- **DSR** — *does this strategy's Sharpe survive the number of trials searched?*
  A **strategy-level** test.
- **PBO** — *is the selection of the best CONFIGURATION overfit?* A
  **selection-level** test, computed across a configuration set.

Requiring both to fire demands that one strategy fail two unrelated tests. A
no-edge strategy whose variants are highly **correlated** (the chart-pattern
rule: same detector, only hold period and entry threshold vary) has almost no
selection to overfit, so its PBO sits near random — while its DSR correctly
says "no edge." The planted-edge control settles the interpretation: **PBO 0.514
alongside a genuine edge. PBO does not measure edge.**

## 2. Amended criterion (this is the change)

A subject is **REJECTED if EITHER fires**:

- **(a) strategy-level:** DSR **not significant** at `DSR_ALPHA = 0.05`, **or**
- **(b) selection-level:** `PBO ≥ 0.5`.

Rationale for OR: the two are independent failure modes and either one is
disqualifying. A strategy whose Sharpe does not survive its trial count is dead
regardless of how its configs were picked; a strategy whose config selection is
worse than random is dead regardless of the headline Sharpe.

**Both statistics are still REPORTED SEPARATELY in every run.** Collapsing them
to one verdict flag must not hide which axis fired — the V1 run is the proof
that the distinction carries information.

## 3. What must NOT change (guarding against a convenient amendment)

This amendment is only defensible if it does not quietly loosen everything else.
Explicitly unchanged from V1 §4:

- `DSR_ALPHA = 0.05` — **not** relaxed.
- `PBO_FAIL_AT = 0.5` — **not** relaxed.
- Criterion 3 (purging must demonstrably bite), 4 (cost model fails loud), and
  5 (DSR refuses a missing/stale trial log) stand **verbatim**.
- The trial count still comes from `docs/trial_log.json` as a hard input, still
  uses the **larger** of the two figures, and still raises when stale.
- The §5 planted-edge falsifier stands, and its expected outcome is unchanged:
  **it must NOT be rejected**. Under the new OR-rule this is a *stricter* test of
  the harness than it was under AND — the planted edge must now clear **both**
  axes, and its V1 PBO of 0.514 means **it is expected to FAIL the new rule.**

## 4. Pre-registered prediction, written before re-running

Stated now so the re-run cannot be read as confirmation of whatever happens:

- **Noise:** rejected (DSR 0.0001 fires (a); PBO 0.900 fires (b)). High confidence.
- **Chart-pattern rule:** rejected via (a) — DSR 0.0168. High confidence.
- **Planted edge:** **expected to be REJECTED via (b)**, because its PBO was
  0.514 ≥ 0.5. **This is a predicted FALSE POSITIVE of the amended rule**, and it
  is written down in advance rather than explained away afterwards.

## 5. Acceptance criteria for the AMENDED harness

Accepted only if all hold:

1. Noise **rejected**.
2. Chart-pattern rule **rejected**.
3. Criteria 3/4/5 from V1 still pass unchanged.
4. **The axis that fired is reported for every subject** — a bare "rejected" is
   not acceptable output.

## 6. The falsifier problem this amendment creates, named in advance

If the planted edge is rejected via PBO (as §4 predicts), then **the harness
rejects a known edge**, and its rejections are less informative than the V1 run
showed. That is a real cost of the OR-rule and must not be buried.

**Pre-committed handling:** report it as a *stated limitation of the selection-
level axis with correlated-or-independent config sets*, and record the honest
conclusion — **PBO is only meaningful when the configuration set represents a
genuine selection choice**, not when configs are independent draws or trivial
variants. Do **not** respond by loosening `PBO_FAIL_AT`, and do **not** drop the
falsifier. If this occurs, the recommended next step is a V3 that computes PBO
only over configuration sets where selection is real — pre-registered separately,
never patched in after seeing output.
