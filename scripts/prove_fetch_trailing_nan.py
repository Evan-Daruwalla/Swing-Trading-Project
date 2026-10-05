r"""Proof: prices.fetch() RETRIES when the vendor's last row carries a NaN.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False) --
identical to swing_bot/prices.py, because these fixtures stand in for what
yfinance hands that function, not for a cleaner version of it.

WHY THIS EXISTS (records GH, GJ.1). On 2026-09-08 Yahoo published the QQQ bar
clean at 17:35 CT and had REVISED it into a NaN-carrying row by 19:00 CT.
`fetch()`'s ladder was `if not df.empty: break`, so a non-empty frame satisfied
it on the first attempt and it never re-fetched; the O/H/L/C filter then deleted
that row, the series came back a session short, and the live loop's feed-clock
guard refused -- while the log blamed the vendor for a bar the vendor had
actually published. The retry is what separates "not published yet" from
"published then revised", because once the row is filtered the two are
indistinguishable.

This calls the SAME `prices.fetch` the live loop calls -- not a copy of the
branch -- so it cannot drift from the shipped code.

WRITES NOTHING. No network: `prices.yf.download` is monkeypatched to serve
fixture frames and `prices.time.sleep` is neutered so the 2/5/15s backoff costs
no wall clock. Both are restored in a `finally`. swing.db is never opened, no
order is placed, no rebalance runs.

FIRST-OF-ITS-KIND NOTE: every other `scripts/prove_*.py` builds fixtures as
plain 8-element bar lists (`prove_cache_guard.py:53-54`). This one has to build
a real pandas frame, because the defect lives UPSTREAM of the bar list -- in the
frame `fetch()` accepts or rejects.

    .venv\Scripts\python.exe scripts\prove_fetch_trailing_nan.py

Exits non-zero on any failure.
"""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd  # noqa: E402

from swing_bot import prices  # noqa: E402

TICK = "QQQ"
FIELDS = ("Open", "High", "Low", "Close", "Adj Close", "Volume")
failures = []


def frame(dates, nan_last=False):
    """A yfinance-shaped frame: DatetimeIndex, 2-level (field, ticker) columns.

    nan_last puts a NaN in the LAST row's O/H/L/C only -- Adj Close and Volume
    stay populated, so the trailing-NaN check is what fires, not a blank row.
    """
    idx = pd.DatetimeIndex([pd.Timestamp(d) for d in dates])
    cols = pd.MultiIndex.from_tuples([(f, TICK) for f in FIELDS])
    df = pd.DataFrame(
        [[100.0 + i] * len(FIELDS) for i in range(len(dates))],
        index=idx, columns=cols)
    if nan_last:
        for f in ("Open", "High", "Low", "Close"):
            df.iloc[-1, df.columns.get_loc((f, TICK))] = float("nan")
    return df


def serve(*frames):
    """Monkeypatch download to hand back `frames` in order, then repeat the
    last one forever. Returns a mutable call counter."""
    calls = []

    def fake(ticker, start=None, end=None, **kw):
        i = min(len(calls), len(frames) - 1)
        calls.append(ticker)
        return frames[i]

    prices.yf.download = fake
    return calls


def check(name, fn):
    try:
        fn()
        print(f"  PASS  {name}")
    except AssertionError as exc:
        failures.append(name)
        print(f"  FAIL  {name}: {exc}")


DATES = ["2026-09-04", "2026-09-08"]


def case_retries_on_trailing_nan():
    """THE DEFECT. NaN last row on attempt 1, clean on attempt 2 -> refetch."""
    calls = serve(frame(DATES, nan_last=True), frame(DATES))
    bars = prices.fetch(TICK, start="2026-09-01")
    assert len(calls) == 2, f"expected 2 download calls (1 retry), got {len(calls)}"
    assert len(bars) == 2, f"expected the FULL 2-bar series, got {len(bars)}"
    assert bars[-1][1] == "2026-09-08", f"last bar should be 2026-09-08, got {bars[-1][1]}"


def case_clean_frame_does_not_retry():
    """The mandatory negative: a guard that always fires is as useless as one
    that never does (prove_cache_guard.py:120-127)."""
    calls = serve(frame(DATES))
    bars = prices.fetch(TICK, start="2026-09-01")
    assert len(calls) == 1, f"clean frame must NOT retry; got {len(calls)} calls"
    assert len(bars) == 2, f"expected 2 bars, got {len(bars)}"


def case_exhaustion_says_it_was_our_filter():
    """NaN on every attempt -> 4 calls, the row is dropped (short series), and
    the log says the vendor DID publish. Record GH option (c)."""
    calls = serve(frame(DATES, nan_last=True))
    buf = io.StringIO()
    with redirect_stdout(buf):
        bars = prices.fetch(TICK, start="2026-09-01")
    out = buf.getvalue()
    assert len(calls) == 4, f"expected 4 attempts, got {len(calls)}"
    assert len(bars) == 1, f"NaN row must be dropped -> 1 bar, got {len(bars)}"
    assert bars[-1][1] == "2026-09-04", f"series should end short at 2026-09-04, got {bars[-1][1]}"
    assert "STILL carries a NaN" in out, f"missing the distinct message:\n{out}"
    assert "not a vendor no-show" in out, f"message must not blame the vendor:\n{out}"


def case_empty_still_retries():
    """Regression: the pre-existing retry-on-empty behaviour is untouched."""
    calls = serve(frame([]), frame(DATES))
    bars = prices.fetch(TICK, start="2026-09-01")
    assert len(calls) == 2, f"empty frame must still retry; got {len(calls)}"
    assert len(bars) == 2, f"expected 2 bars after the retry, got {len(bars)}"


def case_helper_ignores_empty():
    """_trailing_nan must not claim an empty frame is NaN-tailed -- that is the
    caller's df.empty branch, and conflating them would double-count."""
    assert prices._trailing_nan(frame([])) is False, "empty frame -> False"
    assert prices._trailing_nan(None) is False, "None -> False"
    assert prices._trailing_nan(frame(DATES)) is False, "clean frame -> False"
    assert prices._trailing_nan(frame(DATES, nan_last=True)) is True, "NaN tail -> True"


def main():
    real_download, real_sleep = prices.yf.download, prices.time.sleep
    prices.time.sleep = lambda s: None
    try:
        print("prove_fetch_trailing_nan -- prices.fetch retries a revised (NaN) last row\n")
        for name, fn in (
            ("retries on a trailing-NaN last row      ", case_retries_on_trailing_nan),
            ("clean frame does NOT retry (negative)   ", case_clean_frame_does_not_retry),
            ("exhaustion blames our filter, not vendor", case_exhaustion_says_it_was_our_filter),
            ("retry-on-empty still works (regression) ", case_empty_still_retries),
            ("_trailing_nan on empty/None/clean/NaN   ", case_helper_ignores_empty),
        ):
            check(name, fn)
    finally:
        prices.yf.download, prices.time.sleep = real_download, real_sleep

    if failures:
        print(f"\nFETCH TRAILING-NAN PROOF: {len(failures)} FAILED -> {failures}")
        return 1
    print("\nFETCH TRAILING-NAN PROOF: 5/5 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
