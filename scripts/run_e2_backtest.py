"""E2 — leveraged-ETF IBS, per prereg 865c09e.

Gate = HOLDOUT (2022-01-01..2026-07-08), K=2, next-open, 5bps/side, must
clear: n>=100, expectancy>0, net CAGR>=15%, maxDD<=60%. Sharpe reported as
context (not a gate). Train window + K=1/K=3 + cost/fill sensitivities are
reported context only. PRE-COMMITTED STOP: if E2 fails, the IBS family is
shelved. No tuning.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices, universe, backtest

LEV = universe.LEVERAGED
TRAIN = ("2014-01-02", "2021-12-31")
HOLD = ("2022-01-01", "2026-07-08")


def subset(src, start, end):
    mem = sqlite3.connect(":memory:")
    mem.execute(prices.SCHEMA)
    rows = src.execute(
        "SELECT ticker,date,open,high,low,close,adj_close,volume FROM bars "
        "WHERE date>=? AND date<=?", (start, end)).fetchall()
    mem.executemany("INSERT INTO bars VALUES (?,?,?,?,?,?,?,?)", rows)
    mem.commit()
    return mem


def show(label, conn, k=2, fill="next_open", cost_bps=5.0):
    m = backtest.metrics(backtest.run_backtest(
        conn, entries=LEV, fill=fill, cost_bps=cost_bps, k=k))
    print(f"{label:32} n={m['n_trades']:>4} "
          f"exp={m['mean_net_ret']*10000:>7.1f}bps "
          f"CAGR={m['cagr']*100:>7.2f}% maxDD={m['max_dd']*100:>5.1f}% "
          f"Sharpe={m['ann_sharpe']:>5.2f} hold={m['mean_hold']:.1f}")
    return m


def main():
    conn = prices.connect()
    train = subset(conn, *TRAIN)
    hold = subset(conn, *HOLD)

    print("=== TRAIN 2014..2021 (context) ===")
    show("K=2 train", train)

    print("\n=== HOLDOUT 2022..2026 (THE GATE, K=2 next-open 5bps) ===")
    gate = show("K=2 HOLDOUT", hold)

    print("\n=== holdout context (not gates) ===")
    show("K=1 HOLDOUT", hold, k=1)
    show("K=3 HOLDOUT", hold, k=3)
    show("K=2 HOLDOUT 0bps", hold, cost_bps=0.0)
    show("K=2 HOLDOUT 10bps/side", hold, cost_bps=10.0)
    show("K=2 HOLDOUT c2c 5bps", hold, fill="c2c")

    print("\n=== KILL CRITERIA (K=2 HOLDOUT, next-open, 5bps/side) ===")
    checks = [
        ("n_trades >= 100", gate["n_trades"] >= 100, gate["n_trades"]),
        ("mean net ret/trade > 0", gate["mean_net_ret"] > 0,
         f"{gate['mean_net_ret']*10000:.1f}bps"),
        ("net CAGR >= 15%", gate["cagr"] >= 0.15,
         f"{gate['cagr']*100:.2f}%"),
        ("max drawdown <= 60%", gate["max_dd"] <= 0.60,
         f"{gate['max_dd']*100:.1f}%"),
    ]
    ok = True
    for name, passed, val in checks:
        ok = ok and passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name:24} (got {val})")
    print(f"\n  E2 VERDICT: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  (pre-committed stop: IBS family SHELVED)")


if __name__ == "__main__":
    main()
