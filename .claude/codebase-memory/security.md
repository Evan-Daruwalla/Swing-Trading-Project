# security — Swing Trading

- 2026-07-08: Alpaca keys pattern inherited from Trading: keys live in a
  gitignored `alpaca_keys.env`, loaded by a no-dep loader
  (`trading_bot/execution/alpaca_accounts.py` there). ~~If this project gets its
  own keys file~~ **it has one — see the 2026-08-18 bullet below**; same rules:
  gitignored, never committed, never echoed to chat.
- 2026-07-08: Trading's `alpaca_client.py` hard-guards live trading via
  `is_live()` — any client ported here must keep that guard. PAPER base URL is
  the default; live is opt-in and currently out of scope entirely.
- 2026-08-16 (record EV, ST-1; bin obligation met late — 2026-08-18, record EY):
  **this repo now has a secret gate on the native git path.** `core.hooksPath` is
  set to `scripts/git-hooks`, and `scripts/git-hooks/pre-commit` delegates to the
  canonical `~/.claude/skills/commit-gate/hooks/pre-commit`. Before this,
  `core.hooksPath` was unset and no `.git/hooks/pre-commit` existed, so a
  SHELL-made commit ran no scanner. Model-made commits were already gated by the
  PreToolUse hook at `~/.claude/settings.json` — so the pre-fix exposure was the
  shell path only, NOT "no scanner on any commit" as EV.2 stated (corrected in
  record EY). Verified live 2026-08-18: hook runs, delegates, exits 0.
- 2026-08-18: this project DOES have its own keys file — `alpaca_keys.env` at the
  repo root, three per-sleeve Alpaca PAPER key pairs, untracked and ignored via
  `.gitignore:18` (`*.env`), never tracked on any branch (`git log --all --
  alpaca_keys.env` is empty). Supersedes the conditional "If this project gets
  its own keys file" phrasing in the 2026-07-08 bullet above.

