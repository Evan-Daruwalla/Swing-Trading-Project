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

NAV (finding-things map): foundation OHLCV store, no swing_bot deps of its own.
Imported by swing_bot.{backtest, rotation, coverage_gate, test_frozen} and ~15
scripts/ runners (run_e1..e8, run_e4_rotation, run_e6_deleveraged,
daily_swing_paper, ...). CAVEAT: most scripts/ EXPERIMENTS do not read prices
directly — they fetch via `run_e8_squeeze.cache_fetch` (a permanent on-disk
yfinance cache; that function is the repo's real shared data layer, ~26
importers). This module is the store used by the swing_bot engines + the live
M3 loop; cache_fetch is the store used by the experiment jungle.
"""
import sqlite3
import time
from pathlib import Path

import yfinance as yf

from swing_bot import DB_PATH   # single home (M13.6)

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
    """READ-WRITE handle; also runs CREATE TABLE IF NOT EXISTS.

    Use connect_ro() unless you actually write. swing.db is the LIVE paper
    ledger and the 19:00 scheduled job writes it.
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA busy_timeout=30000")   # see paper_sleeves.connect (audit #4 E9)
    conn.execute(SCHEMA)
    return conn


def connect_ro(db_path=DB_PATH):
    """READ-ONLY handle on the same file (audit #3).

    "Open read-only / never run these concurrently" was an UNENFORCEABLE
    contract: it was written in CLAUDE.md and honoured by exactly one module
    (test_frozen, which rolled its own). Seven read-only consumers still called
    connect(), taking a write handle -- and a write handle also mutates schema
    via CREATE TABLE IF NOT EXISTS. A read-only handle makes the contract
    mechanical: a stray write raises instead of landing on the live ledger.
    """
    return sqlite3.connect("file:%s?mode=ro" % str(db_path).replace("\\", "/"),
                           uri=True)


def _flatten(df):
    """yfinance returns a 2-level column MultiIndex even for one ticker;
    drop the ticker level so columns are Open/High/Low/Close/Adj Close/Volume.
    """
    if df.columns.nlevels == 2:
        df = df.copy()
        df.columns = df.columns.droplevel(1)
    return df


def _trailing_nan(df):
    """True if the frame's LAST row carries a NaN in any of O/H/L/C.

    Record GH (2026-09-08): Yahoo published the 2026-09-08 QQQ bar clean at
    17:35 CT and had REVISED it into a NaN-carrying row by 19:00 CT. fetch()'s
    filter then deletes that row, the series ends a session short, and the live
    loop's feed-clock guard refuses -- while the log blames the vendor for a bar
    the vendor actually published. A retry is the only thing that distinguishes
    'not published yet' from 'published then revised', because both look
    identical once the row is gone.

    NaN is the only float not equal to itself -- the same test the row filter
    uses below, and the one `scripts/probe_feed_publication.py:60-66` performs
    out-of-library today. Empty frames are the caller's `df.empty` check, not
    this one's business.
    """
    if df is None or df.empty:
        return False
    last = _flatten(df).iloc[-1]
    return any(last.get(c) != last.get(c)
               for c in ("Open", "High", "Low", "Close"))


# shortcut: retry-on-empty assumes an empty result is a yfinance blip, which
# holds for THIS project (every ticker requested here has history in the range).
# If a caller ever legitimately requests an empty range, it pays 22s of backoff.
FETCH_RETRY_BACKOFF_S = (2.0, 5.0, 15.0)


def fetch(ticker, start, end=None):
    """Fetch daily OHLCV for one ticker; return list of bar tuples.

    Rows with any NaN in O/H/L/C are dropped (yfinance occasionally emits a
    trailing partial/blank row). Prices are split-adjusted, dividend-UNADJ.

    RETRIES on exception OR empty result (audit finding #8, 2026-07-28).
    yfinance is flaky, and a bare blip here was not a harmless no-op: the daily
    loop turns a missing price into a SKIPPED FILL LEG, and realize_pending
    clears the pending target afterwards regardless -- so a single failed fetch
    silently dropped that leg and left the sleeve sitting in cash with no
    record. For m10_1_nagel's K=4 basket one bad fetch = 25% silently
    uninvested. Retrying here removes the common cause; the daily loop also now
    reports any leg it still could not fill."""
    last_err = None
    for i in range(len(FETCH_RETRY_BACKOFF_S) + 1):
        try:
            df = yf.download(ticker, start=start, end=end, auto_adjust=False,
                             progress=False, actions=False)
            if not df.empty and not _trailing_nan(df):
                break
            last_err = "empty result" if df.empty else "trailing NaN in last row"
        except Exception as e:                      # noqa: BLE001 - yfinance raises broadly
            last_err = repr(e)
            df = None
        if i < len(FETCH_RETRY_BACKOFF_S):
            time.sleep(FETCH_RETRY_BACKOFF_S[i])
    if df is None or df.empty:
        print(f"  prices.fetch({ticker}): no data after "
              f"{len(FETCH_RETRY_BACKOFF_S) + 1} attempts ({last_err})", flush=True)
        return []
    if _trailing_nan(df):
        # Record GH option (c): say what actually happened. The row is still
        # dropped by the filter below, so the series ends a session short and
        # the feed clock will refuse -- but "the vendor never published it" and
        # "the vendor published it and then revised it into a NaN" are opposite
        # problems with opposite fixes, and the log has to tell them apart.
        print(f"  prices.fetch({ticker}): last row STILL carries a NaN after "
              f"{len(FETCH_RETRY_BACKOFF_S) + 1} attempts. The vendor DID publish "
              f"this bar and then revised it; our O/H/L/C filter drops it, so the "
              f"series ends short. This is our filter, not a vendor no-show "
              f"(record GH).", flush=True)
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
