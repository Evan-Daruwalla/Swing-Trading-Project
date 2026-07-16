"""E20 - dividend capture, per prereg d0642ad.

Buy close before ex-date, sell ex-date open, credit the dividend. Per-trade
net = (openE-closePrior)/closePrior + D/closePrior - 2*5bps. Equal-weight
across same-day ex-dates; 1-session holds; compound. D1 verdict + the real
question: mean net per-trade return. Reuses .e8e9_cache; no swing.db writes.

DATA: ETF OHLCV + dividends via yfinance (div-UNADJ closes; dividend credited
explicitly). auto_adjust=False.

NAV (finding-things map): imports run_e8_squeeze (CACHE, CAP0, COST,
cache_fetch); swing_bot.universe (UNIVERSE). Imported by: run_ex_decomp.py.
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
from run_e8_squeeze import cache_fetch, CACHE, COST, CAP0
from swing_bot.universe import UNIVERSE
import yfinance as yf

GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")


def divs(ticker):
    f = CACHE / f"{ticker}_div.json"
    if f.exists():
        return json.loads(f.read_text())
    for attempt in range(4):
        try:
            s = yf.Ticker(ticker).dividends
            out = {ts.strftime("%Y-%m-%d"): float(v) for ts, v in s.items()
                   if v == v and v > 0}
            f.write_text(json.dumps(out))
            return out
        except Exception as e:
            print(f"  {ticker} div attempt {attempt+1}: {type(e).__name__}",
                  flush=True)
        time.sleep(12 * (attempt + 1))
    return {}


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
    by_entry = {}          # entry_date -> list of (ticker, net_ret)
    n_trades = 0
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        oc = {b[1]: (b[2], b[5]) for b in bars}
        dl = [b[1] for b in bars]
        di = {d: i for i, d in enumerate(dl)}
        for exd, amt in divs(e.ticker).items():
            if exd not in di:
                continue
            j = di[exd]
            if j == 0:
                continue
            prior = dl[j - 1]
            p0 = oc[prior][1]              # close before ex
            p1 = oc[exd][0]               # open on ex-date
            if p0 <= 0:
                continue
            net = (p1 - p0) / p0 + amt / p0 - 2 * COST
            by_entry.setdefault(prior, []).append((e.ticker, net))
            n_trades += 1

    master = sorted(set().union(*[set(cache_fetch(e.ticker) and
                    [b[1] for b in cache_fetch(e.ticker)]) for e in UNIVERSE]))
    # daily strat return realized on entry date = mean of that day's captures
    nav_by_date, nav = {}, CAP0
    all_net = []
    for d in master:
        r = 0.0
        if d in by_entry:
            rs = [x[1] for x in by_entry[d]]
            r = sum(rs) / len(rs)
            all_net.extend(rs)
        nav *= (1 + r)
        nav_by_date[d] = nav

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def win(lo, hi):
        return [nav_by_date[d] for d in master if lo <= d <= hi]

    def spybh(lo, hi):
        seg = [d for d in sorted(spy) if lo <= d <= hi]
        return stats([spy[d]/spy[seg[0]] for d in seg]) if seg else None

    print(f"capture trades: {n_trades}; mean net/trade "
          f"{100*sum(all_net)/len(all_net):.4f}%; "
          f"win {100*sum(1 for x in all_net if x>0)/len(all_net):.1f}%")
    rows = {}
    for wn, (lo, hi) in [("2000-2013", GATE), ("2014-", SEC)]:
        s = stats(win(lo, hi))
        rows[wn] = s
        nt = sum(1 for d in by_entry if lo <= d <= hi for _ in by_entry[d])
        print(f"{wn:12} CAGR {s['cagr']*100:.2f}%  maxDD {s['mdd']*100:.1f}%  "
              f"Sharpe {s['sharpe']:.2f}  trades {nt}")

    g, sec = rows["2000-2013"], rows["2014-"]
    gsp, ssp = spybh(*GATE), spybh(*SEC)
    n_gate = sum(1 for d in by_entry if GATE[0] <= d <= GATE[1] for _ in by_entry[d])
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60
          and sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and gsp and g["sharpe"] > gsp["sharpe"]
          and ssp and sec["sharpe"] > ssp["sharpe"] and g["cagr"] > 0 and sec["cagr"] > 0)
    floor = n_gate >= 30
    print(f"\n=== D1 VERDICT (prereg d0642ad) ===")
    print(f"  gate trades {n_gate} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR (CAGR>=15% & DD<=60% both)")
    print(f"  [{'PASS' if ra else 'fail'}] PASS-RA (gate Sharpe>=0.80={g['sharpe']:.2f})")
    verdict = ("INCONCLUSIVE" if not floor else
               "PASS-HR" if hr else "PASS-RA" if ra else "FAIL")
    print(f"\n  E20 VERDICT: {verdict}")
    print(f"  (the real question) mean net per-trade after cost: "
          f"{100*sum(all_net)/len(all_net):+.4f}% -> "
          f"{'positive edge' if sum(all_net) > 0 else 'no edge / negative'}")


if __name__ == "__main__":
    main()
