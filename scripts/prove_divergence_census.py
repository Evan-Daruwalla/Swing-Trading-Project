r"""Proof that the fidelity instrument reports its own dark half, on EVERY run
including a dry run (PRD M13.3, record FH). Run:

    .venv\Scripts\python.exe scripts\prove_divergence_census.py

Two halves, because proving the function is not proving the call site:

  A. NUMBERS -- seed a throwaway DB with the exact shape of the live
     fill_divergence table and assert the buckets and the printed line. No
     network, no Alpaca, and swing.db is never opened.
  B. UNGATED -- parse scripts/daily_swing_paper.py with `ast` and assert the
     print_divergence_census(...) call inside _run() is NOT nested under any
     `if args.execute:`. That is the whole point of M13.3's done-check: the
     line has to appear on a dry run, and backfill_divergence -- which the PRD
     named as the printer -- is called only under --execute.

DATA CONVENTION: no price data is read; the seeded prices are synthetic
placeholders, so no split-adjusted / dividend-UNADJUSTED question arises.
"""
import ast
import io
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from swing_bot import paper_sleeves as ps  # noqa: E402

# The live table's SHAPE at 2026-09-05, read read-only and transcribed as
# (order_id, status, alpaca_price). 10 rows: 4 measured, 1 canceled with no fill
# price, 5 never mirrored, 0 pending. The order ids are SYNTHETIC on purpose --
# the census only ever tests NULL vs NOT NULL, so the real Alpaca ids would add
# nothing here and this file lives in a public repo. Prices are the real ones,
# because they are what makes the "+0.0/+0.0/+1.3 bps is 3 of 4" arithmetic
# checkable.
LIVE_SHAPE = [
    ("oid-1", "filled",   712.0),
    ("oid-2", "filled",   712.0),
    (None,    None,       None),
    (None,    None,       None),
    ("oid-3", "canceled", None),
    ("oid-4", "filled",   702.35),
    (None,    None,       None),
    (None,    None,       None),
    ("oid-5", "filled",   700.622),
    (None,    None,       None),
]

ok = True
n = 0


def check(label, got, want):
    global ok, n
    n += 1
    hit = got == want
    ok = ok and hit
    print("  %-4s %-52s %s" % ("PASS" if hit else "FAIL", label, got))
    if not hit:
        print("       want: %r" % (want,))


def seed(rows):
    """A throwaway DB carrying only the table under test."""
    path = Path(tempfile.mkdtemp()) / "census.db"
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE fill_divergence (
        id INTEGER PRIMARY KEY AUTOINCREMENT, sleeve TEXT NOT NULL,
        date TEXT NOT NULL, ticker TEXT NOT NULL, sim_price REAL NOT NULL,
        alpaca_price REAL, alpaca_order_id TEXT, logged_at TEXT NOT NULL,
        alpaca_status TEXT, alpaca_qty REAL)""")
    for oid, status, px in rows:
        conn.execute(
            "INSERT INTO fill_divergence (sleeve, date, ticker, sim_price, "
            "alpaca_price, alpaca_order_id, logged_at, alpaca_status) "
            "VALUES ('e6_1x', '2026-07-15', 'QQQ', 700.0, ?, ?, 'x', ?)",
            (px, oid, status))
    conn.commit()
    return conn


print("A. buckets on the live table's exact shape")
conn = seed(LIVE_SHAPE)
c = ps.divergence_census(conn)
check("total", c["total"], 10)
check("measured (a real broker fill to compare)", c["measured"], 4)
check("resolved_no_price (canceled: outcome known, no fill)",
      c["resolved_no_price"], 1)
check("dark (no alpaca_order_id, PERMANENTLY unmeasurable)", c["dark"], 5)
check("pending (backfill work list)", c["pending"], 0)
check("buckets sum to total",
      c["measured"] + c["resolved_no_price"] + c["dark"] + c["pending"],
      c["total"])

print("\nA2. degenerate and all-good tables")
check("empty table -> all zeros", ps.divergence_census(seed([]))["total"], 0)
allgood = seed([("a", "filled", 1.0), ("b", "filled", 2.0)])
cg = ps.divergence_census(allgood)
check("2 measured, 0 dark", (cg["measured"], cg["dark"]), (2, 0))

print("\nB. the call site is NOT gated behind --execute")
src = io.open(ROOT / "scripts" / "daily_swing_paper.py", encoding="utf-8").read()
tree = ast.parse(src)
run_fn = next(f for f in ast.walk(tree)
              if isinstance(f, ast.FunctionDef) and f.name == "_run")


def gated_calls(node, inside_execute):
    """Yield (call_name, is_inside_an_args.execute_branch) for every call."""
    for child in ast.iter_child_nodes(node):
        nested = inside_execute
        if isinstance(child, ast.If):
            t = ast.dump(child.test)
            if "attr='execute'" in t or 'attr="execute"' in t:
                nested = True
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
            yield child.func.id, inside_execute
        yield from gated_calls(child, nested)


found = [g for name, g in gated_calls(run_fn, False)
         if name == "print_divergence_census"]
check("print_divergence_census called in _run", len(found), 1)
check("...and NOT under `if args.execute:`", found[0] if found else None, False)

backfill = [g for name, g in gated_calls(run_fn, False)
            if name == "backfill_divergence"]
check("backfill_divergence IS still --execute-only (why we split)",
      backfill, [True])

print("\nC. the line the operator actually reads")
sys.path.insert(0, str(ROOT / "scripts"))
import daily_swing_paper as dsp  # noqa: E402

buf = io.StringIO()
_stdout, sys.stdout = sys.stdout, buf
try:
    dsp.print_divergence_census(conn)
finally:
    sys.stdout = _stdout
out = buf.getvalue()
for frag in ("10 row(s)", "4 MEASURED", "5 PERMANENTLY DARK",
             "0 awaiting backfill", "4 of 10 rows can EVER yield"):
    check("line contains %r" % frag, frag in out, True)
print(out.strip())

print("\n%s: %d checks" % ("PROVEN" if ok else "FAILED", n))
sys.exit(0 if ok else 1)
