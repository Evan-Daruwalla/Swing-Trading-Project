r"""Proof: a session missing from the MIDDLE of a price series is now caught.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False) --
the fixtures stand in for a prices.fetch() bar list, whose layout is
(ticker, date, o, h, l, c, adj, vol).

WHY THIS EXISTS (record GJ.6). coverage_gate.scan_ohlc walks rows POSITIONALLY:
`prev_close` is just "the previous row in the list". A session missing from the
middle therefore produces a two-day return compared as if it were one day, and
every downstream `[-200:]` slice (swing_bot/paper_sleeves.py:341,
the live loop's sane_window) silently spans 201 sessions while calling
itself "the last 200". Nothing in the repo could detect this: trading_calendar
had is_trading_day (one date) and last_completed_session (tail only, capped at
10 days), but no range enumerator, so the EXPECTED session set could not be
built. sessions_between() is that enumerator; missing_sessions() does the diff.

This calls the SAME coverage_gate.scan_fetched_bars the live loop calls at
its DATA-SANITY GATE block -- not a copy of the rule -- so it cannot
drift from the shipped code.

WRITES NOTHING. Pure in-memory fixtures; no network, no DB, swing.db never
opened, no order placed, no rebalance run.

    .venv\Scripts\python.exe scripts\prove_session_gap.py

Exits non-zero on any failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from swing_bot import coverage_gate, trading_calendar  # noqa: E402

import datetime as dt  # noqa: E402

TICK = "QQQ"
failures = []


def bars(dates):
    """Valid OHLC so only the gap rule can fire: l <= o,c <= h and h != l
    (h == l would trip zero_range), closes flat so no extreme_ret."""
    return [(TICK, d, 100.0, 101.0, 99.0, 100.0, 100.0, 1_000_000) for d in dates]


def kinds(anoms):
    return sorted(a[2] for a in anoms)


def check(name, fn):
    try:
        fn()
        print(f"  PASS  {name}")
    except AssertionError as exc:
        failures.append(name)
        print(f"  FAIL  {name}: {exc}")


# 2026-09-01 Tue .. 2026-09-04 Fri, all four are sessions.
FULL_WEEK = ["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"]
# 2026-09-07 is Labor Day (first Monday of September 2026).
ACROSS_HOLIDAY = ["2026-09-04", "2026-09-08"]


def case_complete_series_is_clean():
    assert coverage_gate.scan_fetched_bars(TICK, bars(FULL_WEEK)) == [], \
        "a complete series must produce no anomalies"


def case_mid_series_hole_is_caught():
    """THE DEFECT. Drop 2026-09-03 (a Thursday) from the middle."""
    holed = [d for d in FULL_WEEK if d != "2026-09-03"]
    anoms = coverage_gate.scan_fetched_bars(TICK, bars(holed))
    assert kinds(anoms) == ["missing_session"], f"expected one missing_session, got {anoms}"
    assert anoms[0][1] == "2026-09-03", f"should name 2026-09-03, got {anoms[0][1]}"


def case_holiday_is_not_a_false_hole():
    """The mandatory negative: Labor Day 2026-09-07 sits inside this span and
    must NOT be reported. A guard that fires on every holiday is worse than
    none -- it trains people to ignore red."""
    anoms = coverage_gate.scan_fetched_bars(TICK, bars(ACROSS_HOLIDAY))
    assert anoms == [], f"Labor Day must not be reported as missing, got {anoms}"


def case_weekend_is_not_a_false_hole():
    weekend_span = ["2026-09-04", "2026-09-09"]   # Fri .. Wed, incl. Labor Day
    anoms = coverage_gate.missing_sessions(TICK, bars(weekend_span))
    assert [a[1] for a in anoms] == ["2026-09-08"], \
        f"only the real 09-08 session should be missing, got {anoms}"


def case_short_series_has_no_span():
    """Fewer than 2 bars defines no interval, so there is nothing to diff --
    and inventing a span from one date would make every first-run series red."""
    assert coverage_gate.missing_sessions(TICK, bars(["2026-09-04"])) == []
    assert coverage_gate.missing_sessions(TICK, []) == []


def case_sessions_between_itself():
    d = dt.date.fromisoformat
    got = trading_calendar.sessions_between(d("2026-09-04"), d("2026-09-08"))
    assert [x.isoformat() for x in got] == ["2026-09-04", "2026-09-08"], \
        f"Sat/Sun/LaborDay must all be excluded, got {got}"
    assert trading_calendar.sessions_between(d("2026-09-08"), d("2026-09-04")) == [], \
        "end before start must be empty, not an error"


def case_ad_hoc_closures_are_not_holes():
    """The ten unscheduled closures are the enumerator's ONLY false positives
    against real data -- derived 2026-09-09 by diffing QQQ's whole history
    (6,918 bars, 1999-03-10..2026-09-09). Pinned here so the set cannot silently
    shrink: Hurricane Sandy and 9/11 are weekdays and not holidays, so without
    AD_HOC_CLOSURES both would be reported as missing sessions."""
    d = dt.date.fromisoformat
    for day in ("2012-10-29", "2001-09-11", "2025-01-09"):
        assert not trading_calendar.is_trading_day(d(day)), \
            f"{day} was an ad-hoc closure, not a session"
    assert len(trading_calendar.AD_HOC_CLOSURES) == 10, \
        f"expected 10 derived closures, got {len(trading_calendar.AD_HOC_CLOSURES)}"
    # Sandy spanned Mon+Tue; the Wednesday after it reopened must still count.
    assert trading_calendar.is_trading_day(d("2012-10-31")), \
        "2012-10-31 reopened after Sandy and must remain a session"


def case_juneteenth_only_from_2022():
    """The REVERSE false positive, found by the GL landing-check: holidays() added
    Juneteenth for every year, so 23 real QQQ sessions on June dates 1999-2021
    were called holidays and a hole on one was invisible. NYSE first closed for
    it on 2022-06-20 (Mon, observed for Sun 06-19)."""
    d = dt.date.fromisoformat
    for day in ("2020-06-19", "2021-06-18"):  # a Friday; 2021's Sat-observed Friday
        assert trading_calendar.is_trading_day(d(day)), \
            f"{day} traded -- Juneteenth was not an NYSE holiday before 2022"
    for day in ("2022-06-20", "2026-06-19"):
        assert not trading_calendar.is_trading_day(d(day)), \
            f"{day} is an observed Juneteenth closure"


def main():
    print("prove_session_gap -- a hole in the MIDDLE of a series is now caught\n")
    for name, fn in (
        ("complete series is clean               ", case_complete_series_is_clean),
        ("mid-series hole IS caught (the defect) ", case_mid_series_hole_is_caught),
        ("holiday is NOT a false hole (negative) ", case_holiday_is_not_a_false_hole),
        ("weekend is NOT a false hole            ", case_weekend_is_not_a_false_hole),
        ("series shorter than 2 bars has no span ", case_short_series_has_no_span),
        ("sessions_between excludes wknd+holiday ", case_sessions_between_itself),
        ("ad-hoc closures are not false holes    ", case_ad_hoc_closures_are_not_holes),
        ("Juneteenth is a holiday only from 2022 ", case_juneteenth_only_from_2022),
    ):
        check(name, fn)

    if failures:
        print(f"\nSESSION GAP PROOF: {len(failures)} FAILED -> {failures}")
        return 1
    print("\nSESSION GAP PROOF: 8/8 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
