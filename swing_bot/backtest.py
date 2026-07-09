"""Minimal daily backtest engine for E1 (ETF IBS mean reversion).

Implements EXACTLY the frozen pre-registration `docs/prereg_E1_ibs.md`
(commit 8963e49) — do not deviate:
  entry  : IBS < 0.20 at close of day T (long-only, eligible = listed +
           not zero-range)
  exit   : first close with IBS > 0.80, OR 5-trading-day time stop
  sizing : capital/K per position, K=5 max concurrent, lowest-IBS-first,
           ties alphabetical, one position/ticker, fractional shares
  fills  : 'next_open' (PRIMARY, decide close[T] -> fill open[T+1]) or
           'c2c' (decide close[T] -> fill close[T])
  cost   : cost_bps per side applied to every fill price

Purpose-built (~200 lines); deliberately NOT adapted from Trading's monthly
factor_backtest.py. Prices split-adjusted, dividend-UNADJUSTED.
"""
import math

from swing_bot import prices, universe, signals

IBS_ENTRY = 0.20
IBS_EXIT = 0.80
MAX_HOLD = 5        # trading days
K = 5               # max concurrent positions


def _load(conn, entries):
    """Return (all_dates sorted, bars[ticker][date] = (o,h,l,c))."""
    bars = {}
    dates = set()
    for e in entries:
        rows = conn.execute(
            "SELECT date, open, high, low, close FROM bars WHERE ticker=? "
            "ORDER BY date", (e.ticker,)).fetchall()
        bars[e.ticker] = {d: (o, h, l, c) for d, o, h, l, c in rows}
        dates.update(bars[e.ticker].keys())
    return sorted(dates), bars


def run_backtest(conn, entries=None, fill="next_open", cost_bps=5.0,
                 capital=500.0, k=K, ibs_entry=IBS_ENTRY, ibs_exit=IBS_EXIT,
                 max_hold=MAX_HOLD, size_on_nav=False):
    """size_on_nav=False (v1, default): positions sized at FIXED
    initial-capital/k dollars — can drive cash negative after losses
    (implicit leverage; see gotchas bin, E2 K=1). All E1/E1b/E2 pinned refs
    use this path — do not change its behavior.
    size_on_nav=True (v2, C1 2026-07-09): target = min(prev-close-NAV/k,
    available cash), floored at 0 — sizes shrink with losses, cash can never
    go negative."""
    entries = entries or universe.UNIVERSE
    dates, bars = _load(conn, entries)
    cost = cost_bps / 10000.0
    fixed_target = capital / k
    defer = (fill == "next_open")

    cash = capital
    pos = {}            # ticker -> dict(entry_date, entry_fill, shares, ei)
    pend_entry, pend_exit = [], []   # decided at close, fill next open
    trades, nav = [], []

    def cur_target():
        if not size_on_nav:
            return fixed_target
        nav_prev = nav[-1][1] if nav else capital
        return max(0.0, min(nav_prev / k, cash))

    def do_buy(tk, price, date, ei):
        nonlocal cash
        target = cur_target()
        if target <= 0:
            return
        fillp = price * (1 + cost)
        shares = target / fillp
        cash -= shares * fillp
        pos[tk] = dict(entry_date=date, entry_fill=fillp, shares=shares, ei=ei)

    def do_sell(tk, price, date):
        nonlocal cash
        p = pos.pop(tk)
        fillp = price * (1 - cost)
        cash += p["shares"] * fillp
        net = fillp / p["entry_fill"] - 1.0
        trades.append(dict(ticker=tk, entry_date=p["entry_date"],
                           exit_date=date, net_ret=net,
                           hold_days=dates.index(date) - p["ei"]))

    for i, d in enumerate(dates):
        # 1. next_open model: execute yesterday's decisions at today's open
        if defer:
            for tk in pend_exit:
                if d in bars[tk]:
                    do_sell(tk, bars[tk][d][0], d)
            for tk in pend_entry:
                if d in bars[tk] and len(pos) < k:
                    do_buy(tk, bars[tk][d][0], d, i)
            pend_entry, pend_exit = [], []

        # 2. at close[d]: mark, decide exits then entries
        # exits
        exit_now = []
        for tk, p in list(pos.items()):
            bar = bars[tk].get(d)
            if bar is None:
                continue
            v = signals.ibs(bar[1], bar[2], bar[3])
            held = i - p["ei"]
            if (v is not None and v > ibs_exit) or held >= max_hold:
                exit_now.append(tk)
        # entries: eligible candidates by IBS asc, then ticker
        cands = []
        held_set = set(pos.keys())
        for e in entries:
            tk = e.ticker
            if tk in held_set or e.data_start > d:
                continue
            bar = bars[tk].get(d)
            if bar is None:
                continue
            v = signals.ibs(bar[1], bar[2], bar[3])
            if v is not None and v < ibs_entry:
                cands.append((v, tk))
        cands.sort(key=lambda x: (x[0], x[1]))
        slots = k - len(pos) + len(exit_now)
        picks = [tk for _, tk in cands[:max(0, slots)]]

        if defer:
            pend_exit, pend_entry = exit_now, picks
        else:  # c2c: fill immediately at close[d]
            for tk in exit_now:
                do_sell(tk, bars[tk][d][3], d)
            for tk in picks:
                if len(pos) < k:
                    do_buy(tk, bars[tk][d][3], d, i)

        # 3. mark NAV at close[d]
        mtm = sum(p["shares"] * bars[tk][d][3]
                  for tk, p in pos.items() if d in bars[tk])
        nav.append((d, cash + mtm))

    return dict(trades=trades, nav=nav,
                params=dict(fill=fill, cost_bps=cost_bps, capital=capital,
                            k=k, ibs_entry=ibs_entry, ibs_exit=ibs_exit,
                            max_hold=max_hold, size_on_nav=size_on_nav))


def metrics(result):
    """Kill-criteria metrics from a backtest result."""
    trades = result["trades"]
    nav = [v for _, v in result["nav"]]
    n = len(trades)
    # net_ret/hold_days are IBS-trade fields; absent for NAV-only strategies
    # (e.g. rotation switches) — degrade to nan rather than KeyError.
    _nets = [t["net_ret"] for t in trades if "net_ret" in t]
    mean_net = sum(_nets) / len(_nets) if _nets else float("nan")
    # daily NAV returns -> annualized Sharpe
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1]]
    if len(rets) > 1:
        mu = sum(rets) / len(rets)
        var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
        sd = math.sqrt(var)
        sharpe = (mu / sd) * math.sqrt(252) if sd > 0 else float("nan")
    else:
        sharpe = float("nan")
    # max drawdown on NAV
    peak, mdd = -1e18, 0.0
    for v in nav:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak if peak > 0 else 0.0)
    total_ret = nav[-1] / nav[0] - 1 if nav else float("nan")
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav and yrs > 0 else float("nan")
    _holds = [t["hold_days"] for t in trades if "hold_days" in t]
    return dict(n_trades=n, mean_net_ret=mean_net, ann_sharpe=sharpe,
                max_dd=mdd, total_ret=total_ret, cagr=cagr,
                mean_hold=sum(_holds) / len(_holds) if _holds else float("nan"))
