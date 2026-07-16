"""Data coverage + quality gate for swing_bot.

The daily loop must NOT emit signals on incomplete or corrupted data. Two
independent checks:

1. COVERAGE — on a given as-of date, every universe ticker that is already
   listed (data_start <= as_of) must have a bar. A ticker not yet listed as
   of that date is NOT counted missing (handles XLC pre-2018, XLRE pre-2015).
   This is the "gate on coverage count, not on 'ran today'" lesson carried
   over from the Trading project.

2. SANITY — scan bars for corruption tells: OHLC ordering violations, zero
   -range bars (IBS undefined), and extreme day-over-day moves (the
   >~100% single-day tell for a mis-applied split; ETFs in this universe
   have no leveraged products, so any |ret| above MAX_ABS_DAILY_RET is
   almost certainly bad data, not a real move).

Prices are split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): the M0.4 data-quality gate. Imports swing_bot.
{prices, universe}. CAVEAT (2026-07-15): NO module currently imports it — it
was built for M0.4 but is NOT yet wired into the live loop (daily_swing_paper
does its own fetch without this gate). If you add a pre-signal data check to
the daily loop, call it from here.
"""
import sqlite3

from swing_bot import prices, universe

MAX_ABS_DAILY_RET = 0.35  # 35% close-to-close; investigate above this


def coverage(conn, as_of, entries=None):
    """Return (ok, missing) for as_of (ISO 'YYYY-MM-DD').

    missing = tickers listed as of `as_of` (data_start <= as_of) that lack a
    bar on that date. ok = not missing.
    """
    entries = entries or universe.UNIVERSE
    have = {r[0] for r in conn.execute(
        "SELECT ticker FROM bars WHERE date=?", (as_of,))}
    expected = [e.ticker for e in entries if e.data_start <= as_of]
    missing = [t for t in expected if t not in have]
    return (len(missing) == 0, missing)


def latest_common_date(conn, entries=None):
    """Most recent date for which every currently-listed ticker has a bar.
    Used as the live loop's as-of date."""
    entries = entries or universe.UNIVERSE
    # newest date any ticker reports; walk back until coverage is complete
    dates = [r[0] for r in conn.execute(
        "SELECT DISTINCT date FROM bars ORDER BY date DESC LIMIT 10")]
    for d in dates:
        ok, _ = coverage(conn, d, entries)
        if ok:
            return d
    return dates[0] if dates else None


def sanity_scan(conn, entries=None, max_abs_ret=MAX_ABS_DAILY_RET):
    """Return a list of (ticker, date, kind, detail) anomalies."""
    entries = entries or universe.UNIVERSE
    anomalies = []
    for e in entries:
        rows = conn.execute(
            "SELECT date, open, high, low, close FROM bars "
            "WHERE ticker=? ORDER BY date", (e.ticker,)).fetchall()
        prev_close = None
        for d, o, h, l, c in rows:
            if not (l <= o <= h and l <= c <= h and l <= h):
                anomalies.append((e.ticker, d, "ohlc_order",
                                  f"O{o} H{h} L{l} C{c}"))
            if h == l:
                anomalies.append((e.ticker, d, "zero_range",
                                  f"H==L=={h}"))
            if prev_close:
                ret = c / prev_close - 1
                if abs(ret) > max_abs_ret:
                    anomalies.append((e.ticker, d, "extreme_ret",
                                      f"{ret:+.1%} vs prev {prev_close}"))
            prev_close = c
    return anomalies


def main():
    conn = prices.connect()
    as_of = latest_common_date(conn)
    ok, missing = coverage(conn, as_of)
    print(f"coverage as-of {as_of}: {'OK' if ok else 'FAIL'}"
          f"{'' if ok else ' missing=' + ','.join(missing)}")
    anomalies = sanity_scan(conn)
    print(f"sanity scan: {len(anomalies)} anomalies")
    for a in anomalies[:20]:
        print("  ", *a)
    # Gate semantics: nonzero exit if coverage fails.
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
