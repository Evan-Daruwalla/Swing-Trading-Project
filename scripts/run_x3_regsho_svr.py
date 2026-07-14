"""X3 - Reg SHO daily short-volume drift, per prereg prereg_x3_regsho_svr.md
(committed doc-only before this runner).

Rank 39 survivors by trailing-5-session mean SVR (ShortVolume/TotalVolume) at
each ISO-week-end; long the K=5 LOWEST-SVR names, weekly rebalance, enter next
open (1-session lag), 5 bps/side. Existence spread (low-K minus high-K) for the
sign. Gate 2009-08..2013-12 / secondary 2014- -> MODIFIED-WINDOW CAP (PROMISING).
No swing.db writes.

DATA CONVENTION: prices split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
SVR = executed short flow (MM-hedging contaminated), NOT short interest.
"""
import datetime as dt
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e10_earnings_drift import UNIV

K = 5
MEAN_N = 5
GATE = ("2009-08-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
SVR = json.loads((Path("D:/ClaudeCode/Swing Trading/.regsho_cache") /
                  "short_volume.json").read_text())


def isoweek(d):
    y, m, dd = map(int, d.split("-"))
    return dt.date(y, m, dd).isocalendar()[:2]


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


def main():
    oc, tdates = {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = [b[1] for b in bars]
    master = sorted({d for t in UNIV for d in tdates[t] if d >= GATE[0]})
    svr_days = sorted(SVR)

    # trailing-5-session mean SVR per name at each master date (through that date)
    def mean_svr(t, d):
        idx = [x for x in svr_days if x <= d][-MEAN_N:]
        vals = [SVR[x][t] for x in idx if t in SVR[x]]
        return sum(vals) / len(vals) if len(vals) >= 3 else None

    weekend = [master[i] for i in range(len(master) - 1)
               if isoweek(master[i]) != isoweek(master[i + 1])]
    # precompute rankings at each week-end
    rank_at = {}
    for d in weekend:
        scored = [(mean_svr(t, d), t) for t in UNIV]
        scored = [(s, t) for s, t in scored if s is not None and d in oc[t]]
        if len(scored) >= 2 * K:
            scored.sort()
            rank_at[d] = ([t for _, t in scored[:K]], [t for _, t in scored[-K:]])
    entries_dates = sorted(rank_at)

    idx = {t: {d: i for i, d in enumerate(tdates[t])} for t in UNIV}

    def next_open_date(d):
        after = [x for x in master if x > d]
        return after[0] if after else None

    # map: entry_date (next session after weekend) -> (low, high)
    ecal = {}
    for d in entries_dates:
        nd = next_open_date(d)
        if nd:
            ecal[nd] = rank_at[d]

    def long_leg(fill, cost):
        px = 0 if fill == "open" else 1
        cash, pos, navd = CAP0, {}, {}
        for d in master:
            if d in ecal:
                navv = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
                for t in list(pos):
                    if d in oc[t]:
                        cash += pos[t] * oc[t][d][px] * (1 - cost); del pos[t]
                per = navv / K
                for t in ecal[d][0]:
                    if d in oc[t] and oc[t][d][px] > 0:
                        sh = per / (oc[t][d][px] * (1 + cost))
                        cash -= sh * oc[t][d][px] * (1 + cost); pos[t] = sh
            navd[d] = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
        return [navd[d] for d in master]

    def spread():
        lo_nav, hi_nav, held = [CAP0], [CAP0], None
        for i in range(1, len(master)):
            d0, d1 = master[i - 1], master[i]
            if d0 in ecal:
                held = ecal[d0]
            if held is None:
                lo_nav.append(lo_nav[-1]); hi_nav.append(hi_nav[-1]); continue
            def bret(names):
                rs = [oc[t][d1][1] / oc[t][d0][1] - 1 for t in names
                      if d0 in oc[t] and d1 in oc[t] and oc[t][d0][1] > 0]
                return sum(rs) / len(rs) if rs else 0.0
            lo_nav.append(lo_nav[-1] * (1 + bret(held[0])))
            hi_nav.append(hi_nav[-1] * (1 + bret(held[1])))
        ls = [1.0]
        for i in range(1, len(lo_nav)):
            ls.append(ls[-1] * (1 + (lo_nav[i]/lo_nav[i-1]-1) - (hi_nav[i]/hi_nav[i-1]-1)))
        return stats(lo_nav), stats(hi_nav), stats(ls)

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def wins(nav):
        out = {}
        for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
            seg = [nav[i] for i, d in enumerate(master) if lo <= d <= hi]
            sseg = [d for d in sorted(spy) if lo <= d <= hi]
            ew = []
            for d in master:
                if lo <= d <= hi:
                    vals = [oc[t][d][1] / oc[t][tdates[t][0]][1]
                            for t in UNIV if d in oc[t]]
                    ew.append(sum(vals) / len(vals))
            out[wn] = (stats(seg), stats([spy[d]/spy[sseg[0]] for d in sseg]), stats(ew))
        return out

    print(f"X3 Reg SHO SVR | {master[0]}..{master[-1]} ({len(master)} sessions); "
          f"cycles {len(ecal)}; K={K}\n")
    rC = wins(long_leg("open", COST))
    rB = wins(long_leg("open", 0.0))
    rA = wins(long_leg("close", 0.0))
    r15 = wins(long_leg("open", 0.0015))
    lo_s, hi_s, ls_s = spread()

    print(f"{'leg':22}{'gate CAGR/DD/Sh':>26}{'sec CAGR/DD/Sh':>26}")
    for tag, r in [("long C next-open+5bps", rC), ("long B next-open 0bps", rB),
                   ("long A c2c 0bps", rA), ("long 15bps", r15)]:
        g, _, _ = r["gate"]; s, _, _ = r["sec"]
        print(f"{tag:22}{g['cagr']*100:8.2f}%/{g['mdd']*100:4.1f}%/{g['sharpe']:4.2f}"
              f"{'':>6}{s['cagr']*100:8.2f}%/{s['mdd']*100:4.1f}%/{s['sharpe']:4.2f}")
    g, gspy, gew = rC["gate"]; s, sspy, sew = rC["sec"]
    print(f"\nbenchmarks gate: SPY {gspy['cagr']*100:.2f}%/{gspy['sharpe']:.2f}  "
          f"EW-39 {gew['cagr']*100:.2f}%/{gew['sharpe']:.2f}")
    print(f"benchmarks sec:  SPY {sspy['cagr']*100:.2f}%/{sspy['sharpe']:.2f}  "
          f"EW-39 {sew['cagr']*100:.2f}%/{sew['sharpe']:.2f}")
    print(f"existence spread: low-SVR {lo_s['cagr']*100:+.2f}%  high-SVR "
          f"{hi_s['cagr']*100:+.2f}%  LONG-SHORT {ls_s['cagr']*100:+.2f}%/Sh {ls_s['sharpe']:.2f}")

    beats = (g["cagr"] > gspy["cagr"] and g["cagr"] > gew["cagr"]
             and s["cagr"] > sspy["cagr"] and s["cagr"] > sew["cagr"]
             and g["sharpe"] > gspy["sharpe"] and s["sharpe"] > sspy["sharpe"])
    sign_ok = ls_s["cagr"] > 0
    floor = len(ecal) >= 30
    print(f"\n=== VERDICT (prereg prereg_x3_regsho_svr.md; PROMISING-capped) ===")
    print(f"  cycles {len(ecal)} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  long-only beats SPY&EW both windows CAGR+Sharpe: {beats}; "
          f"spread sign +: {sign_ok}")
    if not floor:
        v = "INCONCLUSIVE"
    elif beats and sign_ok:
        v = "PROMISING (forward-only; PASS-HR/RA not claimable)"
    else:
        v = "FAIL (Reg SHO short-volume drift closed)"
    print(f"\n  X3 VERDICT: {v}")


if __name__ == "__main__":
    main()
