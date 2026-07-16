"""C6 - even-week FOMC-cycle overlay (CMVJ 2019), per prereg
prereg_c6_fomc_cycle.md (committed doc-only before this runner).

Long SPY in FOMC-cycle even weeks (t in [0,4]|[10,14]|[20,24]|[30,34] sessions
since the latest scheduled announcement), flat otherwise (incl. t>34). Signal
close -> next open; 1 bp/side. Calendar: data/fomc_announcement_dates.json
(federalreserve.gov primary sources). D1 verdict. No swing.db writes.

DATA CONVENTION: SPY split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): imports run_e8_squeeze (CAP0, cache_fetch).
Imported by: no other module (standalone runner).
"""
import bisect
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, CAP0

GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
EVEN = [(0, 4), (10, 14), (20, 24), (30, 34)]
FOMC = json.loads((Path(__file__).resolve().parent.parent /
                   "data/fomc_announcement_dates.json").read_text())["dates"]


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
    bars = cache_fetch("SPY")
    dates = [b[1] for b in bars]
    op = [b[2] for b in bars]
    cl = [b[5] for b in bars]
    n = len(dates)
    # cycle position t per session: sessions since (incl.) latest announcement
    ann_idx = sorted({bisect.bisect_left(dates, a) for a in FOMC
                      if a <= dates[-1]})
    t_of = [None] * n
    for i in range(n):
        j = bisect.bisect_right(ann_idx, i) - 1
        if j >= 0:
            t_of[i] = i - ann_idx[j]
    even = [t is not None and any(lo <= t <= hi for lo, hi in EVEN)
            for t in t_of]

    def run(cost):
        cash, sh_, pend = CAP0, 0.0, None
        nav, toggles = [], 0
        for i in range(n):
            if pend is not None:
                if pend and sh_ == 0.0 and cash > 0:
                    sh_ = cash / (op[i] * (1 + cost)); cash = 0.0; toggles += 1
                elif not pend and sh_ > 0.0:
                    cash = sh_ * op[i] * (1 - cost); sh_ = 0.0; toggles += 1
                pend = None
            nav.append(cash + sh_ * cl[i])
            want = even[i + 1] if i + 1 < n else False
            if want and sh_ == 0.0:
                pend = True
            elif not want and sh_ > 0.0:
                pend = False
        return nav, toggles

    def win(series, lo, hi):
        return [v for d, v in zip(dates, series) if lo <= d <= hi]

    spy_bh = [c / cl[0] for c in cl]
    nav1, tog = run(0.0001)
    inmkt = 100.0 * sum(even) / n
    print(f"C6 FOMC even-week | SPY {dates[0]}..{dates[-1]}; {len(ann_idx)} "
          f"announcements mapped; exposure {inmkt:.1f}%; toggles {tog}\n")

    # CMVJ signature: mean daily close-to-close return, even vs odd cycle-weeks
    for wn, (lo, hi) in [("gate", GATE), ("sec", SEC), ("full 1994-", ("1994-01-01", "2099-12-31"))]:
        ev, od = [], []
        for i in range(1, n):
            if not (lo <= dates[i] <= hi) or t_of[i] is None:
                continue
            r = cl[i] / cl[i - 1] - 1
            (ev if even[i] else od).append(r)
        me = sum(ev) / len(ev) * 1e4 if ev else float("nan")
        mo = sum(od) / len(od) * 1e4 if od else float("nan")
        print(f"  {wn:12} mean daily ret: even-week {me:+6.2f}bps ({len(ev)}d)  "
              f"odd-week {mo:+6.2f}bps ({len(od)}d)")

    rows = {}
    print(f"\n  {'window':14}{'C6 CAGR':>9}{'maxDD':>8}{'Sharpe':>8}{'SPY CAGR':>10}{'SPY Sh':>8}")
    for wn, (lo, hi) in [("2000-2013", GATE), ("2014-", SEC)]:
        s = stats(win(nav1, lo, hi)); b = stats(win(spy_bh, lo, hi))
        rows[wn] = (s, b)
        print(f"  {wn:14}{s['cagr']*100:>8.2f}%{s['mdd']*100:>7.1f}%{s['sharpe']:>8.2f}"
              f"{b['cagr']*100:>9.2f}%{b['sharpe']:>8.2f}")
    for cst, lab in [(0.0005, "5bp"), (0.0015, "15bp")]:
        navs, _ = run(cst)
        s = stats(win(navs, *GATE))
        print(f"  stress {lab}: gate CAGR {s['cagr']*100:.2f}% Sh {s['sharpe']:.2f}")

    g, gb = rows["2000-2013"]; s, sb = rows["2014-"]
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gb["sharpe"] and s["sharpe"] > sb["sharpe"]
          and g["cagr"] > 0 and s["cagr"] > 0)
    floor = tog >= 30
    print(f"\n=== D1 VERDICT (prereg prereg_c6_fomc_cycle.md) ===")
    print(f"  toggles {tog} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR   [{'PASS' if ra else 'fail'}] "
          f"PASS-RA (gate Sharpe {g['sharpe']:.2f} vs SPY {gb['sharpe']:.2f})")
    v = ("INCONCLUSIVE" if not floor else "PASS-HR" if hr else "PASS-RA" if ra
         else "FAIL (FOMC even-week overlay closed)")
    print(f"\n  C6 VERDICT: {v}")


if __name__ == "__main__":
    main()
