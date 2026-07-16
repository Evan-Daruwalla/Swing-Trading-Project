"""E9 — "never book a loss" deep-dip audit, per prereg 9b49190.

Buy broad-US/sector ETFs at close <= 0.80*ATH, sell at +15%, NO stop, NO max
hold, K=5. Gate 2000-2013: CAGR>=15% AND maxDD<=60%, n>=10. Dual a-priori
predictions in the prereg: realized-loss rate ~0 (the seduction) but low
CAGR + large unrealized drawdown (the hidden tail). No tuning after results.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted,
dividend-UNADJUSTED (understates multi-year holds; disclosed, biases AGAINST
the strategy). Live fetch from inception; does NOT touch swing.db. Reuses
the E8 scratch cache.

NAV (finding-things map): imports run_e8_squeeze (COST, GATE_END, SEC_START,
SIM_START, cache_fetch, window_stats); swing_bot.universe (UNIVERSE).
Imported by: no other module (standalone runner).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot.universe import UNIVERSE
from run_e8_squeeze import cache_fetch, window_stats, SIM_START, GATE_END, \
    SEC_START, COST

K = 5
CAP0 = 1000.0
DIP = 0.80
TARGET = 1.15
TICKERS = [e.ticker for e in UNIVERSE if e.group in ("broad_us",
                                                     "spdr_sector")]


def simulate(data):
    all_dates = sorted({b[1] for t in data for b in data[t][0]
                        if b[1] >= SIM_START})
    cash, nav_prev = CAP0, CAP0
    pos, pend_in, pend_out = {}, {}, {}
    trades, nav_path = [], []
    last_close = {}
    idle_days = 0
    for d in all_dates:
        for t in list(pend_out):
            bars, ath, idx = data[t]
            if d in idx and t in pos:
                o = bars[idx[d]][2]
                p = pos.pop(t)
                cash += p["sh"] * o * (1 - COST)
                net = (o * (1 - COST)) / (p["fill"] * (1 + COST)) - 1
                trades.append(dict(ticker=t, entry=p["entry_date"], exit=d,
                                   net=net, hold=idx[d] - p["entry_i"],
                                   minret=p["minret"]))
                del pend_out[t]
        for t in list(pend_in):
            bars, ath, idx = data[t]
            if d in idx and t not in pos and len(pos) < K:
                o = bars[idx[d]][2]
                size = min(cash, nav_prev / K)
                if size > 10.0 and o > 0:
                    sh = size / (o * (1 + COST))
                    cash -= size
                    pos[t] = dict(sh=sh, fill=o, entry_date=d,
                                  entry_i=idx[d], minret=0.0)
                del pend_in[t]
            elif d in idx:
                del pend_in[t]
        for t in data:
            bars, ath, idx = data[t]
            if d in idx:
                last_close[t] = bars[idx[d]][5]
        nav = cash + sum(p["sh"] * last_close[t] for t, p in pos.items())
        nav_path.append((d, nav))
        if cash > 0.5 * nav:
            idle_days += 1
        nav_prev = nav
        for t, p in pos.items():
            bars, ath, idx = data[t]
            if d in idx:
                i = idx[d]
                c = bars[i][5]
                p["minret"] = min(p["minret"], c / p["fill"] - 1)
                if t not in pend_out and c >= TARGET * p["fill"]:
                    pend_out[t] = d
        cands = []
        for t in data:
            bars, ath, idx = data[t]
            if d in idx and t not in pos and t not in pend_in:
                i = idx[d]
                c = bars[i][5]
                if c <= DIP * ath[i]:
                    cands.append((c / ath[i], t))   # deepest first
        cands.sort()
        free = K - len(pos) - len(pend_in)
        for _, t in cands[:max(0, free)]:
            pend_in[t] = d
    return nav_path, trades, pos, last_close, idle_days, len(all_dates)


def main():
    data = {}
    for t in TICKERS:
        bars = cache_fetch(t)
        closes = [b[5] for b in bars]
        ath, m = [], 0.0
        for c in closes:
            m = max(m, c)
            ath.append(m)
        idx = {b[1]: i for i, b in enumerate(bars)}
        data[t] = (bars, ath, idx)
        print(f"loaded {t}: {bars[0][1]}..{bars[-1][1]} ({len(bars)} bars)",
              flush=True)
    nav_path, trades, open_pos, last_close, idle, ndays = simulate(data)

    print(f"\ntotal closed trades: {len(trades)}")
    gate = window_stats(nav_path, trades, SIM_START, GATE_END)
    sec = window_stats(nav_path, trades, SEC_START, "2099-01-01")
    full = window_stats(nav_path, trades, SIM_START, "2099-01-01")
    for name, s in [("GATE 2000-2013", gate), ("SECONDARY 2014-", sec),
                    ("FULL 2000-", full)]:
        print(f"\n{name}: CAGR {s['cagr']*100:.2f}%  ({s['mo']*100:.2f}%/mo)  "
              f"maxDD {s['mdd']*100:.1f}%  Sharpe {s['sharpe']:.2f}  "
              f"n_trades {s['n']}  win {s['win']*100:.1f}%")

    # --- audit metrics (reported regardless of verdict) ---
    losses = [x for x in trades if x["net"] < 0]
    worst_unreal = min([x["minret"] for x in trades] +
                       [p["minret"] for p in open_pos.values()] + [0.0])
    longest = max([x["hold"] for x in trades] + [0])
    print(f"\nAUDIT: realized-loss trades {len(losses)}/{len(trades)} "
          f"({100*len(losses)/max(1,len(trades)):.1f}%)")
    print(f"AUDIT: worst per-position unrealized drawdown "
          f"{worst_unreal*100:.1f}%")
    print(f"AUDIT: longest closed hold {longest} trading days "
          f"(~{longest/252:.1f} yr)")
    print(f"AUDIT: idle cash >50% of NAV on {idle}/{ndays} days "
          f"({100*idle/ndays:.1f}%)")
    for t, p in open_pos.items():
        ur = last_close[t] / p["fill"] - 1
        print(f"AUDIT: open at end: {t} entered {p['entry_date']} "
              f"unrealized {ur*100:+.1f}% (min {p['minret']*100:.1f}%)")

    g1 = gate["cagr"] >= 0.15
    g2 = gate["mdd"] <= 0.60
    g3 = gate["n"] >= 10
    print(f"\n  [{'PASS' if g1 else 'FAIL'}] gate CAGR>=15% "
          f"({gate['cagr']*100:.2f}%)")
    print(f"  [{'PASS' if g2 else 'FAIL'}] gate maxDD<=60% "
          f"({gate['mdd']*100:.1f}%)")
    print(f"  [{'OK' if g3 else 'INCONCLUSIVE'}] n_trades>=10 ({gate['n']})")
    if not g3:
        verdict = "INCONCLUSIVE"
    else:
        verdict = "PASS" if (g1 and g2) else "FAIL"
    print(f"\n  E9 VERDICT (high-return gate): {verdict}")


if __name__ == "__main__":
    main()
