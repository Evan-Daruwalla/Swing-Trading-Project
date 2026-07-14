"""C7 - SVXY short-vol carry gated by VIX term structure, per prereg
prereg_c7_svxy_carry.md (committed doc-only before this runner).

Long SVXY iff VIX/VIX3M<1 at close, else flat; next-open; 5 bps/side.
Kill-switch: held-day close-to-close <= -20% -> exit next open + 21-session
stand-down. Single 2012- window -> PROMISING cap. Arms: gated+KS (main),
gated no-KS, SVXY-BH, SPY-BH. No swing.db writes.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
SVXY was -1x until 2018-02-27, -0.5x after (actual prices, disclosed).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from run_e18_regime_gates import macro_close

START = "2012-01-01"
KS_RET = -0.20
KS_STAND = 21


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
    bars = [b for b in cache_fetch("SVXY") if b[1] >= START]
    dates = [b[1] for b in bars]
    op = [b[2] for b in bars]
    cl = [b[5] for b in bars]
    n = len(dates)
    vix, vix3m = macro_close("^VIX"), macro_close("^VIX3M")

    def contango(d):
        if d in vix and d in vix3m and vix3m[d] > 0:
            return vix[d] / vix3m[d] < 1.0
        return False

    def run(kill_switch, cost):
        cash, sh_, pend, standdown = CAP0, 0.0, None, 0
        nav, toggles, ks_events = [], 0, []
        for i in range(n):
            if pend is not None:
                if pend and sh_ == 0.0 and cash > 0:
                    sh_ = cash / (op[i] * (1 + cost)); cash = 0.0; toggles += 1
                elif not pend and sh_ > 0.0:
                    cash = sh_ * op[i] * (1 - cost); sh_ = 0.0; toggles += 1
                pend = None
            nav.append(cash + sh_ * cl[i])
            if standdown > 0:
                standdown -= 1
            # kill-switch check on a held day
            if (kill_switch and sh_ > 0.0 and i > 0
                    and cl[i] / cl[i - 1] - 1 <= KS_RET):
                pend = False
                standdown = KS_STAND
                ks_events.append((dates[i], cl[i] / cl[i - 1] - 1))
                continue
            want = contango(dates[i]) and standdown == 0
            if want and sh_ == 0.0:
                pend = True
            elif not want and sh_ > 0.0:
                pend = False
        return nav, toggles, ks_events

    spy = {b[1]: b[5] for b in cache_fetch("SPY") if b[1] >= START}
    sd = sorted(spy)
    spy_nav = [spy[d] / spy[sd[0]] for d in sd]
    svxy_bh = [c / cl[0] for c in cl]

    main_nav, tog, ks = run(True, COST)
    noks_nav, _, _ = run(False, COST)
    s15, _, _ = run(True, 0.0015)

    print(f"C7 SVXY carry | {dates[0]}..{dates[-1]} ({n} bars); toggles {tog}; "
          f"kill-switch events {len(ks)}")
    for d, r in ks:
        print(f"  KS fired {d}: day return {r*100:.1f}% -> exit next open + "
              f"{KS_STAND}d stand-down")
    print(f"\n{'arm':26}{'CAGR':>9}{'maxDD':>8}{'Sharpe':>8}")
    rows = {}
    for nm, nav in [("gated + kill-switch MAIN", main_nav),
                    ("gated, no kill-switch", noks_nav),
                    ("MAIN @15bps", s15),
                    ("SVXY buy-hold", svxy_bh),
                    ("SPY buy-hold", spy_nav)]:
        s = stats(nav)
        rows[nm] = s
        print(f"{nm:26}{s['cagr']*100:>8.2f}%{s['mdd']*100:>7.1f}%{s['sharpe']:>8.2f}")

    # Volmageddon trace
    print("\nVolmageddon trace (2018-02-01..2018-02-09):")
    for i in range(n):
        if "2018-02-01" <= dates[i] <= "2018-02-09":
            r = cl[i] / cl[i - 1] - 1 if i else 0
            print(f"  {dates[i]}  close {cl[i]:8.2f}  day {r*100:+7.1f}%  "
                  f"contango={contango(dates[i])}")

    m = rows["gated + kill-switch MAIN"]
    b = rows["SPY buy-hold"]
    floor = tog >= 20
    promising = (m["cagr"] > b["cagr"] and m["sharpe"] > b["sharpe"]
                 and m["mdd"] <= 0.60)
    print(f"\n=== VERDICT (prereg prereg_c7_svxy_carry.md; PROMISING-capped) ===")
    print(f"  toggles {tog} (>=20: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  MAIN {m['cagr']*100:.2f}%/DD {m['mdd']*100:.1f}%/Sh {m['sharpe']:.2f} "
          f"vs SPY {b['cagr']*100:.2f}%/Sh {b['sharpe']:.2f}")
    if not floor:
        v = "INCONCLUSIVE"
    elif promising:
        v = "PROMISING (forward-only; single window; PASS-HR/RA not claimable)"
    else:
        v = "FAIL (short-vol carry not capturable under the pre-registered bar)"
    print(f"\n  C7 VERDICT: {v}")


if __name__ == "__main__":
    main()
