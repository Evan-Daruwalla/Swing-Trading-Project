"""X7 - HYG:IEF credit-appetite regime gate, per prereg prereg_x7_credit_gate.md
(committed doc-only BEFORE this runner, hash f4a4d34).

Long QQQ 1x when the HYG:IEF price ratio > its trailing 200-session SMA (credit
appetite ON), else cash. Signal at close, execute next open. The free credit-spread
proxy E18's HY-OAS arm could not test (FRED OAS was 2023+; HYG:IEF runs 2007+).
Head-to-head vs the plain QQQ 200-DMA overlay (the incumbent E18 could not beat).
MODIFIED-WINDOW (gate 2007-2013, contains the GFC) -> verdict capped at PROMISING.
Not survivor-biased (market-wide ETF signal). No swing.db writes.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False). HYG/IEF are
dividend-heavy -> the ratio is a PRICE-ONLY credit-regime signal (not total return),
which is correct: it is never traded, only gates QQQ.

NAV (finding-things map): imports `cache_fetch, CAP0` <- run_e8_squeeze and
`sma, stats` <- run_e18_regime_gates (the shared-helper hub). RESULT = FAIL,
2026-07-15 (gate beat the 200-DMA in-window — the program's first to do so —
but the post-window sec bar failed; crisis specialist that whipsaws in bulls) —
NOT forwarded to M3 paper. See docs/research/2026-07-15_X7_credit_gate_results.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, CAP0
from run_e18_regime_gates import sma, stats

QCOST = 0.0001                       # 1 bp/side, QQQ broad-ETF tier
GATE = ("2007-04-11", "2013-12-31")  # HYG start .. ; contains the 2008 GFC
SEC = ("2014-01-01", "2099-01-01")


def main():
    qb = cache_fetch("QQQ")
    qd = [b[1] for b in qb]
    qo = {b[1]: b[2] for b in qb}
    qc = {b[1]: b[5] for b in qb}
    qcl = [b[5] for b in qb]
    hyg = {b[1]: b[5] for b in cache_fetch("HYG")}
    ief = {b[1]: b[5] for b in cache_fetch("IEF")}
    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    ratio = [(hyg[d] / ief[d]) if (d in hyg and d in ief and ief[d] > 0) else None
             for d in qd]
    n = len(qd)
    rma = [None] * n
    for i in range(199, n):
        w = ratio[i - 199:i + 1]
        if all(x is not None for x in w):
            rma[i] = sum(w) / 200.0
    risk_credit = [(ratio[i] > rma[i]) if (ratio[i] is not None and rma[i] is not None)
                   else None for i in range(n)]

    qsma = sma(qcl, 200)             # plain QQQ 200-DMA overlay (the incumbent)
    risk_200 = [(qcl[i] > qsma[i]) if qsma[i] is not None else None for i in range(n)]

    def overlay_nav(risk, cost, c2c):
        cash, sh, pend = CAP0, 0.0, None
        nav = {}
        for i, d in enumerate(qd):
            c = qc[d]
            if not c2c and pend is not None:            # execute prior decision at open
                f = qo[d]
                if pend == 1 and sh == 0.0 and f > 0:
                    sh = cash / (f * (1 + cost)); cash = 0.0
                elif pend == 0 and sh > 0.0:
                    cash = sh * f * (1 - cost); sh = 0.0
                pend = None
            w = risk[i]
            if c2c and w is not None:                   # rung A: fill at signal close
                if w and sh == 0.0 and cash > 0:
                    sh = cash / (c * (1 + cost)); cash = 0.0
                elif (not w) and sh > 0.0:
                    cash = sh * c * (1 - cost); sh = 0.0
            nav[d] = cash + sh * c
            if not c2c and w is not None:
                if w and sh == 0.0 and cash > 0:
                    pend = 1
                elif (not w) and sh > 0.0:
                    pend = 0
        return nav

    def switches(risk):
        s, last = 0, None
        for i in range(n):
            if risk[i] is not None:
                if last is not None and risk[i] != last:
                    s += 1
                last = risk[i]
        return s

    def win(nav, lo, hi):
        return [nav[d] for d in qd if lo <= d <= hi]

    def bh(pmap, lo, hi):
        seg = [d for d in sorted(pmap) if lo <= d <= hi]
        return stats([pmap[d] / pmap[seg[0]] for d in seg]) if seg else None

    def row(tag, risk, cost, c2c):
        nav = overlay_nav(risk, cost, c2c)
        g = stats(win(nav, *GATE)); s = stats(win(nav, *SEC))
        gs = f"{g['cagr']*100:6.2f}%/DD{g['mdd']*100:5.1f}%/Sh{g['sharpe']:5.2f}" if g else "  n/a"
        ss = f"{s['cagr']*100:6.2f}%/DD{s['mdd']*100:5.1f}%/Sh{s['sharpe']:5.2f}" if s else "  n/a"
        print(f"{tag:30} gate {gs} | sec {ss}")
        return g, s

    print(f"\nX7 HYG:IEF credit gate | long QQQ iff ratio>200DMA(ratio) | gate {GATE[0]}..{GATE[1]}")
    print(f"credit-gate switches: {switches(risk_credit)}   plain-200DMA switches: {switches(risk_200)}\n")
    cg = row("CREDIT next-open 1bp MAIN", risk_credit, QCOST, False)
    row("  credit next-open 0bp (B)", risk_credit, 0.0, False)
    row("  credit c2c 0bp (A upper)", risk_credit, 0.0, True)
    row("  credit stress 15bp", risk_credit, 0.0015, False)
    p200 = row("PLAIN-200DMA next-open 1bp", risk_200, QCOST, False)

    # benchmarks
    gq = bh(qc, *GATE); sq = bh(qc, *SEC); gsp = bh(spy, *GATE); ssp = bh(spy, *SEC)
    print(f"\nbenchmarks gate: QQQ-BH {gq['cagr']*100:.2f}%/DD{gq['mdd']*100:.1f}%/{gq['sharpe']:.2f}  "
          f"SPY-BH {gsp['cagr']*100:.2f}%/{gsp['sharpe']:.2f}")
    print(f"benchmarks sec:  QQQ-BH {sq['cagr']*100:.2f}%/DD{sq['mdd']*100:.1f}%/{sq['sharpe']:.2f}  "
          f"SPY-BH {ssp['cagr']*100:.2f}%/{ssp['sharpe']:.2f}")

    # descriptive sensitivity: 50-day ratio MA (NOT gated)
    rma50 = [None] * n
    for i in range(49, n):
        w = ratio[i - 49:i + 1]
        if all(x is not None for x in w):
            rma50[i] = sum(w) / 50.0
    risk50 = [(ratio[i] > rma50[i]) if (ratio[i] is not None and rma50[i] is not None)
              else None for i in range(n)]
    print("  --- descriptive (NOT gated): 50-day ratio MA ---")
    row("  credit-50dma next-open 1bp", risk50, QCOST, False)

    # verdict
    cg_g, cg_s = cg; p_g, p_s = p200
    def overlay_ok(cg_w, bh_w):
        return (bh_w["mdd"] - cg_w["mdd"] >= 0.10) and (cg_w["sharpe"] >= bh_w["sharpe"])
    both = overlay_ok(cg_g, gq) and overlay_ok(cg_s, sq)
    beats_200 = cg_g["sharpe"] > p_g["sharpe"]
    ra = (cg_g["sharpe"] >= 0.80 and cg_g["sharpe"] > gsp["sharpe"]
          and cg_s["sharpe"] > ssp["sharpe"] and cg_g["cagr"] > 0 and cg_s["cagr"] > 0)
    print(f"\n=== D1 VERDICT (prereg prereg_x7_credit_gate.md; MODIFIED-WINDOW -> PROMISING cap) ===")
    print(f"  overlay-ok (DD cut>=10pp AND Sharpe>=QQQ-BH) both windows: {'YES' if both else 'no'}")
    print(f"    gate: credit DD {cg_g['mdd']*100:.1f}% vs QQQ-BH {gq['mdd']*100:.1f}%; "
          f"Sh {cg_g['sharpe']:.2f} vs {gq['sharpe']:.2f}")
    print(f"    sec:  credit DD {cg_s['mdd']*100:.1f}% vs QQQ-BH {sq['mdd']*100:.1f}%; "
          f"Sh {cg_s['sharpe']:.2f} vs {sq['sharpe']:.2f}")
    print(f"  beats plain-200DMA on gate Sharpe: {'YES' if beats_200 else 'no'} "
          f"({cg_g['sharpe']:.2f} vs {p_g['sharpe']:.2f})")
    print(f"  PASS-RA-equiv (capped): {'yes' if ra else 'no'} (gate Sharpe {cg_g['sharpe']:.2f})")
    if both and beats_200:
        v = "PROMISING - beats the incumbent 200-DMA overlay; FORWARD PAPER required (modified window), not PASS-HR/RA"
    else:
        v = "FAIL (credit gate does not beat the plain 200-DMA overlay; extends E18/X1 to the credit channel)"
    print(f"\n  X7 VERDICT: {v}")


if __name__ == "__main__":
    main()
