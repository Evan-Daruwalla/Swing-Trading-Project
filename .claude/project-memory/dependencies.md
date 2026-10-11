# dependencies — Swing Trading

Last updated 2026-08-25 (finding 9). Canonical home; exact pins in
`requirements.txt` (direct, pinned 2026-07-08) + `requirements.lock` (full
transitive, `pip freeze`).

- Python **3.14.4** (`.venv`). pandas/numpy are BLEEDING-EDGE majors (pandas
  3.0.x) — if a pandas/numpy edge breaks a milestone, **revisit the Python
  version, don't code around it** (record Appendix E).
- `yfinance==1.5.1` (own price fetcher — see data.md), `httpx==0.28.1`.
- `pandas==3.0.3` / `numpy==2.5.1` — RE-PINNED 2026-08-16 (audit finding
  ST-2): both are DIRECT imports (`scripts/run_c1_residual_reversal.py`,
  `scripts/run_e10_earnings_drift.py`) that were previously pinned only in
  `requirements.lock`'s transitive freeze, so a clean-machine
  `pip install -r requirements.txt` would have resolved them to whatever's
  newest, straight into the pandas-3.0.x default-changing edge this file's
  header already warns about. Versions now match `requirements.lock`.
- `markdown==3.10.3` — direct import in `scripts/render_record_html.py:30`
  (renders the append-only record to a standalone HTML twin).
- pytest OPTIONAL — frozen-regression tests run via their own `__main__`
  (`swing_bot/test_frozen.py`), matching Trading's pattern (see testing.md).
- After any dependency change, re-pin `requirements.txt` and refresh the lock.

- Reviewed 2026-09-05 against `requirements.txt`: no change; no dependency added by F3 (stdlib only).

- 2026-10-04 (record GW, audit GT MED 12): **anyio 4.14.1 -> 4.14.2, urllib3 2.7.0 ->
  2.8.0, soupsieve 2.8.4 -> 2.9.0** in `requirements.lock` and `.venv`; pip 26.1.2 ->
  26.2.1 in `.venv` only (pip is not in the runtime lock). `pip-audit -r
  requirements.lock` went from 8 advisories in 3 packages to "No known
  vulnerabilities found". Gate before Monday's run: test_frozen GREEN, all 9
  proofs exit 0, `swing_bot.alpaca_client` imports, the harness stays ACCEPTED with
  identical numbers, and a read-only fetch of QQQ, ^VIX, VIX3M (CBOE) and FF3 works.
  Rollback = reinstall the three old pins.
