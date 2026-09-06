r"""M13.2 instrument: WHEN does yfinance publish the current session's QQQ bar?

    .venv\Scripts\python.exe scripts\probe_feed_publication.py            # one sample
    .venv\Scripts\python.exe scripts\probe_feed_publication.py --watch    # until it lands

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False) --
identical to swing_bot/prices.py, because the point is to reproduce what the M3
loop sees, not a cleaner version of it.

WHY (record FP, FQ). From 2026-09-02 the 19:00 CT scheduled run stopped finding
the same day's bar and silently processed the previous session, three runs in a
row after a 17-run same-day streak. PRD M13.2 asks which of two things happened:
yfinance publishing late, or prices.fetch serving a cached series. **The cached
hypothesis is already dead** -- prices.fetch (swing_bot/prices.py:92-136) is a
bare yf.download per call with no store and no memo, and site-packages shows
yfinance 1.5.1 installed 2026-07-08 and untouched since, matching the lockfile.
So nothing changed on this machine and the M3 path fetches live every run.

THE THIRD HYPOTHESIS this probe adds, which M13.2's binary does not have:
prices.fetch DROPS any row with NaN in O/H/L/C. If Yahoo starts emitting the
current day's row with a NaN in it, our own filter deletes the bar and the loop
sees yesterday -- indistinguishable, from the log alone, from "not published
yet". The fix would then be in this repo, not in the schedule. So every sample
records the RAW yfinance frame AND the post-filter result, and flags any
disagreement.

WRITES: appends one JSON line per sample to var/feed_publication_probe.jsonl
(var/ is gitignored). Touches NO database, submits NO orders, and never imports
daily_swing_paper.
"""
import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from swing_bot import prices, trading_calendar as tc  # noqa: E402

ET = ZoneInfo("America/New_York")
CT = ZoneInfo("America/Chicago")
TICKER = "QQQ"
OUT = Path(__file__).resolve().parent.parent / "var" / "feed_publication_probe.jsonl"
OHLC = ("Open", "High", "Low", "Close")


def raw_probe(start):
    """What yfinance ACTUALLY returned, before prices.fetch's NaN filter.

    Deliberately a separate yf.download rather than a peek inside fetch(): the
    two calls are what tell us whether the row exists upstream at all."""
    import yfinance as yf
    df = yf.download(TICKER, start=start, auto_adjust=False, progress=False,
                     actions=False)
    if df is None or df.empty:
        return {"rows": 0, "last": None, "last_has_nan": None, "tail": []}
    df = prices._flatten(df)
    tail = [ts.strftime("%Y-%m-%d") for ts in df.index[-3:]]
    lastrow = df.iloc[-1]
    # NaN is the only float that is not equal to itself -- same test fetch() uses.
    has_nan = any(lastrow.get(c) != lastrow.get(c) for c in OHLC)
    return {"rows": int(len(df)), "last": tail[-1], "last_has_nan": bool(has_nan),
            "tail": tail}


def verdicts(raw_last, filtered_last, expected):
    """The two things this probe exists to separate, as a pure function so
    --selftest can pin the branch that has never fired live."""
    return {
        "published": raw_last == expected,
        # Yahoo HAS the bar but prices.fetch's NaN filter deleted it: our bug,
        # not the vendor's, and invisible in daily_swing_paper.log.
        "dropped_by_our_filter": raw_last == expected and filtered_last != expected,
    }


def sample(start):
    now_ct = dt.datetime.now(CT)
    t0 = time.time()
    raw = raw_probe(start)
    t1 = time.time()
    bars = prices.fetch(TICKER, start=start)
    t2 = time.time()
    filtered_last = bars[-1][1] if bars else None
    expected = tc.last_completed_session(now_ct).isoformat()
    rec = {
        "wall_ct": now_ct.isoformat(timespec="seconds"),
        "wall_et": now_ct.astimezone(ET).isoformat(timespec="seconds"),
        "expected_session": expected,
        "raw_last": raw["last"],
        "raw_tail": raw["tail"],
        "raw_rows": raw["rows"],
        "raw_last_has_nan": raw["last_has_nan"],
        "filtered_last": filtered_last,
        "raw_secs": round(t1 - t0, 2),
        "fetch_secs": round(t2 - t1, 2),
    }
    rec.update(verdicts(raw["last"], filtered_last, expected))
    return rec


def line(rec):
    if rec["dropped_by_our_filter"]:
        verdict = "OUR FILTER DROPPED IT"
    elif rec["published"]:
        verdict = "PUBLISHED"
    else:
        verdict = "not yet"
    return ("%s CT (%s ET)  expected=%s  raw_last=%s  filtered_last=%s  "
            "nan=%s  -> %s"
            % (rec["wall_ct"][11:19], rec["wall_et"][11:19],
               rec["expected_session"], rec["raw_last"], rec["filtered_last"],
               rec["raw_last_has_nan"], verdict))


def selftest():
    """Offline proof of the three states, including the one no live run has
    produced yet. Cheap because verdicts() is pure."""
    CASES = [
        # raw_last,      filtered_last,  expected,       published, dropped
        ("2026-09-08", "2026-09-08", "2026-09-08", True,  False),  # normal
        ("2026-09-04", "2026-09-04", "2026-09-08", False, False),  # vendor late
        ("2026-09-08", "2026-09-04", "2026-09-08", True,  True),   # OUR filter
        (None,         None,         "2026-09-08", False, False),  # empty fetch
    ]
    ok = True
    for raw, filt, exp, want_pub, want_drop in CASES:
        v = verdicts(raw, filt, exp)
        hit = v["published"] == want_pub and v["dropped_by_our_filter"] == want_drop
        ok = ok and hit
        print("  %-4s raw=%-12s filtered=%-12s expected=%s -> published=%s dropped=%s"
              % ("PASS" if hit else "FAIL", raw, filt, exp,
                 v["published"], v["dropped_by_our_filter"]))
    print("SELFTEST: %s (%d cases)" % ("PASS" if ok else "FAIL", len(CASES)))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true",
                    help="keep sampling until the expected session's bar appears")
    ap.add_argument("--interval-min", type=float, default=15.0)
    ap.add_argument("--max-hours", type=float, default=6.0)
    ap.add_argument("--selftest", action="store_true",
                    help="pin the verdict branches offline; no network")
    ap.add_argument("--start", default="2026-08-01",
                    help="fetch window start; short by design, this is a timing probe")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    now_ct = dt.datetime.now(CT)
    if not tc.is_trading_day(now_ct.date()):
        print("!! %s is NOT a trading day, so the expected session is already "
              "old and published -- this run measures nothing about publication "
              "timing. Run it on a trading day, ideally from ~15:15 CT."
              % now_ct.date(), flush=True)

    OUT.parent.mkdir(exist_ok=True)
    deadline = time.time() + args.max_hours * 3600
    n = 0
    while True:
        rec = sample(args.start)
        n += 1
        print(line(rec), flush=True)
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        if not args.watch:
            break
        if rec["published"] or rec["dropped_by_our_filter"]:
            print("resolved after %d sample(s); log: %s" % (n, OUT), flush=True)
            break
        if time.time() >= deadline:
            print("!! gave up after %.1fh / %d samples WITHOUT the bar appearing. "
                  "That is itself the finding -- record it." % (args.max_hours, n),
                  flush=True)
            return 1
        time.sleep(args.interval_min * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
