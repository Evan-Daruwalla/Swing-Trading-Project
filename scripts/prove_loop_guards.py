r"""Proof that the daily loop's two new guards behave on the dates that broke
the old logic (record GT MED 6, 2026-09-08 late-fill case). Run:

    .venv\Scripts\python.exe scripts\prove_loop_guards.py

WHAT IS PROVEN.
  fill_session(signal_date, today) returns the ISO date of the first trading
  session STRICTLY AFTER signal_date -- not `today`. The case that matters:
  the Thursday 2026-09-03 signal's Friday 09-04 run was lost, and the next run
  is Tuesday 2026-09-08 (Labor Day 09-07 is closed). The pending order must
  fill dated 09-04, the session it should have filled on, not 09-08. When
  nothing was lost (signal 09-04, next session 09-08) the answer is unchanged
  from `today`. It also returns `today` for a falsy signal_date, for
  signal_date >= today, and (by contract) when no session lies in between.
  stale_sessions(qdates, asof_dt, today) counts the quote dates strictly after
  asof_dt and at or before today, and is 0 when asof_dt is None.
  Case 8 runs the pair end to end on a temp DB: a sleeve holding 1.0 QQQ with a
  pending cash target, fed through fill_session into the UNCHANGED
  realize_pending, must book exactly one sell row dated 2026-09-04 at the
  given open and credit its proceeds to cash.
  Section D (record GX, 2026-10-11): on a temp DB, a run_lock row 3 h old is
  declared stale -- _acquire_run_lock returns a connection, the row now holds
  this pid, and RUN_FAILURES names the stale lock; a 10 min old row is refused
  (returns None) and left byte-for-byte unchanged.
  Section E (GX): an AST tripwire -- the fresh_ff3() and series_with_volume()
  calls inside _run each sit in a try body whose handler catches Exception.

DATA CONVENTION: no price data is read. The prices below are synthetic
placeholders, so no split-adjusted / dividend-UNADJUSTED question arises.
Every DB is a throwaway under tempfile.mkdtemp(); swing.db is never opened.
"""
import ast
import datetime as dt
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from swing_bot import paper_sleeves as ps  # noqa: E402
import daily_swing_paper as dsp  # noqa: E402

SLEEVE = "e6_1x"
failures = []
n = 0


def check(label, got, want):
    global n
    n += 1
    hit = got == want
    if not hit:
        failures.append("%s: got %r, want %r" % (label, got, want))
    print("  %-4s %-62s %s" % ("PASS" if hit else "FAIL", label, got))
    if not hit:
        print("       want: %r" % (want,))


print("A. fill_session -- the first session strictly after the signal")
check("Thu signal, Fri run lost, run Tue after Labor Day -> Fri",
      dsp.fill_session("2026-09-03", "2026-09-08"), "2026-09-04")
check("Fri signal, Labor Day skipped, nothing lost -> Tue",
      dsp.fill_session("2026-09-04", "2026-09-08"), "2026-09-08")
check("signal_date == today -> today",
      dsp.fill_session("2026-09-08", "2026-09-08"), "2026-09-08")
check("signal_date None -> today",
      dsp.fill_session(None, "2026-09-08"), "2026-09-08")

print("\nB. stale_sessions -- quote dates after asof, up to today")
QDATES = ["2026-09-02", "2026-09-03", "2026-09-04"]
check("asof 09-02 -> 2 stale sessions",
      dsp.stale_sessions(QDATES, "2026-09-02", "2026-09-04"), 2)
check("asof 09-04 (current) -> 0",
      dsp.stale_sessions(QDATES, "2026-09-04", "2026-09-04"), 0)
check("asof None -> 0",
      dsp.stale_sessions(QDATES, None, "2026-09-04"), 0)

print("\nC. END TO END -- late fill books the Friday session, not the Tuesday")
tmpdir = Path(tempfile.mkdtemp())
try:
    conn = ps.connect(tmpdir / "loop_guards.db")
    ps.init_sleeve(conn, SLEEVE)
    ps.upsert_position(conn, SLEEVE, "QQQ", 1.0, 100.0, "2026-09-01")
    conn.execute("UPDATE paper_sleeves SET cash=0.0 WHERE sleeve=?", (SLEEVE,))
    conn.commit()
    ps.set_pending(conn, SLEEVE, {}, "2026-09-03")
    conn.commit()
    before = conn.execute("SELECT COUNT(*) FROM paper_transactions "
                          "WHERE sleeve=?", (SLEEVE,)).fetchone()[0]
    fill_date = dsp.fill_session("2026-09-03", "2026-09-08")
    dsp.realize_pending(conn, SLEEVE, fill_date, {"QQQ": 101.0})
    rows = conn.execute("SELECT date, ticker, side, price FROM paper_transactions "
                        "WHERE sleeve=? ORDER BY id", (SLEEVE,)).fetchall()
    cash = ps.get_sleeve(conn, SLEEVE)["cash"]
    conn.close()
    check("exactly ONE new paper_transactions row", len(rows) - before, 1)
    check("row == (2026-09-04, QQQ, sell, 101.0)",
          tuple(rows[-1]) if rows else None,
          ("2026-09-04", "QQQ", "sell", 101.0))
    check("sleeve cash == 101.0 (within 1e-9)", abs(cash - 101.0) < 1e-9, True)
finally:
    shutil.rmtree(tmpdir, ignore_errors=True)

print("\nD. stale run_lock is cleared after 2 h; a live one still refuses")
lock_dir = Path(tempfile.mkdtemp())
orig_db = ps.DB_PATH
try:
    ps.DB_PATH = lock_dir / "lock.db"

    def plant(age):
        """Write the single run_lock row aged `age`; return its held_at string."""
        held = (dt.datetime.now(dt.timezone.utc) - age).isoformat()
        c = sqlite3.connect(str(ps.DB_PATH))
        c.execute("CREATE TABLE IF NOT EXISTS run_lock ("
                  "id INTEGER PRIMARY KEY CHECK (id = 1), "
                  "held_at TEXT NOT NULL, pid INTEGER NOT NULL)")
        c.execute("DELETE FROM run_lock")
        c.execute("INSERT INTO run_lock (id, held_at, pid) VALUES (1, ?, 99999)",
                  (held,))
        c.commit()
        c.close()
        return held

    dsp.RUN_FAILURES.clear()
    plant(dt.timedelta(hours=3))
    lk = dsp._acquire_run_lock()
    check("3 h old lock -> acquired", lk is not None, True)
    check("lock row now holds this pid",
          lk is not None and lk.execute(
              "SELECT pid FROM run_lock WHERE id=1").fetchone()[0] == os.getpid(),
          True)
    check("RUN_FAILURES names the stale lock",
          any("stale run_lock" in f for f in dsp.RUN_FAILURES), True)
    if lk is not None:
        dsp._release_run_lock(lk)

    dsp.RUN_FAILURES.clear()
    ha = plant(dt.timedelta(minutes=10))
    lk2 = dsp._acquire_run_lock()
    check("10 min old lock -> refused", lk2 is None, True)
    if lk2 is not None:
        dsp._release_run_lock(lk2)
    c = sqlite3.connect(str(ps.DB_PATH))
    row = c.execute("SELECT held_at, pid FROM run_lock WHERE id=1").fetchone()
    c.close()
    check("live lock row unchanged", tuple(row) if row else None, (ha, 99999))
    dsp.RUN_FAILURES.clear()
finally:
    ps.DB_PATH = orig_db
    shutil.rmtree(lock_dir, ignore_errors=True)

print("\nE. the FF3 and universe fetches are inside try/except Exception (AST)")
tree = ast.parse((ROOT / "scripts" / "daily_swing_paper.py").read_text(encoding="utf-8"))
run_fn = next((f for f in ast.walk(tree)
               if isinstance(f, ast.FunctionDef) and f.name == "_run"), None)


def guarded(fn, name):
    """True if some ast.Try in fn has `name(...)` in its body and an
    `except Exception` handler."""
    if fn is None:
        return False
    for t in ast.walk(fn):
        if not isinstance(t, ast.Try):
            continue
        in_body = any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                      and c.func.id == name
                      for stmt in t.body for c in ast.walk(stmt))
        catches = any(isinstance(h.type, ast.Name) and h.type.id == "Exception"
                      for h in t.handlers)
        if in_body and catches:
            return True
    return False


for name in ("fresh_ff3", "series_with_volume"):
    check("%s() call is inside try/except Exception" % name,
          guarded(run_fn, name), True)

if failures:
    print("\nLOOP GUARDS PROOF: %d/%d PASS -- FAILED" % (n - len(failures), n))
    for f in failures:
        print("  FAIL " + f)
    sys.exit(1)
print("\nLOOP GUARDS PROOF: %d/%d PASS" % (n, n))
sys.exit(0)
