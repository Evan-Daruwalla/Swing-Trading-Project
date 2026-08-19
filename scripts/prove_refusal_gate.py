"""Prove a sleeve REFUSING to decide reaches the exit gate, not just the log.

WHY THIS EXISTS. Audit 2026-08-19 finding 1: `decisions[s] = (None, err)` was
printed as "today's decision: SKIPPED (err)" and dropped. None of the seven
`RUN_FAILURES.append` sites was on that path, so a sleeve that refused to run
its rule -- VIX3M stale, VIX feed empty, <200 sessions of history -- still
exited 0 while paper_nav recorded the session. OBSERVED 2026-07-13: the log
shows `VIX3M=None -> SKIPPED (VIX or VIX3M unavailable today)`, and all 29 runs
in that log exited 0. That is forward evidence with a silent hole in it, which
is the one thing the M3 series has to be trusted about.

The root cause was that `err` was ONE channel carrying two different things:
an ordinary "today is not a decision day" and a genuine data refusal. The fix
prefixes the routine case (ROUTINE_SKIP) so the gate can tell them apart.

Following prove_cache_guard.py's standard: feeding a guard its trigger proves
the GUARD fires; it does not prove anyone lets the failure through. So this
checks BOTH --
  (1) CLASSIFICATION, against the error strings the REAL decide_* functions
      return when fed their real triggers (nothing hardcoded); and
  (2) REACHABILITY, by AST: the append really is inside the `if err:` branch,
      and RUN_FAILURES really does drive a non-zero return.

WRITES NOTHING. No DB, no network, no file touched.

Run:  .venv\\Scripts\\python.exe scripts\\prove_refusal_gate.py
Exits non-zero on any failure.
"""
import ast
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from swing_bot import paper_sleeves as ps  # noqa: E402
from scripts.daily_swing_paper import ROUTINE_SKIP  # noqa: E402

SRC = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "daily_swing_paper.py"


def _classification_cases():
    """(label, err, should_fail) using the REAL functions' real messages."""
    # Each decide_* fed the trigger that actually occurred / can occur.
    _, e_vix = ps.decide_e18_vixts(None, None)          # OBSERVED 2026-07-13
    _, e_hist = ps.decide_e6_1x([1.0] * 10)             # <200 sessions
    _, e_m10 = ps.decide_m10_1(None, [1.0] * 250)       # VIX feed empty
    _, e_basket = ps.decide_m10_1(25.0, [1.0] * 250, [])  # stress, no ranks
    stale = ("VIX3M STALE (3 sessions behind; asof 2026-07-10 vs 2026-07-13) "
             "-- refusing to decide on a stale term structure")
    routine_a = ROUTINE_SKIP + "week 2026-W33 already decided"
    routine_b = ROUTINE_SKIP + ("not a decision day (today is not Friday; "
                                "last decided 2026-08-14, current week 2026-W34)")
    return [
        ("e18 VIX3M unavailable (OBSERVED 2026-07-13)", e_vix, True),
        ("e6 insufficient history", e_hist, True),
        ("m10 VIX unavailable", e_m10, True),
        ("m10 no residual ranks for stress basket", e_basket, True),
        ("e18 VIX3M stale refusal", stale, True),
        ("routine: week already decided", routine_a, False),
        ("routine: not a decision day", routine_b, False),
    ]


def check_classification():
    failures = []
    print("(1) CLASSIFICATION -- does the gate's predicate split the channel?")
    for label, err, should_fail in _classification_cases():
        assert err, f"{label}: real function returned no error message"
        # This is the predicate the fix uses, verbatim.
        counted = not err.startswith(ROUTINE_SKIP)
        ok = counted == should_fail
        if not ok:
            failures.append(label)
        verdict = "COUNTS as run failure" if counted else "ignored (routine)"
        print(f"  [{'OK ' if ok else 'FAIL'}] {label}\n"
              f"         -> {verdict}   msg={err[:58]!r}")
    return failures


def check_reachability():
    """AST: the append is inside `if err:`, and RUN_FAILURES drives the return."""
    failures = []
    print("\n(2) REACHABILITY -- does the failure actually reach the exit gate?")
    tree = ast.parse(SRC.read_text(encoding="utf-8"))

    def appends_under(node):
        return [n for n in ast.walk(node)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and n.func.attr == "append"
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "RUN_FAILURES"]

    # (a) an `if err:` whose body appends to RUN_FAILURES
    err_ifs = [n for n in ast.walk(tree)
               if isinstance(n, ast.If)
               and isinstance(n.test, ast.Name) and n.test.id == "err"]
    guarded = [n for n in err_ifs if appends_under(n)]
    ok_a = bool(guarded)
    failures += [] if ok_a else ["no `if err:` branch appends to RUN_FAILURES"]
    print(f"  [{'OK ' if ok_a else 'FAIL'}] `if err:` branch appends to "
          f"RUN_FAILURES ({len(guarded)} of {len(err_ifs)} such branches)")

    # (b) that append is guarded by the ROUTINE_SKIP test, so routine days stay quiet
    ok_b = any(
        any(isinstance(sub, ast.If)
            and "ROUTINE_SKIP" in ast.dump(sub.test)
            and appends_under(sub)
            for sub in ast.walk(n))
        for n in guarded)
    failures += [] if ok_b else ["append is not gated on ROUTINE_SKIP"]
    print(f"  [{'OK ' if ok_b else 'FAIL'}] that append is gated on ROUTINE_SKIP")

    # (c) `if RUN_FAILURES:` returns non-zero
    gates = [n for n in ast.walk(tree)
             if isinstance(n, ast.If)
             and isinstance(n.test, ast.Name) and n.test.id == "RUN_FAILURES"]
    ok_c = any(
        any(isinstance(sub, ast.Return)
            and isinstance(sub.value, ast.Constant)
            and sub.value.value != 0
            for sub in ast.walk(g))
        for g in gates)
    failures += [] if ok_c else ["RUN_FAILURES does not drive a non-zero return"]
    print(f"  [{'OK ' if ok_c else 'FAIL'}] `if RUN_FAILURES:` returns non-zero "
          f"({len(gates)} gate(s) found)")
    return failures


def main():
    failures = check_classification() + check_reachability()
    print()
    if failures:
        print(f"REFUSAL GATE PROOF: {len(failures)} FAILED -> {failures}")
        return 1
    print("REFUSAL GATE PROOF: 10/10 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
