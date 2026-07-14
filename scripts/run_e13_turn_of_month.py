"""E13 - turn-of-the-month overlay, per prereg 0324196.

Long SPY on TOM-days (last trading day of month + first 3 of next), cash
otherwise; signal at close, execute next open; 5 bps/side. D1 dual-bar
verdict (PASS-HR / PASS-RA / FAIL). Reuses .e8e9_cache; no swing.db writes.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted,
dividend-UNADJUSTED.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0

GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
FULL = ("2000-01-01", "2099-01-01")


def tom_flags(dates):
    """TOM-day = last trading day of its month OR first 3 trading days."""
    n = len(dates)
    month = [d[:7] for d in dates]
    flags = [False] * n
    cnt = 0
    for i in range(n):
        if i == 0 or month[i] != month[i - 1]:
            cnt = 1
        else:
            cnt += 1
        is_first3 = cnt <= 3
        is_last = (i == n - 1) or (month[i + 1] != month[i])
        flags[i] = is_first3 or is_last
    return flags


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return None
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav))]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mo=(1 + cagr) ** (1 / 12) - 1, mdd=mdd, sharpe=sh)


def main():
    bars = cache_fetch("SPY")
    dates = [b[1] for b in bars]
    op = [b[2] for b in bars]
    cl = [b[5] for b in bars]
    tom = tom_flags(dates)
    n = len(dates)

    cash, sh, pend, days_in = CAP0, 0.0, None, 0
    nav = []
    buys = []          # (date) of entries for trade counting
    for i in range(n):
        if pend is not None:
            if pend == 1 and sh == 0.0:
                sh = cash / (op[i] * (1 + COST)); cash = 0.0; buys.append(dates[i])
            elif pend == 0 and sh > 0.0:
                cash = sh * op[i] * (1 - COST); sh = 0.0
            pend = None
        nav.append(cash + sh * cl[i])
        if sh > 0.0:
            days_in += 1
        want = tom[i + 1] if i + 1 < n else False
        if want and sh == 0.0 and cash > 0:
            pend = 1
        elif (not want) and sh > 0.0:
            pend = 0

    spy_nav = [c / cl[0] for c in cl]

    def window(series, lo, hi):
        return [v for d, v in zip(dates, series) if lo <= d <= hi]

    print(f"SPY {dates[0]}..{dates[-1]} ({n} bars); in-market {days_in}/{n} "
          f"({100*days_in/n:.1f}%); round-trips {len(buys)}")
    rows = {}
    for name, (lo, hi) in [("GATE 2000-2013", GATE), ("SECONDARY 2014-", SEC),
                           ("FULL 2000-", FULL)]:
        s = stats(window(nav, lo, hi))
        b = stats(window(spy_nav, lo, hi))
        rows[name] = (s, b)
        nb = sum(1 for d in buys if lo <= d <= hi)
        print(f"\n{name}: E13 CAGR {s['cagr']*100:.2f}% ({s['mo']*100:.2f}%/mo) "
              f"maxDD {s['mdd']*100:.1f}% Sharpe {s['sharpe']:.2f} | "
              f"SPY-BH CAGR {b['cagr']*100:.2f}% Sharpe {b['sharpe']:.2f} | "
              f"round-trips {nb}")

    g, gb = rows["GATE 2000-2013"]
    sec, secb = rows["SECONDARY 2014-"]
    n_gate = sum(1 for d in buys if GATE[0] <= d <= GATE[1])
    # PASS-HR
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60
          and sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60)
    # PASS-RA
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gb["sharpe"]
          and sec["sharpe"] > secb["sharpe"]
          and g["cagr"] > 0 and sec["cagr"] > 0)
    floor = n_gate >= 30
    print(f"\n=== D1 VERDICT (prereg 0324196) ===")
    print(f"  gate round-trips {n_gate} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR: CAGR>=15% & maxDD<=60% both windows")
    print(f"  [{'PASS' if ra else 'fail'}] PASS-RA: gate Sharpe>=0.80 ({g['sharpe']:.2f}) "
          f"& > SPY both ({g['sharpe']:.2f}>{gb['sharpe']:.2f}, "
          f"{sec['sharpe']:.2f}>{secb['sharpe']:.2f}) & CAGR>0 both")
    verdict = ("INCONCLUSIVE" if not floor else
               "PASS-HR" if hr else "PASS-RA" if ra else "FAIL")
    print(f"\n  E13 VERDICT: {verdict}")
    # EX-DECOMP hook (M9 #44): benchmark = SPY-BH (rows[*][1]); additive only.
    return {"rows": rows, "n_gate": n_gate, "bench": "SPY-BH"}


if __name__ == "__main__":
    main()
