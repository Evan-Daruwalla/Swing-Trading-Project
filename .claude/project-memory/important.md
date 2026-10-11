# important - Swing Trading

> Critical facts: getting one wrong is irreversible or expensive, invalidates
> results, or breaks a live external constraint. Numbered, dated, newest last.
> CLAUDE.md wins on conflict. Never remove an entry without telling Evan.
> Keep entries short; detail lives in the topic bin. ASCII only.
> Created 2026-09-30 from CLAUDE.md, HANDOFF.md and the bins (Skills record EA follow-up).

## 1. Never run the paper loop yourself (2026-09-30)
**What:** re-running the loop places Alpaca PAPER orders. Never run `scripts/daily_swing_paper.py` or any `.bat` yourself; never fire `SwingTradingDailyPaper` manually intraday.
**Constrains:** the DB ledger advances on ANY run, even when the market-open guard blocks the order.
**Why:** a manual intraday run caused the 2026-07-20 round-trip and the e18 fork.
**Source:** HANDOFF M3 block ("Do NOT fire it manually intraday") and the handoff prompt's HARD CONSTRAINTS; detail in operations.md (when migrated). (HANDOFF line numbers replaced by section names 2026-10-04, record GW: they drift with every HANDOFF edit.)

## 2. Frozen tests after any change to swing_bot/ or the paper script (2026-09-30)
**What:** `.venv\Scripts\python.exe -m swing_bot.test_frozen` must print `FROZEN TESTS: GREEN (all d=0)` (12 pinned refs + 22 invariants).
**Constrains:** it is the REQUIRED done-check; paste the real output.
**Why:** it is the tripwire that keeps live code equal to tested code.
**Source:** CLAUDE.md:49-54; detail in testing.md.

## 3. Rigor is fixed: preregister before results, never tune a FAIL (2026-09-30)
**What:** risk appetite changes gate NUMBERS, never the discipline. The search phase is closed (37 attempts).
**Constrains:** any new strategy test needs a `docs/prereg_*.md` written before its results.
**Why:** tuning after the fact invalidates every result in the program.
**Source:** CLAUDE.md:14-15; HANDOFF "Current state" section (37 vs 38; search phase closed).

## 4. STRESS_K = 4 is a dated exception - do not "fix" it (2026-09-30)
**What:** `swing_bot/paper_sleeves.py:43` sets `STRESS_K = 4` for the M10-1 stress branch only; e6_1x and e18_vixts stay K=1.
**Constrains:** moving it to K=3 needs a fresh prereg whose gates pass.
**Why:** K=4 is the parameter the backtests ran; K=3 would be a rule no backtest has tested.
**Source:** CLAUDE.md:16-28.

## 5. Trading is a separate project - read-only from here (2026-09-30)
**What:** never modify `D:\ClaudeCode\Trading` or its DB from this project without Evan's explicit instruction; never run backtests concurrently against Trading's DB; honor split-adjusted / dividend-UNadjusted when reading its `price_cache`.
**Constrains:** every consumer of Trading's data.
**Why:** a write or a concurrent run corrupts the other project's live state.
**Source:** CLAUDE.md:29-31, 60-63.

## 6. NAV holes are permanent - never backfill or "fix" them (2026-09-30)
**What:** the acknowledged holes (2026-07-30 x3; e6_1x 08-25..08-31) stay holes (Evan, 2026-09-05). The 30 rows backfilled for 09-08..09-22 (27 on 2026-09-22, record GP; the 3 for 09-22 on 2026-10-04, record GU) must be excluded from uptime metrics. They were backfilled only because each was proven exact (ledger frozen, every rule said HOLD, formula reproduced every live row); that is the bar for any future backfill.
**Constrains:** any NAV repair or uptime number.
**Why:** a silent backfill is a fabricated track record.
**Source:** data.md:57-63, 125-132.

## 7. Public repo under Evan's real name (2026-09-30)
**What:** the repo is public as a college-application portfolio piece. Never commit `alpaca_keys.env` (3 PAPER key pairs), `swing.db` or `var/`. Evan alone pushes; no Co-Authored-By.
**Constrains:** every commit; nothing may imply live trading.
**Why:** public history is permanent.
**Source:** disclosure.md:10, 21-26; CLAUDE.md:69; detail in disclosure.md.

## 8. The record holds Evan's personal email - no record commit until it is redacted (2026-09-30)
**What:** Appendix GJ has the address on one line of the .md and one of the .html; HEAD has none. Evan's chosen fix (2026-09-11): relaunch with PM_RECORD_UNLOCK=1, replace it with [redacted], re-render the twin, confirm 0 hits in both.
**Constrains:** only then may a commit include the record.
**Why:** the record ships in this PUBLIC repo.
**Source:** HANDOFF handoff prompt, BLOCKED-ON-EVAN item 1; disclosure.md:79-85.
**RESOLVED 2026-10-11 (record GZ):** GJ's email and GN's quoted account path replaced with [redacted]; 0 case-insensitive hits in .md and .html; the record may be committed again. The rule that remains: grep every staged record diff for emails and absolute user paths (disclosure.md). Still public: `docs/prereg_e10_earnings_drift.md:9` (account path in HEAD since 129dc22).

## 9. The 23:45 CT schedule: 13 of 14 nights passed the feed clock (2026-09-30; updated 2026-10-11)
**What:** `SwingTradingDailyPaper` moved 19:00 -> 23:45 CT Mon-Fri on 2026-09-22 (record GO). The first 23:45 run (09-22) still saw the NaN and refused; all 13 runs 09-23..10-09 passed the feed clock (records GT, GU, GX). 09-23..10-02 still exited 1 on the missed-session check until the 09-22 backfill; 10-05..10-09 all ended `exit code 0`.
**Constrains:** check `var/daily_swing_paper.log` for the line `REFUSING TO RUN -- price feed is BEHIND` (it said "FEED-CLOCK", text the log never prints, until 2026-10-04 - record GT HIGH 3) and that `paper_nav` has rows for all three sleeves. Since the 09-22 backfill a clean night ends `exit code 0`.
**Why:** the feed-clock guard has no override on purpose; a wrong start time silently skips days.
**Source:** HANDOFF top blocks (records GO, GU); gotchas.md (feed clock).
