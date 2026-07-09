# security — Swing Trading

- 2026-07-08: Alpaca keys pattern inherited from Trading: keys live in a
  gitignored `alpaca_keys.env`, loaded by a no-dep loader
  (`trading_bot/execution/alpaca_accounts.py` there). If this project gets its
  own keys file, same rules: gitignored, never committed, never echoed to chat.
- 2026-07-08: Trading's `alpaca_client.py` hard-guards live trading via
  `is_live()` — any client ported here must keep that guard. PAPER base URL is
  the default; live is opt-in and currently out of scope entirely.
