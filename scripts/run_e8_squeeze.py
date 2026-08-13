"""E8 — volatility-compression breakout (squeeze), per prereg 9b49190.

Long-only breakout after >=5-session BB-inside-Keltner squeeze, K=3,
exit on close<EMA20 or 40-bar max hold. Gate window 2000-2013:
CAGR>=15% AND maxDD<=60%, n_trades>=30. No tuning after results.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted,
dividend-UNADJUSTED. Fetched live from inception; does NOT touch swing.db
(protects frozen-regression refs). Cache in scratchpad only.

NAV (finding-things map): this file is E8's own experiment, BUT its
`cache_fetch(ticker)` (below) + `CACHE, COST, CAP0` are the repo's de-facto
SHARED DATA LAYER — imported by 31 files (30 experiment runners + the standing
proof script; 28 name `cache_fetch` itself: e18, m10-1, m11, x7,
c1, c4, c7, x1, ...). If you are hunting for "where do the experiments get
their prices," it is here, not swing_bot/prices.py (that store feeds the
swing_bot engines + the live M3 loop instead). Returns rows as
(ticker, date, open, high, low, close, ...); most callers use b[1]=date,
b[2]=open, b[5]=close.
"""
import datetime
import json
import math
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices
from swing_bot.universe import UNIVERSE

CACHE = Path(os.environ.get("E8E9_CACHE",
    Path(__file__).resolve().parent.parent / ".e8e9_cache"))
K = 3
COST = 5.0 / 10000.0
CAP0 = 1000.0
MAX_HOLD = 40
SQUEEZE_MIN = 5
SIM_START = "2000-01-01"
GATE_END = "2013-12-31"
SEC_START = "2014-01-01"


def _last_bar_date(bars):
    """Last bar date of a cached series, or None if `bars` is not bar-shaped.

    Deliberately total (audit E13). `.e8e9_cache` is ONE filename namespace over
    three shapes: bar lists, dicts (`*_div`, `ff3_daily`, `*_idx`), and lists of
    date strings (`*_earn`). Indexing `bars[-1][1]` blind raises KeyError or
    TypeError on the other two, which is why the freshness check must not assume.
    """
    if not isinstance(bars, list) or not bars:
        return None
    row = bars[-1]
    # Must be a ROW, not a bare string: the `*_earn` shape is a list of date
    # STRINGS, and "2026-01-01"[1] is the character "0" -- which is a str, passes
    # a naive isinstance check, and quietly becomes the series' "end date".
    if not isinstance(row, (list, tuple)) or len(row) < 2:
        return None
    return row[1] if isinstance(row[1], str) else None


def cache_last_date(ticker):
    """Last bar date held in cache for `ticker`, or None if not cached."""
    f = CACHE / f"{ticker}.json"
    if not f.exists():
        return None
    try:
        bars = json.loads(f.read_text())
    except (ValueError, OSError):
        return None
    return _last_bar_date(bars)


# Every series this PROCESS has read, so a mixed-vintage universe announces
# itself (audit #1). The `through=` freshness parameter added after the M12
# incident is opt-in and no caller passes it, so the guard cannot fire and the
# corruption it was written to stop is still undetectable. This is the passive
# half of that fix: it changes no result and refetches nothing, it just refuses
# to let vintages diverge SILENTLY. Threading a real `through` through every
# call site would move recorded numbers and needs its own pre-registration.
_VINTAGES = {}
_VINTAGE_REPORTED = set()
_STALE_REPORTED = set()

# Audit #2 (2026-08-12). Two changes, both to guards that could not do their job.
#
# 1. The mixed-vintage check requires len(distinct) > 1, comparing series against
#    EACH OTHER. With one series in play that bound is exactly 1, so for a
#    single-ticker script (c4=QQQ, c6=SPY, x1=SPY) the branch was unreachable BY
#    CONSTRUCTION -- and uniform staleness was invisible to it for the same
#    reason. Those are precisely the scripts that read a SPY benchmark 18 sessions
#    older than the universe it was tabulated against. Staleness is now measured
#    against the CLOCK, which neither blind spot can hide from. (Measuring against
#    the newest date on disk would not close the uniform case: if every series is
#    equally old, the max equals the value under test.)
# 2. Both checks now RAISE. Printing WAS the defect -- SEC's window end is open
#    (2099-01-01), so a stale series silently sets its own evaluation-window end
#    and the CAGR denominator with it, the warning scrolls past, and the number is
#    believed. Deliberate historical run: SWING_ALLOW_STALE_CACHE=1.
_ALLOW_STALE = os.environ.get("SWING_ALLOW_STALE_CACHE") == "1"
_MAX_STALE_DAYS = int(os.environ.get("SWING_MAX_CACHE_STALE_DAYS", "5"))


class StaleCacheError(RuntimeError):
    """A VINTAGE VERDICT, not a fetch failure. Subclasses RuntimeError so
    nothing that already caught RuntimeError changes behaviour, but it is named
    so that a consumer with a broad `except Exception` around cache_fetch can
    re-raise it instead of dropping the ticker. Two did exactly that
    (run_m12_factorial, run_v1_harness_check) and turned "refuse to run" into
    "run on a silently emptied universe" -- record EO, 2026-08-13."""


def _vintage_fail(msg):
    if _ALLOW_STALE:
        print("  !! " + msg + "\n     [SWING_ALLOW_STALE_CACHE=1 -- continuing]", flush=True)
        return
    raise StaleCacheError(
        msg + "\n     Refresh the cache: delete EVERY price-series *.json in "
        ".e8e9_cache, not a subset, and re-run every consumer in one sitting "
        "-- cache_fetch refetches only on a MISS for the tickers the running "
        "script names, so a one-script re-run just replaces the old mixed "
        "vintage with a new one. Or set SWING_ALLOW_STALE_CACHE=1 if this run "
        "is deliberately historical."
    )


def _note_vintage(ticker, bars):
    last = _last_bar_date(bars)
    if last is None:
        return
    _VINTAGES[ticker] = last
    distinct = set(_VINTAGES.values())
    if len(distinct) > 1 and not distinct <= _VINTAGE_REPORTED:
        _VINTAGE_REPORTED.update(distinct)
        newest = max(distinct)
        behind = sorted(t for t, d in _VINTAGES.items() if d != newest)
        _vintage_fail(
            "MIXED-VINTAGE CACHE: %d distinct end-dates in play (%s .. %s). "
            "%d of %d series stop before %s: %s%s. Cross-sectional results "
            "computed over this panel are NOT comparable -- a short series that "
            "ends mid-window is what overstated M12's headline effect 3x."
            % (len(distinct), min(distinct), newest, len(behind),
               len(_VINTAGES), newest, ", ".join(behind[:8]),
               " ..." if len(behind) > 8 else ""))
        return
    if ticker in _STALE_REPORTED:
        return
    try:
        age = (datetime.date.today() - datetime.date.fromisoformat(last)).days
    except ValueError:
        return
    if age > _MAX_STALE_DAYS:
        _STALE_REPORTED.add(ticker)
        _vintage_fail(
            "STALE CACHE: %s ends %s, %d calendar days ago (tolerance %d days, "
            "SWING_MAX_CACHE_STALE_DAYS). The evaluation window terminates "
            "wherever the data stops, so this series sets its own window end -- "
            "and a benchmark read at a different vintage is not comparable to it."
            % (ticker, last, age, _MAX_STALE_DAYS))


def cache_fetch(ticker, through=None):
    """Cached bars for `ticker` (permanent on-disk cache; the repo's shared
    data layer, ~29 importers).

    FRESHNESS (audit finding #1, 2026-08-03): this cache had NO end-date check
    and returned any existing file unconditionally. Because entries are written
    on whatever day a ticker is first touched, a universe assembled across
    sessions silently mixes VINTAGES -- and that corrupted a committed result.
    M12 ran 142 names of which 38 stopped at 2026-07-10 while 104 ran to
    2026-07-31; every number in the secondary window was wrong (the headline
    effect was overstated 3x) because the 38 short names went None mid-window
    and were marked at zero rather than dropped.

    `through`: optional ISO date the cached series must reach. When the cache
    falls short, it is REFETCHED rather than silently returned stale. Callers
    that do not care (single-ticker experiments already run and recorded) keep
    the old behaviour by omitting it, so no prior result shifts underneath.

    MISSING-BAR SEMANTICS -- consumers must choose deliberately (audit #7).
    A ticker can be absent on a date another ticker trades. Two live consumers
    already disagree, and neither choice was written down:
      * run_c3_vol_breakout carries the last known close FORWARD (stale-mark).
      * run_m12_factorial dropped the position's value to ZERO -- which is not a
        price, and is exactly what let a mixed-vintage cache silently rewrite a
        published result. It now truncates the date axis instead.
    Zero is never correct for a HELD position. Carry forward, or truncate the
    axis. If you add a consumer, state which you chose.
    """
    CACHE.mkdir(exist_ok=True)
    f = CACHE / f"{ticker}.json"
    if f.exists():
        bars = json.loads(f.read_text())
        last = _last_bar_date(bars)
        if not through or (last and last >= through):
            _note_vintage(ticker, bars)
            return bars
        print(f"  cache STALE {ticker}: ends {last or 'empty'} "
              f"< {through} -- refetching", flush=True)
    for attempt in range(4):
        try:
            bars = prices.fetch(ticker, start="1990-01-01")
        except Exception as e:
            print(f"  {ticker} attempt {attempt+1} error: {e}", flush=True)
            bars = None
        # OUTSIDE the try on purpose. _note_vintage used to sit inside it, so a
        # StaleCacheError was caught by the fetch handler, printed as an
        # "attempt N error", and the fetch retried 4x before dying with
        # "could not fetch" -- a vintage verdict reported as a network failure
        # (record EO). The retry loop guards prices.fetch, nothing else.
        if bars:
            f.write_text(json.dumps(bars))
            _note_vintage(ticker, bars)
            return bars
        time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"could not fetch {ticker}")


def indicators(bars):
    """Per prereg: SMA20, population sigma20, EMA20 (alpha=2/21, SMA-seeded),
    ATR20 (simple mean of TR), squeeze flag, entry/exit signal arrays."""
    n = len(bars)
    close = [b[5] for b in bars]
    high = [b[3] for b in bars]
    low = [b[4] for b in bars]
    sma = [None] * n
    ema = [None] * n
    atr = [None] * n
    squeeze = [None] * n
    tr = [None] * n
    e = None
    for i in range(n):
        if i >= 19:
            w = close[i - 19:i + 1]
            mu = sum(w) / 20.0
            sma[i] = mu
            if e is None:
                e = mu                      # seed EMA with first SMA
            else:
                e = e + (2.0 / 21.0) * (close[i] - e)
            ema[i] = e
        if i >= 1:
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]),
                        abs(low[i] - close[i - 1]))
        if i >= 20:
            atr[i] = sum(tr[i - 19:i + 1]) / 20.0
            w = close[i - 19:i + 1]
            mu = sma[i]
            sd = math.sqrt(sum((x - mu) ** 2 for x in w) / 20.0)  # population
            ub, lb = mu + 2.0 * sd, mu - 2.0 * sd
            uk, lk = ema[i] + 1.5 * atr[i], ema[i] - 1.5 * atr[i]
            squeeze[i] = (ub < uk) and (lb > lk)
    entry = [False] * n
    for i in range(SQUEEZE_MIN + 21, n):
        if squeeze[i] is False and all(squeeze[i - j] is True
                                       for j in range(1, SQUEEZE_MIN + 1)) \
                and close[i] > sma[i]:
            entry[i] = True
    return dict(close=close, sma=sma, ema=ema, entry=entry)


def simulate(data):
    """Global event-driven sim. data[t] = (bars, ind, date->idx)."""
    all_dates = sorted({b[1] for t in data for b in data[t][0]
                        if b[1] >= SIM_START})
    cash, nav_prev = CAP0, CAP0
    pos = {}            # ticker -> dict(sh, fill, entry_date, entry_i, minret)
    pend_in, pend_out = {}, {}   # ticker -> signal date
    trades = []
    nav_path = []       # (date, nav)
    last_close = {}
    for d in all_dates:
        # 1) executions at today's open (only tickers with a bar today)
        for t in list(pend_out):
            bars, ind, idx = data[t]
            if d in idx and t in pos:
                o = bars[idx[d]][2]
                p = pos.pop(t)
                cash += p["sh"] * o * (1 - COST)
                net = (o * (1 - COST)) / (p["fill"] * (1 + COST)) - 1
                trades.append(dict(ticker=t, entry=p["entry_date"],
                                   exit=d, net=net,
                                   hold=idx[d] - p["entry_i"],
                                   minret=p["minret"]))
                del pend_out[t]
        for t in list(pend_in):
            bars, ind, idx = data[t]
            if d in idx and t not in pos and len(pos) < K:
                o = bars[idx[d]][2]
                size = min(cash, nav_prev / K)
                if size > 10.0 and o > 0:
                    sh = size / (o * (1 + COST))
                    cash -= size
                    pos[t] = dict(sh=sh, fill=o, entry_date=d,
                                  entry_i=idx[d], minret=0.0)
                del pend_in[t]
            elif d in idx:
                del pend_in[t]      # slot lost or already held: drop order
        # 2) mark NAV at close
        for t in data:
            bars, ind, idx = data[t]
            if d in idx:
                last_close[t] = ind["close"][idx[d]]
        nav = cash + sum(p["sh"] * last_close[t] for t, p in pos.items())
        nav_path.append((d, nav))
        nav_prev = nav
        # 3) signals at close
        for t, p in pos.items():
            bars, ind, idx = data[t]
            if d in idx:
                i = idx[d]
                p["minret"] = min(p["minret"],
                                  ind["close"][i] / p["fill"] - 1)
                if t not in pend_out and (
                        ind["close"][i] < ind["ema"][i]
                        or i - p["entry_i"] >= MAX_HOLD):
                    pend_out[t] = d
        cands = []
        for t in data:
            bars, ind, idx = data[t]
            if d in idx and t not in pos and t not in pend_in:
                i = idx[d]
                if ind["entry"][i]:
                    cands.append((ind["close"][i] / ind["sma"][i] - 1, t))
        cands.sort(reverse=True)
        free = K - len(pos) - len(pend_in)
        for _, t in cands[:max(0, free)]:
            pend_in[t] = d
    return nav_path, trades, pos, last_close


def window_stats(nav_path, trades, lo, hi):
    seg = [(d, v) for d, v in nav_path if lo <= d <= hi]
    if len(seg) < 30:
        return None
    nav = [v for _, v in seg]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav))]
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    tw = [x for x in trades if lo <= x["entry"] <= hi]
    return dict(cagr=cagr, mo=(1 + cagr) ** (1 / 12) - 1, mdd=mdd,
                sharpe=sh, n=len(tw),
                win=sum(1 for x in tw if x["net"] > 0) / len(tw) if tw else
                float("nan"))


def main():
    data = {}
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        idx = {b[1]: i for i, b in enumerate(bars)}
        data[e.ticker] = (bars, indicators(bars), idx)
        print(f"loaded {e.ticker}: {bars[0][1]}..{bars[-1][1]} "
              f"({len(bars)} bars)", flush=True)
    nav_path, trades, open_pos, last_close = simulate(data)
    print(f"\ntotal closed trades: {len(trades)}; "
          f"open at end: {list(open_pos)} (marked to last close)")
    gate = window_stats(nav_path, trades, SIM_START, GATE_END)
    sec = window_stats(nav_path, trades, SEC_START, "2099-01-01")
    full = window_stats(nav_path, trades, SIM_START, "2099-01-01")
    for name, s in [("GATE 2000-2013", gate), ("SECONDARY 2014-", sec),
                    ("FULL 2000-", full)]:
        print(f"\n{name}: CAGR {s['cagr']*100:.2f}%  ({s['mo']*100:.2f}%/mo)  "
              f"maxDD {s['mdd']*100:.1f}%  Sharpe {s['sharpe']:.2f}  "
              f"n_trades {s['n']}  win {s['win']*100:.1f}%")
    g1 = gate["cagr"] >= 0.15
    g2 = gate["mdd"] <= 0.60
    g3 = gate["n"] >= 30
    print(f"\n  [{'PASS' if g1 else 'FAIL'}] gate CAGR>=15% "
          f"({gate['cagr']*100:.2f}%)")
    print(f"  [{'PASS' if g2 else 'FAIL'}] gate maxDD<=60% "
          f"({gate['mdd']*100:.1f}%)")
    print(f"  [{'OK' if g3 else 'INCONCLUSIVE'}] n_trades>=30 ({gate['n']})")
    if not g3:
        verdict = "INCONCLUSIVE"
    else:
        s1 = sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60
        verdict = "PASS" if (g1 and g2 and s1) else "FAIL"
        print(f"  [{'PASS' if s1 else 'FAIL'}] secondary CAGR>=15% & DD<=60% "
              f"({sec['cagr']*100:.2f}%, {sec['mdd']*100:.1f}%)")
    print(f"\n  E8 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
