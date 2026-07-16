"""E7 — international validation across unseen regimes, per prereg 70ed2a1.

Arm 1: 1x MA-rotation drawdown overlay (confirm E6) per market.
Arm 2: a-priori-vol-gated 3x rotation (vol<30%, drag 5%/yr, fixed a priori).
Local-index returns (currency-neutral); price indices understate return by
dividends. No tuning. Does NOT touch swing.db.

NAV (finding-things map): imports swing_bot (prices). Imported by: no other
module (standalone runner).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices

MARKETS = ["^N225", "^GDAXI", "^FTSE", "^HSI", "^AXJO"]   # gated set
CROSS = "^GSPC"                                            # context only
VTHR = 0.30      # a-priori vol gate (prereg 70ed2a1)
DRAG = 0.05      # a-priori synthetic-3x drag
MA = 200


def load(t):
    bars = [(b[1], b[2], b[5]) for b in prices.fetch(t, start="1985-01-01")]
    dates = [d for d, _, _ in bars]
    oc = {d: (o, c) for d, o, c in bars}
    close = {d: c for d, _, c in bars}
    return dates, close, oc, bars


def synth(bars, lev, d_annual):
    drag = d_annual / 252.0
    out, lvl, prev = {}, 1.0, None
    for dt, o, c in bars:
        if prev is None:
            out[dt] = (lvl, lvl)
        else:
            # floor at 0: a real leveraged fund cannot go below zero (a >1/lev
            # single-day drop = total wipeout, stays ~0 thereafter).
            oo = max(0.0, lvl * (1 + lev * (o/prev - 1) - drag))
            cc = max(0.0, lvl * (1 + lev * (c/prev - 1) - drag))
            out[dt] = (oo, cc)
        lvl = out[dt][1]; prev = c
    return out


def vol_series(bars):
    rets = [None] + [bars[i][2]/bars[i-1][2] - 1 for i in range(1, len(bars))]
    vol = [None]*len(bars)
    for i in range(20, len(bars)):
        w = rets[i-19:i+1]; mu = sum(w)/20
        vol[i] = math.sqrt(sum((x-mu)**2 for x in w)/19) * math.sqrt(252)
    return vol


def rotation(dates, sig_close, pos_oc, vthr=None, vol=None, cost_bps=5.0):
    cost = cost_bps/10000.0
    closes = [sig_close[d] for d in dates]
    cash, sh, state, pend = 1.0, 0.0, 0, None
    nav = []
    for i, d in enumerate(dates):
        o, c = pos_oc[d]
        if pend is not None and (i - pend[1]) >= 1:
            if pend[0] == 1 and state == 0 and o > 0:   # can't buy a dead fund
                sh = cash/(o*(1+cost)); cash = 0.0; state = 1
            elif pend[0] == 0 and state == 1:
                cash = sh*o*(1-cost); sh = 0.0; state = 0
            pend = None
        nav.append(cash + sh*c)
        if i >= MA:
            m = sum(closes[i-MA:i])/MA
            trend = closes[i] > m
            volok = (vthr is None) or (vol[i] is not None and vol[i] < vthr)
            want = 1 if (trend and volok) else 0
            if want != state and pend is None:
                pend = (want, i)
    return nav


def bh(bars):
    base = bars[0][2]
    return [c/base for _, _, c in bars]


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mo=float("nan"), mdd=float("nan"),
                    sharpe=float("nan"))
    rets = [nav[i]/nav[i-1]-1 for i in range(1, len(nav)) if nav[i-1] > 0]
    yrs = len(nav)/252.0
    cagr = (nav[-1]/nav[0])**(1/yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets)/len(rets)
    sd = math.sqrt(sum((r-mu)**2 for r in rets)/(len(rets)-1))
    sh = mu/sd*math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak-v)/peak)
    return dict(cagr=cagr, mo=(1+cagr)**(1/12)-1, mdd=mdd, sharpe=sh)


def main():
    data = {}
    for t in MARKETS + [CROSS]:
        data[t] = load(t)
        print(f"loaded {t}: {data[t][3][0][1]}..{data[t][3][-1][1]} "
              f"({len(data[t][0])} bars)")

    print("\n=== ARM 1: 1x rotation vs buy-hold (drawdown overlay) ===")
    print(f"{'market':8}{'rot CAGR':>10}{'rot maxDD':>11}{'rot Sh':>8}"
          f"{'BH maxDD':>10}{'BH Sh':>8}{'  pass'}")
    arm1_pass = 0
    for t in MARKETS + [CROSS]:
        dates, close, oc, bars = data[t]
        r = stats(rotation(dates, close, oc))
        b = stats(bh(bars))
        ok = (r["mdd"] <= b["mdd"] - 0.10) and (r["sharpe"] >= b["sharpe"])
        if t in MARKETS and ok:
            arm1_pass += 1
        print(f"{t:8}{r['cagr']*100:>9.2f}%{r['mdd']*100:>10.1f}%"
              f"{r['sharpe']:>8.2f}{b['mdd']*100:>9.1f}%{b['sharpe']:>8.2f}"
              f"{'   YES' if ok else '   no'}")
    a1 = arm1_pass >= 4
    print(f"Arm 1: {arm1_pass}/5 non-US markets pass -> "
          f"{'PASS' if a1 else 'FAIL'} (need >=4)")

    print("\n=== ARM 2: a-priori vol-gated 3x rotation (high-return shot) ===")
    print(f"{'market':8}{'vg3x CAGR':>11}{'%/mo':>8}{'vg3x maxDD':>12}"
          f"{'plain3x DD':>12}{'BH3x CAGR':>11}")
    cagrs, nikkei = [], None
    for t in MARKETS + [CROSS]:
        dates, close, oc, bars = data[t]
        vol = vol_series(bars)
        s3 = synth(bars, 3.0, DRAG)
        vg = stats(rotation(dates, close, s3, VTHR, vol))
        p3 = stats(rotation(dates, close, s3))          # no vol gate
        b3 = stats(bh([(d, 0, s3[d][1]) for d in dates]))   # buy-hold 3x
        if t in MARKETS:
            cagrs.append(vg["cagr"])
            if t == "^N225":
                nikkei = vg
        print(f"{t:8}{vg['cagr']*100:>10.2f}%{vg['mo']*100:>7.2f}%"
              f"{vg['mdd']*100:>11.1f}%{p3['mdd']*100:>11.1f}%"
              f"{b3['cagr']*100:>10.2f}%")
    mean_cagr = sum(cagrs)/len(cagrs)
    c1 = all(c > 0 for c in cagrs)
    c2 = True  # computed below with maxDD; recompute cleanly
    # recompute maxDD gate cleanly
    dds = []
    for t in MARKETS:
        dates, close, oc, bars = data[t]
        vol = vol_series(bars); s3 = synth(bars, 3.0, DRAG)
        dds.append(stats(rotation(dates, close, s3, VTHR, vol))["mdd"])
    c2 = all(d <= 0.70 for d in dds)
    c3 = nikkei["cagr"] > 0 and nikkei["mdd"] <= 0.70
    c4 = mean_cagr >= 0.15
    print(f"\n  [{'PASS' if c1 else 'FAIL'}] 1 positive CAGR all 5")
    print(f"  [{'PASS' if c2 else 'FAIL'}] 2 maxDD<=70% all 5 (max {max(dds)*100:.1f}%)")
    print(f"  [{'PASS' if c3 else 'FAIL'}] 3 Nikkei CAGR>0 & DD<=70% "
          f"({nikkei['cagr']*100:.2f}%, {nikkei['mdd']*100:.1f}%)")
    print(f"  [{'PASS' if c4 else 'FAIL'}] 4 mean CAGR>=15% ({mean_cagr*100:.2f}%)")
    print(f"\n  ARM 2 VERDICT: {'PASS' if (c1 and c2 and c3 and c4) else 'FAIL'}")


if __name__ == "__main__":
    main()
