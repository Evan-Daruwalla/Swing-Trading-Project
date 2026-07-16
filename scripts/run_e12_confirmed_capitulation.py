"""E12 - confirmed-capitulation mean reversion ("right side of the V"),
per prereg 129dc22.

Arm on >=15% drop off the 10-day high WITH RVOL>=1.5 volume climax (armed 5
days); enter on first close>prior-day-high (confirmed reversal); exit on
close<prior-day-low (prior-bar-low trail) or 40-bar max hold. K=3. Distinct
from E1 IBS (waits for confirmation vs buying the dip). Gate 2000-2013
CAGR>=15% & maxDD<=60%, n>=30. No tuning. Reuses .e8e9_cache; no swing.db.

NAV (finding-things map): imports run_e8_squeeze (CAP0, COST, GATE_END, K,
MAX_HOLD, SEC_START, SIM_START, cache_fetch, window_stats);
swing_bot.universe (UNIVERSE). Imported by: no other module (standalone
runner).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from swing_bot.universe import UNIVERSE
from run_e8_squeeze import (cache_fetch, window_stats, SIM_START, GATE_END,
                            SEC_START, K, COST, CAP0, MAX_HOLD)

DROP = 0.85          # close <= 0.85 * max(close[i-10..i])  => >=15% off high
RVOL_MIN = 1.5
ARM_DAYS = 5


def signals(bars):
    """Return per-bar (entry_sig, exit_sig, drop_ratio). entry at close i =>
    execute next open; exit_sig i (close_i<low_{i-1}) => execute next open."""
    n = len(bars)
    o = [b[2] for b in bars]; h = [b[3] for b in bars]
    l = [b[4] for b in bars]; c = [b[5] for b in bars]; v = [b[7] for b in bars]
    entry = [False] * n
    exit_s = [False] * n
    drop = [1.0] * n
    armed_until = -1
    for i in range(n):
        if i >= 20:
            mx10 = max(c[i - 10:i + 1])
            drop[i] = c[i] / mx10 if mx10 > 0 else 1.0
            base = [x for x in v[i - 20:i] if x is not None]
            avgv = sum(base) / len(base) if base else 0.0
            climax = v[i] is not None and avgv > 0 and v[i] >= RVOL_MIN * avgv
            if drop[i] <= DROP and climax:
                armed_until = i + ARM_DAYS
            if i <= armed_until and c[i] > h[i - 1]:
                entry[i] = True
                armed_until = -1        # disarm on trigger
        if i >= 1 and c[i] < l[i - 1]:
            exit_s[i] = True
    return dict(o=o, c=c, entry=entry, exit=exit_s, drop=drop)


def simulate(data):
    all_dates = sorted({b[1] for t in data for b in data[t][0]
                        if b[1] >= SIM_START})
    cash, nav_prev = CAP0, CAP0
    pos, pend_in, pend_out = {}, {}, {}
    trades, nav_path, last_close = [], [], {}
    for d in all_dates:
        for t in list(pend_out):
            bars, sig, idx = data[t]
            if d in idx and t in pos:
                op = sig["o"][idx[d]]
                p = pos.pop(t)
                cash += p["sh"] * op * (1 - COST)
                trades.append(dict(ticker=t, entry=p["entry_date"], exit=d,
                                   net=(op * (1 - COST)) / (p["fill"] * (1 + COST)) - 1,
                                   hold=idx[d] - p["entry_i"]))
                del pend_out[t]
        for t in list(pend_in):
            bars, sig, idx = data[t]
            if d in idx and t not in pos and len(pos) < K:
                op = sig["o"][idx[d]]
                size = min(cash, nav_prev / K)
                if size > 10.0 and op > 0:
                    sh = size / (op * (1 + COST))
                    cash -= size
                    pos[t] = dict(sh=sh, fill=op, entry_date=d, entry_i=idx[d])
                del pend_in[t]
            elif d in idx:
                del pend_in[t]
        for t in data:
            bars, sig, idx = data[t]
            if d in idx:
                last_close[t] = sig["c"][idx[d]]
        nav = cash + sum(p["sh"] * last_close[t] for t, p in pos.items())
        nav_path.append((d, nav)); nav_prev = nav
        # exits signalled at close
        for t, p in list(pos.items()):
            bars, sig, idx = data[t]
            if d in idx:
                i = idx[d]
                if t not in pend_out and (sig["exit"][i]
                                          or i - p["entry_i"] >= MAX_HOLD):
                    pend_out[t] = d
        # entries signalled at close (rank deepest drop first)
        cands = []
        for t in data:
            bars, sig, idx = data[t]
            if d in idx and t not in pos and t not in pend_in:
                i = idx[d]
                if sig["entry"][i]:
                    cands.append((sig["drop"][i], t))
        cands.sort()
        free = K - len(pos) - len(pend_in)
        for _, t in cands[:max(0, free)]:
            pend_in[t] = d
    return nav_path, trades, pos, last_close


def main():
    data = {}
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        sig = signals(bars)
        idx = {b[1]: i for i, b in enumerate(bars)}
        data[e.ticker] = (bars, sig, idx)
        print(f"loaded {e.ticker}: {bars[0][1]}..{bars[-1][1]} "
              f"({len(bars)} bars, {sum(sig['entry'])} entry signals)",
              flush=True)
    nav_path, trades, open_pos, last_close = simulate(data)
    print(f"\ntotal closed trades: {len(trades)}; open at end: {list(open_pos)}")
    gate = window_stats(nav_path, trades, SIM_START, GATE_END)
    sec = window_stats(nav_path, trades, SEC_START, "2099-01-01")
    full = window_stats(nav_path, trades, SIM_START, "2099-01-01")
    for name, s in [("GATE 2000-2013", gate), ("SECONDARY 2014-", sec),
                    ("FULL 2000-", full)]:
        if s is None:
            print(f"\n{name}: <30 bars, n/a")
            continue
        print(f"\n{name}: CAGR {s['cagr']*100:.2f}%  ({s['mo']*100:.2f}%/mo)  "
              f"maxDD {s['mdd']*100:.1f}%  Sharpe {s['sharpe']:.2f}  "
              f"n_trades {s['n']}  win {s['win']*100:.1f}%")
    g1 = gate["cagr"] >= 0.15
    g2 = gate["mdd"] <= 0.60
    g3 = gate["n"] >= 30
    print(f"\n  [{'PASS' if g1 else 'FAIL'}] gate CAGR>=15% ({gate['cagr']*100:.2f}%)")
    print(f"  [{'PASS' if g2 else 'FAIL'}] gate maxDD<=60% ({gate['mdd']*100:.1f}%)")
    print(f"  [{'OK' if g3 else 'INCONCLUSIVE'}] n_trades>=30 ({gate['n']})")
    if not g3:
        verdict = "INCONCLUSIVE"
    else:
        s1 = sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60
        verdict = "PASS" if (g1 and g2 and s1) else "FAIL"
        print(f"  [{'PASS' if s1 else 'FAIL'}] secondary CAGR>=15% & DD<=60% "
              f"({sec['cagr']*100:.2f}%, {sec['mdd']*100:.1f}%)")
    print(f"\n  E12 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
