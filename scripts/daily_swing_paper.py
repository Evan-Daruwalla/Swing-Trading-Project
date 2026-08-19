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
from zoneinfo import ZoneInfo

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from swing_bot import prices, paper_sleeves as ps, universe
from run_e10_earnings_drift import UNIV
from run_c1_residual_reversal import residual_series, BETA_N

VIX_THR = ps.VIX_STRESS_THR   # single source of truth (audit #6) -- see paper_sleeves

# Anything that should make this RUN report failure appends a line here; main()
# returns 1 when it is non-empty and the .bat propagates that via exit /b
# (audit #4 F4). Until 2026-08-11 every failure -- the missed-session banner,
# a partial realize, a dead sleeve -- was printed to a log nothing reads while
# Task Scheduler showed Last Result 0. A warning the exit path cannot see is
# not a warning.
RUN_FAILURES: list[str] = []

# Marks a decision-skip that is ORDINARY OPERATION, not a failure (audit
# 2026-08-19 finding 1). `err` in the decisions dict was one channel carrying
# two very different things: "today is not a decision day" and "the VIX3M feed
# is stale, I REFUSE to decide". Both printed SKIPPED and neither reached the
# exit gate, so a sleeve that refused to run its rule still exited 0. Prefixing
# the routine case is what lets the gate tell them apart.
ROUTINE_SKIP = "ROUTINE: "

# Permanent, already-recorded holes in paper_nav. Still PRINTED every run (the
# series genuinely lacks them) but they no longer fail the exit code -- a red
# Last Result that fires forever on an unfixable past hole trains the operator
# to ignore red, which un-fixes F4. Add a date here only after it is recorded
# in the project record as permanently lost.
ACKNOWLEDGED_NAV_HOLES = {"2026-07-30"}   # lost to the Interactive-only task; record EI
# Max sessions the VIX3M reading may lag `today` before e18 refuses to decide
# (audit #3). 2 = tolerate the normal 1-session publish lag + a holiday edge;
# the 5-session Yahoo lag that inverted the signal (record DC) trips it.
VIX3M_MAX_STALE_SESSIONS = 2
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


def series_with_volume(ticker, start="1999-01-01"):
    """Like series() but also returns {date: volume} -- needed by the liquidity
    floor (audit #4). prices.fetch bar layout: (ticker, date, o, h, l, c, adj, vol)."""
    bars = prices.fetch(ticker, start=start)
    dates = [b[1] for b in bars]
    close = {b[1]: b[5] for b in bars}
    vol = {b[1]: b[7] for b in bars}
    return dates, close, vol


def median_dollar_volume(dates, close, vol, n=20, asof=None):
    """Median close*volume over the last `n` sessions up to and including `asof`.
    Past-only -- never looks beyond `asof`. Returns None if there is not enough
    data or the feed carries no volume (in which case the caller must NOT treat
    the name as illiquid on missing data alone)."""
    ds = [d for d in dates if asof is None or d <= asof][-n:]
    vals = [close[d] * vol[d] for d in ds
            if close.get(d) is not None and vol.get(d)]
    if len(vals) < max(5, n // 2):
        return None
    vals.sort()
    m = len(vals) // 2
    return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2.0


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
    """Is the US equity market open RIGHT NOW -> True/False (never None).

    Gates --execute order submission to AFTER-HOURS only (record DF): a
    market-notional order placed while the market is OPEN fills intraday
    instead of queuing for the next open, breaking the EOD/execute-next-open
    rule and desyncing the ledger (record DE).

    PRIMARY: Alpaca's market clock (authoritative -- holidays/half-days/DST
    handled server-side). FALLBACK (audit finding #1, 2026-07-28): a local
    America/New_York regular-hours check. The previous version FAILED OPEN --
    it returned None on any AlpacaError and the caller then warned and
    submitted orders ANYWAY, defeating the guard exactly when the broker is
    flaky (a real Alpaca 500 hit this account 2026-07-23). The local fallback
    errs SAFE in the direction that matters: outside 09:30-16:00 ET on a
    weekday the market is never open, so a "closed" verdict is trustworthy;
    inside that window it may be a holiday (really closed) and we
    conservatively say OPEN, which costs only a skipped mirror that the next
    after-hours run reconciles."""
    from swing_bot.alpaca_client import client_for_sleeve, AlpacaError
    for s in ps.SLEEVES:
        try:
            c = client_for_sleeve(s)
        except AlpacaError:
            continue
        try:
            return bool(c.get_clock().get("is_open"))
        except AlpacaError as e:
            print(f"  market clock unavailable ({e}) -- using local ET fallback",
                  flush=True)
            break
        finally:
            c.close()
    now = dt.datetime.now(ZoneInfo("America/New_York"))
    if now.weekday() >= 5:                       # Sat/Sun
        return False
    return dt.time(9, 30) <= now.time() < dt.time(16, 0)


def backfill_divergence(conn):
    """Learn the REAL Alpaca outcome of every mirrored order still unresolved,
    and repair its sim-side so the row is an actual measurement.

    Why this exists (audit finding #2, 2026-07-28): fill_divergence is M3's ONLY
    implementation-fidelity instrument, and it was INERT -- 10/10 rows had
    alpaca_price NULL because all three call sites pass sim_price only. An order
    is submitted the evening BEFORE it fills, so its fill price cannot be known
    at submit time; nothing ever went back for it. The daily_swing_paper
    docstring meanwhile claimed any gap is "visible, never assumed" -- false
    verification, the exact class of claim this project treats as a trust-killer.
    Read-only against Alpaca, so it runs regardless of the intraday guard."""
    from swing_bot.alpaca_client import client_for_sleeve, AlpacaError
    rows = ps.open_divergence_rows(conn)
    if not rows:
        return
    print(f"\nfill_divergence backfill: {len(rows)} unresolved order(s)")
    clients = {}
    try:
        for r in rows:
            s = r["sleeve"]
            if s not in clients:
                try:
                    clients[s] = client_for_sleeve(s)
                except AlpacaError as e:
                    print(f"    [{s}] SKIPPED (creds): {e}")
                    clients[s] = None
            client = clients[s]
            if client is None:
                continue
            try:
                o = client.get_order(r["alpaca_order_id"])
            except AlpacaError as e:
                # leave unresolved -> retried next run (never invent a fill)
                print(f"    [{s}] {r['ticker']} {r['date']}: poll failed ({e})")
                continue
            status = o.get("status")
            if status not in ("filled", "canceled", "expired", "rejected", "done_for_day"):
                print(f"    [{s}] {r['ticker']} {r['date']}: still {status} -- leaving open")
                continue
            fp = o.get("filled_avg_price")
            fq = o.get("filled_qty")
            fp = float(fp) if fp not in (None, "") else None
            fq = float(fq) if fq not in (None, "") else None
            joined = ps.resolve_divergence(conn, r["id"], status=status,
                                           alpaca_price=fp, alpaca_qty=fq)
            row = conn.execute("SELECT sim_price FROM fill_divergence WHERE id=?",
                               (r["id"],)).fetchone()
            sim = row["sim_price"]
            if status == "filled" and fp:
                d = fp - sim
                bps = f"{d / sim * 10000:+.1f} bps" if sim else "n/a bps (no sim fill)"
                note = "" if joined else "  (no DB fill to join -- sim side unrepaired)"
                print(f"    [{s}] {r['ticker']} {r['date']}: sim ${sim:.4f} vs "
                      f"alpaca ${fp:.4f}  d={d:+.4f} ({bps}) "
                      f"qty={fq}{note}")
            else:
                print(f"    [{s}] {r['ticker']} {r['date']}: {status} (no fill)")
    finally:
        for c in clients.values():
            if c is not None:
                c.close()


MIRROR_DRIFT_WARN_PCT = 0.25   # below this = fractional-share rounding, not a fork
MIN_RECONCILE_NOTIONAL = 1.0   # Alpaca rejects sub-$1 notional; not worth an order anyway


def report_mirror_drift(conn):
    """Print DB-ledger vs Alpaca share counts per sleeve (read-only).

    Audit finding #4 (2026-07-28): the e18 sleeve carries a PERMANENT share fork
    -- record DE claimed it would "self-heal at Tue open", which was WRONG. It
    re-converged in STATE (both hold QQQ) but never in QUANTITY: the 07-20
    midday fire had Alpaca fill intraday @700.622 while the DB simulated
    Tuesday's open @706.680, so the same $ notional bought different share
    counts. reconcile-to-DB (record DA) drives SYMBOLS, not quantities, so
    nothing was ever going to close it.

    This does NOT trade to correct the fork -- the DB ledger is the primary
    forward-paper evidence and is next-open disciplined, so it is never rewritten
    to match a broker fill, and placing bookkeeping orders is a trading-behavior
    change that is Evan's call, not a silent default. What it does is make the
    gap VISIBLE every run, so any DB-vs-Alpaca comparison is made knowing the
    offset instead of assuming there is none."""
    from swing_bot.alpaca_client import client_for_sleeve, AlpacaError
    print("\nmirror drift (DB ledger vs Alpaca shares):")
    for s in ps.SLEEVES:
        pos = ps.get_positions(conn, s)
        try:
            c = client_for_sleeve(s)
        except AlpacaError as e:
            print(f"    [{s}] SKIPPED (creds): {e}")
            continue
        try:
            ap = {p["symbol"]: p for p in c.list_positions()}
        except AlpacaError as e:
            print(f"    [{s}] unavailable: {e}")
            continue
        finally:
            c.close()
        syms = set(pos) | set(ap)
        if not syms:
            print(f"    [{s}] both flat -- aligned")
            continue
        for t in sorted(syms):
            dbq = pos[t]["qty"] if t in pos else 0.0
            aq = float(ap[t]["qty"]) if t in ap else 0.0
            dq = aq - dbq
            pct = (dq / dbq * 100) if dbq else float("inf")
            flag = "  <-- MATERIAL FORK" if abs(pct) >= MIRROR_DRIFT_WARN_PCT else ""
            print(f"    [{s}] {t}: DB {dbq:.7f} vs Alpaca {aq:.7f}  "
                  f"d={dq:+.7f} ({pct:+.3f}%){flag}")


def qty_reconcile_orders(positions, held, close_px, pending):
    """Decide the share-count corrections that bring Alpaca back to the DB
    ledger. PURE -- returns a list of dicts, places nothing (audit #4b).

    The symbol-level reconcile (record DA) only ever answered WHICH tickers to
    hold, never HOW MANY shares, so the e18 fork (+0.864%, +$8.14) created by
    the 07-20 intraday fill was permanent by construction. This closes that.

    STEADY STATE ONLY: when `pending` is set the position is about to be
    rebuilt wholesale by the caller, so correcting its share count first would
    fight that and risk double-trading -- return nothing.

    The action threshold is the SAME band the drift report flags, so what the
    operator sees warned is exactly what gets acted on; ordinary fractional
    rounding (e6 -0.001%, m10 -0.014%) sits far below it. Corrections below
    MIN_RECONCILE_NOTIONAL are reported, not placed (Alpaca rejects sub-$1
    notional, and it is not worth an order).

    These are BOOKKEEPING orders, not signals -- the caller deliberately does
    NOT write them to fill_divergence, which measures signal-fill fidelity."""
    if pending is not None:
        return []
    out = []
    for t in sorted(set(positions) & set(held)):
        dbq = positions[t]["qty"]
        aq = float(held[t]["qty"])
        dq = aq - dbq                       # + => Alpaca holds too many
        pct = abs(dq / dbq * 100) if dbq else 0.0
        if pct < MIRROR_DRIFT_WARN_PCT:
            continue
        notional = abs(dq) * (close_px.get(t) or 0.0)
        out.append({
            "ticker": t, "drift": dq, "pct": pct, "notional": notional,
            "qty": round(abs(dq), 9), "side": "sell" if dq > 0 else "buy",
            "action": "skip_small" if notional < MIN_RECONCILE_NOTIONAL else "order",
        })
    return out


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
    # A leg with no price today cannot fill. That is survivable, but it must
    # never be SILENT (audit #8): the pending target is cleared at the end of
    # this function regardless, so an unfilled BUY leg is dropped for good and
    # the sleeve just sits on that cash. Collect both kinds and report below.
    skipped_sell, skipped_buy = [], []
    for t, pos in positions.items():
        px = fill_open.get(t)
        if px is None or px <= 0:
            skipped_sell.append(t)
            continue  # no bar today for this ticker -- leave held, retry next run
        cash += pos["qty"] * px
        ps.record_fill(conn, sleeve, today, t, "sell", pos["qty"], px, "pending-liquidate")
        ps.upsert_position(conn, sleeve, t, 0.0, px, today)
        # NO log_divergence here (audit #4 F6): this call carried no order id,
        # so open_divergence_rows could never resolve it -- one permanent
        # orphan per leg per cycle, 5 of the live table's 10 rows. The sim-side
        # fill this recorded is already in paper_transactions via record_fill
        # above, which is exactly where resolve_divergence's repair join reads
        # it from. Divergence rows are created at SUBMIT time only, with the
        # Alpaca order id attached.
    # Persist cash NOW, before the buy loop (audit #4 E6). record_fill and
    # upsert_position each commit immediately, but cash was only written once,
    # after the buys -- so a kill between the loops (ExecutionTimeLimit,
    # reboot) left the position deletions COMMITTED while cash still held its
    # pre-sale value: the sale proceeds simply vanished from the ledger that
    # IS the forward evidence. Two writes make every kill window consistent.
    conn.execute("UPDATE paper_sleeves SET cash=? WHERE sleeve=?",
                 (round(cash, 9), sleeve))
    conn.commit()
    if target:
        # cash * w, not cash / len(target) (audit #4 F7): the equal-split
        # ignored the weight the decide_* contract says callers must honour
        # ("Callers translate weights -> $ notional using the sleeve's NAV",
        # paper_sleeves.py) -- while the Alpaca mirror DOES honour it
        # (desired = nav * w). A {.50/.30/.20} target would book $333/$333/$333
        # in this ledger vs $500/$300/$200 at the broker: a $167 fork on a
        # $1,000 sleeve. Latent only because every decide_* today returns
        # equal weights, for which cash*w == cash/len exactly (w = 1/K and the
        # tripwire pins that identity).
        cash_at_entry = cash          # snapshot AFTER the sell loop: weights
                                      # size against the post-liquidation pool,
                                      # not a balance that shrinks per leg
        for t, w in target.items():
            px = fill_open.get(t)
            if px is None or px <= 0:
                skipped_buy.append(t)
                continue
            qty = (cash_at_entry * w) / px
            cash -= qty * px
            ps.record_fill(conn, sleeve, today, t, "buy", qty, px, "pending-enter")
            ps.upsert_position(conn, sleeve, t, qty, px, today)
            # no log_divergence here either -- same reason as the sell leg above
    if skipped_sell or skipped_buy:
        # Report BOTH sides (audit E6). The old message divided only skipped_buy
        # by len(target), so a pure sell-side skip printed "buy=- ~0%
        # under-invested" while the sleeve was in fact simultaneously long a
        # stale position AND buying under-sized legs -- because a position that
        # could not be sold never added its proceeds to `cash`, and
        # per_ticker_cash is that reduced cash divided by the full target size.
        # The sizing arithmetic is right (you cannot spend cash you do not have);
        # it is the operator-visible damage that was under-stated.
        buy_pct = 100.0 * len(skipped_buy) / len(target) if target else 0.0
        note = ""
        if skipped_sell:
            note = (f" ALSO still long {len(skipped_sell)} unsold position(s), so "
                    f"the remaining legs are under-sized by the value of those "
                    f"holdings -- this sleeve's weights no longer match the "
                    f"strategy.")
        print(f"  !! [{sleeve}] PARTIAL REALIZE on {today} -- no open price for: "
              f"sell={skipped_sell or '-'} buy={skipped_buy or '-'}. "
              f"Unfilled BUY legs leave ~{buy_pct:.0f}% of the target unbought."
              f"{note} Check the yfinance feed for those tickers.", flush=True)
        RUN_FAILURES.append(f"[{sleeve}] partial realize: sell={skipped_sell} "
                            f"buy={skipped_buy}")
    # Round away float residue (audit E8): full liquidation left cash at
    # -1.14e-13 instead of 0.0. Harmless to arithmetic, but it makes any future
    # `if cash < 0` guard fire on a sleeve that is exactly flat.
    conn.execute("UPDATE paper_sleeves SET cash=? WHERE sleeve=?",
                 (round(cash, 9), sleeve))
    conn.commit()
    # Only clear the pending target if every BUY leg actually filled (audit E6).
    # Clearing unconditionally dropped an unfillable leg for good -- the sleeve
    # then sat ~1/K in cash against its target until the next weekly decision,
    # with no way to recover it. Keeping the pending lets the next run retry the
    # leg; the realize guard (today > pending_signal_date) still prevents a
    # same-session double fill.
    # DISCLOSED TRADEOFF (audit #4 E10): the retried cycle liquidates and
    # re-buys EVERY leg at the retry day's open, not the signal's next open --
    # a deviation from the EOD rule plus one extra round trip of cost on the
    # already-filled legs. Accepted deliberately: a late fill at a known price
    # beats a permanently under-invested sleeve. This is a tradeoff, not a bug.
    if skipped_buy:
        print("  [%s] pending KEPT for retry next run (unfilled buy legs: %s)"
              % (sleeve, skipped_buy), flush=True)
    else:
        ps.clear_pending(conn, sleeve)
    return True


def mark_nav(conn, sleeve, today, close_px):
    """close_px: {ticker: close_price_today}."""
    st = ps.get_sleeve(conn, sleeve)
    positions = ps.get_positions(conn, sleeve)
    # `or` not a dict default (audit #3): close_px[t] is SET to None when a
    # ticker has no bar today (line ~531 `cl.get(today)`), so the key EXISTS
    # holding None and a `.get(t, default)` fallback can never fire.
    nav = st["cash"] + sum(p["qty"] * (close_px.get(t) or p["entry_price"])
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
    # An empty QQQ fetch (rate limit, DNS, feed outage) used to IndexError on
    # qdates[-1] -- losing the day exactly the way 2026-07-30 was lost, with
    # exit 0 (audit #4 E2). Fail loud instead: the retry ladder inside
    # prices.fetch has already done its 3 backoffs by the time this is empty.
    if not qdates:
        print("!! QQQ fetch returned NO DATA after retries -- cannot establish "
              "the session date. Nothing was decided or marked; re-run when the "
              "feed recovers.", flush=True)
        return 1
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

    # ---- MISSED-SESSION DETECTOR (audit #2) ----
    # The nightly task silently skipped 2026-07-30: no error, non-zero exit, or
    # Windows "missed run" -- the session just vanished from paper_nav, which is
    # the forward-evidence series this whole project rests on. `last_run_at` was
    # already being written but READ BY NOTHING, so nothing could ever notice.
    # Compare the sessions that actually traded against the ones NAV has.
    # (audit #3) The first version compared max(date) to today, which can only
    # see a hole at the END of the series: 2026-07-30 went missing, the next run
    # advanced max(date) to 07-31, and the gap became invisible forever. A set
    # difference over the whole series sees interior holes too, and keeps seeing
    # them, so a skipped session stays reported until it is acknowledged.
    have = {r[0] for r in conn.execute("SELECT DISTINCT date FROM paper_nav")}
    if have:
        first = min(have)
        # `d < today` deliberately: this run has not marked today's NAV yet
        # (that happens ~100 lines below), so today is never "missed".
        missed = [d for d in qdates if first < d < today and d not in have]
        if missed:
            print("\n!! MISSED SESSION(S): %d trading session(s) have no paper_nav "
                  "row -- %s. Those NAV rows are PERMANENTLY absent from the "
                  "forward-evidence series. Check the scheduled task."
                  % (len(missed), ", ".join(missed)), flush=True)
            new_holes = [d for d in missed if d not in ACKNOWLEDGED_NAV_HOLES]
            if new_holes:
                RUN_FAILURES.append("missed session(s): " + ", ".join(new_holes))

    # ---- realize any pending from the previous run (needs today's opens for
    # whatever tickers are currently held / newly targeted) ----
    # TICKER-keyed, so it starts EMPTY (audit #3). It used to start as
    # dict(qopen), which is DATE-keyed {'2026-08-05': 703.1, ...}: every consumer
    # does fill_open.get(<ticker>), so those ~6,700 entries were unreachable
    # junk, and QQQ was never actually "always available" -- it arrives through
    # the refetch loop below like every other held name.
    fill_open = {}
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
    # STALENESS GATE (audit finding #3, 2026-07-28): _asof carry-forward will
    # happily reach ARBITRARILY far back, and the CBOE fetch falls back to the
    # yfinance ^VIX3M feed that is exactly the stale source which INVERTED this
    # signal on 2026-07-17 (record DC: stale 1.011 said CASH, fresh 0.914 said
    # HOLD). Carry-forward across 1-2 sessions is the intended live
    # accommodation; beyond that the term structure is no longer current and a
    # decision would be fiction dressed as data. Refuse loudly instead.
    v3_stale = len([d for d in qdates if v3_dt is not None and v3_dt < d <= today])
    if vix3m_today is None or v3_stale > VIX3M_MAX_STALE_SESSIONS:
        target_e18, err = None, (f"VIX3M STALE ({v3_stale} sessions behind; asof "
                                 f"{v3_dt} vs {today}) -- refusing to decide on "
                                 f"a stale term structure")
    else:
        target_e18, err = ps.decide_e18_vixts(vix_today, vix3m_today)
    decisions["e18_vixts"] = (target_e18, err)

    wk = isoweek_str(today)
    m10_st = ps.get_sleeve(conn, "m10_1_nagel")
    # Weekly gate = Friday, OR catch-up when an entire ISO week was skipped
    # (audit #4 E3). `weekday()==4` alone has no slot for a market-holiday
    # Friday (Good Friday; 2026-12-25): the week's last session is a Thursday,
    # the gate never fires, and by Monday `wk` is already the NEXT week -- so
    # that week's m10_1 rebalance was silently never made. The catch-up fires
    # on the first session after such a week (signal at that close, execute
    # next open, as always). DISCLOSED BEHAVIORAL CHANGE to a live sleeve,
    # recorded in the project record 2026-08-11: the prereg specifies a weekly
    # decision; a holiday-delayed one is closer to that intent than a skipped
    # one. Cold start (last_decided_week empty) still waits for a Friday.
    d_today = dt.date.fromisoformat(today)
    prev_wk = isoweek_str((d_today - dt.timedelta(days=7)).isoformat())
    last_wk = m10_st["last_decided_week"]
    is_decision_day = (last_wk != wk) and (
        d_today.weekday() == 4
        or bool(last_wk and last_wk not in (wk, prev_wk)))
    if is_decision_day:
        residual_ranks = None
        if vix_today is not None and vix_today > VIX_THR:
            print("Stress + weekly decision day: fetching 39-name universe + FF3 "
                  "for the residual ranking ...", flush=True)
            ff = fresh_ff3()
            ranks = []
            illiquid = []
            for t in UNIV:
                ds, cl, vol = series_with_volume(t, start="2010-01-01")
                cls = [cl[d] for d in ds]
                # LIQUIDITY FLOOR (audit #4). CLAUDE.md calls this floor
                # mandatory in any universe filter, but MIN_MEDIAN_DOLLAR_VOL
                # was defined in universe.py and READ BY NOTHING -- an
                # UNENFORCEABLE contract. This is the only place the live loop
                # picks individual stocks, so it is the correct chokepoint:
                # screen on 20-session median dollar volume before ranking.
                adv = median_dollar_volume(ds, cl, vol, n=20, asof=today)
                if adv is not None and adv < universe.MIN_MEDIAN_DOLLAR_VOL:
                    illiquid.append((t, adv))
                    continue
                form = residual_series(ds, cls, ff)
                v = dict(zip(ds, form)).get(today)
                if v is not None:
                    ranks.append((v, t))
            if illiquid:
                print("  liquidity floor ($%.0fM/day) excluded %d name(s): %s"
                      % (universe.MIN_MEDIAN_DOLLAR_VOL / 1e6, len(illiquid),
                         ", ".join("%s $%.1fM" % (t, a / 1e6) for t, a in illiquid)),
                      flush=True)
            residual_ranks = sorted(ranks)
        target_m10, err = ps.decide_m10_1(vix_today, list(qclose[d] for d in qdates), residual_ranks)
        decisions["m10_1_nagel"] = (target_m10, err)
        # ONLY burn the week when a target actually exists (audit #3).
        # decide_m10_1 returns (None, reason) on ordinary paths -- VIX feed empty,
        # stress with no residual ranks. Marking the week decided anyway stored
        # no pending (the `target is None: continue` below) while blocking retry
        # until the next Friday: the sleeve would hold stale positions for five
        # sessions, exit 0, and print no error.
        if target_m10 is not None:
            conn.execute("UPDATE paper_sleeves SET last_decided_week=? WHERE sleeve='m10_1_nagel'", (wk,))
            conn.commit()
    else:
        # Say WHICH condition held (audit #4 F18): the old either/or text
        # printed "week 2026-W33 already decided" on a Monday when the DB held
        # W32 -- a false claim about state in the primary evidence log.
        if last_wk == wk:
            reason = f"week {wk} already decided"
        else:
            reason = (f"not a decision day (today is not Friday; last decided "
                      f"{last_wk or 'never'}, current week {wk})")
        decisions["m10_1_nagel"] = (None, ROUTINE_SKIP + reason)

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
    close_px = {}             # TICKER-keyed -- see the fill_open note above
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
            # Audit 2026-08-19 finding 1: this was printed and DROPPED. A
            # genuine refusal (VIX3M stale, VIX feed empty, <200 sessions of
            # history) left the sleeve not running its rule, while the run
            # exited 0 and paper_nav recorded the session anyway -- forward
            # evidence with a silent hole in it. OBSERVED 2026-07-13:
            # "VIX or VIX3M unavailable today". Routine non-decision days are
            # excluded so the red Last Result stays meaningful.
            if not err.startswith(ROUTINE_SKIP):
                RUN_FAILURES.append(f"[{s}] refused to decide: {err}")
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
        # Resolve YESTERDAY's mirrored orders before placing today's (audit #2).
        # Read-only against Alpaca, so it runs even when the guard below skips
        # submission -- a market-open run still learns what actually filled.
        backfill_divergence(conn)
        report_mirror_drift(conn)
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
                desired = {t: round(p["qty"] * (close_px.get(t) or 0.0), 2)
                           for t, p in positions.items()}
            desired = {t: n for t, n in desired.items() if n > 0}
            try:
                client = client_for_sleeve(s)
            except AlpacaError as e:
                print(f"\n--execute [{s}]: SKIPPED (creds): {e}")
                # The DB ledger keeps advancing while this sleeve's broker
                # account silently drifts (audit #4 E1's blast radius) -- that
                # is a failed run, not a quiet skip.
                RUN_FAILURES.append(f"[{s}] mirror skipped: credentials unavailable")
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
                failed_closes = []
                for sym in held:                       # flatten what's not wanted
                    if sym not in target_syms:
                        try:
                            client.close_position(sym)
                            print(f"    CLOSE {sym}")
                        except AlpacaError as e:
                            print(f"    close {sym} FAILED: {e}")
                            failed_closes.append(sym)
                # A failed close must BLOCK the buys (audit #4 F9): proceeding
                # leaves the broker holding both the unwanted and the wanted
                # position while the DB shows one -- a silent fork. DELETE
                # /v2/positions on a 4xx is non-transient, so _request did not
                # retry; the next run re-attempts the whole flatten-then-buy.
                if failed_closes:
                    print(f"    !! {len(failed_closes)} close(s) FAILED "
                          f"({failed_closes}) -- SKIPPING this sleeve's buys to "
                          f"avoid holding both old and new positions.", flush=True)
                    RUN_FAILURES.append(f"[{s}] failed closes: {failed_closes}; "
                                        f"buys skipped")
                    continue
                for t, notional in desired.items():     # enter / repair wanted legs
                    if t in held:
                        print(f"    hold {t} (already held; not re-buying)")
                        continue
                    try:
                        o = client.submit_order(symbol=t, notional=notional, side="buy",
                                                type="market", time_in_force="day")
                        print(f"    BUY {t} ~${notional:.2f} -> order {o.get('id')}")
                        # Provisional sim side = today's close for t. It is only
                        # a placeholder: the real DB-sim fill is TOMORROW's open,
                        # and backfill_divergence repairs this field from
                        # paper_transactions once that fill happens. Fetch the
                        # close rather than defaulting to 0.0 -- close_px is
                        # date-keyed and only gains ticker keys for tickers
                        # already HELD, so a first-ever entry silently logged
                        # sim_price=0.0 (rows 3/4; audit #2).
                        prov = close_px.get(t)
                        if prov is None:
                            _, _cl, _ = series(t, start="2024-01-01")
                            prov = _cl.get(today)
                            close_px[t] = prov
                        ps.log_divergence(conn, s, today, t, prov if prov else 0.0,
                                          alpaca_order_id=o.get("id"))
                    except AlpacaError as e:
                        print(f"    buy {t} FAILED: {e}")
                        # Reaches the exit gate, like its failed-closes sibling
                        # above: a wanted leg that never opened leaves the DB
                        # ledger claiming a position the broker does not hold
                        # (audit #4 finding 3). Printing alone exited 0 and the
                        # scheduled task reported green.
                        RUN_FAILURES.append(f"[{s}] buy {t} failed: {e}")
                # QTY RECONCILE (audit #4b, authorized by Evan 2026-07-28).
                # Symbol-level reconcile (record DA) only ever answered WHICH
                # tickers to hold, never HOW MANY shares -- so the e18 fork
                # (+0.864%, +$8.14) from the 07-20 intraday fill was permanent
                # by construction. This closes share-count drift too.
                #
                # STEADY STATE ONLY (`pending is None`): when a pending target
                # exists the position is about to be rebuilt wholesale above, so
                # correcting its share count first would fight that and could
                # double-trade. Threshold is the same band the drift report
                # flags, so what you see warned is exactly what gets acted on;
                # rounding noise (e6 -0.001%, m10 -0.014%) is far below it.
                # These are BOOKKEEPING orders, not signals -- deliberately NOT
                # written to fill_divergence, which measures signal-fill fidelity
                # and would be polluted by them.
                for corr in qty_reconcile_orders(positions, held, close_px, pending):
                    if corr["action"] == "skip_small":
                        print(f"    qty-drift {corr['ticker']} {corr['pct']:.3f}% but "
                              f"~${corr['notional']:.2f} < ${MIN_RECONCILE_NOTIONAL:.2f} "
                              f"-- too small to correct, leaving it")
                        continue
                    try:
                        o = client.submit_order(symbol=corr["ticker"],
                                                qty=corr["qty"], side=corr["side"],
                                                type="market", time_in_force="day")
                        print(f"    QTY-RECONCILE {corr['side'].upper()} {corr['ticker']} "
                              f"{corr['qty']:.7f} sh (~${corr['notional']:.2f}, drift "
                              f"{corr['drift']:+.7f} = {corr['pct']:.3f}%) "
                              f"-> order {o.get('id')}")
                    except AlpacaError as e:
                        print(f"    qty-reconcile {corr['side']} {corr['ticker']} "
                              f"FAILED: {e}")
                        # Share-count drift left uncorrected is exactly the
                        # permanent fork this reconcile exists to close, so a
                        # silent failure defeats its whole purpose
                        # (audit #4 finding 3).
                        RUN_FAILURES.append(
                            f"[{s}] qty-reconcile {corr['side']} "
                            f"{corr['ticker']} failed: {e}")
            except AlpacaError as e:
                print(f"\n--execute [{s}]: connection failed: {e}")
                # The worst of the five handlers: this wraps list_positions,
                # cancel_all_orders, the closes AND the buys, so it can abort a
                # sleeve AFTER orders were cancelled -- broker and DB forked --
                # and still exit 0 with the task green (audit #4 finding 3).
                RUN_FAILURES.append(f"[{s}] mirror aborted: connection failed: {e}")
            finally:
                client.close()

    conn.close()
    print("\nDone. Scheduled task 'SwingTradingDailyPaper' runs this daily on weekday "
          "evenings (7pm local, --execute). Log: var\\daily_swing_paper.log.")
    if RUN_FAILURES:
        print("\n!! RUN COMPLETED WITH %d FAILURE(S) -- exit 1 so Task Scheduler "
              "shows a red Last Result instead of 0:" % len(RUN_FAILURES), flush=True)
        for f in RUN_FAILURES:
            print("   - " + f, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    # SystemExit(main()) not main() (audit #4 F4): a bare call discards the
    # return value and the process exits 0 no matter what happened above.
    raise SystemExit(main())
