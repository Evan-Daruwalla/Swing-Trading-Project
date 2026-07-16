# testing — Swing Trading

Last updated 2026-07-15. **No test suite exists yet (as of 2026-07-08).**

Planned (CLAUDE.md definition-of-done): once a backtest engine lands, PORT
Trading's frozen-regression-test pattern and make it a required done-check —
pinned reference numbers, fail LOUD on drift. pytest is optional; frozen tests
run via `swing_bot/test_frozen.py`'s own `__main__` (Trading's pattern).

Discipline (independent of risk appetite): prereg before results; NEVER tune a
FAIL. Replace this stub with the real test contract when the engine exists.
