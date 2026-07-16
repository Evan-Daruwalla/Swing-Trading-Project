"""M11 - Algorithmic chart-pattern detection (long-side reversal), per prereg
prereg_m11_chart_patterns.md (committed doc-only BEFORE this runner, hash 9cb5ac5).

Rule-based (NOT LLM) detection of the classic long reversal shapes on the 39
survivor mega-caps: double-bottom OR inverse-head-and-shoulders, entered on a
FRESH upward neckline cross at close, executed next open, time-stop 20 sessions,
K=3, 5 bps/side (+15 bps stress). Causal close-based pivots (half-window w=5,
confirmed at j+w) -> no look-ahead (LMW's two-sided kernel is avoided). Full
window, D1 dual-bar. Survivor universe -> asymmetric: only a FAIL is clean.
Plus a REPORTED-not-gated short-side diagnostic (double-top / H&S forward
returns) documenting the Savin (2007) short effect = non-deployable (X2 lesson).

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False). Pivots
on close (b[5]); fills on open (b[2]); MTM on close. No swing.db writes.

NAV (finding-things map): imports `cache_fetch, COST, CAP0` <- run_e8_squeeze
and `UNIV` (39-name survivor list) <- run_e10_earnings_drift. Self-contained
detectors: causal pivots + detect() (long) / detect_short() (diagnostic).
RESULT = FAIL, 2026-07-14 (signal-dead; survivorship destroyed the edge) — NOT
forwarded to M3 paper. See docs/research/2026-07-14_M11_chart_patterns_results.md.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e10_earnings_drift import UNIV

W = 5                    # pivot half-window (causal confirm at j+W)
K = 3
HOLD = 20                # time-stop baseline (sessions); 10/40 = descriptive
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
BOT_TOL = 0.04           # double-bottom: two bottoms within 4%
PEAK_MIN = 1.05          # intervening peak >= 5% above the higher bottom
HEAD_DEPTH = 0.97        # iH&S: head <= 97% of min(shoulders) (>=3% below)
SHO_TOL = 0.06           # shoulders within 6%
SPAN_MIN, SPAN_MAX = 10, 90
RECENCY = 30             # last trough within 30 sessions of the break
HOLDS_REPORT = (10, 20, 40)


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


def pivots(cl, w):
    """Causal alternating swing highs/lows on close. Each pivot at idx j is
    known only at j+w. Returns (idx, 'H'/'L', price) in time order, alternating."""
    n = len(cl)
    raw = []
    for j in range(w, n - w):
        seg = cl[j - w:j + w + 1]
        if cl[j] == max(seg):
            raw.append((j, "H", cl[j]))
        elif cl[j] == min(seg):
            raw.append((j, "L", cl[j]))
    piv = []                         # dedupe to strictly alternating H/L
    for p in raw:
        if not piv:
            piv.append(p); continue
        if p[1] == piv[-1][1]:       # same type run -> keep the more extreme
            if (p[1] == "H" and p[2] > piv[-1][2]) or (p[1] == "L" and p[2] < piv[-1][2]):
                piv[-1] = p
        else:
            piv.append(p)
    return piv


def detect(conf, cl, i):
    """Long reversal completion at bar i using pivots confirmed by i. Returns
    breakout strength (>0) if a fresh upward neckline cross fires, else 0.0."""
    if i < 1 or len(conf) < 3:
        return 0.0
    # inverse head-and-shoulders (last 5 pivots: L H L H L)
    if len(conf) >= 5:
        ls, p1, head, p2, rs = conf[-5:]
        if ([ls[1], p1[1], head[1], p2[1], rs[1]] == ["L", "H", "L", "H", "L"]
                and min(ls[2], rs[2]) > 0 and p2[0] != p1[0]
                and head[2] <= HEAD_DEPTH * min(ls[2], rs[2])
                and abs(ls[2] - rs[2]) / min(ls[2], rs[2]) <= SHO_TOL
                and SPAN_MIN <= head[0] - ls[0] <= SPAN_MAX
                and SPAN_MIN <= rs[0] - head[0] <= SPAN_MAX
                and i - rs[0] <= RECENCY):
            slope = (p2[2] - p1[2]) / (p2[0] - p1[0])
            neck_i = p1[2] + slope * (i - p1[0])
            neck_p = p1[2] + slope * (i - 1 - p1[0])
            if neck_i > 0 and cl[i] > neck_i and cl[i - 1] <= neck_p:
                return cl[i] / neck_i - 1
    # double bottom (last 3 pivots: L H L)
    t1, pk, t2 = conf[-3:]
    if ([t1[1], pk[1], t2[1]] == ["L", "H", "L"] and min(t1[2], t2[2]) > 0
            and abs(t2[2] - t1[2]) / min(t1[2], t2[2]) <= BOT_TOL
            and pk[2] >= PEAK_MIN * max(t1[2], t2[2])
            and SPAN_MIN <= t2[0] - t1[0] <= SPAN_MAX
            and i - t2[0] <= RECENCY):
        neck = pk[2]
        if cl[i] > neck and cl[i - 1] <= neck:
            return cl[i] / neck - 1
    return 0.0


def detect_short(conf, cl, i):
    """Bearish mirror (double-top / H&S), fresh DOWNWARD neckline cross. For the
    reported short-side DIAGNOSTIC only (never traded)."""
    if i < 1 or len(conf) < 3:
        return 0.0
    if len(conf) >= 5:
        ls, p1, head, p2, rs = conf[-5:]
        if ([ls[1], p1[1], head[1], p2[1], rs[1]] == ["H", "L", "H", "L", "H"]
                and min(ls[2], rs[2]) > 0 and p2[0] != p1[0]
                and head[2] >= (2 - HEAD_DEPTH) * max(ls[2], rs[2])
                and abs(ls[2] - rs[2]) / min(ls[2], rs[2]) <= SHO_TOL
                and SPAN_MIN <= head[0] - ls[0] <= SPAN_MAX
                and SPAN_MIN <= rs[0] - head[0] <= SPAN_MAX
                and i - rs[0] <= RECENCY):
            slope = (p2[2] - p1[2]) / (p2[0] - p1[0])
            neck_i = p1[2] + slope * (i - p1[0])
            neck_p = p1[2] + slope * (i - 1 - p1[0])
            if neck_i > 0 and cl[i] < neck_i and cl[i - 1] >= neck_p:
                return 1 - cl[i] / neck_i
    t1, tr, t2 = conf[-3:]
    if ([t1[1], tr[1], t2[1]] == ["H", "L", "H"] and min(t1[2], t2[2]) > 0
            and abs(t2[2] - t1[2]) / min(t1[2], t2[2]) <= BOT_TOL
            and tr[2] <= (2 - PEAK_MIN) * min(t1[2], t2[2])
            and SPAN_MIN <= t2[0] - t1[0] <= SPAN_MAX
            and i - t2[0] <= RECENCY):
        neck = tr[2]
        if cl[i] < neck and cl[i - 1] >= neck:
            return 1 - cl[i] / neck
    return 0.0


def signals_for(cl, fn):
    piv = pivots(cl, W)
    out, conf, ptr, n = {}, [], 0, len(cl)
    for i in range(1, n):
        while ptr < len(piv) and piv[ptr][0] + W <= i:
            conf.append(piv[ptr]); ptr += 1
        s = fn(conf, cl, i)
        if s > 0:
            out[i] = s
    return out


def main():
    oc, tdates, cls, sigs = {}, {}, {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        ds = [b[1] for b in bars]
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = ds
        cls[t] = [b[5] for b in bars]
        sigs[t] = signals_for(cls[t], detect)
    master = sorted({d for t in UNIV for d in tdates[t]})
    lidx = {t: {d: i for i, d in enumerate(tdates[t])} for t in UNIV}
    total_sig = sum(len(sigs[t]) for t in UNIV)
    print(f"long-signal completions across 39 names: {total_sig}", flush=True)

    def run(cost, c2c, hold=HOLD):
        cash, pos, pend = CAP0, {}, []
        navd, entries, dropped = {}, [], 0

        def fpx(t, d):
            i = lidx[t][d]
            return oc[t][tdates[t][i - 1]][1] if (c2c and i > 0) else oc[t][d][0]

        for m, d in enumerate(master):
            for t in list(pos):
                sh, em = pos[t]
                if m - em >= hold and d in oc[t]:
                    cash += sh * fpx(t, d) * (1 - cost); del pos[t]
            if pend:
                navop = cash + sum(pos[t][0] * oc[t][d][0] for t in pos if d in oc[t])
                per = navop / K
                for t, _ in pend:
                    if len(pos) < K and t not in pos and d in oc[t] and fpx(t, d) > 0:
                        spend = min(cash, per)
                        if spend > 0:
                            sh = spend / (fpx(t, d) * (1 + cost))
                            cash -= sh * fpx(t, d) * (1 + cost); pos[t] = (sh, m)
                            entries.append(d)
                pend = []
            navd[d] = cash + sum(pos[t][0] * oc[t][d][1] for t in pos if d in oc[t])
            cand = []
            for t in UNIV:
                if t in pos:
                    continue
                i = lidx[t].get(d)
                if i is not None and i in sigs[t]:
                    cand.append((sigs[t][i], t))
            if cand:
                cand.sort(reverse=True)
                slots = max(0, K - len(pos))
                for k, (s, t) in enumerate(cand):
                    if k < slots:
                        pend.append((t, s))
                    else:
                        dropped += 1
        return navd, entries, dropped

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def report(tag, cost, c2c, hold=HOLD):
        navd, entries, dropped = run(cost, c2c, hold)
        rows = {}
        for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
            nav = [navd[d] for d in master if lo <= d <= hi]
            seg = [d for d in sorted(spy) if lo <= d <= hi]
            ew = []
            for d in master:
                if lo <= d <= hi:
                    vals = [oc[t][d][1] / oc[t][tdates[t][0]][1]
                            for t in UNIV if d in oc[t]]
                    if vals:
                        ew.append(sum(vals) / len(vals))
            rows[wn] = (stats(nav), stats([spy[d] / spy[seg[0]] for d in seg]),
                        stats(ew), sum(1 for d in entries if lo <= d <= hi))
        g = rows["gate"]; s = rows["sec"]
        print(f"{tag:26} gate {g[0]['cagr']*100:6.2f}%/DD{g[0]['mdd']*100:5.1f}%/Sh{g[0]['sharpe']:5.2f}"
              f" | sec {s[0]['cagr']*100:6.2f}%/DD{s[0]['mdd']*100:5.1f}%/Sh{s[0]['sharpe']:5.2f}"
              f" (gate n={g[3]}, drop={dropped})")
        return rows

    print("\nM11 chart patterns | long reversal (double-bottom + inv-H&S), K=3, hold 20\n")
    rows = report("C next-open 5bps MAIN", COST, False)
    report("B next-open 0bps", 0.0, False)
    report("A c2c 0bps (upper)", 0.0, True)
    report("C stress 15bps", 0.0015, False)
    print("  --- hold sensitivity (descriptive, next-open 5bps) ---")
    for h in HOLDS_REPORT:
        if h != HOLD:
            report(f"C hold={h}", COST, False, h)

    g, gs, gew, ng = rows["gate"]; s, ss, sew, _ = rows["sec"]
    print(f"\nbenchmarks gate: SPY {gs['cagr']*100:.2f}%/{gs['sharpe']:.2f}  "
          f"EW-39 {gew['cagr']*100:.2f}%/{gew['sharpe']:.2f}")
    print(f"benchmarks sec:  SPY {ss['cagr']*100:.2f}%/{ss['sharpe']:.2f}  "
          f"EW-39 {sew['cagr']*100:.2f}%/{sew['sharpe']:.2f}")

    # short-side diagnostic (reported, NOT gated)
    def fwd20(kind):
        rets = []
        for t in UNIV:
            cl = cls[t]
            sg = signals_for(cl, detect_short if kind == "short" else detect)
            for i in sg:
                if i + 20 < len(cl) and cl[i] > 0:
                    rets.append(cl[i + 20] / cl[i] - 1)
        return (sum(rets) / len(rets) if rets else float("nan")), len(rets)
    uncond = []
    for t in UNIV:
        cl = cls[t]
        uncond += [cl[i + 20] / cl[i] - 1 for i in range(len(cl) - 20) if cl[i] > 0]
    bmu, bn = fwd20("long"); smu, sn = fwd20("short")
    umu = sum(uncond) / len(uncond)
    print(f"\n--- short-side diagnostic (fwd-20-session close return; NOT traded) ---")
    print(f"  after LONG-reversal completion : {bmu*100:+.2f}% (n={bn})")
    print(f"  after SHORT (top/H&S) completion: {smu*100:+.2f}% (n={sn})")
    print(f"  unconditional                  : {umu*100:+.2f}%")
    print(f"  (Savin 2007 = bearish underperforms; deployable only via shorting -> X2 wall)")

    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gs["sharpe"] and s["sharpe"] > ss["sharpe"]
          and g["cagr"] > 0 and s["cagr"] > 0)
    floor = ng >= 30
    print(f"\n=== D1 VERDICT (prereg prereg_m11_chart_patterns.md; asymmetric) ===")
    print(f"  gate entries {ng} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR   [{'PASS' if ra else 'fail'}] "
          f"PASS-RA (gate Sharpe {g['sharpe']:.2f} vs SPY {gs['sharpe']:.2f})")
    if not floor:
        v = "INCONCLUSIVE (below entry floor)"
    elif hr or ra:
        v = f"{'PASS-HR' if hr else 'PASS-RA'} (UNINTERPRETABLE - survivorship; forward only)"
    else:
        v = "FAIL (long-side chart patterns do not clear either tier)"
    print(f"\n  M11 VERDICT: {v}")


if __name__ == "__main__":
    main()
