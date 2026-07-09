# Handoff

## Goal

Build a swing-trading bot — positions held days to a few weeks, sized for
genuinely small capital ($100–1,000) — as a SEPARATE project from the
long-term momentum bot in `D:\ClaudeCode\Trading`. Same ethos as Trading:
**build rigor + a track record**, paper first; the documented process is the
portfolio asset. Reuse Trading's infrastructure selectively (backtest harness,
paper-trading DB pattern, Alpaca PAPER mirror) — not its factor logic, which
is long-horizon.

## Current state — M0 in progress (M0.1–M0.3 done)

**Last updated: 2026-07-08** — this file is the only live snapshot; history
lives in the record.

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
| Foundations (repo/venv/data/universe/gate/tripwire) | M0 | **In progress** | M0.1–M0.3 done; own OHLCV fetcher + frozen 29-ETF universe, `swing.db` backfilled (89,666 rows); next M0.4 (coverage gate) |
| Pre-registration & fill ablation | M1 | **Not started** | Ordering-critical: prereg doc before engine code |
| E1 IBS backtest | M2 | **Not started** | Gated behind M1 |
| Live paper: control + LLM-veto sleeves | M3 | **GATED** | Needs M2 PASS + Evan go; Alpaca account BLOCKED-ON-EVAN |
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

- **Capital range**: Evan's 2026-07-08 brief says $100–1,000; his pasted
  infrastructure-inventory header says $100–10,000. Assuming $100–1,000
  (live instruction wins); sizing code parameterizes capital regardless.
- **Alpaca PAPER account** (PRD M3.15): ~3 paper accounts per login, some
  already used by Trading sleeves — which account this project gets.
- **M2→M3 gate** (PRD M2.13): live paper starts only on E1 PASS + Evan go.

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
