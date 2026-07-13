# Research brief — Crypto / 24-7 markets: scope-expansion feasibility

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Question:** does moving to 24/7 crypto structurally dissolve the overnight-gap
problem that killed the equity mean-reversion family; what swing edges survive in a
liquid crypto universe; what NEW failure modes replace the old ones; and is a
paper-first crypto pilot worth pre-registering at $100–1,000? **Audience:** the
operator + Evan (this is an explicit scope-expansion decision).

---

## TL;DR (verdict first)

**24/7 removes the overnight *gap* but does not recover the 54% and does not remove
the *killer* — the killer only wore the gap as a costume.** Three chained facts: (1)
the equity gap-reversal alpha isn't locked treasure behind closed doors — *closure is
what manufactures it* (market-closure → inventory imbalance → snap-back), so a
continuous market never generates it in the first place; (2) the *residual* continuous
crypto reversal fails the same way the equity family did — it's bid-ask-bounce noise
that goes insignificant net of costs and lives in illiquid alts; (3) the un-catchable
adverse jump reappears as an **intraday, fat-tailed, alt-concentrated liquidation
cascade** (Oct-10-2025: −40% Solana intraday, $19B liquidated). The one genuinely-
clean win: for a *liquid* BTC/ETH bar-based bot, "signal at UTC bar-close, execute
next bar" has **zero gap by construction**, and the entire prereg → paper-track →
frozen-tripwire discipline transfers cleanly (Alpaca offers crypto paper trading).
**Recommendation: YES to a narrowly-scoped, paper-first, liquid-only crypto pilot on
the trend/momentum edge — worth pre-registering — but the governing economic fact is
that live retail crypto fees run 25 bps/side at Alpaca (5× the project's 5 bps), so
the pilot must be pre-registered against *crypto* fees, and the single non-negotiable
risk is custody (100% of capital sits uninsured on an exchange that can vanish).**

---

## Method
4 parallel agents (does-24/7-kill-the-gap, crypto swing edges, new failure modes,
retail feasibility/infra), primary-source-graded, mapped to the EOD/K=1–3/$100–1,000/
liquidity-floor constraints and the equity 54%-gap prior. Limitation: desk research;
one key claim (reversal vanishes without closure) is theory-inference across asset
classes, not a direct crypto measurement — flagged as the highest-value gap to close.

---

## Findings

### 1. Does 24/7 dissolve the gap? — RELOCATES-FRICTION, not dissolves-the-killer
- **The clean win (CR1.1):** spot/perp crypto has no close→open gap by construction;
  a UTC daily bar is an arbitrary cut, not a liquidity discontinuity. The specific
  "alpha realizes while I'm locked out" problem genuinely does not exist.
- **But closure *is* the edge (CR1.2):** the leading explanation for short-term
  reversal is that market closure itself generates it (Della Corte-Kosowski / Hong
  2000). Remove closure and you *delete* the gap-reversal alpha — you don't unlock it.
- **The residual reversal dies to costs (CR1.3):** crypto's 1-day reversal is
  bid-ask-bounce-driven, insignificant net of costs, concentrated in illiquid alts —
  the same cost-eats-the-edge killer, worse. In liquid BTC/ETH the same studies find
  *momentum*, not reversal.
- **The jump relocates (CR1.4/CR1.5):** liquidation cascades are the true analog —
  un-catchable, fat-tailed, *any-bar*, alt-concentrated; plus an 8-hour funding clock
  re-imposes a periodic tax on the "continuous" market.

### 2. Which crypto swing edges survive in a liquid universe?
- **Time-series (trend) momentum on the majors — the one clean WORTH-A-PREREG
  candidate.** Liu-Tsyvinski (2021, RFS): 1–4 week predictability; Grayscale
  (survivorship-free, BTC-only, 20/100 MA): Sharpe 1.7 vs 1.3 HODL. Liquid-native,
  days-to-weeks, long-or-flat — matches an EOD spot bot exactly. Honest failure mode:
  whipsaw in range-bound regimes; TS momentum went **negative in the choppy 2022–23**
  tape (pre-register that as an expected drawdown, not a tuning target).
- **Funding-rate carry — real but out-of-scope as a trade; keep the signal.** BIS WP
  1087: >10%/yr average carry, but needs a short-perp derivatives leg, is a continuous
  delta-neutral yield harvest (not a swing), uneconomic net-of-fees at $100–1,000, and
  its tail (counterparty + cascade) is uncapped. Its durable use here is as a
  **sentiment/regime overlay** (extreme positive funding predicts crashes).
- **ILLIQUID-ONLY / vendor-hype:** cross-sectional alt momentum and short-term
  reversal (alpha decays into the liquid universe — the same small-cap liquidity
  wall); on-chain / stablecoin-flow / social sentiment (weak evidence, or
  predictability that lives at 1–6h horizons an EOD bot can't reach).

### 3. New failure modes (the risk ledger)
Being **unlevered + EOD + CEX-only defuses the worst crypto risks** — liquidation
cascades and much of the flash-crash tail are leveraged-trader problems, and
MEV/oracle risk is DeFi-only (N/A). What genuinely threatens this design:
- **Custody / exchange / counterparty (CR3.4) — the one true DEALBREAKER-class risk
  with no equity analog.** 100% of capital sits uninsured on a venue that can be
  hacked ($1.5B Bybit 2025), freeze (Celsius), or be insolvent (FTX, Mt Gox). Not
  diversifiable at this size. Manageable only by large, audited, proof-of-reserve,
  US-regulated venues + withdrawing profits — but the residual tail never reaches
  zero. **This should be the deciding factor.**
- **Manipulation + survivorship, as paired backtest-integrity threats (CR3.2/3.3/
  3.5):** ~70% of reported volume is wash-traded (NBER), ~24% of tokens are
  pump-and-dumps, **>58% of all listed tokens are dead**. A backtest that filters
  liquidity on *reported* volume and runs on the surviving universe shows fictional
  returns (survivorship inflates crypto backtests ~17–22%/yr per Coinbase, up to
  50–200% strategy-dependent). Manageable with rules (survivorship-free point-in-time
  data, depth-not-reported-volume floor, majors-only) — but an automatic rigor FAIL
  if skipped, and the most likely way to fool yourself into a bad decision.
- **Tail vol + stablecoin de-peg (CR3.1/3.7):** worse than equities but manageable —
  no leverage, size for −50% single-name overnight gaps, no naive resting stops, park
  idle capital in fiat or top-tier reserved stablecoins only (even USDC gapped to
  ~$0.87 in Mar-2023).

### 4. Retail feasibility & infra — the fee reality is the governing fact
- **Fees blow up the 5 bps cost model.** Retail taker round-trips: **Alpaca 50 bps
  (25 bps/side), Kraken 80 bps, Coinbase up to 240 bps** — i.e. **5×–24× the
  project's 10 bps round-trip.** An EOD next-open bot is a *taker*, so 25 bps/side is
  the realistic Alpaca number. The lone exception is **Binance.US at ~4 bps RT**
  (0%/0.02%) — cheaper than the equity model, but outside the Alpaca stack, with
  counterparty/regulatory baggage and promotional-fee risk.
- **Ethos transfers cleanly.** A UTC-00:00 daily bar → signal at close → next-bar open
  is mechanically identical to the equity EOD loop and *structurally cleaner* (no
  gaps/halts/corporate-action discontinuities). **Alpaca offers first-class crypto
  paper trading**, so the validation phase runs at zero fee leakage and zero capital
  risk while honoring pre-registration. Data is free/clean (Kraken OHLCV archive),
  fractional/$1-notional orders make small capital work.
- **Tax:** every trade is a taxable event, all short-term/ordinary-income; wash-sale
  rule doesn't apply to crypto (2025) — manageable, a bookkeeping chore only once
  live.

---

## Recommendation — YES to a scoped, paper-first pilot

Pre-register a crypto pilot as:
1. **Paper-first, on Alpaca** — reuse the existing deploy stack + crypto paper sandbox;
   no live capital until a paper record exists. Neutralizes the fee problem for
   validation and preserves the ethos.
2. **Edge = time-series trend/momentum on BTC/ETH-tier liquidity** (the one liquid-
   native, swing-horizon, documented edge) — *not* a resurrection of the gap-reversal
   trade under a 24/7 flag.
3. **Liquid-only, survivorship-free universe** — BTC/ETH + a short top-N by *real
   depth* (not reported volume); enforce the liquidity floor; point-in-time,
   delisting-inclusive data.
4. **Pre-register with CRYPTO fees (25 bps/side Alpaca taker), not equity fees** — the
   frozen tripwire and return gate must clear that 5× bar; an edge that only clears at
   5 bps is a FAIL. Pre-register the 2022–23 trend drawdown as an expected failure
   mode.
5. **Live-money crypto is a separate, explicitly Evan-gated decision** *after* the
   paper record clears the fee-adjusted gate — and only then confront the venue
   question (Alpaca's 50 bps RT vs Binance.US's near-zero fees + counterparty risk)
   and the **custody tail** (the deciding risk).

**Do not** go equity-only by default: the discipline transfers, data + paper infra
are free, and the pilot costs only engineering time. **Do not** let the cheap paper
phase disguise the live economics — the honest headline is that **retail crypto's fee
reality (10–60 bps/side vs 5 bps) governs whether a crypto arm can ever pay for itself
with live money**, and that must be pre-registered into the gate *before* results.

## What would change the conclusion
- A direct crypto measurement confirming (or refuting) that reversal vanishes without
  closure (CR1.2 is theory-inference — the highest-value gap to close).
- The BTC/ETH trend edge clearing the gate at **25 bps/side** on a survivorship-free
  liquid universe.
- A custody solution that removes the uninsured-exchange tail (e.g., a regulated,
  insured venue) — the one risk with no equity analog.

## Sources (dated)
- Della Corte & Kosowski — *Market Closure and Short-Term Reversal* (CICF) — [PDF](https://www.cicfconf.org/sites/default/files/paper_357.pdf); Hong (2000) periodic-closure model
- Liu & Tsyvinski — *Risks and Returns of Cryptocurrency* (2021, RFS) — [NBER w24877](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf); Liu, Tsyvinski, Wu — *Common Risk Factors in Cryptocurrency* (2022, JF) — [NBER w25882](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf)
- Grayscale — *The Trend Is Your Friend* (BTC momentum, survivorship-free) — [Grayscale Research](https://research.grayscale.com/reports/the-trend-is-your-friend-managing-bitcoins-volatility-with-momentum-signals)
- BIS WP 1087 — *Crypto Carry* (2023) — [BIS](https://www.bis.org/publ/work1087.htm)
- Cong, Li, Tang, Yang — *Crypto Wash Trading* (2022/2023, NBER w30783) — [NBER](https://www.nber.org/papers/w30783)
- FTI Consulting — *Crypto Crash October 2025* — [FTI](https://www.fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity); CoinGecko Oct-10-2025 explainer
- FBI IC3 — *Bybit $1.5B heist* (2025-02-26) — [IC3](https://www.ic3.gov/psa/2025/psa250226); FTX bankruptcy; Terra/UST (Harvard CorpGov 2023); USDC de-peg (CNBC 2023-03-11)
- CoinDesk — *More than half of all crypto tokens have failed* (2026-01-14) — [CoinDesk](https://www.coindesk.com/markets/2026/01/14/more-than-half-of-all-crypto-tokens-have-failed-and-most-died-in-2025); UniSG survivorship/delisting-bias paper
- Alpaca [crypto fees](https://docs.alpaca.markets/us/docs/crypto-fees) · [crypto paper](https://docs.alpaca.markets/us/docs/paper-trading); Binance.US zero-fee (2026-04-22); Kraken OHLCV archive (accessed 2026-07-13)
