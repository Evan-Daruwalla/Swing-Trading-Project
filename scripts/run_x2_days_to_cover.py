"""X2 - days-to-cover / short-interest drift, per prereg prereg_x2_days_to_cover.md.

FINRA consolidated short interest (39 survivor large-caps, biweekly settlement
2017-12-29..2026-06-30). Each settlement date, rank by precomputed
days-to-cover. Deployable long-only leg = K=5 LOWEST-DTC, equal-weight,
rebalanced each cycle; existence spread = low-K minus high-K (non-deployable).
Enter 10 sessions AFTER the settlement date (dissemination-lag lookahead guard).
Single 2018-2026 window -> MODIFIED-WINDOW CAP: best verdict = PROMISING.
5 bps/side. Reuses .e8e9_cache; no swing.db writes.

DATA CONVENTION: prices split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
"""
import bisect
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from ingest_finra_short_interest import UNIV, OUT

K = 5
LAG = 10          # trading sessions after settlement date (dissemination guard)


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
    si = json.loads(OUT.read_text())
    oc, tdates = {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = [b[1] for b in bars]
    master = sorted({d for t in UNIV for d in tdates[t]})

    # settlement date -> (entry_date, low-K, high-K) with the LAG guard
    entries = []
    for S in sorted(si):
        ranked = sorted(((v["dtc"], s) for s, v in si[S].items() if v["dtc"] > 0))
        if len(ranked) < 2 * K:
            continue
        low = [s for _, s in ranked[:K]]
        high = [s for _, s in ranked[-K:]]
        j = bisect.bisect_right(master, S) + (LAG - 1)
        if j >= len(master):
            continue
        entries.append((master[j], low, high))
    entries.sort()
    start = entries[0][0]
    ecal = {e[0]: e for e in entries}
    win = [d for d in master if d >= start]

    def long_leg(fill, cost):
        """Rebalance to EW low-K at each entry date. fill='open'|'close'."""
        px = 0 if fill == "open" else 1
        cash, pos, navd = CAP0, {}, {}
        for d in win:
            if d in ecal:
                navv = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
                for t in list(pos):
                    if d in oc[t]:
                        cash += pos[t] * oc[t][d][px] * (1 - cost); del pos[t]
                per = navv / K
                for t in ecal[d][1]:
                    if d in oc[t] and oc[t][d][px] > 0:
                        sh = per / (oc[t][d][px] * (1 + cost))
                        cash -= sh * oc[t][d][px] * (1 + cost); pos[t] = sh
            navd[d] = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
        return [navd[d] for d in win]

    # existence spread: daily EW(low) - EW(high), holding current cycle baskets,
    # close-to-close 0-cost (existence test only, not deployable)
    def spread():
        cur_lo, cur_hi = None, None
        nav_lo, nav_hi = [CAP0], [CAP0]
        held = None
        for i in range(1, len(win)):
            d0, d1 = win[i - 1], win[i]
            if d0 in ecal:
                held = ecal[d0]
            if held is None:
                nav_lo.append(nav_lo[-1]); nav_hi.append(nav_hi[-1]); continue
            def basket_ret(names):
                rs = [oc[t][d1][1] / oc[t][d0][1] - 1
                      for t in names if d0 in oc[t] and d1 in oc[t] and oc[t][d0][1] > 0]
                return sum(rs) / len(rs) if rs else 0.0
            nav_lo.append(nav_lo[-1] * (1 + basket_ret(held[1])))
            nav_hi.append(nav_hi[-1] * (1 + basket_ret(held[2])))
        ls = [1.0]
        for i in range(1, len(nav_lo)):
            rl = nav_lo[i] / nav_lo[i - 1] - 1
            rh = nav_hi[i] / nav_hi[i - 1] - 1
            ls.append(ls[-1] * (1 + rl - rh))
        return stats(nav_lo), stats(nav_hi), stats(ls)

    # benchmarks
    spy = {b[1]: b[5] for b in cache_fetch("SPY")}
    spy_nav = [spy[d] for d in win if d in spy]
    ew = []
    base = {t: oc[t][win[0]][1] for t in UNIV if win[0] in oc[t]}
    for d in win:
        vals = [oc[t][d][1] / base[t] for t in base if d in oc[t]]
        ew.append(sum(vals) / len(vals) if vals else 1.0)

    rC = stats(long_leg("open", COST))
    rB = stats(long_leg("open", 0.0))
    rA = stats(long_leg("close", 0.0))
    r15 = stats(long_leg("open", 0.0015))          # 15 bps stress leg
    lo_s, hi_s, ls_s = spread()
    bspy, bew = stats(spy_nav), stats(ew)

    print(f"X2 days-to-cover | window {win[0]}..{win[-1]} ({len(win)} sessions); "
          f"cycles {len(entries)}; K={K}; lag={LAG}")
    print(f"\n{'leg':26}{'CAGR':>9}{'maxDD':>8}{'Sharpe':>8}")
    for name, s in [("long-only  C next-open+5bps", rC),
                    ("long-only  B next-open 0bps", rB),
                    ("long-only  A c2c 0bps", rA),
                    ("long-only  15bps stress", r15),
                    ("SPY buy-hold", bspy),
                    ("EW-39 buy-hold", bew),
                    ("spread low-K (long)", lo_s),
                    ("spread high-K (short leg)", hi_s),
                    ("long-short SPREAD", ls_s)]:
        print(f"{name:26}{s['cagr']*100:>8.2f}%{s['mdd']*100:>7.1f}%{s['sharpe']:>8.2f}")

    # verdict (MODIFIED-WINDOW CAP: PROMISING max)
    beats = (rC["cagr"] > bspy["cagr"] and rC["cagr"] > bew["cagr"]
             and rC["sharpe"] > bspy["sharpe"] and rC["sharpe"] > bew["sharpe"])
    sign_ok = ls_s["cagr"] > 0
    floor = len(entries) >= 20
    print(f"\n=== VERDICT (prereg prereg_x2_days_to_cover.md; PROMISING-capped) ===")
    print(f"  cycles {len(entries)} (>=20: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  long-only C beats BOTH SPY & EW on CAGR+Sharpe: {beats}")
    print(f"  existence spread (low-high) positive sign: {sign_ok} "
          f"(spread CAGR {ls_s['cagr']*100:+.2f}%)")
    if not floor:
        v = "INCONCLUSIVE"
    elif beats and sign_ok:
        v = "PROMISING (forward-only; single window, cannot claim PASS-HR/RA)"
    else:
        v = "FAIL (clean - days-to-cover long idea closed for this universe)"
    print(f"\n  X2 VERDICT: {v}")


if __name__ == "__main__":
    main()
