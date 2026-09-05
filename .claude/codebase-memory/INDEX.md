# codebase-memory index — Swing Trading

- security.md — API-key handling for Alpaca/data sources; the native-git secret gate (`core.hooksPath` -> `scripts/git-hooks`) (updated 2026-08-18)
- performance.md — empty; no runtime facts measured yet (updated 2026-08-13)
- architecture.md — relationship to the Trading repo; data-layer facts (updated 2026-07-08)
- features.md — the 3 live paper sleeves: e6_1x / e18_vixts / m10_1_nagel (updated 2026-08-13)
- conventions.md — doc system + code conventions; record-heading rules; the dated-exception pattern (updated 2026-09-05)
- gotchas.md — data traps inherited from Trading, plus traps this project measured itself; the "guard that cannot fire" family (updated 2026-09-05)

Standards bins (updated 2026-07-15; the committed choices, one home each):
- dependencies.md — Python 3.14.4, yfinance 1.5.1, httpx, pandas 3.0.x (bleeding-edge); pins in requirements.txt/.lock.
- ui.md — **N/A, no UI/UX** (headless bot).
- testing.md — `python -m swing_bot.test_frozen` must print GREEN (12 pinned refs at d=±0.0000pp + 17 invariants); plus the standalone `scripts/prove_cache_guard.py` (8/8) and `scripts/prove_liquidity_floor.py` (6/6). A native pre-commit hook DOES run (secret scan + record invariants); no CI, no coverage tool. (updated 2026-09-05)
- data.md — own yfinance fetcher → swing.db `bars` (OHLCV), adjustment convention, EOD-only, Trading read-only, liquidity floor; AND the second store, `.e8e9_cache` + its freshness contract; AND the M3 paper ledger — `paper_nav` PK is (sleeve,date) and the sleeves have UNEQUAL series. (updated 2026-09-05)
- tooling.md — .venv, Trading-DB read-only access pattern, .bat ASCII, DST-aware Central timestamp rule, research-cache env knobs. (updated 2026-08-13)

Cross-bin invariants:
- Prices sourced from Trading's price_cache are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED.
- Trading's repo/DB is read-only from this project; no concurrent backtests against it.
- EOD data only: signal at close, execute next open.
- `paper_nav` sleeves have UNEQUAL NAV series (e6_1x 31 vs peers 36, 2026-09-05) — never compare across sleeves without aligning on dates.
- Missing bins: `disclosure.md` and `DIRECTORY.md` were never created at bootstrap (noted 2026-09-05).
