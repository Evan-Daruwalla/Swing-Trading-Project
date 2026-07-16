# dependencies — Swing Trading

Last updated 2026-07-15. Canonical home; exact pins in `requirements.txt` (direct,
pinned 2026-07-08) + `requirements.lock` (full transitive, `pip freeze`).

- Python **3.14.4** (`.venv`). pandas/numpy are BLEEDING-EDGE majors (pandas
  3.0.x) — if a pandas/numpy edge breaks a milestone, **revisit the Python
  version, don't code around it** (record Appendix E).
- `yfinance==1.5.1` (own price fetcher — see data.md), `httpx==0.28.1`.
- pytest OPTIONAL — frozen-regression tests run via their own `__main__`
  (`swing_bot/test_frozen.py`), matching Trading's pattern (see testing.md).
- After any dependency change, re-pin `requirements.txt` and refresh the lock.
