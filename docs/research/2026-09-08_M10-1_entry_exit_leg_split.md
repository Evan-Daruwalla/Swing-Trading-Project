# M10-1's timing gap, split — and fixing the entry would break its PASS

**Swing Trading · 2026-09-08 (CDT) · Evan Daruwalla**

**Type:** DIAGNOSTIC — no D1 verdict, no PASS/FAIL, nothing deployed, **attempt
tally UNCHANGED** (precedent EX-DECOMP record DU/M12, X9's zero-cost split, GD,
GF). **Runner:** `scripts/ablation_m10_1_entry_exit_legs.py`. **No prereg**,
consistent with every diagnostic above. M10-1's runner was **not edited** — it is
the live `m10_1_nagel` paper sleeve's backtest of record.
**Regression:** `FROZEN TESTS: GREEN (all d=0)`. Both runs byte-identical
(F3 protocol), 2,213-byte output. Reconciliation asserted in-run, not eyeballed.

---

## 0. The headline

**Fixing M10-1's entry — the thing X4 exists to do — would convert the program's
only PASS-HR into a FAIL.** At the real cost model, the MOC-entry arm's secondary
window falls to **14.63% CAGR** against the **≥15%** bar, with drawdown blowing
out from 39.7% to **50.6%**.

The as-run sleeve is unaffected and still passes; this is a statement about what
X4 would do to it, measured rather than argued.

## 1. Reconciliation — two cells pinned, two that cannot be

M10-1's own runner prints its rungs. The split reproduces both, asserted:

| cell | this run | runner | |
|---|---|---|---|
| B, next-open 0 bps | **20.77%** | 20.77% | MATCH |
| A, c2c **stocks-only** 0 bps | **22.82%** | 22.82% | MATCH |

**The other two cells of the 2×2 reconcile against nothing** — M10-1 has never
recorded a c2c number that includes the QQQ leg. This is where the
"asserted, not eyeballed" guarantee that made the C1 split self-validating stops,
and it is stated up front rather than discovered later.

## 2. The recorded "~5 pp overnight gap" is mostly COST

Record Appendix CI caveat (5) reads: *"COST/EXEC-FRAGILE: c2c 22.82% ->
next-open 17.87% (~5pp in the overnight gap C1 always leaked)."*

Those two numbers are **Rung A at 0 bps** and **Rung C at 5 bps stocks / 1 bp
QQQ**. The runner also prints **Rung B (next-open, 0 bps) = 20.77%**, which the
caveat skips. So:

| | gate CAGR | |
|---|---|---|
| A — c2c stocks, 0 bps | 22.82% | quoted |
| B — next-open, 0 bps | **20.77%** | **skipped by the caveat** |
| C — next-open, 5 bps | 17.87% | quoted |

**The quoted +4.94 pp is not a timing delta.** It splits as **TIMING +2.04 pp
(A→B)** and **COST +2.90 pp (B→C)**. Most of the "overnight gap" that motivates
X4 on the live sleeve is cost, not the gap.

And the timing half is **stocks-only**: `run_m10_1_nagel_switch.py:157` labels it
`"A (c2c stocks 0bps)"` and means it — `spx()` (`:87`) carries the `c2c` flag,
but the QQQ legs read `qo[d]` directly at `:101` and `:112`. There is no
`qpx()`. Since the Nagel Switch holds QQQ or cash in every non-stress week, the
recorded timing delta never moved the branch that owns most of the calendar.

This is the third instance this session of a recorded number meaning something
narrower than the way it is quoted (record GF §1 and §2a are the other two).

## 3. The split, both branches

Gate 2000–2013, 0 bps, CAGR %/yr:

| | exit @ next open | exit @ signal close |
|---|---|---|
| **entry @ next open** | **20.77%** ← as-run (recorded) | 18.13% |
| **entry @ close (MOC)** | **25.48%** ← X4 upper bound | 22.70% |

Against the as-run 20.77%:

| | pp/yr |
|---|---|
| total c2c gap, both branches | **+1.93** |
| attributable to **ENTRY** timing | **+4.70** |
| attributable to **EXIT** timing | **−2.64** |

**Same shape as C1**: the entry term is ~2.4× the net c2c gap, because moving the
exit to the close costs an overnight leg that masks most of the entry gain. C1's
ratio was 4.8×. The mechanism reproduces on a second, structurally different
strategy.

## 4. Per-fill legs — four populations, and again they do not explain it

| population | n | mean | SE |
|---|---|---|---|
| stress_entry | 2,688 | +11.00 bps | 4.07 |
| stress_exit | 2,688 | +11.62 bps | 4.10 |
| trend_entry | 77 | −2.45 bps | 5.56 |
| trend_exit | 76 | +4.38 bps | 17.14 |

Stress entry and exit legs are **statistically indistinguishable** (+11.00 vs
+11.62, SE ~4.1) — exactly as on C1 (+7.20 vs +6.93). So the +4.70 / −2.64 CAGR
asymmetry is **not** "the names it buys gap up more than the ones it sells." The
mechanism remains a compounding/position-sizing path effect, and two independent
strategies have now failed to explain it through mean legs. **Anyone quoting
+4.70 pp must quote this section with it.**

The trend populations are tiny (77 / 76 fills — the branch only trades on regime
transitions) and their means are not separable from zero. Pooling entry and exit
across branches, as the C1 diagnostic did, would have been swamped by the 2,688
stress fills and would have misattributed the switch's behaviour.

## 5. Why the prize does not survive contact with the cost model

Secondary window 2014–, 0 bps: as-run **17.66%** → entry-fixed **16.39%**. The
sign reverses out of sample, as it did on C1.

At the real 5 bps stocks / 1 bp QQQ:

| arm | gate | secondary |
|---|---|---|
| as-run (entry at next open) | 17.87% / DD 60.0% / Sh 0.66 | 15.88% / DD 39.7% / Sh 0.78 |
| **entry @ close (MOC)** | 22.46% / DD 55.2% / Sh 0.73 | **14.63% / DD 50.6% / Sh 0.67** |

**PASS-HR requires CAGR ≥ 15% AND maxDD ≤ 60% in BOTH windows.** The MOC arm
clears the gate handsomely and then **fails the secondary on return** (14.63% <
15%) while its drawdown deepens by 10.9 pp. The gate improvement is concentrated
in the survivorship-flattered 2000–2013 window; the out-of-sample window gets
worse on both axes.

## 6. The as-run sleeve is unaffected — verified at full precision

Because §5 turns on a 0.37 pp margin, the as-run numbers were re-checked at four
decimals on today's cache vintage:

```
gate CAGR 17.8747%  maxDD 59.9518%  Sharpe 0.6632
sec  CAGR 15.8820%  maxDD 39.6754%  Sharpe 0.7799
PASS-HR: PASS    gate DD margin +0.0482 pp
```

The gate drawdown is **identical to the recorded 59.9518%** and still clears the
60% ceiling by 0.05 pp. **Disclosed drift:** the secondary CAGR is **15.8820%
today vs 15.94% recorded** (2026-07-14) — a −0.06 pp move from the secondary
window extending with the cache (now ending 2026-08-17). Still above the 15%
bar, margin 0.88 pp. Nothing about the recorded verdict changes; the drift is
named because a future run will see it and should not treat it as new.

## 7. What this means for X4

The X4 decision now has a directly measured answer on the sleeve X4 would
actually be mounted on, and it is worse than the C1 evidence suggested:

1. The gap motivating X4 is **58% cost, 42% timing** (2.90 vs 2.04 pp).
2. The timing half was measured **stocks-only** and so understates nothing about
   the QQQ branch — it simply never looked at it.
3. The entry term is real and larger than the net gap (+4.70 vs +1.93 pp), but
4. **implementing it would cost M10-1 its PASS-HR.**

Point 4 is not an argument that X4 is uninteresting. It is an argument that the
one strategy this project could mount X4 on gets *worse* out of sample when the
entry is fixed — which is the same era-confinement C1 showed, now with a verdict
consequence attached.

## 8. What was not done

Only M10-1 and C1 are measured. The remaining live sleeves — `e6_1x`
(`run_e6_deleveraged.py`) and `e18_vixts` (`run_e18_regime_gates.py`) — hold a
single instrument all-in/all-out and have no cross-sectional rebalance, so the
two-flag split is not meaningful for them in the same form. Every closed FAIL
remains unmeasured. No runner was edited; no verdict was moved.
