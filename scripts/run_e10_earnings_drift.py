"""E10 - post-earnings-announcement drift (PEAD), per prereg 129dc22.
FALSIFICATION-ONLY (E3 framing): survivor large-caps, biases can only help,
only a FAIL is clean. On each earnings announcement, if the price reaction
(first full session after the announcement, close-over-prior-close) >= +3%,
buy next open and hold 40 trading days. K=3, 5bps/side. Gate 2000-2013
CAGR>=15% & maxDD<=65%, n>=20. No tuning. Does NOT touch swing.db.

DATA: earnings dates via yfinance get_earnings_dates(limit=100) (~2001 on;
announcement dates are historical fact; estimate/surprise cols NOT used).
OHLCV auto_adjust=False (split-adj, div-UNADJ). Caches to .e8e9_cache.

NAV (finding-things map): imports run_e8_squeeze (CACHE, cache_fetch).
Imported by: daily_swing_paper.py, run_c1_residual_reversal.py,
run_e15_earnings_premium.py, run_e16_weekly_reversal.py, run_e19_insider.py,
run_m10_1_nagel_switch.py, run_m11_chart_patterns.py, run_x3_regsho_svr.py.
"""
import json
import math
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, CACHE
import pandas as pd
import yfinance as yf

UNIV = ("MSFT INTC CSCO ORCL IBM AAPL QCOM TXN ADBE JPM BAC WFC C GS AXP "
        "XOM CVX COP SLB PG KO PEP WMT MCD HD NKE DIS JNJ PFE MRK ABT UNH "
        "GE CAT BA MMM HON T VZ").split()
K = 3
COST = 5.0 / 10000.0
CAP0 = 1000.0
HOLD = 40
REACT = 0.03
SIM_START = "2000-01-01"
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
FULL = ("2000-01-01", "2099-01-01")


def earnings_dates(ticker):
    f = CACHE / f"{ticker}_earn.json"
    if f.exists():
        return json.loads(f.read_text())
    for attempt in range(4):
        try:
            ed = yf.Ticker(ticker).get_earnings_dates(limit=100)
            if ed is not None and len(ed):
                now = pd.Timestamp.now(tz=ed.index.tz)
                out = sorted({d.strftime("%Y-%m-%d")
                              for d in ed.index if d < now})
                f.write_text(json.dumps(out))
                return out
        except Exception as e:
            print(f"  {ticker} earn attempt {attempt+1}: {type(e).__name__}",
                  flush=True)
        time.sleep(15 * (attempt + 1))
    print(f"  {ticker}: NO earnings dates", flush=True)
    return []


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
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}      # date->(open,close)
        tdates[t] = [b[1] for b in bars]
        ed = earnings_dates(t)
        n_ann += len(ed)
        dl, di = tdates[t], {d: i for i, d in enumerate(tdates[t])}
        for E in ed:
            # r = first ticker session strictly after the announcement date
            import bisect
            j = bisect.bisect_right(dl, E)
            if j <= 0 or j >= len(dl):
                continue
            r, prev = dl[j], dl[j - 1]
            cr, cp = oc[t][r][1], oc[t][prev][1]
            if cp <= 0:
                continue
            reaction = cr / cp - 1
            if reaction >= REACT and j + 1 < len(dl):
                exec_d = dl[j + 1]
                ex_i = j + 1 + HOLD
                exit_d = dl[ex_i] if ex_i < len(dl) else dl[-1]
                events.append((exec_d, exit_d, t, reaction))
        print(f"loaded {t}: {len(bars)} bars, {len(ed)} past earnings",
              flush=True)
    print(f"\ntotal announcements {n_ann}; qualifying entries (>= {REACT:.0%} "
          f"reaction): {len(events)}")

    master = sorted({d for t in UNIV for d in tdates[t] if d >= SIM_START})
    ev_by_exec = {}
    for e in events:
        ev_by_exec.setdefault(e[0], []).append(e)

    cash, nav_prev = CAP0, CAP0
    pos = {}                    # ticker -> dict(sh, fill, exit_d)
    nav_by_date, last_close, trades = {}, {}, []
    for d in master:
        for t in list(pos):
            if pos[t]["exit_d"] == d and d in oc[t]:
                op = oc[t][d][0]
                p = pos.pop(t)
                cash += p["sh"] * op * (1 - COST)
                trades.append((t, p["fill"], op))
        for (exec_d, exit_d, t, reaction) in sorted(
                ev_by_exec.get(d, []), key=lambda x: -x[3]):
            if t not in pos and len(pos) < K and d in oc[t]:
                op = oc[t][d][0]
                size = min(cash, nav_prev / K)
                if size > 10.0 and op > 0:
                    sh = size / (op * (1 + COST))
                    cash -= size
                    pos[t] = dict(sh=sh, fill=op, exit_d=exit_d)
        for t in UNIV:
            if d in oc[t]:
                last_close[t] = oc[t][d][1]
        nav = cash + sum(p["sh"] * last_close.get(t, p["fill"])
                         for t, p in pos.items())
        nav_by_date[d] = nav; nav_prev = nav

    spy_bars = cache_fetch("SPY")
    spy = {b[1]: b[5] for b in spy_bars}
    wins = sum(1 for (t, f, x) in trades if x > f)
    print(f"closed trades {len(trades)}; win {100*wins/max(1,len(trades)):.1f}%")
    print(f"\n{'window':12}{'E10 CAGR':>10}{'%/mo':>8}{'maxDD':>8}{'Sharpe':>8}"
          f"{'EWuniv':>9}{'SPY':>8}")
    res = {}
    for wn, (s, e) in [("2000-2013", GATE), ("2014-", SEC), ("2000-", FULL)]:
        nav = [nav_by_date[d] for d in master if s <= d <= e]
        m = stats(nav)
        res[wn] = m
        ewnav = []
        for d in master:
            if s <= d <= e:
                acc, k = 0.0, 0
                for t in UNIV:
                    if d in oc[t]:
                        acc += oc[t][d][1] / oc[t][tdates[t][0]][1]; k += 1
                if k:
                    ewnav.append(acc / k)
        mew = stats(ewnav)
        msp = stats([spy[d] for d in sorted(spy) if s <= d <= e])
        print(f"{wn:12}{m['cagr']*100:>9.2f}%{m['mo']*100:>7.2f}%"
              f"{m['mdd']*100:>7.1f}%{m['sharpe']:>8.2f}"
              f"{mew['cagr']*100:>8.2f}%{msp['cagr']*100:>7.2f}%")

    g = res["2000-2013"]
    n_gate = sum(1 for (exec_d, _, _, _) in events if GATE[0] <= exec_d <= GATE[1])
    g1 = g["cagr"] >= 0.15
    g2 = g["mdd"] <= 0.65
    g3 = n_gate >= 20
    print(f"\n=== KILL CRITERIA (2000-2013 gate; prereg 129dc22) ===")
    print(f"  [{'PASS' if g1 else 'FAIL'}] CAGR>=15% ({g['cagr']*100:.2f}%)")
    print(f"  [{'PASS' if g2 else 'FAIL'}] maxDD<=65% ({g['mdd']*100:.1f}%)")
    print(f"  [{'OK' if g3 else 'INCONCLUSIVE'}] gate entries>=20 ({n_gate})")
    verdict = ("INCONCLUSIVE" if not g3 else
               ("PASS (UNINTERPRETABLE - biases; forward only)" if (g1 and g2)
                else "FAIL (clean - PEAD closed)"))
    print(f"\n  E10 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
