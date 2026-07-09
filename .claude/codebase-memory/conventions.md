# conventions — Swing Trading

- 2026-07-08: Doc system per /project-memory: HANDOFF.md (only live snapshot)
  + append-only record in `docs/` + PRD_ROADMAP.md (once written) + these
  bins. Absolute dates everywhere. No HTML twin yet.
- 2026-07-08: Any script touching price data states its adjustment convention
  in a header comment (project CLAUDE.md rule).
- 2026-07-08: Frozen-regression-test pattern (pinned reference numbers, own
  `__main__`, fail loud on >5bps drift) is the planned test convention once a
  backtest engine exists — port from Trading's
  `trading_bot/strategies/test_strategies.py`.
- 2026-07-08: `.bat` files pure ASCII; JSON data files never rewritten via
  PowerShell (machine-wide gotchas, inherited).
