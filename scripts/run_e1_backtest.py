"""M2.10 — run E1 per pre-registration (8963e49) and judge kill criteria.

Primary verdict basis: next-open fills, 5 bps/side (=10 bps round-trip), full
swing.db window, full 29-ETF universe. Also reports the pre-registered
context: c2c model, 0/20 bps sensitivity, per-group, split-sample.

Kill criteria (E1 PASSES only if ALL): n>=200; mean net return/trade>0;
annualized Sharpe>=0.50; max drawdown<=25%. No tuning on a FAIL.

NAV (finding-things map): imports swing_bot (backtest, prices, universe).
Imported by: no other module (standalone runner).
"""
# DATA CONVENTION: prices are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED (auto_adjust=False)
# -- swing_bot/prices.py & the shared cache both enforce it; stated here per CLAUDE.md.
import os
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
        conn, entries=entries, fill=fill, cost_bps=cost_bps,
        liq=f3_liq(conn, entries)))
    print(f"{label:28} n={m['n_trades']:>5} "
          f"exp/trade={m['mean_net_ret']*10000:>7.1f}bps "
          f"Sharpe={m['ann_sharpe']:>6.2f} maxDD={m['max_dd']*100:>5.1f}% "
          f"CAGR={m['cagr']*100:>6.2f}% hold={m['mean_hold']:.1f}")
    return m


F3_FLOOR = os.environ.get("SWING_F3_FLOOR", "1") != "0"
_F3_CACHE = {}


def f3_liq(conn, entries):
    """{ticker: {date: eligible}} under the liquidity floor, or None when the arm
    is OFF (F3, 2026-09-05, prereg_f3_liquidity_floor_etf_scope.md).

    Reads close+volume from swing.db directly rather than through
    backtest._load, which drops volume — see the note in run_backtest's
    docstring. Cached per entry-set because show() is called many times per run
    and the mask does not change between them.

    DATA VINTAGE: swing.db `bars` is the BACKTEST store and is stale since
    2026-07-08 (record FH). That is fine for an A/B — both arms read the same
    rows — but E1's numbers here are NOT comparable to the .e8e9_cache runs
    (E8/E9/E11/E12/C3), which are pinned at 2026-08-17.
    """
    if not F3_FLOOR:
        print("  [F3 liquidity floor: OFF -- pre-F3 path, SWING_F3_FLOOR=0]")
        return None
    key = tuple(e.ticker for e in (entries or universe.UNIVERSE))
    if key in _F3_CACHE:
        return _F3_CACHE[key]
    from swing_bot import universe as _u
    out, sub = {}, {}
    for tk in key:
        rows = conn.execute(
            "SELECT date, close, volume FROM bars WHERE ticker=? ORDER BY date",
            (tk,)).fetchall()
        # liquidity_mask wants the shared bar layout; close_ix/vol_ix name where
        # they are in THIS tuple rather than reshaping the rows.
        mask = _u.liquidity_mask(rows, close_ix=1, vol_ix=2)
        out[tk] = {r[0]: m for r, m in zip(rows, mask)}
        n = sum(1 for i in range(9, len(mask)) if not mask[i])
        if n:
            sub[tk] = n
    print("  [F3 liquidity floor: ON at $%.0fM/day -- %d of %d names have a "
          "MEASURABLE sub-floor bar (%d bars); swing.db vintage]"
          % (_u.MIN_MEDIAN_DOLLAR_VOL / 1e6, len(sub), len(key), sum(sub.values())))
    if sub:
        top = sorted(sub.items(), key=lambda kv: -kv[1])[:8]
        print("   sub-floor bars: " + ", ".join("%s %d" % kv for kv in top))
    _F3_CACHE[key] = out
    return out


def main():
    # READ-ONLY (audit #3): this only reads swing.db, and the 19:00
    # scheduled job writes it. connect() would take a write handle and
    # run CREATE TABLE IF NOT EXISTS against the live paper ledger.
    conn = prices.connect_ro()

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
