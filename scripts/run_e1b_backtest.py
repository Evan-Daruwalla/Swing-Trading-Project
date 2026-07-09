"""E1b — broad_us IBS mean reversion, out-of-sample test per prereg 0126ce3.

Gate = HOLDOUT (2022-01-01..2026-07-08) on the PRIMARY universe (broad_us),
next-open, 5bps/side, must clear: n>=100, expectancy>0, Sharpe>=0.50,
maxDD<=25%. Train window + secondary universe + sensitivities are reported
context only. No tuning.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices, universe, backtest

BROAD = [e for e in universe.UNIVERSE if e.group == "broad_us"]
BROAD_SECT = [e for e in universe.UNIVERSE
              if e.group in ("broad_us", "spdr_sector")]
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


def show(label, conn, entries, fill="next_open", cost_bps=5.0):
    m = backtest.metrics(backtest.run_backtest(
        conn, entries=entries, fill=fill, cost_bps=cost_bps))
    print(f"{label:34} n={m['n_trades']:>4} "
          f"exp={m['mean_net_ret']*10000:>6.1f}bps "
          f"Sharpe={m['ann_sharpe']:>5.2f} maxDD={m['max_dd']*100:>5.1f}% "
          f"CAGR={m['cagr']*100:>6.2f}%")
    return m


def main():
    conn = prices.connect()
    train = subset(conn, *TRAIN)
    hold = subset(conn, *HOLD)

    print("=== TRAIN 2014..2021 (context, not the gate) ===")
    show("broad_us train", train, BROAD)

    print("\n=== HOLDOUT 2022..2026 (THE GATE) ===")
    gate = show("broad_us HOLDOUT next_open 5bps", hold, BROAD)

    print("\n=== holdout context (not gates) ===")
    show("broad_us HOLDOUT 0bps", hold, BROAD, cost_bps=0.0)
    show("broad_us HOLDOUT 10bps/side", hold, BROAD, cost_bps=10.0)
    show("broad_us HOLDOUT c2c 5bps", hold, BROAD, fill="c2c")
    show("broad_us+sectors HOLDOUT 5bps", hold, BROAD_SECT)

    print("\n=== KILL CRITERIA (broad_us HOLDOUT, next-open, 5bps) ===")
    checks = [
        ("n_trades >= 100", gate["n_trades"] >= 100, gate["n_trades"]),
        ("mean net ret/trade > 0", gate["mean_net_ret"] > 0,
         f"{gate['mean_net_ret']*10000:.1f}bps"),
        ("ann Sharpe >= 0.50", gate["ann_sharpe"] >= 0.50,
         f"{gate['ann_sharpe']:.2f}"),
        ("max drawdown <= 25%", gate["max_dd"] <= 0.25,
         f"{gate['max_dd']*100:.1f}%"),
    ]
    ok = True
    for name, passed, val in checks:
        ok = ok and passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name:24} (got {val})")
    print(f"\n  E1b VERDICT: {'PASS' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
