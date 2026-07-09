"""Frozen-regression tripwire for swing_bot.

Pattern ported from the Trading project (`trading_bot/strategies/
test_strategies.py`): pin deterministic quantities to EXACT reference numbers
and fail loud on any drift (d must be 0 at the case's declared precision — the
project's d=+/-0.0000pp discipline). A cheap tripwire against silent
regressions from "obviously unrelated" changes.

Runs via its OWN __main__ (no pytest needed):
    .venv\\Scripts\\python.exe -m swing_bot.test_frozen

M0.5 STATUS: the numeric cases below are PLACEHOLDER fixtures that prove the
comparison machinery (reference table, drift calc, loud failure, exit code).
They pin the deterministic `signals.ibs` primitive on synthetic bars. In M2
(task 11) these are REPLACED by real E1 backtest references — tpnl% (unit
'pp', dp 4) and closed_count (unit '', dp 0) on two pinned windows. Do not
delete this harness; extend REFERENCES.
"""
from collections import namedtuple

from swing_bot import signals

Case = namedtuple("Case", ["name", "value", "ref", "unit", "dp"])

# --- PLACEHOLDER numeric references (M0.5) -------------------------------
# Synthetic bars: ibs() is exact rational arithmetic, so drift is exactly 0.
REFERENCES = [
    Case("ibs_mid",  signals.ibs(10.0, 8.0, 9.0),  0.5,  "", 6),
    Case("ibs_high", signals.ibs(10.0, 8.0, 9.5),  0.75, "", 6),
    Case("ibs_low",  signals.ibs(10.0, 8.0, 8.2),  0.1,  "", 6),
]

# --- Invariants (non-numeric asserts) -----------------------------------
INVARIANTS = [
    ("ibs_zero_range_is_none", signals.ibs(10.0, 10.0, 10.0) is None),
    ("ibs_inverted_is_none",   signals.ibs(8.0, 10.0, 9.0) is None),
]


def run():
    ok = True
    print(f"{'case':24}{'value':>14}{'ref':>14}{'d':>14}  result")
    print("-" * 82)
    for c in REFERENCES:
        d = round(c.value - c.ref, c.dp)
        passed = (d == 0)
        ok = ok and passed
        u = c.unit
        print(f"{c.name:24}{c.value:>14.{c.dp}f}{c.ref:>14.{c.dp}f}"
              f"{('%+.*f%s' % (c.dp, d, u)):>14}  "
              f"{'PASS' if passed else 'FAIL <<<'}")
    print("-" * 82)
    for name, cond in INVARIANTS:
        ok = ok and cond
        print(f"{name:24}{'':>42}  {'PASS' if cond else 'FAIL <<<'}")
    print("-" * 82)
    print("FROZEN TESTS:", "GREEN (all d=0)" if ok else "RED - DRIFT DETECTED")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
