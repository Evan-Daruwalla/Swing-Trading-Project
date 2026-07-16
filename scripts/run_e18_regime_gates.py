"""E18 - regime-gate bake-off, per prereg f32b008.

Four a-priori risk-on/off gates as drawdown overlays on a 1x QQQ sleeve:
(a) VIX/VIX3M<1 (2006+), (b) HY-OAS<trailing-252d-median, (c) breadth>=50%
of 29-ETF universe above 200DMA, (d) QQQ>200DMA (E6 benchmark). Compared to
QQQ buy-hold; E6 overlay criteria (maxDD cut>=10pp AND Sharpe>=BH both
windows) + D1 tiers. Signal at close, next-open, 5bps. No swing.db writes.

DATA: QQQ/ETFs from .e8e9_cache; ^VIX/^VIX3M via yfinance (cached);
HY-OAS BAMLH0A0HYM2 via FRED keyless CSV (cached). auto_adjust=False.

NAV (finding-things map): SHARED-HELPER HUB. Its `macro_close`, `sma`, `stats`
are imported by run_m10_1_nagel_switch, run_x7_credit_gate, run_c4_vol_sizing,
run_c7_svxy_carry, run_x1_vol_targeting, run_m10_2 — edit them with care.
Shared price data via `cache_fetch` <- run_e8_squeeze; universe via
swing_bot.universe.UNIVERSE. LIVE forward-paper twin:
swing_bot.paper_sleeves.decide_e18_vixts mirrors arm (a) VIX/VIX3M<1.
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
import httpx
import yfinance as yf

GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")


def macro_close(sym):
    """yfinance index close series -> {date: close}, cached."""
    f = CACHE / f"{sym.replace('^','')}_idx.json"
    if f.exists():
        return json.loads(f.read_text())
    for attempt in range(4):
        try:
            d = yf.download(sym, period="max", auto_adjust=False,
                            progress=False)
            if not d.empty:
                if d.columns.nlevels == 2:
                    d.columns = d.columns.droplevel(1)
                out = {ts.strftime("%Y-%m-%d"): float(c)
                       for ts, c in d["Close"].items() if c == c}
                f.write_text(json.dumps(out))
                return out
        except Exception as e:
            print(f"  {sym} attempt {attempt+1}: {type(e).__name__}", flush=True)
        time.sleep(15 * (attempt + 1))
    raise RuntimeError(f"could not fetch {sym}")


def fred_series(sid):
    f = CACHE / f"fred_{sid}.json"
    if f.exists():
        return json.loads(f.read_text())
    r = httpx.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
                  f"&cosd=1996-01-01", timeout=60, follow_redirects=True)
    out = {}
    for line in r.text.strip().splitlines()[1:]:
        d, v = line.split(",")
        if v not in (".", ""):
            out[d] = float(v)
    f.write_text(json.dumps(out))
    return out


def sma(series, n):
    out = [None] * len(series)
    for i in range(n - 1, len(series)):
        out[i] = sum(series[i - n + 1:i + 1]) / n
    return out


def overlay_nav(dates, op, cl, risk_on, start_i):
    """Long QQQ when risk_on[t] (decided at close t, executed t+1 open)."""
    cash, sh, pend = CAP0, 0.0, None
    nav = {}
    offs = 0
    for i in range(start_i, len(dates)):
        if pend is not None:
            if pend == 1 and sh == 0.0 and op[i] > 0:
                sh = cash / (op[i] * (1 + COST)); cash = 0.0
            elif pend == 0 and sh > 0.0:
                cash = sh * op[i] * (1 - COST); sh = 0.0
            pend = None
        nav[dates[i]] = cash + sh * cl[i]
        want = risk_on[i]
        if want is None:
            continue
        if want and sh == 0.0 and cash > 0:
            pend = 1
        elif (not want) and sh > 0.0:
            pend = 0
    return nav


def stats(nav_list):
    if len(nav_list) < 30 or nav_list[0] <= 0:
        return None
    rets = [nav_list[i] / nav_list[i-1] - 1 for i in range(1, len(nav_list))
            if nav_list[i-1] > 0]
    yrs = len(nav_list) / 252.0
    cagr = (nav_list[-1] / nav_list[0]) ** (1/yrs) - 1 if nav_list[-1] > 0 else -1.0
    mu = sum(rets)/len(rets)
    sd = math.sqrt(sum((r-mu)**2 for r in rets)/(len(rets)-1))
    sh = mu/sd*math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav_list[0], 0.0
    for v in nav_list:
        peak = max(peak, v); mdd = max(mdd, (peak-v)/peak)
    return dict(cagr=cagr, mdd=mdd, sharpe=sh)


def main():
    qb = cache_fetch("QQQ")
    dates = [b[1] for b in qb]
    op = [b[2] for b in qb]
    cl = [b[5] for b in qb]
    idxq = {d: i for i, d in enumerate(dates)}
    sma200 = sma(cl, 200)

    vix = macro_close("^VIX")
    vix3m = macro_close("^VIX3M")
    oas = fred_series("BAMLH0A0HYM2")

    # HY-OAS forward-filled to QQQ dates + trailing 252d median
    oas_ff, last = [], None
    for d in dates:
        if d in oas:
            last = oas[d]
        oas_ff.append(last)
    oas_med = [None]*len(dates)
    for i in range(len(dates)):
        w = [x for x in oas_ff[max(0, i-251):i+1] if x is not None]
        if len(w) >= 200:
            s = sorted(w); oas_med[i] = s[len(s)//2]

    # breadth: % of 29-ETF universe above own 200DMA
    etf_cl, etf_sma = {}, {}
    for e in UNIVERSE:
        b = cache_fetch(e.ticker)
        c = {bb[1]: bb[5] for bb in b}
        cs = [bb[5] for bb in b]
        sm = sma(cs, 200)
        etf_cl[e.ticker] = c
        etf_sma[e.ticker] = {b[i][1]: sm[i] for i in range(len(b))}
    breadth = []
    for d in dates:
        above = tot = 0
        for e in UNIVERSE:
            s = etf_sma[e.ticker].get(d)
            c = etf_cl[e.ticker].get(d)
            if s is not None and c is not None:
                tot += 1
                if c > s:
                    above += 1
        breadth.append(above/tot if tot else None)

    # gate risk-on arrays (index-aligned to QQQ dates)
    gates = {}
    gates["(a) VIX-TS<1"] = [
        (vix.get(d)/vix3m[d] < 1.0) if (d in vix and d in vix3m and vix3m[d] > 0)
        else None for d in dates]
    gates["(b) HY-OAS<med"] = [
        (oas_ff[i] < oas_med[i]) if (oas_ff[i] is not None and oas_med[i] is not None)
        else None for i in range(len(dates))]
    gates["(c) breadth>=50%"] = [
        (breadth[i] >= 0.5) if breadth[i] is not None else None
        for i in range(len(dates))]
    gates["(d) QQQ>200DMA"] = [
        (cl[i] > sma200[i]) if sma200[i] is not None else None
        for i in range(len(dates))]

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def win(nav, lo, hi):
        return [nav[d] for d in dates if lo <= d <= hi and d in nav]

    def bh(series_dates, lo, hi):
        seg = [d for d in series_dates if lo <= d <= hi]
        if not seg:
            return None
        base = cl[idxq[seg[0]]]
        return stats([cl[idxq[d]]/base for d in seg])

    def spybh(lo, hi):
        seg = [d for d in sorted(spy) if lo <= d <= hi]
        return stats([spy[d]/spy[seg[0]] for d in seg]) if seg else None

    print(f"QQQ {dates[0]}..{dates[-1]} ({len(dates)}); VIX3M from "
          f"{min(vix3m)}, OAS from {min(oas)}\n")
    print(f"{'gate':18}{'window':11}{'CAGR':>8}{'maxDD':>8}{'Sharpe':>8}"
          f"{'BH maxDD':>10}{'BH Sh':>7}{'  overlay-ok'}")
    summary = {}
    for name, ro in gates.items():
        start_i = next((i for i in range(len(dates)) if ro[i] is not None), 0)
        nav = overlay_nav(dates, op, cl, ro, start_i)
        gate_lo = "2006-01-01" if name.startswith("(a)") else GATE[0]
        res = {}
        for wn, (lo, hi) in [("gate", (gate_lo, GATE[1])), ("secondary", SEC)]:
            s = stats(win(nav, lo, hi))
            b = bh(dates, lo, hi)
            if s and b:
                ok = (b["mdd"] - s["mdd"] >= 0.10) and (s["sharpe"] >= b["sharpe"])
                res[wn] = (s, b, ok)
                print(f"{name:18}{wn:11}{s['cagr']*100:>7.2f}%{s['mdd']*100:>7.1f}%"
                      f"{s['sharpe']:>8.2f}{b['mdd']*100:>9.1f}%{b['sharpe']:>7.2f}"
                      f"{'   YES' if ok else '   no'}")
        summary[name] = res
        print()

    print("=== BAKE-OFF (E6 overlay criteria: maxDD cut>=10pp AND Sharpe>=BH, both windows) ===")
    winner = None
    for name, res in summary.items():
        both = all(res.get(w, (None, None, False))[2] for w in ("gate", "secondary"))
        d_sh = summary["(d) QQQ>200DMA"].get("gate", (None,))[0]
        beats_d = (res.get("gate") and d_sh and res["gate"][0]["sharpe"] > d_sh["sharpe"])
        print(f"  {name:18} overlay-ok both windows: {'YES' if both else 'no'}"
              f"{'  (beats 200DMA on gate Sharpe)' if beats_d and name != '(d) QQQ>200DMA' else ''}")
        if both and name != "(d) QQQ>200DMA" and beats_d:
            winner = name
    # D1 RA check for the benchmark and any winner
    print("\n=== D1 PASS-RA check (gate Sharpe>=0.80 AND >SPY both AND +CAGR both) ===")
    for name in gates:
        res = summary[name]
        if "gate" in res and "secondary" in res:
            g = res["gate"][0]; sec = res["secondary"][0]
            gate_lo = "2006-01-01" if name.startswith("(a)") else GATE[0]
            gsp = spybh(gate_lo, GATE[1]); ssp = spybh(*SEC)
            ra = (g["sharpe"] >= 0.80 and gsp and g["sharpe"] > gsp["sharpe"]
                  and ssp and sec["sharpe"] > ssp["sharpe"]
                  and g["cagr"] > 0 and sec["cagr"] > 0)
            print(f"  {name:18} PASS-RA: {'PASS' if ra else 'fail'} "
                  f"(gate Sharpe {g['sharpe']:.2f})")
    print(f"\n  E18 BAKE-OFF WINNER: {winner if winner else 'NONE beats the plain 200-DMA overlay'}")


if __name__ == "__main__":
    main()
