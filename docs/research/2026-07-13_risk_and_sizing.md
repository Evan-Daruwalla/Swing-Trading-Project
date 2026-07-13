# Research brief — Risk management & bet-sizing for a K=1–3 EOD swing bot

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Question:** given that return-hunting keeps failing (0 PASS-HR / 20 attempts), is
there a defensible risk-management / position-sizing / exit / regime framework that
(a) makes the concentrated high-return mandate survivable and (b) turns the two weak
survivors — E6 (200-DMA 1× rotation) and E18 (VIX/VIX3M gate) — into a deployable,
honestly-testable sleeve? **Audience:** the operator + any future model executing
the PRD.

---

## TL;DR (verdict first)

**At K=1–3 there is no diversification, so *sizing is the entire risk-management
game* — and the defensible policy is capped fractional-Kelly (¼–½), never full.**
Full Kelly on a noisy, backtest-inflated edge with no diversification is
strictly dominated (past the Kelly peak you get *more* drawdown AND *less* growth),
and because backtest edges are systematically optimistic, a paper "half-Kelly" is
probably already real-world over-Kelly. On exits: **a time stop (vertical barrier)
is the robust backbone; tight price stops mostly hurt** (Kaminski-Lo: on a random
walk a stop only subtracts; it helps only under momentum, hurts mean-reversion),
and under Alpaca DAY-TIF a "stop" can only fire at next open anyway, so gap
protection comes from *sizing, not stops*. On regime overlays: only **conditional
volatility targeting** (condition the two survivors on each other) plausibly beats a
lone VIX/200-DMA gate — but the honest, decisive caveat across the whole regime
family is **effective-N**: there are only ~3–5 independent stress episodes in the
sample, so *no* regime rule can be validated to the frozen-tripwire standard on
history; it can only be pre-registered and forward-papered. Finally, **the deployable
E6∩E18 sleeve is a drawdown-reduction allocation, not the high-return engine** — and
its signal is so slow that a forward-paper test can prove *implementation fidelity*
but **cannot statistically prove it beats SPY**. Say that in writing.

---

## Method
4 parallel research agents (sizing, exits/stops, regime/drawdown control, deployable
framework), primary-source-graded, mapped to K=1–3 / $100–1,000 / EOD-DAY-TIF and the
E6/E18 survivors. Limitation: desk research; the strongest sizing/exit results are
[PR], several magnitude claims are [F] blog figures used only directionally.

---

## Findings

### 1. Position sizing — capped fractional-Kelly is the core lever
- **Half-Kelly keeps ~75% of growth at ~50% of volatility** (`G(λ)=G*·λ(2−λ)`);
  quarter-Kelly ~44% growth at ~25% vol (MacLean-Thorp-Ziemba). **Full Kelly is
  fatal here:** extreme sensitivity to the mean estimate, ~50% chance of a 50%
  drawdown, and growth → 0 at 2× Kelly. The dominant reason to fractionalize is
  *systematic edge overestimation* — the default failure mode of a tuned backtest.
- **Implement as fixed-risk-per-trade** (`shares = r·Equity/(entry−stop)`, r≈1–2%):
  a hard, legible per-name loss cap, essential where one name is 33–100% of the book.
  Under EOD next-open the stop is advisory (gap risk), so r is a floor not a ceiling.
- **Vol-targeting overlay** (Harvey et al. 2018) is well-evidenced *for equities*
  specifically; but **inverse-variance return-timing** (Moreira-Muir 2017) **dies
  out-of-sample** (Cederburg et al. 2020) — use the *targeting* form, not the
  return-timing form.
- **Anti-martingale only; martingale is an unconditional no.** The "losses accepted"
  mandate psychologically licenses the martingale "win it back" impulse — at K=1–3
  that is the fastest route to a non-recoverable drawdown. "Accepting losses" must
  mean accepting *pre-sized, capped* losses.

### 2. Exits & stops — time stop backbone, sizing not stops for gaps
- **Kaminski-Lo (peer-reviewed):** on a random walk a stop-loss *always subtracts*
  expected return (truncation + cost); it adds value **only under momentum**, and
  **hurts mean-reversion**. So a stop's sign depends on your strategy's own serial
  correlation.
- **DAY-TIF collapses the design space:** no resting intraday stop → every "stop" is
  a close-triggered, next-open-executed rule with unhedged gap risk. Tight stops
  harvest whipsaw *and* still fail to protect on the gaps that matter.
- **Backbone = time stop / vertical barrier** (fixed N-day hold matched to the edge's
  horizon): lowest overfitting surface, fully DAY-TIF-native, regime-agnostic, no RWH
  penalty. Should be in every variant. Test **"time stop only" as the honest
  baseline** and require any price-stop variant to beat it out-of-sample.
- **Regime-match the price barrier:** momentum entry → close-based trailing stop, *no*
  fixed profit target (don't cap the tail); mean-reversion entry → profit target at
  the reversion level, minimal/wide stop (the stop is the harmful piece).
- **Pre-register as a triple-barrier** (López de Prado) resolved *on the close*
  (TP / wide vol-stop / time), sized from the drawdown distribution (arXiv 1609.00869)
  not grid-searched. **Gap defense = position sizing, not stop tightness.**

### 3. Regime & drawdown control — one candidate, one decisive caveat
- **The only in-scope idea mechanistically different from E6/E18 is conditional
  volatility targeting** (RK3.4): scale down only when high-vol AND falling-trend —
  i.e., condition the two survivors on each other. FAJ 2020: +0.16 Sharpe, −7.4 pp
  max DD on momentum. It targets VT's "sell-the-bottom" failure directly.
- Everything else is the same stress regime slower (credit spreads, yield curve),
  a transform of E6 (breadth = breadth *of* the 200-DMA signal), **net-harmful**
  (equity-curve/drawdown de-risking "mostly locks in losses" — JPM 2025), an
  **overfit trap** (gate ensembles fit the same 3 crises with more parameters), or
  out-of-instrument/EOD-scope (TSMOM crisis-alpha, put tail-hedging).
- **The decisive caveat:** every equity regime gate keys off the *same* vol/trend
  object, which has produced only ~3–5 independent stress episodes (2008, 2011, 2018,
  2020, 2022). Backtest power to detect even a medium effect runs ~0.42 — below
  usable. **E18 "passing" partly because its window skips 2008 is the generic
  condition, not an anomaly.** No regime rule can be *validated* on history to the
  frozen-tripwire standard; it can only be pre-registered and forward-papered.

### 4. The deployable survivor sleeve (E6 ∩ E18) + the forward-test that's actually honest
- **State machine (asymmetric AND):** base = 1× SPY if close > 200-DMA else cash;
  **E18 backwardation overrides to flat** regardless of the trend gate. EOD →
  next-open, 5 bps/side.
- **Sizing:** 100% of the sleeve to SPY when "on" (Kelly cap is *non-binding* — a 1×
  long-only book can't be over-bet); fractional shares ($1 notional) so $100–1,000
  holds true 1× SPY without lot-rounding drag; drawdown ceiling as a *labeled
  tripwire* (halt + human review), not a return input.
- **Honest expectation (Faber):** "equity-like returns, bond-like drawdowns" —
  roughly SPY's return (usually a bit *less* from whipsaw/missed rebounds) with
  materially lower drawdown, *conditional on a bear occurring in the window.* In a
  continued bull it will lag SPY, possibly the whole forward window.
- **The forward-paper problem is the whole ballgame:** the sleeve changes state only
  ~1–4×/year, so reaching 100 trades or the Minimum Track Record Length (further
  inflated by the 20 prior trials, Bailey-López de Prado) against SPY is
  **arithmetically impossible** on any project timeline. Therefore **re-scope the
  forward test's success criterion from "beats benchmark, significant" to
  "implementation is faithful":** run live-paper *alongside a shadow re-run of the
  frozen backtest on the same live dates*, and grade on **tracking fidelity**, with a
  **fixed 6–12-month window, end date pre-committed, one go/no-go, no mid-test
  tuning, no early stop on good P&L** (the peeking trap). Pre-register in writing:
  "this window validates the system *executes as designed*; it is far below MinTRL
  and does not confirm a return edge."
- Benchmarks: primary **SPY total-return buy-hold**, secondary **60/40**; grade on
  **MaxDD / Calmar / Sortino** *and* Sharpe (Sharpe alone flatters buy-hold and
  understates a drawdown-control sleeve).

---

## What to adopt (pre-registrable)
1. **Sizing policy:** capped fractional-Kelly (λ = ¼–½ of the prereg'd estimate) +
   uncertainty haircut, implemented as fixed-risk-per-trade (r = 1–2%), equal-risk
   weighting across the 1–3 names, hard gross + correlation cap, no leverage,
   anti-martingale only. Freeze λ, r, target-vol, gross cap in the prereg.
2. **Exit policy:** time-stop backbone (N-day vertical barrier) as the baseline;
   regime-matched barrier (trail for momentum / target for MR); triple-barrier
   resolved on the close, sized from the drawdown distribution; gap risk handled by
   sizing.
3. **Regime candidate:** pre-register **conditional volatility targeting** (E6×E18
   interaction) with the trend threshold fixed in advance, graded on **forward paper**
   (history is uninformative here).
4. **Deployable sleeve:** the asymmetric-AND E6∩E18 SPY sleeve, run under the
   **fidelity-reframed, fixed-window, no-peeking forward-paper protocol**, then the
   pro-shop staged ramp (tiny real capital → scale iff live matches shadow →
   decommission on divergence) — **Evan-gated on the Alpaca account + go.**

## The honest bottom line
This family cannot manufacture the high-return engine the project set out to find.
Its deliverable is a **defensive, drawdown-controlled allocation** (≈ SPY return,
lower drawdown) plus a **discipline** (capped-Kelly sizing, time-stop exits) that
keeps the concentrated mandate survivable. Selling the E6∩E18 sleeve as anything more
than that — or claiming a slow-signal forward test "proved" it — would break the
project's own rigor rules.

## What would change the conclusion
- The conditional-vol-targeting overlay demonstrably beating a lone VIX/200-DMA gate
  on forward paper.
- Instrument scope expanding to multi-asset futures + shorting → TSMOM crisis-alpha
  (the strongest anti-drawdown mechanism in the literature) becomes investable.
- A genuinely longer forward-test horizon (years) that could approach MinTRL.

## Sources (dated)
- MacLean, Thorp, Ziemba — *Good and Bad Properties of the Kelly Criterion* (2010) — [Berkeley PDF](https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf)
- Harvey et al. — *The Impact of Volatility Targeting* (2018, JPM) — [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)
- Moreira & Muir — *Volatility-Managed Portfolios* (2017, JF); Cederburg, O'Doherty, Wang, Yan — *On the performance of volatility-managed portfolios* (2020, JFE) — [PDF](https://www.lehigh.edu/~xuy219/research/COWY.pdf)
- Kaminski & Lo — *When Do Stop-Loss Rules Stop Losses?* — [PDF](https://www.smallake.kr/wp-content/uploads/2017/02/When_Do_Stop-Loss_Rules_Stop_Losses.pdf); serial-correlation follow-up (J. Financial Markets 2018)
- López de Prado — *Advances in Financial Machine Learning* (2018), triple-barrier
- *Systematic stop-loss threshold from the drawdown distribution* — [arXiv:1609.00869](https://arxiv.org/abs/1609.00869)
- *Conditional Volatility Targeting* (2020, FAJ) — [T&F](https://www.tandfonline.com/doi/full/10.1080/0015198X.2020.1790853)
- Faber — *A Quantitative Approach to Tactical Asset Allocation* (2007/2013) — [PDF](https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf)
- Bailey & López de Prado — *Deflated Sharpe / Minimum Track Record Length* (2014) — [SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)
- *The Stop-Loss That Stops Gains* (summarizing JPM Nov-2025 drawdown-rule study) — [Medium](https://medium.com/@samirvarma/the-stop-loss-that-stops-gains)
