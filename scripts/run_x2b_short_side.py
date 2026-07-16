"""X2b - short-side / long-short days-to-cover, borrow-costed.
Per prereg prereg_x2b_short_side.md (committed e718f6f, predates this runner).

Reuses the X2 FINRA short-interest cache + universe. Two strategies, K=5,
biweekly rebalance, next-open fills, 5 bps/side trading:
  SHORT  - short the K highest-DTC names (1x short)
  LS     - dollar-neutral $1 long lowest-DTC + $1 short highest-DTC (2x gross)
Short accounting is real: shorting receives proceeds, owes a liability marked
daily, and accrues a BORROW FEE swept 0/2/5/10/20%/yr on short market value
(real per-name borrow is paid data, Evan-gated). Single 2018-2026 window ->
MODIFIED-WINDOW CAP: best verdict = PROMISING. No swing.db writes.

DATA CONVENTION: prices split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): imports ingest_finra_short_interest (OUT, UNIV);
run_e8_squeeze (CAP0, COST, cache_fetch). Imported by: no other module
(standalone runner).
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
LAG = 10
SWEEP = [0.0, 0.02, 0.05, 0.10, 0.20]     # annualized borrow on short notional


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


def build():
    si = json.loads(OUT.read_text())
    oc, tdates = {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = [b[1] for b in bars]
    master = sorted({d for t in UNIV for d in tdates[t]})
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
    return oc, master, entries


def sim(oc, master, entries, mode, borrow, tcost=COST):
    """mode 'ls' (dollar-neutral 1x/1x) or 'short' (1x short). Share-based with
    real short proceeds/liability + daily borrow accrual on short MV. Rebalances
    only the DELTA (continuers keep their shares; charge cost on |delta| only)."""
    ecal = {e[0]: e for e in entries}
    start = entries[0][0]
    win = [d for d in master if d >= start]
    cash, nav_prev = CAP0, CAP0
    lsh, ssh = {}, {}            # long / short shares (both stored positive)

    def rebal(cur, names, d, sign, nav, tcost):
        nonlocal cash
        tgt = {t: (nav / K) / oc[t][d][0] for t in names
               if d in oc[t] and oc[t][d][0] > 0}
        for t in set(cur) | set(tgt):
            if d not in oc[t]:
                continue
            op = oc[t][d][0]
            delta = tgt.get(t, 0.0) - cur.get(t, 0.0)     # +buy / -sell (shares)
            if sign > 0:                                   # long leg
                cash -= delta * op + abs(delta) * op * tcost
            else:                                          # short leg
                cash += delta * op - abs(delta) * op * tcost
            if tgt.get(t, 0.0) == 0.0:
                cur.pop(t, None)
            else:
                cur[t] = tgt[t]

    navd = {}
    for d in win:
        smv = sum(ssh[t] * oc[t][d][1] for t in ssh if d in oc[t])
        cash -= smv * borrow / 252.0                      # borrow accrual
        if d in ecal:
            _, lo, hi = ecal[d]
            rebal(lsh, lo if mode == "ls" else [], d, +1, nav_prev, tcost)
            rebal(ssh, hi, d, -1, nav_prev, tcost)
        lmv = sum(lsh[t] * oc[t][d][1] for t in lsh if d in oc[t])
        smv = sum(ssh[t] * oc[t][d][1] for t in ssh if d in oc[t])
        nav_prev = cash + lmv - smv
        navd[d] = nav_prev
    return [navd[d] for d in win]


def per_year(win_dates, nav):
    out = {}
    for i in range(1, len(nav)):
        y = win_dates[i][:4]
        out.setdefault(y, [1.0, None])
    # rebuild properly: group by year, compound daily returns
    years = {}
    for i in range(1, len(nav)):
        if nav[i - 1] <= 0:
            continue
        y = win_dates[i][:4]
        years.setdefault(y, 1.0)
        years[y] *= nav[i] / nav[i - 1]
    return {y: v - 1 for y, v in years.items()}


def main():
    oc, master, entries = build()
    start = entries[0][0]
    win = [d for d in master if d >= start]
    print(f"X2b short-side | window {win[0]}..{win[-1]} ({len(win)} sessions); "
          f"cycles {len(entries)}; K={K}; lag={LAG}")

    # cost ladder + borrow sweep
    print(f"\n{'strategy':10}{'borrow':>8}{'CAGR':>9}{'maxDD':>8}{'Sharpe':>8}")
    gross_ls = stats(sim(oc, master, entries, "ls", 0.0, tcost=0.0))
    print(f"{'LS gross':10}{'0(+0bps)':>8}{gross_ls['cagr']*100:>8.2f}%"
          f"{gross_ls['mdd']*100:>7.1f}%{gross_ls['sharpe']:>8.2f}")
    ls_by_borrow = {}
    for b in SWEEP:
        s = stats(sim(oc, master, entries, "ls", b))
        ls_by_borrow[b] = s
        print(f"{'LS':10}{b*100:>6.0f}%{'':>1}{s['cagr']*100:>8.2f}%"
              f"{s['mdd']*100:>7.1f}%{s['sharpe']:>8.2f}")
    for b in SWEEP:
        s = stats(sim(oc, master, entries, "short", b))
        print(f"{'SHORT':10}{b*100:>6.0f}%{'':>1}{s['cagr']*100:>8.2f}%"
              f"{s['mdd']*100:>7.1f}%{s['sharpe']:>8.2f}")
    s15 = stats(sim(oc, master, entries, "ls", 0.05, tcost=0.0015))
    print(f"{'LS 15bps':10}{'5%':>8}{s15['cagr']*100:>8.2f}%"
          f"{s15['mdd']*100:>7.1f}%{s15['sharpe']:>8.2f}")

    # borrow breakeven (net CAGR -> 0) for LS, bisection on borrow
    lo_b, hi_b = 0.0, 1.0
    for _ in range(40):
        mid = (lo_b + hi_b) / 2
        c = stats(sim(oc, master, entries, "ls", mid))["cagr"]
        if c > 0:
            lo_b = mid
        else:
            hi_b = mid
    breakeven = (lo_b + hi_b) / 2

    # robustness: per-year LS at 5% borrow
    nav5 = sim(oc, master, entries, "ls", 0.05)
    yr = per_year(win, nav5)
    pos_years = sum(1 for v in yr.values() if v > 0)
    print(f"\nborrow breakeven (LS net CAGR->0): {breakeven*100:.1f}%/yr")
    print(f"per-year LS @5% borrow ({pos_years}/{len(yr)} positive):")
    for y in sorted(yr):
        print(f"  {y}: {yr[y]*100:+6.1f}%")

    # short-leg name concentration: mean fwd biweekly return of each name while
    # in the high-DTC basket (annualized), + selection frequency
    ecal = {e[0]: e for e in entries}
    edates = sorted(ecal)
    name_rets, name_cnt = {}, {}
    for i, d in enumerate(edates):
        nxt = edates[i + 1] if i + 1 < len(edates) else win[-1]
        for t in ecal[d][2]:
            if d in oc[t] and nxt in oc[t] and oc[t][d][1] > 0:
                r = oc[t][nxt][1] / oc[t][d][1] - 1
                name_rets.setdefault(t, []).append(r)
                name_cnt[t] = name_cnt.get(t, 0) + 1
    conc = sorted(name_rets, key=lambda t: len(name_rets[t]), reverse=True)
    print(f"\nshort-leg (high-DTC) name concentration - top by selection freq:")
    print(f"  {'name':6}{'cycles':>7}{'mean fwd 2wk ret':>18}{'~annualized':>13}")
    for t in conc[:8]:
        rs = name_rets[t]
        m = sum(rs) / len(rs)
        ann = (1 + m) ** 26 - 1
        print(f"  {t:6}{len(rs):>7}{m*100:>17.2f}%{ann*100:>12.1f}%")

    # verdict (MODIFIED-WINDOW CAP; market-neutral bar at 5% borrow)
    ls5 = ls_by_borrow[0.05]
    floor = len(entries) >= 20
    robust = pos_years / max(1, len(yr)) >= 0.70
    ok = ls5["cagr"] > 0 and ls5["sharpe"] >= 0.80 and robust
    print(f"\n=== VERDICT (prereg prereg_x2b_short_side.md; PROMISING-capped) ===")
    print(f"  cycles {len(entries)} (>=20: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  LS @5% borrow: CAGR {ls5['cagr']*100:.2f}% (>0), "
          f"Sharpe {ls5['sharpe']:.2f} (>=0.80: {ls5['sharpe']>=0.80}), "
          f"years+ {pos_years}/{len(yr)} (>=70%: {robust})")
    print(f"  borrow breakeven {breakeven*100:.1f}%/yr")
    if not floor:
        v = "INCONCLUSIVE"
    elif ok:
        v = "PROMISING (forward-only; market-neutral; single window; needs real borrow data)"
    else:
        v = "FAIL (short-side not capturable under the pre-registered bar)"
    print(f"\n  X2b VERDICT: {v}")


if __name__ == "__main__":
    main()
