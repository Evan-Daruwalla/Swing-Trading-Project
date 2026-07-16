"""M1.8 fill-timing ablation (PRD #15 + #13).

Per-signal DIAGNOSTIC (not the backtest engine): on every IBS<0.20 signal at
close of day T, decompose the 1-day-forward return by fill timing:

  c2c       = close[T+1]/close[T]   - 1   (published basis; enter close T)
  overnight = open[T+1]/close[T]    - 1   (gap Model A forfeits)
  intraday  = close[T+1]/open[T+1]  - 1   (buy-open, sell-close same day)
  nopen1d   = open[T+2]/open[T+1]   - 1   (executable 1-day, enter open T+1)

Question: is the IBS edge mostly OVERNIGHT (close->next open)? If so, the
next-open executable loop (pre-reg Model A) loses it. Gross of costs; a raw
per-signal average, NOT the K=5 strategy return (that is M2).

Returns permitted here: run strictly AFTER the M1.7 pre-registration commit
(8963e49). Prices split-adjusted, dividend-UNADJUSTED.

NAV (finding-things map): imports swing_bot (prices, signals, universe).
Imported by: no other module (standalone runner).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices, universe, signals

THRESH = 0.20


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    conn = prices.connect()
    by_ticker = {}
    pooled = {"c2c": [], "overnight": [], "intraday": [], "nopen1d": []}
    by_group = {}

    for e in universe.UNIVERSE:
        rows = conn.execute(
            "SELECT date, open, high, low, close FROM bars "
            "WHERE ticker=? ORDER BY date", (e.ticker,)).fetchall()
        acc = {"c2c": [], "overnight": [], "intraday": [], "nopen1d": []}
        for i in range(len(rows) - 2):
            d, o, h, l, c = rows[i]
            v = signals.ibs(h, l, c)
            if v is None or v >= THRESH:
                continue
            o1, c1 = rows[i + 1][1], rows[i + 1][4]
            o2 = rows[i + 2][1]
            acc["c2c"].append(c1 / c - 1)
            acc["overnight"].append(o1 / c - 1)
            acc["intraday"].append(c1 / o1 - 1)
            acc["nopen1d"].append(o2 / o1 - 1)
        by_ticker[e.ticker] = (e.group, acc)
        g = by_group.setdefault(e.group,
                                {"c2c": [], "overnight": [],
                                 "intraday": [], "nopen1d": []})
        for k in pooled:
            pooled[k].extend(acc[k])
            g[k].extend(acc[k])

    def bps(x):
        return x * 10000

    print(f"{'ticker':7}{'group':13}{'n':>6}{'c2c_bps':>9}{'ovn_bps':>9}"
          f"{'intra_bps':>10}{'nopen_bps':>10}")
    print("-" * 64)
    for t, (g, acc) in by_ticker.items():
        print(f"{t:7}{g:13}{len(acc['c2c']):>6}"
              f"{bps(mean(acc['c2c'])):>9.1f}{bps(mean(acc['overnight'])):>9.1f}"
              f"{bps(mean(acc['intraday'])):>10.1f}"
              f"{bps(mean(acc['nopen1d'])):>10.1f}")
    print("-" * 64)
    for g, acc in by_group.items():
        print(f"{'GROUP':7}{g:13}{len(acc['c2c']):>6}"
              f"{bps(mean(acc['c2c'])):>9.1f}{bps(mean(acc['overnight'])):>9.1f}"
              f"{bps(mean(acc['intraday'])):>10.1f}"
              f"{bps(mean(acc['nopen1d'])):>10.1f}")
    print("-" * 64)
    print(f"{'POOLED':20}{len(pooled['c2c']):>6}"
          f"{bps(mean(pooled['c2c'])):>9.1f}{bps(mean(pooled['overnight'])):>9.1f}"
          f"{bps(mean(pooled['intraday'])):>10.1f}"
          f"{bps(mean(pooled['nopen1d'])):>10.1f}")
    print()
    print(f"POOLED haircut (c2c - nopen1d) = "
          f"{bps(mean(pooled['c2c']) - mean(pooled['nopen1d'])):.1f} bps")
    print(f"POOLED overnight share of c2c = "
          f"{mean(pooled['overnight']) / mean(pooled['c2c']):.0%}")


if __name__ == "__main__":
    main()
