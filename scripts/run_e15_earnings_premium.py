"""E15 - earnings-announcement premium, per prereg 9b0aeb3.

Buy at open 5 sessions before each scheduled announcement, sell at open the
session after it; K=5; 5 bps/side. Survivor large-caps + scheduled-date
lookahead => asymmetric framing (only a FAIL is clean) on top of the D1
dual-bar verdict. Reuses E10 earnings-date + OHLCV cache; no swing.db writes.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted, div-UNADJUSTED.
"""
import bisect
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e10_earnings_drift import earnings_dates, UNIV

K = 5
PRE = 5           # buy 5 sessions before the announcement session
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
FULL = ("2000-01-01", "2099-01-01")


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
    oc, tdates, events = {}, {}, []
    n_ann = 0
    for t in UNIV:
        bars = cache_fetch(t)
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = [b[1] for b in bars]
        ed = earnings_dates(t)
        n_ann += len(ed)
        dl = tdates[t]
        for E in ed:
            a = bisect.bisect_left(dl, E)       # first session with date >= E
            if a >= len(dl):
                continue
            ei, xi = a - PRE, a + 1
            if ei < 0 or xi >= len(dl):
                continue
            events.append((dl[ei], dl[xi], t))
        print(f"loaded {t}: {len(bars)} bars, {len(ed)} earnings", flush=True)
    print(f"\ntotal announcements {n_ann}; window-valid events {len(events)}")

    master = sorted({d for t in UNIV for d in tdates[t] if d >= GATE[0]})
    ev_by_entry = {}
    for e in events:
        ev_by_entry.setdefault(e[0], []).append(e)

    cash, nav_prev = CAP0, CAP0
    pos, nav_by_date, last_close, trades = {}, {}, {}, []
    entries_used = []
    for d in master:
        # exits first (free capital)
        for t in list(pos):
            if pos[t]["exit_d"] == d and d in oc[t]:
                op = oc[t][d][0]
                p = pos.pop(t)
                cash += p["sh"] * op * (1 - COST)
                trades.append((t, p["fill"], op))
        # entries (earliest-exit-first so we don't starve; ties by ticker)
        for (entry_d, exit_d, t) in sorted(ev_by_entry.get(d, []),
                                           key=lambda x: (x[1], x[2])):
            if t not in pos and len(pos) < K and d in oc[t]:
                op = oc[t][d][0]
                size = min(cash, nav_prev / K)
                if size > 10.0 and op > 0:
                    sh = size / (op * (1 + COST))
                    cash -= size
                    pos[t] = dict(sh=sh, fill=op, exit_d=exit_d)
                    entries_used.append(d)
        for t in UNIV:
            if d in oc[t]:
                last_close[t] = oc[t][d][1]
        nav = cash + sum(p["sh"] * last_close.get(t, p["fill"])
                         for t, p in pos.items())
        nav_by_date[d] = nav; nav_prev = nav

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}
    wins = sum(1 for (t, f, x) in trades if x > f)
    print(f"closed trades {len(trades)}; win {100*wins/max(1,len(trades)):.1f}%")

    rows = {}
    ewrows = {}          # EX-DECOMP hook (M9 #44): honest null = EW-survivor-univ
    print(f"\n{'window':12}{'E15 CAGR':>10}{'%/mo':>8}{'maxDD':>8}{'Sharpe':>8}"
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
        mew = stats(ewnav)
        msp = stats([spy[d] for d in sorted(spy) if s <= d <= e])
        rows[wn] = (m, msp)
        ewrows[wn] = (m, mew)
        print(f"{wn:12}{m['cagr']*100:>9.2f}%{m['mo']*100:>7.2f}%"
              f"{m['mdd']*100:>7.1f}%{m['sharpe']:>8.2f}"
              f"{mew['cagr']*100:>8.2f}%{msp['cagr']*100:>7.2f}%")

    g, gsp = rows["2000-2013"]
    sec, secsp = rows["2014-"]
    n_gate = sum(1 for d in entries_used if GATE[0] <= d <= GATE[1])
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60
          and sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gsp["sharpe"]
          and sec["sharpe"] > secsp["sharpe"] and g["cagr"] > 0 and sec["cagr"] > 0)
    floor = n_gate >= 20
    print(f"\n=== D1 VERDICT (prereg 9b0aeb3; asymmetric: only a FAIL is clean) ===")
    print(f"  gate entries {n_gate} (>=20: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR (CAGR>=15% & DD<=60% both)")
    print(f"  [{'PASS' if ra else 'fail'}] PASS-RA (gate Sharpe>=0.80={g['sharpe']:.2f} "
          f"& >SPY both: {g['sharpe']:.2f}>{gsp['sharpe']:.2f}, "
          f"{sec['sharpe']:.2f}>{secsp['sharpe']:.2f})")
    if not floor:
        verdict = "INCONCLUSIVE"
    elif hr or ra:
        verdict = f"{'PASS-HR' if hr else 'PASS-RA'} (UNINTERPRETABLE - biases; forward only)"
    else:
        verdict = "FAIL (clean - earnings premium closed)"
    print(f"\n  E15 VERDICT: {verdict}")
    return {"rows": ewrows, "n_gate": n_gate, "bench": "EW-univ"}


if __name__ == "__main__":
    main()
