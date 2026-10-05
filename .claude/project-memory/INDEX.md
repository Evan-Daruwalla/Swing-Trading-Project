# project-memory index — Swing Trading

Read first: important.md - critical facts, injected by the important-inject hook (added 2026-09-30)

New standard bins (2026-09-30; first line STATUS: = stub, see that line): decisions, people, timeline, glossary, compliance, budget, operations, services, experiments, writing, hardware, important

- security.md — API-key handling for Alpaca/data sources; the native-git secret gate (`core.hooksPath` -> `scripts/git-hooks`; fails CLOSED since 2026-09-09) (updated 2026-09-10)
- performance.md — research-runner and tripwire runtimes, measured (updated 2026-09-10)
- architecture.md — relationship to the Trading repo; data-layer facts; where the liquidity floor and its enforcement live; the calendar's range enumerator and derived ad-hoc closures (updated 2026-09-10)
- features.md — the 3 live paper sleeves: e6_1x / e18_vixts / m10_1_nagel (updated 2026-08-13)
- conventions.md — doc system + code conventions; record-heading rules; the dated-exception pattern (updated 2026-09-05)
- gotchas.md — data traps inherited from Trading, plus traps this project measured itself; the "guard that cannot fire" family; the vendor's 19:00 NaN-revision window; the 23:45 CT = next-day-ET trap (updated 2026-09-22)
- disclosure.md — what may leave this project vs never; the repo is PUBLIC under Evan's real name since 2026-07-10; grep record diffs for personal identifiers before committing (created 2026-09-05, M13.7; updated 2026-09-10)
- DIRECTORY.md — the tree map: 208 tracked files, per-directory counts, every number grepped with the command recorded (created 2026-09-05, M13.7)

Standards bins (updated 2026-07-15; the committed choices, one home each):
- dependencies.md — Python 3.14.4, yfinance 1.5.1, httpx, pandas 3.0.x (bleeding-edge); pins in requirements.txt/.lock.
- ui.md — **N/A, no UI/UX** (headless bot).
- testing.md — `python -m swing_bot.test_frozen` must print GREEN (12 pinned refs at d=±0.0000pp + 22 invariants; 17 until 2026-09-06, 19 until 2026-09-09); plus EIGHT standalone proofs, none needing network or the live DB: `prove_cache_guard` 8/8, `prove_refusal_gate` 10/10, `prove_liquidity_floor` 11/11 (was 6/6 before F3 — this line said 6/6 until 2026-09-05), `prove_feed_clock` 18/18, `prove_divergence_census` 16/16, `prove_torn_write` 32 (added 2026-09-06, audit FX MED 4), `prove_fetch_trailing_nan` 5/5 and `prove_session_gap` 8/8 (added 2026-09-09, audit GJ; 8th case, Juneteenth, 2026-09-11), `prove_loop_guards` 10/10 (added 2026-10-04, record GU). A native pre-commit hook DOES run (secret scan + record invariants); no CI, no coverage tool. (updated 2026-09-11)
- data.md — own yfinance fetcher → swing.db `bars` (OHLCV), adjustment convention, EOD-only, Trading read-only, liquidity floor; AND the second store, `.e8e9_cache` + its freshness contract; AND the M3 paper ledger — `paper_nav` PK is (sleeve,date) and the sleeves have UNEQUAL series; AND the two price stores cover DIFFERENT WINDOWS; AND `prices.fetch` retries a NaN-tailed frame, which does NOT recover the 19:00 revision; AND 27 backfilled paper_nav rows that uptime metrics must exclude. (updated 2026-09-22)
- tooling.md — .venv, Trading-DB read-only access pattern, .bat ASCII, DST-aware Central timestamp rule, research-cache env knobs. (updated 2026-08-13)

Cross-bin invariants:
- Prices sourced from Trading's price_cache are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED.
- The two price stores have different windows: swing.db bars 2014-01-02..2026-07-08; .e8e9_cache 1998-12-22..2026-08-17. Never compare a result from one against the other.
- The liquidity floor is enforced in the research runners as of 2026-09-05 (F3); SWING_F3_FLOOR=0 selects the pre-F3 path.
- Trading's repo/DB is read-only from this project; no concurrent backtests against it.
- EOD data only: signal at close, execute next open.
- `paper_nav` sleeves have UNEQUAL NAV series (e6_1x 31 vs peers 36, 2026-09-05) — never compare across sleeves without aligning on dates.
- ~~Missing bins: `disclosure.md` and `DIRECTORY.md` were never created at bootstrap (noted 2026-09-05)~~ — **both created 2026-09-05 (M13.7, record FV).**
- The repo is PUBLIC (github.com/Evan-Daruwalla/Swing-Trading-Project) — see `disclosure.md` before committing anything new.
