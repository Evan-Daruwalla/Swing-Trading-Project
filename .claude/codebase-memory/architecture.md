# architecture — Swing Trading

- 2026-07-08: This project is SEPARATE from `D:\ClaudeCode\Trading` (Evan's
  decision 2026-07-08). Trading's repo and DB are read-only from here; never
  run backtests concurrently against Trading's DB.
- 2026-07-08: Data-layer decision OPEN — recommended shape is: read Trading's
  `price_cache` read-only for prices, keep this project's own SQLite DB for
  positions/NAV/results. Not yet decided by Evan.
- 2026-07-08: Reuse targets identified (map, verify before use): Trading's
  `factor_backtest.py` harness, `paper_trader.py` DB schema (cadence-agnostic),
  `alpaca_client.py`/`alpaca_sync.py`/`fractionability.py` for the Alpaca
  PAPER mirror. NOT reusable: `paper_rebalance.py` monthly buy-top-N logic,
  the long-horizon factor set.
