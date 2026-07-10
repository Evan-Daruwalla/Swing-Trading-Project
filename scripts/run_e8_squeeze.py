"""E8 — volatility-compression breakout (squeeze), per prereg 9b49190.

Long-only breakout after >=5-session BB-inside-Keltner squeeze, K=3,
exit on close<EMA20 or 40-bar max hold. Gate window 2000-2013:
CAGR>=15% AND maxDD<=60%, n_trades>=30. No tuning after results.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted,
dividend-UNADJUSTED. Fetched live from inception; does NOT touch swing.db
(protects frozen-regression refs). Cache in scratchpad only.
"""
import json
import math
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices
from swing_bot.universe import UNIVERSE

CACHE = Path(os.environ.get("E8E9_CACHE",
    Path(__file__).resolve().parent.parent / ".e8e9_cache"))
K = 3
COST = 5.0 / 10000.0
CAP0 = 1000.0
MAX_HOLD = 40
SQUEEZE_MIN = 5
SIM_START = "2000-01-01"
GATE_END = "2013-12-31"
SEC_START = "2014-01-01"


def cache_fetch(ticker):
    CACHE.mkdir(exist_ok=True)
    f = CACHE / f"{ticker}.json"
    if f.exists():
        return json.loads(f.read_text())
    for attempt in range(4):
        try:
            bars = prices.fetch(ticker, start="1990-01-01")
            if bars:
                f.write_text(json.dumps(bars))
                return bars
        except Exception as e:
            print(f"  {ticker} attempt {attempt+1} error: {e}", flush=True)
        time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"could not fetch {ticker}")


def indicators(bars):
    """Per prereg: SMA20, population sigma20, EMA20 (alpha=2/21, SMA-seeded),
    ATR20 (simple mean of TR), squeeze flag, entry/exit signal arrays."""
    n = len(bars)
    close = [b[5] for b in bars]
    high = [b[3] for b in bars]
    low = [b[4] for b in bars]
    sma = [None] * n
    ema = [None] * n
    atr = [None] * n
    squeeze = [None] * n
    tr = [None] * n
    e = None
    for i in range(n):
        if i >= 19:
            w = close[i - 19:i + 1]
            mu = sum(w) / 20.0
            sma[i] = mu
            if e is None:
                e = mu                      # seed EMA with first SMA
            else:
                e = e + (2.0 / 21.0) * (close[i] - e)
            ema[i] = e
        if i >= 1:
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]),
                        abs(low[i] - close[i - 1]))
        if i >= 20:
            atr[i] = sum(tr[i - 19:i + 1]) / 20.0
            w = close[i - 19:i + 1]
            mu = sma[i]
            sd = math.sqrt(sum((x - mu) ** 2 for x in w) / 20.0)  # population
            ub, lb = mu + 2.0 * sd, mu - 2.0 * sd
            uk, lk = ema[i] + 1.5 * atr[i], ema[i] - 1.5 * atr[i]
            squeeze[i] = (ub < uk) and (lb > lk)
    entry = [False] * n
    for i in range(SQUEEZE_MIN + 21, n):
        if squeeze[i] is False and all(squeeze[i - j] is True
                                       for j in range(1, SQUEEZE_MIN + 1)) \
                and close[i] > sma[i]:
            entry[i] = True
    return dict(close=close, sma=sma, ema=ema, entry=entry)


def simulate(data):
    """Global event-driven sim. data[t] = (bars, ind, date->idx)."""
    all_dates = sorted({b[1] for t in data for b in data[t][0]
                        if b[1] >= SIM_START})
    cash, nav_prev = CAP0, CAP0
    pos = {}            # ticker -> dict(sh, fill, entry_date, entry_i, minret)
    pend_in, pend_out = {}, {}   # ticker -> signal date
    trades = []
    nav_path = []       # (date, nav)
    last_close = {}
    for d in all_dates:
        # 1) executions at today's open (only tickers with a bar today)
        for t in list(pend_out):
            bars, ind, idx = data[t]
            if d in idx and t in pos:
                o = bars[idx[d]][2]
                p = pos.pop(t)
                cash += p["sh"] * o * (1 - COST)
                net = (o * (1 - COST)) / (p["fill"] * (1 + COST)) - 1
                trades.append(dict(ticker=t, entry=p["entry_date"],
                                   exit=d, net=net,
                                   hold=idx[d] - p["entry_i"],
                                   minret=p["minret"]))
                del pend_out[t]
        for t in list(pend_in):
            bars, ind, idx = data[t]
            if d in idx and t not in pos and len(pos) < K:
                o = bars[idx[d]][2]
                size = min(cash, nav_prev / K)
                if size > 10.0 and o > 0:
                    sh = size / (o * (1 + COST))
                    cash -= size
                    pos[t] = dict(sh=sh, fill=o, entry_date=d,
                                  entry_i=idx[d], minret=0.0)
                del pend_in[t]
            elif d in idx:
                del pend_in[t]      # slot lost or already held: drop order
        # 2) mark NAV at close
        for t in data:
            bars, ind, idx = data[t]
            if d in idx:
                last_close[t] = ind["close"][idx[d]]
        nav = cash + sum(p["sh"] * last_close[t] for t, p in pos.items())
        nav_path.append((d, nav))
        nav_prev = nav
        # 3) signals at close
        for t, p in pos.items():
            bars, ind, idx = data[t]
            if d in idx:
                i = idx[d]
                p["minret"] = min(p["minret"],
                                  ind["close"][i] / p["fill"] - 1)
                if t not in pend_out and (
                        ind["close"][i] < ind["ema"][i]
                        or i - p["entry_i"] >= MAX_HOLD):
                    pend_out[t] = d
        cands = []
        for t in data:
            bars, ind, idx = data[t]
            if d in idx and t not in pos and t not in pend_in:
                i = idx[d]
                if ind["entry"][i]:
                    cands.append((ind["close"][i] / ind["sma"][i] - 1, t))
        cands.sort(reverse=True)
        free = K - len(pos) - len(pend_in)
        for _, t in cands[:max(0, free)]:
            pend_in[t] = d
    return nav_path, trades, pos, last_close


def window_stats(nav_path, trades, lo, hi):
    seg = [(d, v) for d, v in nav_path if lo <= d <= hi]
    if len(seg) < 30:
        return None
    nav = [v for _, v in seg]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav))]
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    tw = [x for x in trades if lo <= x["entry"] <= hi]
    return dict(cagr=cagr, mo=(1 + cagr) ** (1 / 12) - 1, mdd=mdd,
                sharpe=sh, n=len(tw),
                win=sum(1 for x in tw if x["net"] > 0) / len(tw) if tw else
                float("nan"))


def main():
    data = {}
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        idx = {b[1]: i for i, b in enumerate(bars)}
        data[e.ticker] = (bars, indicators(bars), idx)
        print(f"loaded {e.ticker}: {bars[0][1]}..{bars[-1][1]} "
              f"({len(bars)} bars)", flush=True)
    nav_path, trades, open_pos, last_close = simulate(data)
    print(f"\ntotal closed trades: {len(trades)}; "
          f"open at end: {list(open_pos)} (marked to last close)")
    gate = window_stats(nav_path, trades, SIM_START, GATE_END)
    sec = window_stats(nav_path, trades, SEC_START, "2099-01-01")
    full = window_stats(nav_path, trades, SIM_START, "2099-01-01")
    for name, s in [("GATE 2000-2013", gate), ("SECONDARY 2014-", sec),
                    ("FULL 2000-", full)]:
        print(f"\n{name}: CAGR {s['cagr']*100:.2f}%  ({s['mo']*100:.2f}%/mo)  "
              f"maxDD {s['mdd']*100:.1f}%  Sharpe {s['sharpe']:.2f}  "
              f"n_trades {s['n']}  win {s['win']*100:.1f}%")
    g1 = gate["cagr"] >= 0.15
    g2 = gate["mdd"] <= 0.60
    g3 = gate["n"] >= 30
    print(f"\n  [{'PASS' if g1 else 'FAIL'}] gate CAGR>=15% "
          f"({gate['cagr']*100:.2f}%)")
    print(f"  [{'PASS' if g2 else 'FAIL'}] gate maxDD<=60% "
          f"({gate['mdd']*100:.1f}%)")
    print(f"  [{'OK' if g3 else 'INCONCLUSIVE'}] n_trades>=30 ({gate['n']})")
    if not g3:
        verdict = "INCONCLUSIVE"
    else:
        s1 = sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60
        verdict = "PASS" if (g1 and g2 and s1) else "FAIL"
        print(f"  [{'PASS' if s1 else 'FAIL'}] secondary CAGR>=15% & DD<=60% "
              f"({sec['cagr']*100:.2f}%, {sec['mdd']*100:.1f}%)")
    print(f"\n  E8 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
