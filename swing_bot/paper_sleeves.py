"""M3 forward-paper sleeve tracking: DB schema + per-sleeve signal decisions.

Three sleeves, one per documented forward-paper candidate (HANDOFF 2026-07-14):
  e6_1x       - QQQ 1x, invested iff QQQ > 200-DMA (E6 prereg 0526ea2)
  e18_vixts   - QQQ 1x, invested iff VIX/VIX3M < 1 (E18 prereg f32b008, arm a)
  m10_1_nagel - weekly VIX-gated switch: VIX>20 -> bottom-K=4 FF3-residual
                reversal on the 39-survivor universe; VIX<=20 -> QQQ 200-DMA
                trend (M10-1 prereg_m10_1_nagel_switch.md, IN-SAMPLE-COMPOSED)

Every decide_* function here reuses the IDENTICAL signal condition as its
backtest runner (same threshold, same SMA window, same residual machinery) —
this is load-bearing for M3's success criterion (implementation fidelity vs a
shadow backtest, PRD task 51 amendment). Where a backtest runner's own helper
caches PERMANENTLY (e.g. run_e8_squeeze.cache_fetch, run_c1_residual_reversal
.ff3_daily) it is deliberately NOT reused here — live paper needs a fresh
fetch every run, backtests need a frozen one. The pure math (residual_series,
sma) IS reused verbatim.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False),
matching swing_bot.prices. All fills are next-open after a close-computed
signal — never same-bar. No look-ahead: decide_*() must only be called with
data up to and including the "as of" date.

Schema is separate from the `bars` table (prices.py) and untouched by
test_frozen.py's pinned refs — safe to extend without risking the tripwire.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "swing.db"
CAP0 = 1000.0     # starting notional per sleeve; matches E6/M10-1 backtest CAP0
SLEEVES = ("e6_1x", "e18_vixts", "m10_1_nagel")
STRESS_K = 4       # M10-1 stress-mode basket size (matches C1's K)

SCHEMA = """
CREATE TABLE IF NOT EXISTS paper_sleeves (
    sleeve            TEXT PRIMARY KEY,
    cash              REAL NOT NULL,
    started_at        TEXT NOT NULL,
    last_decided_week  TEXT,          -- 'YYYY-Www' of the last weekly decision applied (m10_1_nagel only)
    pending_json      TEXT,           -- JSON target awaiting next-open fill, or NULL
    pending_signal_date TEXT,         -- close date that produced pending_json
    last_run_at       TEXT
);

CREATE TABLE IF NOT EXISTS paper_positions (
    sleeve      TEXT NOT NULL,
    ticker      TEXT NOT NULL,
    qty         REAL NOT NULL,
    entry_price REAL NOT NULL,
    entry_date  TEXT NOT NULL,
    PRIMARY KEY (sleeve, ticker)
);

CREATE TABLE IF NOT EXISTS paper_transactions (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    sleeve  TEXT NOT NULL,
    date    TEXT NOT NULL,
    ticker  TEXT NOT NULL,
    side    TEXT NOT NULL,           -- buy | sell
    qty     REAL NOT NULL,
    price   REAL NOT NULL,           -- DB-simulated fill price (next open)
    reason  TEXT
);

CREATE TABLE IF NOT EXISTS paper_nav (
    sleeve TEXT NOT NULL,
    date   TEXT NOT NULL,
    nav    REAL NOT NULL,
    PRIMARY KEY (sleeve, date)
);

CREATE TABLE IF NOT EXISTS fill_divergence (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sleeve          TEXT NOT NULL,
    date            TEXT NOT NULL,
    ticker          TEXT NOT NULL,
    sim_price       REAL NOT NULL,    -- our DB-simulated fill (yfinance next open)
    alpaca_price    REAL,             -- actual Alpaca paper fill $, if mirrored
    alpaca_order_id TEXT,
    logged_at       TEXT NOT NULL
);
"""


def connect(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def init_sleeve(conn, sleeve, cap0=CAP0):
    """Idempotent — does not reset cash/positions if the sleeve already exists."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT OR IGNORE INTO paper_sleeves (sleeve, cash, started_at) VALUES (?, ?, ?)",
        (sleeve, cap0, now))
    conn.commit()


def get_sleeve(conn, sleeve):
    row = conn.execute("SELECT * FROM paper_sleeves WHERE sleeve=?", (sleeve,)).fetchone()
    return dict(row) if row else None


def get_positions(conn, sleeve):
    rows = conn.execute("SELECT * FROM paper_positions WHERE sleeve=?", (sleeve,)).fetchall()
    return {r["ticker"]: dict(r) for r in rows}


def set_pending(conn, sleeve, target, signal_date):
    conn.execute(
        "UPDATE paper_sleeves SET pending_json=?, pending_signal_date=? WHERE sleeve=?",
        (json.dumps(target), signal_date, sleeve))
    conn.commit()


def clear_pending(conn, sleeve):
    conn.execute(
        "UPDATE paper_sleeves SET pending_json=NULL, pending_signal_date=NULL WHERE sleeve=?",
        (sleeve,))
    conn.commit()


def touch_run(conn, sleeve):
    conn.execute("UPDATE paper_sleeves SET last_run_at=? WHERE sleeve=?",
                 (datetime.now(timezone.utc).isoformat(), sleeve))
    conn.commit()


def record_fill(conn, sleeve, date, ticker, side, qty, price, reason):
    conn.execute(
        "INSERT INTO paper_transactions (sleeve, date, ticker, side, qty, price, reason) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)", (sleeve, date, ticker, side, qty, price, reason))
    conn.commit()


def upsert_position(conn, sleeve, ticker, qty, entry_price, entry_date):
    if qty <= 0:
        conn.execute("DELETE FROM paper_positions WHERE sleeve=? AND ticker=?",
                     (sleeve, ticker))
    else:
        conn.execute(
            "INSERT INTO paper_positions (sleeve, ticker, qty, entry_price, entry_date) "
            "VALUES (?, ?, ?, ?, ?) ON CONFLICT(sleeve, ticker) DO UPDATE SET "
            "qty=excluded.qty, entry_price=excluded.entry_price, entry_date=excluded.entry_date",
            (sleeve, ticker, qty, entry_price, entry_date))
    conn.commit()


def record_nav(conn, sleeve, date, nav):
    conn.execute(
        "INSERT INTO paper_nav (sleeve, date, nav) VALUES (?, ?, ?) "
        "ON CONFLICT(sleeve, date) DO UPDATE SET nav=excluded.nav",
        (sleeve, date, nav))
    conn.commit()


def log_divergence(conn, sleeve, date, ticker, sim_price, alpaca_price=None, alpaca_order_id=None):
    conn.execute(
        "INSERT INTO fill_divergence (sleeve, date, ticker, sim_price, alpaca_price, "
        "alpaca_order_id, logged_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sleeve, date, ticker, sim_price, alpaca_price, alpaca_order_id,
         datetime.now(timezone.utc).isoformat()))
    conn.commit()


# ---------------------------------------------------------------------------
# Signal decisions — one target dict per sleeve, e.g. {"QQQ": 1.0} (100%
# weight) or {} (cash) or {"AAPL": 0.25, "MSFT": 0.25, ...} (equal-weight
# basket). Callers translate weights -> $ notional using the sleeve's NAV.
# ---------------------------------------------------------------------------

def sma(series, n):
    """Verbatim copy of run_e18_regime_gates.sma (avoids importing a scripts/
    module into swing_bot for a 4-line function)."""
    out = [None] * len(series)
    for i in range(n - 1, len(series)):
        out[i] = sum(series[i - n + 1:i + 1]) / n
    return out


def decide_e6_1x(qqq_close_series):
    """qqq_close_series: chronological list of QQQ closes ending at 'today'.
    Target = 100% QQQ iff today's close > 200-DMA, else cash. (E6, prereg
    0526ea2 — identical condition to run_e6_deleveraged.rotation_nav.)"""
    if len(qqq_close_series) < 200:
        return None, "insufficient history (<200 sessions)"
    m = sum(qqq_close_series[-200:]) / 200.0
    return ({"QQQ": 1.0} if qqq_close_series[-1] > m else {}), None


def decide_e18_vixts(vix_today, vix3m_today):
    """Target = 100% QQQ iff VIX/VIX3M < 1.0, else cash. (E18 arm (a), prereg
    f32b008 — identical condition to run_e18_regime_gates gates['(a)'].)"""
    if vix_today is None or vix3m_today is None or vix3m_today <= 0:
        return None, "VIX or VIX3M unavailable today"
    return ({"QQQ": 1.0} if (vix_today / vix3m_today) < 1.0 else {}), None


def decide_m10_1(vix_today, qqq_close_series, residual_ranks=None):
    """VIX>20 -> bottom-K=4 equal-weight FF3-residual reversal basket
    (residual_ranks = pre-sorted [(residual, ticker), ...] ascending, caller
    supplies it via run_c1_residual_reversal.residual_series so the ranking
    math is byte-identical to the backtest); VIX<=20 -> QQQ 200-DMA trend
    (same condition as decide_e6_1x). (M10-1, prereg_m10_1_nagel_switch.md,
    thr=20.0 — IN-SAMPLE-COMPOSED, forward-paper-required per the M10 cap.)"""
    if vix_today is None:
        return None, "VIX unavailable today"
    if vix_today > 20.0:
        if residual_ranks is None or len(residual_ranks) < STRESS_K:
            return None, "insufficient residual-ranked names for stress basket"
        names = [t for _, t in residual_ranks[:STRESS_K]]
        w = 1.0 / STRESS_K
        return {t: w for t in names}, None
    trend, err = decide_e6_1x(qqq_close_series)
    return trend, err
