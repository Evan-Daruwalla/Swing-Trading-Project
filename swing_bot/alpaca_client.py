"""Thin Alpaca Trading API client (PAPER by default), ported from
D:\\ClaudeCode\\Trading\\trading_bot\\execution\\alpaca_client.py (read-only
reference; this is a fresh file, not an import — Trading's repo is never
modified from this project).

A small httpx wrapper, not the alpaca-py SDK: same rationale as Trading's
original — the Trading API is plain REST, so a ~200-line client keeps the
dependency surface flat and the behavior auditable.

THREE-ACCOUNT MODEL (Evan, 2026-07-15): each of the 3 forward-paper sleeves
has its OWN Alpaca paper account ($1,000 each), so their order flow is fully
isolated. Credentials live in `alpaca_keys.env` at the project root (gitignored
via `*_keys.env`), one KEY/SECRET pair per sleeve:
    e6_1x        -> E_SIX_KEY / E_SIX_SECRET
    e18_vixts    -> E_EIGHTEEN_VIX_TS_KEY / E_EIGHTEEN_VIX_TS_SECRET
    m10_1_nagel  -> M_TEN_ONE_KEY / M_TEN_ONE_SECRET
plus a shared APCA_API_BASE_URL (paper endpoint). Use `client_for_sleeve(name)`
to build the right client. NEVER hard-coded, NEVER committed.

The base URL is normalized to strip a trailing `/v2` (the request paths already
include `/v2/...`), so both `https://paper-api.alpaca.markets` and
`https://paper-api.alpaca.markets/v2` work. Nothing here can touch a LIVE
account: `submit_order` refuses to POST against the live host unless the caller
passes allow_live=True (nothing in this project does), on top of the paper
default. Notional (dollar-sized) orders are MARKET orders — Alpaca does not
accept notional+limit — submitted DAY-TIF, so they queue for the next open when
sent after hours (the project's signal-at-close/execute-next-open rule).

NAV (finding-things map): the broker mirror. Imported only by
scripts/daily_swing_paper (the --execute path). Entry point:
`client_for_sleeve(name)` -> AlpacaClient bound to that sleeve's key pair;
then `.submit_order(...)` / `.close_position(...)` / `.cancel_all_orders()`.
Signal logic is NOT here — it lives in swing_bot.paper_sleeves.decide_*.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

log = logging.getLogger(__name__)

PAPER_BASE_URL = "https://paper-api.alpaca.markets"
LIVE_BASE_URL = "https://api.alpaca.markets"
KEYS_FILE = Path(__file__).resolve().parent.parent / "alpaca_keys.env"
REQUEST_ID_LOG = Path(__file__).resolve().parent.parent / "var" / "alpaca_request_ids.log"

# sleeve name -> env-var prefix for its {PREFIX}_KEY / {PREFIX}_SECRET pair
SLEEVE_ENV_PREFIX = {
    "e6_1x": "E_SIX",
    "e18_vixts": "E_EIGHTEEN_VIX_TS",
    "m10_1_nagel": "M_TEN_ONE",
}


def _load_keys_file(path: Path = KEYS_FILE) -> dict:
    """Parse a simple KEY=VALUE-per-line file. '#' starts a comment only at the
    start of a stripped line, so secrets are never truncated. Trailing
    whitespace on a value is stripped (Alpaca secrets have no leading/trailing
    spaces). Missing file -> {} (caller falls back to os.environ)."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _normalize_base(url: str) -> str:
    url = url.strip().rstrip("/")
    if url.endswith("/v2"):
        url = url[:-3]
    return url


class AlpacaError(RuntimeError):
    """Non-2xx response from the Trading API. Carries status + request id so a
    support ticket can quote the X-Request-ID Alpaca asks for."""

    def __init__(self, status: int, request_id: str | None, body: str):
        self.status = status
        self.request_id = request_id
        self.body = body
        super().__init__(f"Alpaca {status} (X-Request-ID={request_id}): {body}")


class AlpacaClient:
    def __init__(self, *, base_url: str | None = None,
                 key_id: str | None = None, secret_key: str | None = None,
                 timeout: float = 15.0):
        env = _load_keys_file()
        raw_base = (base_url or env.get("APCA_API_BASE_URL")
                    or os.environ.get("APCA_API_BASE_URL") or PAPER_BASE_URL)
        self.base_url = _normalize_base(raw_base)
        self._key = key_id or env.get("APCA_API_KEY_ID") or os.environ.get("APCA_API_KEY_ID")
        self._secret = (secret_key or env.get("APCA_API_SECRET_KEY")
                        or os.environ.get("APCA_API_SECRET_KEY"))
        if not self._key or not self._secret:
            raise AlpacaError(
                0, None,
                f"Missing credentials. Paste paper keys into {KEYS_FILE} "
                f"(per-sleeve KEY/SECRET pairs) — see client_for_sleeve().")
        self._client = httpx.Client(
            base_url=self.base_url, timeout=timeout,
            headers={"APCA-API-KEY-ID": self._key,
                     "APCA-API-SECRET-KEY": self._secret})

    @property
    def is_live(self) -> bool:
        return self.base_url == LIVE_BASE_URL

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "AlpacaClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # ---- core request + X-Request-ID persistence ----
    def _request(self, method: str, path: str, **kw) -> Any:
        resp = self._client.request(method, path, **kw)
        rid = resp.headers.get("X-Request-ID")
        self._persist_request_id(method, path, resp.status_code, rid)
        if resp.status_code >= 400:
            raise AlpacaError(resp.status_code, rid, resp.text)
        return resp.json() if resp.content else None

    def _persist_request_id(self, method: str, path: str,
                            status: int, rid: str | None) -> None:
        line = (f"{datetime.now(timezone.utc).isoformat()} {method} {path} "
                f"-> {status} X-Request-ID={rid}")
        log.info(line)
        try:
            REQUEST_ID_LOG.parent.mkdir(parents=True, exist_ok=True)
            with REQUEST_ID_LOG.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError:
            pass  # logging the id is best-effort; never break a call over it

    # ---- read endpoints ----
    def get_account(self) -> dict:
        return self._request("GET", "/v2/account")

    def list_positions(self) -> list[dict]:
        return self._request("GET", "/v2/positions") or []

    def get_position(self, symbol: str) -> dict | None:
        try:
            return self._request("GET", f"/v2/positions/{symbol}")
        except AlpacaError as e:
            if e.status == 404:
                return None
            raise

    def get_asset(self, symbol: str) -> dict:
        return self._request("GET", f"/v2/assets/{symbol}")

    def list_orders(self, *, status: str = "open", limit: int = 100) -> list[dict]:
        return self._request("GET", "/v2/orders",
                             params={"status": status, "limit": limit}) or []

    # ---- order entry / management (caller-driven; paper via base_url) ----
    def submit_order(self, *, symbol: str, qty: float | None = None,
                     notional: float | None = None, side: str = "buy",
                     type: str = "market", time_in_force: str = "day",
                     allow_live: bool = False, **extra) -> dict:
        """Submit an order. Exactly one of qty / notional must be given. Note:
        NOTIONAL orders must be type='market' (Alpaca rejects notional+limit).
        Refuses a live base_url unless allow_live=True (nothing here passes it)."""
        if (qty is None) == (notional is None):
            raise ValueError("Pass exactly one of qty= or notional=.")
        if notional is not None and type != "market":
            raise ValueError("Notional orders must be type='market' (Alpaca constraint).")
        if self.is_live and not allow_live:
            raise AlpacaError(
                0, None,
                "Refusing to submit: base_url is LIVE and allow_live=False. "
                "This project's scope guard is paper-only — see CLAUDE.md.")
        body: dict[str, Any] = {"symbol": symbol, "side": side, "type": type,
                                "time_in_force": time_in_force, **extra}
        if qty is not None:
            body["qty"] = str(qty)
        else:
            body["notional"] = str(notional)
        return self._request("POST", "/v2/orders", json=body)

    def close_position(self, symbol: str) -> dict | None:
        """Liquidate an open position (market order). 404 if none held."""
        try:
            return self._request("DELETE", f"/v2/positions/{symbol}")
        except AlpacaError as e:
            if e.status == 404:
                return None
            raise

    def cancel_all_orders(self) -> None:
        try:
            self._request("DELETE", "/v2/orders")
        except AlpacaError:
            pass  # nothing open / already flat — non-fatal

    def cancel_order(self, order_id: str) -> None:
        self._request("DELETE", f"/v2/orders/{order_id}")


def client_for_sleeve(sleeve: str, env: dict | None = None,
                      timeout: float = 15.0) -> "AlpacaClient":
    """Build the AlpacaClient for one sleeve from its dedicated key pair in
    alpaca_keys.env (3-account model). Raises AlpacaError if the pair is
    missing so the daily loop can skip that sleeve with a clear message."""
    env = env if env is not None else _load_keys_file()
    prefix = SLEEVE_ENV_PREFIX.get(sleeve)
    if not prefix:
        raise AlpacaError(0, None, f"No env-prefix mapping for sleeve {sleeve!r}")
    key = env.get(f"{prefix}_KEY")
    secret = env.get(f"{prefix}_SECRET")
    if not key or not secret:
        raise AlpacaError(
            0, None,
            f"Missing {prefix}_KEY / {prefix}_SECRET in {KEYS_FILE.name} "
            f"for sleeve {sleeve!r}.")
    base = env.get("APCA_API_BASE_URL") or PAPER_BASE_URL
    return AlpacaClient(base_url=base, key_id=key, secret_key=secret, timeout=timeout)


def _smoke_test() -> int:
    """Connectivity check across ALL 3 sleeve accounts: GET /v2/account each.
    Turns a 403 into a per-sleeve status line once keys are pasted into
    alpaca_keys.env. Run:
      .venv\\Scripts\\python.exe -m swing_bot.alpaca_client
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    env = _load_keys_file()
    rc = 0
    for sleeve in SLEEVE_ENV_PREFIX:
        try:
            client = client_for_sleeve(sleeve, env)
        except AlpacaError as e:
            print(f"[{sleeve}] config error: {e}")
            rc = 2
            continue
        tag = "LIVE" if client.is_live else "PAPER"
        try:
            acct = client.get_account()
            print(f"[{sleeve}] {client.base_url} ({tag})  CONNECTED  "
                  f"acct#={acct.get('account_number')} status={acct.get('status')} "
                  f"cash=${acct.get('cash')} portfolio_value=${acct.get('portfolio_value')}")
        except AlpacaError as e:
            print(f"[{sleeve}] {client.base_url} ({tag})  FAILED: {e}")
            rc = rc or 1
        finally:
            client.close()
    print("\n(403 = bad/empty keys for that sleeve; a status line = connected.)")
    return rc


if __name__ == "__main__":
    raise SystemExit(_smoke_test())
