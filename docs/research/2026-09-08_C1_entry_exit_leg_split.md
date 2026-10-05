# C1's entry leg vs its exit leg — the c2c ablation has been measuring the wrong thing

**Swing Trading · 2026-09-08 (CDT) · Evan Daruwalla**

**Type:** DIAGNOSTIC — no D1 verdict, no PASS/FAIL, nothing deployed, **attempt
tally UNCHANGED** (precedent: EX-DECOMP record DU/M12, X9's zero-cost split, GD).
**Runner:** `scripts/ablation_entry_exit_legs.py`. **No prereg**, consistent with
every diagnostic above. C1's runner was **not edited** — it is imported by
`daily_swing_paper.py`, so every parameter is imported, never restated.
**Regression:** `FROZEN TESTS: GREEN (all d=0)` — 12 pinned refs, 19 invariants
(19 when this ran; **22** since audit GJ added three on 2026-09-09).
Both runs byte-identical (F3 protocol), 1,956-byte output.

---

## 0. A correction that has to come first

**`c2c 22.82% → next-open 17.87%` is M10-1's pair, not C1's.**

Record Appendix CI (2026-07-14), caveat (5), reads: *"COST/EXEC-FRAGILE: c2c
22.82% -> next-open 17.87% (~5pp in the overnight gap C1 always leaked)"*. Those
are the **Nagel Switch** gate numbers, with a parenthetical crediting the
*mechanism* to C1. Downstream that compressed into a claim about C1 itself —
record GE §6 ("C1 leaked ~5 pp/yr moving from close-to-close (22.82% CAGR) to
next-open fills (17.87%)"), and the 2026-09-08 session handoff, which restated it
again.

C1's own runner prints its rungs. Gate window, 0 bps: **Rung A c2c = 28.24%,
Rung B next-open = 25.46%**. C1's gap is **2.78 pp**, not 4.95 pp.

This was caught by a reconciliation assert, not by reading. The diagnostic was
written with 22.82/17.87 as its reference constants, refused to report any cell
because they did not reproduce, and printed `MISMATCH` twice. The guard is left
loud on purpose (`ablation_entry_exit_legs.py:79-90`).

## 1. Why a c2c ablation cannot answer "how much is at entry"

`run_c1_residual_reversal.py:135-139` defines one `px()` closure and uses it for
**both** the exit fill (`:146`) and the entry fill (`:149-151`). So the runner's
`c2c` flag moves both fills at once, and the identity is:

```
c2c − next_open  =  entry_overnight − exit_overnight
```

Moving the entry from open to close **gains** an overnight leg. Moving the exit
from open to close **loses** one. The recorded gap is the *net*, and the two
terms have opposite signs — so the gap systematically understates whichever leg
is larger. Splitting `px()` into `px_entry` / `px_exit` gives a 2×2 whose
off-diagonal cell (entry at close, exit at next open) is exactly the fill pattern
an X4 market-on-close arm would have.

## 2. The 2×2 — gate window 2000–2013, 0 bps, CAGR %/yr

|  | exit @ next open | exit @ signal close |
|---|---|---|
| **entry @ next open** | **25.46%** ← as-run (Rung B) | 20.72% |
| **entry @ close (MOC)** | **32.37%** ← X4 upper bound | **28.24%** ← c2c (Rung A) |

Both diagonal cells reproduce C1's own printed rungs exactly (25.46 / 28.24),
asserted in-run, not eyeballed.

## 3. The split, and the sizing artifact that had to be removed first

C1 sizes each rebalance off `navv` marked at **close(d)** while a c2c fill
happens at **close(d−1)** (`run_c1_residual_reversal.py:143` vs `:138`). That is
one day of forward information in the *position size*: on an up day it deploys a
larger `navv` at the cheaper prior close. Re-marking the pre-trade NAV at the
price the exits actually realize measures it:

| cell | as written | mark at fill | artifact |
|---|---|---|---|
| as-run (entry open) | 25.46% | 23.68% | +1.78 pp |
| entry @ close (MOC) | 32.37% | 30.29% | +2.08 pp |
| exit @ close only | 20.72% | 18.74% | +1.97 pp |
| c2c both legs | 28.24% | 25.05% | +3.19 pp |

**The corrected split (vs the as-run 23.68%):**

| | pp/yr |
|---|---|
| total c2c gap | **+1.38** |
| attributable to **ENTRY** timing | **+6.61** |
| attributable to **EXIT** timing | **−4.93** |

**The entry leak is 4.8× the close-to-close gap used to measure it.** Removing
the sizing artifact makes the ratio worse, not better: it shrinks the c2c gap
(2.78 → 1.38) while barely touching the entry attribution (6.91 → 6.61).

## 4. Three things that cut against reading this as "X4's prize is big"

**(a) The sign reverses out of sample.** Secondary window 2014–, 0 bps: as-run
8.88% → entry-fixed **7.95%**. At the real 5 bps/side: as-run 3.42%/DD 38.7%/Sh
0.26 → MOC **2.54%/DD 52.0%/Sh 0.23** — worse return *and* a drawdown 13 pp
deeper. The entry fix helps only in 2000–2013, which is exactly the window C1's
own prereg declared **UNINTERPRETABLE** (the reversal leg buys worst-residual
names among 39 known survivors, in the 2000–02 and 2008 crashes).

**(b) The per-fill legs do not support the mechanism.** Mean overnight leg,
full history: entry fills **+7.20 bps** (n=7,496, SE 1.73), exit fills **+6.93
bps** (n=7,492, SE 1.74), difference **+0.27 bps** — statistically
indistinguishable. So the +6.61 / −4.93 asymmetry is **not** "the names C1 buys
gap up more than the names it sells." It is a compounding/position-sizing path
effect, and this run does not establish its mechanism. Anyone quoting the
+6.61 pp should quote this paragraph with it.

**(c) It is an upper bound, not an estimate.** The entry cell assumes a fill at
exactly the official close: no closing-auction slippage, no decay between a
frozen 15:50 signal and the 16:00 print, and CLS availability assumed. None of
those three is resolved.

## 5. Scope-locked, named not fixed

The sizing artifact in §3 is **not** specific to this diagnostic. It lives in
C1's own `run()`, which means **C1's recorded gate result (19.08% CAGR at 5 bps)
carries roughly +1.78 pp of it**, and E16's weekly engine — which C1 reuses — has
the same shape. Every Rung A in `run_ex_decomp.py` uses the equivalent
"open := prior close" wrapper and therefore inherits it too. Not touched here.
This is a finding about recorded results, and it needs its own dated decision.

## 6. What was asked and not done

The task was "for each live sleeve and each closed FAIL". This covers **C1
only** — the live stress branch of `m10_1_nagel`, and the one with a recorded
c2c→next-open gap. Each other runner needs its own port of the two-flag split
(the runners do not share a fill harness), so the remaining live sleeves
(`e6_1x` = `run_e6_deleveraged.py`, `e18_vixts` = `run_e18_regime_gates.py`) and
the closed FAILs are **not measured**. M10-1 in particular — whose 22.82/17.87
pair started §0 — is unmeasured, and it is the sleeve actually running in paper.
