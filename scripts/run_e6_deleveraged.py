"""E6 — de-leveraged 200-MA rotation as a drawdown overlay, per prereg 0526ea2.

PRIMARY: 1x = QQQ real data (no synthesis). SECONDARY: 2x synthetic (drag
calibrated to real QLD). Gates on the 1x cell across three windows. No tuning.
Does NOT touch swing.db.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices

W = {"2000-2013": ("2000-01-01", "2013-12-31"),
     "2014-2026": ("2014-01-02", "2026-07-08"),
     "2000-2026": ("2000-01-01", "2026-07-08")}
OVL = ("2014-01-02", "2026-07-08")


def series(t, start):
    return [(b[1], b[2], b[5]) for b in prices.fetch(t, start=start)]


def synth(qqq, lev, d_annual):
    drag = d_annual / 252.0
    out, lvl, prev = {}, 1.0, None
    for dt, o, c in qqq:
        if prev is None:
            out[dt] = (lvl, lvl)
        else:
            out[dt] = (lvl * (1 + lev * (o / prev - 1) - drag),
                       lvl * (1 + lev * (c / prev - 1) - drag))
        lvl = out[dt][1]
        prev = c
    return out


def rotation_nav(dates, sig_close, pos_oc, ma=200, cost_bps=5.0,
                 start=None, end=None, cap=500.0):
    cost = cost_bps / 10000.0
    closes = [sig_close[d] for d in dates]
    cash, sh, state, pend = cap, 0.0, 0, None
    nav = []
    for i, d in enumerate(dates):
        o, c = pos_oc[d]
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
            m = sum(closes[i - ma:i]) / ma
            want = 1 if closes[i] > m else 0
            if want != state and pend is None:
                pend = (want, i)
    return nav


def bh(dates, oc, start, end, cap=500.0):
    xs = [oc[d][1] for d in dates if start <= d <= end]
    return [cap * c / xs[0] for c in xs]


def stats(nav):
    if len(nav) < 3 or nav[0] <= 0:
        return dict(cagr=float("nan"), mo=float("nan"), mdd=float("nan"),
                    sharpe=float("nan"), mar=float("nan"))
    rets = [nav[i] / nav[i-1] - 1 for i in range(1, len(nav))]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sharpe = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mo=(1 + cagr) ** (1/12) - 1, mdd=mdd,
                sharpe=sharpe, mar=(cagr / mdd if mdd > 0 else float("nan")))


def calib(qqq, real, lev):
    ov = [d for d, _, _ in qqq if OVL[0] <= d <= OVL[1] and d in real]
    rc = stats([real[d] for d in ov])["cagr"]
    best = None
    for step in range(0, 41):
        D = step * 0.0025
        s = synth(qqq, lev, D)
        c = stats([s[d][1] for d in ov])["cagr"]
        if best is None or abs(c - rc) < best[1]:
            best = (D, abs(c - rc), c)
    return best[0], rc, best[2]


def main():
    qqq = series("QQQ", "1999-01-01")
    qdates = [d for d, _, _ in qqq]
    qclose = {d: c for d, _, c in qqq}
    qoc = {d: (o, c) for d, o, c in qqq}

    # 2x synthetic calibrated to real QLD
    qld = {d: c for d, _, c in series("QLD", "2006-01-01")}
    d2, qld_cagr, syn2_cagr = calib(qqq, qld, 2.0)
    syn2 = synth(qqq, 2.0, d2)
    print(f"2x calib: real QLD overlap CAGR={qld_cagr*100:.2f}% "
          f"drag={d2*100:.2f}%/yr synth={syn2_cagr*100:.2f}%")

    hdr = f"{'window':12}{'strat':16}{'CAGR':>9}{'%/mo':>8}{'maxDD':>8}{'Sharpe':>8}{'MAR':>7}"
    print("\n" + hdr); print("-" * len(hdr))
    res = {}
    for wn, (s, e) in W.items():
        r1 = stats(rotation_nav(qdates, qclose, qoc, 200, 5.0, s, e))
        r2 = stats(rotation_nav(qdates, qclose, syn2, 200, 5.0, s, e))
        bq = stats(bh(qdates, qoc, s, e))
        res[wn] = (r1, bq)
        for lbl, m in [("1x rotation", r1), ("2x-synth rot", r2),
                       ("buy-hold QQQ", bq)]:
            print(f"{wn:12}{lbl:16}{m['cagr']*100:>8.2f}%{m['mo']*100:>7.2f}%"
                  f"{m['mdd']*100:>7.1f}%{m['sharpe']:>8.2f}{m['mar']:>7.2f}")
        print()

    # --- kill criteria (1x) ---
    print("=== KILL CRITERIA (1x rotation; prereg 0526ea2) ===")
    c1 = (res["2000-2013"][0]["mdd"] <= res["2000-2013"][1]["mdd"] - 0.10 and
          res["2000-2026"][0]["mdd"] <= res["2000-2026"][1]["mdd"] - 0.10)
    c2 = all(res[w][0]["sharpe"] >= res[w][1]["sharpe"] for w in W)
    c3 = all(res[w][0]["cagr"] > 0 for w in W)
    print(f"  [{'PASS' if c1 else 'FAIL'}] 1 maxDD >=10pp below BH-QQQ in both crash windows")
    for w in ("2000-2013", "2000-2026"):
        print(f"        {w}: rot {res[w][0]['mdd']*100:.1f}% vs BH {res[w][1]['mdd']*100:.1f}%")
    print(f"  [{'PASS' if c2 else 'FAIL'}] 2 Sharpe >= BH-QQQ in ALL 3 windows")
    for w in W:
        print(f"        {w}: rot {res[w][0]['sharpe']:.2f} vs BH {res[w][1]['sharpe']:.2f}")
    print(f"  [{'PASS' if c3 else 'FAIL'}] 3 CAGR>0 in all 3 windows")
    print(f"\n  E6 VERDICT: {'PASS' if (c1 and c2 and c3) else 'FAIL'}")


if __name__ == "__main__":
    main()
