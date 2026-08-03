# X8 — non-equity trend sleeve (decorrelation candidate): **FAIL, both arms**

**Swing Trading · 2026-08-02 (CDT) · attempt #36**
Prereg: `docs/prereg_x8_noneq_trend.md`, committed doc-only as **`8b408f9`**,
before `scripts/run_x8_noneq_trend.py` existed.

## TL;DR

**Both arms FAIL. Deploy nothing** (prereg §7). But the *way* they failed is the
useful part: **decorrelation was never the hard problem.** Both arms cleared the
correlation bar by a mile — GLD **+0.089**, TLT **−0.191** against the e6 rule,
versus a ≤0.30 ceiling. What neither could do is earn its keep: the trend gate
failed to beat simply *holding the same asset*. Finding an uncorrelated asset is
easy; finding one where this program's single surviving rule adds value is not.

## Results

Rule (E6 verbatim): long iff close > SMA200 at the close, execute next open,
1 bp/side, K=1, $1,000. Split-adjusted, dividend-UNADJUSTED.

### Arm (a) GLD — 5,458 bars, 2004-11-18 → 2026-07-31

| | CAGR | maxDD | Sharpe |
|---|---|---|---|
| trend GATE (→2013-12) | **+11.81%** | 24.5% | **0.73** |
| trend SEC (2014-01→) | +6.26% | 28.4% | **0.52** |
| buy-hold GATE | +12.30% | 37.8% | 0.65 |
| buy-hold SEC | +9.57% | 26.4% | 0.65 |

- correlation to e6 rule: **+0.0886** over 5,243 common sessions
- ① corr ≤0.30 **PASS** · ② CAGR>0 both **PASS** · ③ DD ≤60% both **PASS** ·
  ④ Sharpe > buy-hold both **FAIL**

**A genuine near-miss — 3 of 4, and ④ split the windows.** Trend beat buy-hold
in GATE (0.73 vs 0.65) and lost in SEC (0.52 vs 0.65). That is the *sixth*
appearance of this program's signature death: works in the stressed window,
loses in the calm one (E6-downgrade, C7, X6, X7, M10-2, now X8a).

Note what the gate *did* do: it cut GFC-era drawdown by a third (37.8% → 24.5%).
That is E6's lesson again, now confirmed in a third asset class — **trend gating
is drawdown control, not return enhancement.**

### Arm (b) TLT — 6,040 bars, 2002-07-30 → 2026-07-31

| | CAGR | maxDD | Sharpe |
|---|---|---|---|
| trend GATE | **−0.45%** | 23.7% | 0.02 |
| trend SEC | **−0.74%** | 38.6% | −0.03 |
| buy-hold GATE | +0.89% | 28.5% | 0.13 |
| buy-hold SEC | −1.71% | 52.1% | −0.05 |

- correlation to e6 rule: **−0.1905** over 5,825 common sessions
- ① **PASS** · ② CAGR>0 both **FAIL** (negative in both) · ③ **PASS** ·
  ④ **FAIL**

**Declared bias, restated as promised (prereg §4/§9): dividend-UNADJUSTED prices
materially understate TLT**, a coupon-bearing asset. TLT's real total return over
this period was meaningfully better than −0.45%/−0.74%. This arm is *not* a clean
read on bonds — the convention that is correct for the rest of the project is
wrong for this instrument. Recorded as a limitation, not quietly dropped. Even
so, arm (b) fails ④ independently of the dividend issue: the gate does not beat
holding, and that comparison is internally consistent (both sides
dividend-unadjusted).

## What this means

1. **The decorrelation goal is achievable; the *strategy* is the constraint.**
   Correlations of +0.09 and −0.19 are exactly what M3 wants. The blocker is
   that neither passes the "gate must earn its keep" bar — and lowering that bar
   after seeing these numbers is precisely what the prereg forbids.
2. **The three live sleeves remain ~one strategy** (record DN: m10 duplicates e6
   on 69.7% of 4,226 sessions; all three effectively long 65.3%). Nothing here
   changes that, and nothing was deployed.
3. **The honest uncomfortable observation:** plain **buy-and-hold GLD** would
   decorrelate better than the trend-gated version — same low correlation, higher
   Sharpe in both windows (0.65/0.65 vs 0.73/0.52). But buy-and-hold is an
   *allocation*, not a swing strategy, and sits outside this program's scope
   (EOD swing strategies, holds of days to weeks). Saying so is not a
   recommendation to buy gold; it is the accurate reading of the numbers.
4. **Sixth repetition of the one-window death.** The pattern is now robust across
   US equity, non-US equity, crypto, credit, and gold: this rule family controls
   drawdown in stressed regimes and gives the Sharpe back in calm ones.

## What would change this conclusion

- A non-equity arm where the gate beats buy-hold in **both** windows — untested
  candidates include commodities ex-gold, FX carry, or a *different rule* (not
  the 200-DMA family, which now has six one-window deaths against it).
- A total-return (dividend-adjusted) data path would give TLT a fair test. That
  is a real gap in the project's data layer, not just this experiment's.
- Correlation is measured on history; cross-asset correlations spike in crises
  (prereg §9). Even a passing arm would carry that caveat.

## Provenance

- Prereg `8b408f9` (doc-only) → runner `scripts/run_x8_noneq_trend.py`.
- Reuses `run_e8_squeeze.cache_fetch` (shared data layer) and
  `run_e18_regime_gates.{sma, stats}` (pure helpers). The backtest loop is
  written explicitly rather than reusing `overlay_nav`, which carries a 5 bp
  module cost — this prereg declared 1 bp.
- No `swing.db` writes. The three live sleeves were **not modified**.
