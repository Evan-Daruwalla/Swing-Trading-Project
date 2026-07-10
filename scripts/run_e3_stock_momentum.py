"""E3 — concentrated stock momentum, per prereg 87bc8d9. FALSIFICATION-ONLY:
a FAIL (esp 2000-2013) is clean; a PASS is uninterpretable (survivorship +
lookahead bias) and routes to forward paper. No tuning.

Universe = ~35 survivor large-caps (explicitly biased, see prereg S0). Hold
top K=3 by trailing 63-day return, rebalance every 10 trading days, next-open
fills, 5 bps/side, full rebalance each period (slightly pessimistic on cost =
conservative for a falsification test). Does NOT touch swing.db.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices

UNIV = ("MSFT INTC CSCO ORCL IBM AAPL QCOM TXN ADBE JPM BAC WFC C GS AXP "
        "XOM CVX COP SLB PG KO PEP WMT MCD HD NKE DIS JNJ PFE MRK ABT UNH "
        "GE CAT BA MMM HON T VZ").split()
K = 3
LOOK = 63
REBAL = 10
COST = 5.0 / 10000.0
W = {"2000-2013": ("2000-01-03", "2013-12-31"),
     "2014-2026": ("2014-01-02", "2026-07-08"),
     "2000-2026": ("2000-01-03", "2026-07-08")}


def load(t):
    b = prices.fetch(t, start="2000-01-01")
    return {bb[1]: (bb[2], bb[5]) for bb in b} if b else None   # date->(open,close)


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mo=float("nan"), mdd=float("nan"),
                    sharpe=float("nan"))
    rets = [nav[i]/nav[i-1]-1 for i in range(1, len(nav)) if nav[i-1] > 0]
    yrs = len(nav)/252.0
    cagr = (nav[-1]/nav[0])**(1/yrs)-1 if nav[-1] > 0 else -1.0
    mu = sum(rets)/len(rets)
    sd = math.sqrt(sum((r-mu)**2 for r in rets)/(len(rets)-1))
    sh = mu/sd*math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak-v)/peak)
    return dict(cagr=cagr, mo=(1+cagr)**(1/12)-1, mdd=mdd, sharpe=sh)


def main():
    data, missing = {}, []
    for t in UNIV:
        d = None
        for _ in range(4):
            d = load(t)
            if d:
                break
        if d:
            data[t] = d
        else:
            missing.append(t)
    print(f"fetched {len(data)}/{len(UNIV)} stocks; missing: {missing}")
    spy = None
    for _ in range(4):
        spy = load("SPY")
        if spy:
            break

    # common trading dates (present in ALL fetched stocks)
    dates = sorted(set.intersection(*(set(d) for d in data.values())))
    tick = list(data.keys())
    print(f"common dates: {dates[0]}..{dates[-1]} ({len(dates)})")

    # continuous backtest 2000..2026
    cash, pos = 1.0, {}          # pos: ticker -> shares
    pend = None                  # (targets, decided_i)
    nav_by_date = {}
    for i, d in enumerate(dates):
        # execute pending full-rebalance at today's open
        if pend is not None and (i - pend[1]) >= 1:
            targets = pend[0]
            navv = cash + sum(pos[t]*data[t][d][1] for t in pos if d in data[t])
            # liquidate all at open
            for t in list(pos):
                o = data[t][d][0]
                cash += pos[t]*o*(1-COST)
            pos = {}
            per = navv / K
            for t in targets:
                o = data[t][d][0]
                if o > 0:
                    sh = per/(o*(1+COST)); cash -= sh*o*(1+COST); pos[t] = sh
            pend = None
        nav_by_date[d] = cash + sum(pos[t]*data[t][d][1] for t in pos)
        # decide at close on rebalance days
        if i >= LOOK+1 and i % REBAL == 0 and i+1 < len(dates):
            mom = []
            for t in tick:
                c_now, c_prev = data[t][dates[i-1]][1], data[t][dates[i-1-LOOK]][1]
                if c_prev > 0:
                    mom.append((c_now/c_prev - 1, t))
            mom.sort(reverse=True)
            pend = ([t for _, t in mom[:K]], i)

    print(f"\n{'window':12}{'E3 CAGR':>9}{'%/mo':>8}{'maxDD':>8}{'Sharpe':>8}"
          f"{'EWuniv CAGR':>13}{'SPY CAGR':>10}")
    res = {}
    for wn, (s, e) in W.items():
        nav = [nav_by_date[d] for d in dates if s <= d <= e]
        m = stats(nav)
        # equal-weight buy-hold universe
        ew = []
        for d in dates:
            if s <= d <= e:
                ew.append(sum(data[t][d][1]/data[t][dates[0]][1]
                              for t in tick)/len(tick))
        mew = stats(ew)
        msp = stats([spy[d][1] for d in sorted(spy) if s <= d <= e]) if spy else {"cagr": float("nan")}
        res[wn] = m
        print(f"{wn:12}{m['cagr']*100:>8.2f}%{m['mo']*100:>7.2f}%"
              f"{m['mdd']*100:>7.1f}%{m['sharpe']:>8.2f}"
              f"{mew['cagr']*100:>12.2f}%{msp['cagr']*100:>9.2f}%")

    g = res["2000-2013"]
    c1 = g["cagr"] >= 0.15
    c2 = g["mdd"] <= 0.65
    print(f"\n=== KILL CRITERIA (2000-2013 gate; prereg 87bc8d9) ===")
    print(f"  [{'PASS' if c1 else 'FAIL'}] 1 CAGR>=15% ({g['cagr']*100:.2f}%)")
    print(f"  [{'PASS' if c2 else 'FAIL'}] 2 maxDD<=65% ({g['mdd']*100:.1f}%)")
    verdict = c1 and c2
    print(f"\n  E3 backtest gate: {'PASS (UNINTERPRETABLE - biases; forward only)' if verdict else 'FAIL (clean - stocks closed)'}")


if __name__ == "__main__":
    main()
