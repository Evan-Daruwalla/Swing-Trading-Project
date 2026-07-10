# Swing Trading — a falsification program for a small-account systematic trader

**Author:** Evan Daruwalla · **Status:** first research program complete
(2026-07-10), nothing live · **Data:** end-of-day, small capital
($100–1,000), Alpaca paper target.

## What this is

A systematic-trading research project whose goal was a **high percentage
return over short holds** with a small account. It did not find one — and the
*discipline of how it failed* is the point. Ten strategies across five
families were tested under strict **pre-registration** (rules committed to git
*before* the code that produces results), honest kill-criteria (no re-tuning a
failed run), and out-of-sample / out-of-regime tests — culminating in an
international test on five independent markets and a survivorship-aware stock
test, neither used to design anything.

**The honest conclusion:** no robust, regime-independent, cost-surviving
high-return EOD strategy was found across five plausible families — index
mean reversion, leveraged trend, concentrated stock momentum, volatility
breakout, and deep-dip accumulation (0 passes in 10 attempts). This
is backed by out-of-sample evidence from five international regimes (including
the 1990s Japan secular bear) and a survivorship-*flattered* stock test that
still failed. The one partly-deployable result — a 1× 200-day-MA rotation — is
a *market-dependent risk-management overlay*, not a return engine. A rigorous
process correctly told the builder his goal was unreachable with these tools,
before the market charged tuition for the same lesson.

## Read this first

- **[The findings write-up](docs/findings_2026-07-09_experiment_arc.md)** —
  the deliverable: the full E1→E7 arc, method, results, and honest conclusion.
- **[HANDOFF.md](HANDOFF.md)** — current one-page state.
- **[Project record](docs/Project%20Record%20%E2%80%94%20Full%20Chronological%20History.md)**
  — the append-only, dated build log (Appendices A–AF), ground truth.
- **[PRD_ROADMAP.md](PRD_ROADMAP.md)** — the standing execution plan.

## The experiments (all pre-registered, all committed)

| # | Idea | Verdict |
|---|---|---|
| E1 / E1b / E2 | IBS mean reversion (ETFs, broad-US, 3× ETFs) | FAIL — edge is in the overnight gap an EOD bot can't capture; dies on cost |
| E4 | 3× MA leverage rotation | PASS in-sample (33%/yr) … |
| E5 | …E4 across the 2000–13 crashes | FAIL — 93% drawdown; a bull-market artifact |
| E6 | 1× MA rotation | PASS — robust drawdown overlay, but ≈ index return (risk-mgmt, not high return) |
| E7 | International out-of-sample (5 non-US indices) | FAIL — even a-priori-vol-gated 3× fails everywhere; E6 downgraded to market-dependent |
| E3 | Concentrated stock momentum (top-3) | FAIL (clean) — 6% vs 15% bar even bias-flattered; lost to buy-and-hold |
| E8 | Volatility-compression breakout (squeeze) | FAIL — −1.4%/yr in 2000–13, +1.1%/yr even in the 2014–26 bull; compression predicts expansion, not direction |
| E9 | "Never book a loss" deep-dip audit (Reddit's top claim) | FAIL — the claim is *literally true* (0/53 realized losses) and still bad: 3.5%/yr, a −80% unrealized position, a 17-year underwater hold |

## Reproduce

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.lock
.venv\Scripts\python.exe -m swing_bot.test_frozen        # frozen tripwire, d = +/-0.0000pp
.venv\Scripts\python.exe -m scripts.run_e1_backtest      # (and run_e4/e5/e6/e7_*)
```

Code: `swing_bot/` (`prices`, `universe`, `coverage_gate`, `signals`,
`backtest`, `rotation`, `test_frozen`); `scripts/` (per-experiment runners).
Data convention: split-adjusted, dividend-UNadjusted (yfinance
`auto_adjust=False`). Pre-registration docs and every commit hash are listed
in the findings write-up's reproducibility section.

## What is deliberately not here

No live trading, no real money, no dashboard. This is a research record, not a
product. The value is the method: a checkable, dated, falsifiable program —
not an equity curve.
