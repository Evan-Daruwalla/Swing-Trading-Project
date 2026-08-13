"""Prove the .e8e9_cache freshness guard FIRES at every site that can swallow it.

ADJUSTMENT CONVENTION: this script fabricates bar rows and makes no real price
call, but it exercises the shared cache_fetch path, whose data is SPLIT-ADJUSTED
and DIVIDEND-UNADJUSTED (`auto_adjust=False`) like every price series here.

WHY THIS EXISTS. Audit #4 F1 made `_note_vintage` RAISE on a stale or
mixed-vintage cache instead of printing (2026-08-12, record EM). The isolated
function was proven to fire on 5/5 triggers -- and the fix was still inert at
three of its reachable sites, because the raise was caught by broad handlers:
`cache_fetch`'s OWN retry loop reported it as a network failure and refetched
4x, and run_m12_factorial / run_v1_harness_check dropped the ticker and carried
on, turning "refuse to run" into "run on a silently emptied universe"
(record EO, 2026-08-13). That is the fifth consecutive audit finding of the same
class: a guard that cannot fire. Feeding a guard its trigger proves the GUARD
works; it does not prove anyone lets the failure through. This script proves the
callers do.

WRITES NOTHING. E8E9_CACHE is redirected to a temp dir before importing
run_e8_squeeze, and prices.fetch is monkeypatched -- no network call, no touch
of the real .e8e9_cache, swing.db or var/.

Run:  .venv\\Scripts\\python.exe scripts\\prove_cache_guard.py
Exits non-zero on any failure.
"""
import datetime
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRATCH = Path(tempfile.mkdtemp(prefix="cacheguard_"))
os.environ["E8E9_CACHE"] = str(SCRATCH)
os.environ.pop("SWING_ALLOW_STALE_CACHE", None)
os.environ.pop("SWING_MAX_CACHE_STALE_DAYS", None)
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

import run_e8_squeeze as e8        # noqa: E402  (needs the env + path setup above)

assert e8.CACHE == SCRATCH, f"cache not redirected -- refusing to run: {e8.CACHE}"

TODAY = datetime.date.today()
STALE_DAY = (TODAY - datetime.timedelta(days=40)).isoformat()
FRESH_DAY = TODAY.isoformat()

failures = []


def bars_for(tic, day):
    return [[tic, day, 1.0, 1.0, 1.0, 1.0, 1.0, 100]]


def reset():
    e8._VINTAGES.clear()
    e8._VINTAGE_REPORTED.clear()
    e8._STALE_REPORTED.clear()
    for f in SCRATCH.glob("*.json"):
        f.unlink()


def check(name, fn):
    try:
        fn()
        print(f"  PASS  {name}")
    except AssertionError as exc:
        failures.append(name)
        print(f"  FAIL  {name}: {exc}")


def case_hit():
    """Cache-HIT path: a stale entry on disk must raise, not be returned."""
    reset()
    (SCRATCH / "HIT.json").write_text(json.dumps(bars_for("HIT", STALE_DAY)))
    try:
        e8.cache_fetch("HIT")
    except e8.StaleCacheError as exc:
        assert "STALE CACHE" in str(exc), f"wrong message: {exc}"
        return
    raise AssertionError("cache_fetch returned instead of raising on a stale HIT")


def case_refetch():
    """Cache-REFETCH path -- the swallow record EO closed. The verdict must
    propagate, and the fetch must NOT be retried as if it were a network error."""
    reset()
    calls = []
    e8.prices.fetch = lambda t, start=None: (calls.append(t),
                                             bars_for(t, STALE_DAY))[1]
    try:
        e8.cache_fetch("REFETCH")
    except e8.StaleCacheError as exc:
        assert "STALE CACHE" in str(exc), f"wrong message: {exc}"
        assert len(calls) == 1, (
            f"fetch retried {len(calls)}x -- the vintage verdict is being "
            "treated as a fetch failure again")
        return
    raise AssertionError("cache_fetch returned instead of raising on a stale refetch")


def case_mixed():
    """Two differing vintages in one process -> MIXED-VINTAGE, which fires
    BEFORE the staleness branch."""
    reset()
    e8.prices.fetch = lambda t, start=None: bars_for(t, FRESH_DAY)
    e8.cache_fetch("ONE")
    (SCRATCH / "TWO.json").write_text(json.dumps(
        bars_for("TWO", (TODAY - datetime.timedelta(days=2)).isoformat())))
    try:
        e8.cache_fetch("TWO")
    except e8.StaleCacheError as exc:
        assert "MIXED-VINTAGE" in str(exc), f"wrong message: {exc}"
        return
    raise AssertionError("two distinct vintages did not raise")


def case_fresh():
    """A fresh single vintage must stay silent -- a guard that always fires is
    as useless as one that never does."""
    reset()
    e8.prices.fetch = lambda t, start=None: bars_for(t, FRESH_DAY)
    got = e8.cache_fetch("FRESH")
    assert got and got[-1][1] == FRESH_DAY, f"unexpected bars: {got}"


def case_real_fetch_failure():
    """A REAL network failure must still be retried 4x and reported as a fetch
    failure -- proof the fix did not break the retry loop it moved."""
    reset()
    calls = []

    def boom(t, start=None):
        calls.append(t)
        raise ValueError("simulated network error")

    e8.prices.fetch = boom
    slept = e8.time.sleep
    e8.time.sleep = lambda s: None
    try:
        e8.cache_fetch("BOOM")
    except e8.StaleCacheError:
        raise AssertionError("a network error was misreported as a vintage verdict")
    except RuntimeError as exc:
        assert "could not fetch" in str(exc), f"wrong message: {exc}"
        assert len(calls) == 4, f"retry loop broken: {len(calls)} attempts, expected 4"
        return
    finally:
        e8.time.sleep = slept
    raise AssertionError("cache_fetch returned on a total fetch failure")


def consumer_case(modname, call):
    reset()
    e8.prices.fetch = lambda t, start=None: bars_for(t, STALE_DAY)
    mod = __import__(modname)
    try:
        call(mod)
    except e8.StaleCacheError:
        return
    raise AssertionError(
        f"{modname} swallowed the vintage verdict and continued -- every ticker "
        "would be silently dropped and the run would report on an empty universe")


def case_override():
    """The documented escape hatch must still downgrade the raise to a print."""
    reset()
    e8._ALLOW_STALE = True
    try:
        (SCRATCH / "OVR.json").write_text(json.dumps(bars_for("OVR", STALE_DAY)))
        assert e8.cache_fetch("OVR"), "override path returned nothing"
    finally:
        e8._ALLOW_STALE = False


def main():
    print("proving the .e8e9_cache freshness guard fires at every swallow site:")
    for name, fn in [
        ("1 cache-HIT stale         -> raises", case_hit),
        ("2 cache-REFETCH stale     -> raises, fetch NOT retried", case_refetch),
        ("3 two vintages            -> raises MIXED-VINTAGE", case_mixed),
        ("4 fresh single vintage    -> silent", case_fresh),
        ("5 real fetch failure      -> still a fetch failure, 4 attempts",
         case_real_fetch_failure),
        ("6 run_m12_factorial       -> re-raises, no mass-drop",
         lambda: consumer_case("run_m12_factorial", lambda m: m.load())),
        ("7 run_v1_harness_check    -> re-raises, no mass-drop",
         lambda: consumer_case("run_v1_harness_check",
                               lambda m: m.load_panel(["AAA", "BBB"]))),
        ("8 SWING_ALLOW_STALE_CACHE -> downgrades to a print", case_override),
    ]:
        check(name, fn)

    shutil.rmtree(SCRATCH, ignore_errors=True)
    print()
    if failures:
        print(f"CACHE GUARD PROOF: {len(failures)} FAILED -> {failures}")
        return 1
    print("CACHE GUARD PROOF: 8/8 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
