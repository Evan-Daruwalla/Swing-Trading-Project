"""Independent US-equity trading calendar -- the M3 loop's clock, derived from
the WALL CLOCK and the exchange's published holiday rules, never from the price
feed (PRD M13.1; record FP).

DATA CONVENTION: this module reads NO price data, so the project's
split-adjusted / dividend-UNADJUSTED convention does not arise here -- it
compares DATES only. (The header is required anyway: test_frozen's
convention guard counts a file as price-touching when the string "yfinance"
appears anywhere in it, including in prose like the paragraph below.)

WHY THIS EXISTS. `scripts/daily_swing_paper.py` set `today = qdates[-1]`, i.e.
it let the yfinance series define which session it was processing. From
2026-09-02 the feed stopped publishing the current bar before the 19:00 CT
scheduled run, so three consecutive runs silently processed the PREVIOUS
session (log-verified: 09-02 -> 09-01, 09-03 -> 09-02, 09-04 -> 09-03) and
2026-09-04 got no paper_nav row in any sleeve. The per-sleeve missed-session
detector could not see it because its `today` was the same lagged value -- a
detector whose clock comes from the feed it is checking. This module is the
second, independent clock that makes the comparison possible.

WHY RULES, NOT A PINNED TABLE. A hardcoded holiday list goes stale silently and
would have to be re-recalled correctly each year (a fabrication risk this
project does not take). The NYSE's ten holidays are rule-derived here, so the
calendar is correct for any year without maintenance.

WHY NOT ALPACA'S CALENDAR API. It is authoritative, but the M3 loop's DB ledger
is deliberately independent of broker connectivity (daily_swing_paper docstring
step 3), and a TOTAL Alpaca credential outage is a real logged event for this
account (record FH). Sourcing the clock from Alpaca would convert a credential
outage into a refusal to mark NAV -- manufacturing exactly the holes this guard
exists to prevent.
# shortcut: rules cover only SCHEDULED closures. An ad-hoc closure (national
# day of mourning, weather) is not modelled; the guard then expects a session
# that never happened and REFUSES, which is the safe direction -- a false red
# that a human clears, never a silent wrong-date mark. Upgrade trigger: if an
# ad-hoc closure ever actually fires this, add a dated exception set here.
"""
import datetime as dt
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

# The guard only has to know "has the session finished". Half-days end 13:00 ET;
# using the REGULAR 16:00 close means a run between 13:00 and 16:00 on a half-day
# does not yet expect that day's bar -- conservative in the no-false-refusal
# direction. The scheduled run is 19:00 CT = 20:00 ET, well past either.
REGULAR_CLOSE_ET = dt.time(16, 0)

# How far back last_completed_session() will walk before giving up. The longest
# real US market gap is a 4-day Thanksgiving/Christmas weekend; 10 is slack.
_MAX_WALKBACK_DAYS = 10


def _easter(year):
    """Gregorian Easter Sunday (anonymous algorithm). Good Friday = Easter - 2."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return dt.date(year, month, day + 1)


def _nth_weekday(year, month, weekday, n):
    """n-th `weekday` (Mon=0) of a month; n=-1 means the LAST one."""
    if n == -1:
        d = dt.date(year, month, 1)
        d = (d.replace(month=month + 1) if month < 12
             else dt.date(year + 1, 1, 1)) - dt.timedelta(days=1)
        return d - dt.timedelta(days=(d.weekday() - weekday) % 7)
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def _observed(d):
    """NYSE observance for a FIXED-DATE holiday: Saturday -> preceding Friday,
    Sunday -> following Monday. Returns None only for the New Year's case
    handled by the caller."""
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def holidays(year):
    """The NYSE's ten scheduled full closures for `year`, as observed."""
    out = set()
    # New Year's Day is the one exception to _observed(): when Jan 1 falls on a
    # SATURDAY the NYSE does NOT close the preceding Friday (Dec 31 trades).
    ny = dt.date(year, 1, 1)
    if ny.weekday() != 5:
        out.add(_observed(ny))
    out.add(_nth_weekday(year, 1, 0, 3))            # MLK Day, 3rd Monday Jan
    out.add(_nth_weekday(year, 2, 0, 3))            # Washington's Birthday
    out.add(_easter(year) - dt.timedelta(days=2))   # Good Friday
    out.add(_nth_weekday(year, 5, 0, -1))           # Memorial Day, last Monday
    out.add(_observed(dt.date(year, 6, 19)))        # Juneteenth (NYSE since 2022)
    out.add(_observed(dt.date(year, 7, 4)))         # Independence Day
    out.add(_nth_weekday(year, 9, 0, 1))            # Labor Day, 1st Monday
    out.add(_nth_weekday(year, 11, 3, 4))           # Thanksgiving, 4th Thursday
    out.add(_observed(dt.date(year, 12, 25)))       # Christmas
    return out


def is_trading_day(d):
    """True if `d` (a datetime.date) is a scheduled US equity session."""
    return d.weekday() < 5 and d not in holidays(d.year)


def last_completed_session(now=None):
    """The most recent US equity session that has ALREADY CLOSED as of `now`.

    `now` is a timezone-aware datetime (converted to ET); default = real clock.
    This is the value `today` in the daily loop is supposed to equal."""
    now_et = (dt.datetime.now(ET) if now is None else now.astimezone(ET))
    d = now_et.date()
    if is_trading_day(d) and now_et.time() >= REGULAR_CLOSE_ET:
        return d
    for _ in range(_MAX_WALKBACK_DAYS):
        d -= dt.timedelta(days=1)
        if is_trading_day(d):
            return d
    raise RuntimeError("no trading day within %d days before %s"
                       % (_MAX_WALKBACK_DAYS, now_et.date()))


def check_feed_clock(feed_last_session, now=None):
    """Compare the feed's newest session against the real calendar.

    `feed_last_session` is the loop's `qdates[-1]` (a 'YYYY-MM-DD' string).
    Returns None when the feed is current, else a one-line refusal REASON --
    the caller appends it to RUN_FAILURES and refuses to decide or mark, the
    same shape as mark_nav's refusal on a missing close."""
    expected = last_completed_session(now).isoformat()
    if feed_last_session == expected:
        return None
    if feed_last_session < expected:
        return ("price feed is BEHIND the calendar: newest bar is %s, but %s "
                "has already closed. Processing %s now would mark NAV and "
                "realize fills against a session that was already processed, "
                "and the missed-session detector cannot see it (its clock is "
                "this same value)." % (feed_last_session, expected, feed_last_session))
    return ("price feed is AHEAD of the calendar: newest bar is %s, but the "
            "latest CLOSED session is %s. Either the bar is a partial/live row "
            "or this calendar is wrong about %s."
            % (feed_last_session, expected, feed_last_session))
