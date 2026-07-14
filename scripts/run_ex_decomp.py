"""EX-DECOMP (M9 #44) - execution/signal decomposition ladder on closed FAILs.

DIAGNOSTIC, no D1 verdict, no tuning. For each closed FAIL runner, run three
rungs and locate where the (benchmark-relative) alpha dies:
  Rung A - frictionless CLOSE-TO-CLOSE, 0 bps   (raw signal alpha)
  Rung B - next-OPEN, 0 bps                      (removes the overnight gap)
  Rung C - next-OPEN + 5 bps/side                (the as-run result)

Rung A is obtained WITHOUT editing any runner's execution logic: the price
feed is wrapped so each bar's open := prior close, which turns the runner's
"fill at next open" into "fill at signal-day close" = frictionless c2c.
Rung B/C differ only by COST (monkeypatched to 0 for A/B). Benchmarks use
closes, so they are identical across rungs. E20 (entry is already a close, so
the open-transform degenerates) is computed directly from its documented
per-trade formula, reusing its divs() loader.

Classification (gate window 2000-2013 primary), benchmark = each strategy's
honest null:
  SIGNAL-DEAD  - Rung A does NOT beat the null (no edge even frictionless c2c)
  GAP-DWELLER  - beats null at A, dies A->B (edge lived in the overnight gap)
  COST-GATED   - beats null at B, dies B->C (edge real+executable, killed by cost)
  SURVIVES-NULL- still beats null at C (real benchmark-relative alpha; the D1
                 FAIL is then about the 15% high-return bar / DD, not the signal)

Reuses .e8e9_cache; no swing.db writes; frozen tripwire unaffected.
"""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_e13_turn_of_month as m13
import run_e14_sector_momentum as m14
import run_e15_earnings_premium as m15
import run_e16_weekly_reversal as m16
import run_e20_dividend_capture as m20
from run_e8_squeeze import cache_fetch, COST as C0
from swing_bot.universe import UNIVERSE

GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")


def make_c2c(fetch):
    """Wrap a cache_fetch so each bar's open := prior close (c2c execution)."""
    def wrapped(t):
        out, prev_cl = [], None
        for b in fetch(t):
            nb = list(b)
            if prev_cl is not None:
                nb[2] = prev_cl
            prev_cl = b[5]
            out.append(nb)
        return out
    return wrapped


def run_rungs(mod):
    """Run a next-open runner at rungs C/B/A; return {rung: main()-dict}."""
    orig, ocost = mod.cache_fetch, mod.COST
    res = {}
    for rung, cost, fetch in [("C", ocost, orig), ("B", 0.0, orig),
                              ("A", 0.0, make_c2c(orig))]:
        mod.COST, mod.cache_fetch = cost, fetch
        with redirect_stdout(io.StringIO()):
            res[rung] = mod.main()
    mod.COST, mod.cache_fetch = ocost, orig
    return res


def e20_rungs():
    """E20 dividend capture, three rungs, as mean net per-trade (bps)."""
    buckets = {"gate": [], "sec": []}      # (a_net, b_net) 0-cost
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        oc = {b[1]: (b[2], b[5]) for b in bars}
        dl = [b[1] for b in bars]
        di = {d: i for i, d in enumerate(dl)}
        for exd, amt in m20.divs(e.ticker).items():
            if exd not in di:
                continue
            j = di[exd]
            if j == 0:
                continue
            prior = dl[j - 1]
            p0 = oc[prior][1]
            if p0 <= 0:
                continue
            b_net = (oc[exd][0] - p0) / p0 + amt / p0      # close->open, 0 cost
            a_net = (oc[exd][1] - p0) / p0 + amt / p0      # close->close, 0 cost
            w = ("gate" if GATE[0] <= prior <= GATE[1]
                 else "sec" if prior >= SEC[0] else None)
            if w:
                buckets[w].append((a_net, b_net))
    out = {}
    for w, lst in buckets.items():
        n = len(lst)
        a = sum(x[0] for x in lst) / n
        b = sum(x[1] for x in lst) / n
        c = b - 2 * C0                                     # add 5bps/side back
        out[w] = dict(n=n, A=a, B=b, C=c)
    return out


def classify(a, b, c, null):
    """CAGR-based, benchmark-relative. a/b/c/null are gate-window CAGRs."""
    if a <= null:
        return "SIGNAL-DEAD"
    if b <= null:
        return "GAP-DWELLER"
    if c <= null:
        return "COST-GATED"
    return "SURVIVES-NULL"


def pct(x):
    return f"{x*100:6.2f}%"


def main():
    specs = [("E13 turn-of-month", m13, "GATE 2000-2013", "SECONDARY 2014-"),
             ("E14 sector-momentum", m14, "GATE 2000-2013", "SECONDARY 2014-"),
             ("E15 earnings-premium", m15, "2000-2013", "2014-"),
             ("E16 weekly-reversal", m16, "2000-2013", "2014-")]

    print("=" * 78)
    print("EX-DECOMP (M9 #44) - signal/execution decomposition of the closed FAILs")
    print("Rung A=c2c 0bps | B=next-open 0bps | C=next-open 5bps (as-run)")
    print("=" * 78)

    table = []
    regcheck = {}
    for label, mod, kg, ks in specs:
        r = run_rungs(mod)
        null_g = r["C"]["rows"][kg][1]["cagr"]      # null identical across rungs
        null_s = r["C"]["rows"][ks][1]["cagr"]
        ag, bg, cg = (r[x]["rows"][kg][0]["cagr"] for x in ("A", "B", "C"))
        as_, bs, cs = (r[x]["rows"][ks][0]["cagr"] for x in ("A", "B", "C"))
        cls = classify(ag, bg, cg, null_g)
        bench = r["C"]["bench"]
        regcheck[label] = cg
        table.append((label, bench, null_g, ag, bg, cg, cls, null_s, as_, bs, cs))

    hdr = (f"\n{'strategy':22}{'null':11}{'A(c2c)':>9}{'B(open)':>9}"
           f"{'C(+cost)':>9}{'null_bh':>9}  classification")
    print("\n--- GATE 2000-2013 (primary) ---")
    print(hdr)
    for (label, bench, ng, ag, bg, cg, cls, ns, a2, b2, c2) in table:
        print(f"{label:22}{bench:11}{pct(ag)}{pct(bg)}{pct(cg)}{pct(ng)}  {cls}")

    print("\n--- SECONDARY 2014- (context) ---")
    print(f"\n{'strategy':22}{'A(c2c)':>9}{'B(open)':>9}{'C(+cost)':>9}{'null_bh':>9}")
    for (label, bench, ng, ag, bg, cg, cls, ns, a2, b2, c2) in table:
        print(f"{label:22}{pct(a2)}{pct(b2)}{pct(c2)}{pct(ns)}")

    # E20 - overnight overlay, reported as mean net per-trade (bps)
    e = e20_rungs()
    print("\n--- E20 dividend-capture (overnight overlay; mean NET per-trade, bps) ---")
    for w in ("gate", "sec"):
        d = e[w]
        edge = ("SIGNAL-DEAD" if d["A"] <= 0 and d["B"] <= 0
                else "GAP-DWELLER" if d["B"] > max(d["A"], 0)
                else "COST-effect")
        tag = "REAL-BUT-SUBSCALE" if d["C"] > 0 else "DEAD-AFTER-COST"
        print(f"  {w:5} n={d['n']:4}  A(c2c) {d['A']*1e4:+7.1f}  "
              f"B(open) {d['B']*1e4:+7.1f}  C(+cost) {d['C']*1e4:+7.1f}  "
              f"-> {tag} / gap:{edge}")

    # regression check: Rung C reproduces the recorded FAILs
    print("\n--- REGRESSION CHECK (Rung C gate CAGR vs recorded) ---")
    pins = {"E13 turn-of-month": (0.014, 0.004),
            "E16 weekly-reversal": (0.1676, 0.005)}
    ok = True
    for label, cg in regcheck.items():
        if label in pins:
            ref, tol = pins[label]
            good = abs(cg - ref) <= tol
            ok = ok and good
            print(f"  {label:22} C={pct(cg)}  ref={pct(ref)}  "
                  f"{'OK' if good else 'DRIFT!!'}")
    egate = e["gate"]["C"]
    print(f"  E20 dividend-capture   C-mean-net={egate*1e4:+.1f}bps "
          f"(recorded +~10bps/trade)")
    print(f"\nREGRESSION: {'GREEN' if ok else 'RED - investigate'}")


if __name__ == "__main__":
    main()
