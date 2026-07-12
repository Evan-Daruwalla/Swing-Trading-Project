"""E16 - cross-sectional weekly reversal, per prereg a090294.

Each week-end, rank 39 survivor large-caps by trailing 5-session return,
buy the bottom 4 (biggest losers) at next open, full weekly rebalance,
5 bps/side, NAV/4. Survivor universe => asymmetric framing (only FAIL clean)
+ D1 tiers. Reuses .e8e9_cache; no swing.db writes.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted, div-UNADJUSTED.
"""
import datetime as dt
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e10_earnings_drift import UNIV

K = 4
LOOK = 5
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
FULL = ("2000-01-01", "2099-01-01")


def isoweek(d):
    y, m, dd = map(int, d.split("-"))
    iso = dt.date(y, m, dd).isocalendar()
    return (iso[0], iso[1])


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mo=float("nan"), mdd=float("nan"),
                    sharpe=float("nan"))
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1] > 0]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mo=(1 + cagr) ** (1 / 12) - 1, mdd=mdd, sharpe=sh)


def main():
    oc, tdates = {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = [b[1] for b in bars]
    master = sorted({d for t in UNIV for d in tdates[t]})
    idx = {t: {d: i for i, d in enumerate(tdates[t])} for t in UNIV}

    # week-end master sessions: next master session is a different iso week
    weekend = [master[i] for i in range(len(master) - 1)
               if isoweek(master[i]) != isoweek(master[i + 1])]
    weekend_set = set(weekend)

    cash, pos, pend = CAP0, {}, None
    nav_by_date, entries = {}, []
    for i, d in enumerate(master):
        if pend is not None:               # execute rebalance at this open
            navv = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
            for t in list(pos):
                if d in oc[t]:
                    cash += pos[t] * oc[t][d][0] * (1 - COST); del pos[t]
            per = navv / K
            for t in pend:
                if d in oc[t] and oc[t][d][0] > 0:
                    sh = per / (oc[t][d][0] * (1 + COST))
                    cash -= sh * oc[t][d][0] * (1 + COST); pos[t] = sh
                    entries.append(d)
            pend = None
        nav_by_date[d] = cash + sum(pos[t] * oc[t][d][1]
                                    for t in pos if d in oc[t])
        if d in weekend_set:
            rets = []
            for t in UNIV:
                if d in idx[t]:
                    j = idx[t][d]
                    if j >= LOOK:
                        base = oc[t][tdates[t][j - LOOK]][1]
                        if base > 0:
                            rets.append((oc[t][d][1] / base - 1, t))
            if len(rets) >= K:
                rets.sort()                # ascending: biggest losers first
                pend = [t for _, t in rets[:K]]

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}
    print(f"master {master[0]}..{master[-1]} ({len(master)}); "
          f"week-ends {len(weekend)}; entries {len(entries)}")
    rows = {}
    print(f"\n{'window':12}{'E16 CAGR':>10}{'%/mo':>8}{'maxDD':>8}{'Sharpe':>8}"
          f"{'EWuniv':>9}{'SPY':>8}")
    for wn, (s, e) in [("2000-2013", GATE), ("2014-", SEC), ("2000-", FULL)]:
        nav = [nav_by_date[d] for d in master if s <= d <= e]
        m = stats(nav)
        ewnav = []
        for d in master:
            if s <= d <= e:
                acc, kk = 0.0, 0
                for t in UNIV:
                    if d in oc[t]:
                        acc += oc[t][d][1] / oc[t][tdates[t][0]][1]; kk += 1
                if kk:
                    ewnav.append(acc / kk)
        msp = stats([spy[d] for d in sorted(spy) if s <= d <= e])
        rows[wn] = (m, msp)
        print(f"{wn:12}{m['cagr']*100:>9.2f}%{m['mo']*100:>7.2f}%"
              f"{m['mdd']*100:>7.1f}%{m['sharpe']:>8.2f}"
              f"{stats(ewnav)['cagr']*100:>8.2f}%{msp['cagr']*100:>7.2f}%")

    g, gsp = rows["2000-2013"]
    sec, secsp = rows["2014-"]
    n_gate = sum(1 for d in entries if GATE[0] <= d <= GATE[1])
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60
          and sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gsp["sharpe"]
          and sec["sharpe"] > secsp["sharpe"] and g["cagr"] > 0 and sec["cagr"] > 0)
    floor = n_gate >= 30
    print(f"\n=== D1 VERDICT (prereg a090294; asymmetric: only FAIL clean) ===")
    print(f"  gate entries {n_gate} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR (CAGR>=15% & DD<=60% both)")
    print(f"  [{'PASS' if ra else 'fail'}] PASS-RA (gate Sharpe>=0.80={g['sharpe']:.2f}"
          f" & >SPY both: {g['sharpe']:.2f}>{gsp['sharpe']:.2f},"
          f" {sec['sharpe']:.2f}>{secsp['sharpe']:.2f})")
    if not floor:
        verdict = "INCONCLUSIVE"
    elif hr or ra:
        verdict = f"{'PASS-HR' if hr else 'PASS-RA'} (UNINTERPRETABLE - biases; forward only)"
    else:
        verdict = "FAIL (clean - weekly reversal closed)"
    print(f"\n  E16 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
