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
- 2026-09-05 (record FK): **record CORRECTIONS are written as `## <X>-note -
  ...` sub-heads, NEVER as `# Appendix <X>-note - ...`.** The latter is
  unparseable to `append-record-entry.js` and wedges every future append to the
  project (it did, for 54 days). Existing precedent in this record:
  `## 2. CORRECTION to Appendix EF`. A top-level `# Appendix <LETTERS> -`
  heading must use a fresh, unused letter with no suffix.
- 2026-09-05 (record FK): **a hard rule the code must contradict gets a DATED
  EXCEPTION in CLAUDE.md plus a pointer comment at the code line - never a
  silent divergence and never a "fix" that breaks the evidence.** Live case:
  `swing_bot/paper_sleeves.py:43` `STRESS_K = 4` exceeds the K=1-3 ceiling.
  K=4 is the parameter C1 and M10-1 were backtested at, so dropping to 3 would
  make the live sleeve run a rule no backtest has tested. The exception states
  its scope (M10-1 stress branch only) and its reversal path (re-run both at
  K=3 under a fresh prereg).
