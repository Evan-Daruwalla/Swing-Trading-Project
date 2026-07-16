"""M10-2 - Gap-Amortized Stress IBS, per prereg prereg_m10_2_gap_amortized_ibs.md
(committed doc-only before this runner).

Attacks the overnight-gap killer that ended the IBS family. State machine on QQQ:
STRESS (VIX>20) + oversold (IBS<=0.20) -> buy synthetic-2x QQQ at next open, hold
until IBS>=0.80 OR 5 sessions (time-stop); else VIX<=20 -> QQQ 200DMA trend
fallback; else cash. 1bp/side. 5-session hold amortizes the lost first-night gap;
stress-only entry concentrates the edge. Full window, D1. IN-SAMPLE-COMPOSED
(M10 cap - a pass = forward-paper-required). No swing.db writes.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED. 2x = E6 synth/calib (drag
QLD-calibrated). No look-ahead (signal close t -> execute open t+1).

NAV (finding-things map): imports run_e18_regime_gates (macro_close, sma);
run_e6_deleveraged (calib, synth); run_e8_squeeze (CAP0); swing_bot
(prices); swing_bot.signals (ibs). Imported by: no other module (standalone
runner).
"""
import bisect
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from swing_bot import prices
from swing_bot.signals import ibs
from run_e8_squeeze import CAP0
from run_e6_deleveraged import synth, calib
from run_e18_regime_gates import macro_close, sma

QCOST = 0.0001          # 1 bp/side
GATE = ("2000-01-01", "2013-12-31")
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
    qb = prices.fetch("QQQ", start="1999-01-01")
    qd = [b[1] for b in qb]
    qo = {b[1]: b[2] for b in qb}
    qh = {b[1]: b[3] for b in qb}
    ql = {b[1]: b[4] for b in qb}
    qc = {b[1]: b[5] for b in qb}
    qcl = [b[5] for b in qb]
    dma = dict(zip(qd, sma(qcl, 200)))
    qld = {b[1]: b[5] for b in prices.fetch("QLD", start="2007-01-01")}
    qqq_oc = [(b[1], b[2], b[5]) for b in qb]
    d2, qld_cagr, syn_cagr = calib(qqq_oc, qld, 2.0)
    syn2 = synth(qqq_oc, 2.0, d2)          # {d: (open_lvl, close_lvl)}
    print(f"2x calib: QLD overlap CAGR {qld_cagr*100:.2f}% drag {d2*100:.2f}%/yr "
          f"synth {syn_cagr*100:.2f}%")
    vix = macro_close("^VIX"); vd = sorted(vix)

    def vix_at(d):
        i = bisect.bisect_right(vd, d) - 1
        return vix[vd[i]] if i >= 0 else None

    def run(qcost, c2c):
        cash, state, held, entry_i, pend = CAP0, "cash", 0.0, None, None
        navd, mr_entries = {}, []
        for i, d in enumerate(qd):
            pd = qd[i - 1] if i > 0 else d
            mr_fill = syn2[pd][1] if c2c else syn2[d][0]
            tr_fill = qc[pd] if c2c else qo[d]
            if pend is not None and pend != state:
                if state == "mr":
                    cash += held * mr_fill * (1 - qcost)
                elif state == "trend":
                    cash += held * tr_fill * (1 - qcost)
                held = 0.0
                if pend == "mr" and mr_fill > 0:
                    held = cash / (mr_fill * (1 + qcost)); cash = 0.0
                    entry_i = i; mr_entries.append(d)
                elif pend == "trend" and tr_fill > 0:
                    held = cash / (tr_fill * (1 + qcost)); cash = 0.0
                state = pend; pend = None
            navd[d] = (cash + held * syn2[d][1] if state == "mr"
                       else cash + held * qc[d] if state == "trend" else cash)
            ib = ibs(qh[d], ql[d], qc[d])
            v = vix_at(d)
            if state == "mr":
                if (ib is not None and ib >= 0.80) or (entry_i is not None and i - entry_i >= 5):
                    pend = "cash"
            else:
                if v is not None and v > 20.0 and ib is not None and ib <= 0.20:
                    pend = "mr"
                elif v is not None and v <= 20.0:
                    want = "trend" if (dma.get(d) is not None and qc[d] > dma[d]) else "cash"
                    if want != state:
                        pend = want
                elif state != "cash":
                    pend = "cash"
        return navd, mr_entries

    spy = {b[1]: b[5] for b in prices.fetch("SPY", start="1999-01-01")}

    def report(tag, qcost, c2c):
        navd, me = run(qcost, c2c)
        rows = {}
        for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
            nav = [navd[d] for d in qd if lo <= d <= hi]
            qseg = [qc[d] for d in qd if lo <= d <= hi]
            sseg = [spy[d] for d in sorted(spy) if lo <= d <= hi]
            rows[wn] = (stats(nav), stats([q / qseg[0] for q in qseg]),
                        stats([s / sseg[0] for s in sseg]),
                        sum(1 for d in me if lo <= d <= hi))
        g = rows["gate"]; s = rows["sec"]
        print(f"{tag:26} gate {g[0]['cagr']*100:6.2f}%/DD{g[0]['mdd']*100:5.1f}%/Sh{g[0]['sharpe']:5.2f}"
              f" | sec {s[0]['cagr']*100:6.2f}%/DD{s[0]['mdd']*100:5.1f}%/Sh{s[0]['sharpe']:5.2f}"
              f" (gate MR={g[3]})")
        return rows

    print(f"\nGap-Amortized Stress IBS | 2x QQQ MR (VIX>20 & IBS<=0.20), 5d/IBS>=0.8 exit\n")
    rows = report("C next-open 1bp MAIN", QCOST, False)
    report("B c2c 0bp (E2-gap upper)", 0.0, True)
    report("C stress 5bp", 0.0005, False)

    g, gq, gs, ng = rows["gate"]; s, sq, ss, _ = rows["sec"]
    print(f"\nbenchmarks gate: QQQ {gq['cagr']*100:.2f}%/{gq['sharpe']:.2f}  "
          f"SPY {gs['cagr']*100:.2f}%/{gs['sharpe']:.2f}")
    print(f"benchmarks sec:  QQQ {sq['cagr']*100:.2f}%/{sq['sharpe']:.2f}  "
          f"SPY {ss['cagr']*100:.2f}%/{ss['sharpe']:.2f}")

    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gq["sharpe"] and s["sharpe"] > sq["sharpe"]
          and g["cagr"] > 0 and s["cagr"] > 0)
    floor = ng >= 20
    print(f"\n=== D1 VERDICT (prereg prereg_m10_2_gap_amortized_ibs.md; IN-SAMPLE-COMPOSED) ===")
    print(f"  gate MR entries {ng} (>=20: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR   [{'PASS' if ra else 'fail'}] "
          f"PASS-RA (gate Sharpe {g['sharpe']:.2f} vs QQQ {gq['sharpe']:.2f})")
    if not floor:
        v = "INCONCLUSIVE"
    elif hr or ra:
        v = (f"{'PASS-HR' if hr else 'PASS-RA'} - IN-SAMPLE-COMPOSED; FORWARD PAPER "
             f"REQUIRED, not a clean pass")
    else:
        v = "FAIL (gap-amortized stress IBS does not clear either tier)"
    print(f"\n  M10-2 VERDICT: {v}")


if __name__ == "__main__":
    main()
