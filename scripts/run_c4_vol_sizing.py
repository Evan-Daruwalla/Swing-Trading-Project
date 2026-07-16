"""C4 - Moreira-Muir vol-targeting sizing overlay, per prereg
prereg_c4_vol_sizing.md (committed doc-only before this runner).

Bases: E6 (QQQ>200DMA) and E18 (VIX/VIX3M<1) on QQQ. Overlay: when gate on,
w = min(1, 0.15/sigma_ann20d); rebalance band |dw|>0.05; signal close -> next
open; 1 bp/side. Arms: each base unmanaged vs managed + QQQ-BH. PASS-RA-only,
DESCRIPTIVE. No swing.db writes.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): imports run_e18_regime_gates (macro_close, sma);
run_e8_squeeze (CAP0, cache_fetch). Imported by: no other module (standalone
runner).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, CAP0
from run_e18_regime_gates import macro_close, sma

E6_WIN = (("2000-01-01", "2013-12-31"), ("2014-01-01", "2099-01-01"))
E18_WIN = (("2006-01-01", "2013-12-31"), ("2014-01-01", "2099-01-01"))
BAND = 0.05
TGT = 0.15
COST1 = 0.0001


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
    bars = cache_fetch("QQQ")
    dates = [b[1] for b in bars]
    op = [b[2] for b in bars]
    cl = [b[5] for b in bars]
    dma = sma(cl, 200)
    vix, vix3m = macro_close("^VIX"), macro_close("^VIX3M")
    n = len(dates)
    rets = [0.0] + [cl[i] / cl[i - 1] - 1 for i in range(1, n)]
    sig = [None] * n
    for i in range(20, n):
        mu = sum(rets[i - 19:i + 1]) / 20
        sig[i] = math.sqrt(sum((r - mu) ** 2 for r in rets[i - 19:i + 1]) / 20) * math.sqrt(252)

    def gate(base, i):
        d = dates[i]
        if base == "e6":
            return dma[i] is None or cl[i] > dma[i]
        r = (vix[d] / vix3m[d]) if (d in vix and d in vix3m and vix3m[d] > 0) else None
        return r is None or r < 1.0

    def run(base, managed, cost):
        cash, sh_, w_cur, trades = CAP0, 0.0, 0.0, 0
        pend, navs = None, []
        for i in range(n):
            if pend is not None:
                tgt_w = pend
                nav = cash + sh_ * op[i]
                d_val = tgt_w * nav - sh_ * op[i]
                sh_new = sh_ + d_val / op[i]
                cash -= d_val + abs(d_val) * cost
                sh_ = sh_new
                w_cur = tgt_w
                trades += 1
                pend = None
            navs.append(cash + sh_ * cl[i])
            g = gate(base, i)
            w = 0.0
            if g:
                w = 1.0
                if managed and sig[i]:
                    w = min(1.0, TGT / sig[i])
            if abs(w - w_cur) > BAND or (w == 0.0 and w_cur > 0.0):
                pend = w
        return navs, trades

    qqq_bh = [c / cl[0] for c in cl]

    def win(series, lo, hi):
        return [v for d, v in zip(dates, series) if lo <= d <= hi]

    print(f"C4 vol-sizing | QQQ {dates[0]}..{dates[-1]}; w=min(1,{TGT}/sig20d), "
          f"band {BAND}, 1bp\n")
    verdicts = {}
    for base, wins, label in [("e6", E6_WIN, "E6 200DMA"), ("e18", E18_WIN, "E18 VIX-TS")]:
        (glo, ghi), (slo, shi) = wins
        um, tu = run(base, False, COST1)
        mg, tm = run(base, True, COST1)
        print(f"--- base {label} (gate {glo[:4]}-{ghi[:4]}) ---")
        print(f"  {'arm':16}{'gCAGR':>8}{'gDD':>7}{'gSh':>6}{'sCAGR':>8}{'sDD':>7}{'sSh':>6}{'trades':>8}")
        rows = {}
        for nm, nav, tr in [("unmanaged", um, tu), ("vol-managed", mg, tm)]:
            g, s = stats(win(nav, glo, ghi)), stats(win(nav, slo, shi))
            rows[nm] = (g, s)
            print(f"  {nm:16}{g['cagr']*100:>7.2f}%{g['mdd']*100:>6.1f}%{g['sharpe']:>6.2f}"
                  f"{s['cagr']*100:>7.2f}%{s['mdd']*100:>6.1f}%{s['sharpe']:>6.2f}{tr:>8}")
        bg, bs = stats(win(qqq_bh, glo, ghi)), stats(win(qqq_bh, slo, shi))
        print(f"  {'QQQ buy-hold':16}{bg['cagr']*100:>7.2f}%{bg['mdd']*100:>6.1f}%{bg['sharpe']:>6.2f}"
              f"{bs['cagr']*100:>7.2f}%{bs['mdd']*100:>6.1f}%{bs['sharpe']:>6.2f}")
        g_m, s_m = rows["vol-managed"]; g_u, s_u = rows["unmanaged"]
        ra = (g_m["sharpe"] >= 0.80 and g_m["sharpe"] > g_u["sharpe"]
              and s_m["sharpe"] > s_u["sharpe"] and g_m["cagr"] > 0 and s_m["cagr"] > 0)
        verdicts[label] = (ra, g_m, g_u)
        print()
    # stress
    for cst, lab in [(0.0005, "5bp"), (0.0015, "15bp")]:
        mg, _ = run("e6", True, cst)
        s = stats(win(mg, *E6_WIN[0]))
        print(f"stress {lab}: E6-managed gate CAGR {s['cagr']*100:.2f}% Sh {s['sharpe']:.2f}")
    print(f"\n=== VERDICT (prereg prereg_c4_vol_sizing.md; DESCRIPTIVE) ===")
    any_pass = False
    for label, (ra, g_m, g_u) in verdicts.items():
        print(f"  {label}: managed gate Sh {g_m['sharpe']:.2f} vs unmanaged "
              f"{g_u['sharpe']:.2f} -> {'PASS-RA bar met' if ra else 'fail'}")
        any_pass = any_pass or ra
    print(f"\n  C4 VERDICT: "
          f"{'PASS-RA (DESCRIPTIVE - forward only)' if any_pass else 'FAIL (vol-managing adds nothing to the overlays)'}")


if __name__ == "__main__":
    main()
