r"""Entry-leg vs exit-leg split of M10-1's timing gap, both branches.

    set SWING_ALLOW_STALE_CACHE=1
    .venv\Scripts\python.exe scripts\ablation_m10_1_entry_exit_legs.py

DATA CONVENTION. Prices SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED (auto_adjust=False),
inherited from the shared .e8e9_cache via run_e8_squeeze.cache_fetch. This
UNDERSTATES every overnight leg by the whole dividend yield, because on
dividend-unadjusted prices the ex-dividend drop falls entirely in the
close[t-1]->open[t] window (record GD sec. 4). All legs are affected in the same
direction, so DIFFERENCES between them are far more robust than their levels.

DIAGNOSTIC. No PASS/FAIL, no D1 verdict, nothing deployed, ATTEMPT TALLY
UNCHANGED (precedent EX-DECOMP record DU/M12, X9's zero-cost split, GD, GF). It
does not reopen the closed search phase and tunes nothing: every M10-1 parameter
is imported from the runner, never restated. M10-1's runner is NOT edited -- it
is the live m10_1_nagel paper sleeve's backtest of record.

WHY. M10-1 is the sleeve actually running in paper, and the pair everything
quotes -- "c2c 22.82% -> next-open 17.87%, ~5pp in the overnight gap" (record
Appendix CI caveat 5) -- is M10-1's, not C1's (record GF sec. 1). Two things are
wrong with how it has been used, both visible in the runner's own output:

  1. IT IS NOT A TIMING DELTA. 22.82% is Rung A at 0 bps; 17.87% is Rung C at
     5 bps stocks / 1 bp QQQ. The runner also prints Rung B (next-open, 0 bps) =
     20.77%, which the caveat skips. So the gap splits as TIMING 2.04 pp (A->B)
     and COST 2.90 pp (B->C), totalling 4.94 pp. Most of the "overnight gap" is
     cost. Those three are the runner's own full-precision differences, printed
     below; subtracting the 2-dp rung DISPLAYS instead gives 2.05 and 4.95, and
     an earlier version of this docstring quoted those (audit GJ LOW). Derive
     from the printed split, never from the displayed rungs.
  2. RUNG A IS STOCKS-ONLY. run_m10_1_nagel_switch.py:157 labels it "A (c2c
     stocks 0bps)" and means it: spx() (:87) carries the c2c flag, but the QQQ
     legs read qo[d] directly at :101 (exit) and :112 (entry). There is no
     qpx(). Since the Nagel Switch holds QQQ or cash in every non-stress week,
     the recorded timing delta is a STRESS-BRANCH-ONLY number.

This splits the timing term into its entry and exit legs, on BOTH branches,
using the identity established in GF: for any trade,

    c2c - next_open  =  entry_overnight - exit_overnight

so a flag that moves both fills at once reports the NET and hides whichever leg
is larger.

WHAT THIS CAN AND CANNOT DO:
  * It CAN pin two cells exactly. The as-run cell must reproduce the runner's
    Rung B, and the stocks-only-c2c cell must reproduce its Rung A. Both are
    asserted, not eyeballed.
  * It CANNOT self-validate the both-branches cells. M10-1 has never recorded a
    c2c number that includes the QQQ leg, so those cells reconcile against
    NOTHING. This is where GF's "asserted, not eyeballed" guarantee stops, and
    it is stated here rather than discovered later.
  * It does NOT carry GF's size_at_fill arm. M10-1 sets navv = cash AFTER
    liquidation (:102), so it already sizes off realized proceeds at the actual
    fill prices net of exit cost -- cleaner than C1, which marks at close(d)
    while filling elsewhere. That artifact is 0 pp here by construction.

NAV (finding-things map): imports run_m10_1_nagel_switch (QCOST); run_e8_squeeze
(cache_fetch, COST, CAP0); run_e10_earnings_drift (UNIV); run_c1_residual_reversal
(ff3_daily, residual_series, isoweek, stats, K, GATE, SEC); run_e18_regime_gates
(macro_close, sma). Imported by nothing. Writes nothing; swing.db never opened.
"""
import bisect
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# SWING_ALLOW_STALE_CACHE must be set EXTERNALLY. Setting it here, or wrapping
# cache_fetch in `except`, is the record-EO defect class. Let it propagate.
from run_e8_squeeze import CAP0, COST, cache_fetch  # noqa: E402
from run_e10_earnings_drift import UNIV  # noqa: E402
from run_c1_residual_reversal import (  # noqa: E402
    GATE, SEC, ff3_daily, isoweek, residual_series, stats,
)
from run_c1_residual_reversal import K  # noqa: E402
from run_e18_regime_gates import macro_close, sma  # noqa: E402
from run_m10_1_nagel_switch import QCOST  # noqa: E402

# M10-1's OWN printed rungs, gate window, as emitted by
# run_m10_1_nagel_switch.py. These are what the two pinnable cells must
# reproduce. NOT the record's 22.82/17.87 pair -- that pair compares Rung A at
# 0 bps against Rung C at 5 bps and is therefore timing PLUS cost (see WHY).
REF_B_NOPEN = 20.77       # "B (next-open 0bps)"      gate
REF_A_STOCKS = 22.82      # "A (c2c stocks 0bps)"     gate
REF_C_MAIN = 17.87        # "C (5bps stk/1bp QQQ) MAIN" gate -- context, not pinned
RECON_TOL = 0.02          # pp; the runner prints 2 dp, so this is exact-to-print


def build():
    """M10-1's main() lines 41-80, lifted verbatim in behaviour."""
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

    qcd = sorted(qc)

    def qc_at(d):
        i = bisect.bisect_right(qcd, d) - 1
        return qc[qcd[i]] if i >= 0 else 0.0

    scd = {t: sorted(oc[t]) for t in UNIV}

    def sc_at(t, d):
        lst = scd[t]; i = bisect.bisect_right(lst, d) - 1
        return oc[t][lst[i]][1] if i >= 0 else 0.0

    # Bar-index map over the QQQ calendar. qpx() needs "the bar BEFORE this one",
    # which qc_at CANNOT give: qc_at is an as-of carry-forward MARK (it returns
    # the last known close on or before d, repeating stale prices across gaps).
    # Using it for a FILL would quietly trade at a carried-forward price.
    qidx = {d: i for i, d in enumerate(qd)}
    return dict(oc=oc, tdates=tdates, forms=forms, qo=qo, qc=qc, qd=qd,
                q200=q200, vix_at=vix_at, master=master, weekend=weekend,
                idx=idx, qc_at=qc_at, sc_at=sc_at, qidx=qidx)


def run(B, scost, qcost, s_entry_close, s_exit_close,
        q_entry_close, q_exit_close, thr=20.0):
    """M10-1's run() with spx() split in two and a new qpx(). All four fills are
    addressed separately so the stocks-only recorded rung stays reproducible."""
    oc, tdates, forms = B["oc"], B["tdates"], B["forms"]
    qo, qc, q200, qidx, qd = B["qo"], B["qc"], B["q200"], B["qidx"], B["qd"]
    master, weekend, idx = B["master"], B["weekend"], B["idx"]
    vix_at, qc_at, sc_at = B["vix_at"], B["qc_at"], B["sc_at"]

    cash, spos, qu, cur, pend = CAP0, {}, 0.0, "cash", None
    navd = {}
    stress_entries = []
    legs = {"stress_entry": [], "stress_exit": [],
            "trend_entry": [], "trend_exit": []}

    def spx(t, d, at_close):
        i = idx[t][d]
        if at_close and i > 0:
            return oc[t][tdates[t][i - 1]][1]
        return oc[t][d][0]

    def qpx(d, at_close):
        i = qidx.get(d)
        if at_close and i is not None and i > 0:
            return qc[qd[i - 1]]
        return qo[d]

    def sleg(t, d):
        """log(open[d] / close[d-1]) for a stock -- the leg this fill sits on."""
        i = idx[t][d]
        if i == 0:
            return None
        pc, po = oc[t][tdates[t][i - 1]][1], oc[t][d][0]
        return math.log(po / pc) if pc > 0 and po > 0 else None

    def qleg(d):
        i = qidx.get(d)
        if i is None or i == 0:
            return None
        pc, po = qc[qd[i - 1]], qo[d]
        return math.log(po / pc) if pc > 0 and po > 0 else None

    for d in master:
        if pend is not None:
            mode, payload = pend
            for t in list(spos):
                if d in oc[t]:
                    cash += spos[t] * spx(t, d, s_exit_close) * (1 - scost)
                    lg = sleg(t, d)
                    if lg is not None:
                        legs["stress_exit"].append(lg)
                    del spos[t]
            if qu > 0 and d in qo:
                cash += qu * qpx(d, q_exit_close) * (1 - qcost)
                lg = qleg(d)
                if lg is not None:
                    legs["trend_exit"].append(lg)
                qu = 0.0
            navv = cash
            if mode == "stress":
                per = navv / K
                for t in payload:
                    if d in oc[t] and spx(t, d, s_entry_close) > 0:
                        p = spx(t, d, s_entry_close)
                        sh = per / (p * (1 + scost))
                        cash -= sh * p * (1 + scost)
                        spos[t] = sh
                        lg = sleg(t, d)
                        if lg is not None:
                            legs["stress_entry"].append(lg)
                stress_entries.append(d)
            elif mode == "trend_on" and d in qo and qpx(d, q_entry_close) > 0:
                p = qpx(d, q_entry_close)
                u = navv / (p * (1 + qcost))
                cash -= u * p * (1 + qcost)
                qu = u
                lg = qleg(d)
                if lg is not None:
                    legs["trend_entry"].append(lg)
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
    return navd, stress_entries, legs


def win(navd, master, w):
    lo, hi = w
    return stats([navd[d] for d in master if lo <= d <= hi])


def legstats(xs):
    if not xs:
        return 0, float("nan"), float("nan")
    mu = sum(xs) / len(xs)
    if len(xs) > 1:
        sd = math.sqrt(sum((v - mu) ** 2 for v in xs) / (len(xs) - 1))
        se = sd / math.sqrt(len(xs))
    else:
        se = float("nan")
    return len(xs), mu * 10000, se * 10000


def precision_block(B):
    """The as-run cell at 4 decimals, with the PASS-HR margins spelled out.

    EXISTS BECAUSE OF AUDIT GJ. Record GI quoted these figures from a throwaway
    inline `python -c`, so no file in the repo could reproduce them and the
    audit could not tell a captured number from a composed one -- every gate
    printer here formats to 2 decimals. The numbers were real; the COMMAND was
    unreproducible. A named flag fixes the class, not just the instance.

    Two decimals is the right default everywhere else; this exists only because
    M10-1's PASS-HR turns on a 0.05 pp drawdown margin that 1-dp output hides.
    """
    g = win(run(B, COST, QCOST, False, False, False, False)[0], B["master"], GATE)
    s = win(run(B, COST, QCOST, False, False, False, False)[0], B["master"], SEC)
    print("AS-RUN MAIN (5bps stk/1bp QQQ), today cache vintage:")
    print(f"  gate CAGR {g['cagr']*100:.4f}%  maxDD {g['mdd']*100:.4f}%  "
          f"Sharpe {g['sharpe']:.4f}")
    print(f"  sec  CAGR {s['cagr']*100:.4f}%  maxDD {s['mdd']*100:.4f}%  "
          f"Sharpe {s['sharpe']:.4f}")
    print()
    print("  recorded 2026-07-14: gate 17.87 / DD 59.9518 / Sh 0.66 ; "
          "sec 15.94 / DD 39.68 / Sh 0.78")
    print("  PASS-HR needs CAGR>=15 AND maxDD<=60 in BOTH windows")
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60
          and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    print(f"  PASS-HR on today cache: {'PASS' if hr else 'FAIL'}   "
          f"gate DD margin {60 - g['mdd']*100:+.4f} pp")
    return 0


def main():
    if "--precision" in sys.argv:
        print("loading bars + FF3 + VIX ...", flush=True)
        return precision_block(build())
    print("M10-1 entry-leg vs exit-leg split -- DIAGNOSTIC, no verdict, tally unchanged")
    print(f"M10-1 params imported, not restated: K={K}, "
          f"stocks {COST*10000:.0f} bps/side, QQQ {QCOST*10000:.0f} bp/side")
    print("loading bars + FF3 + VIX ...", flush=True)
    B = build()
    print(f"  {len(UNIV)} names, {len(B['master'])} sessions, "
          f"{len(B['weekend'])} weekly decision dates\n", flush=True)

    def cell(se, sx, qe, qx, cost=False):
        sc, qcst = (COST, QCOST) if cost else (0.0, 0.0)
        navd, _, legs = run(B, sc, qcst, se, sx, qe, qx)
        return dict(gate=win(navd, B["master"], GATE),
                    sec=win(navd, B["master"], SEC), legs=legs)

    asrun = cell(False, False, False, False)
    a_stocks = cell(True, True, False, False)

    print("=== RECONCILIATION against the runner's own printed rungs (asserted) ===")
    got_b = asrun["gate"]["cagr"] * 100
    got_a = a_stocks["gate"]["cagr"] * 100
    ok_b = abs(got_b - REF_B_NOPEN) <= RECON_TOL
    ok_a = abs(got_a - REF_A_STOCKS) <= RECON_TOL
    print(f"  B next-open 0bps      : got {got_b:.2f}%  runner {REF_B_NOPEN:.2f}%  "
          f"{'MATCH' if ok_b else 'MISMATCH'}")
    print(f"  A c2c STOCKS-ONLY 0bps: got {got_a:.2f}%  runner {REF_A_STOCKS:.2f}%  "
          f"{'MATCH' if ok_a else 'MISMATCH'}")
    if not (ok_b and ok_a):
        print("\n  RECONCILIATION FAILED -- the split does not reproduce the runner's")
        print("  own rungs, so every cell below is untrustworthy. Stopping.")
        return 1

    print("\n=== WHAT THE RECORDED '~5 pp OVERNIGHT GAP' ACTUALLY IS ===")
    navd_c, _, _ = run(B, COST, QCOST, False, False, False, False)
    got_c = win(navd_c, B["master"], GATE)["cagr"] * 100
    print(f"  A c2c stocks 0bps {got_a:6.2f}%   (record CI caveat 5 quotes this)")
    print(f"  B next-open  0bps {got_b:6.2f}%   (the caveat SKIPS this rung)")
    print(f"  C next-open  5bps {got_c:6.2f}%   (record CI caveat 5 quotes this)")
    print(f"  -> the quoted gap {got_a - got_c:+5.2f} pp is NOT a timing delta:")
    print(f"       TIMING (A->B) {got_a - got_b:+5.2f} pp   "
          f"COST (B->C) {got_b - got_c:+5.2f} pp")
    print("     and the TIMING half is stocks-only -- the QQQ legs never moved.")

    print("\n=== THE 2x2, BOTH BRANCHES, gate 2000-2013, 0 bps, CAGR %/yr ===")
    x4ub = cell(True, False, True, False)
    exit_only = cell(False, True, False, True)
    c2c_both = cell(True, True, True, True)
    print(f"{'':22} {'exit @ next open':>18} {'exit @ signal close':>21}")
    print(f"{'entry @ next open':22} {asrun['gate']['cagr']*100:17.2f}% "
          f"{exit_only['gate']['cagr']*100:20.2f}%")
    print(f"{'entry @ close (MOC)':22} {x4ub['gate']['cagr']*100:17.2f}% "
          f"{c2c_both['gate']['cagr']*100:20.2f}%")
    print("  NOTE: only the top-left cell is a recorded number. The other three")
    print("  include the QQQ leg and reconcile against NOTHING (see header).")

    base = asrun["gate"]["cagr"] * 100
    print(f"\n=== THE SPLIT (gate, pp/yr vs the as-run {base:.2f}%) ===")
    print(f"  total c2c gap, both branches  {c2c_both['gate']['cagr']*100 - base:+6.2f} pp")
    print(f"  attributable to ENTRY timing  {x4ub['gate']['cagr']*100 - base:+6.2f} pp")
    print(f"  attributable to EXIT timing   {exit_only['gate']['cagr']*100 - base:+6.2f} pp")

    print("\n=== PER-FILL OVERNIGHT LEGS, four populations (log bps, as-run cell) ===")
    for name in ("stress_entry", "stress_exit", "trend_entry", "trend_exit"):
        n, mu, se = legstats(asrun["legs"][name])
        print(f"  {name:14} n={n:5d}  mean {mu:+7.2f} bps  SE {se:6.2f}")
    print("  (pooled entry/exit would be swamped by the stress branch -- the")
    print("   trend branch fills only on regime transitions.)")

    print("\n=== SECONDARY WINDOW 2014- (0 bps) ===")
    print(f"  as-run {asrun['sec']['cagr']*100:6.2f}%   "
          f"entry-fixed {x4ub['sec']['cagr']*100:6.2f}%   "
          f"c2c both {c2c_both['sec']['cagr']*100:6.2f}%")

    print("\n=== AT THE REAL 5 bps stocks / 1 bp QQQ ===")
    for label, (se, sx, qe, qx) in (("as-run (entry open)", (False, False, False, False)),
                                    ("entry @ close (MOC)", (True, False, True, False))):
        c = cell(se, sx, qe, qx, cost=True)
        print(f"  {label:22} gate {c['gate']['cagr']*100:6.2f}%/DD{c['gate']['mdd']*100:5.1f}%"
              f"/Sh{c['gate']['sharpe']:5.2f} | sec {c['sec']['cagr']*100:6.2f}%"
              f"/DD{c['sec']['mdd']*100:5.1f}%/Sh{c['sec']['sharpe']:5.2f}")

    print("\nNo verdict. X4 stays BLOCKED-ON-BROKER-TIER and on the EOD-only rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
