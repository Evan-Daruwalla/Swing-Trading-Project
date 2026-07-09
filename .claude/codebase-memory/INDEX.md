# codebase-memory index — Swing Trading

- security.md — API-key handling for Alpaca/data sources (updated 2026-07-08)
- performance.md — empty; no code yet (updated 2026-07-08)
- architecture.md — relationship to the Trading repo; data-layer facts (updated 2026-07-08)
- features.md — empty; no code yet (updated 2026-07-08)
- conventions.md — doc system + code conventions inherited at bootstrap (updated 2026-07-08)
- gotchas.md — data traps inherited from Trading that apply to any yfinance pipeline here (updated 2026-07-08)

Cross-bin invariants:
- Prices sourced from Trading's price_cache are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED.
- Trading's repo/DB is read-only from this project; no concurrent backtests against it.
- EOD data only: signal at close, execute next open.
