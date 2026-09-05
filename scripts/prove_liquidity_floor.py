r"""Proof that the liquidity floor FAILS CLOSED on unmeasurable volume (finding 4,
2026-09-05). Pure in-memory: no DB, no network, no orders. Run:

    .venv\Scripts\python.exe scripts\prove_liquidity_floor.py

Before the fix the call site read `adv is not None and adv < FLOOR`, so
median_dollar_volume() returning None -- fewer than max(5, 20//2)=10 sessions
with usable close AND volume -- meant the name was never tested and went
straight into the K=4 stress basket. These four cases pin the new behaviour.

DATA CONVENTION: synthetic bars only; no price_cache read, so no adjustment
convention applies.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from daily_swing_paper import median_dollar_volume  # noqa: E402
from swing_bot import universe  # noqa: E402

FLOOR = universe.MIN_MEDIAN_DOLLAR_VOL


def bars(n, price, volume):
    ds = ["2026-%02d-%02d" % (1 + i // 28, 1 + i % 28) for i in range(n)]
    return ds, {d: price for d in ds}, {d: volume for d in ds}


def screen(ds, cl, vol, asof):
    """The exact branch now at daily_swing_paper.py:836-846."""
    adv = median_dollar_volume(ds, cl, vol, n=20, asof=asof)
    if adv is None:
        return "EXCLUDED-unknown"
    if adv < FLOOR:
        return "EXCLUDED-illiquid"
    return "RANKED"


def old_screen(ds, cl, vol, asof):
    """The pre-fix branch, kept to show the difference is real."""
    adv = median_dollar_volume(ds, cl, vol, n=20, asof=asof)
    if adv is not None and adv < FLOOR:
        return "EXCLUDED-illiquid"
    return "RANKED"


ok = True
n_run = 0
n_pass = 0


def t(name, got, want):
    # Counts are DERIVED, never written by hand: the first version of this file
    # printed "GREEN (12/12)" while 11 cases ran, because the total was a
    # literal. A checker that miscounts itself is not a checker (2026-09-05).
    global ok, n_run, n_pass
    good = got == want
    ok = good and ok
    n_run += 1
    n_pass += bool(good)
    print("%-4s %-46s got=%-18s want=%s" % ("PASS" if good else "FAIL", name, got, want))


# 1. Healthy, liquid name -> ranked.
ds, cl, vol = bars(30, 100.0, 5_000_000)          # $500M/day
t("liquid, 30 bars", screen(ds, cl, vol, ds[-1]), "RANKED")

# 2. Healthy history, genuinely thin -> excluded by the floor as before.
ds, cl, vol = bars(30, 1.0, 100)                  # $100/day
t("illiquid, 30 bars", screen(ds, cl, vol, ds[-1]), "EXCLUDED-illiquid")

# 3. Data-starved: 9 usable bars < max(5, 10). THE FIX.
ds, cl, vol = bars(9, 100.0, 5_000_000)
t("9 bars -> unknown, fail closed", screen(ds, cl, vol, ds[-1]), "EXCLUDED-unknown")
t("  ...and the OLD branch ranked it", old_screen(ds, cl, vol, ds[-1]), "RANKED")

# 4. Feed gap: 30 dates, only 4 carry volume (a halt, or a broken feed).
ds, cl, vol = bars(30, 100.0, 5_000_000)
for d in ds[:-4]:
    vol[d] = 0                                    # falsy -> not usable
t("volume gap -> unknown, fail closed", screen(ds, cl, vol, ds[-1]), "EXCLUDED-unknown")
t("  ...and the OLD branch ranked it", old_screen(ds, cl, vol, ds[-1]), "RANKED")


# --- liquidity_mask, added 2026-09-05 for F3 -------------------------------
# The research runners screen candidates through this before ranking them, so
# a wrong mask silently changes which names an experiment holds. Bars use the
# cached layout (ticker, date, o, h, l, c, adj, vol).


def mkbars(vols, price=100.0):
    return [["T", "2026-01-%02d" % (i + 1), price, price, price, price, price, v]
            for i, v in enumerate(vols)]


# 5. Fail closed at the START of a series: the first 9 indices have fewer than
#    max(5, 20//2)=10 bars behind them, so liquidity is UNKNOWN, not adequate.
m = universe.liquidity_mask(mkbars([5_000_000] * 30))
t("mask fails closed for i<9", m[:10], [False] * 9 + [True])
t("mask true once measurable", all(m[9:]), True)

# 6. PAST-ONLY. A series that is illiquid then liquid must not light up early:
#    index 14 sees ten $100 bars behind it, and no amount of later volume can
#    reach back. Recomputing on the truncated prefix must give the same answer.
vols = [1] * 15 + [5_000_000] * 15
m = universe.liquidity_mask(mkbars(vols))
t("illiquid prefix stays False", any(m[:15]), False)
t("past-only: prefix recompute matches",
  universe.liquidity_mask(mkbars(vols)[:20]), m[:20])

# 7. A zero-volume bar is NOT usable, so a name whose feed dies mid-series
#    falls back to unknown rather than coasting on its old median.
m = universe.liquidity_mask(mkbars([5_000_000] * 15 + [0] * 15))
t("feed death -> False, not coasting", m[-1], False)

print("\nFLOOR = $%.0fM/day (universe.MIN_MEDIAN_DOLLAR_VOL)" % (FLOOR / 1e6))
print("LIQUIDITY FLOOR PROOF: %s (%d/%d)" % ("GREEN" if ok else "RED", n_pass, n_run))
sys.exit(0 if ok else 1)
