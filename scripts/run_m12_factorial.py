"""M12 - constraint-relaxation factorial (horizon x concentration), per prereg
prereg_m12_constraint_factorial.md (committed doc-only BEFORE this runner,
hash 43e4d42).

Tests WHICH constraint binds. 2x2: hold (10 vs 63 sessions) x K (3 vs 20), with
12-1 cross-sectional momentum HELD CONSTANT so the only thing that varies is the
constraint. Universe: swing_bot/universe_m12.py (142 large-caps, frozen).

DIAGNOSTIC ONLY (prereg 6). Reports 4 cells + both main effects + the
interaction. Issues NO pass/fail, and no cell becomes a sleeve on this run --
picking the best of four would be in-sample composition (the M10-1 mistake).

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
Dividends are NOT reinvested -- understates every cell and the EW benchmark
roughly equally, high-yield sectors most (prereg 8). No swing.db writes.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch
from swing_bot.universe_m12 import TICKERS

FORM_LONG = 252        # 12-month formation
FORM_SKIP = 21         # skip the most recent month (short-term reversal)
CAP0 = 1000.0
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
CELLS = (("(1) BASELINE", 10, 3), ("(2) H  horizon", 63, 3),
         ("(3) C  breadth", 10, 20), ("(4) H+C both", 63, 20))
COSTS = (0.0005, 0.0015)   # 5 bps and the 15 bps stress report


def load():
    """date-indexed opens/closes per ticker, aligned to a master date list."""
    raw = {}
    for t in TICKERS:
        try:
            b = cache_fetch(t)
        except Exception as e:
            print("  WARN %s unfetchable (%r) -- EXCLUDED" % (t, e), flush=True)
            continue
        if b:
            raw[t] = {x[1]: (x[2], x[5]) for x in b}
    dates = sorted(set().union(*[set(v) for v in raw.values()]))
    idx = {d: i for i, d in enumerate(dates)}
    op, cl = {}, {}
    for t, m in raw.items():
        o = [None] * len(dates); c = [None] * len(dates)
        for d, (a, b_) in m.items():
            o[idx[d]] = a; c[idx[d]] = b_
        op[t], cl[t] = o, c
    return dates, op, cl


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return None
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


def run_cell(dates, op, cl, hold_n, k, cost, start_i):
    """Rank at close T (12-1 momentum), fill at open T+1, equal-weight top-K.
    Returns ({date: nav}, n_rebal, turnover_frac)."""
    cash, pos = CAP0, {}          # pos: ticker -> shares
    nav, pend = {}, None
    n_rebal, traded_notional, nav_sum = 0, 0.0, 0.0

    for i in range(start_i, len(dates)):
        d = dates[i]
        # --- execute yesterday's decision at today's OPEN ---
        if pend is not None:
            # sell everything not wanted (and everything, if rebalancing fully)
            for t in list(pos):
                o = op[t][i]
                if o is None or o <= 0:
                    continue
                cash += pos[t] * o * (1 - cost)
                traded_notional += pos[t] * o
                del pos[t]
            keep = [t for t in pend if op[t][i] not in (None, 0)]
            if keep:
                each = cash / len(keep)
                for t in keep:
                    o = op[t][i]
                    sh = each / (o * (1 + cost))
                    pos[t] = sh
                    cash -= sh * o * (1 + cost)
                    traded_notional += sh * o
            pend = None

        # --- mark NAV at today's CLOSE ---
        v = cash
        for t, sh in pos.items():
            c = cl[t][i]
            if c is not None:
                v += sh * c
        nav[d] = v
        nav_sum += v

        # --- decide at the close, every hold_n sessions ---
        if (i - start_i) % hold_n == 0:
            scores = []
            for t in TICKERS:
                if t not in cl:
                    continue
                c_now, c_then = cl[t][i - FORM_SKIP], cl[t][i - FORM_LONG]
                if c_now is None or c_then is None or c_then <= 0:
                    continue
                if cl[t][i] is None:          # must be trading today
                    continue
                scores.append((c_now / c_then - 1.0, t))
            if len(scores) >= k:
                scores.sort(key=lambda z: -z[0])
                pend = [t for _, t in scores[:k]]
                n_rebal += 1
    turn = traded_notional / nav_sum if nav_sum else 0.0
    return nav, n_rebal, turn


def ew_hold(dates, op, cl, start_i, cost):
    """Equal-weight buy-and-hold of the whole universe -- the survivorship-honest
    benchmark (it inherits the SAME bias as every cell)."""
    elig = [t for t in cl if op[t][start_i] not in (None, 0)]
    each = CAP0 / len(elig)
    pos = {t: each / (op[t][start_i] * (1 + cost)) for t in elig}
    nav = {}
    for i in range(start_i, len(dates)):
        v = 0.0
        for t, sh in pos.items():
            c = cl[t][i]
            if c is not None:
                v += sh * c
        nav[dates[i]] = v
    return nav


def win(nav, lo, hi):
    return [nav[d] for d in sorted(nav) if lo <= d <= hi]


def corr(a, b):
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    if n < 2:
        return float("nan")
    ma, mb = sum(a) / n, sum(b) / n
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / den if den else float("nan")


def rets_on(nav, ds):
    return [nav[ds[i]] / nav[ds[i - 1]] - 1 for i in range(1, len(ds))
            if nav.get(ds[i - 1], 0) > 0 and ds[i] in nav]


def e6_nav():
    b = cache_fetch("QQQ")
    d = [x[1] for x in b]; o = [x[2] for x in b]; c = [x[5] for x in b]
    ma = [None] * len(c)
    for i in range(199, len(c)):
        ma[i] = sum(c[i - 199:i + 1]) / 200.0
    nav, cash, sh, pend = {}, CAP0, 0.0, None
    for i in range(199, len(d)):
        if pend is not None:
            if pend == 1 and sh == 0 and o[i] > 0:
                sh = cash / (o[i] * 1.0001); cash = 0.0
            elif pend == 0 and sh > 0:
                cash = sh * o[i] * 0.9999; sh = 0.0
            pend = None
        nav[d[i]] = cash + sh * c[i]
        if ma[i] is None:
            continue
        w = c[i] > ma[i]
        if w and sh == 0 and cash > 0:
            pend = 1
        elif not w and sh > 0:
            pend = 0
    return nav


def fmt(s):
    return "    n/a" if s is None else "%+7.2f%% / DD %5.1f%% / Sh %5.2f" % (
        s["cagr"] * 100, s["mdd"] * 100, s["sharpe"])


def main():
    print("M12 constraint factorial (prereg 43e4d42) -- loading %d names..." % len(TICKERS),
          flush=True)
    dates, op, cl = load()
    print("loaded %d tickers, %d sessions (%s..%s)" % (len(cl), len(dates), dates[0], dates[-1]))
    start_i = next(i for i, d in enumerate(dates) if d >= GATE[0])
    if start_i < FORM_LONG:
        start_i = FORM_LONG
    print("backtest starts at index %d (%s)\n" % (start_i, dates[start_i]))

    e6 = e6_nav()
    for cost in COSTS:
        print("=" * 78)
        print("COST = %.0f bps/side" % (cost * 10000))
        print("=" * 78)
        cells = {}
        for label, hold_n, k in CELLS:
            nav, nreb, turn = run_cell(dates, op, cl, hold_n, k, cost, start_i)
            g, s = stats(win(nav, *GATE)), stats(win(nav, *SEC))
            cells[label] = (g, s, nav)
            print("  %-16s hold=%-3d K=%-3d  GATE %s" % (label, hold_n, k, fmt(g)))
            print("  %-16s %-14s SEC  %s   (%d rebal, turnover %.1fx/yr)"
                  % ("", "", fmt(s), nreb, turn * 252))
        ew = ew_hold(dates, op, cl, start_i, cost)
        print("  %-16s %-14s GATE %s" % ("BENCH EW-hold", "", fmt(stats(win(ew, *GATE)))))
        print("  %-16s %-14s SEC  %s" % ("", "", fmt(stats(win(ew, *SEC)))))

        # main effects + interaction on CAGR, both windows
        def cg(lbl, w):
            v = cells[lbl][0 if w == "G" else 1]
            return v["cagr"] * 100 if v else float("nan")
        for w, wname in (("G", "GATE"), ("S", "SEC ")):
            b, h, c_, hc = (cg(CELLS[0][0], w), cg(CELLS[1][0], w),
                            cg(CELLS[2][0], w), cg(CELLS[3][0], w))
            print("\n  %s effects (CAGR pp vs baseline %.2f%%):" % (wname, b))
            print("     horizon alone      %+6.2f pp" % (h - b))
            print("     breadth alone      %+6.2f pp" % (c_ - b))
            print("     interaction        %+6.2f pp" % (hc - h - c_ + b))
        # correlation of the widest cell to e6
        nav4 = cells[CELLS[3][0]][2]
        common = sorted(set(nav4) & set(e6))
        print("\n  corr(cell 4, e6 rule) = %+.4f over %d sessions"
              % (corr(rets_on(nav4, common), rets_on(e6, common)), len(common)))
        print()


if __name__ == "__main__":
    main()
