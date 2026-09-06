r"""Proof that realize_pending's ledger writes are ATOMIC PER PHASE, so a kill
mid-cycle can never leave a transaction row without its position row (audit FX
MED 4, 2026-09-06). Run:

    .venv\Scripts\python.exe scripts\prove_torn_write.py

WHY A CHILD PROCESS. An in-process `raise` only proves `with conn:` rolls back
on an exception -- it unwinds cleanly, so it does not model ExecutionTimeLimit
or a reboot. Each kill arm re-execs THIS file as a child, which monkeypatches
one paper_sleeves function to call os._exit(137). os._exit skips every
finalizer: no __exit__, no atexit, no conn.close(). The parent then reopens the
file and lets SQLite's rollback journal decide what survived, and asserts the
child died with exactly 137 so a child that merely errored cannot pass as a kill.

WHY FX'S OWN FIX WOULD NOT HAVE WORKED. FX prescribed wrapping the
record_fill/upsert_position pair in one BEGIN/COMMIT. Those functions committed
internally, and an inner commit ENDS the transaction a `with conn:` opened -- so
the wrap was a no-op that made the source read as fixed. Arm G measures that
directly, on this machine, rather than asserting it.

DATA CONVENTION: no price data is read. The prices below are synthetic
placeholders, so no split-adjusted / dividend-UNADJUSTED question arises.
"""
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from swing_bot import paper_sleeves as ps  # noqa: E402

SLEEVE = "e6_1x"
SIGNAL_DATE = "2026-09-03"
TODAY = "2026-09-04"
SELL_PX, BUY_PX = 710.0, 700.0
KILL_CODE = 137


# ---------------------------------------------------------------- child half
def _child(db_path, arm):
    """Runs in a fresh process; dies by os._exit so nothing is flushed."""
    import daily_swing_paper as dsp
    conn = ps.connect(Path(db_path))
    if arm == "pre_fix_pair":
        # The PRE-FIX shape, reproduced verbatim: record_fill self-commits, then
        # the process dies before the position write. This is the control -- if
        # it does not tear, the harness cannot detect tearing at all.
        ps.record_fill(conn, SLEEVE, TODAY, "QQQ", "sell", 1.0, SELL_PX,
                       "pending-liquidate")          # commit=True, the old way
        os._exit(KILL_CODE)
    if arm == "kill_between_pair":
        ps.upsert_position = lambda *a, **k: os._exit(KILL_CODE)
    elif arm == "kill_at_clear_pending":
        ps.clear_pending = lambda *a, **k: os._exit(KILL_CODE)
    dsp.realize_pending(conn, SLEEVE, TODAY, {"QQQ": SELL_PX})
    os._exit(0)          # should be unreachable in the kill arms


# --------------------------------------------------------------- parent half
ok = True
n = 0


def check(label, got, want):
    global ok, n
    n += 1
    hit = got == want
    ok = ok and hit
    print("  %-4s %-56s %s" % ("PASS" if hit else "FAIL", label, got))
    if not hit:
        print("       want: %r" % (want,))


def seed(target, held_qty=1.0, cash=0.0):
    """A throwaway ledger. swing.db is never opened."""
    db = Path(tempfile.mkdtemp()) / "torn.db"
    conn = ps.connect(db)
    ps.init_sleeve(conn, SLEEVE)
    conn.execute("UPDATE paper_sleeves SET cash=? WHERE sleeve=?", (cash, SLEEVE))
    conn.commit()
    if held_qty:
        ps.upsert_position(conn, SLEEVE, "QQQ", held_qty, 700.0, SIGNAL_DATE)
    ps.set_pending(conn, SLEEVE, target, SIGNAL_DATE)
    conn.close()
    return db


def state(db):
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    sl = conn.execute("SELECT * FROM paper_sleeves WHERE sleeve=?", (SLEEVE,)).fetchone()
    tx = conn.execute("SELECT * FROM paper_transactions WHERE sleeve=? "
                      "ORDER BY date, id", (SLEEVE,)).fetchall()
    pos = {r["ticker"]: r["qty"] for r in
           conn.execute("SELECT * FROM paper_positions WHERE sleeve=?", (SLEEVE,))}
    out = dict(cash=sl["cash"], pending=sl["pending_json"],
               tx=[(r["side"], r["ticker"], r["qty"], r["price"]) for r in tx],
               pos=pos)
    conn.close()
    return out


def replay_consistent(st, open_cash, open_pos):
    """Replay every transaction row from the opening state; the result must
    equal the stored cash and positions. This is the mechanised form of the
    hand check clean_ledger_2026-08-25.py had to make after the real incident."""
    cash, pos = open_cash, dict(open_pos)
    for side, tkr, qty, px in st["tx"]:
        if side == "sell":
            cash += qty * px
            pos[tkr] = pos.get(tkr, 0.0) - qty
        else:
            cash -= qty * px
            pos[tkr] = pos.get(tkr, 0.0) + qty
    pos = {k: v for k, v in pos.items() if abs(v) > 1e-9}
    return (abs(cash - st["cash"]) < 1e-9
            and set(pos) == set(st["pos"])
            and all(abs(pos[k] - st["pos"][k]) < 1e-9 for k in pos))


def kill_run(db, arm):
    r = subprocess.run([sys.executable, __file__, "--child", str(db), arm],
                       capture_output=True, text=True)
    return r.returncode


if len(sys.argv) > 1 and sys.argv[1] == "--child":
    _child(sys.argv[2], sys.argv[3])
    raise SystemExit(0)


print("A. CONTROL -- the harness can detect a tear (pre-fix shape)")
db = seed({})
rc = kill_run(db, "pre_fix_pair")
check("child died by os._exit(137)", rc, KILL_CODE)
st = state(db)
check("orphan transaction row survived", len(st["tx"]), 1)
check("position was NOT updated (still held)", st["pos"], {"QQQ": 1.0})
check("replay MISMATCHES stored state -> tear detected",
      replay_consistent(st, 0.0, {"QQQ": 1.0}), False)

print("\nB. FIXED -- the same kill lands nothing")
db_b = seed({})
rc = kill_run(db_b, "kill_between_pair")
check("child died by os._exit(137)", rc, KILL_CODE)
st = state(db_b)
check("transaction rows written", len(st["tx"]), 0)
check("position untouched", st["pos"], {"QQQ": 1.0})
check("cash untouched", st["cash"], 0.0)
check("pending still set (cycle will retry)", st["pending"] is not None, True)
check("replay consistent", replay_consistent(st, 0.0, {"QQQ": 1.0}), True)

print("\nC. RETRY IS CLEAN -- one row, not two (FX's stated failure)")
import daily_swing_paper as dsp  # noqa: E402
conn = ps.connect(db_b)
dsp.realize_pending(conn, SLEEVE, TODAY, {"QQQ": SELL_PX})
conn.close()
st = state(db_b)
check("exactly ONE sell row after the retry", len(st["tx"]), 1)
check("position closed", st["pos"], {})
check("cash = proceeds", round(st["cash"], 6), round(SELL_PX, 6))
check("pending cleared", st["pending"], None)
check("replay consistent", replay_consistent(st, 0.0, {"QQQ": 1.0}), True)

print("\nD. PHASE BOUNDARY -- a kill at clear_pending rolls back the buys too")
db_d = seed({"QQQ": 1.0}, held_qty=0.0, cash=1000.0)
rc = kill_run(db_d, "kill_at_clear_pending")
check("child died by os._exit(137)", rc, KILL_CODE)
st = state(db_d)
check("buy rows written", len(st["tx"]), 0)
check("no position created", st["pos"], {})
check("cash untouched", st["cash"], 1000.0)
check("pending still set -> ONE clean rebuild next run, not churn",
      st["pending"] is not None, True)

print("\nE. HAPPY PATH -- boundaries changed, outcomes did not")
db_e = seed({})
conn = ps.connect(db_e)
dsp.realize_pending(conn, SLEEVE, TODAY, {"QQQ": SELL_PX})
conn.close()
st = state(db_e)
check("sell cycle: 1 row", len(st["tx"]), 1)
check("sell cycle: cash", round(st["cash"], 6), round(SELL_PX, 6))
check("sell cycle: pending cleared", st["pending"], None)

db_e2 = seed({"QQQ": 1.0}, held_qty=0.0, cash=1000.0)
conn = ps.connect(db_e2)
dsp.realize_pending(conn, SLEEVE, TODAY, {"QQQ": BUY_PX})
conn.close()
st = state(db_e2)
check("buy cycle: 1 row", len(st["tx"]), 1)
check("buy cycle: qty = cash/px", round(st["pos"].get("QQQ", 0), 9),
      round(1000.0 / BUY_PX, 9))
check("buy cycle: replay consistent",
      replay_consistent(st, 1000.0, {}), True)

print("\nF. AST TRIPWIRE -- a later edit cannot silently un-defer the writes")
import ast  # noqa: E402
src = (ROOT / "scripts" / "daily_swing_paper.py").read_text(encoding="utf-8")
tree = ast.parse(src)
fn = next(f for f in ast.walk(tree)
          if isinstance(f, ast.FunctionDef) and f.name == "realize_pending")


def calls_in_with(node, inside):
    for child in ast.iter_child_nodes(node):
        nested = inside or (isinstance(child, ast.With) and any(
            getattr(i.context_expr, "id", None) == "conn" for i in child.items))
        if isinstance(child, ast.Call):
            name = getattr(child.func, "attr", None)
            if name in ("record_fill", "upsert_position", "clear_pending"):
                deferred = any(k.arg == "commit"
                               and getattr(k.value, "value", None) is False
                               for k in child.keywords)
                yield name, deferred, inside
        yield from calls_in_with(child, nested)


found = list(calls_in_with(fn, False))
check("ledger-write calls found in realize_pending", len(found), 5)
check("every one passes commit=False", all(d for _, d, _ in found), True)
check("every one is inside a `with conn:`", all(w for _, _, w in found), True)
cash_writes = [nd for nd in ast.walk(fn)
               if isinstance(nd, ast.Call)
               and getattr(nd.func, "attr", None) == "execute"
               and nd.args and isinstance(nd.args[0], ast.Constant)
               and "UPDATE paper_sleeves SET cash" in str(nd.args[0].value)]
check("both cash writes still present", len(cash_writes), 2)
withs = [nd for nd in ast.iter_child_nodes(fn) if isinstance(nd, ast.With)]
check("realize_pending has exactly TWO transactions", len(withs), 2)

print("\nG. FX's PRESCRIBED FIX, measured -- wrapping alone is a NO-OP")
tmp = Path(tempfile.mkdtemp()) / "semantics.db"
c = sqlite3.connect(str(tmp))
c.execute("CREATE TABLE t (x INTEGER)")
c.commit()
try:
    with c:
        c.execute("INSERT INTO t VALUES (1)")
        c.commit()                      # what the OLD record_fill did
        c.execute("INSERT INTO t VALUES (2)")
        c.commit()                      # what the OLD upsert_position did
        raise RuntimeError("simulated kill")
except RuntimeError:
    pass
c.close()
survived = sqlite3.connect(str(tmp)).execute("SELECT count(*) FROM t").fetchone()[0]
check("rows surviving a ROLLED-BACK `with conn:` (2 => wrap is a no-op)",
      survived, 2)

print("\n%s: %d checks" % ("PROVEN" if ok else "FAILED", n))
sys.exit(0 if ok else 1)
