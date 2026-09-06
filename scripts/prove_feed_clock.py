r"""Proof that the M3 loop REFUSES when the price feed lags the real trading
calendar (PRD M13.1, record FP). Pure in-memory: no DB, no network, no orders,
no clock dependence -- every case pins an explicit `now`. Run:

    .venv\Scripts\python.exe scripts\prove_feed_clock.py

It calls swing_bot.trading_calendar.check_feed_clock directly, which is the SAME
function scripts/daily_swing_paper.py calls -- not a copy of the branch, so this
cannot drift away from the shipped guard.

Case 1 replays the real incident: on Fri 2026-09-04 at 19:00 CT the feed's newest
bar was 2026-09-03 (var/daily_swing_paper.log: "latest session: 2026-09-03"), the
loop processed it as today, and no sleeve got a 2026-09-04 paper_nav row.

DATA CONVENTION: no price data is read; no adjustment convention applies.
"""
import datetime as dt
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from swing_bot import trading_calendar as tc  # noqa: E402

CT = ZoneInfo("America/Chicago")


def at(y, m, d, hh=19, mm=0):
    """The scheduled run's wall clock: 19:00 America/Chicago unless overridden."""
    return dt.datetime(y, m, d, hh, mm, tzinfo=CT)


ok = True
n = 0


def check(label, got, want):
    global ok, n
    n += 1
    hit = (got == want) if want is not None else (got is None)
    ok = ok and hit
    print("  %-4s %-58s -> %s" % ("PASS" if hit else "FAIL", label,
                                  "accept" if got is None else "REFUSE"))
    if not hit:
        print("       got:  %r" % (got,))
        print("       want: %r" % (want,))


print("A. last_completed_session (the independent clock)")
CLOCK = [
    ("Fri 2026-09-04 19:00 CT (the incident run)", at(2026, 9, 4), "2026-09-04"),
    ("Sat 2026-09-05 19:00 CT (weekend -> Friday)", at(2026, 9, 5), "2026-09-04"),
    ("Mon 2026-09-07 19:00 CT (Labor Day -> Friday)", at(2026, 9, 7), "2026-09-04"),
    ("Tue 2026-09-08 19:00 CT (next scheduled run)", at(2026, 9, 8), "2026-09-08"),
    ("Tue 2026-09-08 11:00 CT (before the close)", at(2026, 9, 8, 11), "2026-09-04"),
    ("Fri 2026-04-03 19:00 CT (Good Friday -> Thursday)", at(2026, 4, 3), "2026-04-02"),
    ("Fri 2026-07-03 19:00 CT (Jul 4 observed Friday)", at(2026, 7, 3), "2026-07-02"),
    ("Thu 2026-11-26 19:00 CT (Thanksgiving -> Wednesday)", at(2026, 11, 26), "2026-11-25"),
]
for label, now, want in CLOCK:
    got = tc.last_completed_session(now).isoformat()
    n += 1
    hit = got == want
    ok = ok and hit
    print("  %-4s %-58s -> %s" % ("PASS" if hit else "FAIL", label, got))
    if not hit:
        print("       want: %s" % want)

print("\nB. check_feed_clock (the guard the loop calls)")
# 1. THE INCIDENT: feed one session behind on a trading evening -> must refuse.
r = tc.check_feed_clock("2026-09-03", now=at(2026, 9, 4))
check("feed 2026-09-03 on Fri 2026-09-04 19:00 CT", r is None and "accept" or "REFUSE", "REFUSE")
assert r is not None and "BEHIND" in r, r
print("       reason: %s" % r.split(".")[0])

# 2. Same evening, feed current -> must accept.
check("feed 2026-09-04 on Fri 2026-09-04 19:00 CT",
      tc.check_feed_clock("2026-09-04", now=at(2026, 9, 4)), None)

# 3. Monday 09-07 is Labor Day: 09-04 is the latest CLOSED session, so a run
#    that evening legitimately processes 09-04. This is the path that would
#    close the 2026-09-04 NAV hole WITHOUT any backfill.
check("feed 2026-09-04 on Mon 2026-09-07 19:00 CT (holiday run)",
      tc.check_feed_clock("2026-09-04", now=at(2026, 9, 7)), None)

# 4. Tuesday 09-08 with the lag still present -> refuse (the deadline run).
r4 = tc.check_feed_clock("2026-09-04", now=at(2026, 9, 8))
check("feed 2026-09-04 on Tue 2026-09-08 19:00 CT (lag persists)",
      r4 is None and "accept" or "REFUSE", "REFUSE")

# 5. Weekend manual fire processing Friday -> accept (log shows three real ones).
check("feed 2026-09-04 on Sat 2026-09-05 19:00 CT (manual fire)",
      tc.check_feed_clock("2026-09-04", now=at(2026, 9, 5)), None)

# 6. Feed AHEAD (partial/live row, or this calendar wrong) -> refuse.
r6 = tc.check_feed_clock("2026-09-08", now=at(2026, 9, 7))
check("feed 2026-09-08 on Mon 2026-09-07 19:00 CT (ahead)",
      r6 is None and "accept" or "REFUSE", "REFUSE")
assert r6 is not None and "AHEAD" in r6, r6

# 7. A multi-session stall must keep refusing, not heal itself.
check("feed 2026-09-01 on Thu 2026-09-10 19:00 CT (4 sessions behind)",
      tc.check_feed_clock("2026-09-01", now=at(2026, 9, 10)) is None and "accept" or "REFUSE",
      "REFUSE")

print("\nC. Derived 2026 NYSE closures (eyeball these -- they are computed, not recalled)")
for d in sorted(tc.holidays(2026)):
    print("     %s  %s" % (d.isoformat(), d.strftime("%a")))

print("")
print("D. Fixed-date observance rules (the shifts a recalled table gets wrong)")
OBS = [
    ("Jul 4 2020 = Sat -> Fri Jul 3 closed", 2020, (2020, 7, 3), True),
    ("Jul 4 2021 = Sun -> Mon Jul 5 closed", 2021, (2021, 7, 5), True),
    # The NYSE exception: Jan 1 on a Saturday does NOT close the prior Friday,
    # so Dec 31 2021 was a full trading day.
    ("Jan 1 2022 = Sat -> Dec 31 2021 still TRADES", 2021, (2021, 12, 31), False),
]
for label, year, ymd, want_closed in OBS:
    d = dt.date(*ymd)
    closed = d in tc.holidays(year)
    n += 1
    hit = closed == want_closed
    ok = ok and hit
    print("  %-4s %-58s -> %s" % ("PASS" if hit else "FAIL", label,
                                  "closed" if closed else "trades"))
print("")
print("\n%s: %d checks" % ("PROVEN" if ok else "FAILED", n))
sys.exit(0 if ok else 1)
