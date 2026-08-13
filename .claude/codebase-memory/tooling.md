# tooling — Swing Trading

Last updated 2026-07-15. Canonical home for run/tooling.

- Python via `.venv`. Code under `swing_bot/` and `scripts/`.
- **Accessing Trading's repo/DB**: Grep/Glob tools do NOT reach
  `D:\ClaudeCode\Trading` (no matches despite files present). Use venv-python
  sqlite (`file:D:\ClaudeCode\Trading\var\trades.db?mode=ro`) + PowerShell.
- `.bat` files: keep PURE ASCII (cmd.exe silently corrupts its whole parse
  otherwise).
- Never rewrite JSON data files with PowerShell (UTF-16/BOM corrupts multibyte);
  use Node / dedicated tools.
- Doc timestamps in **Central, DST-AWARE**: run `date` and label by the reported
  offset — **UTC-6 → CST, UTC-5 → CDT**. The /project-memory cadence hook reports
  UTC (Z); subtract the CURRENT offset (6h CST / 5h CDT), never a hardcoded 5
  (date rolls back if UTC time is before the offset). This bullet read
  "CST (UTC-5)" — self-contradictory, since CST is UTC-6 — from bootstrap until
  2026-08-13; HANDOFF had the same wording fixed on 2026-07-28 by audit #7 and
  this bin was never updated. Corrected in record EO.
- **Research-cache env knobs** (read ONCE at import of
  `scripts/run_e8_squeeze.py`, so set them before the process starts):
  `SWING_ALLOW_STALE_CACHE=1` disables the vintage guard for a deliberately
  historical run — strict `=1`, so `true`/`yes` silently do NOTHING and the run
  still raises (fails closed, on purpose). `SWING_MAX_CACHE_STALE_DAYS`
  (default 5) is the calendar-day tolerance; it is parsed with a bare `int()` at
  module level, so a non-integer value is an uncaught `ValueError` at import —
  loud and before any order, which is the intended direction. `E8E9_CACHE`
  redirects the cache directory (used by `scripts/prove_cache_guard.py` to test
  without touching the real one).
