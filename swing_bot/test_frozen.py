"""Frozen-regression tripwire for swing_bot.

Pattern ported from the Trading project (`trading_bot/strategies/
test_strategies.py`): pin deterministic quantities to EXACT reference numbers
and fail loud on any drift (d must be 0 at the case's declared precision — the
project's d=+/-0.0000pp discipline). A cheap tripwire against silent
regressions from "obviously unrelated" changes.

Runs via its OWN __main__ (no pytest needed):
    .venv\\Scripts\\python.exe -m swing_bot.test_frozen

M2.11 STATUS: real E1 references pinned. The numeric cases run the E1 engine
(frozen pre-reg `8963e49`: next-open, 5bps/side) on two fixed windows of the
backfilled `swing.db` and pin total-return% (unit 'pp', dp 4) and closed-
trade count (unit '', dp 0). If this test goes RED after a code change with
no data change, a regression was introduced. NOTE: it depends on the frozen
`swing.db` backfill (M0.3 universe, 2014-01-01 start) — a RED after a
re-backfill with unchanged code means upstream yfinance DATA drift, not a
code bug; investigate the data. Do not delete this harness; extend
REFERENCES.
"""
import sqlite3
from collections import namedtuple

from swing_bot import prices, signals, backtest

Case = namedtuple("Case", ["name", "value", "ref", "unit", "dp"])


def _window(start, end, entries=None, k=5, size_on_nav=False):
    """Run the engine (next-open, 5bps) on a fixed swing.db window; return
    (total_return_pct, closed_count). Default entries/k = E1 config."""
    src = prices.connect()
    mem = sqlite3.connect(":memory:")
    mem.execute(prices.SCHEMA)
    rows = src.execute(
        "SELECT ticker,date,open,high,low,close,adj_close,volume FROM bars "
        "WHERE date>=? AND date<=?", (start, end)).fetchall()
    mem.executemany("INSERT INTO bars VALUES (?,?,?,?,?,?,?,?)", rows)
    mem.commit()
    m = backtest.metrics(backtest.run_backtest(mem, entries=entries,
                                               fill="next_open",
                                               cost_bps=5.0, k=k,
                                               size_on_nav=size_on_nav))
    return m["total_ret"] * 100, m["n_trades"]

_w1_tpnl, _w1_n = _window("2019-01-01", "2019-06-30")
_w2_tpnl, _w2_n = _window("2020-01-01", "2020-06-30")

# E2 config: LEVERAGED universe, K=2 (prereg 865c09e; verdict FAIL,
# record Appendix T — pinned so the failed result stays tamper-evident)
from swing_bot import universe as _universe
_e2w1_tpnl, _e2w1_n = _window("2019-01-01", "2019-06-30",
                              entries=_universe.LEVERAGED, k=2)
_e2w2_tpnl, _e2w2_n = _window("2020-01-01", "2020-06-30",
                              entries=_universe.LEVERAGED, k=2)

# Engine v2 (C1 2026-07-09): NAV-proportional cash-capped sizing path
_v2w1_tpnl, _v2w1_n = _window("2019-01-01", "2019-06-30", size_on_nav=True)

# --- REAL E1 references (M2.11), pinned 2026-07-09 -----------------------
# E1 = full 29-ETF universe, next-open, 5bps/side. These are the deterministic
# engine outputs; E1 FAILED its kill criteria (record Appendix O) but the
# tripwire pins the engine so the result stays tamper-evident.
REFERENCES = [
    Case("E1_2019H1_tpnl",   _w1_tpnl, 8.815909, "pp", 4),
    Case("E1_2019H1_closed", _w1_n,    134,      "",   0),
    Case("E1_2020H1_tpnl",   _w2_tpnl, 6.209800, "pp", 4),
    Case("E1_2020H1_closed", _w2_n,    162,      "",   0),
    Case("E2_2019H1_tpnl",   _e2w1_tpnl, 25.374807, "pp", 4),
    Case("E2_2019H1_closed", _e2w1_n,    31,        "",   0),
    Case("E2_2020H1_tpnl",   _e2w2_tpnl, 60.397839, "pp", 4),
    Case("E2_2020H1_closed", _e2w2_n,    56,        "",   0),
    Case("E1v2_2019H1_tpnl",   _v2w1_tpnl, 9.016509, "pp", 4),
    Case("E1v2_2019H1_closed", _v2w1_n,    134,      "",   0),
]

# --- Invariants (non-numeric asserts) -----------------------------------
INVARIANTS = [
    ("ibs_zero_range_is_none", signals.ibs(10.0, 10.0, 10.0) is None),
    ("ibs_inverted_is_none",   signals.ibs(8.0, 10.0, 9.0) is None),
]


def run():
    ok = True
    print(f"{'case':24}{'value':>14}{'ref':>14}{'d':>14}  result")
    print("-" * 82)
    for c in REFERENCES:
        d = round(c.value - c.ref, c.dp)
        passed = (d == 0)
        ok = ok and passed
        u = c.unit
        print(f"{c.name:24}{c.value:>14.{c.dp}f}{c.ref:>14.{c.dp}f}"
              f"{('%+.*f%s' % (c.dp, d, u)):>14}  "
              f"{'PASS' if passed else 'FAIL <<<'}")
    print("-" * 82)
    for name, cond in INVARIANTS:
        ok = ok and cond
        print(f"{name:24}{'':>42}  {'PASS' if cond else 'FAIL <<<'}")
    print("-" * 82)
    print("FROZEN TESTS:", "GREEN (all d=0)" if ok else "RED - DRIFT DETECTED")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
