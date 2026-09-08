r"""Unconditional overnight vs intraday return decomposition on the broad-US ETFs.

    set SWING_ALLOW_STALE_CACHE=1
    .venv\Scripts\python.exe scripts\ablation_overnight_decomp.py

DIAGNOSTIC. No PASS/FAIL, no D1 verdict, nothing deployed, ATTEMPT TALLY
UNCHANGED (precedent: EX-DECOMP, record DU/M12, X9's zero-cost split). It does
not reopen the closed search phase; it tests a CITED PRIOR against our own data.

WHY. `docs/research/2026-07-13_execution_microstructure.md:53-55` says the NY Fed
dates the overnight drift "flat since 2021". That sentence carries no sample, no
universe and no magnitude, it has never been checked here, and it is half of X4's
pre-registered prior (PRD_ROADMAP.md:1026). ablation_fill_timing.py measured the
overnight leg only on IBS<0.20 signals, averaged rather than compounded, gross
only, on swing.db (2014+). Nothing in this repo has ever decomposed returns
UNCONDITIONALLY. This does.

TWO THINGS THIS CANNOT AND CAN DO, stated before any number is printed:
  * It CANNOT answer "did the drift die after 2021". The overnight leg's vol is
    ~10.6%/yr, so a 4.6-year window carries a standard error near +-5 pp/yr
    against an effect of ~1-2 pp/yr. Resolving that at 2 sigma needs ~200 years.
    Every era row therefore prints a CI, and the era table is descriptive.
  * It CAN settle viability, and that answer needs no era split at all. An
    overnight-only trade is a full round trip every session, so breakeven
    per-side cost is (G-1)/(G+1) on the daily geometric overnight factor G.

DATA CONVENTION. Reads BOTH price conventions from the shared cache_fetch bars:
`close` (idx 5) is SPLIT-ADJUSTED and DIVIDEND-UNADJUSTED, `adj_close` (idx 6) is
split+dividend adjusted (yfinance auto_adjust=False provenance, prices.py:109).
THE DIFFERENCE BETWEEN THEM IS THIS DIAGNOSTIC'S SUBJECT: on dividend-unadjusted
prices the ex-dividend drop falls entirely in the close[t-1]->open[t] window, so
a price-only overnight leg is understated by the whole dividend yield (~183 bps/yr
on SPY) -- the same order as the effect under test, and differential across
tickers (QQQ ~51 bps/yr), so a price-only cross-ticker table measures dividend
policy rather than drift.

STATS CONVENTIONS, PRE-COMMITTED so "flat" cannot be phrased 32 ways:
PRIMARY = SPY, total-return arm, LOG space, both cut-points reported. Log is
primary because the arithmetic-minus-log wedge is sigma^2/2 and differs per leg,
handing intraday a spurious +0.59 pp/yr on SPY and +1.63 on QQQ -- larger than
the effect. Arithmetic bps/day is a LABELED SECONDARY, never mixed in one table.

NAV (finding-things map): imports run_e8_squeeze.{cache_fetch, COST} and
swing_bot.universe. Imported by nothing. Writes nothing; swing.db is never opened.
"""
import json
import math
import os
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# SWING_ALLOW_STALE_CACHE must be set EXTERNALLY. Setting it here, or wrapping
# cache_fetch in `except`, is the record-EO defect class: it turned "refuse to
# run" into "run on a silently emptied universe". Let StaleCacheError propagate.
from run_e8_squeeze import CACHE, COST, cache_fetch  # noqa: E402
from swing_bot import universe  # noqa: E402

TRADING_DAYS = 252.0
DIV_XCHECK_THROUGH = "2026-06-30"   # *_div.json vintage 2026-07-11; bars 2026-08-18
CUTS = [("2021-01-01", "the cited claim's literal reading"),
        ("2022-01-01", "the repo's E1b train/holdout split -- coincidence, NOT "
                       "a prior about a break in overnight drift")]


def legs(bars):
    """Per-session log legs. Returns a list of dicts, one per session from bar 1.

    F_TR  = adj[t]/adj[t-1]                 total return
    F_ID  = close[t]/open[t]                intraday, dividend-free by construction
    F_ON  = F_TR * (open[t]/close[t])       overnight INCLUDING the dividend
    F_ONp = open[t]/close[t-1]              overnight, PRICE-ONLY (the naive arm)

    F_ON * F_ID == F_TR exactly, so log F_ON + log F_ID == log F_TR per day and
    that identity survives summing over ANY date subset -- which is why every
    aggregate below is computed in logs and converted only at print time.
    Bar 0 is dropped: it has no prior close.
    """
    out = []
    for i in range(1, len(bars)):
        p, b = bars[i - 1], bars[i]
        o, c, adj = b[2], b[5], b[6]
        f_tr = adj / p[6]
        f_id = c / o
        f_on = f_tr * (o / c)
        out.append(dict(date=b[1], f_tr=f_tr, f_id=f_id, f_on=f_on,
                        f_onp=o / p[5], synth_open=(o == p[5])))
    return out


def ann(rows, key):
    """Annualized pp/yr from summed daily logs -- the primary statistic."""
    if not rows:
        return float("nan")
    tot = sum(math.log(r[key]) for r in rows)
    return 100.0 * (tot / len(rows)) * TRADING_DAYS


def se_ann(rows, key):
    """Standard error of the annualized figure, in pp/yr."""
    if len(rows) < 2:
        return float("nan")
    sd = statistics.stdev([math.log(r[key]) for r in rows])
    return 100.0 * sd * math.sqrt(TRADING_DAYS / len(rows)) * math.sqrt(TRADING_DAYS)


def selfcheck(t, bars, rws, fails):
    """Three checks. #1 is tautological by construction and catches only coding
    slips -- F_ON is DEFINED as F_TR/F_ID, so it holds even if `open` is garbage.
    #2 is the one that binds: it ties the legs to the raw bars, so a dropped,
    duplicated or misaligned session fails it. #3 binds the dividend correction
    to an independent source.
    Tolerance 1e-10: deterministic bound N*2eps ~ 3.7e-12, observed ~6e-15, so it
    can only fire on a structural bug, never on rounding."""
    def prod(key):
        v = 1.0
        for r in rws:
            v *= r[key]
        return v

    def rel(a, b):
        return abs(a / b - 1.0)

    # 1. decomposition identity
    d1 = rel(prod("f_on") * prod("f_id"), prod("f_tr"))
    # 2. telescoping -- binds open, both closes, and every bar's presence/order
    d2 = rel(prod("f_tr"), bars[-1][6] / bars[0][6])
    d3 = rel(prod("f_onp") * prod("f_id"), bars[-1][5] / bars[0][5])
    # back-adjustment anchor: the newest bar must be unadjusted
    d4 = abs(bars[-1][6] / bars[-1][5] - 1.0)
    for name, d, tol in [("decomposition", d1, 1e-10), ("telescope-TR", d2, 1e-10),
                         ("telescope-price", d3, 1e-10), ("adj-anchor", d4, 1e-10)]:
        status = "ok" if d < tol else "FAIL"
        print("    %-16s %-5s  %.2e" % (name, status, d))
        if d >= tol:
            fails.append("%s %s %.2e" % (t, name, d))

    # 3. dividend attribution vs the independent *_div.json. Yahoo's adjustment
    # is MULTIPLICATIVE -- k = 1/(1 - D/close[t-1]) -- not additive.
    divf = CACHE / ("%s_div.json" % t)
    if not divf.exists():
        print("    dividend-xcheck  SKIP   no %s" % divf.name)
        return
    divs = json.loads(divf.read_text(encoding="utf-8"))
    # rws[j] is built from bars[j+1], so its prior close is bars[j][5].
    prev_close = {r["date"]: bars[j][5] for j, r in enumerate(rws)}
    by_date = {r["date"]: r for r in rws}
    worst, n_ck = 0.0, 0
    for d, amt in sorted(divs.items()):
        if d > DIV_XCHECK_THROUGH or d not in by_date:
            continue
        r = by_date[d]
        implied = r["f_on"] / r["f_onp"] - 1.0
        expect = amt / (prev_close[d] - amt)
        worst = max(worst, abs(implied - expect))
        n_ck += 1
    status = "ok" if worst < 5e-5 else "FAIL"
    print("    dividend-xcheck  %-5s  %.2e  (%d ex-dates)" % (status, worst, n_ck))
    if worst >= 5e-5:
        fails.append("%s dividend-xcheck %.2e" % (t, worst))


def era(rows, lo=None, hi=None):
    return [r for r in rows if (lo is None or r["date"] >= lo)
            and (hi is None or r["date"] < hi)]


def main():
    if os.environ.get("SWING_ALLOW_STALE_CACHE") != "1":
        print("NOTE: the cache is a frozen 2026-08-17 vintage and this is a "
              "deliberate historical run.\n      Set SWING_ALLOW_STALE_CACHE=1 "
              "externally; cache_fetch will refuse otherwise.\n", flush=True)

    tks = universe.tickers(group="broad_us")
    print("=" * 78)
    print("OVERNIGHT vs INTRADAY DECOMPOSITION -- DIAGNOSTIC, no verdict, tally "
          "unchanged")
    print("=" * 78)
    print("Legs: F_ON = adj[t]/adj[t-1] * open[t]/close[t]   (overnight, incl. "
          "dividend)")
    print("      F_ID = close[t]/open[t]                     (intraday, "
          "dividend-free)")
    print("      F_ONp = open[t]/close[t-1]                  (overnight, "
          "PRICE-ONLY)")
    print("Primary statistic: annualized pp/yr from summed daily LOGS.\n")

    data, fails = {}, []
    for t in tks:
        bars = cache_fetch(t)
        rws = legs(bars)
        data[t] = rws
        print("%s: %d bars %s..%s -> %d sessions %s..%s"
              % (t, len(bars), bars[0][1], bars[-1][1], len(rws),
                 rws[0]["date"], rws[-1]["date"]))
        selfcheck(t, bars, rws, fails)

    if fails:
        print("\n!! SELF-CHECKS FAILED: %s" % "; ".join(fails))
        return 1

    # ---- per-year table (primary ticker first) ----
    for t in tks:
        rws = data[t]
        print("\n" + "-" * 78)
        print("%s -- per year (pp/yr, log space).  SE is on the OVERNIGHT leg."
              % t)
        print("%-6s %9s %9s %9s %8s %9s %9s %6s %5s"
              % ("year", "overnite", "intraday", "total", "SE", "cumON", "cumID",
                 "synth", "n"))
        years = sorted({r["date"][:4] for r in rws})
        cum_on = cum_id = 0.0
        for y in years:
            g = [r for r in rws if r["date"][:4] == y]
            cum_on += sum(math.log(r["f_on"]) for r in g)
            cum_id += sum(math.log(r["f_id"]) for r in g)
            print("%-6s %9.2f %9.2f %9.2f %8.2f %9.3f %9.3f %6d %5d"
                  % (y, ann(g, "f_on"), ann(g, "f_id"), ann(g, "f_tr"),
                     se_ann(g, "f_on"), cum_on, cum_id,
                     sum(1 for r in g if r["synth_open"]), len(g)))
        print("  cumON/cumID are cumulative LOG NAV of each leg at year end.")
        print("  synth = sessions with open == prior close EXACTLY: the overnight")
        print("          leg is mechanically 0 and the session dumps into "
              "intraday.")

    # ---- era rows, both cut-points, every one with a CI ----
    print("\n" + "=" * 78)
    print("ERA ROWS -- annualized pp/yr with a 95% CI (+-1.96 SE) on each leg.")
    print("A CI this wide is the finding: the era comparison cannot resolve a")
    print("1-2 pp/yr effect. Read it as descriptive, not as a test.")
    print("=" * 78)
    for t in tks:
        rws = data[t]
        print("\n%s" % t)
        rows = [("full", rws)]
        for cut, _why in CUTS:
            rows.append(("< " + cut, era(rws, hi=cut)))
            rows.append((">= " + cut, era(rws, lo=cut)))
        for label, g in rows:
            if not g:
                continue
            s = se_ann(g, "f_on")
            print("  %-14s n=%5d  overnight %7.2f +- %5.2f   intraday %7.2f   "
                  "priceonly-ON %7.2f"
                  % (label, len(g), ann(g, "f_on"), 1.96 * s, ann(g, "f_id"),
                     ann(g, "f_onp")))
    print("\n  Cut-point labels: %s" % "; ".join("%s = %s" % c for c in CUTS))

    # ---- robustness: SPY from 1996 (early synthetic opens) ----
    spy = data["SPY"]
    g96 = era(spy, lo="1996-01-01")
    print("\nROBUSTNESS  SPY from 1996-01-01 (drops the 14.2%% synthetic-open "
          "1993):\n  n=%d  overnight %.2f  intraday %.2f  (full: %.2f / %.2f)"
          % (len(g96), ann(g96, "f_on"), ann(g96, "f_id"),
             ann(spy, "f_on"), ann(spy, "f_id")))

    # ---- matched-length window percentile: the fair form of the question ----
    print("\n" + "=" * 78)
    print("MATCHED-LENGTH TEST -- comparing a 4.6y window to a 29y window is not")
    print("a fair test (the long window's SE is ~5x tighter). Instead: where does")
    print("the CURRENT window's overnight drift sit among ALL overlapping windows")
    print("of the SAME length? Descriptive only -- overlapping windows are")
    print("autocorrelated, so this is a percentile, NOT a p-value.")
    print("=" * 78)
    for t in tks:
        rws = data[t]
        for cut, _ in CUTS:
            cur = era(rws, lo=cut)
            w = len(cur)
            if w < 30 or len(rws) < 2 * w:
                continue
            lg = [math.log(r["f_on"]) for r in rws]
            run, sums = sum(lg[:w]), []
            sums.append(run)
            for i in range(w, len(lg)):
                run += lg[i] - lg[i - w]
                sums.append(run)
            cur_sum = sum(math.log(r["f_on"]) for r in cur)
            pct = 100.0 * sum(1 for s in sums if s <= cur_sum) / len(sums)
            print("  %-5s window %4dd from %s: %.2f pp/yr = %5.1fth pctile of "
                  "%d windows" % (t, w, cut, ann(cur, "f_on"), pct, len(sums)))

    # ---- the decisive arithmetic: cost ----
    print("\n" + "=" * 78)
    print("VIABILITY -- needs NO era split. An overnight-only trade is a FULL")
    print("ROUND TRIP every session: F_net = F_ON * (1-c)/(1+c), the repo's")
    print("multiplicative buy*(1+c)/sell*(1-c) convention (run_e8_squeeze:349).")
    print("Breakeven per side c* = (G-1)/(G+1) on the daily geometric factor G.")
    print("=" * 78)
    print("%-5s %10s %12s %s" % ("", "gross", "breakeven", "net pp/yr at c ="))
    print("%-5s %10s %12s %8s %8s %8s %8s"
          % ("", "pp/yr", "bps/side", "1bp", "2bps", "5bps", "10bps"))
    for t in tks:
        rws = data[t]
        g = math.exp(sum(math.log(r["f_on"]) for r in rws) / len(rws))
        cstar = 10000.0 * (g - 1.0) / (g + 1.0)
        nets = []
        for cb in (1, 2, 5, 10):
            c = cb / 10000.0
            nets.append(100.0 * (math.exp(math.log(g) + math.log((1 - c) / (1 + c)))
                                 ** TRADING_DAYS - 1.0))
        print("%-5s %10.2f %12.2f %8.1f %8.1f %8.1f %8.1f"
              % (t, ann(rws, "f_on"), cstar, *nets))
    print("\n  This project prices %.0f bps/side (run_e8_squeeze.COST). Compare "
          "that\n  against the breakeven column: the gap is the whole answer, "
          "and it is\n  arithmetic forced by ~252 round trips a year, not an "
          "estimate."
          % (COST * 10000))

    # ---- secondary + honesty block ----
    print("\n" + "=" * 78)
    print("SECONDARY (labeled, never mixed with the log table): arithmetic "
          "bps/day")
    print("=" * 78)
    print("%-5s %12s %12s %12s %12s" % ("", "ON mean", "ON median", "ID mean",
                                        "ID median"))
    for t in tks:
        rws = data[t]
        on = [10000.0 * (r["f_on"] - 1) for r in rws]
        idl = [10000.0 * (r["f_id"] - 1) for r in rws]
        print("%-5s %12.3f %12.3f %12.3f %12.3f"
              % (t, statistics.mean(on), statistics.median(on),
                 statistics.mean(idl), statistics.median(idl)))
    print("  The overnight leg is heavy-tailed, so the median is here on "
          "purpose.")

    print("\nLEG CORRELATIONS (overnight) -- pooling does NOT help: these move")
    print("together, so an equal-weight basket is no tighter than SPY alone.")
    n = min(len(data[t]) for t in tks)
    tail = {t: [math.log(r["f_on"]) for r in data[t][-n:]] for t in tks}
    print("      " + "".join("%8s" % t for t in tks))
    for a in tks:
        print("%-6s" % a + "".join("%8.3f" % statistics.correlation(tail[a],
                                                                    tail[b])
                                   for b in tks))

    print("\nDISCLOSED, NOT CORRECTED:")
    print("  * COVID (Feb-Apr 2020) sits in the PRE window under BOTH cut-points.")
    print("  * 3 'overnights' are multi-day closures, not overnights: 2001-09-17")
    print("    (7d, the 9/11 closure and SPY's 3rd-largest |overnight| move),")
    print("    2007-01-03, 2012-10-31.")
    print("  * The legs are NOT per-unit-time comparable: overnight spans ~72% of")
    print("    calendar time, intraday ~28%. 'Overnight beats intraday' is a")
    print("    PER-SESSION statement only.")
    print("  * We do not know whether the NY Fed source measured price-only or")
    print("    total return. If it measured one and we compare the other, a")
    print("    mismatch is a DEFINITIONAL ARTIFACT, not a failed reproduction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
