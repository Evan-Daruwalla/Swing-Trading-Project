"""Backfill the paper_nav holes of the 2026-09-04..09-22 dark window (Evan's call,
2026-09-22). Prices: split-adjusted, dividend-UNADJUSTED (prices.fetch,
auto_adjust=False) -- the same Close the live loop marks with.

A backfilled row is written ONLY if it is exactly the row the live loop would
have written. That holds when, and only when:
  (1) the DB ledger did not change across the window -- no transaction after the
      first validated date, no pending order, cash as stored;
  (2) every rule would have said HOLD on every missed session (a different
      target means the loop would have traded, and a mark-only row would then be
      a guess, not a reconstruction);
  (3) the reconstruction reproduces every row that DOES exist in the window,
      to 1e-9, from today's fetch -- proving the formula and the closes match
      what the loop actually used.
Any failure aborts before a single write.

  backfill_nav_holes.py                        dry run: all checks, prints the rows
  backfill_nav_holes.py --end YYYY-MM-DD       dry run, window ends on that date
                                               (default 2026-09-21)
  backfill_nav_holes.py --apply                writes (after a consistent backup of swing.db)
  backfill_nav_holes.py --end YYYY-MM-DD --apply
"""
import datetime as dt
import sqlite3
import sys
from pathlib import Path

ROOT = Path(r"D:\ClaudeCode\Swing Trading")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

from swing_bot import paper_sleeves as ps, trading_calendar as tc  # noqa: E402
import daily_swing_paper as live  # noqa: E402  (functions only; main() is guarded)

APPLY = "--apply" in sys.argv
# default 2026-09-21 reproduces record GP's run; --end 2026-10-02 covers the 09-22 hole (record GT, 2026-10-03)
END = (dt.date.fromisoformat(sys.argv[sys.argv.index("--end") + 1])
       if "--end" in sys.argv else dt.date(2026, 9, 21))
WINDOW = (dt.date(2026, 9, 1), END)
DB = ROOT / "swing.db"
fail = []


def die(msg):
    print("ABORT:", msg)
    raise SystemExit(1)


now = dt.datetime.now()
if APPLY and now.time() >= dt.time(23, 15):
    die(f"{now:%H:%M} local -- too close to the 23:45 scheduled run")

ro = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
if ro.execute("SELECT name FROM sqlite_master WHERE name='run_lock'").fetchone() \
        and ro.execute("SELECT 1 FROM run_lock WHERE id=1").fetchone():
    die("run_lock is held -- a live run is in progress")

sessions = [d.isoformat() for d in tc.sessions_between(*WINDOW)]
have = {(s, d): n for s, d, n in ro.execute(
    "SELECT sleeve, date, nav FROM paper_nav WHERE date BETWEEN ? AND ?",
    (sessions[0], sessions[-1]))}
holes = [(s, d) for s in ps.SLEEVES for d in sessions if (s, d) not in have]
print(f"window {sessions[0]}..{sessions[-1]}: {len(sessions)} sessions, "
      f"{len(have)} rows present, {len(holes)} holes")

# ---- (1) the ledger was frozen across the window ----
last_tx = ro.execute("SELECT MAX(date) FROM paper_transactions").fetchone()[0]
if last_tx > sessions[0]:
    die(f"a transaction is dated {last_tx}, after {sessions[0]}")
state = {}
for s in ps.SLEEVES:
    cash, pend = ro.execute("SELECT cash, pending_json FROM paper_sleeves WHERE sleeve=?",
                            (s,)).fetchone()
    if pend:
        die(f"{s} has a pending order {pend}")
    pos = dict(ro.execute("SELECT ticker, qty FROM paper_positions WHERE sleeve=?", (s,)))
    state[s] = (cash, pos)
    print(f"  {s}: cash {cash}, positions {pos}")
tickers = {t for _, pos in state.values() for t in pos}
if tickers != {"QQQ"}:
    die(f"held tickers {tickers}, this script only reconstructs QQQ")

# ---- fetch, exactly as the live loop does ----
qdates, qclose, _ = live.series("QQQ")
_, vclose, _ = live.series("^VIX", start="2015-01-01")
v3 = live.vix3m_close()


def nav(s, d):
    cash, pos = state[s]
    return cash + sum(q * qclose[d] for t, q in pos.items())


# ---- (3) reproduce every existing row ----
for (s, d), stored in sorted(have.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    got = nav(s, d)
    ok = abs(got - stored) < 1e-9
    print(f"  reproduce {s:12} {d}: stored {stored:.10f} got {got:.10f} "
          f"{'OK' if ok else 'MISMATCH'}")
    if not ok:
        fail.append(f"reproduce {s} {d}")

# ---- (2) every rule says HOLD on every missed session ----
missed_days = sorted({d for _, d in holes})
for d in missed_days:
    if d not in qclose:
        fail.append(f"no clean QQQ close for {d}")
        continue
    hist = [qclose[x] for x in qdates if x <= d]
    e6, e6err = ps.decide_e6_1x(hist)
    vix, vx3 = vclose.get(d), v3.get(d)
    e18, e18err = ps.decide_e18_vixts(vix, vx3)
    m10_calm = vix is not None and vix <= live.VIX_THR
    line = (f"  {d}: close {qclose[d]:.2f} 200dma {sum(hist[-200:]) / 200:.2f} "
            f"e6={e6} | VIX {vix} VIX3M {vx3} e18={e18} | m10 calm={m10_calm}")
    print(line)
    if e6 != {"QQQ": 1.0}:
        fail.append(f"{d}: e6 would not hold ({e6}, {e6err})")
    if e18 != {"QQQ": 1.0}:
        fail.append(f"{d}: e18 would not hold ({e18}, {e18err})")
    if not m10_calm:
        fail.append(f"{d}: VIX {vix} > {live.VIX_THR} -- m10 stress branch could trade")

if fail:
    print("\nNOT WRITTEN -- checks failed:")
    for f in fail:
        print("  x", f)
    raise SystemExit(1)

rows = [(s, d, nav(s, d)) for s, d in holes]
print(f"\nall checks passed; {len(rows)} rows:")
for r in rows:
    print(f"  {r[0]:12} {r[1]}  {r[2]:.4f}")

if not APPLY:
    print("\nDRY RUN -- nothing written. Re-run with --apply.")
    raise SystemExit(0)

# var/ is gitignored; the backup used to land in scripts/ once this file moved there (record GT LOW)
backup = ROOT / "var" / f"swing.db.pre-backfill-{now:%Y%m%d-%H%M%S}"
dst = sqlite3.connect(str(backup))
ro.backup(dst)
dst.close()
print(f"\nbackup: {backup}")
ro.close()

w = ps.connect()
for s, d, n in rows:
    ps.record_nav(w, s, d, n)
w.close()
print(f"WROTE {len(rows)} paper_nav rows")
