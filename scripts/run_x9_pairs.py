"""X9 - pairs / relative-value (market-neutral family), per prereg
prereg_x9_pairs_relative_value.md (committed doc-only BEFORE this runner,
hash 00c8c44).

Gatev-Goetzmann-Rouwenhorst (2006) distance method at the PUBLISHED defaults --
adopted wholesale so nothing here is tuned: 252-session formation, 63-session
trading, K=3 lowest-SSD pairs, entry when |spread| > 2 * formation-sigma, exit
when the spread changes SIGN (prices cross = convergence) or a 20-session stop.
Long the underperformer / short the outperformer, equal dollar. Signal at close,
execute NEXT OPEN. 5 bps per side PER LEG (a round trip pays 4 legs --
understating this is how pairs is usually flattered).

Construction detail (faithful to the paper): both members are normalized to
their price at the FORMATION-WINDOW START and that same normalization is carried
through the trading window, so the spread is a cumulative relative-performance
gap and "convergence" is a genuine sign change. sigma is the standard deviation
of that spread over the formation window.

H0 is the FAVORED prior (Do & Faff 2010: the edge decayed to ~nil net
post-2002). Verdict (prereg 5): Sharpe >= 0.50 both windows, CAGR > 0 both,
maxDD <= 60% both, |corr to e6 rule| <= 0.30.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
Leveraged members excluded (embedded decay breaks the mean-reverting premise).
No swing.db writes.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch
from run_e18_regime_gates import stats
from swing_bot.universe import UNIVERSE

FORM_N = 252
TRADE_N = 63
K = 3
ENTRY_SD = 2.0
STOP_N = 20
COST = 0.0005          # 5 bps PER SIDE PER LEG
CAP0 = 1000.0
GATE_END = "2013-12-31"
SEC_START = "2014-01-01"
CORR_MAX = 0.30
DD_MAX = 0.60
SHARPE_MIN = 0.50
LEVERAGED = {"TQQQ", "UPRO", "SPXL", "SOXL", "TNA"}


def load():
    out = {}
    for e in UNIVERSE:
        if e.ticker in LEVERAGED:
            continue
        bars = cache_fetch(e.ticker)
        if len(bars) < FORM_N + TRADE_N:
            continue
        out[e.ticker] = {b[1]: (b[2], b[5]) for b in bars}
    return out


def e6_rule_nav(cost=0.0001):
    """The e6 reference sleeve (QQQ > SMA200), for the correlation criterion."""
    b = cache_fetch("QQQ")
    d = [x[1] for x in b]
    o = [x[2] for x in b]
    c = [x[5] for x in b]
    ma = [None] * len(c)
    for i in range(199, len(c)):
        ma[i] = sum(c[i - 199:i + 1]) / 200.0
    nav, cash, sh, pend = {}, CAP0, 0.0, None
    for i in range(199, len(d)):
        if pend is not None:
            if pend == 1 and sh == 0 and o[i] > 0:
                sh = cash / (o[i] * (1 + cost)); cash = 0.0
            elif pend == 0 and sh > 0:
                cash = sh * o[i] * (1 - cost); sh = 0.0
            pend = None
        nav[d[i]] = cash + sh * c[i]
        if ma[i] is None:
            continue
        want = c[i] > ma[i]
        if want and sh == 0 and cash > 0:
            pend = 1
        elif not want and sh > 0:
            pend = 0
    return nav


def corr(a, b):
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    if n < 2:
        return float("nan")
    ma, mb = sum(a) / n, sum(b) / n
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / den if den else float("nan")


def main():
    px = load()
    tickers = sorted(px)
    all_dates = sorted(set().union(*[set(v) for v in px.values()]))
    dates = [d for d in all_dates if sum(1 for t in tickers if d in px[t]) >= 10]
    print("X9 pairs (prereg 00c8c44) -- %d eligible ETFs, %d sessions (%s..%s)"
          % (len(tickers), len(dates), dates[0], dates[-1]))

    cash = CAP0
    open_pos, pend, nav = [], [], {}
    pairs, form_end = [], -10 ** 9
    n_open = n_conv = n_stop = 0

    for i in range(FORM_N, len(dates)):
        d = dates[i]

        # ---------- execute yesterday's decisions at TODAY'S OPEN ----------
        for act in pend:
            if act["kind"] == "open":
                a, b = act["lo"], act["hi"]
                if d not in px[a] or d not in px[b]:
                    continue
                oa, ob = px[a][d][0], px[b][d][0]
                if oa <= 0 or ob <= 0:
                    continue
                leg = act["dollars"]
                qa, qb = leg / oa, leg / ob          # equal DOLLAR legs at mid
                cash -= qa * oa * (1 + COST)         # buy underperformer (cost paid)
                cash += qb * ob * (1 - COST)         # short outperformer (cost paid)
                open_pos.append(dict(a=a, b=b, qa=qa, qb=qb, entry_i=i,
                                     pa=act["pa"], pb=act["pb"], sign=act["sign"]))
            else:
                p = act["pos"]
                if p not in open_pos:
                    continue
                if d not in px[p["a"]] or d not in px[p["b"]]:
                    continue
                oa, ob = px[p["a"]][d][0], px[p["b"]][d][0]
                cash += p["qa"] * oa * (1 - COST)    # sell long leg
                cash -= p["qb"] * ob * (1 + COST)    # buy back short leg
                open_pos.remove(p)
        pend = []

        # ---------- re-form every TRADE_N sessions ----------
        if i - form_end >= TRADE_N:
            w = dates[i - FORM_N:i]
            elig = [t for t in tickers if all(dd in px[t] for dd in w)]
            norm = {}
            for t in elig:
                base = px[t][w[0]][1]
                if base > 0:
                    norm[t] = [px[t][dd][1] / base for dd in w]
            cands = []
            keys = sorted(norm)
            for x in range(len(keys)):
                for y in range(x + 1, len(keys)):
                    ta, tb = keys[x], keys[y]
                    diff = [p - q for p, q in zip(norm[ta], norm[tb])]
                    ssd = sum(v * v for v in diff)
                    mu = sum(diff) / len(diff)
                    sd = math.sqrt(sum((v - mu) ** 2 for v in diff) / (len(diff) - 1))
                    cands.append((ssd, ta, tb, sd))
            cands.sort(key=lambda z: z[0])
            # carry each pair's normalization base (formation START price) forward
            pairs = [dict(a=a, b=b, sd=sd, pa=px[a][w[0]][1], pb=px[b][w[0]][1])
                     for _, a, b, sd in cands[:K]]
            form_end = i

        # ---------- mark NAV at today's CLOSE ----------
        mtm = cash
        for p in open_pos:
            if d in px[p["a"]] and d in px[p["b"]]:
                mtm += p["qa"] * px[p["a"]][d][1] - p["qb"] * px[p["b"]][d][1]
        nav[d] = mtm

        # ---------- decide at close (executed next open) ----------
        closing = {id(a["pos"]) for a in pend if a["kind"] == "close"}
        for p in list(open_pos):
            if id(p) in closing or d not in px[p["a"]] or d not in px[p["b"]]:
                continue
            s = px[p["a"]][d][1] / p["pa"] - px[p["b"]][d][1] / p["pb"]
            # entered with spread of `sign`; convergence = spread crosses zero
            if (p["sign"] > 0 and s <= 0) or (p["sign"] < 0 and s >= 0):
                pend.append(dict(kind="close", pos=p)); n_conv += 1
            elif (i - p["entry_i"]) >= STOP_N:
                pend.append(dict(kind="close", pos=p)); n_stop += 1

        held = {frozenset((p["a"], p["b"])) for p in open_pos}
        held |= {frozenset((a["lo"], a["hi"])) for a in pend if a["kind"] == "open"}
        slots = K - len(open_pos) - sum(1 for a in pend if a["kind"] == "open")
        if slots > 0 and nav[d] > 0:
            for pr in pairs:
                if slots <= 0:
                    break
                a, b, sd = pr["a"], pr["b"], pr["sd"]
                if frozenset((a, b)) in held or sd <= 0:
                    continue
                if d not in px[a] or d not in px[b]:
                    continue
                s = px[a][d][1] / pr["pa"] - px[b][d][1] / pr["pb"]
                if abs(s) > ENTRY_SD * sd:
                    # s>0 => a outperformed => short a, long b
                    lo, hi = (b, a) if s > 0 else (a, b)
                    plo, phi = (pr["pb"], pr["pa"]) if s > 0 else (pr["pa"], pr["pb"])
                    pend.append(dict(kind="open", lo=lo, hi=hi, dollars=nav[d] / K,
                                     pa=plo, pb=phi, sign=1 if s < 0 else -1))
                    held.add(frozenset((a, b)))
                    slots -= 1
                    n_open += 1

    ds = sorted(nav)
    g = stats([nav[x] for x in ds if x <= GATE_END])
    s_ = stats([nav[x] for x in ds if x >= SEC_START])

    def fmt(x):
        return "n/a" if x is None else "%+7.2f%% / DD %5.1f%% / Sh %5.2f" % (
            x["cagr"] * 100, x["mdd"] * 100, x["sharpe"])

    print("\n  trades: %d opened, %d converged, %d time-stopped" % (n_open, n_conv, n_stop))
    print("  final NAV: $%.2f" % nav[ds[-1]])
    print("  X9 GATE %s" % fmt(g))
    print("  X9 SEC  %s" % fmt(s_))

    e6 = e6_rule_nav()
    common = sorted(set(nav) & set(e6))
    ra = [nav[common[i]] / nav[common[i - 1]] - 1 for i in range(1, len(common))
          if nav[common[i - 1]] > 0]
    rb = [e6[common[i]] / e6[common[i - 1]] - 1 for i in range(1, len(common))
          if e6[common[i - 1]] > 0]
    rho = corr(ra, rb)
    print("  corr to e6 rule: %+.4f over %d sessions" % (rho, min(len(ra), len(rb))))

    c1 = bool(g and s_ and g["sharpe"] >= SHARPE_MIN and s_["sharpe"] >= SHARPE_MIN)
    c2 = bool(g and s_ and g["cagr"] > 0 and s_["cagr"] > 0)
    c3 = bool(g and s_ and g["mdd"] <= DD_MAX and s_["mdd"] <= DD_MAX)
    c4 = bool(abs(rho) <= CORR_MAX)
    for lbl, ok in (("1 Sharpe>=0.50 both", c1), ("2 CAGR>0 both", c2),
                    ("3 DD<=60% both", c3), ("4 |corr|<=0.30", c4)):
        print("    [%s] %s" % ("PASS" if ok else "FAIL", lbl))
    print("\nVERDICT: %s" % ("CLEARS" if all([c1, c2, c3, c4])
                             else "FAIL -> deploy nothing (prereg 6)"))


if __name__ == "__main__":
    main()
