"""OHLCV price store for swing_bot.

DATA CONVENTION: yfinance with auto_adjust=False → SPLIT-ADJUSTED,
DIVIDEND-UNADJUSTED, matching the Trading project's price_cache. We keep the
dividend-UNADJUSTED `close` as the trading price and also retain `adj_close`
(dividend-adjusted) for reference only.

WHY an own store instead of reusing Trading's price_cache (decided M0.2,
2026-07-08, record Appendix F): Trading's price_cache stores only `close`,
`volume`, and derived flags — it has NO high/low/open series. IBS =
(close - low) / (high - low) needs daily High/Low/Close, so the #1 strategy
is uncomputable from it. Trading's cache is also missing DIA/IWM and every
country/international ETF, and has zero `next_open` rows for ETFs. Hence this
project fetches its own full OHLCV.

DB: swing.db at project root (gitignored). Table `bars`, PK (ticker, date).
"""
import sqlite3
from pathlib import Path

import yfinance as yf

DB_PATH = Path(__file__).resolve().parent.parent / "swing.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS bars (
    ticker    TEXT NOT NULL,
    date      TEXT NOT NULL,          -- ISO YYYY-MM-DD (session date)
    open      REAL NOT NULL,
    high      REAL NOT NULL,
    low       REAL NOT NULL,
    close     REAL NOT NULL,          -- dividend-UNADJUSTED
    adj_close REAL,                   -- dividend-adjusted, reference only
    volume    INTEGER,
    PRIMARY KEY (ticker, date)
);
"""


def connect(db_path=DB_PATH):
    conn = sqlite3.connect(str(db_path))
    conn.execute(SCHEMA)
    return conn


def _flatten(df):
    """yfinance returns a 2-level column MultiIndex even for one ticker;
    drop the ticker level so columns are Open/High/Low/Close/Adj Close/Volume.
    """
    if df.columns.nlevels == 2:
        df = df.copy()
        df.columns = df.columns.droplevel(1)
    return df


def fetch(ticker, start, end=None):
    """Fetch daily OHLCV for one ticker; return list of bar tuples.

    Rows with any NaN in O/H/L/C are dropped (yfinance occasionally emits a
    trailing partial/blank row). Prices are split-adjusted, dividend-UNADJ.
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=False,
                     progress=False, actions=False)
    if df.empty:
        return []
    df = _flatten(df)
    bars = []
    for ts, row in df.iterrows():
        o, h, l, c = row["Open"], row["High"], row["Low"], row["Close"]
        if any(v != v for v in (o, h, l, c)):  # NaN check
            continue
        adj = row.get("Adj Close")
        vol = row.get("Volume")
        bars.append((
            ticker, ts.strftime("%Y-%m-%d"),
            float(o), float(h), float(l), float(c),
            None if adj is None or adj != adj else float(adj),
            None if vol is None or vol != vol else int(vol),
        ))
    return bars


def store(conn, bars):
    """Idempotent upsert of bar tuples. Returns rows written."""
    conn.executemany(
        "INSERT OR REPLACE INTO bars "
        "(ticker, date, open, high, low, close, adj_close, volume) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", bars)
    conn.commit()
    return len(bars)


def backfill(conn, ticker, start="2014-01-01", end=None):
    """Fetch + store one ticker. Returns rows written."""
    return store(conn, fetch(ticker, start, end))


def coverage(conn, ticker):
    """Return (n_rows, min_date, max_date) for a ticker in the store."""
    return conn.execute(
        "SELECT count(*), min(date), max(date) FROM bars WHERE ticker=?",
        (ticker,)).fetchone()
