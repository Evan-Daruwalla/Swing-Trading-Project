# Swing Trading — project instructions

Read `HANDOFF.md` FIRST in a fresh session. Append-only record:
`docs/Project Record — Full Chronological History.md` (ground truth when
anything disagrees). No PRD yet — once `PRD_ROADMAP.md` exists, its next open
task is the default work.

## Project identity
- Swing-trading bot: holds of days to a few weeks, small capital
  ($100–1,000 assumed — see HANDOFF Open decisions).
- Goal (Evan 2026-07-09): HIGH percent return, concentrated (K=1–3
  positions), losses explicitly accepted. Gates are return-centric with
  loosened-but-present drawdown ceilings. Risk appetite changes gate
  NUMBERS, never rigor DISCIPLINE (prereg before results; no tuning a FAIL).
- SEPARATE from `D:\ClaudeCode\Trading`. Never modify that repo from this
  project without Evan's explicit instruction. Never run backtests
  concurrently against Trading's DB.

## Doc cadence (wired 2026-07-08, defaults — soft, self-enforced)
- Record entry (/project-memory §2): every 3 prompts of real work.
- Handoff (§3): session end.
- PRD next-task (§4): on request; default idle action once a PRD exists.
- Codebase-memory bins (§5): same session as any fact-changing change.
- Misses are logged in the record, not hidden.

## Definition of done (additive to global standards)
- No test suite exists yet (2026-07-08). Once a backtest engine lands, port
  Trading's frozen-regression-test pattern and make it a required done-check
  here — pinned reference numbers, fail loud on drift.
- Any script that touches price data states its adjustment convention in a
  header comment (split-adjusted / dividend-UNadjusted if sourced from
  Trading's price_cache).

## Hard rules
- EOD data only: signal at close, execute next open. No intraday logic until
  an intraday data source exists.
- If reading Trading's `price_cache`: READ-ONLY from this project; honor
  split-adjusted / dividend-UNadjusted in every consumer.
- Liquidity floor is mandatory in any universe filter — at this capital size,
  spread/slippage dominate.
- `.bat` files pure ASCII (cmd.exe silently corrupts its parse otherwise).
- Never rewrite JSON data files with PowerShell; use Node/dedicated tools.
