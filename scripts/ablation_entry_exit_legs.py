r"""Entry-leg vs exit-leg split of C1's close-to-close -> next-open gap.

    set SWING_ALLOW_STALE_CACHE=1
    .venv\Scripts\python.exe scripts\ablation_entry_exit_legs.py

DIAGNOSTIC. No PASS/FAIL, no D1 verdict, nothing deployed, ATTEMPT TALLY
UNCHANGED (precedent: EX-DECOMP record DU/M12, X9's zero-cost split, GD's
overnight decomposition). It does not reopen the closed search phase and it
tunes nothing: every C1 parameter is imported from the runner, never restated.

DATA CONVENTION. Prices SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED (auto_adjust=False),
inherited from the shared .e8e9_cache via run_e8_squeeze.cache_fetch. This
UNDERSTATES both overnight legs by the whole dividend yield, because on
dividend-unadjusted prices the ex-dividend drop falls entirely in the
close[t-1]->open[t] window (GD sec. 4). The two legs are affected in the same
direction, so their DIFFERENCE -- the reconciled gap -- is far more robust than
either leg's level. Levels are reported as a floor, not a point.

WHY. The record (GE sec. 6) and PRD X4 both rest on "C1 leaks ~5 pp/yr moving
from close-to-close (22.82%) to next-open (17.87%), and that leak is at ENTRY."
The first half is measured. The second half has never been: run_c1_residual_
reversal.py:135-139 routes BOTH the exit fill (:146) and the entry fill
(:149-151) through ONE px() closure, so the runner's c2c flag moves both at
once. (Those citations read :129-133/:139/:144 until 2026-09-09; audit GJ found
the same mis-read baked into this docstring, record GF and the C1 results doc at
once.) The
4.95 pp is therefore a NET of two opposing effects, because moving the exit from
close to open GAINS an overnight leg at the same time the entry LOSES one:

    c2c - next_open  =  entry_overnight  -  exit_overnight        (per trade, log)

GD measured the unconditional overnight leg as strongly POSITIVE (+9.60 pp/yr
SPY, +13.12 QQQ). If C1's exit leg is positive too, the ENTRY leak is LARGER
than the observed 4.95 pp, and X4's prize is bigger than the headline. If the
exit leg is the larger one, the framing in GE sec. 6 is wrong. Neither has been
measured. This measures it.

WHAT THIS CAN AND CANNOT DO, stated before any number is printed:
  * It CAN size the entry leg, because the 2x2 below is a reconciled identity,
    not an estimate: the two diagonal cells must reproduce C1's already-recorded
    Rung A and Rung B to the penny, and they are asserted, not eyeballed.
  * It CANNOT say whether X4 would PASS. The entry-fixed cell is an UPPER BOUND
    on a market-on-close arm: it assumes a fill exactly at the official close,
    with no auction slippage, no 15:50-snapshot signal decay, and no CLS
    availability. All three are unresolved (X4 is BLOCKED-ON-BROKER-TIER and on
    the EOD-only hard rule). Read it as "is the prize worth unblocking", nothing
    more.

THE 2x2. Cost is held at 0 bps across all four cells so this measures TIMING
only; the cost question is answered separately at the bottom, at the real 5 bps.

                        exit at next open      exit at signal close
    entry at next open   B = as-run 17.87%      (exit-only "fix")
    entry at close       X4 UPPER BOUND         A = c2c 22.82%

NAV (finding-things map): imports run_c1_residual_reversal (ff3_daily, isoweek,
stats, residual_series, K, BETA_N, FORM_N, GATE, SEC); run_e8_squeeze (COST,
CAP0, cache_fetch); run_e10_earnings_drift (UNIV). Imported by nothing.
Writes nothing; swing.db is never opened; C1's runner is never edited.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# SWING_ALLOW_STALE_CACHE must be set EXTERNALLY. Setting it here, or wrapping
# cache_fetch in `except`, is the record-EO defect class. Let it propagate.
from run_c1_residual_reversal import (  # noqa: E402
    BETA_N, FORM_N, GATE, K, SEC, ff3_daily, isoweek, residual_series, stats,
)
from run_e8_squeeze import CAP0, COST, cache_fetch  # noqa: E402
from run_e10_earnings_drift import UNIV  # noqa: E402

# C1's OWN rung numbers, gate window, as printed by run_c1_residual_reversal.py
# itself ("A (c2c, 0bps)" / "B (next-open, 0bps)"). This run must reproduce them.
#
# DO NOT put 22.82 / 17.87 here. Those are M10-1's numbers, not C1's -- record
# Appendix CI (2026-07-14) caveat (5) reads "c2c 22.82% -> next-open 17.87% (~5pp
# in the overnight gap C1 always leaked)", which is the NAGEL SWITCH gate pair
# with a parenthetical crediting the mechanism to C1. Record GE sec. 6 and the
# 2026-09-08 session handoff both restate that pair as C1's own, giving a 4.95 pp
# gap. C1's real gap is 2.78 pp. Corrected here 2026-09-08; this guard is what
# caught it, so it is left loud on purpose.
REF_A_C2C = 28.24      # Rung A, close-to-close, 0 bps
REF_B_NOPEN = 25.46    # Rung B, next-open,      0 bps
RECON_TOL = 0.02       # pp; these are printed to 2 dp, so this is exact-to-print


def build():
    """Load bars + FF3 residual formation values. Identical to C1's main()."""
    ff = ff3_daily()
    oc, tdates, forms = {}, {}, {}
    for t in UNIV:
        bars = cache_fetch(t)
        ds = [b[1] for b in bars]
        cl = [b[5] for b in bars]
        oc[t] = {b[1]: (b[2], b[5]) for b in bars}   # (open, close)
        tdates[t] = ds
        forms[t] = dict(zip(ds, residual_series(ds, cl, ff)))
    master = sorted({d for t in UNIV for d in tdates[t]})
    weekend_set = {master[i] for i in range(len(master) - 1)
                   if isoweek(master[i]) != isoweek(master[i + 1])}
    return oc, tdates, forms, master, weekend_set


def run(oc, tdates, forms, master, weekend_set, cost, entry_close, exit_close,
        size_at_fill=False):
    """C1's run() with px() split in two. Every other line is C1's, unchanged.

    entry_close / exit_close True  -> that fill uses the PRIOR CLOSE (c2c side)
                             False -> that fill uses TODAY'S OPEN (as-run side)

    size_at_fill=False reproduces C1 exactly, INCLUDING a defect it inherits to
    every Rung A in this repo: `navv` is marked at close(d) while a c2c fill
    happens at close(d-1), so the rebalance is SIZED with one day of forward
    information -- on an up day it deploys a larger navv at the cheaper prior
    close. True marks the pre-trade NAV at the same prices the exits actually
    realize, which is what the account would really hold. The difference between
    the two is the size of that artifact; it is reported, not silently fixed,
    because the recorded 28.24% was produced with it.
    """
    cash, pos, pend = CAP0, {}, None
    navd = {}
    entry_legs, exit_legs = [], []
    idx = {t: {d: i for i, d in enumerate(tdates[t])} for t in UNIV}

    def px(t, d, at_close):
        i = idx[t][d]
        if at_close and i > 0:
            return oc[t][tdates[t][i - 1]][1]
        return oc[t][d][0]

    def leg(t, d):
        """log(open[d] / close[d-1]) -- the overnight leg this fill sits on."""
        i = idx[t][d]
        if i == 0:
            return None
        prior_close = oc[t][tdates[t][i - 1]][1]
        today_open = oc[t][d][0]
        if prior_close > 0 and today_open > 0:
            return math.log(today_open / prior_close)
        return None

    for d in master:
        if pend is not None:
            if size_at_fill:
                navv = cash + sum(pos[t] * px(t, d, exit_close)
                                  for t in pos if d in oc[t])
            else:
                navv = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
            for t in list(pos):
                if d in oc[t]:
                    cash += pos[t] * px(t, d, exit_close) * (1 - cost)
                    lg = leg(t, d)
                    if lg is not None:
                        exit_legs.append(lg)
                    del pos[t]
            per = navv / K
            for t in pend:
                if d in oc[t] and px(t, d, entry_close) > 0:
                    p = px(t, d, entry_close)
                    sh = per / (p * (1 + cost))
                    cash -= sh * p * (1 + cost)
                    pos[t] = sh
                    lg = leg(t, d)
                    if lg is not None:
                        entry_legs.append(lg)
            pend = None
        navd[d] = cash + sum(pos[t] * oc[t][d][1] for t in pos if d in oc[t])
        if d in weekend_set:
            ranked = sorted((forms[t].get(d), t) for t in UNIV
                            if forms[t].get(d) is not None)
            if len(ranked) >= K:
                pend = [t for _, t in ranked[:K]]
    return navd, entry_legs, exit_legs


def window_cagr(navd, master, win):
    lo, hi = win
    nav = [navd[d] for d in master if lo <= d <= hi]
    return stats(nav)


def legstats(xs):
    if not xs:
        return 0, float("nan"), float("nan")
    mu = sum(xs) / len(xs)
    if len(xs) > 1:
        sd = math.sqrt(sum((v - mu) ** 2 for v in xs) / (len(xs) - 1))
        se = sd / math.sqrt(len(xs))
    else:
        se = float("nan")
    return len(xs), mu * 10000, se * 10000


def main():
    print("C1 entry-leg vs exit-leg split -- DIAGNOSTIC, no verdict, tally unchanged")
    print(f"C1 params imported, not restated: K={K}, beta {BETA_N}d, formation {FORM_N}d")
    print("loading bars + FF3 ...", flush=True)
    oc, tdates, forms, master, weekend_set = build()
    print(f"  {len(UNIV)} names, {len(master)} sessions, "
          f"{len(weekend_set)} weekly rebalance dates\n", flush=True)

    cells = {}
    for entry_close in (False, True):
        for exit_close in (False, True):
            navd, e_legs, x_legs = run(oc, tdates, forms, master, weekend_set,
                                       0.0, entry_close, exit_close)
            cells[(entry_close, exit_close)] = dict(
                gate=window_cagr(navd, master, GATE),
                sec=window_cagr(navd, master, SEC),
                entry_leg=e_legs, exit_leg=x_legs,
            )

    B = cells[(False, False)]   # as-run:  entry open, exit open
    A = cells[(True, True)]     # c2c:     entry close, exit close
    X = cells[(True, False)]    # X4 UB:   entry close, exit open
    Z = cells[(False, True)]    # exit-only fix: entry open, exit close

    print("=== THE 2x2, gate window 2000-2013, 0 bps, CAGR %/yr ===")
    print(f"{'':22} {'exit @ next open':>18} {'exit @ signal close':>21}")
    print(f"{'entry @ next open':22} {B['gate']['cagr']*100:17.2f}% "
          f"{Z['gate']['cagr']*100:20.2f}%")
    print(f"{'entry @ close (MOC)':22} {X['gate']['cagr']*100:17.2f}% "
          f"{A['gate']['cagr']*100:20.2f}%")

    print("\n=== RECONCILIATION (asserted, not eyeballed) ===")
    got_b, got_a = B['gate']['cagr'] * 100, A['gate']['cagr'] * 100
    ok_b = abs(got_b - REF_B_NOPEN) <= RECON_TOL
    ok_a = abs(got_a - REF_A_C2C) <= RECON_TOL
    print(f"  Rung B next-open 0bps: got {got_b:.2f}%  recorded {REF_B_NOPEN:.2f}%  "
          f"{'MATCH' if ok_b else 'MISMATCH'}")
    print(f"  Rung A c2c       0bps: got {got_a:.2f}%  recorded {REF_A_C2C:.2f}%  "
          f"{'MATCH' if ok_a else 'MISMATCH'}")
    if not (ok_a and ok_b):
        print("\n  RECONCILIATION FAILED -- the split does not reproduce the recorded")
        print("  numbers, so every cell below is untrustworthy. Reporting and stopping.")
        return 1

    gap = got_a - got_b
    entry_only = X['gate']['cagr'] * 100 - got_b
    exit_only = Z['gate']['cagr'] * 100 - got_b
    print(f"\n=== THE SPLIT (gate, pp/yr of CAGR vs the as-run {got_b:.2f}%) ===")
    print(f"  total c2c gap                  {gap:+6.2f} pp   (the recorded ~5 pp)")
    print(f"  attributable to ENTRY timing   {entry_only:+6.2f} pp   "
          f"(move entry open->close, exit unchanged)")
    print(f"  attributable to EXIT timing    {exit_only:+6.2f} pp   "
          f"(move exit open->close, entry unchanged)")
    print(f"  interaction / non-additivity   {gap - entry_only - exit_only:+6.2f} pp")

    ne, mue, see = legstats(B['entry_leg'])
    nx, mux, sex = legstats(B['exit_leg'])
    print("\n=== PER-FILL OVERNIGHT LEGS (log bps, full history, as-run cell) ===")
    print(f"  entry fills  n={ne:5d}  mean {mue:+7.2f} bps  SE {see:5.2f}")
    print(f"  exit fills   n={nx:5d}  mean {mux:+7.2f} bps  SE {sex:5.2f}")
    print(f"  difference               {mue - mux:+7.2f} bps per rebalance")
    print("  (dividend-UNadjusted prices understate BOTH legs; the DIFFERENCE is")
    print("   the robust quantity -- see the header's data-convention note.)")

    print("\n=== SECONDARY WINDOW 2014- (same cells, 0 bps) ===")
    print(f"  as-run {B['sec']['cagr']*100:6.2f}%   entry-fixed {X['sec']['cagr']*100:6.2f}%   "
          f"c2c {A['sec']['cagr']*100:6.2f}%")

    print(f"\n=== THE COST QUESTION, at the real {COST*10000:.0f} bps/side ===")
    for label, (ec, xc) in (("as-run (entry open)", (False, False)),
                            ("entry @ close (MOC)", (True, False))):
        navd, _, _ = run(oc, tdates, forms, master, weekend_set, COST, ec, xc)
        g = window_cagr(navd, master, GATE)
        s = window_cagr(navd, master, SEC)
        print(f"  {label:22} gate {g['cagr']*100:6.2f}%/DD{g['mdd']*100:5.1f}%/Sh{g['sharpe']:5.2f}"
              f" | sec {s['cagr']*100:6.2f}%/DD{s['mdd']*100:5.1f}%/Sh{s['sharpe']:5.2f}")
    print("\n=== IS THE ENTRY PRIZE AN ARTIFACT? sizing mark moved onto the fill ===")
    print("  (C1 sizes each rebalance off navv marked at close(d) while a c2c fill")
    print("   happens at close(d-1) -- one day of forward information in the SIZE.")
    print("   Re-run with the pre-trade mark taken at the exit fill price instead.)")
    fixed = {}
    for label, (ec, xc) in (("as-run (entry open)", (False, False)),
                            ("entry @ close (MOC)", (True, False)),
                            ("exit @ close only", (False, True)),
                            ("c2c both legs", (True, True))):
        navd, _, _ = run(oc, tdates, forms, master, weekend_set, 0.0, ec, xc,
                         size_at_fill=True)
        g = window_cagr(navd, master, GATE)['cagr'] * 100
        fixed[(ec, xc)] = g
        base = cells[(ec, xc)]['gate']['cagr'] * 100
        print(f"  {label:22} {base:6.2f}% -> {g:6.2f}%   artifact {base - g:+5.2f} pp")
    fb = fixed[(False, False)]
    print(f"\n  THE SPLIT with the sizing artifact removed (vs as-run {fb:.2f}%):")
    print(f"    total c2c gap    {fixed[(True, True)] - fb:+6.2f} pp")
    print(f"    ENTRY timing     {fixed[(True, False)] - fb:+6.2f} pp")
    print(f"    EXIT timing      {fixed[(False, True)] - fb:+6.2f} pp")
    print("\n  An MOC arm pays the SAME 5 bps/side round trip as the as-run arm -- the")
    print("  entry fill moves, the trip count does not. This is NOT the overnight-only")
    print("  round-trip-per-session cost wall from GD; C1 holds ~5 sessions.")
    print("\nNo verdict. X4 stays BLOCKED-ON-BROKER-TIER and on the EOD-only rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
