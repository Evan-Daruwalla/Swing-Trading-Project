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
- Doc timestamps in **CST (UTC-5)**: the /project-memory cadence hook reports
  UTC (Z) — subtract 5h before stamping (date rolls back if UTC time < 05:00).
