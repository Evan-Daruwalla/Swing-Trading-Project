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

**GOAL (redefined by Evan 2026-07-09 — supersedes the 2026-07-08 framing;
record Appendix R):** build a swing trader that, as accurately as possible,
invests in a stock or a few stocks (concentrated, K=1–3) with a small amount
of money to earn a HIGH PERCENT RETURN over a shorter amount of time. Losing
money is acceptable and expected — the risk is Evan's, accepted explicitly.
Consequences: future pre-registrations gate on RETURN (CAGR/expectancy)
first, with substantially loosened — but never absent — drawdown ceilings
(ruin guard); single stocks are in scope (survivorship caveat mandatory);
the rigor machinery below is RETAINED as the accuracy instrument, not as a
conservatism instrument. First high-return arm: E2 (leveraged-ETF IBS),
because E1b proved the IBS edge persists OOS in exactly the underlyings the
leveraged funds wrap.

Original 2026-07-08 program (E1, complete — FAILED honestly; E1b near-miss):
build and run the council-selected experimental program (record Appendix B):
prove or kill ETF IBS mean reversion against PRE-REGISTERED criteria, with
execution-timing honesty and always-on divergence logging. The documented rigor loop — pre-registration before
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
- [ ] (M2b) Git history proves `docs/prereg_E2_leveraged_ibs.md` predates the
      E2 runner; E2 verdict stated PASS/FAIL per criterion in the record.
- [ ] (M2b) Frozen tests green (d=±0.0000pp) with E2 refs pinned alongside
      E1's.

## 4. CONSTRAINTS

- Capital assumption $100–1,000 (Evan's brief 2026-07-08; the $100–10,000
  figure in the pasted inventory remains unconfirmed — sizing code takes
  capital as a parameter so this never hard-codes).
- Data: EOD only. Signals at close; fills per the model the ablation
  validates. No intraday logic. `next_open` comes from cache, never invented.
- Alpaca PAPER only. Fractional/notional orders support market **and**
  limit/stop/stop-limit (confirmed 2026-07-13, record Appendix BO; already
  noted in the 2026-07-08 small-account brief) — the binding constraint is
  **TIF = DAY only** (no GTC — exits re-armed daily or software-managed) and
  **no fractional shorting** (long-only unless whole shares). "DAY-TIF" here
  never meant market-only; use a marketable DAY limit to cap fill price. Do NOT read
  `pattern_day_trader` / `daytrade_count` / `daytrading_buying_power` —
  removed from the Alpaca API as of 2026-07-06 (PDT rule eliminated
  2026-06-04, FINRA 26-10).
- Paper fills are SIMULATED (filled at quote; no queue/impact/partials) —
  every divergence/slippage artifact carries this caveat in writing.
- Own SQLite DB (`swing.db` at project root) for positions/NAV/results/logs.
  Prices: read Trading's `price_cache` read-only IF M0 task 2 confirms ETF
  coverage; else own fetcher into `swing.db` honoring the same convention.
- Risk posture (Evan 2026-07-09, record Appendix R): high-return objective;
  losses acceptable and expected. Gates emphasize return; drawdown ceilings
  are loosened per-prereg but a ruin guard always exists. This changes gate
  NUMBERS, never gate DISCIPLINE (pre-reg before results, no tuning on FAIL).
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
| M2b | E2: leveraged-ETF IBS — high-return arm (added by Evan's 2026-07-09 goal redefinition) | frozen leveraged universe, return-centric pre-reg, run vs gates, pin refs |
| M2c | E3: concentrated mega-cap stocks (stub — designed after E2 readout) | liquidity-defined stock universe + survivorship caveat; own pre-reg |
| M2d | Rotation family (E4/E5/E6, done 2026-07-09) | 3× MA rotation PASS-then-regime-FAIL; 1× (E6) robust drawdown overlay |
| M2e | E7: international validation (added 2026-07-10, record Appendix AF) | genuinely-unseen non-US regimes (Nikkei 1990s bear etc.): Arm 1 confirm E6 1×, Arm 2 a-priori-vol-gated 3× high-return shot |
| M3 | Live paper (GATED on a passing pre-registered strategy + Evan approval) | deploy best E-series survivor; daily loop, Alpaca mirror, divergence logging (#28), control + LLM-veto sleeves |
| M6 | Portfolio packaging | README → findings doc, record HTML twin, git tag; make the repo readable cold |
| M4 | Overlay readout (GATED on pre-registered N/horizon) | evaluate veto vs control; continue, add cascade arm, or kill per pre-reg |
| M5 | Expansion (GATED on M3 stable) | deferred ideas only: exit/stop ablations (#17/#18), sizing (#20), RSI comparison (#2), mega-cap pullback (#5), VIX gate (#11) |
| M7 | Catalog arc E13–E17 (added 2026-07-10, record Appendix AT) — **DONE 2026-07-11** | the five untested-with-merit ideas from the strategy-catalog brief: turn-of-month, sector momentum, earnings-announcement premium, x-sectional reversal, days-to-cover; dual-bar verdicts (D1 APPROVED 2026-07-12). Outcome: E13/E14/E15/E16 all FAIL both tiers, E17 BLOCKED-ON-DATA |
| M7b | Data-type arc E18–E20 (added 2026-07-12, record Appendix AV) — **CLOSED 2026-07-13: E18/E20 DONE 2026-07-11; E19 FAIL 2026-07-13** | new-data-type ideas from the data-type brief: E18 regime-gate bake-off (VIX-TS/HY-OAS/breadth/200DMA) — VIX-TS cleared the program's first (weak) PASS-RA; E19 insider opportunistic-buy drift (EDGAR) — full ingestion authorized + running (task `b2wzwj9gb`), verdict pending; E20 dividend capture FAIL; same D1 dual-bar verdicts |
| M8 | Full-method-survey candidates C1–C7 (added 2026-07-12, record Appendix BK) | seven residual candidates after reconciling ~90 methods (8 families) against E1–E20: residual reversal, dividend-initiation drift, one volatility-breakout kill-shot, vol-targeting overlay, Reg SHO short-volume drift, even-week FOMC overlay, SVXY carry — all carry strong-FAIL priors per the survey's structural finding (concentration destroys diversified-decile edges) |
| M9 | Research-batch-2 arc X1–X6 + discipline adoptions (added 2026-07-13, record Appendices BN–BP) | candidates + process upgrades from the LLM brief and the four-topic batch (execution/risk/data/crypto): prereg-template discipline (tiered costs, decomposition ladder, time-stop baseline, capped fractional-Kelly), conditional vol-targeting (E6×E18), E17-free days-to-cover (FINRA 2021+), Reg SHO short-volume drift, MOC close-entry probe, analyst recommendation-change drift ($22-gated), crypto BTC/ETH trend pilot (scope-gated), LLM forward-only arc (M3-attached) |
| M10 | Evidence-synthesis arc: state-conditioned strategies (added 2026-07-14, record Appendices CG–CK) — **DONE** | compose the 31 results into strategies vs BOTH D1 tiers; a design panel proved fixed-weight PASS-HR is arithmetically empty → the only escape is state-conditioning on a causal variable. M10-1 Nagel Switch = program's FIRST PASS-HR (IN-SAMPLE-COMPOSED, forward-paper-only); M10-2 gap-amortized stress IBS = FAIL (closes the E2 c2c mirage). Both panel survivors run |
| M11 | Algorithmic chart-pattern detection (added 2026-07-14, Evan's direction; record Appendix CL) — **CURRENT OPEN DIRECTION, UNSTARTED** | the one untested mechanism family: rule-based (NOT LLM) detection of the chart *shapes* retail traders are taught (H&S, double top/bottom, triangles, flag breakouts), buy on pattern completion. Full-window D1-reachable; honest prior = FAIL (Lo-Mamaysky-Wang: modest info, not cost-surviving; STW / Bajgrowicz-Scaillet snoop-decay; the breakout family already 3× killed). The next honest experiment |

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
    *(Outcome 2026-07-09: E1 FAILED, E1b near-missed OOS; Evan redefined the
    goal — record Appendices O/Q/R — and directed the high-return path.)*

### M2b — E2: leveraged-ETF IBS (high-return arm; Evan's 2026-07-09 goal)

14b. **Extend the universe with a frozen `leveraged` group.** Candidates
     TQQQ, UPRO, SPXL, SOXL, TNA (3x long US equity/sector wrappers of
     underlyings where the IBS edge is validated) — first-bar dates fetched
     EMPIRICALLY (never invented), liquidity probed, appended to
     `swing_bot/universe.py` as a new dated group (universe change = dated
     decision, recorded). Backfill into `swing.db`; coverage gate must stay
     green. Done: probe output + rows in swing.db + gate exit 0.
14c. **Pre-register E2** (`docs/prereg_E2_leveraged_ibs.md`, doc-only commit
     BEFORE the runner exists). Return-centric gates per the redefined goal:
     primary = holdout CAGR / expectancy; drawdown ceiling LOOSENED (risk
     accepted) but present (ruin guard); concentration K per Evan's goal
     (1–3); same train/holdout protocol as E1b (train 2014–2021, holdout
     2022–2026, holdout = the gate); exact numbers fixed in the prereg, not
     here. Done: commit hash contains prereg only.
14d. **Run E2 per prereg; verdict PLAINLY.** No tuning on FAIL. Done:
     results doc + record entry with PASS/FAIL per criterion.
14e. **Pin E2 frozen refs** into `swing_bot/test_frozen.py` (extend
     REFERENCES). STOP at the gate — live requires PASS + Evan go + Alpaca
     account. Done: frozen tests green d=±0.0000pp.

### M2c — E3: concentrated mega-cap stocks (STUB — do not start until E2
reads out and Evan directs)

Liquidity-defined large/mega-cap universe (defined by dollar-volume floor,
NOT by picking today's winners), survivorship-bias caveat mandatory in every
result, own dated pre-registration. Signal family chosen after E2 evidence.

### M2e — E7: international validation (added 2026-07-10; the clean-data unlock)

**WHY:** US backtest data is exhausted — its two crash regimes (2000-02,
2008) have been used to judge the rotation family, so further US tweaks are
hindsight-contaminated (record Appendix AE). Non-US indices (Nikkei back to
1985, DAX/FTSE/HSI/ASX) supply GENUINELY UNSEEN, independent regimes — above
all the 1990s-2000s Japan secular bear, the most hostile trend-rotation
environment in modern history. This is the honest way to test a high-return
idea without live paper.

- **E7.1 pre-register** (`docs/prereg_E7_international.md`, doc-only commit
  BEFORE the runner). Two arms, both a-priori (no fitting on non-US data):
  Arm 1 = confirm E6's 1× MA-rotation drawdown-overlay value generalizes
  across ≥5 non-US indices; Arm 2 = a-priori-VOL-GATED synthetic-3× rotation
  (hold 3× only when index > 200d MA AND 20d annualized vol < 30% — the 30%
  fixed from first principles: 3×·30% ≈ 90% position vol is the prudence
  ceiling, NOT fit to any crash). Return-centric gates for Arm 2; drawdown-
  overlay gates for Arm 1. Nikkei is the make-or-break market.
- **E7.2 run** `scripts/run_e7_international.py` (local-index returns —
  currency-neutral mechanics test; price indices understate return by
  dividends, flagged). Verdict PLAINLY per arm, no tuning.
- **E7.3 record** results doc + record entry. Frozen tests unaffected (E7 is
  a live-fetch analysis script, not pinned).

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

### M7 — Catalog arc: E13–E17 (added 2026-07-10; sourced from
`docs/research/2026-07-10_swing_strategy_catalog.md`)

**Why this exists:** after 0/13, the catalog brief identified exactly five
ideas that are (a) genuinely untested here, (b) evidenced by peer-reviewed
sources, (c) EOD-codifiable at retail scale. Honest prior, stated up front:
none plausibly clears the 15% CAGR high-return bar; three plausibly clear a
risk-adjusted bar. Running them under the primary bar alone is theater —
hence D1 below. Rigor discipline is unchanged: doc-only prereg commit before
each runner, no tuning a FAIL, frozen tripwire green after every run, no
swing.db writes from live-fetch runners.

**D1 — APPROVED by Evan 2026-07-12 (record Appendix AW).** A pre-registered
SECONDARY verdict tier now runs alongside the unchanged primary high-return
gate. Every M7/M7b prereg fixes ALL THREE labels before running:
- **PASS-HR** (unchanged primary): net CAGR ≥ 15% AND maxDD ≤ 60% in the
  2000–2013 gate window, confirmed in 2014→end.
- **PASS-RA** (new secondary): net Sharpe ≥ 0.80 in the gate window AND
  Sharpe strictly above SPY buy-hold's in BOTH windows AND positive net
  CAGR in both windows.
- **FAIL**: neither.
This is a dated goal AMENDMENT to the 2026-07-09 return-centric decision
(per project rules, risk-appetite gate numbers change only by a new dated
Evan decision). PASS-RA does NOT authorize live capital by itself — a
PASS-RA survivor becomes an M3 paper-deploy candidate alongside E6-1×,
still gated on Alpaca account + Evan go.

Execution order = build cost × interpretability (cleanest, cheapest first).
One experiment per sitting; prereg → runner → run → results doc → record →
commit. All ETF experiments are interpretable in BOTH directions; the two
stock experiments inherit E3's survivor universe and therefore its
asymmetric-falsification framing (only a FAIL is clean).

28. **E13 — Turn-of-the-month overlay** (McConnell-Xu 2008). Hold SPY only
    during the 4-session turn window (last trading day of month through the
    first three of the next), cash otherwise; signal at close, execute next
    open; 5 bps/side; data = .e8e9_cache (already fetched). Windows/gates
    per D1; primary metric additionally reported as return-per-day-in-market
    vs SPY's. Done-check: runner output + frozen tests green + results doc.
    Build: trivial (one sitting including prereg).
    *(Outcome 2026-07-12: prereg `0324196`; D1 verdict FAIL both tiers —
    gate CAGR 1.41% (PASS-HR fails, nowhere near 15%), gate Sharpe 0.20
    (PASS-RA fails, <0.80 floor). 19.1% in-market. Results:
    `docs/research/2026-07-12_E13_results.md`.)*
29. **E14 — Diversified sector momentum** (Moskowitz-Grinblatt 1999). The 11
    SPDR sectors (frozen universe, cached): hold top-3 by trailing 126-day
    return, rebalance every 21 sessions, next-open fills, 5 bps/side,
    NAV/3 sizing. Fully survivorship-clean → a PASS would be the program's
    first interpretable pass of any tier. Benchmarks: SPY and equal-weight
    11 sectors. Done-check as #28. Build: low.
    *(Outcome 2026-07-12: prereg `f922f1f`; D1 verdict FAIL both tiers —
    gate CAGR 2.42% (PASS-HR fails), gate Sharpe 0.22 (PASS-RA fails, also
    loses SPY's Sharpe 2014→). Survivorship-CLEAN — the program's cleanest
    negative: momentum lost to equal-weight buy-hold of the same sectors
    every window. Results: `docs/research/2026-07-12_E14_results.md`.)*
30. **E15 — Earnings-announcement premium** (Frazzini-Lamont 2007). E3's 39
    survivor large-caps + cached earnings dates (E10 infra): buy at open 5
    sessions before each scheduled announcement, sell at open the session
    after it; K=5; 5 bps/side. DISCLOSED BIASES: survivor universe
    (asymmetric framing) + scheduled-date lookahead is mild but real
    (date changes correlate with bad news — flag in prereg). Done-check as
    #28. Build: low (infra exists).
    *(Outcome 2026-07-11: prereg `9b0aeb3`; D1 verdict FAIL clean — gate
    CAGR 6.36% (PASS-HR fails vs 15%), gate Sharpe 0.49 (PASS-RA fails,
    <0.80 floor). PEAD's decayed twin — the only experiment to beat both
    benchmarks in 2000–13 (EW −0.47%, SPY 1.72%), a real-but-small effect
    that faded post-2014. Results: `docs/research/2026-07-11_E15_results.md`.)*
31. **E16 — Cross-sectional short-term weekly reversal** (de Groot-Huij-Zhou
    2012). Same 39 survivor large-caps: each Friday close rank by trailing
    5-session return, buy the bottom 4 at Monday open, hold 5 sessions;
    5 bps/side (paper says the edge survives costs only in large caps —
    this is the direct test). COUNTER-EVIDENCE DISCLOSED in prereg: our
    fill-timing ablation (54% of MR edge in the overnight gap) argues the
    next-open version underperforms the paper's close-based construct.
    Asymmetric framing. Build: medium.
    *(Outcome 2026-07-11: prereg `a090294`; D1 verdict FAIL clean — gate
    CAGR **16.76%** cleared the 15% bar (first ever) but maxDD **65.9%**
    breaches the 60% ceiling (PASS-HR fails), gate Sharpe 0.61 (PASS-RA
    fails, <0.80 floor). The disclosed counter-evidence held: expected
    survivorship artifact of dip-buying survivors. Results:
    `docs/research/2026-07-11_E16_results.md`.)*
32. **E17 — Days-to-cover data probe → experiment** (Hong-Li-Ni). STEP 1 is
    a data probe only: free point-in-time HISTORICAL short-interest series
    (FINRA/exchange files) back to ≥2010 — if unavailable, E17 is recorded
    BLOCKED-ON-DATA and closed without a prereg (the E10 probe pattern).
    If available: long low-SI-decile / avoid high-DTC screen, monthly.
    Build: unknown until probed; do the probe last, after 28–31.
    *(Outcome 2026-07-11: BLOCKED-ON-DATA, closed without a prereg — no
    free exchange-listed short-interest history (FINRA free bulk download
    is OTC-only pre-June-2021). Confirmed independently by the 2026-07-12
    full-method survey (family F): only a thin ~4-yr forward-only test is
    free. Probe: `docs/research/2026-07-11_E17_data_probe.md`.)*

**M7 exit conditions — MET 2026-07-11.** Every experiment has a committed
prereg hash, a verdict (PASS-HR / PASS-RA / FAIL / INCONCLUSIVE /
BLOCKED-ON-DATA), and a results doc; findings write-up + README + memory
updated with the arc (record Appendices AX–BC). **Outcome:** E13/E14/E15/E16
all FAIL both tiers; E17 BLOCKED-ON-DATA. Zero PASS-RA survivors from this
arc — the terminal claim upgrades to "the documented, evidenced
strategy-catalog space is exhausted at retail EOD scale," a stronger
portfolio statement than the pre-M7 0/13.

### M7b — Data-type arc: E18–E20 (added 2026-07-12; sourced from
`docs/research/2026-07-12_data_type_exploration.md`)

**Why this exists:** the data-type brief found six free non-OHLCV data types
(all availability probed live 2026-07-12) but they skew to regime gates and
overlays, not return engines. Three carry enough merit to pre-register.
Runs AFTER M7's E13–E17 unless Evan reorders. Same D1 dual-bar verdicts;
same discipline (prereg doc committed before runner, no swing.db writes,
tripwire green after).

33. **E18 — Regime-gate bake-off.** Four a-priori risk-on/off gates on the
    E6 1× equity sleeve, judged head-to-head as drawdown overlays (E6
    criteria: cut maxDD ≥10pp vs buy-hold AND Sharpe ≥ buy-hold): (a) VIX/
    VIX3M term structure < 1; (b) HY OAS (FRED BAMLH0A0HYM2) below its
    trailing median; (c) self-computed breadth (% of 29-ETF universe >200DMA
    > 50%); (d) price >200DMA (the existing E6 gate = the benchmark to beat).
    Data all in hand / probed. Window caveat: VIX3M starts 2006 → gate window
    for the VIX arm is 2006→, disclosed in prereg. This is an OVERLAY test:
    PASS-RA is the only reachable pass (overlays can't clear PASS-HR); if D1
    had been declined this task would be pointless. Done-check: runner +
    tripwire green + results doc. Build: low–medium.
    *(Outcome 2026-07-11: prereg + runner per plan. No gate beat the plain
    200-DMA overlay on the robust both-windows criterion (confirms E6/E7)
    — BUT per D1 the VIX/VIX3M<1 gate cleared **PASS-RA, the program's
    first tier-pass**, flagged WEAK: the 2006–13 window (VIX3M starts 2006)
    has one crash, so the pass largely = dodging 2008, and it has worse
    drawdown than buy-hold in the 2014→ bull. Forward-paper candidate only,
    not a validated edge; PASS-HR stays 0. HY-OAS arm INCONCLUSIVE (FRED
    free data only ~2023+). Results: `docs/research/2026-07-11_E18_results.md`.)*
34. **E19 — Insider opportunistic-buy drift** (Cohen-Malloy-Pomorski 2012).
    STEP 1 = scoped EDGAR probe ONLY: ingest one year of Form 4 filings for
    the 39-stock survivor universe, classify routine vs opportunistic
    (pattern-break heuristic), confirm parseability + coverage. If the probe
    is messy or coverage is poor → record BLOCKED-ON-DATA and close (E10/E17
    pattern). If clean → STEP 2 prereg: long opportunistic-buy names, hold
    ~40 sessions, K per D1 sizing. Survivor + price-side survivorship →
    asymmetric framing (only a FAIL clean). Build: HIGH (heaviest ingestion
    the project has attempted) — do the probe before committing effort.
    *(Outcome — STEP 1 (2026-07-11): probe FEASIBLE-BUT-DEFERRED — Form-4
    parses cleanly (39/39 CIKs) but the full historical build carries three
    hazards (CIK changes needing a former-CIK map, XSL-vs-raw-XML parsing,
    a ~1000-filing API pagination cap); initially deferred vs a
    near-certain-FAIL prior, Evan-gated. Probe:
    `docs/research/2026-07-11_E19_edgar_probe.md`. **STEP 2 authorized
    2026-07-11** — prereg `ebf54a4` committed doc-only (39-name former-CIK
    map resolved: XOM 0000034088, DIS 0001001039; structured-XML floor
    ~2003 → gate window 2003–2013). Full ingestion (104,496 Form-4s, ~7/s)
    launched in background, paused by Evan, **restarted 2026-07-12** (task
    `b2wzwj9gb`, resumable per-ticker cache); backtest runner
    `scripts/run_e19_insider.py` written and ready. **STEP 2 VERDICT
    (2026-07-13): FAIL (clean, robust) — M7b CLOSED.** Ingestion completed
    39/39. Gate 2003–13 CAGR 4.68%/DD 53.6%/Sharpe 0.31; secondary 4.91%/42.6%/
    0.35 — underperforms SPY on CAGR AND Sharpe in BOTH windows; both D1 tiers
    fail; tripwire GREEN. Data heavily transactionCode-"P"-contaminated (BAC =
    44% of P-buys, dominated by BAC's own issuer CIK, incl. $0.01 1-share
    artifacts; CMP classifier passed 95% through — the Appendix-BQ "routine
    absorbs it" prediction FALSIFIED), but a post-hoc de-junk sensitivity
    (price floors + same-owner-day dedup, entries 6119→2675) left the FAIL
    unchanged and flat sub-beta → clean falsification, not a contamination
    artifact. E19 = the program's 8th family (insider/informed-positioning).
    Results: `docs/research/2026-07-13_E19_insider_results.md`; record
    Appendix BR.)*
35. **E20 — Dividend-capture falsification.** Buy each frozen-universe ETF
    at close the session before its ex-date, sell at next open; yfinance
    dividend calendar + our dividend-UNADJUSTED closes (the convention is
    finally correct FOR the measurement). 5 bps/side. Low prior (drop ≈
    dividend). One sitting. Done-check as #33.
    *(Outcome 2026-07-11: prereg `d0642ad`; D1 verdict FAIL both tiers —
    gate CAGR 0.62% (PASS-HR fails). Real but tiny ex-date edge (+0.10%/
    trade mean net, 57.7% win rate) that doesn't compound and goes negative
    post-2014 (secondary −1.15% CAGR, Sharpe −0.39). Results:
    `docs/research/2026-07-11_E20_results.md`.)*

**M7b exit conditions — MET 2026-07-13 (E18/E20 2026-07-11; E19 FAIL 2026-07-13). M7b CLOSED.**
As M7 — every experiment has a committed prereg hash (or a BLOCKED-ON-DATA
record), a D1-tier verdict, and a results doc; findings/README/memory
updated. E18 feeds the M3 overlay directly as a forward-paper candidate (not
yet deployed — still gated on Alpaca account + Evan go). **E19 is the one
still-running experiment in the whole PRD** as of 2026-07-12 — its verdict
closes M7b and, per its asymmetric framing, a FAIL closes the insider-drift
idea cleanly while a PASS routes to forward paper only (survivorship makes
it uninterpretable as a live claim).

### M8 — Full-method-survey candidates: C1–C7 (added 2026-07-12; sourced from
`docs/research/2026-07-12_swing_method_full_survey.md`)

**Why this exists:** after M7/M7b (0 PASS-HR / 1 weak PASS-RA / 20 attempts),
Evan asked for a full in-depth survey of every swing-trading method with
claimed merit. Eight parallel research agents graded ~90 methods across
mean-reversion, trend/momentum, chart-pattern TA, event/catalyst,
seasonality/overnight, sentiment/flow, volatility/options, and factor/ML.
The survey's own reconciliation removed most of the field: the literature's
top "untested" picks (sector momentum, turn-of-month, earnings premium, raw
weekly reversal, dividend capture) are already **E13–E16/E20 FAILs**. What
survives is seven residual candidates — the survey's honest verdict is that
**all seven carry a strong prior of failing the 15% high-return bar**: four
of the seven are overlays that cannot clear PASS-HR at all (only PASS-RA is
reachable, same caveat as E18), one is an intentional kill-shot, and the
structural reason (Hou-Xue-Zhang / McLean-Pontiff / Avramov-Cheng-Metzker:
K=1–3 concentration destroys diversified-decile edges that live in illiquid
names the liquidity floor excludes) argues the remaining engines will also
fail. **Running M8 is lower-expected-value than M7/M7b were** — it exists to
either (a) find the program's second tier-pass or (b) extend the terminal
claim from "the catalog space is exhausted" to "the entire documented
swing-method space is exhausted." Same discipline as M7/M7b: doc-only prereg
commit before each runner, D1 dual-bar verdict, no tuning a FAIL, frozen
tripwire green after, no swing.db writes from live-fetch runners. **Runs
AFTER E19 closes** (M7b's only open item) unless Evan reorders.

Execution order = data-already-in-hand first, new-data-probe-required last
(the E17/E19 pattern: probe before committing build effort).

36. **C1 — Short-term residual reversal** (Blitz-Huij-Lansdorp-Verbeek
    2013). Strip each name's trailing-month return of its Fama-French
    market/size/value factor loading (Ken French library, free), rank on
    the residual, buy the bottom decile/quintile of the 39 survivor
    large-caps at next open, hold ~1 week, 5 bps/side. Direct refinement of
    **E16's** raw-reversal construct (which cleared 15% CAGR but broke the
    60% DD ceiling) — the residual construction is designed to cut the
    factor-driven variance that produced E16's 65.9% drawdown. Disclosed
    counter-evidence: Nagel (2012) — reversal returns are close-anchored
    liquidity provision, so next-open execution likely bleeds the same gap
    that killed the IBS family. Data in hand (`.e8e9_cache` + French
    library). Build: medium (factor-regression step is new).
    *(Outcome 2026-07-14: FAIL — but the program's CLOSEST-EVER HR near-miss
    (attempt 28, record Appendix CB). Gate 19.08%/DD 57.7%/Sh 0.69 — beats
    E16's return AND fixes its DD (both PASS-HR legs clear in the gate, a
    first) — but secondary collapses to 2.92%/0.24 (dead post-2014), and
    survivorship upper-bounds the gate anyway. 15bps kills it. Results
    `docs/research/2026-07-14_C1_residual_reversal_results.md`.)*
37. **C2 — Dividend-initiation drift** (Michaely-Thaler-Womack 1995).
    Long-only: on a stock's first-ever dividend initiation (not resumption),
    buy at next open, hold ~12 months (this stretches "swing" — disclose in
    prereg) or a shorter EOD-truncated window as a sensitivity arm; 5
    bps/side. Distinct from the killed **E20** (which tested dividend
    *capture* around ex-dates on ETFs, not *initiation* drift on stocks).
    Needs a clean "first-ever initiation" flag — probe EDGAR 8-K / dividend
    history for false positives (resumptions, special dividends) before
    pre-registering. Low base rate (thin event flow) is a disclosed risk for
    a K=1–3 book. Build: medium (needs the initiation-flag probe first).
    *(Outcome 2026-07-14: probe found only THREE first-ever in-window
    initiations in 26 years among the 39 survivors (MSFT 2003, ORCL 2009,
    CSCO 2011; AAPL-2012 is a resumption) — n=3 cannot clear any event floor →
    **closed BLOCKED-BY-DESIGN, no prereg/runner** (the E17 pattern). Record
    Appendix CC; probe detail in the C7 results doc.)*
38. **C3 — Consolidated volatility-breakout kill-shot** (Donchian ≈
    Bollinger-squeeze ≈ ATR-channel ≈ Keltner, collapsed into ONE spec to
    avoid multiple-testing snooping). E.g., buy a 20-session closing high
    after a volatility-percentile-below-median squeeze, exit on a 10-session
    low or time stop; 29-ETF universe, 5 bps/side. The only rigorously-
    documented EOD-native chart-pattern construct (Moskowitz-Ooi-Pedersen
    2012 as a *futures* trend factor) — but Sullivan-Timmermann-White (1999)
    and Bajgrowicz-Scaillet (2012) predict it dies on single equities after
    snoop-correction + realistic costs. Pre-register as an honest kill-shot,
    not a hopeful engine. Data in hand. Build: low.
    *(Outcome 2026-07-14: FAIL as predicted (attempt 25, record Appendix CB).
    Gate 3.62%/Sh 0.37 (n=607). Key finding: the time-stop-only arm BEATS the
    channel exit (6.19% vs 3.62%) — the 10d-low exit is a whipsaw tax.
    Breakout family = 3 consistent kills (E8/E11/C3). Results
    `docs/research/2026-07-14_C3_vol_breakout_results.md`.)*
39. **C4 — Vol-targeting sizing overlay** (Moreira-Muir 2017). Scale
    position size inversely to trailing realized volatility on the best
    existing PASS-RA sleeve (E18's VIX-TS gate on E6-1×), A/B'd against the
    unmanaged version. Overlay only — PASS-RA is the only reachable tier;
    cannot improve E6/E18's CAGR, only its Sharpe/DD profile. Disclosed
    counter-evidence: Cederburg-O'Doherty-Wang-Yan (2020) found the effect
    largely fails to survive real-time out-of-sample testing — pre-register
    expecting that. Zero new data (reuses E6/E18 sleeve returns). Build: low.
    *(Outcome 2026-07-14: FAIL on the bar, but a real DD-cutter (attempt 26,
    record Appendix CB). Managed beats base Sharpe both windows on BOTH bases
    (E6 gate DD 53.7→25.1%; E18 sec 43.6→27.0%, Sh 0.82→0.94) yet best gate
    Sharpe 0.77 < 0.80 → FAIL, not tuned. The natural deployment shape if the
    E6/E18 forward-paper candidate ever goes live. Vol-overlay family closed
    (X1+C4). Results `docs/research/2026-07-14_C4_vol_sizing_results.md`.)*
40. **C5 — Free Reg SHO daily short-volume drift** (Boehmer-Jones-Zhang 2008
    lineage). Rank the 39 survivor large-caps by daily executed short volume
    (FINRA/Cboe Reg SHO files, free, 2009+) as a degraded free proxy for the
    paid signed order-flow signal; long low-short-volume / avoid
    high-short-volume, weekly rebalance. Distinct from **E17** (which tested
    bi-monthly short *interest*, BLOCKED-ON-DATA pre-2021) — Reg SHO daily
    volume is a different, unblocked free feed. Probe data availability/
    coverage for the full 2009–2026 window before pre-registering (the
    E17/E19 pattern). Build: medium (new data source, probe first).
    *(2026-07-14: C5 is the SAME signal as M9's X3 — covered there. X3's
    ingester is built (`ingest_regsho_short_volume.py`, parser verified on all
    3 file-format eras, Cloudflare UA fix) and the full 2009–2026 fetch is
    running; prereg+runner follow on INGEST COMPLETE. C5 will not be run
    separately.)*
41. **C6 — Even-week FOMC-cycle overlay** (Cieslak-Morse-Vissing-Jorgensen
    2019). Risk-on/off gate computed purely from the FOMC meeting calendar
    (free) — long the base equity sleeve only in even weeks (0,2,4,6) of the
    cycle since 1994, cash/reduced otherwise. Overlay only, same reachable-
    tier caveat as C4. Distinct from the killed **E13** (turn-of-month is a
    calendar-day rule; this is a meeting-cycle rule) — different mechanism,
    same "overlay not engine" family. Data in hand (need to fetch/cache the
    FOMC meeting-date calendar, free, one-time). Build: low.
    *(Outcome 2026-07-14: FAIL — the cleanest decay exhibit yet (attempt 27,
    record Appendix CB). Calendar compiled from federalreserve.gov primary
    sources → `data/fomc_announcement_dates.json` (260 dates 1994–2026). Gate
    replicates CMVJ exactly (+5.62bps/day even vs −3.15 odd) then INVERTS
    post-2014 (+3.69 vs +6.60) — died at publication. Overlay gate Sh 0.34;
    1585 toggles → 15bps negative. Third decayed-calendar exhibit (E13/E15/C6).
    Results `docs/research/2026-07-14_C6_fomc_cycle_results.md`.)*
42. **C7 — SVXY short-vol carry gated by VIX term structure.** Hold SVXY
    (−0.5× VIX-futures ETF) only when VIX/VIX3M < 1 (contango — reuses E18's
    exact gate signal), flat otherwise; 5 bps/side. The only EOD-equity-proxy
    path into the volatility-risk-premium family without an options feed.
    **Hard drawdown kill-switch mandatory in the prereg** — Volmageddon (Feb
    5 2018) cut short-vol ETPs >90% in one session and terminated XIV
    (Augustin-Cheng-Van den Bergen 2021); this must be modeled honestly, not
    backtested past. Needs new data: SVXY/VXX EOD prices are not yet in
    `.e8e9_cache` — probe coverage/history first. Build: medium (new data +
    the kill-switch mechanic is new engine logic).
    *(Outcome 2026-07-14: FAIL despite the program's highest-ever full-window
    CAGR (attempt 29, record Appendix CC). MAIN 26.45%/DD 55.4%/Sh 0.76 loses
    Sharpe to SPY 0.82 (pre-registered CAGR-AND-Sharpe bar), and the headline
    is an artifact of the dead −1× instrument (era split 47.33%/0.99 pre-2018
    vs 13.18%/0.55 on today's −0.5× SVXY). VIX-TS gate dodged Volmageddon by
    ONE session — effective-N=1, not safety; kill-switch fired once (Brexit).
    VRP family fully surveyed (E18/X1/C4/C7): real regime classifier, no
    engine. Results `docs/research/2026-07-14_C7_svxy_carry_results.md`.)*

**M8 exit conditions:** every candidate that clears its data probe gets a
committed prereg hash, a D1-tier verdict, and a results doc; candidates that
fail their probe are recorded BLOCKED-ON-DATA and closed without a prereg
(C2, C5, C7 all need a probe step first).
**(STATUS 2026-07-14: MET except C5→X3. C1 FAIL, C2 closed-on-probe, C3 FAIL,
C4 FAIL, C6 FAIL, C7 FAIL; C5 is covered by M9's X3, whose data fetch is
running. All seven failed every tier → per the paragraph above, the terminal
claim upgrades to: the entire documented, evidenced swing-method space
surveyed 2026-07-12 is exhausted at retail EOD, K=1–3, $100–1,000 scale —
pending only X3's confirmation.)** Findings write-up + README +
memory updated with the arc. **Feed-forward:** any PASS-RA survivor (C4/C6/
C7's ceiling; C1/C2/C3 could in principle reach PASS-HR) joins E6-1× and any
E18 survivor as an M3 paper-deploy candidate (M3 remains gated on Alpaca
account + Evan go). If all seven fail every tier, the program's terminal
claim upgrades once more: not just the strategy-catalog space but the
**entire documented, evidenced swing-method space surveyed 2026-07-12** is
exhausted at retail EOD, K=1–3, $100–1,000 scale.

### M9 — Research-batch-2 arc: X1–X6 + discipline adoptions (added 2026-07-13;
sourced from `docs/research/2026-07-13_{llm_driven_strategies,
execution_microstructure, risk_and_sizing, data_sources, crypto_feasibility}.md`)

**Why this exists:** the 2026-07-13 research batch produced (a) process upgrades
that should bind every future prereg, (b) five new testable candidates, and
(c) two structural findings that change experiment DESIGN itself:

- **Short-window data breaks the D1 gate protocol.** Several candidates' data
  starts after 2000 (FINRA SI = 2021+, Reg SHO = 2009+, crypto ≈ 2015+ liquid).
  The 2000–2013 hostile-regime gate is unusable there. Rule adopted for M9:
  each prereg fixes a MODIFIED window a priori, discloses the reduced
  confidence, and **caps the best achievable verdict** — a short-window PASS is
  recorded as "PROMISING — needs forward confirmation," never PASS-HR/PASS-RA.
  Only full-window experiments can claim D1 tiers.
- **LLM overlays cannot be backtested honestly, period.** Training-cutoff
  look-ahead (Profit Mirage: 50–72% post-cutoff decay; Levy 2026) means any
  LLM scoring historical dates is partly recalling outcomes. So the LLM
  shortlist (red-team veto, meta-labeler, exit-supervisor, trend-blind
  ablation) is **forward-only** — treatment arms on the M3 live-paper control,
  never M9 backtests. See task 51.

Same discipline as M7/M7b/M8: doc-only prereg before each runner, no tuning a
FAIL, tripwire green after, no swing.db writes from live-fetch runners.
**Ordering:** M9's data-in-hand tasks (43–45) are cheaper than most of M8 and
may interleave with it at the executor's discretion, cheapest-first; 46–47 are
free-data downloads; 48–51 are gated. All run AFTER E19 closes.

43. **Discipline adoptions — prereg-template amendment (one sitting, doc-only).**
    Fold the research-batch process findings into a standing
    `docs/prereg_TEMPLATE.md` that every future prereg copies:
    (a) **tiered cost model** — 1 bp/side broad ETFs, 5 bps/side single
    stocks/sector ETFs, 15–25 bps or exclude below the floor; liquidity floor
    formalized as ADV ≥ $5M AND price ≥ $5; participation cap declared
    non-binding at this AUM; 15 bps/side stress leg reported alongside;
    (b) **execution-vs-signal decomposition ladder** required in every results
    doc — Rung A frictionless close-to-close 0 bps / Rung B next-open 0 bps /
    Rung C next-open + costs (graded rung);
    (c) **time-stop baseline** — every strategy reports a "time-stop-only"
    exit arm as the honest baseline; any price-stop variant must beat it;
    (d) **sizing defaults** — capped fractional-Kelly (λ ≤ ½), fixed-risk
    r = 1–2%/trade, anti-martingale only, no leverage; λ/r frozen per prereg.
    Done-check: template committed; next prereg uses it.
    *(Outcome 2026-07-13: DONE — `docs/prereg_TEMPLATE.md`, record Appendix BT.
    Standing template modeled on the E19 prereg format; all of (a)–(d) folded
    into fixed [STANDING] sections plus the existing standing rules (D1 dual-bar,
    asymmetric framing, prereg-before-code hash, tripwire-GREEN done-check,
    modified-window "PROMISING" cap, LLM-forward-only). Every future prereg
    copies it.)*
44. **EX-DECOMP — decomposition-ladder retrofit (diagnostic, no D1 verdict).**
    Run Rungs A/B/C on the closed FAILs whose runners are in-repo (E13, E14,
    E15, E16, E20; E8/E9 where the runner permits). Output: one table
    classifying each FAIL as SIGNAL-DEAD (fails Rung A), GAP-DWELLER (passes A,
    edge dies A→B), or COST-GATED (passes B, dies at C — candidate for the
    turnover-reduction diagnostic). Expected: most land SIGNAL-DEAD, per the
    execution brief. Done-check: results doc + record entry + tripwire green.
    Build: low (three passes of existing runners).
    *(Outcome 2026-07-13: DONE — `scripts/run_ex_decomp.py`, results
    `docs/research/2026-07-13_EX-DECOMP_results.md`, record Appendix BS. Rung A
    obtained with zero execution-logic edits via an open:=prior-close feed
    wrapper (fill-at-next-open → fill-at-signal-close = c2c); one additive
    `return` hook per runner; regression GREEN (Rung C reproduces E13 1.41%,
    E16 16.76%, E20 +0.10%/trade); frozen tripwire GREEN. **The PRD's "most
    SIGNAL-DEAD" expectation was WRONG — only E14 is signal-dead.** E13 =
    COST-GATED (real calendar edge, turnover-killed); E15 = SURVIVES-NULL gate /
    decays OOS; E16 = SURVIVES-NULL gate but SURVIVORSHIP + fails null 2014→;
    E20 = REAL-BUT-SUBSCALE, gap-loaded overnight edge, negative after cost
    post-2014. Payload: two recurring killers (overnight gap A→B, cost/turnover
    B→C), not one flat null — a stronger terminal statement. E8/E9 not run
    (their runners don't cleanly expose the A/B rung split; the five with
    (open,close) fills covered the diagnostic).)*
45. **X1 — Conditional volatility targeting (E6×E18 interaction).** The one
    regime idea mechanistically distinct from the survivors (FAJ 2020: +0.16
    Sharpe, −7.4 pp maxDD on momentum): de-risk ONLY when vol is elevated AND
    trend is broken, stay invested when vol spikes inside an intact uptrend.
    Three prereg'd arms on SPY: (a) E6 alone, (b) E18 alone (both exist —
    baselines), (c) conditional: exposure 0 iff VIX/VIX3M > 1 AND close <
    200-DMA, else 1. Windows: gate 2006–2013 (VIX3M floor, disclosed — same
    caveat as E18), secondary 2014→. OVERLAY test → PASS-RA is the only
    reachable tier, and per the low-effective-N finding (~3–5 independent
    stress episodes in the whole sample) the prereg must label ANY verdict
    "descriptive — forward paper is the real grade." Data in hand. Build: low.
    *(Outcome 2026-07-13: DONE — FAIL. Prereg `07c22cb`; runner
    `run_x1_vol_targeting.py`; record Appendix BY. Gate 2006–13: (a) E6 200-DMA
    is BEST (6.16%/DD 19.9%/Sharpe 0.58 vs SPY 4.83%/56.5%/0.32); (c) conditional
    5.48%/0.42 TIES (b) VIX-TS and LOSES to (a) → fails PASS-RA (gate Sharpe
    0.42<0.80; must beat both plain overlays, doesn't). Conditioning on vol keeps
    it invested 89% (vs E6 70%) so it barely de-risks. **H1 rejected, null
    survives — confirms E18: no vol gate beats the plain 200-DMA.** Cost-robust.
    Descriptive (low N). Attempt 24; PASS-HR still 0. Results
    `docs/research/2026-07-13_X1_vol_targeting_results.md`.)*
46. **X2 — E17-free: days-to-cover on FINRA official SI (2021–2026).** The
    E17 wall is partly gone: FINRA publishes FREE official exchange-listed
    consolidated short interest biweekly from June 2021 (record Appendix BO).
    Step 1 = data probe (download the biweekly CSVs, verify coverage of a
    liquid universe, confirm publication-date field). Step 2 prereg: DTC =
    SI/ADV; long the lowest-DTC quintile of the liquid universe, rebalance on
    each file's PUBLICATION date (settlement date + ~8 business days —
    using settlement date is look-ahead; disclose). Window: 2021-06→2026 as a
    single OOS window — **modified-window rule applies: best verdict =
    PROMISING, never PASS-HR/RA**; floor ≥ 30 rebalances. Prior: FAIL/weak
    (decayed anomaly, long-only leg is its weak side, liquid universe).
    Build: medium.
    *(Outcome 2026-07-13: DONE — data even better than assumed (FINRA REST API,
    no auth, history to **2017-12-29** not 2021; precomputed DTC; scout record
    Appendix BU). Prereg `prereg_x2_days_to_cover.md` (`4094889`, doc-only,
    first use of the new TEMPLATE); ingester + `scripts/run_x2_days_to_cover.py`;
    205 biweekly dates, 39/39 coverage, entry 10 sessions post-settlement.
    **VERDICT = FAIL (deployable long-only leg):** net 13.32% CAGR / Sharpe 0.60
    beats SPY on CAGR (12.53%) but LOSES Sharpe (0.60<0.71) → fails the
    pre-committed CAGR-AND-Sharpe-vs-both bar. Ladder: A 15.93% → B 16.07% (gap
    flat) → C 13.32% (pure cost); 15bps→8.01%. **PAYLOAD: the short-interest
    anomaly is REAL + correctly signed — long-short spread +18.39%/Sharpe 0.98,
    high-DTC leg −2.63% (underperforms SPY ~15pp/yr) — but the alpha is ENTIRELY
    on the non-deployable SHORT leg (no fractional shorting at this capital),
    exactly as the prereg predicted a priori.** The program's strongest real
    anomaly is one it structurally cannot trade. PASS-HR stays 0; tally 22
    attempts. Results `docs/research/2026-07-13_X2_days_to_cover_results.md`;
    record Appendix BU. **X2b follow-on (Evan "do 1" = pursue short-side; prereg
    `e718f6f`; runner `run_x2b_short_side.py`; record Appendix BW): FAIL — real
    short accounting + borrow sweep (0/2/5/10/20%) + delta-turnover show the
    +18.39% spread was a FRICTIONLESS MIRAGE (LS → 9.24%/Sharpe 0.56 at 5%
    borrow, 5/9 years positive; pure short negative at every borrow level;
    breakeven borrow 13.8% ≫ real large-cap borrow → fails on risk-adjusted
    return + lumpiness, not borrow supply). Short-side lead CLOSED; sizing up a
    shorting account NOT justified. Attempt 23; PASS-HR still 0.)*
47. **X3 — Reg SHO daily short-volume drift (2009+).** Free FINRA/exchange
    daily short-sale-volume files (Boehmer-Jones-Zhang / Diether-Lee-Werner
    lineage). Step 1 = probe (file availability 2009→, decide off-exchange-only
    vs consolidated — disclose whichever). Step 2 prereg: short-volume ratio =
    ShortVolume/TotalVolume; long the lowest-SVR quintile of the liquid
    universe, weekly rebalance, 5 bps/side. Windows: gate 2009–2013 (partial
    overlap with the standard gate — modified-window rule: verdict capped at
    PROMISING), secondary 2014→. Disclosed contamination: market-maker hedging
    shorts inflate SVR (FINRA Information Notice 05/10/19); long-only leg is
    the weaker side of the documented effect. Prior: FAIL/weak. Build: medium.
    *(Step-1 probe DONE 2026-07-13, record Appendix BU: **data access proven** —
    CDN daily files at `cdn.finra.org/equity/regsho/daily/CNMSshvol{YYYYMMDD}.txt`
    (consolidated 2018-08+; per-venue FNYX/FNSQ/FNRA sum for 2009-08+), pipe-
    delimited, trailer line = record count, schema changed 2011-02-28, volumes
    now fractional. **FEASIBLE-DEFERRED, not blocked** — deferred behind X2 (the
    clean short-INTEREST signal ran first); X3 is noisier executed-FLOW and needs
    the heavier per-venue+schema-break daily-file build. Remains an open free
    task.)*
    *(Outcome 2026-07-14: DONE — FAIL (attempt 30, the program's final
    experiment; record Appendix CD). Full ingest 4,260 sessions 2009-08→2026-07,
    39/39 coverage. Long-only lowest-SVR K=5 weekly: gate 13.00%/Sh 0.75 LOSES
    SPY 14.80%/0.91. **Existence spread +1.24%/Sh 0.16 = essentially ZERO signal**
    (low-SVR 14.74% vs high-SVR 12.05%) — executed short volume is MM-hedging
    noise, the clean contrast to X2's real +18.39% short-INTEREST spread. 15bps
    kills it. Informed-positioning family complete. Results
    `docs/research/2026-07-14_X3_regsho_svr_results.md`.)*
48. **X4 — MOC close-entry probe → forward arm (execution experiment).** The
    only fill positioned to capture the ~54% overnight component is a
    market-on-close entry; the backtest upper bound already exists (the c2c
    ablation numbers — E2's c2c would have PASSED). What's genuinely untested
    is IMPLEMENTATION: (step 1, probe) verify CLS/LOC availability on the
    actual Alpaca paper account — the two execution agents disagreed on
    whether CLS is Elite-Smart-Router-gated; if unavailable → record
    BLOCKED-ON-BROKER-TIER and close. (Step 2, forward) if available: a
    forward-paper close-entry arm (signal on a frozen 15:50 snapshot — using
    the 16:00 close for a 15:50 order is look-ahead; measure the 15:50→16:00
    stub as a residual) alongside the next-open control, measuring realized
    overnight capture net of costs. Prior: confirms the kill (NightShares
    failure + NY-Fed flat-since-2021 drift). M3-adjacent: needs the Alpaca
    account → BLOCKED-ON-EVAN.
49. **X5 — Analyst recommendation-change drift (Womack).** Cheapest clean
    event-driven unblock: upgrades/downgrades are EVENT-DATED, so a cheap feed
    avoids the point-in-time consensus trap that gates estimate-revision
    drift. Step 1 = **BLOCKED-ON-EVAN: authorize FMP Starter (~$22, one month,
    then cancel)**. Step 2 = probe FMP grade-history depth (unknown until
    pulled). Step 3 prereg: long-only on upgrades in the liquid universe, buy
    next open, hold ~20 sessions, K=5; windows per actual data depth
    (modified-window rule if < the standard gate). Prior: FAIL (the buy side
    is the documented-weak side; decayed post-Reg-FD). Build: low once data
    is in hand.
50. **X6 — Crypto pilot: BTC/ETH time-series trend (paper-first).**
    **BLOCKED-ON-EVAN: scope expansion to a new asset class.** If authorized:
    universe = BTC + ETH only (majors — kills survivorship + the liquidity
    wall); UTC-00:00 daily bar (no gap by construction); ONE signal fixed a
    priori = 20d/100d MA crossover, long-or-flat (the Grayscale
    survivorship-free spec; Sharpe 1.7 vs 1.3 HODL); **fees pre-registered at
    25 bps/side taker** (Alpaca crypto Tier 1 — 5× the equity model; an edge
    that only clears at 5 bps is a FAIL); data = Kraken free OHLCV archive.
    Windows: gate 2018-01→2022-12 (contains the 2018 AND 2022 bears —
    the honest hostile window), secondary 2023→2026. Verdict: D1 numbers PLUS
    an explicit vs-buy-hold requirement (must beat BTC HODL Sharpe in both
    windows — 15% CAGR alone is trivial in crypto). Disclose the 2022–23
    negative-trend stretch as an expected failure mode, not a tuning target.
    Backtest first (free); Alpaca crypto paper forward only after a
    backtest verdict. The custody tail (uninsured exchange balances) is
    disclosed as the deciding LIVE-money risk — irrelevant to paper. Build:
    medium (new data pipe + fee model).
    *(Outcome 2026-07-14: scope AUTHORIZED via Evan "do 2"; DONE — FAIL
    (attempt 31, first crypto domain; record Appendix CF). Prereg
    `prereg_x6_crypto_trend.md`; runner `run_x6_crypto_trend.py`; data
    yfinance BTC/ETH (not Kraken — free + sufficient for daily trend). Combined
    dual-MA @25bps: gate 2018-22 29.61% CAGR/DD 60.6%/Sh 0.76 CRUSHES HODL
    4.34%/82.3%/0.43, but sec 2023- Sh 0.76 < HODL 1.01 (bull) → fails the
    beat-HODL-Sharpe-BOTH-windows bar. **Cost-robust** (33 toggles/5yr; 25bps
    barely bites — the fee worry was wrong for a slow overlay). **Same lesson as
    equity E6:** MA trend = drawdown control (82%→61% DD), not a return-enhancer
    over HODL in bulls — the structural conclusion generalizes to crypto. 100d
    sensitivity looked better but still < HODL bull; verdict NOT switched (no
    tuning). Paper-first; nothing live; custody stays Evan-gated. Results
    `docs/research/2026-07-14_X6_crypto_trend_results.md`.)*
51. **LLM forward-only arc + M3 protocol amendment (doc task now; execution
    Evan-gated with M3).** Per the LLM brief, the shortlist overlays (B9
    red-team veto — which IS the existing e1_llm_veto design; D3
    triple-barrier meta-labeler; D2 confidence-sizer; D6 exit-supervisor; D15
    trend-blind-vs-trend-aware ablation) are FORWARD-ONLY treatment arms on
    the M3 live-paper control. Amend the M3 spec (tasks 14/18) with the
    non-negotiable gates: pinned model ID + version (an upgrade =
    re-prereg); every verdict logged to an immutable `overlay_log`; the
    frozen tripwire pinned on the DETERMINISTIC REPLAY of that log, never on
    a live model call; ticker anonymization in prompts; the D15 trend-blind
    arm required as the ablation; Tier 0/1 infra (no API key needed — nightly
    runbook). Also fold in the RK4 forward-paper reframe: the M3 success
    criterion for the E6∩E18 sleeve is **implementation fidelity vs a shadow
    backtest over a pre-committed 6–12-month window** (MinTRL is unreachable
    for slow signals — claiming statistical edge from the window would break
    our own rigor rules). Done-check: M3 section amended by appending; record
    entry.

**M9 exit conditions:** tasks 43–44 completed (they upgrade every later
experiment); each X-candidate either has a committed prereg hash + verdict +
results doc, or a BLOCKED-ON-{EVAN, BROKER-TIER, DATA} record; findings/
README/memory updated. **Feed-forward:** any full-window PASS-RA joins the M3
candidate list; short-window "PROMISING" results queue for forward paper only.
If the arc closes with no new tier-pass, the terminal claim extends to the
2026-07-13 research batch: execution, risk, data, and crypto paths were
surveyed, designed, and honestly closed.

### M10 — Evidence-synthesis arc: state-conditioned strategies (added 2026-07-14;
Evan's direction "come up with different strategies … meet both criteria"; record
Appendices CG–CK) — **DONE 2026-07-14**

**Why this exists:** after 31 attempts (0 clean PASS-HR), Evan asked whether the
*accumulated evidence* — not a new single signal — could be composed into a strategy that
clears BOTH D1 tiers. This is explicitly a synthesis over prior results, so it carries a
**data-snooping cap unique to M10: any pass is IN-SAMPLE-COMPOSED → "forward paper
REQUIRED," never clean or live.** A multi-agent design panel (5 designer lenses ×
adversarial judges, record Appendix CH) produced the load-bearing negative: a **fixed-weight
blend of the surviving sleeves cannot clear PASS-HR** — the 2000–13 gate needs C1-reversal
weight ≥ 0.66 while the 2014→ secondary needs ≤ 0.29, a contradiction. **The only escape is
state-conditioning on a causal variable** (regime-switch the weights), which motivated M10-1.
Same discipline as M7–M9 (doc-only prereg before runner, no tuning a FAIL, tripwire GREEN
after, no swing.db writes).

52. **M10-1 — Nagel Switch (VIX-regime state-switch).** VIX>20 → C1 residual reversal
    (bottom-K survivors); VIX≤20 → E6 QQQ 200-DMA trend. Mechanism = Nagel (2012):
    short-term-reversal alpha is liquidity-provision compensation that scales with VIX, so
    the switch is causal, not fit. Full VIX window (1990+), D1 dual-bar, next-open, 1 bp.
    *(Outcome 2026-07-14: **PASS-HR — the program's FIRST — but IN-SAMPLE-COMPOSED /
    forward-paper-only** (attempt 32, record Appendix CI). Gate 17.87% CAGR / DD 59.95% /
    Sh 0.66; sec 15.94% / 39.68% / 0.78 — both windows clear ≥15% CAGR & ≤60% DD. **NOT a
    win by the program's own discipline:** composed after 31 results; survivor-flattered
    (reversal buys known survivors in crashes — C1's in-window passes were declared
    UNINTERPRETABLE); gate DD clears by 0.05 pp; breaks at VIX>18 (14.83% FAIL) and at
    15 bps; fails PASS-RA (Sh 0.66 < 0.80). Per the M10 cap → "PROMISING / forward paper
    REQUIRED." Fixed a carry-forward mark-to-market bug (bisect_right-1, past-only, no
    look-ahead) that had shown a spurious −100% NAV on the final secondary bar; gate was
    already clean. Prereg `docs/prereg_m10_1_nagel_switch.md`; runner
    `scripts/run_m10_1_nagel_switch.py`; results
    `docs/research/2026-07-14_M10-1_nagel_switch_results.md`.)*
53. **M10-2 — Gap-amortized stress IBS (the E2 c2c-mirage kill-shot).** 2× QQQ
    mean-reversion entered on VIX>20 & IBS≤0.20, held 5 sessions (to amortize the lost
    first-night gap that killed the IBS family), trend fallback when VIX≤20. Attacks the
    open question left by E2: *was there real alpha behind the overnight gap next-open
    can't reach?*
    *(Outcome 2026-07-14: **FAIL** (attempt 33, record Appendix CK). Gate 2.99% CAGR /
    **83.3% DD** / Sh 0.28; sec 28.95% / 1.08 (one-window bull artifact). **Payload in the
    FAIL:** the 5-day hold neutralized the gap (c2c 3.18% ≈ next-open 2.99%), isolating the
    reversion's gap-free economics — catastrophic in the gate. This **permanently closes the
    E2 c2c 18.15% "mirage":** the gap was hiding the *drawdown* (2× long into 2000–02/2008
    cascades), not alpha. Sharpens M10-1: unlevered cross-sectional reversal passes HR, 2×
    index MR is an 83%-DD engine → M10-1's pass is a cross-sectional-*survivor* effect, not
    a general stress-reversion edge. Prereg `docs/prereg_m10_2_gap_amortized_ibs.md`; runner
    `scripts/run_m10_2_gap_amortized_ibs.py`; results
    `docs/research/2026-07-14_M10-2_gap_amortized_ibs_results.md`.)*

**M10 exit conditions — MET 2026-07-14.** Both panel survivors have a committed prereg
hash, a verdict, and a results doc; capstone/HANDOFF/record/memory updated. The arc's
lasting outputs: (1) the fixed-weight-impossibility proof, (2) the first (in-sample)
PASS-HR as a forward-paper hypothesis, (3) the E2 mirage closed. **M10 does NOT close the
program** — see M11.

### M11 — Algorithmic chart-pattern detection (added 2026-07-14; Evan's direction; record
Appendix CL) — **CURRENT OPEN DIRECTION, UNSTARTED**

**Why this exists (Evan, 2026-07-14):** "Many traders teach others by showing the graphs
and certain patterns that suggest the market is about to go up or down, then buy when those
patterns arise — algorithmic detection, NOT LLM-driven." This is the **one classical
mechanism family the program has never tested.** Every prior attempt trades a *number*
(IBS, residual rank, MA-cross, short-interest ratio); none trades *shape* — the
head-and-shoulders, double top/bottom, triangle, wedge, cup-and-handle, and flag/breakout
patterns of visual technical analysis. It fits every project constraint: EOD-native (daily
bars, signal at close → next open), K=1–3 (scan the survivor universe, take top-K by a
pre-registered pattern-strength score), and — because it is **price-only, no data wall —
full-window D1-reachable** (it can claim a true tier, unlike every post-2000 experiment).

**Honest prior = FAIL (stated before any run):**
- **Lo, Mamaysky & Wang (2000, *J. Finance*)** — the one rigorous algorithmic detector
  (kernel-smoothing + local extrema, 10 classic patterns, US equities 1962–96) — found
  patterns carry *modest incremental statistical information* (conditional ≠ unconditional
  return distribution) but **explicitly did not show cost-surviving profitability.**
  "Informative ≠ tradeable."
- **Sullivan-Timmermann-White (1999)** and **Bajgrowicz-Scaillet (2012)**: technical-rule
  profits largely vanish under data-snooping / FDR correction + realistic costs, OOS.
- **McLean-Pontiff decay:** a pattern taught publicly for decades is a published,
  arb-eligible signal by definition.
- **Program-internal, mechanistic prediction:** continuation patterns (flags, triangles,
  breakouts) ARE breakouts → inherit the breakout family's three kills (E8/E11/C3; C3
  showed the channel exit is a whipsaw tax). Reversal patterns (double bottoms, inverse
  H&S) are cousins of the reversal near-miss that cleared then decayed (E16/C1). And
  next-open execution bleeds the same overnight gap the program keeps losing.
- **Out of scope for this task (different ask):** CNN chart-*image* classifiers (Jiang-
  Kelly-Xiu 2023) find image predictivity but are ML-driven, cross-sectional over thousands
  of names, not rule-based K=1–3 — Evan specified rule-based, not LLM/ML.

**Expected verdict: FAIL, extending the terminal claim to "even the chart *shapes* don't
trade at retail EOD," with a small chance of a forward-paper "PROMISING."** Either outcome
is a legitimate program result — a FAIL adds the chart-pattern family (a genuine 9th equity
family) to the exhausted set; a PROMISING queues for M3 forward paper. Running it is
**lower-expected-value than M7/M8 were, and that is the point of doing it: it closes the
last obvious gap in "trying everything."**

Discipline unchanged (prereg-before-code hash, D1 dual-bar, asymmetric survivor framing,
tripwire GREEN after, no swing.db writes, tiered costs per `docs/prereg_TEMPLATE.md`).

54. **M11.1 — sourced brief. DONE 2026-07-14.**
    *(Outcome: `docs/research/2026-07-14_chart_pattern_detection_brief.md`. Evidence is
    MIXED, not a clean FAIL — patterns carry modest statistical info (Lo-Mamaysky-Wang 2000)
    and head-and-shoulders has real predictive power (Savin-Weller-Zvingelis 2007) — BUT that
    H&S edge is ~5–7%/yr risk-adjusted **underperformance** (a SHORT signal) that is "not
    profitable as a standalone strategy in rising markets" and works "only in hedged
    portfolios" → the same no-fractional-shorting wall that made X2/X2b uncapturable; and
    Sullivan-Timmermann-White 1999 / Bajgrowicz-Scaillet 2012 show data-snooping + even low
    transaction costs erase technical-rule profits (Bajgrowicz-Scaillet: offset in-sample).
    **Two design corrections fed to M11.2:** (1) the DEPLOYABLE lead is the LONG-side reversal
    (**inverse-H&S / double-BOTTOM**), NOT H&S/double-TOP — that is the short/uncapturable
    side, report it as an X2-style measurement only; (2) LMW's kernel smoother is
    **NON-CAUSAL (look-ahead)** → the deployable detector must be causal, or confirm patterns
    only AFTER the neckline/confirmation break.)*
55. **M11.2 — prereg (doc-only, committed BEFORE the runner).** The discipline-critical
    task: chart patterns are parameter-rich (lookback, extremum prominence, neckline
    tolerance, breakout confirmation %), so the prereg must PIN every parameter a priori by
    **adopting LMW's published detector definitions** (externally anchored, not fit), and
    commit to **ONE consolidated pattern spec, or a small pre-declared set with an explicit
    multiple-testing / snoop adjustment** (the C3 kill-shot model — collapse the variants to
    avoid data-mining). Fix: detection rules; entry (pattern completion, next open) + exit
    (time-stop baseline per TEMPLATE, any price-stop must beat it); K sizing; full-window
    gate 2000–2013 + secondary 2014→; survivor-universe asymmetric framing (only a FAIL is
    clean); tiered costs + the 15 bps stress leg; the D1 dual-bar verdict labels; and the
    a-priori FAIL-lean disclosure above. **Recommended lead (per the M11.1 brief):** a
    **causal** LMW-style detector on the **LONG-side reversal** spec (**inverse-head-and-
    shoulders + double-BOTTOM**) as the deployable arm, WITH the bearish H&S / double-top
    reported as a short-only (uncapturable) measurement — the reversal-side analogue of C3's
    breakout kill-shot. **Look-ahead guard:** causal smoother, or confirm only AFTER the
    neckline break (LMW's two-sided kernel is non-causal). Brief:
    `docs/research/2026-07-14_chart_pattern_detection_brief.md`.
56. **M11.3 — build + run.** Detector (kernel-smooth / rolling local-extrema geometry) +
    a runner reusing the survivor universe, coverage gate, and D1 stats. Run per prereg;
    state the verdict PLAINLY, **no tuning a FAIL.**
57. **M11.4 — record.** Results doc + record entry + tripwire GREEN; capstone §3 ledger +
    §8 frontier + HANDOFF + memory updated with the outcome. If FAIL → the terminal claim
    upgrades to include the chart-pattern family; if PROMISING → joins the M3 forward-paper
    candidate list (still Evan-gated).

**M11 status: UNSTARTED.** Evan *suggested* this direction (2026-07-14); per one-task-per-
sitting it is queued as the next experiment on his go. It is the program's designated
default idle experiment — the one remaining free, autonomously-runnable mechanism.

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
  support market/limit/stop/stop-limit but TIF=DAY only + no fractional
  shorting (record Appendix BO); paper fills are simulated at the quoted
  half-spread with NO price improvement, NO slippage, and NO size check vs
  depth — so paper will NOT surface the liquidity-floor problem; caveat every
  slippage claim and cap fill size at the floor in the backtest.
- The power calc (task 6) must never compute post-signal returns — that's
  peeking before pre-registration.
- A FAILED experiment honestly recorded is a deliverable, not a setback —
  do not tune past a pre-registered kill.
- `.bat` pure ASCII; JSON via Python/Node only; venv python is
  `.venv\Scripts\python.exe`.
