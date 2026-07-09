# Handoff

## Goal

**(Redefined by Evan 2026-07-09, record Appendix R.)** Build a swing trader
that, as accurately as possible, invests in a stock or a few stocks
(concentrated, K=1–3) with a small amount of money ($100–1,000) to earn a
**high percent return over a shorter amount of time** (holds days to a few
weeks). **Losing money is OK and will happen — risk explicitly accepted.**
Gates are return-centric with loosened (never absent) drawdown ceilings; the
pre-registration/OOS rigor machinery stays as the ACCURACY instrument.
SEPARATE project from `D:\ClaudeCode\Trading` (read-only from here). Paper
first; nothing goes live without a pre-registered PASS + Evan's go.

## Current state — screens done: B4 leverage rotation is the live lead (+2.15%/mo holdout)

**Last updated: 2026-07-09** — this file is the only live snapshot; history
lives in the record.

> **2026-07-09 — C1 + three screens (record Appendices W–Y).** Engine v2
> (`size_on_nav=True`: NAV-proportional, cash-capped; v1 refs intact; 10
> frozen refs green d=±0.0000pp). Screens (in-sample, hypothesis-generating):
> **A3 overnight-IBS DEAD** (broad negative; lev holdout +0.56%/mo < failed
> E2) — Evan's A3 override spent, IBS stop resumes; **B1 gap-reversion DEAD**
> (best +0.23%/mo); **B4 TQQQ/QQQ 200d-MA rotation STANDOUT: +2.59%/mo
> train, +2.15%/mo holdout (CAGR 29%), Sharpe ~0.8, maxDD 48–58%, ~4
> switches/yr.** Caveats recorded: screen saw the holdout (contaminated for
> prereg), variant selection, weeks-long holds stretch the "swing" label.
> **Proposed next: pre-register E4 (TQQQ/QQQ rotation) with robustness-
> battery gates + live paper as true OOS — awaiting Evan.**

> **2026-07-09 — E2 = FAIL; IBS FAMILY SHELVED (record Appendices S-U).**
> E2 (leveraged TQQQ/UPRO/SPXL/SOXL/TNA, K=2, prereg `865c09e`) holdout
> 2022-26: n=351 PASS, exp +31bps PASS, **CAGR 7.98% FAIL (vs 15%), maxDD
> 60.6% FAIL (vs 60%)**. Train 19.6% CAGR → holdout 7.98%: same OOS decay as
> E1b. The c2c (non-executable) run would have PASSED (CAGR 18.15%) — the
> overnight gap remains the killer (M1.8: 54% of edge). **Prereg §7 stop
> executed: no E2b/E1c/execution variants without a NEW dated Evan decision.**
> Engine gotcha logged: fixed initial-capital/K sizing (not NAV/K) — K=1 3x
> run sent NAV negative; future engines size on current NAV. Frozen tests:
> 8 refs (E1+E2) green d=±0.0000pp. Three-experiment scoreboard in Appendix
> U. **No live trading. Options: E3 design / Evan overrides stop for
> near-close-execution IBS / write up the arc.**

> **2026-07-09 — E1b OOS test = FAIL (near-miss) (record Appendix Q).** Evan
> chose to pre-register broad_us with a holdout. E1b (`0126ce3`): broad_us
> HOLDOUT 2022-26 next-open 5bps → n=560, exp +17.8bps (PASS), **Sharpe
> 0.4961 (FAIL vs 0.50)**, maxDD 9.8% (PASS). Fails by 0.004 of Sharpe — NOT
> rounded up. BUT the edge substantially PERSISTED OOS (train 0.66 → holdout
> 0.496 through the 2022 bear) — real-but-decayed, unlike E1's decisive fail.
> Cost is the swing factor (0bps→0.76, 10bps/side→0.23); 5bps/side is
> conservative for SPY/QQQ/DIA/IWM (~1bp spreads). Sectors confirmed dead
> weight (Sharpe −0.05). **No live trading. Awaiting Evan — options below.**

> **2026-07-09 — E1 = FAIL (record Appendices N-P).** Full 29-ETF IBS run per
> `8963e49`: Sharpe 0.23, maxDD 36% → FAIL, no tuning. Cost-fragile; country
> ETFs drag; post-2021 decay. Frozen refs pinned (green, d=0.0000pp).

> **2026-07-09 — M0.4 executed (record Appendix H).** Coverage/quality gate
> `swing_bot/coverage_gate.py` (coverage vs listed-tickers + sanity scan);
> done-check green (OK on real data, fails on truncated fixture). Found 19
> real zero-range bars in XLRE's first 5 months → **E1 MUST skip high==low
> days (IBS div-by-zero); logged in gotchas bin.** Next: M0.5 (frozen-
> regression harness).

> **2026-07-08 — M0.3 executed (record Appendix G).** Frozen 29-ETF universe
> in `swing_bot/universe.py` (4 broad US + 11 SPDR sectors + 14 country/
> regional), each with a verified first-bar date + inclusion reason. Full
> backfill (`scripts/backfill_universe.py`) wrote 89,666 rows into
> `swing.db`. Flag for later: country-ETF IBS has a stale-NAV/overnight
> mechanism distinct from US-index IBS — report E1 per-group. Next: M0.4
> (coverage/quality gate).

> **2026-07-08 — M0.2 executed (record Appendix F).** Data-path decision:
> **own yfinance fetcher**, NOT reuse of Trading's price_cache. Reason:
> price_cache has no high/low/open series (only close+volume+flags), so IBS
> is uncomputable from it; it also lacks DIA/IWM + all country ETFs and has
> no next_open for ETFs. Wrote `swing_bot/prices.py` (OHLCV → `swing.db`,
> `auto_adjust=False`); validated (SPY/QQQ backfilled, IBS computes).
> Tooling: Grep/Glob don't reach `D:\ClaudeCode\Trading`; use venv-python +
> PowerShell for its DB. Next: M0.3 (freeze ETF universe).

> **2026-07-08 — M0.1 (record Appendix E).** Repo skeleton, `.venv`, git
> init; commits `4ac785c`/`940a239`; deps pinned `3ba9cc1`
> (requirements.txt + requirements.lock). Env note: Python 3.14 + pandas 3.0
> are bleeding-edge — pin/downgrade rather than code around any pandas edge.

### Workstreams (mapped to PRD milestones)

| Workstream | PRD | Status | Notes |
|---|---|---|---|
| Doc/memory system | — | **Done** | Bootstrapped 2026-07-08 |
| PRD_ROADMAP.md | — | **Done** | Written 2026-07-08 to council program + Evan's overlay decision |
| Foundations (repo/venv/data/universe/gate/tripwire) | M0 | **Done** | All 5 tasks; modules prices/universe/coverage_gate/signals/test_frozen; `swing.db` 89,666 rows |
| Pre-registration & fill ablation | M1 | **Done** | M1.6 power (`2a9edde`) + M1.7 prereg (`8963e49`) + M1.8 ablation; next-open keeps ~64% |
| E1 IBS backtest | M2 | **Done — E1 FAILED** | Engine (`415c527`), verdict (`d28f899`), frozen refs pinned. E1b OOS near-miss (Sharpe 0.4961, `1a71468`). M2.12 survivorship deferred |
| E2 leveraged-ETF IBS (high-return arm) | M2b | **Done — E2 FAILED** | Prereg `865c09e`; CAGR 7.98%/maxDD 60.6% vs 15%/60% gates; refs pinned; **IBS family SHELVED (pre-committed stop)** |
| E3 concentrated stocks | M2c | **Stub — next open path** | Different signal family; own prereg; survivorship caveat mandatory |
| Live paper: control + LLM-veto sleeves | M3 | **BLOCKED — gate not open** | E1 did NOT pass M2→M3; needs a new pre-registered strategy that passes + Evan go + Alpaca account |
| Overlay readout (continue/cascade/kill) | M4 | **GATED** | At pre-registered N / time horizon |
| Expansion (deferred ideas) | M5 | **GATED** | On M3 stable |

## Candidate strategies (supplied by Evan 2026-07-08 — none chosen yet)

| # | Strategy | Codifiability | Notes |
|---|---|---|---|
| 1 | Trend pullback (20 EMA > 50 EMA, buy 1–3 day dip to 20 EMA, stop below pullback low) | High | Objective rules, EOD-data friendly |
| 2 | Bull-flag breakout (pole + flag channel, buy resistance break) | Low | Pattern detection is fuzzy; hardest to backtest honestly |
| 3 | Mean reversion (RSI < 30 / Bollinger extremes, capitulation + reversal day) | High | Survivorship bias hits this hardest — delisted crashers are exactly what it buys |
| 4 | Sector rotation (leading sector ETFs → leading stocks breaking out) | Medium | Longer holds; overlaps Trading's `sector_momentum` factor |

Full descriptions as Evan gave them: record Phase 0.

## Reusable infrastructure (map of `D:\ClaudeCode\Trading` — verify before use)

- **Data**: `scripts/momentum/daily_price_refresh.py` (~5,200 tickers, EOD),
  `price_cache` SQLite table (SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED,
  `auto_adjust=False`; also caches `next_open`), `trading_bot/factors/universe.py`
  data-quality/universe filters (MIN_DOLLAR_VOL currently 0 — a known gap that
  becomes mandatory to fix at this capital size).
- **Backtest**: `trading_bot/execution/factor_backtest.py` harness;
  frozen-regression-test pattern in `trading_bot/strategies/test_strategies.py`.
- **Paper engine**: `trading_bot/execution/paper_trader.py` schema
  (paper_portfolio / paper_positions / paper_nav / paper_transactions)
  tolerates any cadence; `paper_rebalance.py`'s buy-top-N-hold-a-month logic
  will NOT transfer.
- **Alpaca PAPER**: `alpaca_client.py` (live hard-guarded), `alpaca_sync.py`
  (CASH_BUFFER = 0.01), `fractionability.py` — whole-share fallback is
  load-bearing, not an edge case, at $100–1,000.
- Trading's own `HANDOFF.md` / `.claude/codebase-memory/` are ground truth for
  that repo; the inventory in record Phase 0 is the map, not the territory.

## Hard constraints

- EOD data only: signals computed at close, executed next open. No intraday
  entries or candlestick-trigger logic until an intraday data source exists.
- At $100–1,000, spread/slippage and fractionability dominate economics; a
  real liquidity floor is mandatory, not optional.
- Survivorship bias (yfinance carries currently-listed names only) — every
  backtest is upper-bound-biased; short-horizon mean reversion worst-affected.
- Never modify anything in `D:\ClaudeCode\Trading` from this project without
  Evan's explicit instruction. Never run backtests concurrently against
  Trading's DB.
- If Trading's `price_cache` is reused: read-only from here, and honor
  split-adjusted / dividend-UNadjusted everywhere.

## Decisions taken 2026-07-08 (details in record Appendices B–C)

- Strategy: E1 = ETF IBS mean reversion, per evidence brief + council.
- LLM overlays KEPT and LIVE-ACTING (Evan, overriding council's power-based
  drop; amended same day from a shadow-mode draft) — M3 runs `e1_control`
  (mechanical) + `e1_llm_veto` (treatment) sleeves in parallel from day one;
  overlay readout/kill decision gated on pre-registered N (PRD M4).
- Data layer: read Trading's `price_cache` read-only if ETF coverage
  confirms (PRD M0.2 verifies), own `swing.db` for positions/results.
- Bull flag / sector rotation / 16 other ideas dropped with documented
  reasons (record Appendix B).

## Open decisions (BLOCKED-ON-EVAN)

- ~~POST-E1b direction~~ **RESOLVED 2026-07-09 by Evan's goal redefinition
  (record Appendix R): high-return concentrated path → E2 (leveraged-ETF
  IBS) next, E3 (stocks) after. Prior option menus preserved in record
  Appendices P/Q.**
- **Capital range**: brief says $100–1,000; inventory header said $100–10,000.
  Assuming $100–1,000; sizing is parameterized regardless.
- **Alpaca PAPER account** (PRD M3.15): which of ~3 paper accounts — only
  relevant once a strategy passes and live is authorized.
- **M2.12 survivorship bound**: deferred as moot for failed ETF-only E1; run
  only if a stock strategy enters scope.

## Documentation
- `docs/Project Record — Full Chronological History.md` — append-only
  chronological record; the ground truth. No HTML twin yet.
- `PRD_ROADMAP.md` — the standing plan (written 2026-07-08). Source of truth
  for what to build and in what order; next open task = M0.1.
- `docs/research/` — evidence brief, experiment-ideas list (+ council
  outcome pointer), future power calc / ablation docs.
- `.claude/codebase-memory/` — binned technical memory (INDEX + 6 bins).
- `.claude/pm-cadence.json` — record entry every 3 prompts;
  handoff/PRD/bins event-driven.
