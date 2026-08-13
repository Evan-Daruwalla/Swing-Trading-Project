# codebase-memory index — Swing Trading

- security.md — API-key handling for Alpaca/data sources (updated 2026-07-08)
- performance.md — empty; no runtime facts measured yet (updated 2026-08-13)
- architecture.md — relationship to the Trading repo; data-layer facts (updated 2026-07-08)
- features.md — the 3 live paper sleeves: e6_1x / e18_vixts / m10_1_nagel (updated 2026-08-13)
- conventions.md — doc system + code conventions inherited at bootstrap (updated 2026-07-08)
- gotchas.md — data traps inherited from Trading, plus traps this project measured itself (updated 2026-08-13)

Standards bins (updated 2026-07-15; the committed choices, one home each):
- dependencies.md — Python 3.14.4, yfinance 1.5.1, httpx, pandas 3.0.x (bleeding-edge); pins in requirements.txt/.lock.
- ui.md — **N/A, no UI/UX** (headless bot).
- testing.md — `python -m swing_bot.test_frozen` must print GREEN (12 pinned refs at d=±0.0000pp + 17 invariants); plus the standalone `scripts/prove_cache_guard.py`. No CI, no coverage tool, run by hand. (updated 2026-08-13)
- data.md — own yfinance fetcher → swing.db `bars` (OHLCV), adjustment convention, EOD-only, Trading read-only, liquidity floor; AND the second store, `.e8e9_cache` + its freshness contract. (updated 2026-08-13)
- tooling.md — .venv, Trading-DB read-only access pattern, .bat ASCII, DST-aware Central timestamp rule, research-cache env knobs. (updated 2026-08-13)

Cross-bin invariants:
- Prices sourced from Trading's price_cache are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED.
- Trading's repo/DB is read-only from this project; no concurrent backtests against it.
- EOD data only: signal at close, execute next open.
