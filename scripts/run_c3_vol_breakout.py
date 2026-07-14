"""C3 - consolidated volatility-breakout kill-shot, per prereg
prereg_c3_vol_breakout.md (committed doc-only before this runner).

Squeeze (20d realized vol < trailing-252d median, prior session) -> entry on a
20-session closing high (next open) -> exit on close < trailing-10-session low
(next open) OR 40-session time stop. K=5, 5 bps/side, 29-ETF universe. Arms:
main (channel+time exit) and time-stop-only. Rungs A/B/C. D1 dual-bar.
No swing.db writes.

DATA CONVENTION: split-adjusted, dividend-UNADJUSTED (auto_adjust=False).
"""
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0
from swing_bot.universe import UNIVERSE

K = 5
HOLD = 40
ENTRY_N = 20
EXIT_N = 10
VOL_N = 20
MED_N = 252
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mdd=float("nan"), sharpe=float("nan"))
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1] > 0]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mdd=mdd, sharpe=sh)


def load():
    data = {}
    for e in UNIVERSE:
        bars = cache_fetch(e.ticker)
        data[e.ticker] = ([b[1] for b in bars], [b[2] for b in bars],
                          [b[5] for b in bars])
    return data


def signals(dates, cl):
    """Per-ticker: entry_sig[i]=True if signal at close i; exit uses 10d low."""
    n = len(cl)
    rets = [0.0] + [cl[i] / cl[i - 1] - 1 for i in range(1, n)]
    vol = [None] * n
    for i in range(VOL_N, n):
        vol[i] = statistics.pstdev(rets[i - VOL_N + 1:i + 1])
    entry = [False] * n
    for i in range(MED_N + VOL_N, n):
        if vol[i - 1] is None:
            continue
        win = [v for v in vol[i - 1 - MED_N + 1:i] if v is not None]
        if len(win) < MED_N // 2:
            continue
        squeeze_prior = vol[i - 1] < statistics.median(win)
        breakout = cl[i] >= max(cl[i - ENTRY_N + 1:i + 1])
        entry[i] = squeeze_prior and breakout
    return entry


def run(data, channel_exit, cost, c2c):
    idx = {t: {d: i for i, d in enumerate(ds)} for t, (ds, _, _) in data.items()}
    entry_sig = {t: signals(ds, cl) for t, (ds, op, cl) in data.items()}
    master = sorted({d for (ds, _, _) in data.values() for d in ds})
    cash, nav_prev = CAP0, CAP0
    pos, navd, entries = {}, {}, []

    def px(t, i):                      # fill price at session i
        ds, op, cl = data[t]
        return cl[i - 1] if (c2c and i > 0) else op[i]

    pend_entry, pend_exit = [], []
    for d in master:
        # exits first
        for t in list(pend_exit):
            if t in pos and d in idx[t]:
                i = idx[t][d]
                cash += pos[t]["sh"] * px(t, i) * (1 - cost)
                del pos[t]
        pend_exit = []
        # entries
        for t in pend_entry:
            if t not in pos and len(pos) < K and d in idx[t]:
                i = idx[t][d]
                p = px(t, i)
                size = min(cash, nav_prev / K)
                if size > 10.0 and p > 0:
                    pos[t] = dict(sh=size / (p * (1 + cost)), age=0)
                    cash -= size
                    entries.append(d)
        pend_entry = []
        # mark + evaluate close signals
        nav = cash
        for t, p in pos.items():
            if d in idx[t]:
                i = idx[t][d]
                ds, op, cl = data[t]
                p["age"] += 1
                nav += p["sh"] * cl[i]
                low10 = min(cl[max(0, i - EXIT_N):i]) if i > 0 else cl[i]
                hit_low = channel_exit and cl[i] < low10
                if hit_low or p["age"] >= HOLD:
                    pend_exit.append(t)
            else:
                nav += p["sh"] * data[t][2][idx[t].get(d, -1)] if False else 0
        # stale-mark names without today's bar at last known close
        for t, p in pos.items():
            if d not in idx[t]:
                ds, op, cl = data[t]
                j = max(i for i, dd in enumerate(ds) if dd < d)
                nav += p["sh"] * cl[j]
        for t, (ds, op, cl) in data.items():
            if t not in pos and d in idx[t] and entry_sig[t][idx[t][d]]:
                pend_entry.append(t)
        pend_entry.sort()
        navd[d] = nav
        nav_prev = nav
    return navd, master, entries


def main():
    data = load()
    spy = {b[1]: b[5] for b in cache_fetch("SPY")}

    def report(tag, channel_exit, cost, c2c):
        navd, master, entries = run(data, channel_exit, cost, c2c)
        rows = {}
        for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
            nav = [navd[d] for d in master if lo <= d <= hi]
            seg = [d for d in sorted(spy) if lo <= d <= hi]
            rows[wn] = (stats(nav), stats([spy[d] / spy[seg[0]] for d in seg]),
                        sum(1 for d in entries if lo <= d <= hi))
        g, gs, ng = rows["gate"]; s, ss, ns = rows["sec"]
        print(f"{tag:28} gate {g['cagr']*100:6.2f}%/DD{g['mdd']*100:5.1f}%/Sh{g['sharpe']:5.2f}"
              f" (n={ng})   sec {s['cagr']*100:6.2f}%/DD{s['mdd']*100:5.1f}%/Sh{s['sharpe']:5.2f}")
        return rows

    print(f"C3 vol-breakout kill-shot | 29 ETFs, K={K}, entry {ENTRY_N}d-high after "
          f"squeeze, exit {EXIT_N}d-low/{HOLD}d\n")
    rows = report("C (next-open, 5bps) MAIN", True, COST, False)
    report("B (next-open, 0bps)", True, 0.0, False)
    report("A (c2c, 0bps)", True, 0.0, True)
    report("C stress 15bps", True, 0.0015, False)
    report("time-stop-only arm (C)", False, COST, False)

    g, gs, n_gate = rows["gate"]; s, ss, _ = rows["sec"]
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60 and s["cagr"] >= 0.15 and s["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gs["sharpe"] and s["sharpe"] > ss["sharpe"]
          and g["cagr"] > 0 and s["cagr"] > 0)
    floor = n_gate >= 30
    print(f"\n=== D1 VERDICT (prereg prereg_c3_vol_breakout.md) ===")
    print(f"  gate entries {n_gate} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR   [{'PASS' if ra else 'fail'}] "
          f"PASS-RA (gate Sharpe {g['sharpe']:.2f})")
    v = ("INCONCLUSIVE" if not floor else "PASS-HR" if hr else "PASS-RA" if ra
         else "FAIL (breakout/chart-pattern family closed)")
    print(f"\n  C3 VERDICT: {v}")


if __name__ == "__main__":
    main()
