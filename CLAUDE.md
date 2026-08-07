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
- TIMEZONE: record/doc timestamps in **Central time, DST-aware**. Run `date`
  before stamping and label the zone by its UTC offset — **UTC-6 → CST,
  UTC-5 → CDT** — never estimate or hardcode one. The /project-memory cadence
  hook reports UTC (Z); prefer running `date` over hand-converting, but if you
  do convert, subtract the current offset (6h winter/CST, 5h summer/CDT; date
  rolls back if UTC time is before the offset). Set 2026-07-11 (record Appendix
  AZ) after earlier entries were mislabeled UTC-as-local; made DST-aware
  2026-07-19.

## Definition of done (additive to global standards)
- REQUIRED done-check: `.venv\Scripts\python.exe -m swing_bot.test_frozen`
  must print `FROZEN TESTS: GREEN (all d=0)` — 12 pinned refs at d=±0.0000pp
  + 16 invariants. Run after ANY change to `swing_bot/` or to
  `scripts/daily_swing_paper.py`. (This line said "no test suite exists yet"
  until 2026-08-06; the tripwire has been green since 2026-07-09. Corrected by
  audit #3. Detail in `.claude/codebase-memory/testing.md`.)
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
