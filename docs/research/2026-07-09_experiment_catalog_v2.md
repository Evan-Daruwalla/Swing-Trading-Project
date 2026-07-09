# Experiment catalog v2 — grounded in measured E1/E1b/E2 data (2026-07-09)

Supersedes the pre-council idea list (2026-07-08) as the planning surface.
Every prior here is either MEASURED (our backtests), LITERATURE (cited,
unverified), or TBD (no honest number exists — the experiment produces it).
No invented figures.

## The three measured design constraints (what the data taught us)

1. **The overnight gap holds >half the edge.** M1.8: 54% of the pooled IBS
   close-to-close effect is close→next-open. E2's c2c holdout (+1.40%/mo)
   would have passed every gate; its executable next-open twin (+0.64%/mo)
   failed. Any new experiment must state WHERE its signal-to-fill gap sits.
2. **Cost fragility at thin per-trade edges.** E1 died at 10bps round-trip.
   Edges under ~15bps/trade gross don't survive realistic costs.
3. **OOS decay is real.** Train→holdout roughly halved returns in both E1b
   (0.41→0.32%/mo) and E2 (1.50→0.64%/mo). Discount any in-sample number by
   ~half when setting expectations.

Verdicts to date (net, primary configs): E1 +0.19%/mo FAIL · E1b holdout
+0.32%/mo FAIL(near-miss) · E2 holdout +0.64%/mo FAIL · E2 c2c reference
+1.40%/mo (non-executable, passes).

**STOP STATUS:** the IBS family is SHELVED (prereg `865c09e` §7). Family A
below consists of IBS execution variants — running ANY of them requires
Evan's explicit dated override of that stop ("go on A1" = the override,
recorded as such). Families B–D are new families or infrastructure, clear
of the stop.

---

## Family A — capture the measured overnight component (IBS variants; ⚠ STOP-OVERRIDE REQUIRED)

**A1. MOC-execution IBS (E2 config).** Alpaca supports market-on-close
orders → fills at the official close = the measured c2c series. Backtest
already exists (= E2's c2c rows). The experiment is live-paper: signal
computed ~3:50pm from near-final bar, MOC order submitted before the 3:50
cutoff; measures signal-drift error only.
Prior: MEASURED bounds **+0.64 to +1.40%/mo** (holdout; capture ratio is
what the experiment determines). Cost: C2 infra spike + paper account.

**A2. Near-close (≈3:55pm) market-order IBS.** Same target as A1 via
real-time IEX quotes + market orders; more slippage than MOC, simpler
mechanics. Prior: same measured bounds, expected below A1. Cost: C2 + D1.

**A3. Overnight-only IBS harvest.** Enter MOC on signal day, exit market-on-
open next day — holds ONLY the overnight component (measured 6.3bps/signal
pooled 1x; leveraged version never computed). Fully executable with order
types; backtest is ONE SITTING on existing data (close→open in swing.db).
Prior: TBD by that backtest. The purest test of the mechanism.

**A4. True near-close signal backtest via minute bars.** After D1: compute
IBS at 3:55 from minute data (2016+), fill at actual close; measures the
3:55-vs-close signal error that A1/A2 depend on. Prior: bounded by c2c
+1.40%/mo. Cost: D1 first.

## Family B — new signal families (stop-clear)

**B1. Gap-down reversion executed AT the open.** Signal = overnight gap
≤ −X% vs prior close, in an uptrend; computable AT the open and fillable AT
the open (market-on-open) — the signal-to-fill gap is ~zero BY CONSTRUCTION.
Directly dodges constraint #1. Universe: broad + leveraged. Backtest: one
sitting (opens/closes cached). Prior: TBD.

**B2. Gap-up open-drive continuation.** Mirror of B1: buy the open after a
large gap-up in an uptrend, exit at close or next open (momentum, not MR).
One-sitting backtest. Prior: TBD.

**B3. Momentum-burst continuation on leveraged ETFs.** Close > 20-day high →
enter next open; exit close < 10-day low or 10-day time stop. Momentum
signals shouldn't lose their edge overnight the way MR does — testable
claim. One-sitting backtest. Prior: TBD.

**B4. Vol-regime leveraged rotation ("leverage timing").** Hold TQQQ/UPRO
when the underlying is above its 200-day MA, cash (or 1x) otherwise; holds
of weeks. Infrequent signal changes → overnight forfeit negligible (dodges
constraint #1 by trade frequency). Prior: LITERATURE — Gayed, "Leverage for
the Long Run" (2016 Dow Award) claims long-run results ≈ **1.2–1.5%/mo**
class; single-source, unverified, and our OOS-decay rule says discount.
One-sitting backtest on existing data.

**B5. B4 + realized-vol filter.** Add a 20-day realized-vol gate to B4
(rotate out in high vol regardless of trend). One-sitting backtest after B4.
Prior: TBD.

**B6. 52-week-high breakout swing.** Close breaks prior 252-day high →
enter next open, trail or time-stop. Broad + leveraged. Prior: TBD
(long-horizon 52wk-high literature exists; swing-horizon transfer unknown).

**B7. E3 — concentrated mega-cap stock momentum burst (PRD M2c).**
Liquidity-defined top-~100 US stock universe (dollar-volume floor, NOT
today's-winners picking), K=1–3, weekly-burst entry, survivorship caveat
mandatory in every result. Needs stock backfill (D-lite). Prior:
LITERATURE — cross-sectional momentum ≈ 1%/mo long-short at 6–12mo
horizons; weak transfer to days–weeks long-only. Treat as TBD.

**B8. Mega-cap stock gap-down reversion at the open.** B1 on single stocks
(higher vol → bigger gaps). Mechanically distinct from IBS (no IBS input;
open-time execution) → stop-clear, but flagged stop-ADJACENT for honesty
(it is still oversold-buying). Earnings-gap contamination is the known
hazard; without an earnings calendar (D2), accept or crudely filter.
Prior: TBD.

**B9. PEAD swing.** BLOCKED-ON-DATA (needs D2 earnings calendar). Prior:
LITERATURE — decayed in large caps; drift strongest first 5–20 days.

**B10. Long-only relative-value tilt (QQQ vs SPY stretch).** When the
20-day QQQ/SPY ratio z-score is extreme, overweight the laggard. Different
mechanism (cross-sectional, not time-series oversold). One-sitting
backtest. Prior: TBD.

## Family C — engineering (no market hypothesis; mostly prerequisites)

**C1. NAV-proportional sizing engine v2.** Fix the measured fixed-dollar
sizing property (K=1 NAV went negative in E2 context). Prereq for ANY
future experiment; re-pin frozen refs as v2 alongside v1. One sitting.
**C2. Near-close infrastructure spike.** Read Alpaca real-time IEX quote,
schedule a 3:50–3:55pm loop, submit nothing — feasibility for A1/A2.
**C3. LLM overlay.** Already pre-registered; attaches to the first strategy
that passes and goes live. Unchanged.
**C4. Fill-divergence logger (#28).** Arms the day anything goes live.

## Family D — data unlocks

**D1. Alpaca IEX historical minute bars (2016+)** for the 9 core tickers →
enables A4 and any intraday-timing research. Moderate pipeline work.
**D2. Earnings calendar source** → unlocks B9 and earnings filters for B8.

---

## Recommended sequence (given the goal: high %/mo, executable, honest)

| # | Step | Why first | Cost |
|---|---|---|---|
| 1 | C1 engine v2 | prereq; invalid sizing poisons everything after | 1 sitting |
| 2 | A3 backtest (needs stop override) + B1 + B4 backtests | the three cheapest high-information tests; all one-sitting on existing data; B1/B4 are stop-clear | 1–2 sittings |
| 3 | Pre-register + run the best survivor per prereg discipline | only one new prereg at a time | 1 sitting |
| 4 | C2/D1 if A-family wins; B7 (E3) if B-family wins | infra follows evidence | days |

Every runnable experiment still gets its own dated pre-registration with
return-centric gates (%/mo primary, ruin guard present) BEFORE its runner
exists. Exploratory backtests in step 2 are hypothesis-GENERATING screens —
their outputs set priors and must be labeled as in-sample screens, with the
chosen candidate then confirmed on a protocol its prereg fixes.
