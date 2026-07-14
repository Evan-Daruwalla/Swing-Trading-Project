"""C1 - FF3-stripped residual reversal, per prereg prereg_c1_residual_reversal.md
(committed doc-only before this runner).

E16's weekly engine, ranking variable swapped: residual = sum of last 21 daily
OLS residuals (returns ~ Mkt-RF+SMB+HML+const, trailing 126 aligned sessions).
Bottom K=4 at next open, full weekly rebalance, 5 bps/side. FF3 daily from Ken
French library (fetched once, cached, gitignored). D1 + asymmetric framing.
No swing.db writes.

DATA CONVENTION: prices split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
"""
import datetime as dt
import io
import json
import math
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, CACHE, COST, CAP0
from run_e10_earnings_drift import UNIV

K = 4
BETA_N = 126
FORM_N = 21
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
FF_URL = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
          "F-F_Research_Data_Factors_daily_CSV.zip")


def ff3_daily():
    f = CACHE / "ff3_daily.json"
    if f.exists():
        return json.loads(f.read_text())
    req = urllib.request.Request(FF_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        z = zipfile.ZipFile(io.BytesIO(r.read()))
    txt = z.read(z.namelist()[0]).decode("latin-1")
    out = {}
    for line in txt.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 4 and len(parts[0]) == 8 and parts[0].isdigit():
            d = f"{parts[0][:4]}-{parts[0][4:6]}-{parts[0][6:]}"
            try:
                out[d] = [float(parts[1]) / 100, float(parts[2]) / 100,
                          float(parts[3]) / 100]
            except ValueError:
                continue
    f.write_text(json.dumps(out))
    return out


def isoweek(d):
    y, m, dd = map(int, d.split("-"))
    iso = dt.date(y, m, dd).isocalendar()
    return (iso[0], iso[1])


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mdd=float("nan"), sharpe=float("nan"))
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1] > 0]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mdd=mdd, sharpe=sh)


def residual_series(dates, cl, ff):
    """Per name: residual formation value at each index (or None)."""
    n = len(dates)
    rets, fac, ok = [0.0] * n, [None] * n, [False] * n
    for i in range(1, n):
        d = dates[i]
        if d in ff and cl[i - 1] > 0:
            rets[i] = cl[i] / cl[i - 1] - 1
            fac[i] = ff[d]
            ok[i] = True
    form = [None] * n
    aligned = [i for i in range(n) if ok[i]]
    pos_of = {i: j for j, i in enumerate(aligned)}
    R = np.array([rets[i] for i in aligned])
    X = np.column_stack([np.ones(len(aligned)),
                         np.array([fac[i] for i in aligned])])
    for j in range(BETA_N, len(aligned)):
        i = aligned[j]
        sl = slice(j - BETA_N + 1, j + 1)
        Xw, Rw = X[sl], R[sl]
        try:
            beta, *_ = np.linalg.lstsq(Xw, Rw, rcond=None)
        except np.linalg.LinAlgError:
            continue
        resid = Rw - Xw @ beta
        form[i] = float(resid[-FORM_N:].sum())
    return form


def main():
    ff = ff3_daily()
    print(f"FF3 daily: {len(ff)} rows, {min(ff)}..{max(ff)}", flush=True)
    oc, tdates, forms = {}, {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        ds = [b[1] for b in bars]
        cl = [b[5] for b in bars]
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = ds
        forms[t] = dict(zip(ds, residual_series(ds, cl, ff)))
        print(f"  {t}: {len(ds)} bars", flush=True)
    master = sorted({d for t in UNIV for d in tdates[t]})
    weekend = [master[i] for i in range(len(master) - 1)
               if isoweek(master[i]) != isoweek(master[i + 1])]
    weekend_set = set(weekend)

    def run(cost, c2c):
        cash, pos, pend = CAP0, {}, None
        navd, entries = {}, []
        idx = {t: {d: i for i, d in enumerate(tdates[t])} for t in UNIV}

        def px(t, d):
            i = idx[t][d]
            if c2c and i > 0:
                return oc[t][tdates[t][i - 1]][1]
            return oc[t][d][0]

        for d in master:
            if pend is not None:
                navv = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
                for t in list(pos):
                    if d in oc[t]:
                        cash += pos[t] * px(t, d) * (1 - cost); del pos[t]
                per = navv / K
                for t in pend:
                    if d in oc[t] and px(t, d) > 0:
                        sh = per / (px(t, d) * (1 + cost))
                        cash -= sh * px(t, d) * (1 + cost); pos[t] = sh
                        entries.append(d)
                pend = None
            navd[d] = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
            if d in weekend_set:
                ranked = sorted((forms[t].get(d), t) for t in UNIV
                                if forms[t].get(d) is not None)
                if len(ranked) >= K:
                    pend = [t for _, t in ranked[:K]]
        return navd, entries

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def report(tag, cost, c2c):
        navd, entries = run(cost, c2c)
        rows = {}
        for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
            nav = [navd[d] for d in master if lo <= d <= hi]
            seg = [d for d in sorted(spy) if lo <= d <= hi]
            ew = []
            for d in master:
                if lo <= d <= hi:
                    vals = [oc[t][d][1] / oc[t][tdates[t][0]][1]
                            for t in UNIV if d in oc[t]]
                    ew.append(sum(vals) / len(vals))
            rows[wn] = (stats(nav), stats([spy[d] / spy[seg[0]] for d in seg]),
                        stats(ew), sum(1 for d in entries if lo <= d <= hi))
        g, gs, gew, ng = rows["gate"]; s, ss, sew, _ = rows["sec"]
        print(f"{tag:24} gate {g['cagr']*100:6.2f}%/DD{g['mdd']*100:5.1f}%/Sh{g['sharpe']:5.2f}"
              f" | sec {s['cagr']*100:6.2f}%/DD{s['mdd']*100:5.1f}%/Sh{s['sharpe']:5.2f}"
              f" (gate n={ng})")
        return rows

    print(f"\nC1 residual reversal | K={K}, beta {BETA_N}d, formation {FORM_N}d\n")
    rows = report("C (next-open, 5bps) MAIN", COST, False)
    report("B (next-open, 0bps)", 0.0, False)
    report("A (c2c, 0bps)", 0.0, True)
    report("C stress 15bps", 0.0015, False)

    g, gs, gew, n_gate = rows["gate"]; s, ss, sew, _ = rows["sec"]
    print(f"\nbenchmarks gate: SPY {gs['cagr']*100:.2f}%/{gs['sharpe']:.2f}  "
          f"EW-39 {gew['cagr']*100:.2f}%/{gew['sharpe']:.2f}")
    print(f"benchmarks sec:  SPY {ss['cagr']*100:.2f}%/{ss['sharpe']:.2f}  "
          f"EW-39 {sew['cagr']*100:.2f}%/{sew['sharpe']:.2f}")
    print(f"E16 raw-reversal recorded: gate 16.76%/DD 65.9%/Sh 0.61")
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gs["sharpe"] and s["sharpe"] > ss["sharpe"]
          and g["cagr"] > 0 and s["cagr"] > 0)
    floor = n_gate >= 30
    print(f"\n=== D1 VERDICT (prereg prereg_c1_residual_reversal.md; asymmetric) ===")
    print(f"  gate entries {n_gate} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR   [{'PASS' if ra else 'fail'}] "
          f"PASS-RA (gate Sharpe {g['sharpe']:.2f})")
    if not floor:
        v = "INCONCLUSIVE"
    elif hr or ra:
        v = f"{'PASS-HR' if hr else 'PASS-RA'} (UNINTERPRETABLE - survivorship; forward only)"
    else:
        v = "FAIL (residual reversal closed)"
    print(f"\n  C1 VERDICT: {v}")


if __name__ == "__main__":
    main()
