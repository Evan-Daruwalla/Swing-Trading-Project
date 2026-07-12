"""E19 - opportunistic insider-buy drift, per prereg ebf54a4.

Reads .edgar_cache/{ticker}.json (open-market P-buys from Form-4). Classifies
each buy routine vs opportunistic (CMP: routine = same calendar month in each
of the prior 3 years, per reporting owner); trades OPPORTUNISTIC buys only.
Enter next open after filing date, hold 40 sessions, K=5. Gate 2003-2013.
D1 dual-bar verdict + asymmetric framing (survivor => only a FAIL is clean).
Reuses .e8e9_cache prices; no swing.db writes.
"""
import bisect
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e10_earnings_drift import UNIV

EDGAR = Path("D:/ClaudeCode/Swing Trading/.edgar_cache")
K = 5
HOLD = 40
GATE = ("2003-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")


def classify_opportunistic(buys):
    """buys: list of dicts with owner,tdate. Return set of ids (index) that
    are OPPORTUNISTIC. Routine = owner bought same calendar month in each of
    prior 3 years."""
    by_owner = {}
    for i, b in enumerate(buys):
        if b.get("tdate") and b.get("owner"):
            by_owner.setdefault(b["owner"], []).append((b["tdate"], i))
    opp = set()
    for owner, lst in by_owner.items():
        months = {}                      # (year,month) present
        for tdate, i in lst:
            y, m = int(tdate[:4]), int(tdate[5:7])
            months.setdefault((y, m), []).append(i)
        for (y, m), idxs in months.items():
            routine = all((y - k, m) in months for k in (1, 2, 3))
            if not routine:
                opp.update(idxs)
    return opp


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mdd=float("nan"), sharpe=float("nan"))
    rets = [nav[i]/nav[i-1]-1 for i in range(1, len(nav)) if nav[i-1] > 0]
    yrs = len(nav)/252.0
    cagr = (nav[-1]/nav[0])**(1/yrs)-1 if nav[-1] > 0 else -1.0
    mu = sum(rets)/len(rets)
    sd = math.sqrt(sum((r-mu)**2 for r in rets)/(len(rets)-1))
    sh = mu/sd*math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak-v)/peak)
    return dict(cagr=cagr, mdd=mdd, sharpe=sh)


def main():
    missing = [t for t in UNIV if not (EDGAR / f"{t}.json").exists()]
    if missing:
        print(f"INGEST INCOMPLETE - missing {len(missing)}: {missing[:8]}...")
        print("Run scripts/ingest_edgar_form4.py to completion first.")
        return
    oc, tdates, events = {}, {}, []
    total_buys = total_opp = 0
    for t in UNIV:
        bars = cache_fetch(t)
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = [b[1] for b in bars]
        buys = json.loads((EDGAR / f"{t}.json").read_text())
        opp = classify_opportunistic(buys)
        total_buys += len(buys); total_opp += len(opp)
        dl = tdates[t]
        for i in opp:
            fd = buys[i].get("fdate")
            if not fd:
                continue
            j = bisect.bisect_right(dl, fd)        # first session AFTER filing
            if j >= len(dl):
                continue
            xi = j + HOLD
            events.append((dl[j], dl[xi] if xi < len(dl) else dl[-1], t))
    print(f"P-buys {total_buys}; opportunistic {total_opp}; "
          f"tradeable entries {len(events)}")

    master = sorted({d for t in UNIV for d in tdates[t] if d >= GATE[0]})
    ev_by_entry = {}
    for e in events:
        ev_by_entry.setdefault(e[0], []).append(e)

    cash, nav_prev = CAP0, CAP0
    pos, nav_by_date, last_close, entries_used = {}, {}, {}, []
    for d in master:
        for t in list(pos):
            if pos[t]["exit"] == d and d in oc[t]:
                cash += pos[t]["sh"] * oc[t][d][0] * (1 - COST); del pos[t]
        for (entry_d, exit_d, t) in sorted(ev_by_entry.get(d, []), key=lambda x: x[1]):
            if t not in pos and len(pos) < K and d in oc[t]:
                op = oc[t][d][0]
                size = min(cash, nav_prev / K)
                if size > 10.0 and op > 0:
                    sh = size / (op * (1 + COST)); cash -= size
                    pos[t] = dict(sh=sh, exit=exit_d); entries_used.append(d)
        for t in UNIV:
            if d in oc[t]:
                last_close[t] = oc[t][d][1]
        nav = cash + sum(p["sh"] * last_close.get(t, 0) for t, p in pos.items())
        nav_by_date[d] = nav; nav_prev = nav

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def win(lo, hi):
        return [nav_by_date[d] for d in master if lo <= d <= hi]

    def spybh(lo, hi):
        seg = [d for d in sorted(spy) if lo <= d <= hi]
        return stats([spy[d]/spy[seg[0]] for d in seg]) if seg else None

    rows = {}
    print(f"\n{'window':12}{'E19 CAGR':>10}{'maxDD':>8}{'Sharpe':>8}{'SPY CAGR':>10}{'SPY Sh':>8}")
    for wn, (lo, hi) in [("2003-2013", GATE), ("2014-", SEC)]:
        s = stats(win(lo, hi)); sp = spybh(lo, hi)
        rows[wn] = (s, sp)
        print(f"{wn:12}{s['cagr']*100:>9.2f}%{s['mdd']*100:>7.1f}%{s['sharpe']:>8.2f}"
              f"{sp['cagr']*100:>9.2f}%{sp['sharpe']:>8.2f}")

    g, gsp = rows["2003-2013"]; sec, ssp = rows["2014-"]
    n_gate = sum(1 for d in entries_used if GATE[0] <= d <= GATE[1])
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gsp["sharpe"]
          and sec["sharpe"] > ssp["sharpe"] and g["cagr"] > 0 and sec["cagr"] > 0)
    floor = n_gate >= 20
    print(f"\n=== D1 VERDICT (prereg ebf54a4; asymmetric: only FAIL clean) ===")
    print(f"  gate entries {n_gate} (>=20: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR (CAGR>=15% & DD<=60% both)")
    print(f"  [{'PASS' if ra else 'fail'}] PASS-RA (gate Sharpe>=0.80={g['sharpe']:.2f})")
    if not floor:
        v = "INCONCLUSIVE"
    elif hr or ra:
        v = f"{'PASS-HR' if hr else 'PASS-RA'} (UNINTERPRETABLE - survivorship; forward only)"
    else:
        v = "FAIL (clean - insider idea closed)"
    print(f"\n  E19 VERDICT: {v}")


if __name__ == "__main__":
    main()
