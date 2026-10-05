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

DATA CONVENTION: no price data is read. The prices below are synthetic
placeholders, so no split-adjusted / dividend-UNADJUSTED question arises.
Every DB is a throwaway under tempfile.mkdtemp(); swing.db is never opened.
"""
import shutil
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

if failures:
    print("\nLOOP GUARDS PROOF: %d/%d PASS -- FAILED" % (n - len(failures), n))
    for f in failures:
        print("  FAIL " + f)
    sys.exit(1)
print("\nLOOP GUARDS PROOF: %d/%d PASS" % (n, n))
sys.exit(0)
