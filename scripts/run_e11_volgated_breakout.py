"""E11 - volume-gated consolidation breakout, per prereg 129dc22.

E8 IDENTICAL rules + the single added entry condition RVOL>=1.5 on the
breakout bar (RVOL = vol_t / mean(vol[t-20..t-1])). Tests whether volume
confirmation gives breakouts the directional edge E8 lacked. Gate 2000-2013
CAGR>=15% & maxDD<=60%, n>=30. No tuning after results. Reuses E8 engine and
the .e8e9_cache; does NOT touch swing.db.

NAV (finding-things map): imports run_e8_squeeze (GATE_END, SEC_START,
SIM_START, cache_fetch, indicators, simulate, window_stats);
swing_bot.universe (UNIVERSE). Imported by: no other module (standalone
runner).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from swing_bot.universe import UNIVERSE
from run_e8_squeeze import (cache_fetch, indicators, simulate, window_stats,
                            SIM_START, GATE_END, SEC_START)

RVOL_MIN = 1.5


def gate_entry_by_volume(bars, ind):
    """AND E8's entry array with RVOL>=1.5 on the breakout bar."""
    vol = [b[7] for b in bars]
    entry = list(ind["entry"])
    for i in range(len(bars)):
        if not entry[i]:
            continue
        if i < 21 or vol[i] is None:
            entry[i] = False
            continue
        base = [v for v in vol[i - 20:i] if v is not None]
        if len(base) < 20:
            entry[i] = False
            continue
        rvol = vol[i] / (sum(base) / len(base)) if sum(base) > 0 else 0.0
        if rvol < RVOL_MIN:
            entry[i] = False
    return entry


def main():
    data = {}
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        ind = indicators(bars)
        ind["entry"] = gate_entry_by_volume(bars, ind)
        idx = {b[1]: i for i, b in enumerate(bars)}
        data[e.ticker] = (bars, ind, idx)
        print(f"loaded {e.ticker}: {bars[0][1]}..{bars[-1][1]} "
              f"({len(bars)} bars, {sum(ind['entry'])} gated entries)",
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
    print(f"\n  E11 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
