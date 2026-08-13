# conventions — Swing Trading

- 2026-07-08: Doc system per /project-memory: HANDOFF.md (only live snapshot)
  + append-only record in `docs/` + `PRD_ROADMAP.md` (written 2026-07-08) +
  these bins. Absolute dates everywhere. No HTML twin yet. (The "(once
  written)" conditional stood for five weeks after the PRD existed; corrected
  2026-08-13, record EO.)
- 2026-07-08: Any script touching price data states its adjustment convention
  in a header comment (project CLAUDE.md rule).
- 2026-07-08: Frozen-regression-test pattern (pinned reference numbers, own
  `__main__`, fail loud on drift) is the planned test convention once a
  backtest engine exists — port from Trading's
  `trading_bot/strategies/test_strategies.py`.
  **UPDATE 2026-08-13 (record EO): no longer planned — DONE.** The port is
  `swing_bot/test_frozen.py`, green since 2026-07-09, and project CLAUDE.md
  makes it the REQUIRED done-check. Tolerance is tighter than this bullet
  described: refs are pinned at d=±0.0000pp, not ">5bps drift". See testing.md.
- 2026-07-08: `.bat` files pure ASCII; JSON data files never rewritten via
  PowerShell (machine-wide gotchas, inherited).
