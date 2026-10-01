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
**Source:** HANDOFF.md:356-360, :597-598; detail in operations.md (when migrated).

## 2. Frozen tests after any change to swing_bot/ or the paper script (2026-09-30)
**What:** `.venv\Scripts\python.exe -m swing_bot.test_frozen` must print `FROZEN TESTS: GREEN (all d=0)` (12 pinned refs + 22 invariants).
**Constrains:** it is the REQUIRED done-check; paste the real output.
**Why:** it is the tripwire that keeps live code equal to tested code.
**Source:** CLAUDE.md:49-54; detail in testing.md.

## 3. Rigor is fixed: preregister before results, never tune a FAIL (2026-09-30)
**What:** risk appetite changes gate NUMBERS, never the discipline. The search phase is closed (37 attempts).
**Constrains:** any new strategy test needs a `docs/prereg_*.md` written before its results.
**Why:** tuning after the fact invalidates every result in the program.
**Source:** CLAUDE.md:14-15; HANDOFF.md:15-37.

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
**What:** the acknowledged holes (2026-07-30 x3; e6_1x 08-25..08-31) stay holes (Evan, 2026-09-05). The 27 rows backfilled for 09-08..09-21 must be excluded from uptime metrics.
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
**Source:** HANDOFF.md:599-603; disclosure.md:79-85.

## 9. Open: the 23:45 CT schedule fix is APPLIED, NOT VERIFIED (2026-09-30)
**What:** `SwingTradingDailyPaper` moved 19:00 -> 23:45 CT Mon-Fri on 2026-09-22 (record GO).
**Constrains:** check `var/daily_swing_paper.log` for FEED-CLOCK refusals and that `paper_nav` has rows for all three sleeves before trusting it.
**Why:** the feed-clock guard has no override on purpose; a wrong start time silently skips days.
**Source:** HANDOFF.md:45-58; gotchas.md (feed clock).
