"""M3 forward-paper daily loop, per PRD M3 (task 14, adapted 2026-07-15 from
the stale e1_control/e1_llm_veto framing -- E1 FAILED and was shelved months
ago -- to the 3 real forward-paper candidates: E6-1x, E18-VIXTS, M10-1 Nagel
Switch. See docs/research/2026-07-15_M3_forward_paper_setup.md.

Run ONCE DAILY, any time after that day's US-market close (yfinance publishes
it ~4:30pm ET onward). Each run:
  1. Fetches TODAY's fresh bars (QQQ + VIX/VIX3M always; the 39-name survivor
     universe only when a new M10-1 weekly decision is actually being made).
  2. For each of the 3 sleeves: REALIZES any pending order from the PREVIOUS
     run (signal decided at the prior close, filled at TODAY's now-known
     open) -> then COMPUTES today's new signal and stores it as pending for
     tomorrow. This one-day-lag pattern needs only a single daily invocation
     and mirrors every backtest runner's own next-open timing exactly (EOD
     hard rule; PRD CONSTRAINTS -- no intraday logic).
  3. Records NAV for every sleeve in swing.db (paper_nav) regardless of
     Alpaca connectivity -- this DB-simulated ledger IS the forward-paper
     evidence, independent of whether any sleeve is broker-mirrored.
  4. DRY-RUN by default: prints hand-checkable per-sleeve state/orders, no
     network order calls. --execute additionally mirrors EACH sleeve to its
     OWN dedicated Alpaca PAPER account (3-account model, Evan 2026-07-15 --
     $1,000 each, fully isolated order flow), using that sleeve's own key pair
     from alpaca_keys.env (client_for_sleeve). Orders are sized to the sleeve's
     own DB NAV (notional, matches the DB ledger 1:1).

Order timing (disclosed, unverified until a real cycle runs): a mirrored order
is submitted THIS EVENING as a MARKET NOTIONAL DAY order (Alpaca rejects
notional+limit, so market-notional is the canonical fractional order; DAY-TIF
per PRD CONSTRAINTS), intended to fill at TOMORROW's open when Alpaca's session
opens. Whether Alpaca queues an after-hours DAY order for the next session (vs
rejecting it) is confirmed only by the first live cycle; fill_divergence logs
the DB-sim price and the Alpaca order id so any gap is visible, never assumed.

DOES NOT touch swing.db's `bars` table's pinned rows or anything
test_frozen.py reads -- new tables only (paper_sleeves/paper_positions/
paper_transactions/paper_nav/fill_divergence), tripwire-safe by construction.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).

NAV (finding-things map): THE live daily orchestrator. Fired by the Windows
task `SwingTradingDailyPaper` via daily_swing_paper.bat (--execute), logging to
var/daily_swing_paper.log. Imports swing_bot.{prices, paper_sleeves as ps};
alpaca_client is used lazily in the --execute path. Per-sleeve SIGNAL logic
lives in ps.decide_* (swing_bot/paper_sleeves.py), NOT here; this file only
orchestrates fetch -> realize-pending -> decide -> record-NAV -> mirror. The
M10-1 weekly path also pulls `UNIV` <- run_e10_earnings_drift and
`residual_series, BETA_N` <- run_c1_residual_reversal.
"""
import argparse
import bisect
import datetime as dt
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from swing_bot import prices, paper_sleeves as ps
from run_e10_earnings_drift import UNIV
from run_c1_residual_reversal import residual_series, BETA_N

VIX_THR = 20.0
FF3_URL = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
           "F-F_Research_Data_Factors_daily_CSV.zip")


def isoweek_str(d):
    y, m, dd = map(int, d.split("-"))
    iso = dt.date(y, m, dd).isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def fresh_ff3():
    """Always-fresh Ken French daily-factor fetch for live use -- deliberately
    NOT run_c1_residual_reversal.ff3_daily(), which caches permanently
    (correct for a frozen backtest, wrong for a live weekly rebalance)."""
    req = urllib.request.Request(FF3_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        z = zipfile.ZipFile(io.BytesIO(r.read()))
    txt = z.read(z.namelist()[0]).decode("latin-1")
    out = {}
    for line in txt.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 4 and len(parts[0]) == 8 and parts[0].isdigit():
            d = f"{parts[0][:4]}-{parts[0][4:6]}-{parts[0][6:]}"
            try:
                out[d] = [float(parts[1]) / 100, float(parts[2]) / 100, float(parts[3]) / 100]
            except ValueError:
                continue
    return out


def series(ticker, start="1999-01-01"):
    bars = prices.fetch(ticker, start=start)
    dates = [b[1] for b in bars]
    close = {b[1]: b[5] for b in bars}
    openp = {b[1]: b[2] for b in bars}
    return dates, close, openp


VIX3M_CBOE_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv"


def vix3m_close(start="2015-01-01"):
    """VIX3M close series {YYYY-MM-DD: close}. PRIMARY = CBOE's authoritative
    daily CSV (fresh through the latest session). Yahoo's ^VIX3M symbol lags
    ~a week (Yahoo stops updating the term-structure indices while ^VIX stays
    current) -- on 2026-07-17 that stale value INVERTED e18's live signal
    (record DC): stale 18.77/18.57=1.011 said CASH, fresh 18.77/20.54=0.914
    says HOLD. FALLBACK = yfinance ^VIX3M if CBOE is unreachable. The signal
    CONDITION (VIX/VIX3M<1) is unchanged -- this only swaps the live VENDOR
    for the freshest reading, same class of live-vs-backtest data
    accommodation as the VIX3M carry-forward. CBOE's VIX matches Yahoo's ^VIX
    exactly, so mixing CBOE-VIX3M with Yahoo-VIX is consistent."""
    try:
        r = httpx.get(VIX3M_CBOE_URL, timeout=20, follow_redirects=True)
        r.raise_for_status()
        out = {}
        for line in r.text.strip().splitlines()[1:]:      # skip DATE,OPEN,HIGH,LOW,CLOSE
            parts = line.split(",")
            if len(parts) < 5:
                continue
            m, d, y = parts[0].split("/")                  # CBOE date = MM/DD/YYYY
            iso = f"{y}-{int(m):02d}-{int(d):02d}"
            if iso >= start:
                out[iso] = float(parts[4])                 # CLOSE
        if out:
            return out
        print("  VIX3M CBOE returned no rows; falling back to yfinance ^VIX3M", flush=True)
    except Exception as e:
        print(f"  VIX3M CBOE fetch failed ({e}); falling back to yfinance ^VIX3M", flush=True)
    _, v3, _ = series("^VIX3M", start=start)
    return v3


def market_is_open():
    """Alpaca's authoritative market clock -> True/False, or None if it can't
    be determined (no usable creds / clock call failed). Used to gate --execute
    order submission to AFTER-HOURS only (record DF): a market-notional order
    placed while the market is OPEN fills intraday instead of queuing for the
    next open, breaking the EOD/execute-next-open rule and desyncing the ledger
    (record DE)."""
    from swing_bot.alpaca_client import client_for_sleeve, AlpacaError
    for s in ps.SLEEVES:
        try:
            c = client_for_sleeve(s)
        except AlpacaError:
            continue
        try:
            return bool(c.get_clock().get("is_open"))
        except AlpacaError:
            return None
        finally:
            c.close()
    return None


def realize_pending(conn, sleeve, today, fill_open):
    """fill_open: {ticker: open_price_today}. Liquidates every current
    position (sell at today's open), then buys into the sleeve's pending
    target (if any) with the resulting cash. Mirrors the backtest's
    liquidate-then-rebuild transition exactly. Returns True if a fill
    happened.

    GUARD (found by the first dry-run, 2026-07-15): only realize if `today`
    is STRICTLY AFTER the session that produced the pending signal. Without
    this, re-running the script on the same still-latest session (e.g. two
    manual invocations before a new trading day posts) fills the pending
    order against ITS OWN signal day's open instead of waiting for the next
    session -- one day too early, and non-idempotent."""
    st = ps.get_sleeve(conn, sleeve)
    if not st["pending_json"]:
        return False
    if st["pending_signal_date"] and today <= st["pending_signal_date"]:
        return False
    import json
    target = json.loads(st["pending_json"])
    positions = ps.get_positions(conn, sleeve)
    cash = st["cash"]
    for t, pos in positions.items():
        px = fill_open.get(t)
        if px is None or px <= 0:
            continue  # no bar today for this ticker -- leave held, retry next run
        cash += pos["qty"] * px
        ps.record_fill(conn, sleeve, today, t, "sell", pos["qty"], px, "pending-liquidate")
        ps.upsert_position(conn, sleeve, t, 0.0, px, today)
        ps.log_divergence(conn, sleeve, today, t, px)
    if target:
        per_ticker_cash = cash / len(target)
        for t, w in target.items():
            px = fill_open.get(t)
            if px is None or px <= 0:
                continue
            qty = per_ticker_cash / px
            cash -= qty * px
            ps.record_fill(conn, sleeve, today, t, "buy", qty, px, "pending-enter")
            ps.upsert_position(conn, sleeve, t, qty, px, today)
            ps.log_divergence(conn, sleeve, today, t, px)
    conn.execute("UPDATE paper_sleeves SET cash=? WHERE sleeve=?", (cash, sleeve))
    conn.commit()
    ps.clear_pending(conn, sleeve)
    return True


def mark_nav(conn, sleeve, today, close_px):
    """close_px: {ticker: close_price_today}."""
    st = ps.get_sleeve(conn, sleeve)
    positions = ps.get_positions(conn, sleeve)
    nav = st["cash"] + sum(p["qty"] * close_px.get(t, p["entry_price"])
                            for t, p in positions.items())
    ps.record_nav(conn, sleeve, today, nav)
    return nav


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true",
                     help="Mirror SWING_ALPACA_SLEEVE's new orders to Alpaca paper. "
                          "Default is dry-run (no network order calls).")
    args = ap.parse_args()

    for s in ps.SLEEVES:
        conn = ps.connect()
        ps.init_sleeve(conn, s)
        conn.close()

    print("Fetching QQQ + VIX/VIX3M ...", flush=True)
    qdates, qclose, qopen = series("QQQ")
    today = qdates[-1]
    print(f"  latest session: {today}")
    _, vclose, _ = series("^VIX", start="2015-01-01")
    v3close = vix3m_close(start="2015-01-01")   # CBOE-primary (Yahoo ^VIX3M lags, record DC)

    # Carry-forward the most-recent-available reading <= today (PAST-ONLY, no
    # look-ahead). Necessary live: yfinance's ^VIX3M feed lags ^VIX by 1-3
    # sessions, so an exact-date lookup on the newest session returns None and
    # e18_vixts would SKIP (silently under-trade). The E18 backtest aligned on
    # complete cached history where every date already has a VIX3M value;
    # carry-forward reproduces that "decide on the current term structure"
    # intent at the live edge. m10_1_nagel already reads VIX via this same
    # bisect carry-forward. Disclosed live-vs-backtest data-availability
    # accommodation -- the VIX/VIX3M<1 signal CONDITION is unchanged.
    def _asof(cmap, d):
        ks = sorted(cmap)
        i = bisect.bisect_right(ks, d) - 1
        return (ks[i], cmap[ks[i]]) if i >= 0 else (None, None)

    vix_dt, vix_today = _asof(vclose, today)
    v3_dt, vix3m_today = _asof(v3close, today)
    print(f"  VIX={vix_today} (asof {vix_dt})  VIX3M={vix3m_today} (asof {v3_dt})")

    conn = ps.connect()

    # ---- realize any pending from the previous run (needs today's opens for
    # whatever tickers are currently held / newly targeted) ----
    fill_open = dict(qopen)   # QQQ always available
    for s in ps.SLEEVES:
        st = ps.get_sleeve(conn, s)
        positions = ps.get_positions(conn, s)
        import json
        target = json.loads(st["pending_json"]) if st["pending_json"] else {}
        needed = set(positions) | set(target)
        for t in needed - set(fill_open):
            _, _, op = series(t, start="2024-01-01")
            fill_open[t] = op.get(today)
    fills = {}
    for s in ps.SLEEVES:
        fills[s] = realize_pending(conn, s, today, fill_open)

    # ---- decide today's new signal per sleeve ----
    decisions = {}
    target_e6, err = ps.decide_e6_1x(list(qclose[d] for d in qdates))
    decisions["e6_1x"] = (target_e6, err)
    target_e18, err = ps.decide_e18_vixts(vix_today, vix3m_today)
    decisions["e18_vixts"] = (target_e18, err)

    wk = isoweek_str(today)
    m10_st = ps.get_sleeve(conn, "m10_1_nagel")
    is_decision_day = (dt.date.fromisoformat(today).weekday() == 4
                       and m10_st["last_decided_week"] != wk)
    if is_decision_day:
        residual_ranks = None
        if vix_today is not None and vix_today > VIX_THR:
            print("Stress + weekly decision day: fetching 39-name universe + FF3 "
                  "for the residual ranking ...", flush=True)
            ff = fresh_ff3()
            ranks = []
            for t in UNIV:
                ds, cl, _ = series(t, start="2010-01-01")
                cls = [cl[d] for d in ds]
                form = residual_series(ds, cls, ff)
                v = dict(zip(ds, form)).get(today)
                if v is not None:
                    ranks.append((v, t))
            residual_ranks = sorted(ranks)
        target_m10, err = ps.decide_m10_1(vix_today, list(qclose[d] for d in qdates), residual_ranks)
        decisions["m10_1_nagel"] = (target_m10, err)
        conn.execute("UPDATE paper_sleeves SET last_decided_week=? WHERE sleeve='m10_1_nagel'", (wk,))
        conn.commit()
    else:
        decisions["m10_1_nagel"] = (None, f"not a decision day (week {wk} already "
                                          f"decided, or today is not Friday)")

    # ---- store new pending where the target differs from what's now held ----
    # If the target MATCHES current holdings, clear any stale pending: a prior
    # run may have queued a move (e.g. e18's cash SELL on a stale-VIX3M signal,
    # record DC) that this run's corrected signal reverses. Without the clear,
    # the reconcile mirror would still act on the dead pending. (2026-07-18)
    for s, (target, err) in decisions.items():
        if target is None:
            continue
        positions = set(ps.get_positions(conn, s))
        if set(target) != positions:
            ps.set_pending(conn, s, target, today)
        else:
            ps.clear_pending(conn, s)

    # ---- mark NAV + summarize ----
    close_px = dict(qclose)
    for s in ps.SLEEVES:
        needed = set(ps.get_positions(conn, s))
        for t in needed - set(close_px):
            _, cl, _ = series(t, start="2024-01-01")
            close_px[t] = cl.get(today)
    print(f"\n=== {today} - M3 forward-paper daily loop ({'EXECUTE' if args.execute else 'DRY-RUN'}) ===")
    for s in ps.SLEEVES:
        st = ps.get_sleeve(conn, s)
        positions = ps.get_positions(conn, s)
        nav = mark_nav(conn, s, today, close_px)
        target, err = decisions[s]
        held_str = ", ".join(f"{t}:{p['qty']:.3f}" for t, p in positions.items()) or "cash"
        print(f"\n  [{s}]")
        print(f"    filled-today: {fills[s]}   held: {held_str}   NAV: ${nav:,.2f}")
        if err:
            print(f"    today's decision: SKIPPED ({err})")
        elif target is not None:
            same = set(target) == set(positions)
            tgt_str = ", ".join(f"{t}:{w:.2f}" for t, w in target.items()) or "cash"
            print(f"    today's decision: target={tgt_str}  "
                  f"{'(unchanged)' if same else '(NEW pending -> next open)'}")
        ps.touch_run(conn, s)

    if args.execute:
        # THREE-ACCOUNT model (2026-07-15): every sleeve mirrors to its OWN
        # Alpaca paper account.
        #
        # RECONCILE-TO-DB (2026-07-17 footgun fix, record DA): each run drives
        # the Alpaca account toward the DB's AUTHORITATIVE desired holding --
        # the pending target if one is set (the new allocation that fills next
        # open), ELSE the sleeve's current DB positions (steady state). The old
        # code mirrored only a "new pending" and skipped otherwise; but a stray
        # dry-run (which still advances the DB ledger, by design) can REALIZE a
        # pending and clear it before any --execute ever mirrored it -> the DB
        # then holds a position Alpaca never got, and pending-only mirroring
        # can't see it. Reading DB STATE (positions|pending), not "a decision
        # happened this run", lets the account self-heal on the next --execute.
        # Close held symbols not wanted (market liquidation, queues next open
        # after hours); buy each wanted symbol not already held as a MARKET
        # NOTIONAL DAY order (notional+limit is rejected by Alpaca;
        # market-notional-DAY queues for next open, satisfies DAY-TIF).
        # UNVERIFIED against real fills until a live cycle runs -- fill_divergence
        # logs the order ids for audit.
        from swing_bot.alpaca_client import client_for_sleeve, AlpacaError
        import json
        # INTRADAY GUARD (record DF): only submit orders after-hours, so
        # market-notional DAY orders queue for the NEXT open (EOD rule). While
        # the market is OPEN a market order fills intraday -> discipline break +
        # DB/Alpaca desync (record DE). The DB ledger already advanced above and
        # is next-open disciplined on its own; the next after-hours run
        # reconciles Alpaca to it, so skipping order submission here is safe.
        mkt = market_is_open()
        if mkt:
            print("\n--execute: US MARKET IS OPEN -- SKIPPING all Alpaca order "
                  "submission to avoid intraday fills (EOD/execute-next-open rule). "
                  "Re-run after the close; the DB ledger stands and the next "
                  "after-hours run will reconcile the broker to it.")
        elif mkt is None:
            print("\n--execute: WARNING could not verify market state (Alpaca "
                  "clock unavailable) -- proceeding; ensure this is an "
                  "after-hours run.")
        for s in ps.SLEEVES:
            if mkt:
                break                      # market open -> place no orders (guard above)
            st = ps.get_sleeve(conn, s)
            pending = json.loads(st["pending_json"]) if st["pending_json"] else None
            positions = ps.get_positions(conn, s)
            nav = mark_nav(conn, s, today, close_px)
            # {symbol: notional$} the Alpaca account should hold. Pending has
            # explicit weights (nav*w); steady-state positions mirror their
            # current DB dollar exposure (qty*close).
            if pending is not None:
                desired = {t: round(nav * w, 2) for t, w in pending.items()}
            else:
                desired = {t: round(p["qty"] * close_px.get(t, 0.0), 2)
                           for t, p in positions.items()}
            desired = {t: n for t, n in desired.items() if n > 0}
            try:
                client = client_for_sleeve(s)
            except AlpacaError as e:
                print(f"\n--execute [{s}]: SKIPPED (creds): {e}")
                continue
            try:
                held = {p["symbol"]: p for p in client.list_positions()}
                target_syms = set(desired)
                if not target_syms and not held:
                    print(f"\n--execute [{s}]: Alpaca PAPER {client.base_url}  "
                          f"NAV=${nav:,.2f}  DB flat + Alpaca flat -- nothing to mirror.")
                    continue
                src = "pending" if pending is not None else "positions"
                print(f"\n--execute [{s}]: Alpaca PAPER {client.base_url}  NAV=${nav:,.2f}  "
                      f"held={sorted(held)}  target={sorted(target_syms)} (from DB {src})")
                client.cancel_all_orders()
                for sym in held:                       # flatten what's not wanted
                    if sym not in target_syms:
                        try:
                            client.close_position(sym)
                            print(f"    CLOSE {sym}")
                        except AlpacaError as e:
                            print(f"    close {sym} FAILED: {e}")
                for t, notional in desired.items():     # enter / repair wanted legs
                    if t in held:
                        print(f"    hold {t} (already held; not re-buying)")
                        continue
                    try:
                        o = client.submit_order(symbol=t, notional=notional, side="buy",
                                                type="market", time_in_force="day")
                        print(f"    BUY {t} ~${notional:.2f} -> order {o.get('id')}")
                        ps.log_divergence(conn, s, today, t, close_px.get(t, 0.0),
                                          alpaca_order_id=o.get("id"))
                    except AlpacaError as e:
                        print(f"    buy {t} FAILED: {e}")
            except AlpacaError as e:
                print(f"\n--execute [{s}]: connection failed: {e}")
            finally:
                client.close()

    conn.close()
    print("\nDone. Scheduled task 'SwingTradingDailyPaper' runs this daily on weekday "
          "evenings (7pm local, --execute). Log: var\\daily_swing_paper.log.")


if __name__ == "__main__":
    main()
