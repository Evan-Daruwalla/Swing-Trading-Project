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

NAV (finding-things map): the tripwire. Covers backtest.py (E1) + rotation.py
(E4) via swing_bot.{prices, signals, universe}. RUN AFTER ANY swing_bot CHANGE:
    .venv\\Scripts\\python.exe -m swing_bot.test_frozen
d must be +/-0.0000pp at each case's declared precision. It does NOT cover the
scripts/ experiment runners (they have no frozen refs) or the M3 paper tables
(paper_sleeves' schema is orthogonal to `bars`). EXCEPTION since 2026-08-06
(audit #3): the PURE helpers of scripts/daily_swing_paper.py -- the live
orchestrator -- are pinned in INVARIANTS, because it is the highest-churn file
in the repo and the only one that submits orders.
"""
import sqlite3
import sys
from collections import namedtuple
from pathlib import Path

from swing_bot import prices, signals, backtest, rotation, paper_sleeves as ps

# scripts/ is not a package; the live orchestrator's PURE helpers are pinned
# below (audit #3), so the suite needs it importable. Import is side-effect-free
# (~1.3s, no network, no DB write) -- everything in that file runs under main().
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import daily_swing_paper as dsp        # noqa: E402  (needs the path insert above)

Case = namedtuple("Case", ["name", "value", "ref", "unit", "dp"])


def _ro_connect():
    """Open swing.db READ-ONLY. The tripwire must never take a write handle on
    the live paper ledger (audit #10).

    Delegates to prices.connect_ro() as of 2026-08-06 (audit #3): this used to
    be a local copy of that connection string, which is how six other read-only
    consumers went on calling prices.connect() unnoticed -- the contract lived
    in one module's private helper instead of beside connect() where a caller
    would see it.
    """
    return prices.connect_ro()


def _window(start, end, entries=None, k=5, size_on_nav=False):
    """Run the engine (next-open, 5bps) on a fixed swing.db window; return
    (total_return_pct, closed_count). Default entries/k = E1 config."""
    # READ-ONLY (audit #10) + explicitly closed (audit #9). prices.connect()
    # opens swing.db read-WRITE and runs CREATE TABLE IF NOT EXISTS -- the
    # tripwire was taking a write handle on the LIVE paper ledger, which the
    # 19:00 scheduled job also writes. The tripwire only ever reads, so it has
    # no business holding a write handle.
    # (Correction, audit #3 2026-08-06: this comment used to justify the fix
    # with "SQLite's default busy_timeout is 0". That is the C library's
    # default; Python's sqlite3.connect defaults timeout=5.0, so a contended
    # write waits 5s before raising, not instantly. The reason to hold a
    # read-only handle stands on its own -- a reader should not be able to
    # write -- and did not need the wrong number.)
    src = _ro_connect()
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
    src.close(); mem.close()          # audit #9: were leaked (ResourceWarning)
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

# E4 rotation engine (2026-07-09): QQQ->TQQQ N=200 lag0 5bps, fixed window
_e4_conn = _ro_connect()
_e4 = backtest.metrics(rotation.run_rotation(
    _e4_conn, "TQQQ", "QQQ", ma_len=200, exec_lag=0, cost_bps=5.0,
    start="2015-01-01", end="2016-12-31"))
_e4_conn.close()                      # audit #9
_e4_tpnl, _e4_n = _e4["total_ret"] * 100, _e4["n_trades"]

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
    Case("E4rot_1516_tpnl",   _e4_tpnl, -24.174806, "pp", 4),
    Case("E4rot_1516_switch", _e4_n,     16,        "",   0),
]

# --- Invariants (non-numeric asserts) -----------------------------------
INVARIANTS = [
    ("ibs_zero_range_is_none", signals.ibs(10.0, 10.0, 10.0) is None),
    ("ibs_inverted_is_none",   signals.ibs(8.0, 10.0, 9.0) is None),

    # --- LIVE SLEEVE DECISIONS (audit #8, added 2026-08-03) -----------------
    # These three functions decide what the M3 paper sleeves actually trade and
    # had ZERO automated coverage while daily_swing_paper.py was the repo's
    # highest-churn file. They are pure, so they need no fixtures.
    # e6_1x: long QQQ iff last close > its 200-DMA.
    ("e6_above_200dma_is_long",
     ps.decide_e6_1x([100.0] * 199 + [150.0])[0] == {"QQQ": 1.0}),
    ("e6_below_200dma_is_cash",
     ps.decide_e6_1x([100.0] * 199 + [50.0])[0] == {}),
    ("e6_short_series_refuses",
     ps.decide_e6_1x([100.0] * 50)[0] is None),
    # e18_vixts: long QQQ iff VIX/VIX3M < 1 (contango = risk-on).
    ("e18_contango_is_long",
     ps.decide_e18_vixts(15.0, 20.0)[0] == {"QQQ": 1.0}),
    ("e18_backwardation_is_cash",
     ps.decide_e18_vixts(25.0, 20.0)[0] == {}),
    ("e18_missing_vix3m_refuses",
     ps.decide_e18_vixts(15.0, None)[0] is None),
    # m10_1: VIX>THR -> residual-reversal basket, else the e6 trend rule.
    ("m10_calm_uses_trend_rule",
     ps.decide_m10_1(15.0, [100.0] * 199 + [150.0], None)[0] == {"QQQ": 1.0}),
    ("m10_stress_without_ranks_refuses",
     ps.decide_m10_1(25.0, [100.0] * 200, None)[0] is None),
    ("m10_stress_basket_is_equal_weight_K",
     ps.decide_m10_1(25.0, [100.0] * 200,
                     [(-0.5, "AAA"), (-0.4, "BBB"), (-0.3, "CCC"),
                      (-0.2, "DDD"), (0.9, "EEE")])[0]
     == {t: 1.0 / ps.STRESS_K for t in ("AAA", "BBB", "CCC", "DDD")}),

    # --- LIVE ORCHESTRATOR PURE HELPERS (audit #3, added 2026-08-06) --------
    # daily_swing_paper.py is the repo's highest-churn file (13 commits, 2x the
    # next) and the only code that submits orders, yet the suite reached NONE of
    # it. qty_reconcile_orders was deliberately refactored to be PURE so it
    # could be checked, and then never was. These need no fixtures either.
    # Reconcile is STEADY-STATE ONLY: a pending rebuild must suppress it.
    ("reconcile_suppressed_while_pending",
     dsp.qty_reconcile_orders({"QQQ": {"qty": 1.0}}, {"QQQ": {"qty": 1.5}},
                              {"QQQ": 700.0}, {"QQQ": 1.0}) == []),
    # 0.30% drift is above MIRROR_DRIFT_WARN_PCT (0.25) and $2.10 is above
    # MIN_RECONCILE_NOTIONAL ($1), so it is an actionable SELL of the excess.
    ("reconcile_acts_above_drift_band",
     [(o["side"], o["action"], o["qty"]) for o in dsp.qty_reconcile_orders(
         {"QQQ": {"qty": 1.0}}, {"QQQ": {"qty": 1.003}}, {"QQQ": 700.0}, None)]
     == [("sell", "order", 0.003)]),
    # 0.20% is inside the band -- ordinary fractional rounding, never traded.
    ("reconcile_ignores_inside_drift_band",
     dsp.qty_reconcile_orders({"QQQ": {"qty": 1.0}}, {"QQQ": {"qty": 1.002}},
                              {"QQQ": 700.0}, None) == []),
    # The liquidity floor must return None (unknown), NOT 0 (illiquid), on a
    # thin sample -- the caller treats None as "do not exclude".
    ("median_dollar_volume_refuses_thin_sample",
     dsp.median_dollar_volume(["2026-01-0%d" % i for i in range(1, 5)],
                              {"2026-01-0%d" % i: 10.0 for i in range(1, 5)},
                              {"2026-01-0%d" % i: 100 for i in range(1, 5)},
                              n=20) is None),
    # The m10_1 weekly gate is keyed on this string; a wrong week burns or
    # repeats a decision.
    ("isoweek_str_friday_2026_07_31", dsp.isoweek_str("2026-07-31") == "2026-W31"),
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
