"""Purged CV / CPCV / deflated Sharpe / PBO, per
prereg_v1_cost_model_and_validation_harness.md (doc-only commit ec51b91,
before this file existed).

WHAT THIS IS FOR: a backtest Sharpe computed after searching many variants is
not evidence. This module's job is to REJECT things -- specifically, to reject a
strategy whose apparent skill is explained by (a) leakage across overlapping
labels, or (b) the number of trials that were run to find it.

Stdlib only, deliberately: numpy is a transitive dependency here, not a declared
one, and the data volumes are tiny.

DATA CONVENTION: this module consumes RETURN SERIES only, never prices. Callers
that build those returns from prices must honour the project convention
(split-adjusted, dividend-UNADJUSTED) at their own layer.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import statistics
from statistics import NormalDist

EULER_GAMMA = 0.5772156649015329
_N = NormalDist()

# Repo-anchored, not CWD-relative (audit E8): these were "docs/...", so the
# trial count -- DSR's deflation input -- depended on where the caller happened
# to be standing. From a scratch directory load_trial_count() raised
# TrialLogUnavailable (loud, survivable); from another repo with a docs/ tree it
# would have read the wrong project's log (silent, not survivable).
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAL_LOG = os.path.join(_REPO, "docs", "trial_log.json")
PREREG_GLOB_DIR = os.path.join(_REPO, "docs")


class TrialLogUnavailable(RuntimeError):
    """Raised when the trial count cannot be established. Never defaulted: a DSR
    computed from a guessed N is a number that looks rigorous and is not."""


def load_trial_count(path=TRIAL_LOG, check_staleness=True):
    """Trial count for DSR, read from the machine-readable trial log.

    RAISES if the log is missing, unreadable, or older than the newest prereg
    doc (prereg section 3.3). A stale log under-counts trials in exactly the
    direction that flatters the strategy, so staleness is a hard error.

    Returns (n_trials, provenance_string).
    """
    if not os.path.exists(path):
        raise TrialLogUnavailable(
            "trial log %r not found. DSR requires an explicit trial count; "
            "refusing to guess one. Run: python scripts/build_trial_log.py" % path)
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as e:
        raise TrialLogUnavailable("trial log %r unreadable: %s" % (path, e))

    if check_staleness:
        log_mtime = os.path.getmtime(path)
        # Preregs the log deliberately does NOT count as trials (infrastructure
        # docs that build no strategy) must not mark the log stale either --
        # otherwise adding one forces a pointless regeneration and, worse,
        # trains the reader to ignore a real staleness error.
        skip = {os.path.basename(e.get("file", ""))
                for e in doc.get("excluded_non_attempt", [])}
        newest, newest_f = 0.0, None
        for f in os.listdir(PREREG_GLOB_DIR):
            if f.startswith("prereg_") and f.endswith(".md") and f not in skip:
                m = os.path.getmtime(os.path.join(PREREG_GLOB_DIR, f))
                if m > newest:
                    newest, newest_f = m, f
        if newest > log_mtime:
            raise TrialLogUnavailable(
                "trial log is STALE: %r is newer than %s. Regenerate with "
                "`python scripts/build_trial_log.py` -- a stale log under-counts "
                "trials, which inflates DSR." % (newest_f, path))

    # Larger of the two figures, per trial_log_notes.md: erring toward MORE
    # trials makes DSR more conservative; fewer flatters the strategy.
    a = doc.get("max_attempt_number_in_record") or 0
    b = doc.get("declared_variant_total") or 0
    n = max(a, b)
    if n <= 0:
        raise TrialLogUnavailable("trial log contains no usable trial count")
    return n, ("trial_log.json: max(attempts=%s, declared_variants=%s) = %d "
               "(LOWER BOUND -- excludes pre-prereg exploration)" % (a, b, n))


# ---------------------------------------------------------------- purged CV --
def purge_embargo_train(n_obs, test_idx, label_span, embargo_n):
    """Training indices after purging label-overlap and applying an embargo.

    Purge: an observation at t carries a label spanning [t, t+label_span]. If
    that window touches any test observation's window, t leaks and is dropped.
    Embargo: additionally drop `embargo_n` observations immediately AFTER the
    test block, where serial correlation persists.
    """
    if not test_idx:
        return list(range(n_obs))
    lo, hi = min(test_idx), max(test_idx)
    banned_lo = lo - label_span          # its label can reach into the test block
    banned_hi = hi + label_span + embargo_n
    return [i for i in range(n_obs) if i < banned_lo or i > banned_hi]


def cpcv_splits(n_obs, n_groups=6, n_test=2, label_span=1, embargo_pct=0.01):
    """Combinatorial purged CV -> list of (train_idx, test_idx).

    C(n_groups, n_test) paths; C(6,2)=15 at the pre-registered settings. Each
    yields an out-of-sample slice, so the output is a DISTRIBUTION of OOS
    performance rather than one number from one split.
    """
    bounds = [round(i * n_obs / n_groups) for i in range(n_groups + 1)]
    groups = [list(range(bounds[i], bounds[i + 1])) for i in range(n_groups)]
    embargo_n = max(1, int(embargo_pct * n_obs))
    out = []
    for combo in itertools.combinations(range(n_groups), n_test):
        test_idx = sorted(i for g in combo for i in groups[g])
        train_idx = purge_embargo_train(n_obs, test_idx, label_span, embargo_n)
        out.append((train_idx, test_idx))
    return out


# ------------------------------------------------------------------- sharpe --
def sharpe(returns, periods_per_year=252):
    """Per-period Sharpe (NOT annualised) plus its annualised twin.
    DSR consumes the PER-PERIOD figure -- annualising first is a common and
    silent error that shifts the deflation benchmark."""
    r = [x for x in returns if x is not None]
    if len(r) < 3:
        return None
    mu = statistics.fmean(r)
    sd = statistics.pstdev(r)
    if sd == 0:
        return None
    sr = mu / sd
    return {"sr_period": sr, "sr_annual": sr * math.sqrt(periods_per_year),
            "n": len(r), "mean": mu, "sd": sd}


def _moments(returns):
    r = [x for x in returns if x is not None]
    n = len(r)
    mu = statistics.fmean(r)
    sd = statistics.pstdev(r)
    if sd == 0 or n < 4:
        return 0.0, 3.0
    m3 = sum((x - mu) ** 3 for x in r) / n
    m4 = sum((x - mu) ** 4 for x in r) / n
    return m3 / sd ** 3, m4 / sd ** 4          # skew, kurtosis (normal = 3)


def expected_max_sharpe(n_trials, sr_variance):
    """E[max SR] across `n_trials` independent trials whose TRUE Sharpe is zero
    (Bailey & Lopez de Prado 2014). This is the benchmark an observed Sharpe must
    beat to mean anything -- with enough trials, a high Sharpe is the expected
    outcome of searching, not evidence of skill."""
    if n_trials < 2 or sr_variance <= 0:
        return 0.0
    a = _N.inv_cdf(1.0 - 1.0 / n_trials)
    b = _N.inv_cdf(1.0 - 1.0 / (n_trials * math.e))
    return math.sqrt(sr_variance) * ((1.0 - EULER_GAMMA) * a + EULER_GAMMA * b)


def deflated_sharpe(returns, n_trials, sr_variance, periods_per_year=252):
    """Deflated Sharpe ratio. Returns a dict including `dsr` (a probability) and
    `significant` at the caller's alpha.

    NOTE ON sr_variance: the formulation wants the variance of Sharpe ratios
    ACROSS the trials that were searched. This project does not store a Sharpe
    for every historical trial, so callers pass the variance of the CPCV path
    Sharpes as a proxy. That is an APPROXIMATION and is surfaced in the output
    rather than hidden."""
    s = sharpe(returns, periods_per_year)
    if s is None:
        return None
    sr = s["sr_period"]
    skew, kurt = _moments(returns)
    t = s["n"]
    sr0 = expected_max_sharpe(n_trials, sr_variance)
    denom = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr
    if denom <= 0 or t < 2:
        return {"dsr": None, "reason": "denominator non-positive or T<2",
                "sr_period": sr, "sr_annual": s["sr_annual"], "sr0": sr0,
                "skew": skew, "kurtosis": kurt, "n_trials": n_trials, "T": t}
    z = (sr - sr0) * math.sqrt(t - 1) / math.sqrt(denom)
    return {"dsr": _N.cdf(z), "z": z, "sr_period": sr, "sr_annual": s["sr_annual"],
            "sr0_expected_max": sr0, "skew": skew, "kurtosis": kurt,
            "n_trials": n_trials, "T": t, "sr_variance_used": sr_variance,
            "sr_variance_note": "proxy: variance of CPCV path Sharpes"}


# ---------------------------------------------------------------------- PBO --
def pbo_cscv(returns_matrix, n_blocks=8):
    """Probability of backtest overfitting via CSCV (Bailey et al. 2016).

    `returns_matrix`: list of N configurations, each a list of T returns.
    Splits T into `n_blocks` blocks; for every way of choosing half as
    in-sample, picks the IS-best configuration and asks where it lands
    out-of-sample. PBO = fraction of splits where the IS winner falls at or
    below the OOS MEDIAN -- i.e. how often the selection procedure is worse
    than a coin flip.
    """
    n_cfg = len(returns_matrix)
    if n_cfg < 2:
        return {"pbo": None, "reason": "need >= 2 configurations"}
    t = min(len(r) for r in returns_matrix)
    if t < n_blocks * 2:
        return {"pbo": None, "reason": "series too short for %d blocks" % n_blocks}
    if n_blocks % 2:
        n_blocks -= 1
    bnd = [round(i * t / n_blocks) for i in range(n_blocks + 1)]
    blocks = [list(range(bnd[i], bnd[i + 1])) for i in range(n_blocks)]

    lambdas = []
    for combo in itertools.combinations(range(n_blocks), n_blocks // 2):
        is_idx = sorted(i for b in combo for i in blocks[b])
        oos_idx = sorted(i for b in range(n_blocks) if b not in combo
                         for i in blocks[b])
        is_sr, oos_sr = [], []
        for r in returns_matrix:
            a = sharpe([r[i] for i in is_idx])
            b = sharpe([r[i] for i in oos_idx])
            is_sr.append(a["sr_period"] if a else float("-inf"))
            oos_sr.append(b["sr_period"] if b else float("-inf"))
        best = max(range(n_cfg), key=lambda i: is_sr[i])
        # relative rank of the IS winner among OOS performances
        worse = sum(1 for i in range(n_cfg) if oos_sr[i] < oos_sr[best])
        omega = (worse + 1.0) / (n_cfg + 1.0)
        omega = min(max(omega, 1e-9), 1 - 1e-9)
        lambdas.append(math.log(omega / (1 - omega)))
    if not lambdas:
        return {"pbo": None, "reason": "no splits"}
    return {"pbo": sum(1 for x in lambdas if x <= 0) / len(lambdas),
            "n_splits": len(lambdas), "median_lambda": statistics.median(lambdas)}
