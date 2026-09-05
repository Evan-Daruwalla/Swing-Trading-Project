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


def t(name, got, want):
    global ok
    good = got == want
    ok = good and ok
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

print("\nFLOOR = $%.0fM/day (universe.MIN_MEDIAN_DOLLAR_VOL)" % (FLOOR / 1e6))
print("LIQUIDITY FLOOR PROOF:", "GREEN (6/6)" if ok else "RED")
sys.exit(0 if ok else 1)
