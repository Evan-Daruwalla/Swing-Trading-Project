"""IN-SAMPLE SCREENS (2026-07-09) — hypothesis-GENERATING, NOT verdicts.

Three one-sitting screens from catalog v2 (record Appendix W: Evan's dated
override covers A3; B1/B4 are stop-clear):
  A3 — overnight-only IBS harvest: buy close on IBS<0.20 (K=2 lowest),
       sell next open. The purest test of the measured overnight component.
  B1 — gap-down reversion executed AT the open (gap <= X vs prior close,
       prior close > 200d MA), exit same close or next open. Signal-to-fill
       gap ~zero by construction.
  B4 — vol-regime leverage rotation: hold 3x fund while its 1x signal index
       closes above its 200d MA, else cash; switch at next open.

All sized NAV-proportionally (v2 semantics), 5 bps/side. Any survivor gets
its own pre-registration before a confirmatory run — these numbers are
in-sample screens and say NOTHING final.
Prices split-adjusted, dividend-UNADJUSTED (swing.db).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices, universe, signals

COST = 5.0 / 10000.0
TRAIN = ("2014-01-02", "2021-12-31")
HOLD = ("2022-01-01", "2026-07-08")
FULL = ("2014-01-02", "2026-07-08")
WINDOWS = [("train", *TRAIN), ("holdout", *HOLD), ("full", *FULL)]

BROAD = [e.ticker for e in universe.UNIVERSE if e.group == "broad_us"]
LEV = [e.ticker for e in universe.LEVERAGED]


def load(tickers):
    conn = prices.connect()
    bars = {}
    for t in tickers:
        rows = conn.execute(
            "SELECT date, open, high, low, close FROM bars WHERE ticker=? "
            "ORDER BY date", (t,)).fetchall()
        bars[t] = {d: (o, h, l, c) for d, o, h, l, c in rows}
    dates = sorted(set.intersection(*(set(b) for b in bars.values())))
    return dates, bars


def stats(navs):
    if len(navs) < 3 or navs[0] <= 0:
        return dict(cagr=float("nan"), mo=float("nan"), mdd=float("nan"),
                    sharpe=float("nan"))
    rets = [navs[i] / navs[i-1] - 1 for i in range(1, len(navs))]
    yrs = len(navs) / 252.0
    cagr = (navs[-1] / navs[0]) ** (1 / yrs) - 1
    mo = (1 + cagr) ** (1 / 12) - 1
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sharpe = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = navs[0], 0.0
    for v in navs:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mo=mo, mdd=mdd, sharpe=sharpe)


def row(label, navs, n):
    s = stats(navs)
    print(f"{label:44} n={n:>5}  {s['mo']*100:>6.2f}%/mo "
          f"CAGR={s['cagr']*100:>7.2f}% maxDD={s['mdd']*100:>5.1f}% "
          f"Sharpe={s['sharpe']:>5.2f}")


def a3_screen(tickers, k, label):
    dates, bars = load(tickers)
    for wname, ws, we in WINDOWS:
        idx = [i for i, d in enumerate(dates) if ws <= d <= we]
        nav, navs, n = 1.0, [1.0], 0
        for i in idx:
            if i + 1 >= len(dates):
                break
            d, d1 = dates[i], dates[i + 1]
            cands = []
            for t in tickers:
                o, h, l, c = bars[t][d]
                v = signals.ibs(h, l, c)
                if v is not None and v < 0.20:
                    cands.append((v, t))
            cands.sort()
            picks = cands[:k]
            day_ret = 0.0
            for _, t in picks:
                buy = bars[t][d][3] * (1 + COST)
                sell = bars[t][d1][0] * (1 - COST)
                day_ret += (sell / buy - 1) / k
                n += 1
            nav *= (1 + day_ret)
            navs.append(nav)
        row(f"A3 overnight IBS {label} K={k} [{wname}]", navs, n)


def b1_screen(tickers, thresh, exit_mode, k, label):
    dates, bars = load(tickers)
    closes = {t: [bars[t][d][3] for d in dates] for t in tickers}
    for wname, ws, we in WINDOWS:
        idx = [i for i, d in enumerate(dates) if ws <= d <= we]
        nav, navs, n = 1.0, [1.0], 0
        for i in idx:
            if i < 200 or (exit_mode == "next_open" and i + 1 >= len(dates)):
                navs.append(nav)
                continue
            d = dates[i]
            cands = []
            for t in tickers:
                prev_c = closes[t][i - 1]
                ma200 = sum(closes[t][i - 200:i]) / 200.0
                if prev_c <= ma200:
                    continue
                gap = bars[t][d][0] / prev_c - 1
                if gap <= thresh:
                    cands.append((gap, t))
            cands.sort()
            picks = cands[:k]
            day_ret = 0.0
            for _, t in picks:
                buy = bars[t][d][0] * (1 + COST)
                if exit_mode == "close":
                    sell = bars[t][d][3] * (1 - COST)
                else:
                    sell = bars[t][dates[i + 1]][0] * (1 - COST)
                day_ret += (sell / buy - 1) / k
                n += 1
            nav *= (1 + day_ret)
            navs.append(nav)
        row(f"B1 gap<={thresh*100:.0f}% {label} exit={exit_mode} K={k} "
            f"[{wname}]", navs, n)


def b4_screen(lev_t, sig_t, label):
    dates, bars = load([lev_t, sig_t])
    sig_closes = [bars[sig_t][d][3] for d in dates]
    for wname, ws, we in WINDOWS:
        idx = [i for i, d in enumerate(dates) if ws <= d <= we]
        nav, navs = 1.0, [1.0]
        state, shares, switches = 0, 0.0, 0   # 0=cash, 1=long
        pend = None
        for i in idx:
            d = dates[i]
            o, _, _, c = bars[lev_t][d]
            # execute pending switch at today's open
            if pend is not None:
                if pend == 1 and state == 0:
                    shares = nav / (o * (1 + COST)); state = 1; switches += 1
                elif pend == 0 and state == 1:
                    nav = shares * o * (1 - COST); state = 0; switches += 1
                pend = None
            if state == 1:
                nav = shares * c
            navs.append(nav)
            # decide at close (need 200 prior signal closes)
            if i >= 200:
                ma200 = sum(sig_closes[i - 200:i]) / 200.0
                want = 1 if sig_closes[i] > ma200 else 0
                if want != state:
                    pend = want
        row(f"B4 rotation {label} [{wname}]", navs, switches)


def main():
    print("IN-SAMPLE SCREENS — hypothesis-generating only (no verdicts)")
    print("=" * 78)
    print("--- A3: overnight-only IBS harvest (stop-override, Appendix W) ---")
    a3_screen(BROAD, 2, "broad")
    a3_screen(LEV, 2, "lev")
    print("--- B1: gap-down reversion at the open ---")
    b1_screen(BROAD, -0.01, "close", 2, "broad")
    b1_screen(BROAD, -0.01, "next_open", 2, "broad")
    b1_screen(LEV, -0.02, "close", 2, "lev")
    b1_screen(LEV, -0.02, "next_open", 2, "lev")
    b1_screen(LEV, -0.03, "close", 2, "lev")
    b1_screen(LEV, -0.03, "next_open", 2, "lev")
    print("--- B4: vol-regime leverage rotation (200d MA of 1x signal) ---")
    b4_screen("TQQQ", "QQQ", "TQQQ/QQQ")
    b4_screen("UPRO", "SPY", "UPRO/SPY")


if __name__ == "__main__":
    main()
