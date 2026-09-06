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
{prices, universe}.

WIRED 2026-09-06 (audit FX HIGH #3), after 53 days with ZERO importers — the
gap was flagged on 2026-07-15, again on 2026-08-06 (audit E14), and again by
FX before it was closed. `scripts/daily_swing_paper.py` now calls
scan_fetched_bars() on the QQQ series it actually decides on, BEFORE any
decide_* call, and REFUSES the run on any anomaly. So MAX_ABS_DAILY_RET — the
mis-applied-split tell — can finally fire in production.

WHAT IS STILL NOT COVERED, stated so this does not read as blanket protection:
  * Only QQQ. It is the only ticker the live sleeves have ever held
    (`SELECT DISTINCT ticker FROM paper_transactions` → ['QQQ']) and the only
    one fetched unconditionally. The 39-name UNIV pulled for an M10-1 weekly
    STRESS decision is NOT scanned; that path is conditional and has never
    fired live (it needs VIX>20).
  * latest_common_date() and coverage() still read the `bars` TABLE, frozen at
    2026-07-08. They remain UNCALLED by the live loop and would report a stale
    date if they ever were — do not wire those two without fixing that first.
    Only the scan_* functions are on the live path.
"""
from swing_bot import prices, universe

MAX_ABS_DAILY_RET = 0.35  # 35% close-to-close; investigate above this.
                          # REACHABLE in production since 2026-09-06: the live
                          # loop scans QQQ through scan_fetched_bars(). A real
                          # QQQ move of this size does not happen; a mis-applied
                          # split does.


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


def scan_ohlc(ticker, rows, max_abs_ret=MAX_ABS_DAILY_RET):
    """The anomaly rules themselves, over `rows` of (date, o, h, l, c).

    Split out of sanity_scan on 2026-09-06 (audit FX HIGH #3) so ONE rule set
    has TWO callers: the DB scan below, and the LIVE loop, which decides on an
    in-memory yfinance series and never writes the `bars` table. Duplicating
    the rules for the live path would have been the F2 defect this project
    keeps naming -- the live code and the checked code diverging."""
    anomalies = []
    prev_close = None
    for d, o, h, l, c in rows:
        if not (l <= o <= h and l <= c <= h and l <= h):
            anomalies.append((ticker, d, "ohlc_order", f"O{o} H{h} L{l} C{c}"))
        if h == l:
            anomalies.append((ticker, d, "zero_range", f"H==L=={h}"))
        if prev_close:
            ret = c / prev_close - 1
            if abs(ret) > max_abs_ret:
                anomalies.append((ticker, d, "extreme_ret",
                                  f"{ret:+.1%} vs prev {prev_close}"))
        prev_close = c
    return anomalies


def scan_fetched_bars(ticker, bars, max_abs_ret=MAX_ABS_DAILY_RET):
    """scan_ohlc for a prices.fetch() bar list, whose layout is
    (ticker, date, o, h, l, c, adj, vol). This is the LIVE loop's entry point."""
    return scan_ohlc(ticker, [(b[1], b[2], b[3], b[4], b[5]) for b in bars],
                     max_abs_ret=max_abs_ret)


def sanity_scan(conn, entries=None, max_abs_ret=MAX_ABS_DAILY_RET):
    """Return a list of (ticker, date, kind, detail) anomalies from the DB."""
    entries = entries or universe.UNIVERSE
    anomalies = []
    for e in entries:
        rows = conn.execute(
            "SELECT date, open, high, low, close FROM bars "
            "WHERE ticker=? ORDER BY date", (e.ticker,)).fetchall()
        anomalies += scan_ohlc(e.ticker, rows, max_abs_ret=max_abs_ret)
    return anomalies


def main():
    # READ-ONLY (audit #3): this only reads swing.db, and the 19:00
    # scheduled job writes it. connect() would take a write handle and
    # run CREATE TABLE IF NOT EXISTS against the live paper ledger.
    conn = prices.connect_ro()
    as_of = latest_common_date(conn)
    # Empty bars table -> as_of None -> `e.data_start <= None` TypeError in
    # coverage() (audit #4 E8). A clean "no data" beats a traceback.
    if as_of is None:
        print("coverage: bars table is EMPTY -- no as-of date exists. "
              "Run scripts/backfill_universe.py first.")
        return 1
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
