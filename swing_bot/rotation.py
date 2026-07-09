"""Moving-average leverage-rotation engine for swing_bot (E4).

Implements the frozen pre-registration `docs/prereg_E4_rotation.md`
(commit 313d88a): hold `fund` while `signal` closes above its N-day SMA,
else cash; switch at the open `exec_lag` days after the signal, cost per side.
K=1 (full capital in one instrument). Separate from the IBS backtest engine —
different strategy class (regime timing, single instrument).

Prices split-adjusted, dividend-UNADJUSTED. Returns a dict compatible with
`backtest.metrics` ('nav' + 'trades' where trades = switch records).
"""
from swing_bot import prices


def _series(conn, ticker):
    rows = conn.execute(
        "SELECT date, open, close FROM bars WHERE ticker=? ORDER BY date",
        (ticker,)).fetchall()
    return rows  # list of (date, open, close)


def run_rotation(conn, fund, signal, ma_len=200, exec_lag=0, cost_bps=5.0,
                 start=None, end=None, capital=500.0):
    cost = cost_bps / 10000.0
    fund_rows = _series(conn, fund)
    sig_rows = _series(conn, signal)
    fund_by = {d: (o, c) for d, o, c in fund_rows}
    sig_close = {d: c for d, _, c in sig_rows}
    sig_dates = [d for d, _, _ in sig_rows]
    # trade on dates present in BOTH series
    dates = [d for d in (d for d, _, _ in fund_rows) if d in sig_close]

    # index of each date in sig_dates for SMA lookback
    sig_idx = {d: i for i, d in enumerate(sig_dates)}
    sig_closes_list = [c for _, _, c in sig_rows]

    cash, shares, state = capital, 0.0, 0     # 0=cash, 1=long fund
    pending = None                            # (target_state, decided_index)
    nav_hist, switches = [], []

    win = [d for d in dates if (start is None or d >= start)
           and (end is None or d <= end)]

    for i, d in enumerate(dates):
        o, c = fund_by[d]
        # execute a pending switch whose lag has elapsed, at today's open.
        # decided at close of index j=pending[1]; lag 0 => next open (i=j+1),
        # lag L => i = j+1+L.
        if pending is not None and (i - pending[1]) >= exec_lag + 1:
            target = pending[0]
            if target == 1 and state == 0:
                buy = o * (1 + cost)
                shares = cash / buy
                cash = 0.0
                state = 1
                switches.append(dict(date=d, kind="buy"))
            elif target == 0 and state == 1:
                cash = shares * o * (1 - cost)
                shares = 0.0
                state = 0
                switches.append(dict(date=d, kind="sell"))
            pending = None

        # mark NAV at close
        nav = cash + shares * c
        if d in win or (start is None and end is None):
            nav_hist.append((d, nav))

        # decide at close (needs ma_len prior signal closes)
        si = sig_idx[d]
        if si >= ma_len:
            ma = sum(sig_closes_list[si - ma_len:si]) / ma_len
            want = 1 if sig_close[d] > ma else 0
            if want != state and pending is None:
                pending = (want, i)

    # restrict switches to window for reporting
    sw = [s for s in switches if (start is None or s["date"] >= start)
          and (end is None or s["date"] <= end)]
    return dict(nav=nav_hist, trades=sw)


def buy_hold(conn, ticker, start=None, end=None, capital=500.0):
    rows = [r for r in _series(conn, ticker)
            if (start is None or r[0] >= start) and (end is None or r[0] <= end)]
    if not rows:
        return dict(nav=[], trades=[])
    base = rows[0][2]
    return dict(nav=[(d, capital * c / base) for d, _, c in rows], trades=[])
