"""E4 — 200d-MA leverage rotation, per prereg 313d88a. No tuning.

PRIMARY cell: QQQ->TQQQ, N=200, lag 0, 5bps. Gates on the full window
(holdout contaminated by the B4 screen — see prereg §0). Robustness battery =
MA{150,175,200,225,250} x lag{0,1} x cost{5,10} (20 cells). Benchmarks:
buy-hold TQQQ, buy-hold QQQ. Live paper is the true OOS (Evan-gated).

NAV (finding-things map): imports swing_bot (backtest, prices, rotation).
Imported by: no other module (standalone runner).
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices, rotation, backtest

FULL = ("2014-01-02", "2026-07-08")


def met(res):
    return backtest.metrics(res)


def mopct(m):
    return (1 + m["cagr"]) ** (1 / 12) - 1


def main():
    conn = prices.connect()

    # --- benchmarks ---
    bh_tqqq = met(rotation.buy_hold(conn, "TQQQ", *FULL))
    bh_qqq = met(rotation.buy_hold(conn, "QQQ", *FULL))
    print("=== benchmarks (full window) ===")
    for lbl, m in [("buy-hold TQQQ", bh_tqqq), ("buy-hold QQQ", bh_qqq)]:
        print(f"{lbl:16} CAGR={m['cagr']*100:>7.2f}% "
              f"maxDD={m['max_dd']*100:>5.1f}% {mopct(m)*100:>5.2f}%/mo")

    # --- primary cell ---
    prim = met(rotation.run_rotation(conn, "TQQQ", "QQQ", ma_len=200,
                                     exec_lag=0, cost_bps=5.0,
                                     start=FULL[0], end=FULL[1]))
    print("\n=== PRIMARY QQQ->TQQQ N=200 lag0 5bps (full) ===")
    print(f"CAGR={prim['cagr']*100:.2f}%  {mopct(prim)*100:.2f}%/mo  "
          f"maxDD={prim['max_dd']*100:.1f}%  Sharpe={prim['ann_sharpe']:.2f}  "
          f"switches={prim['n_trades']}")

    # --- robustness battery ---
    print("\n=== robustness battery (QQQ->TQQQ, full window) ===")
    cell_cagr, by_ma = [], {}
    for N in (150, 175, 200, 225, 250):
        for lag in (0, 1):
            for cost in (5.0, 10.0):
                m = met(rotation.run_rotation(conn, "TQQQ", "QQQ", ma_len=N,
                                              exec_lag=lag, cost_bps=cost,
                                              start=FULL[0], end=FULL[1]))
                cell_cagr.append(m["cagr"])
                by_ma.setdefault(N, []).append(m["cagr"])
                print(f"  N={N} lag={lag} cost={cost:>4.0f}: "
                      f"CAGR={m['cagr']*100:>7.2f}% "
                      f"{mopct(m)*100:>5.2f}%/mo maxDD={m['max_dd']*100:>5.1f}%")
    pos_frac = sum(1 for c in cell_cagr if c > 0) / len(cell_cagr)
    med = statistics.median(cell_cagr)
    ma_pos = {N: all(c > 0 for c in cs) for N, cs in by_ma.items()}

    # --- secondary context ---
    print("\n=== secondary (context, not gates) ===")
    for fund, sig in [("SPXL", "SPY"), ("SOXL", "SOXL")]:
        m = met(rotation.run_rotation(conn, fund, sig, ma_len=200, exec_lag=0,
                                      cost_bps=5.0, start=FULL[0], end=FULL[1]))
        print(f"  {sig}->{fund} N=200 lag0 5bps: CAGR={m['cagr']*100:>7.2f}% "
              f"{mopct(m)*100:>5.2f}%/mo maxDD={m['max_dd']*100:>5.1f}%")

    # --- kill criteria ---
    print("\n=== KILL CRITERIA (prereg 313d88a) ===")
    c1 = prim["cagr"] >= 0.15
    c2 = prim["max_dd"] <= 0.65
    c3a = prim["max_dd"] <= bh_tqqq["max_dd"] - 0.15
    c3b = prim["cagr"] >= bh_qqq["cagr"]
    c4 = (pos_frac >= 0.80) and (med >= 0.10) and all(ma_pos.values())
    checks = [
        ("1 CAGR>=15%", c1, f"{prim['cagr']*100:.1f}%"),
        ("2 maxDD<=65%", c2, f"{prim['max_dd']*100:.1f}%"),
        ("3a cuts BH-TQQQ DD by >=15pp", c3a,
         f"{prim['max_dd']*100:.1f}% vs {bh_tqqq['max_dd']*100:.1f}%"),
        ("3b CAGR>=BH-QQQ", c3b,
         f"{prim['cagr']*100:.1f}% vs {bh_qqq['cagr']*100:.1f}%"),
        ("4 non-fragile grid", c4,
         f"pos={pos_frac*100:.0f}% med={med*100:.1f}% ma_all_pos={all(ma_pos.values())}"),
    ]
    ok = True
    for name, passed, val in checks:
        ok = ok and passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name:32} ({val})")
    print(f"\n  E4 VERDICT: {'PASS' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
