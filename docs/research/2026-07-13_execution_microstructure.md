# Research brief — Execution & microstructure for a $100–1,000 EOD swing bot

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Question:** how much of the program's 0-PASS-HR / 20-attempt record is *execution*
(fills, costs, the overnight gap) versus *genuine no-signal*, and what execution
policy + cost model should the project standardize on? **Audience:** the operator +
any future model executing the PRD.

---

## TL;DR (verdict first)

**The 0-for-20 is overwhelmingly a genuine no-edge result, not an execution
artifact — and that is the single most important finding.** The project already
fills at next-open and charges 5 bps/side, which *surrenders* the one-directional
positive bias (close-fills, zero cost) that manufactures fake backtest alpha; a
pipeline that is already realistic and still returns 0-for-20 has no hidden
optimism left to strip. This matches the literature base rate: **~93% of published
anomaly gross alpha dies once realistic costs are applied** (Chen-Velikov 2023).
Three actionable consequences: (1) the overnight-gap killer is **confirmed
structural** — a next-open order captures 0% of the close→open move by construction,
and the one real-money test of holding the gap (NightShares ETFs) lost money and
liquidated in 14 months; (2) there is **exactly one honest execution experiment
left** — a market-on-close (MOC) entry variant, the only fill positioned to capture
the gap; (3) a **3-rung decomposition ladder** can settle "execution vs signal" for
every FAIL, and the 5 bps/side assumption is fair-to-conservative for the
liquidity-floored universe (needs tiering, not loosening).

---

## Method
4 parallel research agents (overnight-gap/fills, cost modeling, order types,
backtest realism), primary-source-graded ([PR]/[WP]/[V]/[F]), mapped to the
Alpaca-paper deploy target and the project's next-open + 5 bps + liquidity-floor
model. Limitation: desk research, no backtests run; several Alpaca mechanics
verified from current docs (they correct a stale HANDOFF note — see below).

---

## Findings

### 1. The overnight gap is structurally uncapturable at retail — confirmed, not fixable
- **Arithmetic:** ~54% of the mean-reversion edge lives in close(t)→open(t+1). A
  next-open fill executes *at* open(t+1) — the far end of the gap — so it captures
  **0%** of it by construction (EX1).
- **The open is the worst fill of the day** for exactly the small-cap universe a
  floored $100–1,000 book is pushed toward: Berkman et al. (2012, JFQA) — open-buy
  implicit cost *exceeds the effective half-spread*; Lou-Polk-Skouras (2019, JFE) —
  liquidity deep at close, shallow at open.
- **Market-level confirmation:** the NightShares NSPY/NIWM ETFs (buy close, sell
  open) returned **−6.9% / −10%+ vs +22% / +16% benchmarks** and **liquidated in
  ~14 months** — "transaction costs of turning the portfolio over twice a day." The
  NY Fed ("The Disappearing Overnight Drift," 2026) dates the drift **flat since
  2021**. The overnight component is both uncapturable *and* now decayed.
- **The one honest experiment left — a market-on-close (MOC) entry.** A close entry
  is the *only* fill positioned to hold across the gap, Alpaca supports CLS, and the
  closing auction is the deep-liquidity side of the asymmetry. **Catch:** Alpaca
  rejects CLS after 15:50 ET, so a legitimate MOC variant must re-derive its signal
  on a **frozen 15:50 snapshot** (using the 16:00 close to justify a 15:50 order is
  look-ahead) and measure the 15:50→16:00 stub as a residual. Pre-register expecting
  it to *confirm the kill with costs* rather than rescue the edge.

### 2. "0-for-20: execution or signal?" — decisively signal
- Execution-optimism (close fills, 0 cost, 100%-limit fills) is a **one-directional
  positive bias** — it can only make a backtest look *better*. The project already
  gave that up (next-open + 5 bps), so there's no fake alpha left to blame (EX4.1/4.4).
- Base rate: Chen-Velikov (2023, JFQA) — 204 anomalies decay ~50% out-of-sample and
  **~93% net of costs**; the average anomaly nets ~4 bps/month. 0-for-20 is the
  *expected* output of honest research, not a pipeline defect.
- **The one place execution could still hide a signal is turnover/cost capacity**
  (Novy-Marx-Velikov 2016): high-turnover variants die on costs a lower-turnover
  reformulation survives, best mitigated by an asymmetric buy/hold band. Borderline
  FAILs deserve this diagnostic before burial.

### 3. Cost model — 5 bps/side is fair-to-conservative, tier it
- Liquid ETFs (SPY/QQQ): true half-spread ~0.1 bp → 5 bps is 10–50× conservative.
  S&P-500 single stocks: ~2–4 bps/side effective after retail price improvement
  (Dyhrberg-Shkilko 2024) → 5 bps is fair. Genuine small-caps: 15–50+ bps → 5 bps is
  *optimistic*, which the liquidity floor must exclude.
- **Market impact ≈ 0** at $100–1,000 (sqrt-law: ~0.002 bps on SPY) — do not model it.
- **Alpaca paper fills at the full quoted half-spread (no price improvement, no
  slippage, no size check)** — so aligning the backtest cost model to "quoted
  half-spread" semantics matches the deploy target; 5 bps is a conservative envelope
  over that for the intended universe.

### 4. Order-type policy (Alpaca fractional, DAY-TIF) — with a stale-note correction
- **CORRECTION to the HANDOFF:** Alpaca fractional is no longer "market only" (since
  Mar 2024) — it supports **market/limit/stop/stop-limit, all TIF=DAY**, no
  fractional shorting, no auctions (OPG/CLS = Elite Smart Router only).
- **Entry:** buffered **marketable DAY limit** (cap = ref × (1+buffer)); fills near
  the intended level, *doesn't fill on a gap past the cap* — that non-fill is the
  gap-pickoff defense. Never a passive behind-quote limit (adverse selection).
- **Stops:** evaluate on the EOD close in software, exit next open. DAY-re-arm ≈ GTC
  through a gap (the gap fills at the gapped open either way), so **gap risk is
  handled by position sizing, not order type**. If resting stops are ever used,
  stop-*market* never stop-limit.
- **Cash/settlement:** the account can't meet the $2,000 margin minimum (even
  post-PDT-elimination), so it runs as a **cash account** — settled-cash-only sizing
  + T+1 rotation delay to avoid free-riding. Paper won't enforce this (live-only
  landmine).
- **The single biggest backtest-honesty lever (EX3.6):** model limit-order gap
  non-fills explicitly. Silently filling them (they cluster on large-gap names) both
  over-fills missed trades and under-charges slippage — manufacturing edge from
  nothing. Alpaca paper's *unlimited-size* fills will hide the liquidity-floor
  problem, so cap fill size at the floor in the backtest.

---

## What to adopt (pre-registrable)

1. **Standardized fill model:** signal at close → fill next official **open (MOO)**,
   **5 bps/side** both legs (or tiered: 1 bp ETFs / 5 bps single stocks / exclude
   sub-floor), liquidity floor **ADV ≥ $5M AND price ≥ $5**, participation-cap
   declared non-binding at this AUM, tripwire pinned d=±0.0000pp.
2. **The execution-vs-signal decomposition ladder** (3 passes of the built backtest,
   run on any FAIL): **A** frictionless close-to-close 0 bps (paper edge) → **B**
   next-open 0 bps (A−B = look-ahead/gap premium) → **C** next-open + 5 bps [+15 bps
   stress] (B−C = explicit cost; grade C). A FAIL at Rung A = signal genuinely dead
   (where most of a real 0-for-20 lands); PASS A/B but FAIL C = fixable cost/turnover
   problem; PASS A but the A→B drop is most of the edge = lived entirely in the
   look-ahead gap, uninvestable.
3. **One new honest experiment:** the **MOC close-entry variant** (15:50-snapshot
   signal → MOC entry → next-open exit), pre-registered to test how much of the 54%
   gap survives costs. Prior: confirms the kill.
4. **Turnover-reduction diagnostic** (asymmetric entry/exit band) on borderline FAILs
   before final burial.

## What would change the conclusion
- The MOC variant clearing the gate after costs (prior: it won't).
- An intraday data source (unblocks the pullback-entry family, currently EOD-barred).
- Account upgrade to whole-share + Elite Smart Router → MOC/LOC auction fills become
  the #1 execution improvement available.

## Sources (dated)
- Lou, Polk, Skouras — *A Tug of War* (2019, JFE) — [PDF](https://personal.lse.ac.uk/polk/research/TugOfWar.pdf)
- Berkman, Koch, Tuttle, Zhang — *Paying Attention* (2012, JFQA)
- NY Fed — *The Disappearing Overnight Drift* (2026-07-01) — [Liberty St Economics](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Elm Wealth — *Night Shift* (NightShares post-mortem, 2024) — [elmwealth.com](https://elmwealth.com/night-shift/)
- Chen & Velikov — *Zeroing In on the Expected Returns of Anomalies* (2023, JFQA; Fed WP 2020-039) — [Fed PDF](https://www.federalreserve.gov/econres/feds/files/2020039pap.pdf)
- Novy-Marx & Velikov — *A Taxonomy of Anomalies and Their Trading Costs* (2016, RFS) — [SSRN 2535173](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2535173)
- Dyhrberg & Shkilko — *The Retail Execution Quality Landscape* (AEA 2024) — [AEA](https://www.aeaweb.org/conference/2024/program/paper/5Gtsa7ra)
- Perold — *The Implementation Shortfall: Paper vs. Reality* (1988, JPM)
- Frazzini, Israel, Moskowitz — *Trading Costs* (AQR, 2018) — [SSRN 3229719](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3229719)
- Alpaca docs: [order types](https://alpaca.markets/learn/13-order-types-you-should-know-about) · [fractional trading](https://docs.alpaca.markets/us/docs/fractional-trading) · [paper trading](https://docs.alpaca.markets/us/docs/paper-trading) (accessed 2026-07-13)
