"""X1 - conditional volatility targeting (E6xE18 interaction), per prereg
prereg_x1_vol_targeting.md (committed 07c22cb, predates this runner).

SPY binary overlay (exposure 0/1), signal at close, next-open, 1 bp/side (broad
ETF). Three arms: (a) E6 = SPY>200DMA; (b) E18 = VIX/VIX3M<1; (c) conditional =
flat iff (VIX/VIX3M>1 AND SPY<200DMA). Gate 2006-2013 (VIX3M floor), secondary
2014-. OVERLAY -> PASS-RA reachable only, labelled DESCRIPTIVE (low effective N).
No swing.db writes.

DATA CONVENTION: SPY split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): imports run_e18_regime_gates (macro_close, sma);
run_e8_squeeze (CAP0, COST, cache_fetch). Imported by: no other module
(standalone runner).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e18_regime_gates import macro_close, sma

GATE = ("2006-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mdd=float("nan"), sharpe=float("nan"))
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1] > 0]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mdd=mdd, sharpe=sh)


def main():
    bars = cache_fetch("SPY")
    dates = [b[1] for b in bars]
    op = [b[2] for b in bars]
    cl = [b[5] for b in bars]
    dma = sma(cl, 200)
    vix, vix3m = macro_close("^VIX"), macro_close("^VIX3M")

    def ratio(d):
        if d in vix and d in vix3m and vix3m[d] > 0:
            return vix[d] / vix3m[d]
        return None

    def want(arm, i):
        d = dates[i]
        trend_ok = dma[i] is not None and cl[i] > dma[i]
        r = ratio(d)
        vol_ok = r is not None and r < 1.0            # contango = calm
        if arm == "a":
            return 1 if (dma[i] is None or trend_ok) else 0
        if arm == "b":
            return 1 if (r is None or vol_ok) else 0
        # (c) conditional: flat iff vol elevated AND trend broken
        vol_bad = r is not None and r > 1.0
        trend_bad = dma[i] is not None and cl[i] < dma[i]
        return 0 if (vol_bad and trend_bad) else 1

    def run_arm(arm, cost):
        cash, sh, pend = CAP0, 0.0, None
        nav, toggles = [], []
        for i in range(len(dates)):
            if pend is not None:
                if pend == 1 and sh == 0.0 and cash > 0:
                    sh = cash / (op[i] * (1 + cost)); cash = 0.0; toggles.append(dates[i])
                elif pend == 0 and sh > 0.0:
                    cash = sh * op[i] * (1 - cost); sh = 0.0; toggles.append(dates[i])
                pend = None
            nav.append((dates[i], cash + sh * cl[i], sh > 0.0))
            w = want(arm, i)
            if w == 1 and sh == 0.0 and cash > 0:
                pend = 1
            elif w == 0 and sh > 0.0:
                pend = 0
        return nav, toggles

    def win(nav, lo, hi):
        return [v for (d, v, _) in nav if lo <= d <= hi]

    def expo(nav, lo, hi):
        seg = [inm for (d, v, inm) in nav if lo <= d <= hi]
        return 100.0 * sum(seg) / len(seg) if seg else 0.0

    spy_bh = [(d, c / cl[0]) for d, c in zip(dates, cl)]

    def bh(lo, hi):
        return stats([v for (d, v) in spy_bh if lo <= d <= hi])

    arms = {a: run_arm(a, 0.0001) for a in ("a", "b", "c")}
    print(f"X1 vol-targeting | SPY {dates[0]}..{dates[-1]}; "
          f"VIX3M from {min(vix3m)}\n")
    for wn, (lo, hi) in [("GATE 2006-2013", GATE), ("SECONDARY 2014-", SEC)]:
        b = bh(lo, hi)
        print(f"--- {wn} ---")
        print(f"  {'arm':22}{'CAGR':>8}{'maxDD':>8}{'Sharpe':>8}{'expo%':>8}{'toggles':>9}")
        for a, label in [("a", "(a) E6 200DMA"), ("b", "(b) E18 VIX-TS"),
                         ("c", "(c) conditional")]:
            nav, tog = arms[a]
            s = stats(win(nav, lo, hi))
            nt = sum(1 for d in tog if lo <= d <= hi)
            print(f"  {label:22}{s['cagr']*100:>7.2f}%{s['mdd']*100:>7.1f}%"
                  f"{s['sharpe']:>8.2f}{expo(nav, lo, hi):>7.1f}%{nt:>9}")
        print(f"  {'SPY buy-hold':22}{b['cagr']*100:>7.2f}%{b['mdd']*100:>7.1f}%"
              f"{b['sharpe']:>8.2f}{'100.0%':>8}{'0':>9}\n")

    # stress legs on arm (c)
    print("arm (c) cost stress:")
    for cst, lab in [(0.0001, "1bp"), (0.0005, "5bp"), (0.0015, "15bp")]:
        nav, _ = run_arm("c", cst)
        s = stats(win(nav, *GATE))
        print(f"  {lab:5} gate CAGR {s['cagr']*100:.2f}%  Sharpe {s['sharpe']:.2f}")

    # verdict
    def arm_stats(a, lo, hi):
        return stats(win(arms[a][0], lo, hi))
    gc, sc = arm_stats("c", *GATE), arm_stats("c", *SEC)
    ga, gb = arm_stats("a", *GATE), arm_stats("b", *GATE)
    bg, bs = bh(*GATE), bh(*SEC)
    ntg = sum(1 for d in arms["c"][1] if GATE[0] <= d <= GATE[1])
    dd_cut = (bg["mdd"] - gc["mdd"]) * 100
    ra = (gc["sharpe"] >= 0.80 and gc["sharpe"] > bg["sharpe"] and sc["sharpe"] > bs["sharpe"]
          and gc["cagr"] > 0 and sc["cagr"] > 0 and dd_cut >= 10.0
          and gc["sharpe"] > ga["sharpe"] and gc["sharpe"] > gb["sharpe"])
    floor = ntg >= 10
    print(f"\n=== VERDICT (prereg prereg_x1_vol_targeting.md; DESCRIPTIVE, overlay) ===")
    print(f"  gate toggles {ntg} (>=10: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  (c) gate Sharpe {gc['sharpe']:.2f} (>=0.80 & >SPY {bg['sharpe']:.2f} "
          f"& >a {ga['sharpe']:.2f} & >b {gb['sharpe']:.2f}); DD cut {dd_cut:.1f}pp (>=10)")
    if not floor:
        v = "INCONCLUSIVE"
    elif ra:
        v = "PASS-RA (DESCRIPTIVE - forward paper is the real grade; PASS-HR unreachable)"
    else:
        v = "FAIL (conditional interaction does not beat the plain overlays / SPY)"
    print(f"\n  X1 VERDICT: {v}")


if __name__ == "__main__":
    main()
