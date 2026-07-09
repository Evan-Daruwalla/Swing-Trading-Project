"""M2.10 — run E1 per pre-registration (8963e49) and judge kill criteria.

Primary verdict basis: next-open fills, 5 bps/side (=10 bps round-trip), full
swing.db window, full 29-ETF universe. Also reports the pre-registered
context: c2c model, 0/20 bps sensitivity, per-group, split-sample.

Kill criteria (E1 PASSES only if ALL): n>=200; mean net return/trade>0;
annualized Sharpe>=0.50; max drawdown<=25%. No tuning on a FAIL.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices, universe, backtest


def subset_db(src, start=None, end=None):
    """Copy bars in [start,end] into an in-memory DB (keeps engine frozen)."""
    mem = sqlite3.connect(":memory:")
    mem.execute(prices.SCHEMA)
    q = "SELECT ticker,date,open,high,low,close,adj_close,volume FROM bars"
    cond, args = [], []
    if start:
        cond.append("date>=?"); args.append(start)
    if end:
        cond.append("date<=?"); args.append(end)
    if cond:
        q += " WHERE " + " AND ".join(cond)
    rows = src.execute(q, args).fetchall()
    mem.executemany("INSERT INTO bars VALUES (?,?,?,?,?,?,?,?)", rows)
    mem.commit()
    return mem


def show(label, conn, entries=None, fill="next_open", cost_bps=5.0):
    m = backtest.metrics(backtest.run_backtest(
        conn, entries=entries, fill=fill, cost_bps=cost_bps))
    print(f"{label:28} n={m['n_trades']:>5} "
          f"exp/trade={m['mean_net_ret']*10000:>7.1f}bps "
          f"Sharpe={m['ann_sharpe']:>6.2f} maxDD={m['max_dd']*100:>5.1f}% "
          f"CAGR={m['cagr']*100:>6.2f}% hold={m['mean_hold']:.1f}")
    return m


def main():
    conn = prices.connect()

    print("=== PRIMARY (next-open, 5bps/side = 10bps round-trip, full) ===")
    prim = show("PRIMARY next_open 5bps", conn)

    print("\n=== cost sensitivity (next-open, full) ===")
    show("next_open 0bps", conn, cost_bps=0.0)
    show("next_open 10bps/side", conn, cost_bps=10.0)

    print("\n=== reference fill model (c2c, full) ===")
    show("c2c 5bps", conn, fill="c2c", cost_bps=5.0)
    show("c2c 0bps", conn, fill="c2c", cost_bps=0.0)

    print("\n=== per-group (next-open, 5bps) ===")
    for g in ("broad_us", "spdr_sector", "country_intl"):
        ents = [e for e in universe.UNIVERSE if e.group == g]
        show(g, conn, entries=ents)

    print("\n=== split-sample (next-open, 5bps, full universe) ===")
    a = subset_db(conn, end="2021-12-31")
    b = subset_db(conn, start="2022-01-01")
    show("2014..2021", a)
    show("2022..2026", b)

    print("\n=== KILL CRITERIA (primary) ===")
    checks = [
        ("n_trades >= 200", prim["n_trades"] >= 200, prim["n_trades"]),
        ("mean net ret/trade > 0", prim["mean_net_ret"] > 0,
         f"{prim['mean_net_ret']*10000:.1f}bps"),
        ("ann Sharpe >= 0.50", prim["ann_sharpe"] >= 0.50,
         f"{prim['ann_sharpe']:.2f}"),
        ("max drawdown <= 25%", prim["max_dd"] <= 0.25,
         f"{prim['max_dd']*100:.1f}%"),
    ]
    all_ok = True
    for name, ok, val in checks:
        all_ok = all_ok and ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:26} (got {val})")
    print(f"\n  E1 VERDICT: {'PASS' if all_ok else 'FAIL'}")


if __name__ == "__main__":
    main()
