"""E5 — E4 rotation across 2000-2013 hostile regimes, per prereg 09a3a31.

Synthesize daily-rebalanced 3x Nasdaq from QQQ (1999+), calibrate drag to real
TQQQ over 2014-2026 (validation gate), then run the 200-MA rotation over the
UNSEEN 2000-2013 window. No tuning; drag METHOD fixed, its VALUE data-derived.

Does NOT touch swing.db — fetches fresh into memory.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from swing_bot import prices

OVL = ("2014-01-02", "2026-07-08")   # overlap for calibration/validation
HOSTILE = ("2000-01-01", "2013-12-31")
FULL = ("2000-01-01", "2026-07-08")


def series(ticker, start):
    bars = prices.fetch(ticker, start=start)          # (ticker,date,o,h,l,c,adj,vol)
    return [(b[1], b[2], b[5]) for b in bars]          # (date, open, close)


def synth_3x(qqq, d_annual):
    """Daily-rebalanced 3x from QQQ returns, drag d_annual/yr. Returns
    {date: (syn_open, syn_close)} indexed like qqq (open approximated by
    prior close * intraday-open ratio of QQQ)."""
    drag = d_annual / 252.0
    out = {}
    lvl = 1.0
    prev_c = None
    for i, (dt, o, c) in enumerate(qqq):
        if prev_c is None:
            syn_o = lvl
        else:
            # overnight piece of the 3x move (QQQ open vs prev close)
            r_on = o / prev_c - 1
            syn_o = lvl * (1 + 3 * r_on - drag)     # open level
        # full-day close level from prev close
        if prev_c is None:
            syn_c = lvl
        else:
            r_cc = c / prev_c - 1
            syn_c = lvl * (1 + 3 * r_cc - drag)
        out[dt] = (syn_o, syn_c)
        lvl = syn_c
        prev_c = c
    return out


def rotation_nav(dates, sig_close, pos_oc, ma=200, cost_bps=5.0,
                 start=None, end=None, cap=500.0):
    cost = cost_bps / 10000.0
    closes = [sig_close[d] for d in dates]
    cash, sh, state, pend = cap, 0.0, 0, None
    nav = []
    for i, d in enumerate(dates):
        o, c = pos_oc[d]
        if pend is not None and (i - pend[1]) >= 1:      # lag 0 => next open
            if pend[0] == 1 and state == 0:
                sh = cash / (o * (1 + cost)); cash = 0.0; state = 1
            elif pend[0] == 0 and state == 1:
                cash = sh * o * (1 - cost); sh = 0.0; state = 0
            pend = None
        v = cash + sh * c
        if (start is None or d >= start) and (end is None or d <= end):
            nav.append(v)
        if i >= ma:
            m = sum(closes[i - ma:i]) / ma
            want = 1 if closes[i] > m else 0
            if want != state and pend is None:
                pend = (want, i)
    return nav


def bh_nav(dates, oc, start, end, cap=500.0):
    xs = [(d, oc[d][1]) for d in dates if start <= d <= end]
    base = xs[0][1]
    return [cap * c / base for _, c in xs]


def stats(nav):
    if len(nav) < 3 or nav[0] <= 0:
        return dict(cagr=float("nan"), mo=float("nan"), mdd=float("nan"))
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v); mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mo=(1 + cagr) ** (1 / 12) - 1, mdd=mdd)


def corr(a, b):
    n = len(a); ma = sum(a) / n; mb = sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = math.sqrt(sum((x - ma) ** 2 for x in a))
    vb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return cov / (va * vb) if va and vb else float("nan")


def main():
    print("fetching QQQ (1999+) and TQQQ (2010+)...")
    qqq = series("QQQ", "1999-01-01")
    tqqq = series("TQQQ", "2010-01-01")
    qdates = [d for d, _, _ in qqq]
    qclose = {d: c for d, _, c in qqq}
    tclose = {d: c for d, _, c in tqqq}

    # --- calibrate drag to real TQQQ over overlap ---
    ov_dates = [d for d in qdates if OVL[0] <= d <= OVL[1] and d in tclose]
    real_cagr = stats([tclose[d] for d in ov_dates])["cagr"]
    best = None
    for step in range(0, 41):                      # 0..10%/yr in 0.25 steps
        D = step * 0.0025
        syn = synth_3x(qqq, D)
        syn_ov = [syn[d][1] for d in ov_dates]
        c = stats(syn_ov)["cagr"]
        err = abs(c - real_cagr)
        if best is None or err < best[1]:
            best = (D, err, c)
    D_cal = best[0]
    print(f"real TQQQ overlap CAGR={real_cagr*100:.2f}%  "
          f"calibrated drag={D_cal*100:.2f}%/yr  synth CAGR={best[2]*100:.2f}%")

    syn = synth_3x(qqq, D_cal)
    syn_close = {d: syn[d][1] for d in qdates}
    # daily-return correlation on overlap
    ov = [d for d in ov_dates]
    r_syn = [syn_close[ov[i]] / syn_close[ov[i-1]] - 1 for i in range(1, len(ov))]
    r_real = [tclose[ov[i]] / tclose[ov[i-1]] - 1 for i in range(1, len(ov))]
    rho = corr(r_syn, r_real)
    val_ok = rho >= 0.99 and abs(best[2] - real_cagr) <= 0.03
    print(f"\n=== VALIDATION GATE ===")
    print(f"  daily-return corr={rho:.4f} (need >=0.99)  "
          f"|synth-real CAGR|={abs(best[2]-real_cagr)*100:.2f}pp (need <=3)")
    print(f"  validation: {'PASS' if val_ok else 'FAIL'}")

    # --- windows ---
    def report(label, s, e):
        rot = stats(rotation_nav(qdates, qclose, syn, 200, 5.0, s, e))
        b3 = stats(bh_nav(qdates, syn, s, e))
        bq = stats(bh_nav(qdates, {d: (o, qclose[d]) for d, o, _ in qqq}, s, e))
        print(f"  [{label}] rotation CAGR={rot['cagr']*100:>7.2f}% "
              f"({rot['mo']*100:>5.2f}%/mo) maxDD={rot['mdd']*100:>5.1f}%  |  "
              f"BH-3x CAGR={b3['cagr']*100:>7.2f}% maxDD={b3['mdd']*100:>5.1f}%  |  "
              f"BH-QQQ CAGR={bq['cagr']*100:>6.2f}%")
        return rot, b3, bq

    print("\n=== windows (rotation vs buy-hold-3x vs buy-hold-QQQ) ===")
    rot_h, b3_h, bq_h = report("2000-2013 UNSEEN", *HOSTILE)
    report("2014-2026 seen", *OVL)
    report("2000-2026 full", *FULL)

    print("\n=== KILL CRITERIA (2000-2013 unseen; prereg 09a3a31) ===")
    c1 = rot_h["cagr"] > 0
    c2 = rot_h["mdd"] <= 0.65 and rot_h["mdd"] <= b3_h["mdd"] - 0.25
    c3 = rot_h["cagr"] >= bq_h["cagr"]
    for name, ok, val in [
        ("val gate", val_ok, f"corr {rho:.3f}"),
        ("1 CAGR>0", c1, f"{rot_h['cagr']*100:.1f}%"),
        ("2 maxDD<=65 & >=25pp below BH-3x", c2,
         f"{rot_h['mdd']*100:.1f}% vs BH-3x {b3_h['mdd']*100:.1f}%"),
        ("3 CAGR>=BH-QQQ", c3,
         f"{rot_h['cagr']*100:.1f}% vs {bq_h['cagr']*100:.1f}%"),
    ]:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:34} ({val})")
    verdict = val_ok and c1 and c2 and c3
    print(f"\n  E5 VERDICT: {'PASS' if verdict else 'FAIL'}")


if __name__ == "__main__":
    main()
