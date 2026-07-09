# Swing Trading — Experimental Program PRD & Roadmap

**Written 2026-07-08 by Claude (Fable 5 session), decisions by Evan. Standing
document — the executing model works through TASK BREAKDOWN top to bottom,
one task at a time, and checks off SUCCESS CRITERIA.**

**SCOPE GUARD (decided by Evan 2026-07-08): NEVER modify anything in
`D:\ClaudeCode\Trading` (repo or DB) from this project. Trading's
`price_cache` is READ-ONLY from here; never run backtests concurrently with
Trading's. Paper trading only — no real-money order paths, period. No
strategy surface beyond this PRD without a new dated Evan decision. If a
task seems to require breaking any of these, STOP and report.**

---

## 1. OBJECTIVE

Build a systematic swing-trading bot (holds days–weeks, $100–1,000 capital,
Alpaca PAPER) and run the council-selected experimental program (record
Appendix B, 2026-07-08): prove or kill ETF IBS mean reversion against
PRE-REGISTERED criteria, with execution-timing honesty and always-on
divergence logging. The documented rigor loop — pre-registration before
code, kill-switches, honest negative results — is the deliverable as much as
the strategy. LLM overlays are KEPT and LIVE-ACTING from
day one (decided by Evan 2026-07-08, amended same day from the earlier
shadow-mode draft, overriding the council's drop): M3 runs a control sleeve
(pure mechanical E1) and an LLM cash-veto treatment sleeve in parallel —
Trading's control-vs-treatment pattern at daily cadence. The overlay trades
immediately; statistical CONCLUSIONS about it wait for the pre-registered N
(the council's power objection binds the claims, not the running).

## 2. CONTEXT

### What exists (verified 2026-07-08)

- This project: docs only. `HANDOFF.md`, append-only record (Phase 0 +
  Appendices A–B), `.claude/codebase-memory/` bins,
  `docs/research/2026-07-08_small-account-swing-strategies.md` (evidence
  brief), `docs/research/2026-07-08_experiment_ideas.md` (30 ideas +
  council outcome). No code, no git repo, no venv, no DB.
- `D:\ClaudeCode\Trading` (reference implementations to PORT, not import):
  `trading_bot/execution/paper_trader.py` (sleeve DB schema),
  `alpaca_client.py` / `alpaca_accounts.py` / `alpaca_sync.py`
  (CASH_BUFFER=0.01) / `fractionability.py`,
  `strategies/test_strategies.py` (frozen-regression pattern),
  `scripts/momentum/daily_price_refresh.py` (yfinance convention),
  `factors/universe.py` (data-quality filters).
- Trading's `price_cache` SQLite: close/next_open series, SPLIT-ADJUSTED,
  DIVIDEND-UNADJUSTED (`auto_adjust=False`). ETF coverage UNVERIFIED — M0
  task 2 checks it.

### Must not break

- Trading repo/DB untouched (scope guard) — testable: `git -C
  D:\ClaudeCode\Trading status` clean of our fingerprints; no writer in this
  repo opens Trading's DB in write mode.
- Price convention: every price consumer/writer in this project states
  split-adjusted / dividend-UNadjusted in a header comment.
- Record append-only; pre-registration ordering (doc commit BEFORE backtest
  engine commit) — provable from `git log` forever after.
- Once pinned (M2 task 11): frozen-regression tests print d=±0.0000pp after
  every strategy/factor change.

## 3. SUCCESS CRITERIA

- [ ] Git history proves pre-registration: commit of
      `docs/prereg_E1_ibs.md` predates the first commit of any backtest
      engine code (`git log --follow --oneline` pasted in the record).
- [ ] Power calc documented: IBS<0.20 signal counts/year across the ETF
      universe, computed WITHOUT looking at post-signal returns.
- [ ] Fill-timing ablation (#15+#13) produces per-ETF close-to-close vs
      next-open haircut numbers, saved in docs + record.
- [ ] E1 (ETF IBS MR) backtest run against pre-registered gates; PASS or
      FAIL stated plainly in a record entry either way.
- [ ] Frozen-regression tripwire pinned and green:
      `python -m swing_bot.test_frozen` prints d=±0.0000pp.
- [ ] (Gated) Live paper sleeve ≥20 consecutive trading days unattended;
      `fill_divergence` table populated; NAV table in a record entry.
- [ ] (Gated) Control and LLM-veto treatment sleeves both live from M3 day
      one; control sleeve provably unaffected by overlay decisions
      (assertion in code); every decision logged with UNIQUE(date,ticker).
- [ ] Overlay readout happens at the pre-registered N / time horizon, not
      before; interim numbers labeled descriptive-only in every doc.

## 4. CONSTRAINTS

- Capital assumption $100–1,000 (Evan's brief 2026-07-08; the $100–10,000
  figure in the pasted inventory remains unconfirmed — sizing code takes
  capital as a parameter so this never hard-codes).
- Data: EOD only. Signals at close; fills per the model the ablation
  validates. No intraday logic. `next_open` comes from cache, never invented.
- Alpaca PAPER only. Fractional orders are DAY-TIF only (no GTC stops —
  exits re-armed daily or software-managed). Do NOT read
  `pattern_day_trader` / `daytrade_count` / `daytrading_buying_power` —
  removed from the Alpaca API as of 2026-07-06 (PDT rule eliminated
  2026-06-04, FINRA 26-10).
- Paper fills are SIMULATED (filled at quote; no queue/impact/partials) —
  every divergence/slippage artifact carries this caveat in writing.
- Own SQLite DB (`swing.db` at project root) for positions/NAV/results/logs.
  Prices: read Trading's `price_cache` read-only IF M0 task 2 confirms ETF
  coverage; else own fetcher into `swing.db` honoring the same convention.
- Out of scope — do not start even if convenient: real-money trading; any
  strategy from the dropped-16 list (record Appendix B); intraday data
  sources; dashboards beyond a minimal status page; touching Trading's
  scheduler tasks.
- Environment: Windows 11, PowerShell 5.1 primary. Project venv at
  `.venv\` (create in M0), run via `.venv\Scripts\python.exe`. Never rewrite
  JSON with PowerShell; no `node -e` with arrow functions; `.bat` files pure
  ASCII. Per-task commits AUTHORIZED by this PRD once git init lands (M0
  task 1); NEVER push without Evan's instruction.

## 5. MILESTONES

| # | Milestone | Goal |
|---|---|---|
| M0 | Foundations | git repo, venv, data access verified, ETF universe frozen, coverage gate, tripwire harness |
| M1 | Pre-registration & ablation | power calc → pre-reg doc committed → fill-timing ablation (#15+#13) |
| M2 | E1 backtest | IBS MR engine, run vs pre-registered gates, pin frozen refs, survivorship bound (#27) |
| M3 | Live paper (GATED on M2 pass + Evan approval) | daily loop, Alpaca mirror, divergence logging (#28), control + LLM-veto sleeves live from day one |
| M4 | Overlay readout (GATED on pre-registered N/horizon) | evaluate veto vs control; continue, add cascade arm, or kill per pre-reg |
| M5 | Expansion (GATED on M3 stable) | deferred ideas only: exit/stop ablations (#17/#18), sizing (#20), RSI comparison (#2), mega-cap pullback (#5), VIX gate (#11) |

Order is deliberate: infrastructure before science (council 5/5); thresholds
provably precede results (M1 before M2); nothing goes live on an unvalidated
edge (M3 gate); the overlay Evan wants trades from day one but inside a
controlled design — a separate treatment sleeve that can never contaminate
the mechanical control, with conclusions gated on pre-registered N (M4);
breadth only after one strategy survives contact (M5 last).

## 6. TASK BREAKDOWN

### M0 — Foundations

1. **Project skeleton + git init.** `swing_bot/` package, `scripts/`,
   `.gitignore` (venv, `swing.db`, `*_keys.env`), `.venv` via
   `python -m venv .venv`, `requirements.txt` (yfinance, httpx; pytest
   optional — frozen tests use their own `__main__`). Initial commit.
   Done: `git log --oneline` shows the commit;
   `.venv\Scripts\python.exe -c "import yfinance, httpx"` exits 0.
2. **Verify ETF price coverage in Trading's `price_cache` (READ-ONLY).**
   Script opens the DB read-only (`file:...?mode=ro`), reports rows/date
   span for each candidate universe ticker. If coverage is full → write
   `swing_bot/prices.py` read-only reader. If not → own yfinance fetcher
   writing to `swing.db` with `auto_adjust=False` + convention header.
   Done: script output pasted in record; chosen path stated.
3. **Freeze the ETF universe.** `swing_bot/universe.py`: broad US (SPY, QQQ,
   DIA, IWM) + the SPDR sectors + a small international/country set per the
   Pagonidis/arXiv papers. Each ticker gets a one-line inclusion reason and
   its listing date. Dated, committed; changes require a new dated decision.
   Done: file exists; every ticker has reason + listing date.
4. **Data-coverage gate.** `swing_bot/coverage_gate.py`: refuses to emit
   signals unless 100% of the universe has a bar for the as-of date (tiny
   universe → no partial-coverage tolerance needed).
   Done: unit check — truncated fixture data makes it exit nonzero.
5. **Frozen-regression harness.** `swing_bot/test_frozen.py` with own
   `__main__`, Trading's pattern: reference-number table, ±0.0000pp
   comparison, loud failure. Ships with mechanics-proving placeholder
   fixtures; real refs pinned in M2 task 11.
   Done: `.venv\Scripts\python.exe -m swing_bot.test_frozen` runs green.

### M1 — Pre-registration & ablation

6. **Power calculation (NO RETURN PEEKING).** Count IBS<0.20 signal days
   per ticker per year over full cached history. Compute signal counts
   ONLY — post-signal returns are off-limits until after task 7 commits.
   Output: `docs/research/<date>_E1_power.md` — signals/year, expected
   trades at plausible concurrency caps, months-to-N under pre-reg N.
   Done: doc committed with real counts; states whether E1 is powerable
   and on what timeline.
7. **Pre-registration doc — THE ordering-critical task.**
   `docs/prereg_E1_ibs.md`: exact entry/exit rules (IBS<0.20 entry; exit
   IBS>0.80 or time stop, parameters fixed); evaluation window; BOTH fill
   models to be reported; kill criteria (minimum closed-trade N from task
   6, expectancy floor, Sharpe floor, max-drawdown cap); AND the overlay
   experiment's own pre-registration — arms (control + cash-veto; cascade
   deferred), decision N and/or fixed time horizon for the readout,
   overlay kill criteria (Trading's discipline: drop if veto decisions
   don't predict outcomes by the readout point). Explicit "no parameter
   changes after this commit" clause. Committed BEFORE any backtest-engine
   code exists.
   Done: commit hash recorded in the record entry; repo contains no
   backtest engine yet at that hash.
8. **Fill-timing ablation (#15 + #13).** `scripts/ablation_fill_timing.py`:
   on every historical IBS<0.20 signal, compare (a) close-to-close returns
   (the published effect), (b) next-open entries (the default executable
   loop), (c) the overnight-only component (close→next open). Simple
   vectorized study — not the backtest engine.
   Done: per-ETF haircut table in `docs/research/` + record entry naming
   which fill model M2 will treat as primary.

### M2 — E1 backtest

9. **Minimal daily backtest engine.** Purpose-built for a small-basket MR
   sleeve (~200 lines): positions, cash, fills per chosen model, MTM,
   closed-trade ledger. Do NOT adapt Trading's `factor_backtest.py`
   (monthly top-N economics baked in). Every module: convention header.
   Done: toy-series unit checks — hand-computed P&L reproduced exactly.
10. **Run E1 per pre-registration.** Both fill models, full window, capital
    parameter at $500 nominal. Full results table (trades, expectancy,
    Sharpe, maxDD, exposure) into a record entry — PASS or FAIL against
    every pre-registered gate, stated plainly. A FAIL is a valid,
    publishable outcome; do not tune parameters to rescue it (that path
    requires a new pre-registration doc and Evan's sign-off).
    Done: record entry exists with the verdict.
11. **Pin frozen-regression references.** Two short windows × the E1
    config(s) pinned to exact tpnl%/closed_count.
    Done: `python -m swing_bot.test_frozen` prints d=±0.0000pp.
12. **Survivorship bound (#27).** Same engine, same rules, on an
    always-listed mega-cap basket vs the ETF universe; document the delta
    as the project's standing survivorship caveat.
    Done: comparison table in docs + record.
13. **GATE — BLOCKED-ON-EVAN.** Present M2 results; M3 starts only on E1
    PASS + Evan's explicit go. On FAIL: stop, record, await direction
    (fallback candidates: deferred list, M5).

### M3 — Live paper (gated)

14. **Sleeve DB + daily loop.** Port `paper_trader.py` schema into
    `swing.db` (portfolio/positions/nav/transactions + `fill_divergence` +
    `overlay_log`), TWO sleeves from day one: `e1_control` (pure mechanical)
    and `e1_llm_veto` (treatment). `scripts/daily_swing.py`: refresh →
    coverage gate → signals → control orders computed and finalized BEFORE
    any overlay call (runtime assertion) → overlay decisions applied to the
    treatment sleeve only → MTM both. Exits software-managed daily (DAY-TIF
    constraint).
    Done: dry-run against a historical date produces hand-checkable orders
    for both sleeves; control orders byte-identical with overlay disabled.
15. **Alpaca PAPER account — BLOCKED-ON-EVAN.** Which of the ~3 paper
    accounts (some hold Trading sleeves); keys into gitignored
    `alpaca_keys.env`. Reported, never worked around.
16. **Alpaca mirror port.** `alpaca_client.py` + `alpaca_sync.py` pattern:
    paper base URL, live hard-guard kept, CASH_BUFFER=0.01, fractionability
    whole-share fallback, dry-run default / `--execute`. Mirrors
    `e1_control` (one Alpaca account; the treatment sleeve lives DB-only
    unless a second account frees up — decide at task 15). Strip every PDT
    field reference.
    Done: dry-run sync prints sane target orders; grep confirms no
    `daytrade` / `pattern_day_trader` reads.
17. **Divergence logging (#28).** Every fill: DB-sim price vs Alpaca-paper
    fill into `fill_divergence`, with the simulated-fill caveat in the
    module docstring and in `HANDOFF.md`.
    Done: first live day populates the table.
18. **Overlay live cash-veto arm (Evan's decision 2026-07-08, amended from
    shadow-mode the same day).** Every entry candidate gets an LLM verdict
    (BUY/VETO + invalidation + rationale) logged to `overlay_log` —
    UNIQUE(date,ticker), Trading's overlay-log schema. VETO → the treatment
    sleeve sits that entry out in cash (cash-veto arm); the control sleeve
    always takes it. Cascade arm deferred to the M4 readout. Interactive
    runbook first (Trading's `overlay_prep` pattern — no API key needed);
    unattended mode optional later and BLOCKED-ON-EVAN (needs
    ANTHROPIC_API_KEY). All interim overlay numbers labeled
    descriptive-only until the pre-registered readout.
    Done: signal-day dry run writes decision rows and diverges ONLY the
    treatment sleeve; control unaffected (task 14 assertion holds).
19. **Scheduling.** Daily `.bat` (pure ASCII) → Task Scheduler, Trading's
    daily.bat pattern (refresh → loop → mirror → stamp log).
    Done: task fires on a test run; stamp log written.
20. **Stabilization month.** ≥20 consecutive trading days unattended, both
    sleeves; misses/interventions logged honestly.
    Done: record entry with per-sleeve NAV table, divergence stats,
    overlay-decision count vs the pre-registered N trajectory.

### M4 — Overlay readout (gated on pre-registered N / time horizon)

21. **Evaluate veto vs control at the pre-registered point** — not before,
    however tempting interim numbers look. Did vetoes predict worse
    outcomes? Per pre-reg: continue, add the cascade arm as a third sleeve,
    or KILL the overlay (Trading's kill-switch discipline). If N is
    arriving too slowly to ever read out, report that honestly as the
    result.
    Done: dated continue/expand/kill decision in the record with the
    numbers.

### M5 — Expansion (gated on M3 stable; one at a time, in this order)

22. Exit-rule ablation (#17) → 23. Stop-loss ablation (#18) → 24. Sizing
    (#20) → 25. RSI(2) comparison arm (#2, backtest only) → 26. Mega-cap
    pullback (#5) as second strategy → 27. VIX gate (#11). Each gets its own
    pre-registration section before running.

## 7. HANDOFF NOTES

**Read first, in order:** project `CLAUDE.md` → `HANDOFF.md` → this PRD →
record front-matter (`docs/Project Record — Full Chronological History.md`).
**Work order:** M0 → M5 strictly. One task per sitting; finish (done-check
+ commit + record entry) before the next.
**Gotchas that will bite you:**
- Pre-registration ordering is sacred: if backtest-engine code exists
  before `docs/prereg_E1_ibs.md` is committed, the project's core claim is
  dead. When in doubt, commit the doc first.
- Trading's DB is read-only from here; open with SQLite URI `mode=ro`.
  Never run our backtests while Trading's are running.
- Prices are split-adjusted, dividend-UNadjusted — state it in every
  module header; dividend-heavy ETFs understate long-hold returns, note it
  in result docs.
- Alpaca: PDT fields are GONE from the API (2026-07-06); fractional orders
  are DAY-TIF only; paper fills are simulated — caveat every slippage claim.
- The power calc (task 6) must never compute post-signal returns — that's
  peeking before pre-registration.
- A FAILED experiment honestly recorded is a deliverable, not a setback —
  do not tune past a pre-registered kill.
- `.bat` pure ASCII; JSON via Python/Node only; venv python is
  `.venv\Scripts\python.exe`.
