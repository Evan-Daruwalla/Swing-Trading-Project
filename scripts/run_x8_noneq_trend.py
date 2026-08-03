"""X8 - non-equity trend sleeve (decorrelation candidate), per prereg
prereg_x8_noneq_trend.md (committed doc-only BEFORE this runner, hash 8b408f9).

E6's rule VERBATIM (long iff close > SMA200, signal at close, execute next open)
applied to two pre-declared NON-EQUITY arms: (a) GLD, (b) TLT. This tests the
ASSET, not a new rule -- the program's one survivor (200-DMA trend gating) has
only ever been tested on equities (E7: 3/5 non-US regions) and crypto (X6: FAIL).

Verdict uses the prereg's explicitly-labelled DIVERSIFIER bar, NOT D1 (which
would reject on a CAGR>=15% criterion this sleeve was never meant to satisfy):
  1. |corr(daily rets, e6 rule)| <= 0.30   (the actual purpose)
  2. net CAGR > 0 in BOTH windows          (not value-destroying)
  3. maxDD <= 60% in BOTH windows          (ruin guard)
  4. Sharpe > the asset's OWN buy-and-hold in BOTH windows  (gate earns its keep)
D1 numbers are reported regardless, for comparability with the other 35 attempts.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
DECLARED BIAS: dividend-unadjusted materially understates TLT (coupon-bearing) --
prereg section 4/9. No swing.db writes.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch
from run_e18_regime_gates import sma, stats

ARMS = (("a", "GLD"), ("b", "TLT"))
MA = 200
COST = 0.0001                      # 1 bp/side, broad liquid ETF tier (prereg 4)
CAP0 = 1000.0
GATE_END = "2013-12-31"
SEC_START = "2014-01-01"
CORR_MAX = 0.30                    # prereg 6.1
DD_MAX = 0.60                      # prereg 6.3


def series(ticker):
    b = cache_fetch(ticker)
    return [x[1] for x in b], [x[2] for x in b], [x[5] for x in b]


def trend_nav(dates, op, cl, start_i=MA - 1):
    """Long iff close > SMA200 at close t -> execute at open t+1. Returns
    {date: nav}. Mirrors E6/overlay_nav semantics at this prereg's cost."""
    ma = sma(cl, MA)
    cash, sh, pend = CAP0, 0.0, None
    nav = {}
    for i in range(start_i, len(dates)):
        if pend is not None:
            if pend == 1 and sh == 0.0 and op[i] > 0:
                sh = cash / (op[i] * (1 + COST)); cash = 0.0
            elif pend == 0 and sh > 0.0:
                cash = sh * op[i] * (1 - COST); sh = 0.0
            pend = None
        nav[dates[i]] = cash + sh * cl[i]
        if ma[i] is None:
            continue
        want = cl[i] > ma[i]
        if want and sh == 0.0 and cash > 0:
            pend = 1
        elif (not want) and sh > 0.0:
            pend = 0
    return nav


def hold_nav(dates, op, cl, start_i=MA - 1):
    """Buy-and-hold the same asset from the same first bar, same cost model."""
    nav = {}
    sh = None
    for i in range(start_i, len(dates)):
        if sh is None:
            if op[i] <= 0:
                continue
            sh = CAP0 / (op[i] * (1 + COST))
        nav[dates[i]] = sh * cl[i]
    return nav


def window(nav, lo=None, hi=None):
    ds = sorted(d for d in nav if (lo is None or d >= lo) and (hi is None or d <= hi))
    return [nav[d] for d in ds]


def daily_rets(nav, dates):
    return [nav[dates[i]] / nav[dates[i - 1]] - 1
            for i in range(1, len(dates)) if nav[dates[i - 1]] > 0]


def corr(a, b):
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return cov / den if den else float("nan")


def fmt(s):
    if s is None:
        return "   n/a "
    return "%+7.2f%% / DD %5.1f%% / Sh %5.2f" % (s["cagr"] * 100, s["mdd"] * 100, s["sharpe"])


def main():
    print("X8 - non-equity trend sleeve (prereg 8b408f9)\n" + "=" * 78)
    # e6 reference rule on QQQ, for the correlation criterion
    qd, qo, qc = series("QQQ")
    e6 = trend_nav(qd, qo, qc)
    print("reference: e6 rule (QQQ>SMA200) %s .. %s" % (min(e6), max(e6)))

    results = {}
    for arm, tk in ARMS:
        d, o, c = series(tk)
        print("\n--- arm (%s) %s : %d bars, %s .. %s ---" % (arm, tk, len(d), d[0], d[-1]))
        tn = trend_nav(d, o, c)
        bh = hold_nav(d, o, c)
        gate_t, sec_t = stats(window(tn, hi=GATE_END)), stats(window(tn, lo=SEC_START))
        gate_b, sec_b = stats(window(bh, hi=GATE_END)), stats(window(bh, lo=SEC_START))
        print("  trend   GATE %s" % fmt(gate_t))
        print("  trend   SEC  %s" % fmt(sec_t))
        print("  BUYHOLD GATE %s" % fmt(gate_b))
        print("  BUYHOLD SEC  %s" % fmt(sec_b))

        common = sorted(set(tn) & set(e6))
        r_arm, r_e6 = daily_rets(tn, common), daily_rets(e6, common)
        rho = corr(r_arm, r_e6)
        print("  corr to e6 rule: %+.4f  over %d common sessions (%s..%s)"
              % (rho, len(common), common[0], common[-1]))

        # --- pre-declared criteria, evaluated exactly as written ---
        c1 = abs(rho) <= CORR_MAX
        c2 = all(s and s["cagr"] > 0 for s in (gate_t, sec_t))
        c3 = all(s and s["mdd"] <= DD_MAX for s in (gate_t, sec_t))
        c4 = (gate_t and gate_b and sec_t and sec_b
              and gate_t["sharpe"] > gate_b["sharpe"]
              and sec_t["sharpe"] > sec_b["sharpe"])
        checks = [("1 corr<=0.30", c1), ("2 CAGR>0 both", c2),
                  ("3 DD<=60% both", c3), ("4 Sh>buyhold both", c4)]
        for label, ok in checks:
            print("    [%s] %s" % ("PASS" if ok else "FAIL", label))
        cleared = all(ok for _, ok in checks)
        results[tk] = cleared
        print("  ARM (%s) %s: %s" % (arm, tk, "CLEARS" if cleared else "FAIL"))

    print("\n" + "=" * 78)
    for tk, ok in results.items():
        print("  %s: %s" % (tk, "CLEARS -> eligible as forward sleeve #4" if ok else "FAIL"))
    if not any(results.values()):
        print("\nVERDICT: BOTH ARMS FAIL -> deploy nothing (prereg 7). The program has no\n"
              "uncorrelated candidate; the 3 live sleeves remain ~one strategy.")
    else:
        print("\nVERDICT: at least one arm CLEARS -> eligible for forward paper as sleeve #4,\n"
              "ADDED alongside the untouched existing three (prereg 7/8).")


if __name__ == "__main__":
    main()
