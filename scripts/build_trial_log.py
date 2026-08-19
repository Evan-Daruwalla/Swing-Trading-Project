"""Extract a MACHINE-READABLE trial log from the project's own artifacts.

WHY THIS EXISTS: the deflated Sharpe ratio (Bailey & Lopez de Prado) deflates an
observed Sharpe by the number of trials the search actually conducted. That
number is the single easiest input to fudge -- understate it and DSR reports
significance that was bought by search effort. This project's append-only record
already IS an unusually honest trial log (every attempt pre-registered and
dated), but it is PROSE. A DSR calculation cannot consume prose, and a human
re-counting it by hand each time will drift.

SOURCES (all first-party, nothing invented):
  - docs/prereg_*.md          one file per pre-registered attempt (TEMPLATE excluded)
  - git log                   the prereg commit hash + author date (the
                              "hash predates the runner" claim is the project's
                              core rigor claim, so the hash is part of the record)
  - docs/research/*results*   the verdict, where a results doc exists
  - the appendix record       attempt numbering ("Attempt #38")

ANYTHING NOT DETERMINABLE IS EMITTED AS null WITH A `_unknown` NOTE. This script
never guesses a verdict, a date, or a variant count. A trial log that quietly
fills gaps would defeat its own purpose.

DATA CONVENTION: this script touches no price data. It reads docs and git only.
"""
import json
import os
import re
import subprocess
import sys

# Anchored to THIS FILE, not to os.getcwd() (audit E8). With getcwd(), running
# the script from another repo that happens to have a docs/ tree would build a
# trial log out of THAT project's preregs and write it there -- and the trial
# count is DSR's deflation input, so a wrong-project N silently produces a
# significance number that looks rigorous and is not.
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREREG_DIR = os.path.join(REPO, "docs")
RESEARCH_DIR = os.path.join(REPO, "docs", "research")
RECORD = os.path.join(REPO, "docs",
                      "Project Record — Full Chronological History.md")
OUT = os.path.join(REPO, "docs", "trial_log.json")

# Attempts whose prereg declares MORE THAN ONE tested variant/arm/cell. Each
# entry cites the prereg section that declares it -- this is transcription from
# a committed doc, not estimation. Attempts absent here are treated as 1 declared
# variant, which is a LOWER BOUND (see `variant_count_is_lower_bound` in output).
DECLARED_VARIANTS = {
    "e18_regime_gate_bakeoff": (4, "4 pre-declared gates (a)-(d), prereg 'Four a-priori "
                                   "risk-on/off gates'"),
    "m12_constraint_factorial": (8, "2x2 cells x 2 cost levels (5bps + 15bps stress), "
                                    "prereg sections 3-4"),
    "x8_noneq_trend": (2, "2 pre-declared arms GLD/TLT, prereg section 3, with an explicit "
                          "multiple-comparison disclosure"),
    "m11_chart_patterns": (2, "long-side gated rule + a REPORTED-not-gated short-side "
                              "diagnostic"),
    "x9_pairs_relative_value": (2, "gated run + a post-hoc zero-cost diagnostic "
                                   "(explicitly not gated)"),
}

# Preregs that are INFRASTRUCTURE, not attempts: they build no strategy and
# claim no edge, so they are not trials in DSR's search space.
#
# EXPLICIT, not prose-detected (audit E9). This used to be a regex for "not an
# attempt" over the first 4000 chars of every prereg. That put DSR's deflation
# input at the mercy of an English phrase: any STRATEGY prereg that used those
# words in any sense would drop out of N, lowering the trial count and INFLATING
# DSR -- the exact direction validation.py exists to guard against, and silently.
# An explicit list fails the other way: forget to add one and N is too LARGE,
# which only makes DSR more conservative. Both errors now point somewhere safe.
NON_ATTEMPT_PREREGS = frozenset({
    "v1_cost_model_and_validation_harness",
    "v2_harness_acceptance_amendment",
    # V3 scopes WHERE the PBO axis applies; it builds no strategy and claims no
    # edge, and its own section 7.4 states the attempt tally does not move --
    # same class as V1/V2 (added 2026-08-19, record FC).
    # DIRECTION DISCLOSED: excluding a prereg LOWERS N, which INFLATES DSR --
    # the unsafe direction this list's own comment warns about. It is done here
    # because the classification is correct and consistent with V1/V2, not
    # because it helps; the record states N and the DSR consequence BOTH ways.
    "v3_pbo_scoping",
})

# Kept only to FLAG a mismatch between the list above and what a doc says about
# itself; it never excludes anything on its own.
SELF_DECLARES_NON_ATTEMPT = re.compile(
    r"not an attempt|does not increment the (?:attempt )?tally", re.I)


def sh(args):
    try:
        return subprocess.check_output(args, cwd=REPO, text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def git_first_commit(path):
    """(hash, iso_date) of the commit that ADDED this file, or (None, None)."""
    out = sh(["git", "log", "--diff-filter=A", "--format=%h|%aI", "--", path])
    if not out:
        out = sh(["git", "log", "--format=%h|%aI", "--", path])
    if not out:
        return None, None
    h, d = out.splitlines()[-1].split("|", 1)
    return h, d


def find_results(stem):
    """Results doc for an attempt stem, or None.

    STRICT token match. A loose match is not a cosmetic problem here: the first
    version of this matcher took the token before the first '_', so `m10_2_...`
    matched M10-**1**'s results doc and the log recorded m10_2 as PASS-HR when
    M10-2 actually FAILED (2.99% CAGR / 83.3% DD). A trial log that invents a
    verdict is worse than no trial log, so the token now keeps its numeric
    suffix and must be delimited on BOTH sides.
    """
    parts = stem.lower().split("_")
    token = parts[0]
    # keep a numeric sub-index: m10_2 -> m10-2, x2b stays x2b, e1b stays e1b
    if len(parts) > 1 and parts[1].isdigit():
        token = "%s-%s" % (parts[0], parts[1])
    pat = re.compile(r"(?:^|[_\-])%s(?:[_\-]|$)" % re.escape(token))
    hits = []
    for f in sorted(os.listdir(RESEARCH_DIR)):
        low = f.lower()
        if "result" not in low:
            continue
        # strip the leading date so it cannot contribute delimiters/digits
        body = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", low)
        if pat.search(body):
            hits.append(os.path.join("docs", "research", f))
    return hits or None


VERDICT_RE = re.compile(
    r"\b(FAIL|PASS-HR|PASS-RA|PASS|PROMISING|DIAGNOSTIC|NEAR-MISS|CLEARS)\b")


def verdict_from(paths):
    """First verdict token in the results doc's headline area, or None."""
    if not paths:
        return None
    try:
        head = open(os.path.join(REPO, paths[0]), encoding="utf-8").read()[:1600]
    except OSError:
        return None
    m = VERDICT_RE.search(head)
    return m.group(1) if m else None


def main():
    stems, excluded = [], []
    for f in sorted(os.listdir(PREREG_DIR)):
        m = re.match(r"^prereg_(.+)\.md$", f)
        if not m:
            continue
        stem = m.group(1)
        if stem == "TEMPLATE":
            continue
        path = os.path.join("docs", f)
        try:
            txt = open(os.path.join(REPO, path), encoding="utf-8").read(4000)
        except OSError:
            txt = ""
        if stem in NON_ATTEMPT_PREREGS:
            excluded.append({"file": path,
                             "reason": "infrastructure, not an attempt (explicit "
                                       "NON_ATTEMPT_PREREGS entry)"})
            continue
        if SELF_DECLARES_NON_ATTEMPT.search(txt):
            # Self-declaration is a PROMPT, never the decision (audit E9). Left
            # counted, which is the conservative direction; the operator adds it
            # to NON_ATTEMPT_PREREGS deliberately if it really is infrastructure.
            print("  ?? %s self-declares 'not an attempt' but is not in "
                  "NON_ATTEMPT_PREREGS -- COUNTING it as a trial. Add it to the "
                  "constant if that is wrong." % path)
        stems.append((stem, path))

    trials, unknowns = [], 0
    for stem, path in stems:
        h, d = git_first_commit(path)
        res = find_results(stem)
        v = verdict_from(res)
        nvar, vnote = DECLARED_VARIANTS.get(stem, (1, "no additional arms declared in prereg"))
        rec = {
            "id": stem,
            "prereg_file": path,
            "prereg_commit": h,
            "prereg_date": (d or "")[:10] or None,
            "results_files": res,
            # NOT the program's final verdict. This is the first verdict token in
            # the results doc's headline AT PUBLICATION. Several were later
            # superseded -- E4 published PASS and was then KILLED by E5 (92.7% DD
            # in the unseen 2000-13 window); E6 published PASS and was downgraded
            # to a market-dependent risk overlay. The append-only record is
            # authoritative for final verdicts; this field is a pointer, not a
            # ruling, and DSR must not treat it as one.
            "headline_verdict_at_publication": v,
            "final_verdict": None,
            "_final_verdict_note": "requires the record; not auto-derivable",
            "declared_variants": nvar,
            "variant_basis": vnote,
        }
        miss = [k for k in ("prereg_commit", "prereg_date",
                            "headline_verdict_at_publication") if rec[k] is None]
        if miss:
            rec["_unknown"] = miss
            unknowns += 1
        trials.append(rec)

    # attempt numbering as the RECORD states it (not inferred from file count)
    rec_txt = open(RECORD, encoding="utf-8").read()
    nums = [int(x) for x in re.findall(r"[Aa]ttempt #?(\d+)", rec_txt)]
    max_attempt = max(nums) if nums else None

    total_declared = sum(t["declared_variants"] for t in trials)
    doc = {
        "generated_by": "scripts/build_trial_log.py",
        "sources": ["docs/prereg_*.md", "git log", "docs/research/*results*",
                    "docs/Project Record — Full Chronological History.md"],
        "prereg_docs_found": len(trials),
        "max_attempt_number_in_record": max_attempt,
        "attempt_count_discrepancy": (
            None if max_attempt is None or max_attempt == len(trials) else
            {"record_says": max_attempt, "prereg_docs": len(trials),
             "note": "UNRESOLVED -- do not silently pick one. See docs/trial_log_notes.md"}),
        "declared_variant_total": total_declared,
        "variant_count_is_lower_bound": True,
        "lower_bound_reason": (
            "Counts only variants DECLARED in a prereg. Excludes: parameter values "
            "explored before pre-registration, the ~90-method survey and the "
            "dropped-16 list (record Appendix B), and any abandoned variant never "
            "written down. The true search effort is strictly LARGER, so any DSR "
            "computed from this number is OPTIMISTIC (too generous to the strategy)."),
        "entries_with_unknown_fields": unknowns,
        # Files intentionally NOT counted as trials. validation.load_trial_count
        # also skips these in its staleness scan, so adding infrastructure docs
        # cannot spuriously mark the log stale.
        "excluded_non_attempt": excluded,
        "trials": trials,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")

    print("prereg docs (TEMPLATE excluded): %d" % len(trials))
    print("max attempt number in record   : %s" % max_attempt)
    print("declared-variant total         : %d  (LOWER BOUND)" % total_declared)
    print("entries with unknown fields    : %d" % unknowns)
    if doc["attempt_count_discrepancy"]:
        print("\n!! ATTEMPT-COUNT DISCREPANCY: record says %d, prereg docs = %d"
              % (max_attempt, len(trials)))
    print("\nverdict tally:")
    tally = {}
    for t in trials:
        k = t["headline_verdict_at_publication"]
        tally[k] = tally.get(k, 0) + 1
    for k in sorted(tally, key=lambda z: (z is None, str(z))):
        print("   %-12s %d" % (k, tally[k]))
    print("\nwrote %s" % os.path.relpath(OUT, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
