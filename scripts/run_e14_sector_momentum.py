"""E14 - diversified sector momentum, per prereg f922f1f.

Top-3 of the 11 SPDR sectors by trailing 126-session return, rebalance every
21 sessions, next-open full rebalance, 5 bps/side, NAV/3. Survivorship-clean.
D1 dual-bar verdict. Reuses .e8e9_cache; no swing.db writes.

DATA CONVENTION: yfinance auto_adjust=False -> split-adjusted,
dividend-UNADJUSTED.

NAV (finding-things map): imports run_e8_squeeze (CAP0, COST, cache_fetch).
Imported by: run_ex_decomp.py.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e8_squeeze import cache_fetch, COST, CAP0, f3_masks_by_date

SECTORS = ["XLE", "XLF", "XLK", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB",
           "XLRE", "XLC"]
K = 3
LOOK = 126
REBAL = 21
GATE = ("2000-01-01", "2013-12-31")
SEC = ("2014-01-01", "2099-01-01")
FULL = ("2000-01-01", "2099-01-01")


def stats(nav):
    if len(nav) < 30 or nav[0] <= 0:
        return None
    rets = [nav[i] / nav[i - 1] - 1 for i in range(1, len(nav)) if nav[i - 1] > 0]
    yrs = len(nav) / 252.0
    cagr = (nav[-1] / nav[0]) ** (1 / yrs) - 1 if nav[-1] > 0 else -1.0
    mu = sum(rets) / len(rets)
    sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
    sh = mu / sd * math.sqrt(252) if sd > 0 else float("nan")
    peak, mdd = nav[0], 0.0
    for v in nav:
        peak = max(peak, v)
        mdd = max(mdd, (peak - v) / peak)
    return dict(cagr=cagr, mo=(1 + cagr) ** (1 / 12) - 1, mdd=mdd, sharpe=sh)


def main():
    data, raw = {}, {}
    for t in SECTORS:
        bars = cache_fetch(t)
        raw[t] = bars
        data[t] = {b[1]: (b[2], b[5]) for b in bars}   # date -> (open, close)
        print(f"loaded {t}: {bars[0][1]}..{bars[-1][1]} ({len(bars)} bars)",
              flush=True)
    # F3 (PRD M13.4, 2026-09-05): E14 was the one in-scope ETF experiment the
    # F3 redirect never measured -- its prereg scoped it as a count, not a
    # verdict. `data` keeps only (open, close) and drops volume, so the masks
    # are built from `raw`, the same cache_fetch bars, exactly as X9 and E20 do.
    # Applied at RANKING: an illiquid name cannot enter the top-K momentum
    # queue. SPY is the benchmark, not a candidate, so it is not screened --
    # same convention as every other F3 runner.
    LIQ = f3_masks_by_date(raw)
    spy = {b[1]: (b[2], b[5]) for b in cache_fetch("SPY")}

    dates = sorted(set().union(*[set(d) for d in data.values()]))
    cash, pos, pend = CAP0, {}, None      # pos: ticker -> shares
    nav_by_date, entries = {}, []
    n_illiquid = n_rebal = n_candidates = n_no_quorum = 0
    illiquid_by_ticker, illiquid_dates = {}, []
    for i, d in enumerate(dates):
        if pend is not None and (i - pend[1]) >= 1:
            targets = pend[0]
            navv = cash + sum(pos[t] * data[t][d][1] for t in pos if d in data[t])
            for t in list(pos):
                if d in data[t]:
                    cash += pos[t] * data[t][d][0] * (1 - COST)
                    del pos[t]
            per = navv / K
            for t in targets:
                if d in data[t] and data[t][d][0] > 0:
                    sh = per / (data[t][d][0] * (1 + COST))
                    cash -= sh * data[t][d][0] * (1 + COST)
                    pos[t] = sh
                    entries.append(d)
            pend = None
        nav_by_date[d] = cash + sum(pos[t] * data[t][d][1]
                                    for t in pos if d in data[t])
        if i >= LOOK + 1 and i % REBAL == 0 and i + 1 < len(dates):
            prev = dates[i - 1]
            base = dates[i - 1 - LOOK]
            mom = []
            for t in SECTORS:
                if prev in data[t] and base in data[t] and data[t][base][1] > 0:
                    if LIQ is not None and not LIQ[t].get(prev, False):
                        n_illiquid += 1
                        illiquid_by_ticker[t] = illiquid_by_ticker.get(t, 0) + 1
                        illiquid_dates.append(prev)
                        continue
                    mom.append((data[t][prev][1] / data[t][base][1] - 1, t))
            mom.sort(reverse=True)
            n_rebal += 1
            n_candidates += len(mom)
            if len(mom) >= K:
                pend = ([t for _, t in mom[:K]], i)
            else:
                # The floor does not only RE-RANK: when it leaves fewer than K
                # eligible sectors the rebalance cannot fire at all and the
                # strategy sits in cash. Counted rather than inferred from the
                # entry delta (PRD M13.4).
                n_no_quorum += 1

    def win(series_dict, lo, hi, base=None):
        ds = [d for d in dates if lo <= d <= hi and d in series_dict]
        if base is None:
            return [series_dict[d] for d in ds]
        return [series_dict[d][1] / series_dict[ds[0]][1] for d in ds]

    def ew(lo, hi):
        ds = [d for d in dates if lo <= d <= hi]
        out = []
        avail0 = [t for t in SECTORS if ds[0] in data[t]]
        for d in ds:
            vals = [data[t][d][1] / data[t][ds[0]][1] for t in avail0 if d in data[t]]
            out.append(sum(vals) / len(vals) if vals else 1.0)
        return out

    print(f"\ncommon dates {dates[0]}..{dates[-1]} ({len(dates)}); "
          f"total entries {len(entries)}")
    if LIQ is None:
        print("F3 count: floor OFF (SWING_F3_FLOOR=0) -- no candidate screened.")
    else:
        print("F3 count: %d of %d ticker-rebalance candidacies dropped by the "
              "$20M/day floor across %d rebalances (%.2f%%)."
              % (n_illiquid, n_illiquid + n_candidates, n_rebal,
                 100.0 * n_illiquid / max(1, n_illiquid + n_candidates)))
        if n_illiquid:
            print("  by ticker: %s" % ", ".join(
                "%s=%d" % kv for kv in sorted(illiquid_by_ticker.items())))
            print("  date range of drops: %s..%s"
                  % (min(illiquid_dates), max(illiquid_dates)))
            print("  rebalances that could not fire (fewer than K=%d eligible, "
                  "so the strategy sat in CASH): %d of %d"
                  % (K, n_no_quorum, n_rebal))
    rows = {}
    for name, (lo, hi) in [("GATE 2000-2013", GATE), ("SECONDARY 2014-", SEC),
                           ("FULL 2000-", FULL)]:
        s = stats(win(nav_by_date, lo, hi))
        b = stats(win(spy, lo, hi, base=True))
        e = stats(ew(lo, hi))
        rows[name] = (s, b)
        ne = sum(1 for d in entries if lo <= d <= hi)
        print(f"\n{name}: E14 CAGR {s['cagr']*100:.2f}% ({s['mo']*100:.2f}%/mo) "
              f"maxDD {s['mdd']*100:.1f}% Sharpe {s['sharpe']:.2f} | "
              f"SPY {b['cagr']*100:.2f}%/{b['sharpe']:.2f} | "
              f"EW-sectors {e['cagr']*100:.2f}%/{e['sharpe']:.2f} | entries {ne}")

    g, gb = rows["GATE 2000-2013"]
    sec, secb = rows["SECONDARY 2014-"]
    n_gate = sum(1 for d in entries if GATE[0] <= d <= GATE[1])
    hr = (g["cagr"] >= 0.15 and g["mdd"] <= 0.60
          and sec["cagr"] >= 0.15 and sec["mdd"] <= 0.60)
    ra = (g["sharpe"] >= 0.80 and g["sharpe"] > gb["sharpe"]
          and sec["sharpe"] > secb["sharpe"] and g["cagr"] > 0 and sec["cagr"] > 0)
    floor = n_gate >= 30
    print(f"\n=== D1 VERDICT (prereg f922f1f) ===")
    print(f"  gate entries {n_gate} (>=30: {'ok' if floor else 'INCONCLUSIVE'})")
    print(f"  [{'PASS' if hr else 'fail'}] PASS-HR (CAGR>=15% & DD<=60% both)")
    print(f"  [{'PASS' if ra else 'fail'}] PASS-RA (gate Sharpe>=0.80={g['sharpe']:.2f}"
          f" & >SPY both: {g['sharpe']:.2f}>{gb['sharpe']:.2f},"
          f" {sec['sharpe']:.2f}>{secb['sharpe']:.2f})")
    verdict = ("INCONCLUSIVE" if not floor else
               "PASS-HR" if hr else "PASS-RA" if ra else "FAIL")
    print(f"\n  E14 VERDICT: {verdict}")
    # EX-DECOMP hook (M9 #44): honest null = EW-sectors buy-hold; additive only.
    ewrows = {name: (rows[name][0], stats(ew(lo, hi)))
              for name, (lo, hi) in [("GATE 2000-2013", GATE),
                                     ("SECONDARY 2014-", SEC), ("FULL 2000-", FULL)]}
    return {"rows": ewrows, "n_gate": n_gate, "bench": "EW-sectors"}


if __name__ == "__main__":
    main()
