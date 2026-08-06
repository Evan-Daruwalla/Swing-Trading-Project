"""V1 harness ACCEPTANCE TEST, per prereg_v1_cost_model_and_validation_harness.md
(doc-only commit ec51b91, before any harness code existed).

THE DONE-CHECK IS INVERTED: success is the harness REJECTING both test subjects.
A validation layer that passes noise is not weak, it is harmful -- it manufactures
confidence in exactly the situation it was built to prevent. If either subject
PASSES, that is the finding; it is reported and no strategy work proceeds.

Subjects (prereg section 6):
  6.1 classical chart-pattern rule -- ranked #6 of 6 on evidence by the brief, and
      already FAILED here as M11 (2026-07-14, signal-dead). Reuses M11's causal
      pivot detector rather than rebuilding it.
  6.2 pure-noise control -- seeded PRNG, independent of price by construction.
  5   planted-edge falsifier (REPORTED, NOT GATED) -- a harness that also rejects
      a KNOWN edge would make criteria 1-2 pass trivially.

DATA CONVENTION: prices are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED (auto_adjust=False),
via run_e8_squeeze.cache_fetch. Signal at close, execute NEXT OPEN (EOD rule).
No swing.db writes; the ledger is opened READ-ONLY by the cost model.
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_e8_squeeze import cache_fetch
# M11's pinned detector, reused verbatim (prereg 6.1): signals_for() runs the
# causal confirmation loop (a pivot at j is only visible from j+W), so no
# look-ahead is introduced by calling it here.
from run_m11_chart_patterns import signals_for, detect
from swing_bot import costs, validation
from swing_bot.universe_m12 import TICKERS

DSR_ALPHA = 0.05          # prereg section 4
PBO_FAIL_AT = 0.5         # prereg section 4
HOLD = 20
SEED = 20260806


def load_panel(tickers, start="2000-01-01"):
    """{ticker: (dates, opens, closes)} from the shared cache."""
    out = {}
    for t in tickers:
        try:
            b = cache_fetch(t)
        except Exception:
            continue
        d = [x[1] for x in b if x[1] >= start]
        if len(d) < 800:
            continue
        o = [x[2] for x in b if x[1] >= start]
        c = [x[5] for x in b if x[1] >= start]
        out[t] = (d, o, c)
    return out


def fwd_returns(dates, opens, closes, entries, hold, cost_bps):
    """Signal at close t -> fill at open t+1 -> exit at open t+1+hold.
    Returns a per-session return series aligned to `dates` (0 when flat)."""
    r = [0.0] * len(dates)
    cost = cost_bps / 10000.0
    for i in entries:
        j, k = i + 1, i + 1 + hold
        if k >= len(dates) or opens[j] <= 0 or opens[k] <= 0:
            continue
        gross = opens[k] / opens[j] - 1.0
        net = gross - 2 * cost
        # spread the trade's return across its holding window so the series is
        # per-session (CPCV blocks on sessions, not on trades)
        per = net / hold
        for x in range(j, k):
            r[x] += per
    return r


def pattern_signals_cached(panel):
    """Run M11's detector ONCE per ticker; configurations are then built by
    varying parameters at THIS layer (hold period, minimum breakout strength)
    rather than by mutating M11's pinned internals."""
    out = {}
    for t, (d, o, c) in panel.items():
        out[t] = signals_for(c, detect)      # {bar index: breakout strength}
    return out


def pattern_signal(panel, sigs, hold, min_strength, cost_bps):
    """One configuration of the chart-pattern rule, equal-weighted across the
    panel. Entries are M11's detections filtered at `min_strength`."""
    agg = None
    for t, (d, o, c) in panel.items():
        ent = [i for i, s in sigs[t].items() if s >= min_strength]
        r = fwd_returns(d, o, c, ent, hold, cost_bps)
        if agg is None:
            agg = r
        else:
            n = min(len(agg), len(r))
            agg = [agg[i] + r[i] for i in range(n)]
    if agg is None:
        return []
    n_t = max(1, len(panel))
    return [x / n_t for x in agg]            # equal-weight across tickers


def noise_signal(n, seed, cost_bps):
    """Pure noise: returns drawn independently of any price. By construction
    there is nothing to find."""
    rng = random.Random(seed)
    cost = cost_bps / 10000.0
    return [rng.gauss(0.0, 0.01) - cost / HOLD for _ in range(n)]


def planted_edge(n, seed, strength=0.05):
    """A series with a REAL, planted edge -- positive drift relative to its own
    volatility. Used only as the section-5 falsifier."""
    rng = random.Random(seed + 1)
    return [rng.gauss(strength * 0.01, 0.01) for _ in range(n)]


def evaluate(name, series_by_cfg, n_trials, gated=True):
    """Run one subject through CPCV -> DSR -> PBO and print the verdict."""
    print("\n" + "=" * 74)
    print("SUBJECT: %s   (%d configuration(s))" % (name, len(series_by_cfg)))
    print("=" * 74)
    base = series_by_cfg[0]
    n = len(base)
    if n < 100:
        print("  series too short (%d) -- cannot evaluate" % n)
        return None

    splits = validation.cpcv_splits(n, n_groups=6, n_test=2,
                                    label_span=HOLD, embargo_pct=0.01)
    path_sr = []
    for _, test_idx in splits:
        s = validation.sharpe([base[i] for i in test_idx])
        if s:
            path_sr.append(s["sr_period"])
    if len(path_sr) < 2:
        print("  too few usable CPCV paths")
        return None
    sr_var = statistics_pvariance(path_sr)
    print("  CPCV: %d paths | OOS per-period Sharpe median %+.4f  (min %+.4f, max %+.4f)"
          % (len(path_sr), sorted(path_sr)[len(path_sr) // 2],
             min(path_sr), max(path_sr)))

    d = validation.deflated_sharpe(base, n_trials, sr_var)
    if d is None or d.get("dsr") is None:
        print("  DSR: not computable (%s)" % (d or {}).get("reason", "n/a"))
        dsr_sig = False
        dsr_val = None
    else:
        dsr_val = d["dsr"]
        dsr_sig = dsr_val > (1.0 - DSR_ALPHA)
        print("  Sharpe (annualised)      %+.3f" % d["sr_annual"])
        print("  E[max Sharpe] under null %+.5f  (from n_trials=%d)"
              % (d["sr0_expected_max"], d["n_trials"]))
        print("  DSR                      %.4f   -> %s at alpha=%.2f"
              % (dsr_val, "SIGNIFICANT" if dsr_sig else "NOT significant", DSR_ALPHA))

    p = validation.pbo_cscv(series_by_cfg, n_blocks=8) if len(series_by_cfg) > 1 \
        else {"pbo": None, "reason": "single configuration"}
    if p.get("pbo") is None:
        print("  PBO                      n/a (%s)" % p.get("reason"))
    else:
        print("  PBO                      %.3f over %d splits -> %s"
              % (p["pbo"], p["n_splits"],
                 "OVERFIT (>=%.1f)" % PBO_FAIL_AT if p["pbo"] >= PBO_FAIL_AT
                 else "below threshold"))

    rejected = (not dsr_sig) and (p.get("pbo") is None or p["pbo"] >= PBO_FAIL_AT)
    if gated:
        print("  VERDICT: %s" % ("REJECTED (as required)" if rejected
                                 else "*** NOT REJECTED -- see done-check ***"))
    else:
        print("  VERDICT (diagnostic, not gated): %s"
              % ("rejected" if rejected else "not rejected"))
    return {"rejected": rejected, "dsr": dsr_val, "pbo": p.get("pbo"),
            "sr_var": sr_var, "paths": path_sr}


def statistics_pvariance(xs):
    import statistics as st
    return st.pvariance(xs) if len(xs) > 1 else 0.0


def main():
    print("V1 HARNESS ACCEPTANCE TEST (prereg ec51b91)")

    # --- criterion 4: cost model must FAIL LOUD on today's data -------------
    print("\n[criterion 4] cost model must RAISE on insufficient fills")
    try:
        est = costs.estimate_friction()
        print("  *** DID NOT RAISE -- returned %s" % est)
        c4 = False
    except costs.InsufficientFillData as e:
        print("  RAISED as required: %s" % str(e).splitlines()[0])
        c4 = True
    est_assumed = costs.estimate_friction(assumed_bps=5.0)
    print("  explicit override -> %s" % est_assumed)
    cost_bps = est_assumed.median_bps

    # --- criterion 5: DSR must refuse a missing/stale trial log -------------
    print("\n[criterion 5] DSR must RAISE without a usable trial log")
    try:
        validation.load_trial_count(path="docs/__no_such_trial_log__.json")
        print("  *** DID NOT RAISE")
        c5 = False
    except validation.TrialLogUnavailable as e:
        print("  RAISED as required: %s" % str(e).splitlines()[0])
        c5 = True
    n_trials, prov = validation.load_trial_count()
    print("  live trial count: %d\n    source: %s" % (n_trials, prov))

    # --- subjects ------------------------------------------------------------
    print("\nloading price panel (subset of the frozen 142-name universe)...")
    panel = load_panel(TICKERS[:40])
    print("  %d tickers loaded" % len(panel))

    # 6.1 chart-pattern rule. PBO needs a SET of configurations, so sweep the
    # parameters a researcher would actually sweep (hold period, entry-strength
    # filter). Each is a trial, which is precisely why the trial log matters.
    print("  running M11 detector over the panel ...")
    sigs = pattern_signals_cached(panel)
    n_sig = sum(len(v) for v in sigs.values())
    print("  M11 detections: %d across %d tickers" % (n_sig, len(sigs)))
    cfgs = [(10, 0.0), (20, 0.0), (20, 0.01), (40, 0.0), (40, 0.02)]
    pat = []
    for hold, ms in cfgs:
        s = pattern_signal(panel, sigs, hold, ms, cost_bps)
        if s:
            pat.append(s)
    if not pat:
        print("  no pattern series produced -- cannot evaluate subject 6.1")
        return 1
    n_min = min(len(x) for x in pat)
    pat = [x[:n_min] for x in pat]
    r_pat = evaluate("6.1 classical chart-pattern rule (M11 detector)",
                     pat, n_trials)

    # 6.2 pure noise
    noise = [noise_signal(n_min, SEED + i, cost_bps) for i in range(len(cfgs))]
    r_noise = evaluate("6.2 pure-noise control (seeded PRNG)", noise, n_trials)

    # criterion 3: purging must demonstrably bite
    print("\n[criterion 3] purge+embargo must change the result")
    sp_on = validation.cpcv_splits(n_min, 6, 2, label_span=HOLD, embargo_pct=0.01)
    sp_off = validation.cpcv_splits(n_min, 6, 2, label_span=0, embargo_pct=0.0)
    tr_on = statistics_mean([len(a) for a, _ in sp_on])
    tr_off = statistics_mean([len(a) for a, _ in sp_off])
    print("  mean train size  purge OFF %.0f -> purge ON %.0f  (%.0f obs removed)"
          % (tr_off, tr_on, tr_off - tr_on))
    c3 = tr_on < tr_off

    # section 5 falsifier: a KNOWN edge should NOT be rejected
    planted = [planted_edge(n_min, SEED + 100 + i) for i in range(len(cfgs))]
    r_plant = evaluate("5 planted-edge falsifier (DIAGNOSTIC, not gated)",
                       planted, n_trials, gated=False)

    # --- acceptance ----------------------------------------------------------
    print("\n" + "=" * 74)
    print("ACCEPTANCE (prereg section 4)")
    print("=" * 74)
    c1 = bool(r_noise and r_noise["rejected"])
    c2 = bool(r_pat and r_pat["rejected"])
    for lbl, ok in (("1 rejects pure noise", c1),
                    ("2 rejects chart-pattern rule", c2),
                    ("3 purging demonstrably bites", c3),
                    ("4 cost model fails loud", c4),
                    ("5 DSR refuses stale/missing trial log", c5)):
        print("  [%s] %s" % ("PASS" if ok else "FAIL", lbl))
    ok = all([c1, c2, c3, c4, c5])
    print("\nHARNESS %s" % ("ACCEPTED" if ok else "NOT ACCEPTED -- report as the finding"))
    if r_plant is not None:
        print("diagnostic: planted edge was %s"
              % ("REJECTED -- harness may reject everything; rejections carry "
                 "little information" if r_plant["rejected"] else
                 "NOT rejected (expected) -- rejections are informative"))
    return 0 if ok else 1


def statistics_mean(xs):
    import statistics as st
    return st.fmean(xs) if xs else 0.0


if __name__ == "__main__":
    sys.exit(main())
