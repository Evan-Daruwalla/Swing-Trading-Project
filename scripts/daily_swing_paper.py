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
    _, v3close, _ = series("^VIX3M", start="2015-01-01")

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
    for s, (target, err) in decisions.items():
        if target is None:
            continue
        positions = set(ps.get_positions(conn, s))
        if set(target) != positions:
            ps.set_pending(conn, s, target, today)

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
        # Alpaca paper account. For each sleeve with a NEW pending target,
        # reconcile the account: close held symbols not in the target (market
        # liquidation, queues for next open after hours), then buy each target
        # symbol not already held as a MARKET NOTIONAL DAY order (notional+limit
        # is rejected by Alpaca; market-notional-DAY queues for next open and
        # satisfies the DAY-TIF rule). UNVERIFIED against real fills until a
        # live cycle runs -- fill_divergence logs the order ids for audit.
        from swing_bot.alpaca_client import client_for_sleeve, AlpacaError
        import json
        for s in ps.SLEEVES:
            st = ps.get_sleeve(conn, s)
            pending = json.loads(st["pending_json"]) if st["pending_json"] else None
            if not pending and pending != {}:
                print(f"\n--execute [{s}]: no new pending decision today -- nothing to mirror.")
                continue
            try:
                client = client_for_sleeve(s)
            except AlpacaError as e:
                print(f"\n--execute [{s}]: SKIPPED (creds): {e}")
                continue
            try:
                nav = mark_nav(conn, s, today, close_px)
                held = {p["symbol"]: p for p in client.list_positions()}
                target_syms = set(pending)
                print(f"\n--execute [{s}]: Alpaca PAPER {client.base_url}  NAV=${nav:,.2f}  "
                      f"held={sorted(held)}  target={sorted(target_syms)}")
                client.cancel_all_orders()
                for sym in held:                       # flatten what's not wanted
                    if sym not in target_syms:
                        try:
                            client.close_position(sym)
                            print(f"    CLOSE {sym}")
                        except AlpacaError as e:
                            print(f"    close {sym} FAILED: {e}")
                for t, w in pending.items():            # enter new target legs
                    if t in held:
                        print(f"    hold {t} (already held; not re-buying)")
                        continue
                    notional = round(nav * w, 2)
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
