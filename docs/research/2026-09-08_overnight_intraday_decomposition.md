# Overnight vs intraday decomposition — the buy-close/sell-open premium on our own data

**Swing Trading · 2026-09-08 (CDT) · Evan Daruwalla**

**Type:** DIAGNOSTIC — no D1 verdict, no PASS/FAIL, nothing deployed, **attempt
tally UNCHANGED** (precedent: EX-DECOMP, record DU/M12, X9's zero-cost split).
**Runner:** `scripts/ablation_overnight_decomp.py`. **No prereg**, consistent with
every diagnostic above.
**Regression:** `FROZEN TESTS: GREEN (all d=0)` — 12 pinned refs at d=±0.0000pp,
19 invariants. All six proofs pass. Both runs byte-identical (F3 protocol).

---

## Read this before the tables

**The era question is underpowered by roughly 40×, and no amount of care fixes
it.** The overnight leg's annualized volatility is ~10.6%. Over the post-2022
window (n=1,159) the 95% CI on SPY's overnight drift is **±9.57 pp/yr** against an
effect of interest around 1–2 pp/yr. Resolving that at 2σ needs ~200 years of
data. Every era row below carries its CI for exactly this reason: a table that
printed a pre number and a post number without one would manufacture a
conclusion its data cannot support.

**Disclosure — a result leaked before the runner existed.** While validating the
reconciliation identity during planning, a sub-agent computed full-history leg
products and reported them: SPY `prod(F_TR)=32.043`, `prod(F_ON)=24.91`,
`prod(F_ID)=1.286`. The finished run reproduces these (SPY cumulative log-NAV
overnight 3.215 → e³·²¹⁵ = 24.90). No era split, per-year row or pre/post
comparison was computed at that stage — but the headline was out before the
script was written, and this is recorded rather than presented as a virgin run.

---

## 1. The anomaly is real here, and it is not subtle

Annualized pp/yr, log space, total-return arm (dividends credited to the
overnight leg — see §4):

| ticker | window | sessions | **overnight** | **intraday** | total |
|---|---|---|---|---|---|
| SPY | 1993-02-01 … 2026-08-17 | 8,443 | **+9.60** | +0.75 | 10.35 |
| QQQ | 1999-03-11 … 2026-08-17 | 6,901 | **+13.12** | −2.78 | 10.34 |
| DIA | 1998-01-21 … 2026-08-17 | 7,187 | **+7.12** | +1.67 | 8.79 |
| IWM | 2000-05-30 … 2026-08-17 | 6,593 | **+12.63** | −4.09 | 8.54 |

In cumulative terms SPY's overnight leg compounded **24.9×** over 33.5 years
while its intraday leg compounded **1.29×**. For QQQ and IWM the intraday leg is
outright *negative* across a quarter-century in which both indices roughly
tripled. This is the Lou-Polk-Skouras (2019, JFE) result reproduced on this
project's own cache, and it is the first unconditional decomposition this repo
has ever run — `ablation_fill_timing.py` measured only IBS<0.20 signal days,
averaged rather than compounded, gross-only, on `swing.db` (2014+).

External validation that the construction is right: SPY's total-return CAGR from
`prod(F_TR)=32.043` over 33.55y is **10.9%/yr**, which matches SPY's published
total return.

## 2. "Flat since 2021" does NOT reproduce

`docs/research/2026-07-13_execution_microstructure.md:53-55` records: *"The NY Fed
("The Disappearing Overnight Drift," 2026) dates the drift **flat since 2021**.
The overnight component is both uncapturable *and* now decayed."* That sentence
carries no sample, no universe and no magnitude, and had never been checked here.

Against our data, at the claim's own literal cut-point:

| ticker | ≥ 2021-01-01 overnight | 95% CI | vs pre-2021 | **percentile of all matched-length windows** |
|---|---|---|---|---|
| SPY | **+8.07** | ±8.28 | 9.90 | **56.0th** |
| QQQ | **+10.27** | ±11.03 | 13.85 | **50.7th** |
| DIA | **+5.36** | ±7.28 | 7.55 | 45.5th |
| IWM | **+12.97** | ±11.17 | 12.54 | **57.3rd** |

The percentile column is the fair form of the question — comparing a 4.6-year
window to a 29-year window is not a test, because the long window's standard
error is ~5× tighter, so any gap looks large against it while sitting well inside
the short window's own error bar. Instead: where does the current window's drift
sit among *all* overlapping windows of the *same length* in that ticker's own
history?

**All four sit at or near the median of their own history.** Three of four are
still above +8 pp/yr. Not one decline approaches its own confidence interval.
Whatever the NY Fed measured, **the claim as this project recorded it does not
reproduce on our data.**

At the repo's 2022 cut the picture is weaker but the conclusion is unchanged —
SPY +6.31 (37.1st pctile), QQQ +9.22 (45.7th), IWM +9.06 (44.9th), DIA +3.38
(27.2nd). Note that boundary is the E1b train/holdout split
(`run_e1b_backtest.py:23`), **coincidence, not a project prior about a structural
break in overnight drift** — recorded so nobody later cites it as one.

The post-2022 softness is concentrated in a single year. SPY's overnight leg by
year: 2021 **+16.18**, 2022 **−14.37**, 2023 +5.75, 2024 **+21.38**, 2025 +8.06,
2026 (156 sessions) +13.31. QQQ 2022 was **−23.51**. One bad year inside a series
with a 10.6% annual standard deviation is not a regime change, and reading it as
one is precisely the error the CI column exists to prevent.

**Honest limit on this finding.** We do not know whether the source measured
price-only or total return, which index, or over what window. If it measured
price-only and we compare total return, a mismatch is a *definitional artifact,
not a failed reproduction*. Our price-only arm is also reported above (SPY
+7.81 full, +6.75 post-2021) and does not change the conclusion, but the
source's own definition remains unverified. **This does not falsify the NY Fed
paper. It falsifies the confidence with which one uncited sentence has been
carried in this project's docs.**

## 3. It is still not tradeable — and that part needs no era split

An overnight-only trade is a **full round trip every session**, so with the
repo's multiplicative convention the net daily factor is `F_ON · (1−c)/(1+c)`
and breakeven per-side cost is `c* = (G−1)/(G+1)` on the daily geometric
overnight factor `G`.

| ticker | gross pp/yr | **breakeven bps/side** | net @1bp | net @2bps | **net @5bps** | net @10bps |
|---|---|---|---|---|---|---|
| SPY | 9.60 | **1.90** | +4.7 | −0.5 | **−14.4** | −33.5 |
| QQQ | 13.12 | **2.60** | +8.4 | +3.1 | **−11.4** | −31.1 |
| DIA | 7.12 | **1.41** | +2.1 | −2.9 | **−16.5** | −35.1 |
| IWM | 12.63 | **2.51** | +7.9 | +2.6 | **−11.8** | −31.5 |

**This project prices 5 bps/side.** Breakeven is 1.41–2.60. The trade is short by
2× to 3.5× and loses **−11.4 to −16.5 pp/yr**, arithmetic forced by ~252 round
trips a year in every era, gross number notwithstanding. Even at a fantasy
1 bp/side, SPY's +4.7 pp/yr is *below its own buy-and-hold* of 10.35.

This is the same wall the NightShares NSPY/NIWM ETFs hit with real money —
**−6.9% / −10%+ against +22% / +16% benchmarks, liquidated in ~14 months**,
post-mortem blaming "transaction costs of turning the portfolio over twice a
day" (`execution_microstructure.md:51-53`). Our arithmetic and their outcome
agree.

**So the recorded prior is half right.** *Uncapturable* — confirmed, decisively,
and by a mechanism (per-session round-trip cost) that no era can rescue.
*Now decayed* — does not reproduce. The kill stands; one of its two stated
reasons does not.

## 4. Method, and the trap that would have inverted the answer

**Legs.** `F_TR = adj[t]/adj[t-1]`; `F_ID = close[t]/open[t]`;
`F_ON = F_TR · (open[t]/close[t])`; price-only `F_ONp = open[t]/close[t-1]`.
`F_ON · F_ID = F_TR` exactly, so `log F_ON + log F_ID = log F_TR` holds per day
and survives summing over any date subset — which is why every aggregate is
computed in logs and converted only at print time.

**The trap.** On dividend-unadjusted `close`, the ex-dividend drop falls entirely
in the `close[t-1] → open[t]` window. A price-only decomposition therefore
understates the overnight leg by the **whole dividend yield — ~183 bps/yr on SPY
pre-2022** — which is the same order of magnitude as the effect under test. A
naive price-only run would have printed a materially weaker overnight leg and
made "the premium died" look supported. It is also *differential* across tickers
(QQQ ~51 bps/yr vs SPY ~183), so a price-only cross-ticker table measures
dividend policy rather than drift. Both arms are reported for this reason.

An earlier construction — `DIV = TR − PR`, added to the overnight leg — was
**wrong**: it breaks by the cross term `DIV·ID`, up to 154 bps summed over full
history. The multiplicative form above is exact to one ULP.

**Self-checks, all four tickers, run every time (20 assertions):**

| check | worst observed | tolerance | what it binds |
|---|---|---|---|
| decomposition `prod(F_ON)·prod(F_ID)/prod(F_TR)` | 6.44e-15 | 1e-10 | coding slips only — **tautological**, holds even if `open` is garbage |
| telescope-TR vs `adj[-1]/adj[0]` | 8.88e-15 | 1e-10 | **binds** every bar's presence and order |
| telescope-price vs `close[-1]/close[0]` | 1.13e-14 | 1e-10 | **binds** `open` and both closes |
| adj-anchor `adj[-1]/close[-1] == 1` | 0.00e+00 | 1e-10 | back-adjustment anchor |
| dividend cross-check vs `*_div.json` | **1.87e-06** | 5e-5 | **667 independent ex-dates** |

The dividend cross-check is the one that validates §4's whole correction against
a source the legs never touch. Yahoo's adjustment is *multiplicative* —
`k = 1/(1 − D/close[t-1])` — not additive.

## 5. Disclosed, not corrected

- **Early synthetic opens**, sitting exactly where the baseline is computed: SPY
  1993 has 33/233 (14.2%) sessions with `open == prior close` exactly, deflating
  the pre-era overnight leg. Robustness row, SPY from 1996: overnight **9.58**
  vs 9.60 full — immaterial.
- **COVID (Feb–Apr 2020) is in the PRE window under both cut-points**, so it
  distorts the baseline, not the post period.
- **Three "overnights" are multi-day closures**: 2001-09-17 (7 days, the 9/11
  closure, and SPY's 3rd-largest |overnight| move at −8.22%), 2007-01-03,
  2012-10-31.
- **The legs are not per-unit-time comparable** — overnight spans ~72% of
  calendar time, intraday ~28%. "Overnight beats intraday" is a *per-session*
  statement.
- **Pooling does not help**: overnight-leg correlations are SPY–DIA 0.962,
  SPY–IWM 0.916, SPY–QQQ 0.893, so an equal-weight basket is no tighter than SPY
  alone. Every table is per-ticker.
- **Arithmetic vs log.** Primary is log. The arithmetic−log wedge is `σ²/2` and
  differs per leg, handing intraday a spurious ~+0.59 pp/yr on SPY. Arithmetic
  bps/day is reported as a labeled secondary (SPY overnight mean 4.033, median
  6.162) and never mixed into the log tables.
- **`*_div.json` is never vintage-checked** — `_last_bar_date` returns `None` for
  dict-shaped files, so the staleness guard skips them. They are vintage
  2026-07-11 against 2026-08-18 bars, hence the cross-check is restricted to
  ex-dates ≤ 2026-06-30. Known consequence: DIA's 2026-07-17 ex-date is in
  `adj_close` and absent from `DIA_div.json`.

## 6. What this changes, and what it does not

**Changes:** the "now decayed" half of the overnight kill is unsupported on our
data and should not be restated without this caveat. That weakens half of X4's
stated prior (`PRD_ROADMAP.md:1026`, "Prior: confirms the kill (NightShares
failure + NY-Fed flat-since-2021 drift)") — the NightShares leg stands, the
NY-Fed leg does not reproduce. X4 remains BLOCKED-ON-EVAN and BLOCKED-ON-BROKER-TIER
regardless; nothing here unblocks it.

**Does not change:** the 54%-of-edge-in-the-gap figure (different conditioning —
IBS<0.20 signal days, not unconditional), E2's c2c "mirage" (record CK closed
that on drawdown grounds), the closed search phase, or any live sleeve. Nothing
is deployed and no verdict is issued.
