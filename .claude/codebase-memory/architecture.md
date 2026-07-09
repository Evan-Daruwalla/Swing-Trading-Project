# architecture — Swing Trading

- 2026-07-08: This project is SEPARATE from `D:\ClaudeCode\Trading` (Evan's
  decision 2026-07-08). Trading's repo and DB are read-only from here; never
  run backtests concurrently against Trading's DB.
- 2026-07-08 (M0.2, supersedes the earlier "OPEN — read price_cache read-only"
  entry): Data layer DECIDED = **own yfinance fetcher**, NOT price_cache
  reuse. `swing_bot/prices.py` fetches full OHLCV (`auto_adjust=False`) into
  `swing.db` table `bars` (PK ticker,date; open/high/low/close/adj_close/
  volume). Reason: Trading's `price_cache` (in `var/trades.db`) stores only
  `close`+`volume`+derived flags — NO high/low/open — so IBS is uncomputable
  from it; it also lacks DIA/IWM + all country ETFs and has zero `next_open`
  rows for ETFs. `swing.db` also holds positions/NAV/results (M3+).
- 2026-07-08: TOOLING — Grep/Glob tools do not reach `D:\ClaudeCode\Trading`
  (returns no matches despite files present). Access that repo's DB via
  venv-python sqlite (`file:...?mode=ro`) + PowerShell, not Grep/Glob.
  Trading DB path: `D:\ClaudeCode\Trading\var\trades.db`.
- 2026-07-08: Reuse targets identified (map, verify before use): Trading's
  `factor_backtest.py` harness, `paper_trader.py` DB schema (cadence-agnostic),
  `alpaca_client.py`/`alpaca_sync.py`/`fractionability.py` for the Alpaca
  PAPER mirror. NOT reusable: `paper_rebalance.py` monthly buy-top-N logic,
  the long-horizon factor set.
