# codebase-memory index — Swing Trading

- security.md — API-key handling for Alpaca/data sources; the native-git secret gate (`core.hooksPath` -> `scripts/git-hooks`) (updated 2026-08-18)
- performance.md — research-runner and tripwire runtimes, measured (updated 2026-09-05)
- architecture.md — relationship to the Trading repo; data-layer facts; where the liquidity floor and its enforcement live (updated 2026-09-05)
- features.md — the 3 live paper sleeves: e6_1x / e18_vixts / m10_1_nagel (updated 2026-08-13)
- conventions.md — doc system + code conventions; record-heading rules; the dated-exception pattern (updated 2026-09-05)
- gotchas.md — data traps inherited from Trading, plus traps this project measured itself; the "guard that cannot fire" family (updated 2026-09-05)
- disclosure.md — what may leave this project vs never; the repo is PUBLIC under Evan's real name since 2026-07-10 (created 2026-09-05, M13.7)
- DIRECTORY.md — the tree map: 208 tracked files, per-directory counts, every number grepped with the command recorded (created 2026-09-05, M13.7)

Standards bins (updated 2026-07-15; the committed choices, one home each):
- dependencies.md — Python 3.14.4, yfinance 1.5.1, httpx, pandas 3.0.x (bleeding-edge); pins in requirements.txt/.lock.
- ui.md — **N/A, no UI/UX** (headless bot).
- testing.md — `python -m swing_bot.test_frozen` must print GREEN (12 pinned refs at d=±0.0000pp + 17 invariants); plus FIVE standalone proofs, none needing network or DB: `prove_cache_guard` 8/8, `prove_refusal_gate` 10/10, `prove_liquidity_floor` 11/11 (was 6/6 before F3 — this line said 6/6 until 2026-09-05), `prove_feed_clock` 18/18, `prove_divergence_census` 16/16. A native pre-commit hook DOES run (secret scan + record invariants); no CI, no coverage tool. (updated 2026-09-05)
- data.md — own yfinance fetcher → swing.db `bars` (OHLCV), adjustment convention, EOD-only, Trading read-only, liquidity floor; AND the second store, `.e8e9_cache` + its freshness contract; AND the M3 paper ledger — `paper_nav` PK is (sleeve,date) and the sleeves have UNEQUAL series; AND the two price stores cover DIFFERENT WINDOWS. (updated 2026-09-05)
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
