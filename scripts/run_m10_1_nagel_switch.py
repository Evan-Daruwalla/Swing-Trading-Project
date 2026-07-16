"""M10-1 - Nagel Switch: VIX-gated residual reversal / trend rotation.
Per prereg prereg_m10_1_nagel_switch.md (committed doc-only before this runner).

Weekly regime: VIX close > 20 -> STRESS = C1 residual reversal (bottom-K=4 FF3
residual, verbatim C1 machinery); VIX <= 20 -> CALM = E6 trend (long QQQ iff
QQQ>200DMA else cash). Decisions at ISO-week-end close, executed next open,
held one week. 5bps/side stocks, 1bp/side QQQ. Full window (VIX 1990+, no cap).
D1 dual-bar. IN-SAMPLE-COMPOSED (M10 snooping disclosure) - a pass = forward
paper REQUIRED, never clean. No swing.db writes.

DATA CONVENTION: prices split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): stitches four modules — `cache_fetch, COST, CAP0` <-
run_e8_squeeze (shared data); `macro_close, sma` <- run_e18_regime_gates;
`ff3_daily, residual_series, isoweek, stats, K, BETA_N, FORM_N` <-
run_c1_residual_reversal (the verbatim STRESS machinery); `UNIV` (39-name
survivor list) <- run_e10_earnings_drift. LIVE forward-paper twin:
swing_bot.paper_sleeves.decide_m10_1.
"""
import bisect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e10_earnings_drift import UNIV
from run_c1_residual_reversal import (ff3_daily, residual_series, isoweek, stats,
                                      K, BETA_N, FORM_N, GATE, SEC)
from run_e18_regime_gates import macro_close, sma

QCOST = 0.0001          # 1 bp/side broad-ETF (QQQ)


def main():
    ff = ff3_daily()
    oc, tdates, forms = {}, {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        ds = [b[1] for b in bars]
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}
        tdates[t] = ds
        forms[t] = dict(zip(ds, residual_series(ds, [b[5] for b in bars], ff)))
    qbars = cache_fetch("QQQ")
    qo = {b[1]: b[2] for b in qbars}
    qc = {b[1]: b[5] for b in qbars}
    qd = [b[1] for b in qbars]
    qcl = [b[5] for b in qbars]
    q200 = dict(zip(qd, sma(qcl, 200)))
    vix = macro_close("^VIX")
    vd = sorted(vix)

    def vix_at(d):
        i = bisect.bisect_right(vd, d) - 1
        return vix[vd[i]] if i >= 0 else None

    master = sorted({d for t in UNIV for d in tdates[t]})
    weekend = set(master[i] for i in range(len(master) - 1)
                  if isoweek(master[i]) != isoweek(master[i + 1]))
    idx = {t: {d: i for i, d in enumerate(tdates[t])} for t in UNIV}

    # carry-forward marks: a held position on a date it lacks a bar (holiday /
    # calendar-boundary, e.g. QQQ ends one session before some stocks) is marked
    # at its last known close, NOT zero. Trading still only happens on real bars.
    qcd = sorted(qc)

    def qc_at(d):
        i = bisect.bisect_right(qcd, d) - 1
        return qc[qcd[i]] if i >= 0 else 0.0

    scd = {t: sorted(oc[t]) for t in UNIV}

    def sc_at(t, d):
        lst = scd[t]; i = bisect.bisect_right(lst, d) - 1
        return oc[t][lst[i]][1] if i >= 0 else 0.0

    def run(scost, qcost, c2c, thr=20.0):
        cash, spos, qu, cur, pend = CAP0, {}, 0.0, "cash", None
        navd = {}
        stress_entries = []

        def spx(t, d):
            i = idx[t][d]
            if c2c and i > 0:
                return oc[t][tdates[t][i - 1]][1]
            return oc[t][d][0]

        for d in master:
            if pend is not None:
                mode, payload = pend
                # liquidate everything held
                for t in list(spos):
                    if d in oc[t]:
                        cash += spos[t] * spx(t, d) * (1 - scost); del spos[t]
                if qu > 0 and d in qo:
                    cash += qu * qo[d] * (1 - qcost); qu = 0.0
                navv = cash
                if mode == "stress":
                    per = navv / K
                    for t in payload:
                        if d in oc[t] and spx(t, d) > 0:
                            sh = per / (spx(t, d) * (1 + scost))
                            cash -= sh * spx(t, d) * (1 + scost); spos[t] = sh
                    stress_entries.append(d)
                elif mode == "trend_on" and d in qo and qo[d] > 0:
                    u = navv / (qo[d] * (1 + qcost))
                    cash -= u * qo[d] * (1 + qcost); qu = u
                cur = mode
                pend = None
            navd[d] = (cash + sum(spos[t] * sc_at(t, d) for t in spos)
                       + (qu * qc_at(d) if qu > 0 else 0.0))
            if d in weekend:
                v = vix_at(d)
                if v is not None and v > thr:
                    ranked = sorted((forms[t].get(d), t) for t in UNIV
                                    if forms[t].get(d) is not None)
                    if len(ranked) >= K:
                        pend = ("stress", [t for _, t in ranked[:K]])
                elif d in q200 and q200[d] is not None and qc[d] > q200[d]:
                    if cur != "trend_on":
                        pend = ("trend_on", None)
                else:
                    if cur != "cash":
                        pend = ("cash", None)
        return navd, stress_entries

    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def report(tag, scost, qcost, c2c, thr=20.0):
        navd, se = run(scost, qcost, c2c, thr)
        rows = {}
        for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
            nav = [navd[d] for d in master if lo <= d <= hi]
            seg = [d for d in sorted(spy) if lo <= d <= hi]
            ew = []
            for d in master:
                if lo <= d <= hi:
                    vals = [oc[t][d][1] / oc[t][tdates[t][0]][1]
                            for t in UNIV if d in oc[t]]
                    ew.append(sum(vals) / len(vals))
            rows[wn] = (stats(nav), stats([spy[d] / spy[seg[0]] for d in seg]),
                        stats(ew), sum(1 for d in se if lo <= d <= hi))
        g = rows["gate"]; s = rows["sec"]
        print(f"{tag:26} gate {g[0]['cagr']*100:6.2f}%/DD{g[0]['mdd']*100:5.1f}%/Sh{g[0]['sharpe']:5.2f}"
              f" | sec {s[0]['cagr']*100:6.2f}%/DD{s[0]['mdd']*100:5.1f}%/Sh{s[0]['sharpe']:5.2f}"
              f" (gate stress-wk={g[3]})")
        return rows

    print(f"Nagel Switch | VIX>20 -> C1 reversal (K={K}) / else QQQ 200DMA trend\n")
    rows = report("C (5bps stk/1bp QQQ) MAIN", COST, QCOST, False)
    report("B (next-open 0bps)", 0.0, 0.0, False)
    report("A (c2c stocks 0bps)", 0.0, 0.0, True)
    report("C stress 15bps stocks", 0.0015, QCOST, False)

    g, gs, gew, ng = rows["gate"]; s, ss, sew, _ = rows["sec"]
    print(f"\nbenchmarks gate: SPY {gs['cagr']*100:.2f}%/{gs['sharpe']:.2f}  "
          f"EW-39 {gew['cagr']*100:.2f}%/{gew['sharpe']:.2f}")
    print(f"benchmarks sec:  SPY {ss['cagr']*100:.2f}%/{ss['sharpe']:.2f}  "
          f"EW-39 {sew['cagr']*100:.2f}%/{sew['sharpe']:.2f}")

    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gs["sharpe"] and s["sharpe"] > ss["sharpe"]
          and g["cagr"] > 0 and s["cagr"] > 0)
    floor = ng >= 30
    print(f"\n=== D1 VERDICT (prereg prereg_m10_1_nagel_switch.md; IN-SAMPLE-COMPOSED) ===")
    print(f"  gate stress-weeks {ng} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR   [{'PASS' if ra else 'fail'}] "
          f"PASS-RA (gate Sharpe {g['sharpe']:.2f})")
    if not floor:
        v = "INCONCLUSIVE"
    elif hr or ra:
        v = (f"{'PASS-HR' if hr else 'PASS-RA'} - IN-SAMPLE-COMPOSED + survivor-flattered; "
             f"FORWARD PAPER REQUIRED, not a clean pass")
    else:
        v = "FAIL (Nagel Switch does not clear either tier)"
    print(f"\n  M10-1 VERDICT: {v}")

    # VIX threshold sensitivity (report-only, not verdict)
    print("\nVIX threshold sensitivity (report-only, C main costs):")
    for thr in (18.0, 22.0):
        report(f"  VIX>{thr:.0f}", COST, QCOST, False, thr)


if __name__ == "__main__":
    main()
