"""PRESSURE-TEST (exploratory, CONTAMINATED) — can a volatility gate save 3x
leverage rotation across 2000-2013?

NOT a pre-registered experiment. 2000-2013 is already seen (E5), so a vol
threshold chosen with hindsight is fit to those crashes. Asymmetric info:
a FAIL here (even hindsight can't save it) kills the idea cleanly; a PASS is
only a hypothesis for a clean forward/new-market test. Labeled as such.

Synthetic 3x Nasdaq from QQQ (drag 4%/yr, validated in E5). Gate: hold 3x when
QQQ close > 200d MA AND 20d annualized realized vol < V; else cash.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices

W = {"2000-2013": ("2000-01-01", "2013-12-31"),
     "2014-2026": ("2014-01-02", "2026-07-08"),
     "2000-2026": ("2000-01-01", "2026-07-08")}


def synth3(qqq, d=0.04):
    drag = d / 252.0
    out, lvl, prev = {}, 1.0, None
    for dt, o, c in qqq:
        if prev is None:
            out[dt] = (lvl, lvl)
        else:
            out[dt] = (lvl * (1 + 3 * (o / prev - 1) - drag),
                       lvl * (1 + 3 * (c / prev - 1) - drag))
        lvl = out[dt][1]; prev = c
    return out


def stats(nav):
    if len(nav) < 3 or nav[0] <= 0:
        return (float("nan"),) * 3
    rets = [nav[i] / nav[i-1] - 1 for i in range(1, len(nav))]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return cagr, (1 + cagr) ** (1/12) - 1, mdd


def run(dates, qclose, syn, vol, ma=200, vthr=None, cost_bps=5.0,
        start=None, end=None, cap=500.0):
    cost = cost_bps / 10000.0
    closes = [qclose[d] for d in dates]
    cash, sh, state, pend = cap, 0.0, 0, None
    nav = []
    for i, d in enumerate(dates):
        o, c = syn[d]
        if pend is not None and (i - pend[1]) >= 1:
            if pend[0] == 1 and state == 0:
                sh = cash / (o * (1 + cost)); cash = 0.0; state = 1
            elif pend[0] == 0 and state == 1:
                cash = sh * o * (1 - cost); sh = 0.0; state = 0
            pend = None
        v = cash + sh * c
        if (start is None or d >= start) and (end is None or d <= end):
            nav.append(v)
        if i >= ma:
            m = sum(closes[i-ma:i]) / ma
            trend = closes[i] > m
            volok = (vthr is None) or (vol[i] is not None and vol[i] < vthr)
            want = 1 if (trend and volok) else 0
            if want != state and pend is None:
                pend = (want, i)
    return nav


def main():
    qqq = prices.fetch("QQQ", start="1999-01-01")
    qqq = [(b[1], b[2], b[5]) for b in qqq]
    dates = [d for d, _, _ in qqq]
    qclose = {d: c for d, _, c in qqq}
    syn = synth3(qqq)
    # 20d annualized realized vol aligned to dates index
    rets = [None] + [qqq[i][2] / qqq[i-1][2] - 1 for i in range(1, len(qqq))]
    vol = [None] * len(qqq)
    for i in range(20, len(qqq)):
        w = rets[i-19:i+1]
        mu = sum(w) / 20
        sd = math.sqrt(sum((x-mu)**2 for x in w) / 19)
        vol[i] = sd * math.sqrt(252)

    print("PRESSURE-TEST: vol-gated 3x rotation (CONTAMINATED / exploratory)")
    print(f"{'gate':16}{'window':12}{'CAGR':>9}{'%/mo':>8}{'maxDD':>8}")
    print("-" * 53)
    for label, vthr in [("no gate (E4/E5)", None), ("vol<25%", 0.25),
                        ("vol<30%", 0.30), ("vol<40%", 0.40)]:
        for wn, (s, e) in W.items():
            cagr, mo, mdd = stats(run(dates, qclose, syn, vol, vthr=vthr,
                                      start=s, end=e))
            print(f"{label:16}{wn:12}{cagr*100:>8.2f}%{mo*100:>7.2f}%"
                  f"{mdd*100:>7.1f}%")
        print()


if __name__ == "__main__":
    main()
