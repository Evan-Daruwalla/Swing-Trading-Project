"""X6 - crypto BTC/ETH time-series trend (paper-first), per prereg
prereg_x6_crypto_trend.md (committed doc-only before this runner).

Per-asset long-or-flat dual-MA (SMA20>SMA100), signal at daily close, execute
next bar's open, 25 bps/side (crypto taker). BTC + ETH + equal-weight K=2 vs
HODL. Gate 2018-2022 / secondary 2023- -> MODIFIED-WINDOW CAP (PROMISING).
Paper-first; live-money crypto is Evan-gated (custody). No swing.db writes.

DATA: yfinance BTC-USD/ETH-USD daily, auto_adjust=False (crypto: close=actual),
24/7 bars. New domain - does NOT touch swing.db or frozen refs.
"""
import json
import math
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import CAP0
import yfinance as yf

CACHE = Path("D:/ClaudeCode/Swing Trading/.crypto_cache")
CACHE.mkdir(exist_ok=True)
CRY_COST = 0.0025           # 25 bps/side crypto taker
GATE = ("2018-01-01", "2022-12-31")
SEC = ("2023-01-01", "2099-01-01")


def fetch(sym):
    f = CACHE / f"{sym}.json"
    if f.exists():
        return json.loads(f.read_text())
    for attempt in range(4):
        try:
            d = yf.download(sym, period="max", auto_adjust=False, progress=False)
            if not d.empty:
                if d.columns.nlevels == 2:
                    d.columns = d.columns.droplevel(1)
                out = {ts.strftime("%Y-%m-%d"): [float(o), float(c)]
                       for ts, o, c in zip(d.index, d["Open"], d["Close"])
                       if o == o and c == c}
                f.write_text(json.dumps(out))
                return out
        except Exception as e:
            print(f"  {sym} attempt {attempt+1}: {type(e).__name__}", flush=True)
        time.sleep(15 * (attempt + 1))
    raise RuntimeError(f"could not fetch {sym}")


def sma(x, n):
    out = [None] * len(x)
    for i in range(n - 1, len(x)):
        out[i] = sum(x[i - n + 1:i + 1]) / n
    return out


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return dict(cagr=float("nan"), mdd=float("nan"), sharpe=float("nan"))
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1] > 0]
    yrs = len(nav) / 365.0                     # crypto = 365 bars/yr
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(365) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mdd=mdd, sharpe=sh)


def sleeve(dates, op, cl, fast, slow, cost):
    """long-or-flat when SMA(fast)>SMA(slow); return (nav_by_date, toggles)."""
    sf, ss = sma(cl, fast), sma(cl, slow)
    cash, units, pend = CAP0, 0.0, None
    navd, toggles = {}, []
    for i, d in enumerate(dates):
        if pend is not None:
            if pend == 1 and units == 0.0 and cash > 0:
                units = cash / (op[i] * (1 + cost)); cash = 0.0; toggles.append(d)
            elif pend == 0 and units > 0.0:
                cash = units * op[i] * (1 - cost); units = 0.0; toggles.append(d)
            pend = None
        navd[d] = cash + units * cl[i]
        w = 1 if (sf[i] is not None and ss[i] is not None and sf[i] > ss[i]) else 0
        if w == 1 and units == 0.0 and cash > 0:
            pend = 1
        elif w == 0 and units > 0.0:
            pend = 0
    return navd, toggles


def load(sym):
    d = fetch(sym)
    dates = sorted(d)
    return dates, [d[k][0] for k in dates], [d[k][1] for k in dates]


def win(navd, dates, lo, hi):
    seg = [navd[d] for d in dates if lo <= d <= hi and d in navd]
    return seg


def combine(nBTC, dBTC, nETH, dETH):
    """equal-weight daily-rebalanced 50/50 of the two sleeve NAV curves."""
    common = sorted(set(d for d in dBTC if d in set(dETH)))
    nav = [CAP0]
    for i in range(1, len(common)):
        d0, d1 = common[i - 1], common[i]
        rb = nBTC[d1] / nBTC[d0] - 1 if nBTC[d0] > 0 else 0
        re = nETH[d1] / nETH[d0] - 1 if nETH[d0] > 0 else 0
        nav.append(nav[-1] * (1 + 0.5 * rb + 0.5 * re))
    return common, {d: v for d, v in zip(common, nav)}


def hodl(dates, cl):
    return {d: cl[i] / cl[0] * CAP0 for i, d in enumerate(dates)}


def report(name, navd, dates, hodld):
    row = {}
    for wn, (lo, hi) in [("gate", GATE), ("sec", SEC)]:
        s = stats(win(navd, dates, lo, hi))
        h = stats(win(hodld, dates, lo, hi))
        row[wn] = (s, h)
        print(f"  {name:16}{wn:5} sleeve CAGR {s['cagr']*100:8.2f}% DD {s['mdd']*100:5.1f}% "
              f"Sh {s['sharpe']:5.2f} | HODL CAGR {h['cagr']*100:8.2f}% DD {h['mdd']*100:5.1f}% "
              f"Sh {h['sharpe']:5.2f}")
    return row


def main():
    dB, oB, cB = load("BTC-USD")
    dE, oE, cE = load("ETH-USD")
    print(f"X6 crypto trend | BTC {dB[0]}..{dB[-1]} ({len(dB)}); "
          f"ETH {dE[0]}..{dE[-1]} ({len(dE)}); cost {CRY_COST*1e4:.0f}bps/side\n")

    nB, tB = sleeve(dB, oB, cB, 20, 100, CRY_COST)
    nE, tE = sleeve(dE, oE, cE, 20, 100, CRY_COST)
    hB, hE = hodl(dB, cB), hodl(dE, cE)
    print("PRIMARY dual-MA (SMA20>SMA100), 25bps/side:")
    report("BTC", nB, dB, hB)
    report("ETH", nE, dE, hE)
    cdates, ncomb = combine(nB, dB, nE, dE)
    # combined HODL 50/50
    hcomb = {}
    for i in range(len(cdates)):
        d = cdates[i]
        hcomb[d] = 0.5 * hB[d] + 0.5 * hE[d]
    # rebase combined HODL to CAP0 at first common date
    base = hcomb[cdates[0]]
    hcomb = {d: v / base * CAP0 for d, v in hcomb.items()}
    comb_row = report("COMBINED K=2", ncomb, cdates, hcomb)
    ntg = sum(1 for d in tB + tE if GATE[0] <= d <= GATE[1])

    print("\nsensitivity - 100d single MA (SMA100 vs price via fast=1):")
    for sym, dd, oo, cc, hh in [("BTC", dB, oB, cB, hB), ("ETH", dE, oE, cE, hE)]:
        n100, _ = sleeve(dd, oo, cc, 1, 100, CRY_COST)
        report(sym + "-100d", n100, dd, hh)

    print("\ncost stress (combined K=2 dual-MA):")
    for c, lab in [(0.0010, "10bps"), (0.0025, "25bps"), (0.0050, "50bps")]:
        nb, _ = sleeve(dB, oB, cB, 20, 100, c)
        ne, _ = sleeve(dE, oE, cE, 20, 100, c)
        cd, nc = combine(nb, dB, ne, dE)
        g = stats(win(nc, cd, *GATE)); s = stats(win(nc, cd, *SEC))
        print(f"  {lab:6} gate CAGR {g['cagr']*100:7.2f}% Sh {g['sharpe']:.2f} | "
              f"sec CAGR {s['cagr']*100:7.2f}% Sh {s['sharpe']:.2f}")

    # verdict (PROMISING-capped): combined sleeve beats HODL on Sharpe both windows
    # AND cuts gate maxDD >=20pp AND +CAGR both
    (gs, gh), (ss, sh) = comb_row["gate"], comb_row["sec"]
    dd_cut = (gh["mdd"] - gs["mdd"]) * 100
    floor = ntg >= 10
    ok = (gs["sharpe"] > gh["sharpe"] and ss["sharpe"] > sh["sharpe"]
          and dd_cut >= 20.0 and gs["cagr"] > 0 and ss["cagr"] > 0)
    print(f"\n=== VERDICT (prereg prereg_x6_crypto_trend.md; PROMISING-capped) ===")
    print(f"  gate toggles {ntg} (>=10: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  combined sleeve>HODL Sharpe both ({gs['sharpe']:.2f}>{gh['sharpe']:.2f}, "
          f"{ss['sharpe']:.2f}>{sh['sharpe']:.2f}); gate DD cut {dd_cut:.1f}pp (>=20); "
          f"+CAGR both ({gs['cagr']*100:.1f}/{ss['cagr']*100:.1f})")
    if not floor:
        v = "INCONCLUSIVE"
    elif ok:
        v = "PROMISING (paper-first; live-money custody Evan-gated; PASS-HR/RA not claimable)"
    else:
        v = "FAIL (crypto trend sleeve does not clear the HODL-relative bar net of 25bps)"
    print(f"\n  X6 VERDICT: {v}")


if __name__ == "__main__":
    main()
