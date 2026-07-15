# Project Record — Full Chronological History

Written 2026-07-08. Every entry is grounded in one of:
- Evan's project brief of 2026-07-08 (the session that created this project),
  including his infrastructure inventory of `D:\ClaudeCode\Trading` and his
  candidate strategy list
- File-system state of `D:\ClaudeCode\Swing Trading` at bootstrap time
- Evan's global CLAUDE.md standards

Sections where a timestamp can't be precisely verified are explicitly
marked. No fabricated metrics, dates, or file names.

---

# How this document is organized

This record has two parts plus this navigation front-matter:

- **Part I — Phases** (`##` headings): the original consolidation, written in
  one pass from real history at bootstrap time.
- **Part II — Appendices A–…** (`#` headings): chronological addenda appended
  one session at a time per the `CLAUDE.md` cadence rule. **Append-only** —
  prior appendices are never edited.

The two heading levels encode that distinction (Phases are sections of the
original record; Appendices are top-level addenda). Sub-sections use the
`Letter.Number` convention (e.g. `B.7`, `Q.2`).

The sections below are reading aids. The authoritative detail always lives in
the dated entry, not the digest.

---

# Table of Contents

**Part I — Original record (2026-07-08)**
- [Phase 0 — Inception and doc-system bootstrap](#phase-0--inception-and-doc-system-bootstrap-2026-07-08) (~07-08)

**Part II — Appendices (chronological)**
- [A — Strategy research brief; PDT rule found eliminated](#appendix-a---strategy-research-brief-pdt-rule-found-eliminated-2026-07-08) (07-08)
- [B — 30 experiment ideas; council verdict selects the program](#appendix-b---30-experiment-ideas-council-verdict-selects-the-program-2026-07-08) (07-08)
- [C — PRD written; Evan keeps LLM overlays as gated shadow mode](#appendix-c---prd-written-evan-keeps-llm-overlays-as-gated-shadow-mode-2026-07-08) (07-08)
- [D — Overlay amended shadow→live-acting: control + veto sleeves from M3 day one](#appendix-d---overlay-amended-shadowlive-acting-control--veto-sleeves-from-m3-day-one-2026-07-08) (07-08)
- [E — M0.1 executed: skeleton, venv, git init (first commit)](#appendix-e---m01-executed-skeleton-venv-git-init-first-commit-2026-07-08) (07-08)
- [F — M0.2: price_cache lacks OHLC → own fetcher (swing_bot/prices.py)](#appendix-f---m02-price_cache-lacks-ohlc--own-fetcher-swing_botpricespy-2026-07-08) (07-08)
- [G — M0.3: frozen 29-ETF universe + full backfill](#appendix-g---m03-frozen-29-etf-universe--full-backfill-2026-07-08) (07-08)
- [H — M0.4: coverage+quality gate; found XLRE zero-range bars](#appendix-h---m04-coveragequality-gate-found-xlre-zero-range-bars-2026-07-08) (07-08)
- [I — M0.5: frozen-regression harness; M0 complete](#appendix-i---m05-frozen-regression-harness-m0-complete-2026-07-09) (07-09)
- [J — Design Q&A: return prior + high-risk (leveraged-ETF) direction](#appendix-j---design-qa-return-prior--high-risk-leveraged-etf-direction-2026-07-09) (07-09)
- [K — M1.6: power calc; E1 is powerable (19.6% signal rate)](#appendix-k---m16-power-calc-e1-is-powerable-196-signal-rate-2026-07-09) (07-09)
- [L — M1.7: E1 PRE-REGISTRATION committed (8963e49) before any engine](#appendix-l---m17-e1-pre-registration-committed-8963e49-before-any-engine-2026-07-09) (07-09)
- [M — M1.8: fill-timing ablation; M1 complete](#appendix-m---m18-fill-timing-ablation-m1-complete-2026-07-09) (07-09)
- [N — M2.9: backtest engine (hand-checked P&L exact)](#appendix-n---m29-backtest-engine-hand-checked-pl-exact-2026-07-09) (07-09)
- [O — M2.10: E1 backtest VERDICT = FAIL (honest, no tuning)](#appendix-o---m210-e1-backtest-verdict--fail-honest-no-tuning-2026-07-09) (07-09)
- [P — M2.11: real E1 frozen refs pinned; STOP at M2.13 gate](#appendix-p---m211-real-e1-frozen-refs-pinned-stop-at-m213-gate-2026-07-09) (07-09)
- [Q — E1b: broad_us OOS test = FAIL (near-miss, Sharpe 0.496)](#appendix-q---e1b-broad_us-oos-test--fail-near-miss-sharpe-0496-2026-07-09) (07-09)
- [R — GOAL REDEFINED by Evan: high-return concentrated swing, risk accepted](#appendix-r---goal-redefined-by-evan-high-return-concentrated-swing-risk-accepted-2026-07-09) (07-09)
- [S — M2b.1: frozen LEVERAGED universe (5 ETFs) + backfill](#appendix-s---m2b1-frozen-leveraged-universe-5-etfs--backfill-2026-07-09) (07-09)
- [T — M2b.2-3: E2 prereg (865c09e) + run = FAIL; IBS family SHELVED](#appendix-t---m2b2-3-e2-prereg-865c09e--run--fail-ibs-family-shelved-2026-07-09) (07-09)
- [U — M2b.4: E2 refs pinned; M2b complete; STOP at gate](#appendix-u---m2b4-e2-refs-pinned-m2b-complete-stop-at-gate-2026-07-09) (07-09)
- [V — Experiment catalog v2 (data-grounded, 20 items) + %/mo verdicts](#appendix-v---experiment-catalog-v2-data-grounded-20-items--mo-verdicts-2026-07-09) (07-09)
- [W — Evan overrides IBS stop for A3; C1+screens sitting begins](#appendix-w---evan-overrides-ibs-stop-for-a3-c1screens-sitting-begins-2026-07-09) (07-09)
- [X — C1: engine v2 (NAV-proportional, cash-capped) verified](#appendix-x---c1-engine-v2-nav-proportional-cash-capped-verified-2026-07-09) (07-09)
- [Y — Screens: A3 dead, B1 dead, B4 rotation +2.15%/mo holdout standout](#appendix-y---screens-a3-dead-b1-dead-b4-rotation-215mo-holdout-standout-2026-07-09) (07-09)
- [Z — Findings write-up (E1→B4 arc) produced; session close](#appendix-z---findings-write-up-e1b4-arc-produced-session-close-2026-07-09) (07-09)
- [AA — E4 leverage rotation: pre-reg (313d88a), engine, VERDICT = PASS; STOP at live gate](#appendix-aa---e4-leverage-rotation-pre-reg-313d88a-engine-verdict--pass-stop-at-live-gate-2026-07-09) (07-09)
- [AB — E5 regime test: E4 loses 93% in 2000-2013; VERDICT = FAIL; E4 de-authorized for paper](#appendix-ab---e5-regime-test-e4-loses-93-in-2000-2013-verdict--fail-e4-de-authorized-for-paper-2026-07-09) (07-09)
- [AC — E6 de-leveraged rotation VERDICT = PASS (robust drawdown overlay, not high-return)](#appendix-ac---e6-de-leveraged-rotation-verdict--pass-robust-drawdown-overlay-not-high-return-2026-07-09) (07-09)
- [AD — Full E1→E6 program write-up (option 1); program complete](#appendix-ad---full-e1e6-program-write-up-option-1-program-complete-2026-07-09) (07-09)
- [AE — Pressure-test: buy-hold-TQQQ claim retracted; clean test data exhausted](#appendix-ae---pressure-test-buy-hold-tqqq-claim-retracted-clean-test-data-exhausted-2026-07-10) (07-10)
- [AF — E7 international validation: BOTH arms FAIL; high-return-robust question CLOSED](#appendix-af---e7-international-validation-both-arms-fail-high-return-robust-question-closed-2026-07-10) (07-10)
- [AG — Write-up updated to E7 + M6 packaging; at the deploy wall](#appendix-ag---write-up-updated-to-e7--m6-packaging-readme-tag-at-the-deploy-wall-2026-07-10) (07-10)
- [AH — Evan opens E3 (stock momentum); survivorship-bias design problem](#appendix-ah---evan-opens-e3-stock-momentum-survivorship-bias-design-problem-2026-07-10) (07-10)
- [AI — E3 stock momentum FAIL (clean); all three families now falsified](#appendix-ai---e3-stock-momentum-fail-clean-all-three-families-now-falsified-2026-07-10) (07-10)

---

## Phase 0 — Inception and doc-system bootstrap (2026-07-08)

**WHAT:** Project created. Evan's brief: build a bot that swing trades —
positions held a few days to a few weeks — workable with a small amount of
money ($100–1,000), as a separate project from the long-term momentum bot in
`D:\ClaudeCode\Trading`, reusing that repo's infrastructure where it fits.
He explicitly required the memory/doc system NOT live in the original Trading
folder. This session bootstrapped the `/project-memory` system in
`D:\ClaudeCode\Swing Trading`: `HANDOFF.md`, this record, project `CLAUDE.md`
with cadence wiring, `.claude/codebase-memory/` bins, and auto-memory files.
`.claude/pm-cadence.json` was auto-created by the skill hook with defaults
(record entry every 3 prompts; handoff/PRD/bins event-driven) — kept, since
they match Evan's global standard.

**Directory state at bootstrap:** empty except `.claude/` (the auto-created
cadence config). No code, no git repo, no PRD.

### Candidate strategies (Evan's brief, 2026-07-08, condensed faithfully)

1. **Trend pullback** — stock in strong uptrend with 20-day EMA above 50-day
   EMA; wait for a 1–3 day pullback to support (20 EMA or prior swing low);
   buy on signs of a bounce (reversal candlestick); stop just below the
   pullback low.
2. **Bull-flag breakout** — sharp upward move (pole) then sideways drift in a
   parallel channel/small wedge (flag); enter on break above the flag's upper
   resistance; stop below the flag's support.
3. **Mean reversion** — RSI below 30 or price below the third Bollinger
   deviation band; look for a capitulation day on massive volume followed by
   a strong reversal day; enter long as panic subsides; tight stops
   (falling-knife risk).
4. **Sector rotation** — for choppy/directionless markets: track leading
   sector ETFs, buy leading stocks in outperforming sectors breaking out of
   clean bases or reclaiming key MAs; scale out into the breakout, trail
   stops to breakeven.

### Infrastructure inventory Evan supplied (map of `D:\ClaudeCode\Trading`)

Condensed; that repo's own `HANDOFF.md` and `.claude/codebase-memory/` are
ground truth — verify before assuming behavior.

| Area | Key pieces | Portability note |
|---|---|---|
| Data pipeline | `daily_price_refresh.py` (~5,200 tickers), `price_cache` SQLite (SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED, caches close/next_open/ATR/MA flags), `factors/universe.py` quality filters | Directly reusable; MIN_DOLLAR_VOL=0 is a known gap, mandatory to fix at small capital |
| Backtest | `execution/factor_backtest.py` harness; frozen-regression-test pattern (`strategies/test_strategies.py`, own `__main__`, fails >5bps drift) | Reuse the HARNESS + test pattern, not the long-horizon factor logic |
| Paper engine | `paper_trader.py` (paper_portfolio/positions/nav/transactions), `paper_rebalance.py`, `paper_mtm.py` | Schema tolerates any cadence; monthly buy-top-N rebalance logic will NOT transfer |
| Alpaca PAPER | `alpaca_client.py` (httpx, live hard-guarded), `alpaca_accounts.py` (~3 paper accts/login), `alpaca_sync.py` (CASH_BUFFER=0.01), `fractionability.py` | Most directly reusable piece; whole-share fallback becomes load-bearing at $100–1,000 |
| LLM overlay | candidate/decide/rebalance CLIs, 3-arm experiment design (control / cash-veto / cascade), kill-switch discipline | Pattern portable if an overlay experiment is wanted later |
| Dashboard | Streamlit `dashboard/web.py` (port 8501) | Extend or clone later |
| Automation | Windows Task Scheduler + Claude Code scheduled tasks; pure-ASCII `.bat` requirement | Pattern portable |
| Known data traps | yfinance split-misapplication (>1000% one-day move tell), incomplete same-day publication (gate on coverage count), Friday-spike corruption, cache-gap phantom-ranking | All apply to any yfinance-based swing pipeline |

Dominant known limitation carried over: **survivorship bias** — yfinance only
has currently-listed names, so all backtests are upper-bound-biased.

### Decisions taken this session

- Doc/memory system lives in `D:\ClaudeCode\Swing Trading` (decided by Evan
  2026-07-08 — explicitly not in the Trading folder).
- Cadence defaults kept (record 3 / rest event-driven), matching Evan's
  global standard.

### Open decisions (not taken — BLOCKED-ON-EVAN)

- Capital range discrepancy: brief prose says $100–1,000; the pasted
  inventory header says $100–10,000. Assumed $100–1,000 (live instruction
  wins) pending confirmation.
- Strategy selection (which of the four first), data-layer approach
  (read-only reuse of Trading's price_cache vs. separate stack), Alpaca
  paper-account allocation.

**HONEST OPEN ITEM (not fixed):** no PRD_ROADMAP.md yet — deliberately
deferred until Evan makes the scope calls above. No git repo initialized;
Evan hasn't asked for one.

---

# Appendix A - Strategy research brief; PDT rule found eliminated (2026-07-08)

**WHAT:** Evan chose option 2 (research before PRD). Produced
`docs/research/2026-07-08_small-account-swing-strategies.md` via
/research-brief — ~12 web searches, cross-checked load-bearing claims.

**Ranked outcome:** (1) IBS/RSI-family mean reversion on liquid index/sector
ETFs — build first (best replicated EOD evidence: Pagonidis 2013 + arXiv 2023
+ independent practitioner replications; ETFs also sidestep survivorship
bias); (2) trend-filtered pullback on mega-caps — Evan's "trend pullback" and
"mean reversion" candidates collapse into this one codified family
(200-day-MA gate + short-term oversold trigger); (3) PEAD swing variant —
parked, needs earnings data and evidence has decayed in large caps; (4)
sector rotation — skipped as duplicating Trading's horizon/factors; (5) bull
flag — rejected, no credible codified evidence (Lo-Mamaysky-Wang established
informativeness at best, not profitability).

**Material regulatory find (verified, 3+ independent sources):** FINRA's PDT
rule was ELIMINATED effective 2026-06-04 (SEC approved 2026-04-14; FINRA
Reg Notice 26-10). Alpaca implemented the new intraday-margin framework
2026-06-04 and removes the PDT fields (`pattern_day_trader`,
`daytrade_count`, etc.) from its API by 2026-07-06 — any code ported from
Trading that reads those fields will break. Same-day stop-outs are no longer
a regulatory trap for sub-$25k margin accounts.

**Other load-bearing finds:** short-term reversal survives transaction costs
only in large caps (de Groot/Huij/Zhou 2012) — never run mean reversion on
the broad 5,200-ticker universe; Alpaca fractional orders are DAY-TIF only
(no GTC stops on fractional positions — exits must be re-armed daily or
managed in software); published mean-reversion effects are measured
close-to-close, so next-open execution forfeits the overnight component —
the backtest must model whichever execution timing the PRD picks.

**HONEST OPEN ITEM (not fixed):** all practitioner CAGRs in the brief are
single-source hypotheses until reproduced on our own price_cache; PRD still
unwritten pending Evan's sign-off on the ranking.

---

# Appendix B - 30 experiment ideas; council verdict selects the program (2026-07-08)

**WHAT:** Brainstormed 30 experiment ideas across 5 blocks (strategy edges /
execution / sizing / LLM overlays / methodology), saved to
`docs/research/2026-07-08_experiment_ideas.md`, then ran /llm-council
(5 advisors → anonymized peer review → chairman) to select the program.

**VERDICT (chairman synthesis, full text in session chat 2026-07-08):**
- Wave 0, infra not experiments: #29 frozen-regression tripwire, #30
  data-coverage gate, #28 fill-divergence logging (armed from day one).
- Wave 1, backtest: pre-register kill criteria for #1 (ETF IBS mean
  reversion) FIRST; then #15+#13 fill-timing ablation (close-to-close vs
  next-open) using the already-cached next_open series; then #1 under the
  validated fill assumption, with #27 survivorship bound as a side-check.
- Wave 2, live paper, gated on #1 passing pre-registered thresholds: #1
  live with residual-slippage A/B embedded (#15), #28 logging.
- Deferred: #17, #18, #20, #2/#4, #11, #5. Dropped (16 ideas): #3, #6, #7,
  #8, #9, #10, #12, #14, #16, #19-standalone, #21, #22, #23, #24, #25, #26.
- LLM overlays rejected for now on statistical power: MR entries cluster in
  panics → single-digit veto events per quarter → unpowerable.

**Blind spots caught only by peer review (not by any single advisor):**
(a) #15 is answerable as a one-day backtest since price_cache stores
historical next_open — no live months needed for the first-order answer;
(b) nobody had pre-registered what "#1 survives" means — kill criteria must
be dated and committed before backtest code runs, else the rigor story is
p-hacking with better documentation; (c) Alpaca PAPER fills are simulated
(filled at quote, no queue/impact/partials) — #15-live and #28 measure
simulator behavior and must carry that caveat; (d) statistical power
(IBS<0.2 signals/year on the ETF universe) is unquantified and gates
everything.

**Peer-review meta:** 4 of 5 reviewers ranked the Contrarian's response
strongest; the Expansionist's (novelty-first, LLM overlay #25 promoted) was
unanimously flagged as the biggest blind spot — scope creep vs falsifiability.

**HONEST OPEN ITEM (not fixed):** PRD_ROADMAP.md still unwritten — the
council verdict + research brief now supply its content, pending Evan's
approval. The power calculation (signals/year) and the pre-registration doc
are the first two concrete artifacts the PRD should demand.

---

# Appendix C - PRD written; Evan keeps LLM overlays as gated shadow mode (2026-07-08)

**WHAT:** `PRD_ROADMAP.md` written to the council program (Appendix B) with
one scope change from Evan: **LLM overlays KEPT** (his live instruction,
2026-07-08, overriding the council's unanimous power-based drop). His first
phrasing in the same prompt was "no llm overlay", immediately self-corrected
to "keep llm overlays" — the correction governs. **HOW the keep is squared
with the power problem:** overlays enter as SHADOW MODE from live day one
(every entry candidate gets a logged LLM verdict that never touches orders;
runtime assertion enforces zero order effect), and promotion to the real
3-arm control/veto/cascade experiment (M4) is gated on a shadow-log N fixed
in the M1 pre-registration doc. This was Claude's proposed compromise,
flagged to Evan at delivery — he can override to act-live sooner.

**PRD shape:** M0 foundations (git/venv/data-access verify/ETF universe/
coverage gate/tripwire harness) → M1 pre-registration & fill-timing ablation
(ordering-critical: prereg doc commit must predate any engine code) → M2 E1
IBS backtest vs pre-registered gates + frozen-ref pinning + survivorship
bound → M3 live paper (GATED on M2 PASS + Evan) with divergence logging and
the overlay shadow log → M4 overlay promotion (GATED on N) → M5 deferred
expansion. Per-task commits authorized by the PRD; push never. Scope guard:
Trading repo/DB read-only, paper only, no dropped-idea resurrection.
`HANDOFF.md` synced (workstream table now maps to PRD milestones; next open
task M0.1).

**Cadence note:** pm-cadence hook fired on this prompt (#3); this entry
satisfies it — no miss.

**HONEST OPEN ITEM (not fixed):** capital range still unconfirmed
($100–1,000 assumed); Alpaca paper-account allocation still BLOCKED-ON-EVAN
(PRD M3.15); no code exists yet — M0.1 is the next action.

---

# Appendix D - Overlay amended shadow→live-acting: control + veto sleeves from M3 day one (2026-07-08, ~23:15)

**WHAT:** Evan chose to amend the PRD (his option "2") rather than start
M0.1 — the flagged amendment being overlay timing. `PRD_ROADMAP.md` updated
(decided by Evan 2026-07-08): the LLM overlay is LIVE-ACTING from M3 day
one, not shadow-mode. **HOW rigor is preserved:** Trading's
control-vs-treatment pattern at daily cadence — two DB paper sleeves,
`e1_control` (pure mechanical E1, orders computed and finalized BEFORE any
overlay call, runtime assertion) and `e1_llm_veto` (cash-veto treatment).
Cascade arm deferred to the M4 readout. M4 repurposed from
"promote-shadow-to-3-arm" to "readout at pre-registered N/time horizon:
continue / add cascade / kill". The overlay experiment's own
pre-registration (arms, readout N/horizon, kill criteria) folded into M1
task 7. Alpaca mirror (M3.16) mirrors `e1_control`; the treatment sleeve is
DB-only unless a second paper account frees up. All interim overlay numbers
labeled descriptive-only until the readout — the council's power objection
now binds the CLAIMS, not the running.

**WHY this shape:** Evan wants the overlay trading, not just logging; acting
without a control would make the overlay unfalsifiable, and paper sleeves
are free — so the treatment runs against a concurrent control instead of
alone. Cost acknowledged: LLM decisions needed on every signal day
(interactive runbook until unattended mode is unblocked).

**Docs synced:** PRD §1/§3/M1.7/M3.14/M3.16/M3.18/M3.20/M4.21 + milestone
table + rationale; HANDOFF decisions + workstream table; auto-memory file.

**HONEST OPEN ITEM (not fixed):** unchanged from Appendix C — capital
unconfirmed, Alpaca account BLOCKED-ON-EVAN, no code yet; next action M0.1.

---

# Appendix E - M0.1 executed: skeleton, venv, git init (first commit) (2026-07-08, ~23:15)

**WHAT:** Ran PRD task M0.1. Created `swing_bot/` package
(`__init__.py` with the split-adjusted/dividend-UNadjusted convention note),
`scripts/` (`.gitkeep`), `.gitignore` (`.venv/`, `swing.db*`, `*_keys.env`,
`*.env`, pycache), `requirements.txt` (yfinance, httpx; pytest optional).
Created `.venv` and installed deps. `git init` (identity already configured:
Evan-Daruwalla), staged all bootstrap docs + skeleton, verified `.venv/` is
git-ignored, committed.

**Commit:** `4ac785c` "M0.1: project skeleton, venv, git init". Working tree
clean after.

**Done-check (both pass):**
- `git -C . log --oneline` → shows `4ac785c`.
- `.venv\Scripts\python.exe -c "import yfinance, httpx"` → `import OK 1.5.1
  0.28.1`, exit 0.

**Environment captured:** Python 3.14.4 (system + venv), git 2.53.0.
Resolved dep versions are NEW majors — pandas 3.0.3, numpy 2.5.1,
yfinance 1.5.1, httpx 0.28.1, curl_cffi 0.15.0. requirements.txt is
intentionally UNPINNED at bootstrap; will pin once E1 backtest is stable.

**HONEST OPEN ITEM (flagged, not blocking):** Python 3.14 + pandas 3.0 are
both bleeding-edge majors (pandas 3.0 defaults copy-on-write and drops some
legacy APIs). yfinance imported clean, but a 3.14/pandas-3.0 edge could
surface during M0.2 (price_cache reads) or M2 (backtest vectorization) — if
so, the fix is pinning to a known-good set, not code contortions. Noted so a
future session recognizes the symptom fast.

**Cadence:** pm-cadence fired at prompt #6; this entry satisfies it (Appendix
C covered #3). No miss.

**Next action:** M0.2 — verify ETF price coverage in Trading's `price_cache`
(read-only) and choose the data path.

---

# Appendix F - M0.2: price_cache lacks OHLC → own fetcher (swing_bot/prices.py) (2026-07-08, ~23:35)

**WHAT:** Ran PRD task M0.2 (verify ETF coverage in Trading's `price_cache`,
read-only; choose the data path). Outcome: **reuse is not viable; own
yfinance fetcher chosen.** Wrote `swing_bot/prices.py` (own OHLCV store in
`swing.db`) and validated it end-to-end.

**Tooling note:** the Grep/Glob tools return "no files found" against
`D:\ClaudeCode\Trading` (an additional working dir) even though PowerShell
confirms 6,961 `.py` files and the full `trading_bot/` package are present.
All Trading-DB access this session went through venv Python scripts +
PowerShell instead. Trading's `var/trades.db` is the DB; `price_cache` is
real and matches the inventory: cols `(ticker, kind, key_date, price)`,
37.4M rows, 12,486 tickers.

**DECISIVE FINDING — why reuse fails for THIS project:**
1. `price_cache` stores only `close`, `volume`, and derived flags
   (`kind`s: next_open, close, next_open_vol, next_open_range, above_ma_50,
   atr_pct_20, above_ma_200, split_ratio, splits_json, dividends_json,
   dividends_total, volume). **There is NO high/low/open series.** IBS =
   (close − low)/(high − low) — the #1 strategy — is therefore UNCOMPUTABLE
   from it.
2. `next_open` has ZERO rows for every ETF checked (even SPY) — so the
   executable-fill model / M1 fill-timing ablation couldn't source it here.
3. Universe gaps: DIA, IWM, and ALL country/international ETFs (EWJ, EWZ,
   EWG, EWU, EWA, EWC, EWH, EWW, EWT, EWY, INDA, FXI, EEM, EFA) are absent.

### Coverage snapshot (read-only probe, 2026-07-08)

| Group | Tickers with `close` | Span | `next_open` |
|---|---|---|---|
| Broad | SPY, QQQ (3,043 rows, 2014-06→2026-07) | ~12yr | 0 for all |
| Broad missing | DIA, IWM | — | — |
| SPDR sectors | XLE/XLF/XLK/XLV/XLI/XLY/XLP/XLU/XLB (3,043); XLRE (2,701, from 2015-10); XLC (2,023, from 2018-06) | 8–12yr | 0 for all |
| Country/intl | none present | — | — |

**DECISION (decided 2026-07-08):** own yfinance fetcher, `auto_adjust=False`
(split-adjusted, dividend-UNadjusted, matching Trading's convention), full
OHLCV into `swing.db` table `bars` (PK ticker,date; cols
open/high/low/close/adj_close/volume). This also removes cross-project data
coupling and lets M0.3 freeze a universe that includes DIA/IWM + country
ETFs.

**VALIDATION (real output):**
- yfinance smoke test: `SPY` OHLCV fetched, columns Open/High/Low/Close/
  Adj Close/Volume present, network OK.
- `prices.backfill` SPY + QQQ → 3,146 rows each, 2014-01-02..2026-07-08
  (more complete than Trading's 3,043). `swing.db` created (gitignored).
- IBS computes from a stored bar: SPY 2026-07-08 H=746.15 L=739.51 C=745.40
  → IBS=0.887. The thing price_cache could not do, the own store does.

**Downstream implications:** M0.3 universe can include DIA/IWM/country ETFs;
M0.4 coverage gate runs on `swing.db` bars; M1.8 ablation sources next-day
open as the following row's `open` (present in our OHLCV). Full-universe
backfill deferred to after M0.3 (universe not yet frozen — one task per
sitting).

**HONEST OPEN ITEM (not fixed):** `prices.py` is minimal — no split-
misapplication sanity check (Trading's >1000%-one-day-move tell) or
incomplete-publication gate yet; those belong to M0.4 (coverage/quality
gate) and M0.3 (universe filters). yfinance rate-limiting on a full-universe
backfill is untested at scale.

**Cadence:** not a cadence-fire prompt; entry written as part of the task's
done sequence.

**Next action:** M0.3 — freeze the ETF universe (`swing_bot/universe.py`)
with per-ticker inclusion reason + listing date.

---

# Appendix G - M0.3: frozen 29-ETF universe + full backfill (2026-07-08, ~23:50)

**WHAT:** Ran PRD task M0.3. Wrote `swing_bot/universe.py` freezing a
29-ticker ETF universe and `scripts/backfill_universe.py`; backfilled all 29
into `swing.db` (89,666 rows).

**Universe (frozen 2026-07-08; change = new dated decision):**
- broad_us (4): SPY, QQQ, DIA, IWM
- spdr_sector (11): XLE XLF XLK XLV XLI XLY XLP XLU XLB XLRE XLC
- country_intl (14): EWJ EWZ EWG EWU EWA EWC EWH EWW EWT EWY INDA FXI EEM EFA

Each entry carries name, group, `data_start`, and a one-line reason.
`data_start` = the ticker's FIRST yfinance bar (auto_adjust=False), fetched
empirically 2026-07-08 — NOT invented. First-bar dates span 1993 (SPY) to
2018 (XLC); recorded exactly as returned.

**WHY this composition:** IBS is best-evidenced on liquid equity-index ETFs
(Pagonidis) and liquid country ETFs (arXiv 2306.12434); a broader-but-liquid
basket also raises independent-signal count, the binding statistical-power
constraint for this small-capital program (research brief 2026-07-08).
Liquidity is a non-issue at $100–1,000 — the least-liquid member (EWG) had
~$47M/day median dollar volume at the probe, orders of magnitude above any
order here. `MIN_MEDIAN_DOLLAR_VOL = 20M` defined as a forward guard;
enforcement is M0.4's job, not the universe file's.

**VALIDATION (real output):**
- Structure check: 29 tickers, all have reason + ISO `data_start`, no
  duplicates; group counts 4/11/14.
- Backfill: 27 of 29 have full 3,146 rows (2014-01-02..2026-07-08); XLRE
  2,701 (from 2015-10-08) and XLC 2,023 (from 2018-06-19) shorter, matching
  their real launch dates. Total 89,666 rows in `swing.db`.

**KNOWN PROPERTY (not a defect, flag for E1 interpretation):** IBS on
US-listed single-country ETFs (EWJ, EWG, …) has a different mechanism than
on US-index ETFs — the home market is closed during US hours, so the US
close reflects stale NAV plus US-hours repricing. This is part of WHY country
-ETF mean reversion exists (arXiv paper), but it means the `country_intl`
group's IBS behavior may not be homogeneous with `broad_us`/`spdr_sector`.
E1 results should be reported per-group, not just pooled.

**HONEST OPEN ITEM (not fixed):** no data-quality sanity checks run on the
89,666 rows yet (split-misapplication tell, gaps) — that is M0.4. Backfill
default history start is 2014-01-01; deeper history exists for most (SPY to
1993) if a longer window is wanted later.

**Next action:** M0.4 — data-coverage/quality gate
(`swing_bot/coverage_gate.py`): refuse to emit signals unless the full
universe has a bar for the as-of date; fold in a basic split-misapplication
sanity check.

---

# Appendix H - M0.4: coverage+quality gate; found XLRE zero-range bars (2026-07-08, ~00:05 07-09 local)

**WHAT:** Ran PRD task M0.4. Wrote `swing_bot/coverage_gate.py` with two
checks and a nonzero-exit `__main__`.

1. **Coverage** (`coverage(conn, as_of)`): every ticker LISTED as of that
   date (`data_start <= as_of`) must have a bar; a not-yet-listed ticker is
   not counted missing (handles XLC pre-2018, XLRE pre-2015). Carries over
   Trading's "gate on coverage count, not on 'ran today'" lesson.
   `latest_common_date()` walks back to the newest fully-covered date for
   the live loop's as-of.
2. **Sanity** (`sanity_scan`): flags OHLC-ordering violations, zero-range
   bars (IBS undefined), and |daily ret| > 35% (the split-misapplication
   tell; our no-leverage ETF universe never legitimately moves that much).

**DONE-CHECK (real output, both pass):**
- `python -m swing_bot.coverage_gate` on real `swing.db`: `coverage as-of
  2026-07-08: OK`, exit 0.
- Truncated fixture (drop XLK's latest bar) → `coverage_ok=False
  missing=['XLK']` — gate correctly fails/exits nonzero.

**REAL DATA-QUALITY FINDING (not invented):** the sanity scan flagged 19
anomalies, ALL `zero_range` (High==Low) in **XLRE 2015-10-13 .. 2016-02-25**
— its first ~5 months after the 2015-10-08 launch. Cause: illiquid early
trading (flat/'single-print' days), NOT a mis-applied split. Consequence:
IBS = (close-low)/(high-low) DIVIDES BY ZERO on those bars. The other 28
tickers were fully clean (no OHLC-order violations, no extreme returns, no
zero-range).

**DECISION:** coverage gate stays GREEN on zero-range days (coverage is
about bar presence, not usability); handling is the E1 signal layer's job.
Logged as a hard M2 requirement + in the gotchas bin: **E1 must skip any
ticker on a day where high==low (IBS undefined → no signal), never crash.**

**HONEST OPEN ITEM (not fixed):** sanity_scan is O(all bars) each call —
fine at 90k rows, would need incremental scoping if the universe/history
grows a lot. The 35% return threshold is a heuristic, not tuned. Neither is
blocking.

**Cadence:** pm-cadence fired at prompt #9; this entry satisfies it (last
was Appendix E at #6). No miss.

**Next action:** M0.5 — frozen-regression harness
(`swing_bot/test_frozen.py`, own `__main__`, ±0.0000pp comparison,
placeholder fixtures until real refs are pinned in M2).

---

# Appendix I - M0.5: frozen-regression harness; M0 complete (2026-07-09, ~00:20 local)

**WHAT:** Ran PRD task M0.5, completing milestone M0 (Foundations). Wrote
`swing_bot/test_frozen.py` (frozen-regression tripwire, Trading's pattern:
reference table, exact-drift comparison, loud failure, own `__main__` exit
code) plus `swing_bot/signals.py` (the `ibs()` primitive).

**Judgment call (flagged to Evan):** added `signals.ibs(high, low, close)`
now rather than in M2, so the frozen harness pins a REAL deterministic
function instead of a self-referential toy. Kept strictly to the primitive
(zero-range/inverted guard → returns None; the M0.4 gotcha baked in at the
primitive level). No thresholds/entry/exit — E1 strategy logic remains M2.

**DONE-CHECK (real output):**
- `python -m swing_bot.test_frozen` → all cases PASS, "FROZEN TESTS: GREEN
  (all d=0)", exit 0.
- Teeth test (not committed): injected a 0.0001 drift → harness prints
  "FAIL <<<" / "RED - DRIFT DETECTED", returns exit 1. The tripwire is not
  vacuously green.

**Placeholder fixtures:** 3 numeric IBS cases on synthetic bars (0.5/0.75/
0.1, exact) + 2 invariants (zero-range→None, inverted→None). Per M2 task 11
these get REPLACED by real E1 backtest refs (tpnl% unit 'pp' dp 4,
closed_count unit '' dp 0) on two pinned windows. Harness is generic
(`Case(name,value,ref,unit,dp)`), so M2 just extends `REFERENCES`.

**Minor:** the RED banner originally used an em-dash that rendered as
mojibake under the Windows console codepage — switched to ASCII hyphen
(project ASCII-safety posture).

### Point-in-time snapshot — M0 (Foundations) COMPLETE (2026-07-09)

| Task | Deliverable | Status |
|---|---|---|
| M0.1 | skeleton, venv, git (`4ac785c`), pinned deps (`3ba9cc1`) | Done |
| M0.2 | own OHLCV fetcher `swing_bot/prices.py` → `swing.db` (`11d2116`) | Done |
| M0.3 | frozen 29-ETF `swing_bot/universe.py` + backfill 89,666 rows (`54f3876`) | Done |
| M0.4 | coverage/quality gate `swing_bot/coverage_gate.py` (`731ff43`) | Done |
| M0.5 | frozen harness `swing_bot/test_frozen.py` + `signals.py` | Done (this entry) |

Code modules: prices, universe, coverage_gate, signals, test_frozen.
Data: `swing.db` 89,666 OHLCV rows, 29 ETFs, clean except XLRE's 19
early zero-range bars (guarded).

**HONEST OPEN ITEM (not fixed):** frozen refs are placeholders (real ones
need E1, M2). `signals.py` has only `ibs()`; the E1 entry/exit rules and the
zero-range SKIP behavior at the strategy level are still M2.

**Next action: M1 — Pre-registration & ablation.** First task M1.6 (power
calc: IBS<0.20 signals/year per ticker, NO post-signal return peeking),
which gates the pre-registration doc M1.7 (must be committed before any
backtest-engine code — the project's core rigor claim).

---

# Appendix J - Design Q&A: return prior + high-risk (leveraged-ETF) direction (2026-07-09, ~00:35 local)

No code this turn — two design questions from Evan, recorded for scope
context (cadence prompt #12).

**Q1 "what do returns look like now (estimate)?"** Declined to compute a
return on our data: doing so would run the E1 backtest before the M1.7
pre-registration commit, breaking Success Criterion #1 (git proves prereg
predates engine code) — the core rigor claim. Gave the LITERATURE PRIOR only
(not our data): Pagonidis IBS next-day +0.35% after IBS<0.2 vs -0.13% after
IBS>0.8; de Groot reversal 30-50 bps/week net (large caps only); RSI2 SPY
~9%/yr invested ~28% of time (single-source). Honest executable band after
haircuts (next-open forfeits overnight component; spread; crowding/decay):
"roughly flat after costs" to "low-double-digit %/yr" — wide because the
load-bearing unknowns are exactly what M1.8/M2 measure.

**Q2 "high-risk strategies that could earn more?"** Recommendation
(discussion, NOT yet a committed scope change): the cleanest higher-variance
extension is running the SAME IBS mean-reversion signal on a LEVERAGED-ETF
universe (TQQQ/UPRO/SOXL/TNA/...) as a SEPARATE pre-registered arm ("E2"),
after E1's machinery is proven — same code, same harness, A/B-able vs E1,
studied edge (leveraged ETFs overshoot intraday and revert). Honest risk
flags: leverage/volatility decay in chop, 3x drawdowns amplified by MR's
falling-knife tendency, overnight gap risk amplified under next-open fills.
Rejected/deprioritized higher-risk options: concentration (variance knob,
no new edge), high-vol single stocks/small caps (reintroduces survivorship
bias + blow-up risk, weaker MR edge), options (new data + theta + spreads,
scope explosion), crypto (thin MR evidence, scope explosion). Meta-point
stated to Evan: at $100-1,000 the dollar delta between 10% and 30%/yr is
~$50 vs ~$150 — and higher variance makes results LESS statistically
distinguishable at n~20-40 trades, which HURTS the portfolio artifact whose
value is a clean controlled experiment.

**DECISION STATUS:** no scope change committed. Leveraged-ETF "E2" is a
candidate for the M5 expansion list / a future parallel experiment, each
with its own pre-registration; M1 order is unchanged. Awaiting Evan's call.

---

# Appendix K - M1.6: power calc; E1 is powerable (19.6% signal rate) (2026-07-09, ~00:50 local)

**WHAT:** Ran PRD task M1.6 (power calc, NO return peeking). Wrote
`docs/research/2026-07-09_E1_power.md`. Evan authorized running the full PRD
chain this session, checking work + recording after each step, stopping at
the M2.13 BLOCKED-ON-EVAN gate.

**RESULT (signal counts only, from `swing.db`; no returns computed):**
IBS<0.20 fires on 19.6% of valid bar-days (17,572 / 89,647). ~44-59
signals/yr per ticker, strikingly uniform across broad/sector/country groups
(the ~20% threshold mostly sets the count; the untested EDGE is what would
differ). Universe ~1,431 signal-days/yr; 73% of trading days carry >=1
signal; mean 7.6 simultaneous signals on a signal-day. E1 is therefore
signal-ABUNDANT and CAPACITY-constrained (position slots, not signal supply,
bound trade count).

**Capacity/time-to-N (assumed hold H, real hold pinned in M1.7):** K=5,H=3 →
~420 trades/yr → N=100 in ~2.9mo, N=200 in ~5.7mo, N=384 in ~11mo. Backtest
(M2) gets thousands of trades over 12.5yr → not noise-limited.

**VERDICT:** E1 is powerable — overwhelmingly for the backtest, and live
paper reaches a meaningful N=100-200 in 3-6 months. Answers the council's
"powerable before college apps?" concern. Implication logged for M1.7: a
min-N kill criterion of 100-200 closed trades is reasonable AND reachable;
the overlay/veto arm accrues N far slower and needs its own longer readout.

**Integrity:** counts derived from IBS only; zero forward returns touched —
pre-registration not contaminated.

**Next action:** M1.7 — write + commit `docs/prereg_E1_ibs.md` (exact rules,
kill criteria incl. min-N, both fill models, overlay pre-reg). MUST be
committed BEFORE any backtest-engine code (Success Criterion #1).

---

# Appendix L - M1.7: E1 PRE-REGISTRATION committed (8963e49) before any engine (2026-07-09, ~01:05 local)

**WHAT:** Wrote and committed `docs/prereg_E1_ibs.md` — the project's core
rigor artifact. **Commit `8963e49` contains ONLY the prereg doc (1 file, 132
lines); verified no backtest-engine code exists in the repo at that hash**
(swing_bot modules present: prices, universe, coverage_gate, signals,
test_frozen — none an engine). Success Criterion #1 (git proves prereg
predates engine code) is now permanently satisfied.

**FIXED PARAMETERS (immutable after this commit):**
- Entry: IBS<0.20 at close, long-only, on the frozen 29-ETF universe (skip
  high==low). Exit: first close with IBS>0.80, OR 5-trading-day time stop.
  No hard stop-loss in E1 (stop ablation is separate, M5).
- Sizing: $500 nominal, K=5 concurrent, 20% each, lowest-IBS-first selection,
  ties alphabetical. Fractional in backtest.
- Fill models: PRIMARY next-open (executable, judged for kill criteria);
  REFERENCE close-to-close (Pagonidis basis, for the haircut). Cost: PRIMARY
  10bps round-trip; 0/20bps as sensitivity.
- **KILL CRITERIA (E1 PASSES only if ALL, on next-open net of 10bps):**
  >=200 closed trades; net mean return/trade > 0; net annualized Sharpe
  >=0.50; max drawdown <= 25%. Any miss = FAIL = stop + record, no tuning.
- Reported-not-gated: Model B + A-B haircut, per-group split (country ETFs
  separate), 2014-2021 vs 2022-2026 split-sample.
- Overlay veto arm pre-registered: control vs cash-veto, readout at 100
  decisions or 6 months, kill if veto doesn't predict worse outcomes or
  treatment NAV <= control NAV.

**WHY the single-commit discipline:** isolating the doc in its own commit
makes the ordering proof unambiguous — anyone can `git show 8963e49` and see
rules-only, no results, no engine. That is what makes a later "E1 passed"
claim credible rather than potentially p-hacked.

**Next action:** M1.8 — fill-timing ablation (`scripts/ablation_fill_timing
.py`): close-to-close vs next-open vs overnight-only component on IBS<0.20
signals. Returns ARE now permitted (rules are locked). Names which fill model
M2 treats as primary (pre-reg already says next-open).

---

# Appendix M - M1.8: fill-timing ablation; M1 complete (2026-07-09, ~01:25 local)

**WHAT:** Ran PRD task M1.8 (fill-timing ablation), completing milestone M1.
Wrote `scripts/ablation_fill_timing.py` + `docs/research/2026-07-09_E1_fill_
timing_ablation.md`. First return computation of the project — run strictly
AFTER the M1.7 pre-reg commit `8963e49`.

**RESULT (per-signal 1-day-forward, gross, pooled 17,558 signals, bps):**
c2c +11.8 / overnight +6.3 / intraday +5.4 / **next-open (executable) +7.5**.
- **Overnight = 54% of the close-to-close edge** — the council's concern
  was real: over half the idealized IBS effect sits in the post-signal gap.
- **Next-open execution keeps ~64%** (haircut 4.3 bps). The executable edge
  is positive pooled; it does not vanish.
- **Per-group split (nopen1d):** broad_us +11.2, spdr_sector +8.0,
  country_intl +6.1. Many single-country ETFs are weak/negative executable
  (EWA -0.9, EWC -0.5, EWH ~0, EWU +0.1) — IBS edge there is an overnight/
  stale-NAV artifact a next-open loop can't harvest. Strongest executable:
  XLK +25.9, QQQ +21.6, EWY +19.4, XLC +18.9.

**HONEST RISK FLAG carried to M2:** +7.5 bps gross/signal (1-day) is THIN vs
the pre-registered 10 bps round-trip cost — a 1-day-hold view is net
negative. E1's survival depends on the multi-day hold (exit IBS>0.80 or 5
days) capturing materially more reversion than one day. The 1-day ablation
is a LOWER BOUND on per-trade gross, not the strategy return. This lowers the
prior on E1 passing; M2 decides. NO rule changes — universe/params frozen;
the per-group concentration hint would be a FUTURE pre-registration, not an
edit to E1.

### Point-in-time snapshot — M1 (Pre-registration & ablation) COMPLETE

| Task | Deliverable | Commit |
|---|---|---|
| M1.6 | power calc (E1 powerable, 19.6% signal rate) | `2a9edde` |
| M1.7 | E1 pre-registration (doc-only, before engine) | `8963e49` (+rec `0062ec9`) |
| M1.8 | fill-timing ablation (next-open keeps ~64%) | this entry |

**Next action: M2 — E1 backtest.** M2.9: build `swing_bot/backtest.py`
(minimal daily engine, ~200 lines, implements the frozen pre-reg EXACTLY:
IBS<0.20 entry / IBS>0.80-or-5day exit, K=5 20%-each, next-open primary,
10bps). This is the FIRST engine code — it legitimately comes after
`8963e49`. Then M2.10 runs it vs the kill criteria.

---

# Appendix N - M2.9: backtest engine (hand-checked P&L exact) (2026-07-09, ~01:45 local)

**WHAT:** Built `swing_bot/backtest.py` — the minimal daily E1 engine (~200
lines, purpose-built, NOT adapted from Trading's monthly factor_backtest).
Implements the frozen pre-reg (`8963e49`) exactly: IBS<0.20 entry / IBS>0.80-
or-5-day exit, K=5 concurrent at capital/5 each, lowest-IBS-first selection
(ties alphabetical), next-open (primary) or c2c fills, cost_bps per side.
`metrics()` computes the kill-criteria stats (n_trades, mean net return/trade,
annualized Sharpe from daily NAV, max drawdown, CAGR). FIRST engine code in
the repo — commit order after `8963e49` preserved.

**DONE-CHECK (toy series, hand-computed, real output):** single-ticker toy
with a d0 entry signal (IBS=0) and d1 exit signal (IBS=0.875). Engine
reproduced hand math EXACTLY: net_ret 0.0526315789 (= 10.0/9.5-1, enter
open d1, exit open d2), NAV end 505.2631578947, hold_days 1; and the 5bps-
cost case 0.0515794734 (= 10*0.9995/(9.5*1.0005)-1). All asserts < 1e-12.

**Note:** removed a speculative `hasattr(e,'tk')` line before testing
(dead defensive code; simplicity).

**Next action:** M2.10 — run E1 on the full `swing.db` window per the
pre-registration, both fill models + cost sensitivities + per-group + split-
sample, and state PASS/FAIL vs the four kill criteria PLAINLY. No tuning on
a FAIL.

---

# Appendix O - M2.10: E1 backtest VERDICT = FAIL (honest, no tuning) (2026-07-09, ~02:10 local)

**WHAT:** Ran E1 per the frozen pre-registration (`8963e49`) via
`scripts/run_e1_backtest.py`. Full results in
`docs/research/2026-07-09_E1_backtest_results.md`.

**VERDICT: E1 FAILS** (2 of 4 kill criteria). Primary (next-open, 10bps
round-trip, full 29-ETF universe):
- n=3559 (PASS, >=200) · exp +4.7bps/trade (PASS, >0) · **Sharpe 0.23
  (FAIL, need >=0.50)** · **maxDD 36.0% (FAIL, need <=25%)**.

**WHY (diagnostic, NOT tuning):**
- Cost-fragile: 0bps Sharpe 0.56 / +14.7bps; 10bps/side NEGATIVE. The M1.8
  ablation warning was correct — multi-day hold lifted gross to +14.7bps but
  not enough to clear cost + the Sharpe/DD bars.
- country_intl net NEGATIVE (-2.2bps, Sharpe 0.05, 57.5% maxDD) — overnight/
  stale-NAV edge forfeited by next-open; the main drag.
- Recent-era decay: 2014-2021 Sharpe 0.32 -> 2022-2026 Sharpe 0.01 (neg
  expectancy). Public-signal crowding, realized.

**INTEGRITY — the load-bearing moment:** broad_us alone passes all four
(n=1478, Sharpe 0.60, maxDD 14.2%, +23.1bps). This is NOT a pass. The
pre-registered experiment was the full universe and it FAILED; selecting
broad_us post hoc is exactly the universe-narrowing pre-reg §10 forbids.
"broad_us IBS" is a NEW hypothesis requiring its OWN dated pre-registration
(E1b) with a real holdout — a lead, not a result. No tuning applied; the
FAIL stands as the honest outcome. This is the process working as designed:
the scaffolding prevented a p-hacked "win."

**DISPOSITION:** E1 did NOT pass the M2->M3 gate. No live trading. Per PRD
M2.13, stop and await Evan's direction. M2.11 (pin frozen refs) still runs —
it makes this FAIL tamper-evident and tripwires the engine for any E1b.

**Next action:** M2.11 — pin real E1 backtest refs into
`swing_bot/test_frozen.py` (two short windows, exact tpnl%/closed_count),
replacing the M0.5 placeholders. Then STOP at the M2.13 gate and report.

---

# Appendix P - M2.11: real E1 frozen refs pinned; STOP at M2.13 gate (2026-07-09, ~02:30 local)

**WHAT:** M2.11 — replaced the M0.5 placeholder frozen refs in
`swing_bot/test_frozen.py` with REAL E1 engine outputs on two fixed windows
(full universe, next-open, 5bps): W1 2019-H1 tpnl 8.815909% / 134 closed;
W2 2020-H1 tpnl 6.209800% / 162 closed. Kept the `ibs()` invariant guards.

**DONE-CHECK:** `python -m swing_bot.test_frozen` → GREEN, all four E1 cases
d=+0.0000pp (Evan's exact standard), invariants PASS, exit 0. The engine and
the FAILED result are now tamper-evident: any unrelated code change that
alters E1's output trips the tripwire. (Known property documented in the
test: a RED after a swing.db re-backfill with unchanged code = upstream
yfinance data drift, not a code bug.)

**STOP — M2.13 GATE (BLOCKED-ON-EVAN).** E1 FAILED (Appendix O), so per the
pre-reg and PRD M2.13 the M2->M3 live gate does NOT open: no live paper, no
Alpaca account work. Execution of the autonomous PRD run halts here and
awaits Evan's direction.

**M2.12 (survivorship bound) DEFERRED — reported, not silently skipped:** it
compares always-listed mega-cap STOCKS vs the ETF universe to bound
survivorship bias. E1 is ETF-only (our 29 ETFs are all still-listed →
survivorship-immune for this test) and E1 already FAILED, so running a stock
basket now is low-value busywork on a dead strategy and would require
fetching names outside the frozen universe. Recommend running it only if/when
a stock strategy enters scope. Evan's call.

### Point-in-time snapshot — M2 status (2026-07-09)

| Task | Status |
|---|---|
| M2.9 engine (`415c527`) | Done, hand-checked |
| M2.10 run vs kill criteria (`d28f899`) | Done — **E1 FAIL** |
| M2.11 pin frozen refs | Done — green d=0.0000pp |
| M2.12 survivorship bound | Deferred (moot for failed ETF-only E1) |
| M2.13 M2->M3 gate | **STOP — E1 did not pass; awaiting Evan** |

**DECISION FOR EVAN (candidate next directions):**
1. Pre-register **E1b** on broad_us (± sectors) with a real out-of-sample
   holdout — the data's strongest lead, but 2022-2026 decay is a warning.
2. Pre-register a **lower-cost / different-signal** variant (the edge is
   real gross but cost-fragile — e.g. fewer, higher-conviction entries).
3. Pre-register the **leveraged-ETF E2** idea (Appendix J) — higher variance,
   same cost-fragility risk.
4. Shelve mean reversion; move to a deferred idea / different strategy family.
No option proceeds without a NEW dated pre-registration — E1's FAIL does not
authorize live trading or a post-hoc universe rebrand.

**Next action:** NONE autonomous — Evan chooses a direction. The doc system,
data layer, engine, and tripwire (M0-M2 infra) are all reusable for whatever
comes next.

---

# Appendix Q - E1b: broad_us OOS test = FAIL (near-miss, Sharpe 0.496) (2026-07-09, ~03:00 local)

**WHAT:** Evan chose direction 1. Pre-registered E1b (`0126ce3`, doc-only,
before the runner) then ran `scripts/run_e1b_backtest.py`. Full results in
`docs/research/2026-07-09_E1b_broad_us_results.md`.

**VERDICT: E1b FAILS** the pre-registered gate — but as a NEAR-MISS, and a
categorically more encouraging result than E1. broad_us HOLDOUT (2022-01-01..
2026-07-08, next-open, 5bps/side):
- n=560 (PASS) · exp +17.77bps (PASS) · **Sharpe 0.49613 (FAIL vs 0.50)** ·
  maxDD 9.77% (PASS). 3 of 4 pass, 2 decisively. FAILS by 0.0039 of Sharpe.
- **NOT rounded up** — the >=0.50 bar was strict and committed pre-run.

**KEY FINDING — prior was wrong in broad_us's favor:** I expected OOS decay
to ~0 (full universe was Sharpe 0.01 in this window). Instead broad_us held
Sharpe 0.66 (train) -> 0.496 (holdout) through the 2022 bear (maxDD only
9.8%). The IBS edge substantially PERSISTED out-of-sample in the 4 broad US
index ETFs — real but decayed, and just under the tradeability bar.

**Cost is the swing factor:** 0bps Sharpe 0.76 / 5bps-side 0.496 / 10bps-side
0.23. The pre-reg's 5bps/side is CONSERVATIVE for SPY/QQQ/DIA/IWM (~1bp real
spreads). Secondary broad_us+sectors HOLDOUT is net-negative (Sharpe -0.05) —
sectors confirmed dead weight.

**INTEGRITY / multiplicity note:** two pre-registered tests now run (E1 fail,
E1b near-miss). A third (lower-cost E1c) is defensible ONLY on independent
liquidity grounds (real spreads ~1bp) AND with a PRE-COMMITTED STOP (if E1c
fails, shelve ETF IBS). Otherwise it is fishing-by-multiplicity. Recorded so
the temptation is visible, not acted on silently.

**DISPOSITION:** E1b did not pass; no live trading. Awaiting Evan:
(a) pre-register E1c at liquidity-justified ~2bps/side WITH a committed stop
(one final swing); (b) accept broad_us IBS as a real-but-sub-bar effect,
write it up, pivot to a new family; (c) leveraged E2 / other. No option goes
live without passing + Evan go + Alpaca account.

**Next action:** NONE autonomous — Evan chooses.

---

# Appendix R - GOAL REDEFINED by Evan: high-return concentrated swing, risk accepted (2026-07-09, ~14:25 local)

**WHAT (decided by Evan 2026-07-09, verbatim intent):** the project goal is
a swing trader that, as accurately as possible, invests in **a stock or a
few stocks** with a small amount of money to earn a **high percent return
over a shorter amount of time**; **losing money is OK and will happen** —
the risk is accepted. Plan updated accordingly (PRD §1 goal amendment, new
M2b milestone, HANDOFF, project CLAUDE.md risk-posture line, auto-memory).

**What this CHANGES:**
- Objective: from "rigor + track record on a defensible edge" to
  "maximize percent return, short holds, concentrated (K=1–3 positions)" —
  with the rigor machinery RETAINED as the accuracy instrument.
- Kill-criteria philosophy for future pre-registrations: return-centric
  (CAGR/expectancy primary), drawdown ceiling LOOSENED substantially (risk
  accepted) but NOT removed — a ruin guard stays because a near-total
  drawdown ends the compounding experiment (exact numbers set per-prereg).
- Vehicles: single stocks are now in scope (E3, survivorship caveat
  mandatory); leveraged ETFs are the first high-return arm (E2).

**What this does NOT change:** pre-registration-before-results; honest
FAIL reporting; frozen-regression tripwire; EOD-only data; paper-only until
a pass + Evan's go + Alpaca account; Trading repo read-only; no post-hoc
rebrands.

**Path chosen for the next experiment — E2 (leveraged-ETF IBS):** the
evidence points here, not at stocks first: E1b proved the IBS edge persists
OOS specifically in SPY/QQQ-class broad-US indices (holdout Sharpe 0.496,
exp +17.8bps at 5bps/side); TQQQ/UPRO/SPXL/SOXL/TNA are ~3x wrappers of
those same underlyings — same validated signal, mechanically amplified
returns, no survivorship bias, full infra reuse. E3 (concentrated mega-cap
stocks) is designed AFTER E2 reads out.

**Pushback stated to Evan (kept short):** (1) "accurately" and "high return
short-window" trade off — variance blows up confidence intervals; the
pre-reg/OOS machinery is retained as the accuracy tool; (2) stocks
reintroduce yfinance survivorship bias — E3 must use a liquidity-defined
mega-cap universe with the bias caveat in every result; (3) loosened DD
ceiling is not "no ceiling."

**Cadence:** pm-cadence fired at prompt #15; this entry satisfies it (last
was Appendix K at #12-adjacent). No miss.

**Next action:** M2b.1 — extend the universe with a frozen "leveraged" group
(empirical first-bar probe, backfill), then M2b.2 pre-register E2 (doc-only
commit before runner), M2b.3 run vs gates, M2b.4 pin refs, STOP at gate.

---

# Appendix S - M2b.1: frozen LEVERAGED universe (5 ETFs) + backfill (2026-07-09, ~14:45 local)

**WHAT:** PRD task M2b.1. Probed candidates empirically, added a frozen
`LEVERAGED` list to `swing_bot/universe.py` (TQQQ 2010-02-11, UPRO
2009-06-25, SPXL 2008-11-05, SOXL 2010-03-11, TNA 2008-11-19 — first bars
fetched, not invented; liquidity $0.4B–$10.9B/day median). Backfilled all 5
into `swing.db`: 5 × 3,146 rows, 2014-01-02..2026-07-08.

**Design decision:** `LEVERAGED` is a SEPARATE list, deliberately NOT
appended to the frozen 29-ticker `UNIVERSE` — the E1 frozen-regression refs
pin full-UNIVERSE output, so growing UNIVERSE would flip the tripwire RED
and break E1's reproducibility. E2 runs on LEVERAGED explicitly.

**Data hygiene:** market open during this session (2026-07-09) — backfill
end-cut at 2026-07-08 (yfinance `end` exclusive) so no live partial bar
entered the DB; leveraged rows align exactly with the 29-ETF backfill.

**VERIFICATION (real output):** coverage gate exit 0, "coverage as-of
2026-07-08: OK" (a first-look gate_exit=-1 was diagnosed as a PowerShell
Select-Object broken-pipe artifact, re-run cleanly → 0). Frozen tests GREEN
(E1 refs untouched). Sanity scan on LEVERAGED: 4 `extreme_ret` flags, ALL
verified-real 3x moves, not corruption (2020-03-16 COVID crash: SOXL -38.6%,
TNA -37.1%; 2025-04-09 tariff-pause rally: SOXL +54.8%, TQQQ +35.2%). No
zero-range bars (the IBS-killer defect) in the group. NOTE: the 35% extreme-
ret heuristic is calibrated for 1x funds; on 3x funds these are genuine
daily moves — and a preview of the accepted risk profile.

**Next action:** M2b.2 — pre-register E2 (doc-only commit before runner).

---

# Appendix T - M2b.2-3: E2 prereg (865c09e) + run = FAIL; IBS family SHELVED (2026-07-09, ~15:05 local)

**WHAT:** Pre-registered E2 (`865c09e`, doc-only, verified no runner existed;
gates: K=2 holdout n>=100, expectancy>0, net CAGR>=15%, maxDD<=60%; Sharpe
context-only; PRE-COMMITTED STOP in §7). Then built
`scripts/run_e2_backtest.py` and ran. Full results:
`docs/research/2026-07-09_E2_leveraged_results.md`.

**VERDICT: E2 FAIL (2 of 4).** K=2 HOLDOUT (2022-2026, next-open, 5bps/side):
n=351 PASS · exp +31.0bps PASS · **CAGR 7.98% FAIL (vs 15%)** · **maxDD
60.6% FAIL (vs 60%)**. Train context: CAGR 19.6%, Sharpe 0.77 — same OOS
decay pattern as E1b, leverage-amplified.

**Key findings:** (1) the c2c (non-executable) holdout would have PASSED
everything (CAGR 18.15%, maxDD 52.4%) — the overnight gap between signal
close and next-open fill remains the project's central story (M1.8: 54% of
edge is overnight); (2) 3x crash-buying drew down 60.6% — the accepted-risk
profile, realized; (3) **engine property exposed:** K=1 context showed
maxDD 104% (NAV negative) — the engine sizes at FIXED initial-capital/K,
not current-NAV/K, i.e. implicit leverage after losses. Immaterial for
E1/E1b; does not change the E2 verdict (all three experiments shared these
semantics); recorded as a known limitation + gotchas bin. Any future engine
sizes on current NAV.

**THE PRE-COMMITTED STOP EXECUTES:** three pre-registered IBS tests have
failed (E1, E1b near-miss, E2). Per `865c09e` §7 the IBS family — 1x and
leveraged — is SHELVED. No E2b/E1c/execution-shaved re-runs by the executing
model. A near-close-execution variant (which the c2c numbers hint at) is
still IBS family → covered by the stop; only a NEW dated decision by Evan
re-opens it.

**Next action:** M2b.4 — pin E2 frozen refs; then STOP. Remaining open path:
E3 (different signal family, concentrated mega-cap stocks, M2c) — design
with its own prereg, on Evan's go.

---

# Appendix U - M2b.4: E2 refs pinned; M2b complete; STOP at gate (2026-07-09, ~15:20 local)

**WHAT:** Pinned E2 frozen refs into `swing_bot/test_frozen.py` (LEVERAGED,
K=2, next-open, 5bps): 2019H1 tpnl 25.374807% / 31 closed; 2020H1 tpnl
60.397839% / 56 closed — alongside the E1 refs. Engine fixed-sizing property
added to the gotchas bin (future engines size on current NAV).

**DONE-CHECK (real output):** `python -m swing_bot.test_frozen` → 8 numeric
refs + 2 invariants, ALL d=+0.0000pp / +0, GREEN, exit 0.

### Point-in-time snapshot — experiment program state (2026-07-09)

| Experiment | Prereg | Verdict | Gate misses |
|---|---|---|---|
| E1 — 29-ETF IBS | `8963e49` | **FAIL** | Sharpe 0.23 (vs 0.50), maxDD 36% (vs 25%) |
| E1b — broad_us OOS | `0126ce3` | **FAIL (near-miss)** | Sharpe 0.4961 (vs 0.50) |
| E2 — leveraged K=2, return-centric | `865c09e` | **FAIL** | CAGR 7.98% (vs 15%), maxDD 60.6% (vs 60%) |

**IBS family: SHELVED** (pre-committed stop, `865c09e` §7). The recurring
mechanism across all three: the effect is real close-to-close but over half
of it sits in the overnight gap the EOD next-open loop cannot enter
(M1.8: 54%); E2's c2c holdout would have passed everything (CAGR 18.15%).

**STOPPED.** No live trading (nothing passed). Options put to Evan:
(1) design E3 — different signal family on concentrated liquid stocks (PRD
M2c, own prereg, survivorship caveat); (2) Evan overrides the stop with a
NEW dated decision to test near-close execution of IBS (needs real-time
quote infrastructure; the one variant the c2c numbers directly motivate);
(3) pause and write up the E1/E1b/E2 arc as the project's first deliverable.

**Next action:** NONE autonomous — Evan chooses.

---

# Appendix V - Experiment catalog v2 (data-grounded, 20 items) + %/mo verdicts (2026-07-09, ~15:40 local)

**WHAT:** Evan asked for (a) as many experiments as possible planned from
the measured data and (b) %/month figures on the verdicts. Wrote
`docs/research/2026-07-09_experiment_catalog_v2.md` — 20 items in 4
families, each with a MEASURED / LITERATURE / TBD prior (nothing invented).

**Verdicts in %/mo (net, primary configs):** E1 +0.19%/mo FAIL · E1b
holdout +0.32%/mo FAIL(near-miss) · E2 holdout +0.64%/mo FAIL · E2 c2c
non-executable reference +1.40%/mo (would have passed). The 0.76%/mo gap
between executable and c2c IS the overnight component — the prize.

**Catalog structure:** Family A = IBS execution variants targeting the
overnight component (A1 MOC-execution, A2 near-close market orders, A3
overnight-only harvest, A4 minute-bar near-close backtest) — ALL marked
STOP-OVERRIDE REQUIRED (IBS family shelved; a "go" on an A-item = Evan's
dated override, to be recorded as such). Family B = new families,
stop-clear (B1 gap-down reversion executed AT the open — dodges the
overnight mechanism by construction; B2 gap-up continuation; B3
momentum-burst on leveraged; B4 vol-regime leverage rotation, literature
~1.2–1.5%/mo class single-source; B5 vol-filtered B4; B6 52wk-high
breakout; B7 = E3 mega-cap momentum per M2c; B8 stock gap reversion
(stop-adjacent, flagged); B9 PEAD blocked-on-data; B10 QQQ/SPY tilt).
Family C = engineering prereqs (C1 NAV-proportional engine v2 — fixes the
measured fixed-sizing gotcha; C2 near-close infra spike; C3 overlay
unchanged; C4 divergence logger). Family D = data unlocks (D1 IEX minute
bars 2016+; D2 earnings calendar).

**Recommended sequence:** C1 → {A3 (if override) + B1 + B4 one-sitting
screens} → prereg the best survivor → infra per evidence. Screens are
labeled hypothesis-GENERATING; the chosen candidate still gets its own
prereg with return-centric gates before its runner.

**Next action:** Evan picks from the catalog (any A-item = dated stop
override).

---

# Appendix W - Evan overrides IBS stop for A3; C1+screens sitting begins (2026-07-09, ~14:50 local)

**DECISION (Evan, 2026-07-09):** "go" on catalog option 1 — which, per the
catalog's stop clause, constitutes his dated override of the `865c09e` §7
IBS-family stop for **A3 only** (overnight-only IBS harvest screen). The
stop remains in force for all other IBS variants (A1/A2/A4) unless
separately green-lit.

**Sitting plan:** C1 (engine v2: NAV-proportional, cash-capped sizing as an
OPT-IN parameter so v1 frozen refs stay intact) → three one-sitting
IN-SAMPLE SCREENS labeled hypothesis-generating: A3 (overnight-only IBS,
override above), B1 (gap-down reversion executed at the open, stop-clear),
B4 (vol-regime leverage rotation, stop-clear). Screens report train/holdout/
full with %/mo. Best survivor then gets its own pre-registration before any
confirmatory run.

**Cadence:** pm-cadence fired at prompt #18; this entry satisfies it.

**Next action:** C1 implementation.

---

# Appendix X - C1: engine v2 (NAV-proportional, cash-capped) verified (2026-07-09, ~15:00 local)

**WHAT:** Added `size_on_nav` parameter to `swing_bot/backtest.py`.
v1 (default False) = fixed initial-capital/K sizing, byte-identical to all
pinned experiments. v2 (True) = target = min(prev-close-NAV/K, available
cash), floored at 0 — sizes shrink after losses; cash can never go negative.

**DONE-CHECK (real output):**
- Toy v2 hand-check exact: after NAV halves, re-entry sizes at the new NAV
  (final NAV engine 263.1579 = hand 263.1579).
- The v1 failure mode is fixed: E2 K=1 leveraged holdout — v1 min_NAV
  −33.44 (negative, maxDD 104.2%) → v2 min_NAV +109.73, maxDD 84.2%.
- **Honest note:** v2's CAGR on that path is WORSE (−13.62% vs −2.70%) —
  v1's implicit post-loss leverage happened to aid recovery there; v2 is
  simply correct accounting, not a performance improvement.
- Frozen tests: v2 ref pinned (E1-config 2019H1: tpnl 9.016509%/134) —
  now 10 numeric refs + 2 invariants, ALL GREEN d=±0.0000pp, exit 0. v1
  refs unchanged (v1 path untouched).

**Next action:** the three in-sample screens (A3 override / B1 / B4), engine
v2, labeled hypothesis-generating.

---

# Appendix Y - Screens: A3 dead, B1 dead, B4 rotation +2.15%/mo holdout standout (2026-07-09, ~15:15 local)

**WHAT:** Ran the three in-sample screens (`scripts/screens_20260709.py`),
results in `docs/research/2026-07-09_screen_results.md`. NAV-proportional
sizing, 5bps/side, K=2, train/holdout/full reported with %/mo.

**RESULTS (headline, %/mo):**
- **A3 overnight-only IBS: DEAD.** Broad NET-NEGATIVE (−0.11%/mo full) —
  the 6.3bps/signal gross overnight component can't pay 10bps round-trip
  nightly. Leveraged holdout +0.56%/mo — BELOW the already-failed E2
  next-open (+0.64). The overnight component is real but not separately
  harvestable at retail cost. **The A3 override is spent; the IBS stop
  effectively resumes in full.**
- **B1 gap-down reversion at the open: DEAD.** Best variant +0.23%/mo
  holdout (lev −2%, next-open exit), rest ≈0 or negative. Refuted at the
  screened thresholds; no prereg warranted.
- **B4 leverage rotation: STANDOUT.** TQQQ while QQQ > 200d MA else cash:
  train +2.59%/mo (CAGR 35.9%), holdout +2.15%/mo (CAGR 29.0%), Sharpe
  ~0.8, maxDD 48–58%, ~4 switches/yr (execution/cost mechanisms that killed
  E1/E2 are irrelevant at this frequency). UPRO/SPY variant much weaker OOS
  (+0.61%/mo holdout) — effect concentrates in the Nasdaq wrapper,
  consistent with every prior finding (QQQ/XLK carried E1's edge too).
  Matches the Gayed literature prior.

**HONEST CAVEATS (recorded, not buried):** (1) the screens LOOKED at
2022–2026 → holdout is contaminated for any follow-up prereg; confirmation
must rest on a pre-registered robustness battery (MA 150–250, signal-source
variants, execution lag, cost ×2) + LIVE PAPER as the only true OOS;
(2) TQQQ/QQQ was the better of two variants seen (selection), mitigated by
it also being the a priori literature construct; (3) B4 is trend-following
leverage timing with weeks-to-months holds — fits Evan's high-return goal,
stretches the "swing" label; flagged. (4) maxDD ~50–58% is the real
accepted-risk contract.

**Recommendation put to Evan:** pre-register **E4 = TQQQ/QQQ 200d-MA
rotation** (UPRO secondary context) with robustness-battery gates on the
full window (gate basis must acknowledge contamination) and live paper as
confirmation. B1 dropped; A3 closed.

**Next action:** Evan's call on E4 prereg.

---

# Appendix Z - Findings write-up (E1->B4 arc) produced; session close (2026-07-09, ~15:30 local)

**WHAT:** Evan chose to write up the arc rather than proceed to an E4 prereg.
Produced `docs/findings_2026-07-09_experiment_arc.md` — a standalone
synthesis deliverable (reads FROM this record; not part of the append-only
chain). Covers: method/discipline (prereg-before-code, OOS holdout,
kill-criteria, tripwire, data honesty); each experiment with %/mo verdict
(E1 +0.19 FAIL, E1b +0.32 FAIL near-miss, E2 +0.64 FAIL, A3/B1 dead, B4
+2.15%/mo holdout lead); the unifying overnight-execution finding; honest
limitations (B4 unconfirmed + holdout contamination + variant selection +
50-58% DD + swing-label stretch + survivorship returns with stocks); and the
meta-point (the falsifiable process is the deliverable, not a profitable bot).

**Verification:** frozen tests still green (10 refs, d=+/-0.0000pp) — no code
touched this step. All numbers in the write-up trace to committed backtests.

**SESSION CLOSE.** Large session (2026-07-08 bootstrap through 2026-07-09
E1->B4 arc, ~20 commits). Nothing live. The B4 leverage-rotation lead
(+2.15%/mo OOS) is the open thread; next stage = E4 pre-registration +
robustness battery + live paper, on Evan's direction. IBS family remains
SHELVED (A3 override spent).

**Next action:** none autonomous. Resume by pre-registering E4 (or a new
direction).

---

# Appendix AA - E4 leverage rotation: pre-reg (313d88a), engine, VERDICT = PASS; STOP at live gate (2026-07-09, ~16:30 local)

**WHAT:** Ran the full E4 chain (PRD M2d) to the live-paper gate. E4 =
200-day-MA leverage rotation, hold TQQQ while QQQ closes above its 200-day
SMA else cash, K=1.
- **E4 prereg `313d88a`** (doc-only, before the runner): honestly disclosed
  the primary cell is contaminated by the B4 screen, so gates target the
  UNSEEN — fragility across an MA/lag/cost grid, and benchmark-relative
  value (must cut buy-hold-TQQQ maxDD by >=15pp and beat buy-hold-QQQ CAGR).
- **`swing_bot/rotation.py`** (engine, after prereg) — hand-checked on a toy
  (both exec lags exact: lag0 NAV 590.909091, lag1 583.333333). Fixed a lag
  off-by-one before testing (exec at j+1+lag). `scripts/run_e4_rotation.py`
  runs the battery + benchmarks + gates.
- **`backtest.metrics` generalized** to tolerate NAV-only strategies
  (rotation switches lack IBS `net_ret`/`hold_days`) via presence checks —
  pinned fields (total_ret/n_trades) unchanged, frozen refs stayed green.

**VERDICT: E4 PASS (all 5 gates).** Primary QQQ->TQQQ N=200 lag0 5bps, full
window: CAGR 33.76% (+2.45%/mo), maxDD 57.7%, Sharpe 0.86, 51 switches.
Gates: CAGR>=15 PASS; maxDD<=65 PASS; cuts BH-TQQQ DD 81.8->57.7 (-24pp)
PASS; CAGR 33.8 >= BH-QQQ 18.3 PASS; grid 100% cells positive, median 32.5%,
no cliff PASS. Frozen refs: E4 rotation window (2015-16: tpnl -24.174806% /
16 switches) pinned; 12 refs now green d=+/-0.0000pp.

**HONEST FRAMING (recorded, not buried):** (1) rotation does NOT beat
buy-hold TQQQ on return (33.8 vs 38.4% CAGR) — its value is DRAWDOWN
reduction (82->58%), i.e. risk-managed leverage, not return enhancement;
(2) regime-flattered — 3x Nasdaq over the best tech decade; forward returns
almost certainly lower, treat +2.45%/mo as a ceiling not a forecast;
(3) primary cell contaminated (battery/benchmark are the new passing
evidence); (4) ~4 switches/yr => live-paper validation takes YEARS;
(5) 57.7% DD is real ($500 -> ~$210 at trough). Full detail:
`docs/research/2026-07-09_E4_rotation_results.md`.

**STOP — M3 live gate (BLOCKED-ON-EVAN).** E4 passed the backtest gate;
per prereg §5 this authorizes consideration for LIVE PAPER only, requiring
Evan's explicit go + an Alpaca paper account. No live money. This is the
next-stoppage-point requested.

**Next action:** Evan decides — (a) deploy E4 to live paper (needs Alpaca
account + go); (b) pre-register a harder E4 robustness test (other
eras/markets) to fight the regime-flattery concern before committing paper;
(c) new direction.

---

# Appendix AB - E5 regime test: E4 loses 93% in 2000-2013; VERDICT = FAIL; E4 de-authorized for paper (2026-07-09, ~17:30 local)

**WHAT:** Evan chose to harden E4 before paper (option b). Ran E5 (PRD M2d
hardening) per prereg `09a3a31`: synthesize daily-rebalanced 3x Nasdaq from
QQQ (1999+), calibrate drag to real TQQQ, test the 200-MA rotation over the
UNSEEN 2000-2013 (dot-com + 2008). `scripts/run_e5_regime.py` (does not touch
swing.db). Results: `docs/research/2026-07-09_E5_regime_results.md`.

**Validation gate PASS:** calibrated drag 4.00%/yr; synthetic CAGR 38.31% vs
real TQQQ 38.36% (0.05pp); daily-return corr 0.9989. Synthetic is trustworthy.

**VERDICT: E5 FAIL (all 3 gates).** 2000-2013 unseen window: rotation CAGR
-3.37% (FAIL >0), **maxDD 92.7%** (FAIL <=65 and only 7pp better than
buy-hold-3x's 100% wipeout), CAGR -3.4% < buy-hold-QQQ -0.5% (FAIL). Full
2000-2026: rotation +1.01%/mo but with a 92.7% drawdown -- untradeable.

**FINDING:** the 200-MA did NOT protect in choppy secular bears -- whipsaw
(counter-trend rallies push QQQ back above the MA, re-entering 3x right
before the next leg down) plus leverage = ~93% drawdown. **E4's +2.45%/mo
was entirely a 2014-2026 regime artifact**, exactly the flag raised at E4's
PASS (Appendix AA). Per prereg S5: E4 is REGIME-DEPENDENT -> de-authorized
as a live-paper candidate. No tuning.

**META (project state):** the mean-reversion family (E1/E1b/E2/A3/B1) and the
leverage-rotation family (E4/E5) have now all been honestly falsified for a
robust, regime-independent, cost-surviving, executable retail edge. The
recurring, data-grounded finding: simple public EOD strategies do not carry
such an edge at this scale -- caught here BEFORE any capital was risked, which
is the rigor process working as intended. Nothing is live; nothing passed to
paper.

**STOPPAGE POINT.** No autonomous next action -- Evan chooses direction with
this finding in hand (candidates: accept the falsification finding and write
it up as the deliverable / try a genuinely different family from catalog v2 /
test a de-leveraged 1x-2x rotation variant, each its own pre-registration).

---

# Appendix AC - E6 de-leveraged rotation VERDICT = PASS (robust drawdown overlay, not high-return) (2026-07-09, ~18:30 local)

**WHAT:** Evan chose "do 2 then 1." E6 (option 2): pre-registered `0526ea2`
(doc-only), then `scripts/run_e6_deleveraged.py` tested the 200-MA rotation
at 1x (real QQQ, no synthesis) + 2x-synth across three windows. Results:
`docs/research/2026-07-09_E6_deleveraged_results.md`.

**VERDICT: E6 PASS (all 3 gates).** 1x QQQ rotation vs buy-hold QQQ:
- 2000-2013: CAGR +2.66%, maxDD 52.2% vs 83.0%, Sharpe 0.24 vs 0.14
- 2014-2026: CAGR +14.47%, maxDD 24.6% vs 35.6%, Sharpe 0.92 vs 0.89
- 2000-2026: CAGR +8.04%, maxDD 52.2% vs 83.0%, Sharpe 0.54 vs 0.42
Gates: maxDD >=10pp below BH in both crash windows PASS (31pp); Sharpe >= BH
in all 3 windows PASS; CAGR>0 everywhere PASS.

**THE HONEST READ:** this is the FIRST robust, regime-spanning result -- it
passes the exact test E4 failed, because at 1x whipsaws don't compound into
ruin. It roughly HALVES QQQ's worst drawdown (83->52%) and improves Sharpe in
every regime. **BUT it is NOT the high-return goal:** full-period CAGR 8.04%
~= buy-hold QQQ 7.92% -- the value is almost ENTIRELY drawdown reduction, not
return (+0.65%/mo full, +1.13%/mo bull). In the bull it GAVE UP return (14.5
vs 18.3% CAGR) to whipsaws -- the documented cost of trend overlays. 2x-synth
does NOT beat 1x on risk-adjusted return (Sharpe 0.51<0.54, 80% DD) -- the
sweet spot is 1x. Whole rotation arc in two lines: 3x (E4) = bull artifact
that loses 93% in a real bear; 1x (E6) = real but modest, half the drawdown
for ~the same long-run return as the index.

**DISPOSITION:** E6 is a legitimate deployable RISK-MANAGEMENT overlay (not a
return engine), Evan-gated for paper. Per prereg it is the last rotation-
family experiment. E5/E6 are analysis scripts (fetch live pre-2014 history) --
NOT pinned to the frozen tests (which cover the swing.db engines). Frozen
tests remain green (12 refs).

**Next action:** Evan's option 1 -- write up the full E1->E6 falsification +
one-robust-overlay program as the deliverable.

---

# Appendix AD - Full E1->E6 program write-up (option 1); program complete (2026-07-09, ~18:45 local)

**WHAT:** Evan's option 1. Rewrote `docs/findings_2026-07-09_experiment_arc.md`
from the E1->B4 partial into the COMPLETE E1->E6 program deliverable: abstract,
method/discipline, the one-table results summary (%/mo per experiment), the two
families (mean reversion; leverage rotation with the E4-pass -> E5-regime-fail
-> E6-deleveraged-pass subplot), the two through-lines (execution + regime kill
retail edges; the only survivor is risk-management not return), honest
limitations, the process-as-deliverable meta-point, and reproducibility
(all prereg/commit hashes).

**Final honest conclusion (stated in the doc):** no robust, regime-independent,
cost-surviving HIGH-RETURN EOD strategy was found; the goal is unmet and the
evidence says that is the base rate at this scale. One deployable result
emerged -- 1x 200-MA rotation (E6) -- but it is risk-management (halves index
drawdown for ~the same long-run return), not a return engine. The portfolio
value is the falsification program itself: it caught E4 (a 33%-CAGR-looking
false positive) via a pre-registered out-of-regime test before any capital
was risked.

**PROGRAM COMPLETE.** Nothing live. Frozen tests green (12 refs). Open,
Evan-gated: deploy E6 (1x) to paper as a risk-managed core; open a genuinely
new family (stocks/events, needs E3 survivorship-safe universe); or close on
this write-up.

**Next action:** none autonomous -- program is at a clean terminal state.

---

# Appendix AE - Pressure-test: buy-hold-TQQQ claim retracted; clean test data exhausted (2026-07-10, ~00:10 local)

**WHAT:** Evan asked to pressure-test the chat claim "buy-hold TQQQ beats my
bots, and no pre-registerable tweak has a genuine shot at high-return AND
regime-robust." Tried to break it; it half-broke.

**CRACK 1 (my error, RETRACTED):** "buy-hold TQQQ beats my bots" is itself
regime-flattered -- true only for 2014-2026. Over the full cycle (E5
synthetic) buy-hold 3x = -2.74% CAGR / -100% drawdown (wiped out in
2000-2002). I made the exact bull-only-quote mistake I criticized in E4. Over
a full regime cycle E6 (1x) and even E4's rotation beat buy-hold TQQQ; the
"buy-hold wins" statement only holds if you assume a 2014-26-like future.

**CRACK 2 (claim too strong, but reframed):** a volatility-gated leverage
rotation (hold 3x only when trend up AND realized vol low) is a
mechanistically credible UNTESTED idea -- 2000-02/2008 were high-vol, exactly
when leverage+whipsaw kills you, so a vol gate has a real reason to help.
BUT: 2000-2013 is now SEEN twice, so any vol threshold chosen to survive
those crashes is hindsight-fit. Asymmetric info: only a hindsight FAIL would
be informative. Empirical probe `scripts/pt_volgate.py` written but BLOCKED
on yfinance rate-limiting (4 attempts, all 429; pre-2014 QQQ not cached, only
2014+ is in swing.db) -- NaN output; not hammering the API further.

**THE DEEPER, OPERATIVE FINDING:** the binding constraint is no longer "no
more ideas" -- it is EXHAUSTED CLEAN TEST DATA. The two independent US crash
regimes (2000-02, 2008) have now been used to judge the rotation family, so
any further high-return backtest tweak tested on them is contaminated. Honest
validation of any NEW high-return idea must be (a) forward live paper, or
(b) genuinely independent markets/regimes -- in-sample backtesting on the
same crashes has hit negative returns to rigor. This SHARPENS rather than
softens the conclusion: no high-return-AND-robust strategy has been
demonstrated, and the cheap way to keep looking has been used up.

**NET:** claim was half-wrong (buy-hold TQQQ is not robust) but the practical
bottom line stands and is better-grounded: to chase high-return-robust from
here requires forward testing or new data, not more backtests. Nothing live;
frozen tests green.

**Cadence:** pm-cadence fired at prompt #24; this entry satisfies it.

**Next action:** Evan's call -- (a) run the vol-gate probe when the API cools
(exploratory, contaminated); (b) forward-test a candidate via live paper
(needs Alpaca + go); (c) new independent-market data; (d) close on the
write-up.

---

# Appendix AF - E7 international validation: BOTH arms FAIL; high-return-robust question CLOSED (2026-07-10, ~00:45 local)

**WHAT:** Evan said "go / continue the roadmap." Executed E7 (PRD M2e), the
clean-data unlock from Appendix AE: test on genuinely-unseen non-US regimes.
yfinance rate limit had cleared; fetched Nikkei (1985+), DAX, FTSE, HSI, ASX,
+ S&P cross-check. Pre-reg `70ed2a1` (doc-only, a-priori vol=30% + drag=5%/yr
fixed from first principles). Runner `scripts/run_e7_international.py`.
Results: `docs/research/2026-07-10_E7_international_results.md`.

**ARM 1 (does E6 1x overlay generalize?): FAIL, 3/5 (need >=4).** Works in
Japan/Germany/HK/US (big DD cuts incl. Nikkei 82%->34%!, higher Sharpe);
FAILS in UK (barely cut DD, Sharpe 0.39->0.20) and Australia (cut DD but
Sharpe 0.43->0.30). E6 DOWNGRADED: real but MARKET-DEPENDENT, not a universal
law -- in choppy trending markets the whipsaw cost exceeds the drawdown
benefit risk-adjusted.

**ARM 2 (a-priori vol-gated 3x high-return shot): FAIL, all 4 gates.** Mean
CAGR 4.55% (bar 15%); FTSE -1.34% & 97.3% DD; Nikkei +6.93% but 83.3% DD;
vol gate barely beat plain-3x (Nikkei 83.3 vs 85.1). **HSI 3x is degenerate:
the 1987 Hang Seng >33%-one-day crash mathematically WIPES OUT any 3x daily
fund to zero permanently (buy-hold-3x = -100%)** -- a mathematical, not
statistical, argument against extreme leverage. Verdict holds on multiple
independent gates without HSI.

**THE DEFINITIVE CLOSE:** the one credible untested high-return idea
(a-priori-vol-gated leverage rotation) was tested on 5 genuinely independent
unseen regimes with fixed knobs (no fitting) and FAILED every gate. The
conclusion upgrades from "ran out of US data" to "found clean data and the
idea failed on it." **No high-return-AND-robust EOD strategy found -- now
backed by out-of-sample international evidence, not just US in-sample.** Even
the one risk-mgmt survivor (E6 1x) is market-dependent.

**Engine/data notes:** synthetic floored at 0 (real funds can't go negative);
rotation can't buy a dead (o=0) fund; stats() guards 0/0 daily returns post-
wipeout. E7 is a live-fetch analysis script, NOT pinned to frozen tests
(which stay green, 12 refs). PRD updated: M2e (E7) done, M6 (packaging) added.

**Next action (autonomous-continuable):** M6 portfolio packaging (README,
record HTML twin, git tag) -- needs neither Evan nor more data. Then the wall:
M3 deployment is BLOCKED-ON-EVAN (Alpaca account + go).

---

# Appendix AG - Write-up updated to E7 + M6 packaging (README, tag); at the deploy wall (2026-07-10, ~01:10 local)

**WHAT:** Continued autonomously past E7. (1) Updated the deliverable
`docs/findings_2026-07-09_experiment_arc.md` from E1->E6 to the full E1->E7
program: added the international out-of-sample close, a third through-line
(extreme leverage is tail-fatal -- HSI 1987), downgraded E6 to
market-dependent, and strengthened the conclusion to rest on OOS
international evidence. (2) M6 packaging: wrote `README.md` (cold-readable
entry point -> findings doc / HANDOFF / record, experiment table, reproduce
steps, honest conclusion). (3) git tag marking program-complete.

**DELIBERATELY SKIPPED (reported, not silent):** the record HTML twin. This
project never built a renderer (unlike Trading); building an anchor-checking
renderer is disproportionate to the value now, and the markdown record reads
fine on GitHub. Deferred; noted here so a future session doesn't assume one
exists.

**THE WALL.** Everything autonomously doable is done. The only remaining
roadmap items are BLOCKED-ON-EVAN: M3 live-paper deployment needs an Alpaca
paper account + Evan's explicit go; opening a new strategy family (E3 stocks)
needs Evan's direction. Per "keep going until you can't anymore" -- this is
where I can't without Evan. Program is at a clean, packaged terminal state;
nothing live; frozen tests green (12 refs).

**Next action:** none autonomous. Evan-gated: deploy E6-1x to paper (Alpaca +
go) / open a new family / consider the project closed on the write-up.

---

# Appendix AH - Evan opens E3 (stock momentum); survivorship-bias design problem (2026-07-10, ~01:30 local)

**WHAT:** Evan chose option 2 — open a genuinely new family: E3, concentrated
single-stock momentum (K=1-3), the natural home for high return per the
redefined goal.

**THE LOAD-BEARING PROBLEM (design-first, before any run):** yfinance carries
only CURRENTLY-LISTED names, so any stock backtest silently omits companies
that went bankrupt/delisted — and those deaths CLUSTER in the crash regimes
(2000-02, 2008) that decide robustness. So a stock momentum backtest is MOST
survivorship-flattered exactly in the periods that matter most. Compounding
it: using today's large-caps as the universe adds LOOKAHEAD bias (I'd be
picking the names that became winners). No point-in-time constituent data is
available (Trading's price_cache has the same yfinance limitation).

**CONSEQUENCE:** a rigorous return-claim backtest of stock momentum is
effectively impossible with available data. Honest design = ASYMMETRIC
FALSIFICATION (same logic as the AE vol-gate probe): run concentrated
momentum on a current liquid large-cap universe, fully disclose both biases,
and interpret ONLY a FAILURE as clean (if momentum fails even with
survivorship+lookahead+a tech bull ALL in its favor, stocks are closed too);
a PASS is uninterpretable and routes to forward live paper (the only
survivorship-free test) — which is Evan/Alpaca-gated.

**PLAN:** (1) probe stock-data availability (yfinance rate-limited earlier);
(2) if available, pre-register E3 (doc-only) with the falsification-only
interpretation baked in; (3) run a bounded 2014-2026 large-cap momentum
backtest; (4) report per the asymmetric framing. Cadence #27 satisfied by
this entry.

**Next action:** stock-data probe, then E3 pre-registration.

---

# Appendix AI - E3 stock momentum FAIL (clean); all three families now falsified (2026-07-10, ~01:55 local)

**WHAT:** Ran E3 per prereg `87bc8d9` (`scripts/run_e3_stock_momentum.py`,
background run, 39/39 survivor large-caps fetched). Concentrated momentum:
top-3 by 63-day return, 10-day rebalance, next-open, 5bps/side. Results:
`docs/research/2026-07-10_E3_stock_momentum_results.md`.

**VERDICT: E3 FAIL — clean.** 2000-2013 gate: CAGR 6.27% (FAIL vs 15%),
maxDD 61.8% (pass). Per the prereg's asymmetric framing, a FAIL is
interpretable: momentum lost even with survivorship+lookahead+favorable
universe all helping. And it failed BADLY, two ways:
- 6.27% vs the 15% bar (wide miss, not marginal).
- **Momentum was WORSE than passive:** it underperformed equal-weight
  buy-hold of its OWN survivor universe in every window (2014-26: E3 4.79%
  vs EW-universe 14.94%). The selection itself destroyed value.

**THE COMPREHENSIVE CLOSE:** all three plausible high-return routes are now
falsified under pre-registration — index mean reversion (E1/E1b/E2/A3/B1),
leveraged trend (E4/E5/E7), and concentrated stock momentum (E3). Nothing
went live. A single pre-registered momentum spec was tested; hunting a
passing parameterization would be hindsight fishing (not done). The search is
comprehensively closed; only forward live paper (survivorship-free, Evan-
gated) could test any stock idea further, with a poor prior.

**WALL AGAIN.** Autonomous avenues exhausted. Remaining work is Evan-gated
(deploy E6-1x to Alpaca paper) or accept the falsification program as the
deliverable. Frozen tests green (12 refs); E3 is a live-fetch script, not
pinned.

**Next action:** none autonomous. Fold E3 into the write-up (below), then
report the wall to Evan.

---

# Appendix AJ - Program conclusion written; findings-doc consolidation flagged (2026-07-10, ~04:45 local)

**WHAT:** Evan asked to "write the conclusion for all the experiments so far."
Produced a single canonical Conclusion synthesizing all 8 pre-registered
experiments across 3 families (index mean reversion E1/E1b/E2/A3/B1;
leveraged trend E4/E5/E7; concentrated stock momentum E3), the pre-registration
method, the one demoted survivor (1x MA rotation = market-dependent
risk-management overlay), and the honest bottom line. Delivered in-chat.

**HONEST FLAG (not a yes-man pass):** the findings doc
(`docs/findings_2026-07-09_experiment_arc.md`) ALREADY contains the concluding
material, but scattered across four sections (Abstract; "The two through-lines"
- MISLABELED, it lists three; "What this program demonstrates"; "Bottom line
for the stated goal"). Writing a fresh conclusion into the doc would duplicate.
Offered Evan a choice: consolidate those four into one `## Conclusion` (and fix
the two/three label bug) vs leave the doc as-is. Not done unilaterally
(surgical-changes discipline).

**STATE:** program still comprehensively falsified / terminal; nothing live;
frozen tests green (12 refs). No code touched. Reddit-thread read request
(prior prompt) abandoned by Evan via interrupt/compact - reddit.com blocked at
host level for the fetch tools; not pursued.

**Next action:** await Evan's choice on doc consolidation; otherwise no
autonomous work remains (Alpaca deploy is Evan-gated). Cadence #30 satisfied.

---

# Appendix AK - Project published public on GitHub (2026-07-10, ~04:52 local)

**WHAT:** Evan authorized publishing the repo public as
`Swing-Trading-Project`. Pre-publish secret scan first (git-tracked files
only): no `.env`/`.key`/`.pem`, no keys/tokens in tracked text, `swing.db`
and `*.env` correctly gitignored, no >1MB binaries. Clean.

**REMOTE ALREADY EXISTED:** `gh repo create` failed ("Name already exists")
— Evan had created `Evan-Daruwalla/Swing-Trading-Project` (public, default
branch `main`) concurrently, containing only a placeholder `README.md`
("Initial commit" `972d109`). Verified the remote tree held nothing but that
throwaway README before overwriting.

**PUBLISHED:** `git remote add origin` + renamed local `master`->`main` (matches
convention) + `git push -u origin main --force` (replaced the placeholder
`972d109` with full history head `46e3e0f`). Then `git push --tags`
(`v1.0-program-complete`, `v1.1-all-families-closed`). Remote now: 38 commits,
2 tags, full history. URL: https://github.com/Evan-Daruwalla/Swing-Trading-Project

**STATE:** program terminal/falsified, nothing live. Repo is now the public
portfolio artifact. Only remaining work is Evan-gated (Alpaca paper deploy of
the 1x overlay). Cadence #33 satisfied (was overdue one prompt; logged, not
hidden).

**Next action:** none autonomous. This record entry itself is now an
uncommitted local change (offer to commit+push).

---

# Appendix AL - Reddit thread analysis; Evan opens E8+E9 (new families) (2026-07-10, ~04:57 local)

**WHAT:** Evan pasted the r/swingtrading thread "What Is Your Swing Trading
Strategy (that you actually make consistent profit with?)" (reddit was
host-blocked for fetch tools; content supplied manually) and asked for new
ideas. Analysis delivered in-chat: most thread strategies are (a) already
falsified by E1-E7/E3, (b) regime-flattered bull-market anecdotes (the
"never book a loss" crowd = hidden unrealized drawdown, the E4 mistake with
worse bookkeeping), or (c) unfalsifiable/intraday. Survivor selection noted
(one commenter admits blowing 30 accounts). Thread's own median wisdom
(write rules first, paper trade, consistent monthly profit doesn't exist)
converges with this program's method and conclusion.

**GENUINELY NEW families surfaced (never tested here):**
- E8 = volatility-compression breakout (TTM-squeeze proxy: BB inside
  Keltner -> breakout entry). Fourth family - reversion/trend/xs-momentum
  never covered breakouts.
- E9 = "never book a loss" audit: buy large-cap ETFs >=20% below ATH, +15%
  target, NO stop - codifies the thread's most-upvoted claim to expose (or
  refute) the hidden tail across 2000-13.
- (Deferred: E10 pre-earnings run-up - needs earnings-date data probe.
  Scale-in sizing study - requires Evan formally reopening shelved IBS.)

**EVAN DECISION (2026-07-10): "do 1"** = pre-register E8+E9 together, run
both, commit AK with the preregs. Stated priors (honest): both expected to
FAIL the high-return gates per program base rate (0/8 so far); testing is
information because the FAMILIES are new, not parameter fishing.

**Next action:** write prereg_e8/e9 docs, doc-only commit BEFORE runners
(the rigor claim), then runners via live fetch (NOT swing.db writes -
protects frozen refs), run, results docs, verdicts. Cadence #36 satisfied.

---

# Appendix AM - E8 FAIL + E9 FAIL (both predictions confirmed); 0/10 across five families (2026-07-10, ~05:15 local)

**WHAT:** Ran E8 (squeeze breakout) and E9 (deep-dip "never book a loss"
audit) per prereg `9b49190` (doc-only commit BEFORE runners, per
discipline). Runners `scripts/run_e8_squeeze.py` / `run_e9_deepdip.py`;
live-fetch scratch cache (`.e8e9_cache/`, gitignored); swing.db untouched;
frozen tripwire GREEN after (12 refs, d=+/-0.0000pp). Results doc:
`docs/research/2026-07-10_E8_E9_results.md`.

**E8 VERDICT: FAIL.** Gate 2000-13 CAGR -1.43% (bar +15%), win 31%,
n=187; even 2014-26 bull only +1.10%/yr. Compression predicts expansion,
not direction. Breakout family (the fourth) falsified and closed.

**E9 VERDICT: FAIL (high-return gate); BOTH a-priori predictions
CONFIRMED.** 0/53 realized losses - the Reddit claim is literally TRUE -
and gate CAGR 3.46%, worst unrealized position -79.7%, longest hold ~17
YEARS to reach +15%, cash idle 38% of days. The 100% win rate measures
bookkeeping, not performance. Fifth family closed.

**PROGRAM BASE RATE: 0 PASS / 10 pre-registered attempts / 5 families.**
E1-E7+E3 findings doc stays point-in-time; E8/E9 results doc extends the
evidence to the same conclusion. Nothing live; remaining work Evan-gated.

**Next action:** sync README (add E8/E9 rows - repo is now PUBLIC), touch
HANDOFF status, update auto-memory, commit. Push only on Evan's word.

---

# Appendix AN - Evan authorizes push of E8/E9 arc to public repo (2026-07-10, ~19:43 local)

**WHAT:** Evan: "1" = push the three pending commits (46e3e0f findings
Conclusion consolidation, 9b49190 E8/E9 prereg, 9f372b7 E8/E9 results) to
the public GitHub repo. This entry appended per cadence #39, committed with
the push so the remote lands fully current (no trailing local-only record
state).

**STATE:** unchanged otherwise - 0 PASS / 10 attempts / 5 families, nothing
live, frozen tests green. Remaining work Evan-gated (Alpaca paper deploy of
the 1x overlay, or close on the write-up).

**Next action:** commit this entry, push main to origin.

---

# Appendix AO - E10/E11/E12 PRE-REGISTRATION (from swing-trading articles) before runners (2026-07-10, ~20:10 local)

**WHAT:** Evan supplied a 5-source swing-trading article set (Investopedia,
Schwab, TD, CapTrader, + long-form ex-Trillium YouTube trader & SMB Capital
guide) and said "try everything." Assessment (in-chat): nearly all content
reduces to already-falsified primitives (E1 MR, E8 breakout, E9 deep-dip,
E4/E6 trend) or is intraday/discretionary (out of EOD scope). THREE genuinely
testable directions extracted and pre-registered doc-only BEFORE runners:

- **E10** = post-earnings-announcement drift (PEAD / catalyst continuation) -
  the one edge named by 3 independent sources. Data probe (2026-07-10):
  yfinance `get_earnings_dates(limit=100)` reaches ~2001-2002 for large caps
  (100-row cap; earnings_history only 4 quarters; needs lxml, installed).
  Single-stock => inherits E3 survivorship+lookahead => E3's asymmetric-
  falsification framing (only a FAIL is clean). Same 39 survivor large-caps
  as E3. Price-reaction signal (>=+3% earnings reaction -> buy, hold 40d).
- **E11** = volume-gated breakout: E8 IDENTICAL rules + RVOL>=1.5 on the
  breakout bar (the only change). Tests the pros' "volume confirms direction"
  claim. Framed to avoid retuning-a-FAIL: gate specified a priori by sources,
  not reverse-engineered from E8's losers. Weak prior.
- **E12** = confirmed-capitulation MR ("right side of the V"): arm on >=15%
  drop off 10d high WITH RVOL>=1.5 climax, enter on first close>prior high,
  trail on prior-bar low. Distinct from E1 (waits for confirmation vs buying
  the dip). 29-ETF universe (survivorship-clean).

Prereg gates all fixed a priori (2000-13 gate, CAGR>=15% + DD ceiling +
n_trades floor). Runners will NOT write swing.db (protects frozen refs);
E11/E12 reuse the .e8e9_cache. Prior across the board: POOR (program 0/10).
Doc-only commit hash predates all runner code.

**Next action:** commit preregs, write runners E10/E11/E12, run, frozen
tests, results doc, verdicts. Cadence: this entry serves the record step.

---

# Appendix AP - E10/E11/E12 all FAIL; article-set arc closed; 0/13 across six families (2026-07-10, ~20:10 local)

**WHAT:** Ran all three article-set experiments per prereg `129dc22`
(doc-only before runners). Runners: `scripts/run_e10_earnings_drift.py`,
`run_e11_volgated_breakout.py`, `run_e12_confirmed_capitulation.py`.
E11/E12 reused the .e8e9_cache; E10 fetched 39 survivor stocks + earnings
dates (yfinance get_earnings_dates, ~99 quarters/name back to ~2001).
swing.db untouched; frozen tripwire GREEN after runs.

**E11 (volume-gated breakout) FAIL:** gate 2000-13 CAGR -0.74% (n=46, win
30.4%); secondary -0.25%. The a-priori RVOL>=1.5 gate the pros swear by did
NOT give breakouts direction - it just thinned E8's directionless signal.

**E12 (confirmed-capitulation MR) FAIL:** gate CAGR -4.71% (n=90, win
35.6%), maxDD 55%. Waiting for the confirmed "right side of the V" did
WORSE than E1's raw dip-buying: the confirmation bar surrenders the
reversal pop, then the prior-bar-low trail whipsaws out.

**E10 (PEAD) FAIL - clean under the asymmetric framing:** gate CAGR 5.93%
vs 15% bar (n=272 entries, win 58.5%, maxDD 49.3%). NUANCE, honestly noted:
E10 is the ONLY experiment in the whole program to BEAT both benchmarks in
the hostile regime (5.93% vs EW-universe -0.47% and SPY 1.72% in 2000-13,
Sharpe 0.39) - PEAD had a real risk-adjusted signature even before its
survivorship flattery. But post-2014 it underperformed both (5.30% vs EW
13.97% / SPY 11.98%) - consistent with the academic record that PEAD decayed
after ~2010 as it was arbitraged. As a HIGH-RETURN strategy it fails
decisively in every window; because the universe is bias-flattered, the FAIL
is interpretable. PEAD closed for backtested high-return claims.

**SCORE: 0 PASS / 13 pre-registered high-return attempts / 6 families**
(mean reversion incl. E12 refinement, leveraged trend, stock momentum,
breakout incl. E11 refinement, deep-dip, event-driven/PEAD). Every
codifiable idea from the Reddit thread AND the 5-source article set is now
tested and falsified. Cadence #42 satisfied by this entry.

**Next action:** results doc, README/HANDOFF/memory sync, commit. Push only
on Evan's word.

---

# Appendix AQ - graphify knowledge graph built (2026-07-10, ~20:25 local)

**WHAT:** Ran /graphify on the project. 69 files / ~56.6k words ->
281-node / 511-edge graph, 13 communities. AST (26 py files) = 156 nodes;
semantic extraction (43 docs via 2 parallel general-purpose subagents,
no Gemini key so host-LLM path) = 125 nodes. Outputs in graphify-out/
(graph.html, GRAPH_REPORT.md, graph.json, manifest.json, cost.json).

**HEALTH WARNING (surfaced, not hidden):** 87 dangling-endpoint edges
(~14% of 601 raw) from cross-chunk node-id mismatch - chunk 1 anchored
E8-E12 to handoff_* ids, chunk 2 created docs_prereg_* / research_* ids for
the same experiments; edges across the seam dangle. Graph still built (511
valid edges). Fixable with `graphify extract --force` + single-chunk or a
shared id map if a cleaner graph is wanted.

**God nodes** (as expected): HANDOFF (23), PRD_ROADMAP (18), Project Record
(17), findings write-up (15) - the doc system is the spine. Communities map
cleanly to the experiment arc (IBS core, leverage rotation E4-E7, article-set
E8-E12, stock momentum E3, engine/gates). graphify-out/ is a generated
artifact, currently UNCOMMITTED and not gitignored.

**Next action:** none required; offer to commit or gitignore graphify-out.
Cadence #45 satisfied.

---

# Appendix AR - Research brief: exhaustive swing-strategy catalog (2026-07-10, ~20:40 local)

**WHAT:** Ran /research-brief on "every swing-trading idea with merit,"
cross-referenced against the 13 falsified experiments. ~40 documented ideas
catalogued with primary sources (de Groot 2012, Frazzini-Lamont 2007,
George-Hwang 2004, Hong-Li-Ni 2015, McConnell-Xu 2008, Greenwood-Sammon 2025,
Moskowitz-Ooi-Pedersen 2012, etc.). Doc: docs/research/2026-07-10_swing_strategy_catalog.md.

**FINDING:** vast majority are KILLED-HERE, ADJACENT-KILLED, DECAYED,
OUT-OF-SCOPE, or OVERLAY. Only FIVE are genuinely untested-here + merit +
in-scope: (1) cross-sectional short-term reversal (weekly, large-cap,
cost-opt; de Groot); (2) earnings-ANNOUNCEMENT premium (buy PRE-earnings;
distinct from FAILED E10 post-drift; reuses E10 infra); (3) short-interest/
days-to-cover screen; (4) DIVERSIFIED sector momentum (concentrated E3
already FAILED); (5) turn-of-month overlay. Honest caveat recorded: 4 of 5
are diversified/cross-sectional, not the concentrated high-return bet the
goal wanted; the fill-timing ablation is direct counter-evidence vs the
reversal candidates. High-return-robust-retail-EOD cell still empty.

**Next action:** none unless Evan picks a candidate to pre-register. This is
an informational brief, not an experiment.

---

# Appendix AS - Push of E10-E12 arc + catalog + graph; next-steps planning (2026-07-10, ~21:13 local)

**WHAT:** Evan authorized push ("push then plan the next steps"). Pushing 4
pending commits (129dc22 E10-E12 prereg, 46cc68b E10-E12 results, c95800f
catalog+graph, edf7991 path-leak cleanup) plus this entry to the public repo.

**STATE at push:** 0 PASS / 13 attempts / 6 families; strategy-catalog brief
identifies 5 untested-with-merit candidates (x-sectional reversal,
earnings-announcement premium, days-to-cover, diversified sector momentum,
turn-of-month overlay); knowledge graph committed. Next-steps plan to follow
in-chat. Cadence #48 satisfied.

---

# Appendix AT - M7 plan: catalog arc E13-E17 written into PRD (2026-07-10, ~21:20 local)

**WHAT:** Evan asked to "plan out the experiments and next steps for the new
proposed strategies." Added milestone M7 to PRD_ROADMAP.md (table row +
full task section, tasks 28-32): E13 turn-of-month overlay, E14 diversified
sector momentum (survivorship-clean - only M7 candidate where a PASS would
be fully interpretable), E15 earnings-announcement premium (reuses E10
earnings infra; survivor-stock asymmetric framing + scheduled-date caveat),
E16 x-sectional weekly reversal (fill-timing-ablation counter-evidence
disclosed), E17 days-to-cover (data probe first; BLOCKED-ON-DATA likely).
Execution order = build cost x interpretability; one per sitting; rigor
discipline unchanged.

**D1 - NEW DECISION, BLOCKED-ON-EVAN:** the plan's honest premise is that
none of the five plausibly clears the 15% CAGR bar; three plausibly clear a
risk-adjusted bar. Proposed pre-registered SECONDARY verdict tier (PASS-RA:
net Sharpe >= 0.80 in gate window AND > SPY Sharpe both windows AND positive
net CAGR both windows) alongside the UNCHANGED primary PASS-HR gate. This is
a goal amendment vs the 2026-07-09 return-centric decision, so it requires
Evan's dated approval; declined => M7 runs primary-gate-only with the stated
near-certain-FAIL prior. M7 exit conditions + M3 feed-forward defined in the
PRD. PRD/record currently UNCOMMITTED.

**Next action:** Evan decides D1, then M7 task 28 (E13 prereg) is the
default next sitting.

---

# Appendix AU - Data-type exploration started (2026-07-12, ~00:45 local)

**WHAT:** Evan asked to "explore strategies based on other sources of
data/data types" - the data axis, complementing the strategy-space catalog
(Appendix AR). Plan: probe actual availability (no invented claims) of
non-OHLCV data usable at retail: VIX complex, self-computed breadth,
dividend calendars, FRED macro/credit spreads, EDGAR insider filings, short
interest history, Google Trends, options/IV history, news/LLM sentiment;
source the load-bearing anomaly papers; write a ranked brief with honest
BLOCKED-ON-DATA tags. M7 (E13-E17) remains the standing plan; this may add
candidates or a second decision point. Cadence #51 satisfied.

**Next action:** probes + brief, then report.

---

# Appendix AV - Data-type brief done: 6 available, 3 blocked, E18-E20 proposed (2026-07-12, ~01:05 local)

**WHAT:** Completed the data-type exploration (Appendix AU). All availability
claims PROBED live (probe_datatypes.py): VIX 1990+, VIX3M 2006+, VVIX/SKEW,
dividends full history, FRED keyless (T10Y2Y 1976+, ICSA 1967+, HY OAS needs
cosd param), breadth self-computable from 107 cached tickers. BLOCKED at $0:
options/IV history, short-interest history (E17 probe still owns it),
point-in-time news archives; Google Trends REJECTED on reproducibility
(resampled per request). Doc: docs/research/2026-07-12_data_type_exploration.md.

**PROPOSED (not pre-registered):** E18 regime-gate bake-off (VIX term
structure vs HY-OAS vs breadth vs 200DMA as overlays on E6 criteria -
recommended; upgrades the one surviving artifact); E19 insider
opportunistic-buy drift (Cohen-Malloy-Pomorski 82bps/mo - strongest new-type
anomaly, gated behind a scoped EDGAR Form 4 ingestion probe); E20 dividend
capture falsification (cheap, low prior). Honest through-line: available new
data types skew to OVERLAYS, not return engines - same shape as 0/13.
Depends on D1 (risk-adjusted tier) which remains BLOCKED-ON-EVAN; declining
D1 guts E18's point.

**Next action:** Evan decides D1 + whether E18-E20 join M7 (as M7b or after
E13-E17). Docs uncommitted.

---

# Appendix AW - D1 APPROVED (risk-adjusted verdict tier); M7b added (2026-07-12, ~01:15 local)

**EVAN DECISION (2026-07-12, dated goal amendment):** approved D1 - a
pre-registered SECONDARY verdict tier alongside the unchanged primary
high-return gate, for all M7/M7b catalog-arc experiments:
- PASS-HR (primary, unchanged): net CAGR >= 15% AND maxDD <= 60% in the
  2000-2013 gate window, confirmed 2014->end.
- PASS-RA (NEW): net Sharpe >= 0.80 in the gate window AND Sharpe > SPY
  buy-hold in BOTH windows AND positive net CAGR in both.
- FAIL: neither. All three fixed in each prereg before running.
This amends the 2026-07-09 return-centric decision (record Appendix R). Per
project rules, risk-appetite gate numbers change only by a new dated Evan
decision - this is that decision. PASS-RA does NOT authorize live capital;
a PASS-RA survivor is an M3 paper-deploy candidate (Alpaca+go still gated).

**ALSO:** added M7b to PRD (tasks 33-35): E18 regime-gate bake-off, E19
insider opportunistic-buy drift (EDGAR-probe-gated), E20 dividend capture.
Runs after M7's E13-E17.

**INSTRUCTION:** Evan said continue the roadmap, check work, append memory
docs at natural stopping points, keep going until blocked. Executing M7 in
order starting task 28 (E13). One experiment per sitting: prereg doc-only
commit -> runner -> run -> results doc -> record -> commit.

**Next action:** commit+push this planning batch, then E13 prereg.

---

# Appendix AX - E13 turn-of-month FAIL (both D1 tiers) (2026-07-12, ~01:25 local)

**WHAT:** M7 task 28. Ran E13 per prereg 0324196 (doc-only commit first).
Runner run_e13_turn_of_month.py; SPY from cache; swing.db untouched; frozen
tripwire GREEN. Results: docs/research/2026-07-12_E13_results.md.

**VERDICT: FAIL (both tiers).** In-market 19.1% of sessions. Gate 2000-13:
CAGR 1.41%, Sharpe 0.20 (vs SPY-BH 1.72%/0.19). Secondary 2014-: 1.44%/0.23
vs SPY 11.98%/0.74. PASS-HR fails (nowhere near 15%); PASS-RA fails (gate
Sharpe 0.20<0.80, and loses to SPY in the bull window - must beat both).

**NUANCE recorded:** TOM matched SPY's return in the FLAT 2000-13 decade
while holding cash 81% of the time (real McConnell-Xu concentration), but
that's risk-reduction not edge; the 2014 bull exposed it. First experiment
under the D1 dual-bar verdict; the RA tier worked as intended (caught that
a same-return-lower-exposure overlay still isn't a Sharpe-beater in both
regimes). Program 0/14 primary.

**Next action:** commit E13, then M7 task 29 (E14 sector momentum).

---

# Appendix AY - E14 sector momentum FAIL (survivorship-CLEAN; lost to passive) (2026-07-12, ~01:35 local)

**WHAT:** M7 task 29. Ran E14 per prereg f922f1f (doc-only first). Runner
run_e14_sector_momentum.py; 11 SPDR sectors from cache; swing.db untouched;
tripwire GREEN. Results: docs/research/2026-07-12_E14_results.md.

**VERDICT: FAIL (both D1 tiers).** Gate 2000-13 CAGR 2.42%/Sharpe 0.22;
secondary 6.99%/0.48. PASS-HR fails (2.4% vs 15%), PASS-RA fails (Sharpe
0.22<0.80, loses SPY in bull).

**SIGNIFICANCE:** this is the program's CLEANEST negative to date because
the 11 SPDR sectors are SURVIVORSHIP-CLEAN (no delisting bias) - so unlike
E3 the result is fully interpretable both directions, no asymmetric framing
needed. And momentum UNDERPERFORMED equal-weight buy-hold of the same
sectors in EVERY window (gate 2.42% vs 4.13%, sec 6.99% vs 10.53%) - the
same value-destruction as E3, now on unriggable data. Concentrated momentum
does not survive at this horizon net of cost, cleanly demonstrated.

**Next action:** commit E14, then M7 task 30 (E15 earnings-announcement
premium; reuses E10 earnings-date infra).

---

# Appendix AZ - TIMEZONE CORRECTION: record stamps were UTC, adopt CST (UTC-5) (2026-07-11, ~20:55 CST)

**WHAT / CORRECTION (Evan flagged 2026-07-11):** every prior appendix labeled
"local" actually carries the UTC (Z) time copied from the /project-memory
cadence hook, NOT local time. The project's timezone is **CST (UTC-5)**.
Adopted going forward; this and all later entries use CST.

**Conversion for prior entries:** subtract 5 hours from the labeled time; the
DATE rolls back one day when that crosses midnight. Notably:
- Appendices AU-AY are headed "2026-07-12, ~00:45-01:35" (UTC) -> correct CST
  is **2026-07-11, ~19:45-20:35**. Their header DATE (07-12) is wrong; true
  work date is 2026-07-11.
- Appendices AK-AM ("2026-07-10 ~04:52-05:15" UTC) -> 2026-07-09 ~23:52 to
  2026-07-10 ~00:15 CST. All other "local" stamps: -5h, same-day unless the
  UTC time is < 05:00 (then prior day).

Prior committed entries are NOT rewritten in place (append-only discipline;
several predate this session and their exact source times can't be verified).
This note is the authoritative correction. A standing convention added to
project CLAUDE.md so it does not recur.

**Next action:** resume M7 - E15 runner (task 30 in progress).

---

# Appendix BA - E15 earnings-announcement premium FAIL (clean); the decayed-anomaly twin of E10 (2026-07-11, ~21:15 CST)

**WHAT:** M7 task 30. Ran E15 per prereg 9b0aeb3 (doc-only first). Runner
run_e15_earnings_premium.py; reused E10 earnings-date + OHLCV cache;
swing.db untouched; tripwire GREEN. Results: docs/research/2026-07-11_E15_results.md.

**VERDICT: FAIL (clean).** Gate 2000-13 CAGR 6.36%/Sharpe 0.49; secondary
2.50%/0.25. PASS-HR fail (6.4% vs 15%); PASS-RA fail (Sharpe 0.49<0.80,
loses SPY in bull). Asymmetric framing (survivor+lookahead) makes the FAIL
clean.

**PATTERN (worth remembering):** E15 is the twin of E10 - both earnings
anomalies BEAT both benchmarks in the hostile 2000-13 decade (E15 6.36% &
Sharpe 0.49 while EW-universe -0.47%, SPY 1.72%) and both DECAYED after ~2010
(E15 2.5% vs SPY 12% post-2014). Textbook real-but-small-then-arbitraged
anomaly, twice. Not a live edge, but the cleanest positive-in-one-regime
signal the program has produced. Program 0/16 primary, 0/3 D1-tiered.

**Next action:** commit E15, then M7 task 31 (E16 x-sectional weekly reversal).

---

# Appendix BB - E16 weekly reversal FAIL (clean); cleared 15% return but blew DD ceiling on survivor flattery (2026-07-11, ~21:35 CST)

**WHAT:** M7 task 31. Ran E16 per prereg a090294 (doc-only first). Runner
run_e16_weekly_reversal.py; 39 survivor large-caps; swing.db untouched;
tripwire GREEN. Results: docs/research/2026-07-11_E16_results.md.

**VERDICT: FAIL (clean).** THE NOTABLE ONE: gate 2000-13 CAGR 16.76% -
first experiment in 16 to CLEAR the 15% return bar - but maxDD 65.9%
(breaches 60% ceiling) and Sharpe 0.61; secondary 10.68%/64%DD. PASS-HR
fails on drawdown + secondary; PASS-RA fails (Sharpe 0.61<0.80, loses SPY).

**WHY IT'S NOT A DISCOVERY:** reversal/dip-buying is the strategy MOST
flattered by survivorship - buying biggest losers only works if losers
recover, and these 39 are all still alive (no Lehman/Enron). The 16.76% is
the expected survivorship artifact, which is exactly why the prereg fixed
asymmetric framing (only FAIL clean) beforehand. It IS a FAIL (66% DD +
sub-0.80 Sharpe), so interpretable: even with maximal survivorship flattery
weekly reversal couldn't clear the risk-controlled bar. Fill-timing-ablation
counter-evidence also held (next-open long-only = lossy version). NOT tuned
(a DD-cutting stop would be tuning-a-FAIL; refused). Program 0/17 primary,
0/4 D1-tiered.

**Next action:** commit E16, then M7 task 32 (E17 days-to-cover) - which
STARTS with a short-interest history data probe; likely BLOCKED-ON-DATA.

---

# Appendix BC - E17 days-to-cover BLOCKED-ON-DATA; M7 catalog arc complete (2026-07-11, ~21:45 CST)

**WHAT:** M7 task 32 probe step (per PRD, no prereg - the probe gates it).
Free historical short interest for our EXCHANGE-LISTED universe over the
2000-2013 gate window does NOT exist: yfinance = snapshot only; FINRA free
data is OTC-only before June 2021 (archives from 2014, OTC), exchange-listed
history is paid-vendor only. Endpoint probe confirmed (FINRA otcMarket
dataset, 400 on AAPL/MSFT). Probe doc: docs/research/2026-07-11_E17_data_probe.md.

**VERDICT: BLOCKED-ON-DATA** - recorded and closed without a prereg, nothing
run/stubbed/fabricated (E10-probe pattern). Unblock = paid SI feed (Evan
budget decision) or a >=2021 forward window (too short; not adopted).

**M7 CATALOG ARC COMPLETE:** E13 turn-of-month FAIL, E14 sector momentum
FAIL (survivorship-clean, cleanest negative), E15 earnings premium FAIL
(clean; E10 twin), E16 weekly reversal FAIL (clean; cleared 15% return but
66% DD on survivor flattery), E17 BLOCKED. Program 0 PASS / 17 attempts
(16 run + 1 blocked) / 7 families.

**Next action:** natural stopping point - sync HANDOFF + README + memory to
0/17, commit, then continue roadmap into M7b (E18 regime-gate bake-off next;
data in hand).

---

# Appendix BD - E18 regime-gate bake-off: nothing beats 200DMA; VIX-TS is a weak first PASS-RA (2026-07-11, ~22:05 CST)

**WHAT:** M7b task 33. Ran E18 per prereg f32b008 (doc-only first). Runner
run_e18_regime_gates.py; QQQ/ETFs from cache, VIX/VIX3M via yfinance, HY-OAS
via FRED; swing.db untouched; tripwire GREEN. Results:
docs/research/2026-07-11_E18_results.md.

**BAKE-OFF VERDICT (primary question): NO new regime gate beats the plain
200-DMA overlay** on the robust criterion (maxDD cut>=10pp AND Sharpe>=BH
BOTH windows). Only gate (d) 200-DMA qualifies both windows - confirms
E6/E7: trend-timing is the robust overlay, VIX-TS/credit/breadth don't
improve on it across regimes.

**FIRST PASS-RA (reported per pre-registered D1, with heavy caveats):** the
VIX/VIX3M<1 gate cleared PASS-RA - gate(2006-13) Sharpe 0.80, >SPY both
windows, +CAGR both. BUT WEAK/FRAGILE: (1) 2006-13 window has only ONE crash
(2008; VIX3M starts 2006, misses dot-com) - the pass largely = dodging 2008;
(2) in 2014+ it had WORSE drawdown than buy-hold (44% vs 35.6%), whipsawing
the bull; secondary Sharpe 0.79 barely > SPY 0.74. Not robust, not a return
engine. Per D1 -> forward-paper candidate alongside E6-1x, nothing more.
NOT tuned. PASS-HR column still 0.

**DATA LIMIT:** HY-OAS arm INCONCLUSIVE - FRED fredgraph.csv returned
BAMLH0A0HYM2 only from ~2023 despite cosd=1996; no gate-window history.
Unblock = working FRED fetch/API key. Program now 1 weak PASS-RA / 18.

**Next action:** commit E18, then M7b task 35 (E20 dividend capture, cheap);
E19 insider/EDGAR is the heavy probe - attempt after E20.

---

# Appendix BE - E20 dividend capture FAIL (real but sub-scale + tax-eaten) (2026-07-11, ~22:25 CST)

**WHAT:** M7b task 35. Ran E20 per prereg d0642ad (doc-only first). Runner
run_e20_dividend_capture.py; 29 ETFs + yfinance dividends, dividend credited
to P&L; swing.db untouched; tripwire GREEN. Results:
docs/research/2026-07-11_E20_results.md.

**VERDICT: FAIL (both tiers).** Gate 2000-13 CAGR 0.62%/Sharpe 0.18;
secondary -1.15%. Mean net per-trade +0.10% (win 57.7%) - a REAL tiny
ex-date edge (drop ~10bps < dividend) but sub-scale: ~90 1-session trades/yr
barely touch capital, compound to 0.6%/yr and go NEGATIVE post-2014
(decayed). Pre-tax; dividends taxed as income would flip the +0.10% negative
(disclosed). Dividend capture closed. Program 0 PASS-HR / 1 weak PASS-RA /
19 attempts.

**Next action:** commit E20, then M7b task 34 (E19 insider/EDGAR) - the
heavy one; STARTS with a scoped Form-4 ingestion probe per PRD.

---

# Appendix BF - E19 EDGAR probe: FEASIBLE-BUT-DEFERRED; M7/M7b arcs complete; autonomous wall (2026-07-11, ~22:35 CST)

**WHAT:** M7b task 34 probe (per PRD, no prereg). SEC EDGAR Form-4 probe for
the 39-stock universe: 39/39 CIKs resolved, healthy recent Form-4 volume
(AAPL 42, JPM 132, WMT 215, GE 51/yr). BUT three hazards for a 2000-2013
build: (1) CIK changes over time (XOM's history is under a prior CIK -
current map misses it), (2) primaryDocument is the XSL/HTML render not raw
XML, (3) recent-submissions API caps ~1000 filings so historical years need
archive pagination (JPM has 25,342 filings). Probe doc:
docs/research/2026-07-11_E19_edgar_probe.md.

**VERDICT: FEASIBLE-BUT-DEFERRED (not blocked - data exists & parses).** Full
gate-window ingestion is the heaviest build in the project (hours, tens of
thousands of fetches + CIK-history + raw-XML hazards); E19 is
survivorship-flattered (asymmetric, only FAIL clean); base rate 0 PASS-HR/19.
Committing that effort autonomously for a near-certain interpretable-FAIL is
a poor trade -> deferred pending explicit Evan authorization or a vendor feed.

**M7 + M7b COMPLETE.** Catalog arc E13-E17 (4 FAIL + 1 blocked); data-type
arc E18 (weak PASS-RA, VIX-TS, forward-paper candidate only), E20 (FAIL),
E19 (deferred). **PROGRAM: 0 PASS-HR / 1 weak PASS-RA / 20 attempts /
7 families.** AUTONOMOUS WALL: remaining work is all Evan-gated (M3 Alpaca
paper deploy of E6-1x [+ the caveated VIX-TS candidate]; E19 full ingestion
authorization; a paid data budget to unblock HY-OAS/short-interest).

**Next action:** final HANDOFF + memory sync; then report the full session
+ pending push (~18 commits ahead) + the two Evan decisions. Nothing
autonomous remains.

---

# Appendix BG - Pushed M7/M7b arc to public repo (2026-07-11, ~20:26 CST)

**WHAT:** Evan authorized push. Shipping the M7+M7b batch (E13-E20 preregs +
runners + results, D1 approval, timezone correction, doc syncs) to
origin/main. State at push: 0 PASS-HR / 1 weak PASS-RA (VIX-TS, forward-paper
only) / 20 attempts / 7 families; autonomous wall (remaining work Evan-gated:
M3 Alpaca, E19 ingestion authorization, paid-data budget). Cadence #54.

---

# Appendix BH - E19 authorized + launched: EDGAR Form-4 ingestion running (2026-07-11, ~20:45 CST)

**WHAT:** Evan authorized the full E19 EDGAR build ("1"). Sized it first:
104,496 Form-4s across the 39 names (~4h fetch at 7/s), structured-XML floor
~2003 (gate window becomes 2003-2013), XOM/DIS need former-CIK map (XOM
0000034088, DIS 0001001039). Prereg ebf54a4 committed doc-only. Parser
validated on BAC samples (raw XML fetch OK, codes {M,D,P,S,J} extracted,
9 P-buys/8 samples). Ingester (scripts/ingest_edgar_form4.py, resumable
per-ticker cache, .edgar_cache gitignored) launched in BACKGROUND (task
benymlwy5). Backtest (scripts/run_e19_insider.py: CMP opportunistic
classification, 40-session hold, K=5, D1 + asymmetric verdict) written and
ready. Prior: near-certain FAIL (survivorship, 0-PASS-HR/19).

**STATE:** ingestion in progress (~4h); on completion -> run backtest ->
verdict -> results doc -> record -> commit. Nothing else autonomous until it
finishes. swing.db untouched; prices from .e8e9_cache.

**Next action:** await ingestion completion notification, then run E19.

---

# Appendix BI - E19 ingestion restarted (2026-07-12, ~15:27 CST)

**WHAT:** Evan paused the EDGAR ingestion (~20:45 CST 07-11, mid-MSFT, 0/39
tickers fully cached - cache is per-ticker-on-completion so nothing
persisted) then prompted restart now. Relaunching scripts/ingest_edgar_form4.py
in background; resumable (skips completed tickers, currently none -> starts at
MSFT). Same ~104k-doc / ~4h scope. On completion -> run_e19_insider.py ->
verdict -> results -> record -> commit. swing.db untouched. Cadence #57.

---

# Appendix BJ - E19 ingestion ~17% + research-brief on swing methods kicked off (2026-07-12, ~23:04 CST)

**WHAT:** Two threads. (1) E19 EDGAR ingestion (task b2wzwj9gb) healthy at
~17%: 6/39 tickers cached (MSFT 53 / INTC 92 / CSCO 14 / ORCL 35 / IBM 43 /
AAPL 22 P-buys), QCOM in progress. ~17.7k/104.5k docs fetched, ~7/s, no
throttle. ETA ~3h. Runs unattended; E19 backtest fires on INGEST COMPLETE.
(2) Evan requested a full in-depth /research-brief on every possible swing-
trading method. Launching that as a parallel deliverable (survey doc under
docs/research/, does NOT touch swing.db or the ingestion). Scope: catalog +
mechanism + evidence + testability for the full method space, superset of the
2026-07-10 catalog and 2026-07-12 data-type briefs. Cadence #60 (soft cadence,
on time).

**STATE:** ingestion 17% and climbing; research-brief in progress. swing.db
untouched. No new backtests started (autonomous wall holds - this is research
output, not a strategy run).

**Next action:** produce the research brief; keep E19 ingestion running to
completion, then run E19.

---

# Appendix BK - Full swing-method survey delivered (research-brief, 2026-07-12, ~23:25 CST)

**WHAT:** Ran /research-brief on "every possible swing-trading method" as a
superset of the 2026-07-10 catalog. 8 parallel research agents (one per family:
mean-reversion, trend/momentum, chart-pattern TA, event/catalyst, seasonality/
overnight, sentiment/flow/alt-data, volatility/options, factor/ML), primary-
source-graded (~90 methods). Compiled to
docs/research/2026-07-12_swing_method_full_survey.md. Web-research only - no
backtests, swing.db untouched, E19 ingestion (b2wzwj9gb) unaffected.

**KEY RESULT:** the reconciliation layer is the payload. Agents flagged several
"untested" ideas that the project ALREADY KILLED: diversified sector momentum
(E14 FAIL 2.4%), turn-of-month (E13 FAIL 1.4%), earnings-announcement premium
(E15 FAIL 6.4%), raw weekly reversal (E16 FAIL - 16.76% gate CAGR but 65.9%
DD), dividend capture (E20 FAIL). After reconciliation only a short list is
genuinely open, all with strong-FAIL priors: (1) short-term RESIDUAL reversal
(Blitz 2013, the fix for E16's DD), (2) dividend-INITIATION drift (distinct
from E20 capture), (3) one consolidated volatility-breakout kill-shot,
(4) Moreira-Muir vol-targeting sizing overlay, (5) free Reg SHO daily short-
volume drift, (6) even-week FOMC-cycle overlay, (7) SVXY carry gated by VIX-TS.
Structural conclusion (4 independent literatures): concentration to K=1-3
destroys diversified-decile edges; edges live in illiquid names the floor
excludes (Hou-Xue-Zhang 65-82% fail VW; Avramov-Cheng-Metzker; McLean-Pontiff
26-58% decay). The 0-for-20 record is what an honest retail-EOD program should
produce. Null H0 (residual space = overlays + kill-shots, not high-return
engines) survives; strong H1 rejected.

**STATE:** brief committed-pending; E19 ingestion ~7/39 tickers (QCOM in
progress), healthy. Cadence #60 (record done). Nothing else autonomous until
ingestion completes -> run E19.

**Next action:** commit the brief; await ingestion completion; run E19.

---

# Appendix BL - PRD_ROADMAP synced to actual outcomes; M8 added (2026-07-12, ~23:35 CST)

**WHAT:** Evan: "commit this, then update the PRD and ROADMAP." (1) Committed
the survey deliverable (docs/research/2026-07-12_swing_method_full_survey.md
+ HANDOFF + record + pm-cadence) as `8cc7c68`. (2) PRD_ROADMAP.md had not
been synced since the M7/M7b tasks were written 2026-07-10/07-12 - the task
breakdown still read as pending even though E13-E20 had all run. Per the
established convention (task 13's "*(Outcome ...)*" pattern for E1), appended
outcome annotations to tasks 28-35 (E13 FAIL, E14 FAIL, E15 FAIL, E16 FAIL,
E17 BLOCKED-ON-DATA, E18 weak PASS-RA, E19 RUNNING/pending, E20 FAIL), closed
out M7/M7b exit-condition text with actual results, and flagged E19 as "the
one still-running experiment in the whole PRD." Added milestone M8 (tasks
36-42): the 7 residual candidates (C1-C7) from today's full-method survey -
residual reversal, dividend-initiation drift, one volatility-breakout
kill-shot, vol-targeting overlay, Reg SHO short-volume drift, even-week FOMC
overlay, SVXY carry - each with mechanism, disclosed counter-evidence, data
status, and build cost; explicitly framed as lower-expected-value than
M7/M7b per the survey's own structural finding, queued AFTER E19 closes.
Milestones table (section 5) updated with DONE/RUNNING markers per the M2d
row convention. No task text rewritten/deleted - pure ADD-by-appending per
project rules. Frozen tripwire re-run post-edit: GREEN (12/12 refs,
d=+/-0.0000pp) - confirms the doc-only change touched no code.

**STATE:** E19 ingestion (b2wzwj9gb) still running, ~6-7/39 tickers cached,
healthy. PRD_ROADMAP.md now accurately reflects 0 PASS-HR / 1 weak PASS-RA /
20 attempts / 7 families, with M8 queued as the next milestone once E19
closes. Cadence #63 folded into this entry.

**Next action:** commit PRD_ROADMAP.md; await E19 ingestion completion, then
run scripts/run_e19_insider.py -> verdict -> results -> record -> commit ->
close M7b -> M8 becomes the default next-open-task per PRD cadence.

---

# Appendix BM - E19 ingestion ~27/39; armed to run E19 on completion (2026-07-13, ~11:41 CST)

**WHAT:** Evan: "Wait for ingestion to finish, then run E19." E19 EDGAR
Form-4 ingestion (task b2wzwj9gb) is healthy at 27/39 tickers cached (JNJ in
progress; remaining: PFE MRK ABT UNH GE CAT BA MMM HON T VZ). Both former-CIK
names resolved: XOM cached; DIS merged current CIK 0001744489 + former
0001001039 (22 P-buys). P-buy counts sane (HD 69, NKE 41, MCD 39, IBM 43).
No throttle stalls. On INGEST COMPLETE -> run scripts/run_e19_insider.py
(opportunistic-buy drift, CMP classification, 40-session hold, K=5, gate
2003-2013, D1 dual-bar + asymmetric survivorship framing) -> frozen tripwire
must stay GREEN -> results doc docs/research/2026-07-13_E19_results.md ->
record entry -> commit. Prior per prereg ebf54a4: near-certain FAIL
(survivorship-flattered, 0-PASS-HR/20 base rate); a FAIL closes the insider
idea cleanly, a PASS routes to forward paper only (uninterpretable).
Cadence #66.

**STATE:** ingestion running (harness-tracked, will notify on completion -
no polling). swing.db untouched; prices from .e8e9_cache. Nothing else
autonomous until E19 closes.

**Next action:** on ingestion completion, run E19 and close M7b.

---

# Appendix BN - LLM-driven strategy survey delivered (research-brief, 2026-07-13, ~12:15 CST)

**WHAT:** Evan asked (in parallel with the E19 wait) for a /research-brief on
LLM-driven swing-trading paths — "LLM making human-like decisions biased off
stock trends," incl. ideas needing a live-platform connection or more compute,
"as many as possible." 7 parallel agents (analyst / agentic / price-trend /
overlay / feature-factor / macro-regime / pitfalls-infra), ~90 named idea
variants, skeptical evidence grading. Compiled to
docs/research/2026-07-13_llm_driven_strategies.md. Web-research only; no
backtests; swing.db + E19 ingestion (b2wzwj9gb) untouched.

**KEY RESULT:** H1 (LLM = real high-return engine) REJECTED; null H0 (published
LLM alpha is look-ahead-contaminated + illiquid-concentrated + decaying; best
use = a treatment overlay vs a mechanical control, provable only at a
pre-registered N) SURVIVES every family. Four anchors: (1) re-testing the
multi-agent showcases (FinMem/TradingAgents/FinAgent/FinCon) post-training-
cutoff decays returns 50-72%, most fail to beat buy-hold (Profit Mirage 2025;
StockBench 2026); (2) LLMs weak at the literal ask — chart-reading VLMs 49-53%
(chance), best TS foundation models beat random-walk 2/10 tasks — collides with
the project's chart-TA-dies prior; (3) the real residual edge (Lopez-Lira) is
small, decays with adoption, and lives in small/negative-news names the
liquidity floor excludes; (4) LLM non-determinism structurally conflicts with
the frozen tripwire, with ONE clean fix — pin the tripwire on the deterministic
replay of an immutable overlay_log, never on the model call (exactly the
e1_llm_veto design). Ranked 8-item shortlist all at Tier 0/1 (no API key):
E4 LLM offline hypothesis-generator (cleanest fit), D3 triple-barrier
meta-labeler, D2/D16 confidence-sizer, D6 exit-supervisor, A7 LLM-surprise PEAD
overlay, F11/C9 regime-gate vs E18 baseline, B9/B14 red-team/consensus veto,
E11 weak-label→distilled classifier. Non-negotiable gates: strictly-post-cutoff
eval, ticker anonymization, LAP/placebo audit, decision-log tripwire, LLM as
treatment vs e1_control. Extends the 2026-07-12 survey's wall: LLM paths don't
escape it and ADD two failure modes (contamination + non-determinism); ceiling
= risk-adjusted overlay, same tier as E18's weak PASS-RA. Tally UNCHANGED
(research, not a run): 0 PASS-HR / 1 weak PASS-RA / 20 attempts.

**STATE:** brief committed-pending; E19 ingestion ~28/39 (PFE in progress),
healthy. No new backtests started (autonomous wall holds). swing.db untouched.

**Next action:** commit the LLM brief; await E19 ingestion completion, then run
E19 and close M7b.

---

# Appendix BO - Four-topic research batch delivered (execution / risk / data / crypto, 2026-07-13, ~13:05 CST)

**WHAT:** Evan: "continue with another set of research using /research-brief" ->
asked which direction (execution / risk-sizing / alt-data / crypto) -> "do all."
Ran 4 research briefs, 16 parallel agents (4/topic), ~64 findings, skeptically
graded, mapped to constraints + prior kills. Deliverables:
docs/research/2026-07-13_{execution_microstructure, risk_and_sizing, data_sources,
crypto_feasibility}.md. Web-research only; no backtests; swing.db + E19 ingestion
(b2wzwj9gb) untouched.

**KEY RESULTS per topic:**
- EXECUTION: 0-for-20 is GENUINE no-edge not execution artifact (project already
  fills next-open + 5bps, surrendering the one-directional fake-alpha bias;
  Chen-Velikov: ~93% of anomaly gross alpha dies under costs = the base rate).
  Overnight gap CONFIRMED structural (NightShares ETF failed + liquidated 14mo; NY
  Fed drift flat since 2021). ONE honest experiment left = a market-on-close (MOC)
  entry variant (needs a frozen 15:50-snapshot signal to avoid look-ahead). Gave a
  3-rung decomposition ladder (frictionless -> next-open-0bps -> next-open+5bps) to
  settle execution-vs-signal per FAIL. 5bps fair-to-conservative (tier it). CORRECTION
  surfaced: Alpaca fractional is NOT market-only since Mar-2024 -> supports
  market/limit/stop, TIF=DAY, no fractional short (update HANDOFF/PRD note).
- RISK/SIZING: at K=1-3 sizing IS the whole risk game -> capped fractional-Kelly
  (1/4-1/2) never full (full-Kelly on a noisy edge is strictly dominated). Time-stop
  (vertical barrier) is the robust exit backbone; tight price stops mostly hurt
  (Kaminski-Lo) + DAY-TIF makes gap protection a SIZING not a stop problem. Only
  conditional-vol-targeting (condition E6xE18 on each other) plausibly beats a lone
  gate, but effective-N (~3-5 crises) means NO regime rule can be validated on
  history -> forward-paper only. Deployable E6∩E18 sleeve = drawdown-reduction (=SPY
  return, lower DD), NOT high-return; its slow signal means a forward test can prove
  IMPLEMENTATION FIDELITY not statistical edge (reframe the success criterion).
- DATA: E17 wall PARTLY GONE - FINRA free exchange-listed short interest exists from
  June-2021 -> E17 runnable FREE now (2021-2026 OOS). Free Reg SHO daily short-volume
  (2009+) = a BJZ-lineage drift test. Cheapest event test = analyst recommendation-
  CHANGE drift via FMP Starter ($22, event-dated = no PIT trap). Strongest short-side
  edge = loan-fee anomaly (4.01%/mo) via Ortex Advanced (~$129). Muravyev-Pearson-
  Pollet 2025: option skew signals are ~2/3 a borrow-fee proxy -> die on liquid names.
  Exotic alt-data = institutional-only (one satellite study documents RETAIL as the
  harvested counterparty). Escalation path = a university WRDS login (free, unblocks
  I/B/E/S + Compustat PIT).
- CRYPTO: 24/7 RELOCATES-friction, does NOT dissolve the killer - closure IS what
  manufactures the gap-reversal edge, so a continuous market never generates it; the
  jump reappears as intraday liquidation cascades. ONE clean win: liquid BTC/ETH
  bar-based bot has zero gap by construction + the prereg/tripwire ethos transfers
  (Alpaca crypto paper). Recommend YES to a scoped paper-first liquid-only trend/
  momentum pilot (Liu-Tsyvinski + Grayscale), BUT pre-register CRYPTO fees (25bps/side
  Alpaca taker = 5x the 5bps model); custody (100% capital uninsured on-exchange) is
  the deciding risk with no equity analog.

CROSS-CUT: all four confirm the same wall - the high-return cell stays empty; the
value is DISCIPLINE (honest cost model + decomposition ladder + capped-Kelly + a
faithful forward-paper protocol) and a short list of cheap/free next tests (MOC entry,
E17-2021+ free, Reg SHO, FMP recommendation drift, a crypto trend pilot). Tally
UNCHANGED (research, not runs): 0 PASS-HR / 1 weak PASS-RA / 20 attempts.

**STATE:** 4 briefs committed-pending; E19 ingestion ~29/39 (MRK in progress),
healthy. No backtests started. swing.db untouched.

**Next action:** commit the 4 briefs; await E19 ingestion completion, then run E19
and close M7b.

---

# Appendix BP - M9 added to PRD: research-batch-2 experiments designed (2026-07-13, ~13:25 CST)

**WHAT:** Evan: "update the roadmap and design experiments for the new possible
strategies." Appended milestone M9 (tasks 43-51) to PRD_ROADMAP.md + milestones-table
row, per the ADD-by-appending rule. Contents:
- Task 43 discipline adoptions (prereg template: tiered costs 1/5/15-25bps +
  ADV>=$5M/price>=$5 floor, decomposition ladder in every results doc, time-stop
  baseline arm, capped fractional-Kelly defaults).
- Task 44 EX-DECOMP diagnostic (Rungs A/B/C retrofit on E13-E16/E20 FAILs ->
  classify SIGNAL-DEAD / GAP-DWELLER / COST-GATED).
- X-candidates: X1 conditional vol-targeting (E6xE18 interaction, gate 2006-2013,
  PASS-RA ceiling, verdict labeled descriptive per low-N), X2 E17-free days-to-cover
  (FINRA official SI 2021+, publication-date honesty), X3 Reg SHO short-volume drift
  (2009+, MM-hedging contamination disclosed), X4 MOC close-entry probe (CLS
  availability conflict between agents -> probe first; forward-paper arm; M3-adjacent),
  X5 analyst recommendation-change drift (BLOCKED-ON-EVAN $22 FMP), X6 crypto BTC/ETH
  20d/100d trend pilot (BLOCKED-ON-EVAN scope; 25bps/side crypto fees; gate 2018-2022
  = two bears; must beat HODL Sharpe), task 51 LLM forward-only arc + M3 amendment
  (pinned model ID, decision-log tripwire, trend-blind ablation, fidelity-reframed
  forward-paper criterion per RK4).
- TWO NEW DESIGN RULES adopted for M9: (1) modified-window rule — short-window data
  (2021+/2009+/crypto) cannot claim PASS-HR/RA; best verdict = "PROMISING - needs
  forward confirmation"; only full-window experiments claim D1 tiers. (2) LLM
  overlays are forward-only (training-cutoff look-ahead makes LLM backtests
  uninterpretable) — never M9 backtests.
Ordering: 43-45 data-in-hand (may interleave with M8 cheapest-first), 46-47 free
downloads, 48-51 gated. All after E19 closes. Cadence #72 was satisfied by BO; this
entry logs prompt ~#73's work.

**STATE:** PRD updated (uncommitted); E19 ingestion ~30/39 running. No backtests
started; swing.db untouched.

**Next action:** commit the M9 roadmap update on Evan's word; await E19 completion ->
run E19 -> close M7b -> M8/M9 become the open queue.

---

# Appendix BQ - E19 ingestion ~31/39; ABT P-buy anomaly flagged (2026-07-13, ~13:40 CST)

**WHAT:** M9 committed (f66a9d6). E19 EDGAR ingestion (b2wzwj9gb) at 31/39, UNH in
progress; 7 left (GE CAT BA MMM HON T VZ). DATA ANOMALY to carry into the E19 results
doc: ABT cached **388 P-buys** vs a typical name's 10-90 (HD 69, PFE 52, MSFT 53).
388 open-market "P" transactions on one large-cap over ~20yr is implausibly high for
discretionary insider buying - almost certainly dividend-reinvestment-plan / ESPP /
automatic-accumulation purchases mis-coded as transactionCode "P". The CMP routine-vs-
opportunistic classifier SHOULD absorb most of these (regular monthly/quarterly DRIP
buys are the definition of "routine" - same calendar month each year -> classified
routine -> excluded from the opportunistic set E19 trades). But it must be VERIFIED in
the results doc: report per-ticker opportunistic counts, and if ABT (or any name)
dominates the opportunistic set with mechanical-looking cadence, hand-inspect and note
it. This is exactly the kind of survivorship/data-quality artifact the asymmetric
framing anticipates - it can only inflate a spurious PASS, so it strengthens a clean
FAIL. Cadence #75.

**STATE:** ingestion 31/39, healthy; swing.db untouched; no backtests started.

**Next action:** await INGEST COMPLETE -> run run_e19_insider.py (verify opportunistic
counts per ticker, watch ABT) -> D1 verdict -> tripwire -> results doc -> record ->
commit -> close M7b.

---

# Appendix BR - E19 RUN: FAIL (clean, robust to de-junk); M7b CLOSED (2026-07-13, ~13:45 CST)

**WHAT:** EDGAR ingestion completed (task b2wzwj9gb, exit 0, 39/39 tickers, INGEST
COMPLETE; VZ was the 7,669-Form-4 tail). Ran `scripts/run_e19_insider.py` (via
`.venv` python - pythoncore-3.14 lacks yfinance). **E19 = FAIL per D1 prereg
`ebf54a4`.** Numbers: P-buys 6435; opportunistic 6138; entries 6138; gate entries
279. Gate 2003-2013 CAGR 4.68% / maxDD 53.6% / Sharpe 0.31; secondary 2014- CAGR
4.91% / maxDD 42.6% / Sharpe 0.35. **Underperforms SPY buy-hold on BOTH CAGR and
Sharpe in BOTH windows** (SPY 6.65%/0.42 and 11.98%/0.74). PASS-HR fail (needs >=15%),
PASS-RA fail (gate Sharpe 0.31 < 0.80). Frozen tripwire GREEN afterward (12 refs,
d=+/-0.0000pp). Full writeup: `docs/research/2026-07-13_E19_insider_results.md`.

**DATA-QUALITY (carries + CORRECTS Appendix BQ):** the P-buy set is contaminated far
beyond the ABT flag. BAC = **2851 P-buys (44% of all 6435)**, dominated by owner CIK
0000070858 which is **BAC's own ISSUER CIK** (not an insider), including **1-share
lots at $0.01-0.02** (impossible as real open-market buys - DRIP/fractional/accounting
artifacts mis-coded transactionCode "P"). GS 728, ABT 388, JPM 353, GE 310 similar.
**BQ's prediction that the CMP classifier would absorb these as "routine" is
FALSIFIED** - 95% (6138/6435) passed through as opportunistic. **BQ's claim that
contamination "can only inflate a spurious PASS" is imprecise** - signal-free buys
dilute TOWARD beta, which is bidirectional and could equally MASK a real edge (the
genuine threat to a FAIL).

**SENSITIVITY (post-hoc, NOT prereg; scratch script, uncommitted):** re-ran the cache
with de-junk filters to resolve the masking risk. price>=$1 -> FAIL (4.66%/4.96%);
price>=$1 + same-owner/day dedup (entries 6119->2675) -> FAIL (4.54%/4.91%);
price>=$5 + dedup -> FAIL (3.66%/4.67%). Every variant stays flat sub-beta (gate
Sharpe 0.27-0.31); gate entries stable ~279 because a K=5/40-session book SATURATES.
**Cleaning reveals no masked edge -> the FAIL is ROBUST, a clean falsification, not a
contamination artifact.** Per doctrine any flip here would have been "PROMISING /
fresh-prereg-required," never a PASS - moot, nothing flipped.

**INTERPRETATION:** consistent with the program's structural null - K-concentrated,
liquidity-floored, survivor-universe versions of diversified anomalies collapse to a
slightly-worse-than-market long-only sleeve; the documented insider-buy alpha
(Cohen-Malloy-Pomorski, Lakonishok-Lee) lives in small/illiquid names the floor
excludes, and next-open EOD surrenders the announcement pop. Survivorship could only
help; contamination could only have hurt (ruled out) - clean in both directions.

**SNAPSHOT / TALLY:** **0 PASS-HR / 1 weak PASS-RA / 21 attempts / 8 families**
(E19 = insider-transaction / informed-positioning, the 8th family; the never-run E17
short-interest probe would sit in the same family). **M7b CLOSED** (E18 done, E20
done, E19 done). All families the research has surfaced are now falsified or
Evan-gated. Autonomous wall stands: remaining work = M3 Alpaca paper deploy (E6-1x
[+ caveated VIX-TS]); M8/M9 experiments that are BLOCKED-ON-EVAN (paid data budgets
X2/X3/X5, crypto scope X6) or startable-but-low-value; all require Evan's go.

**STATE:** swing.db untouched (E19 reads .edgar_cache + price caches only, no writes);
tripwire GREEN; working tree = new results doc + this record entry + HANDOFF/memory
sync, about to commit. Cadence #77.

**Next action:** commit E19 (results doc + record + HANDOFF + memory). Then the open
queue is M8/M9, all Evan-gated - report the autonomous wall and await Evan's
direction (deploy, fund a data probe, or accept the falsification program as the
deliverable).

---

# Appendix BR-note - CORRECTION to BR's "autonomous wall" claim (2026-07-13, ~13:55 CST)

**Correcting my own error in BR above (append-only: not editing BR).** BR states
"Autonomous wall stands ... M8/M9 ... BLOCKED-ON-EVAN (paid data budgets X2/X3/X5 ...);
all require Evan's go." **That is wrong on two counts** (verified against PRD lines
687-689):
1. **X2 and X3 are FREE, not paid.** X2 = FINRA exchange-listed consolidated short
   interest (free, 2021+); X3 = Reg SHO daily short-volume (free, 2009+). Only X5
   (FMP $22), X6 (crypto fees), and the borrow-fee probe (Ortex ~$129) are paid.
2. **There is no hard autonomous wall anymore.** The 2026-07-11 wall was real (only
   M3 + paid data remained); but the 2026-07-12 survey + the M8 (C1-C7) and M9
   (43-47) tasks I authored REOPENED a queue of free / data-in-hand experiments that
   need neither money nor an Alpaca account: M9 43 (prereg-template), 44 (EX-DECOMP
   retrofit), 45/X1 (vol-targeting), 46/X2, 47/X3, plus M8 C1-C7 (data-probe-gated).
   Genuinely Evan-gated: M3 deploy, X5/X6/borrow-fee (money), X4-MOC + LLM arc
   (intraday data / M3-live; EOD-only rule blocks MOC).

Per the PRD execute-next-task loop the correct default idle action is now the
cheapest open free task (M9 #43, doc-only prereg-template), NOT "stop at a wall."
Expected value is low (survey reconciliation gives every residual a strong-FAIL
prior), so I am surfacing the choice to Evan rather than auto-running - but the
honest framing is "low-value free queue exists," not "blocked." Cadence #77 (same
unit as BR).

---

# Appendix BS - EX-DECOMP (M9 #44): closed FAILs decomposed; only E14 signal-dead (2026-07-13, ~21:50 CST)

**WHAT:** Evan picked option 1 (EX-DECOMP). Ran the execution/signal decomposition
ladder on the five closed FAILs with in-repo runners (E13/E14/E15/E16/E20). Three
rungs: A = frictionless close-to-close 0bps (raw signal); B = next-open 0bps (removes
overnight gap); C = next-open 5bps (as-run). Runner: `scripts/run_ex_decomp.py`;
writeup `docs/research/2026-07-13_EX-DECOMP_results.md`. Diagnostic only - no D1
verdict, no tuning, tally UNCHANGED.

**IMPLEMENTATION (surgical):** got Rung A WITHOUT editing any runner's execution
logic - wrapped the price feed so each bar's open := prior close, turning "fill at
next open" into "fill at signal-day close" = c2c. B/C differ only by COST
(monkeypatched to 0 for A/B). Benchmarks read closes -> identical across rungs. Each
runner (E13/E14/E15/E16) got ONE additive `return {rows,n_gate,bench}` tagged
"EX-DECOMP hook (M9 #44)"; __main__ ignores it, behavior unchanged. E20 (entry is
already a close -> transform degenerates) computed directly from its per-trade
formula reusing divs(). Null per strategy = its honest baseline: SPY-BH (E13),
EW-sectors (E14), EW-survivor-univ (E15/E16), absolute per-trade sign (E20).

**REGRESSION GREEN:** Rung C reproduces recorded FAILs exactly - E13 gate 1.41%
(rec 1.40%), E16 gate 16.76% (rec 16.76%), E20 full-sample mean-net = weighted
gate/sec (+24.5bps*1067 + -5.0bps*1151)/2218 = +9.2bps ~= recorded +0.10%/trade.
Frozen tripwire GREEN (12 refs d=0) after the additive edits.

**RESULT (PRD expected "most SIGNAL-DEAD" - WRONG, only E14 is):**
- E13 turn-of-month = **COST-GATED**: A 3.40% > SPY 1.72%, B 2.64% > 1.72%, C 1.41% <
  1.72% -> real gross calendar edge, killed only by turnover cost (-1.23pp). Not "matched
  SPY by luck."
- E14 sector-momentum = **SIGNAL-DEAD**: A 4.06% < EW-sectors 4.13% -> no alpha even
  frictionless. The cleanest true negative.
- E15 earnings-premium = **SURVIVES-NULL gate, decays OOS**: gate C 6.36% > EW-univ
  -0.47% (real gate alpha; A->B GAINS +2.45pp, run-up is overnight-gap-loaded), but
  sec C 2.50% < null 13.97% -> real-but-decayed.
- E16 weekly-reversal = **SURVIVES-NULL gate (SURVIVORSHIP), fails null OOS**: gate A
  27.97% is the survivorship artifact (buy biggest 5d losers on survivors we know
  recovered); decomposition can't launder it, and sec C 10.68% < null 13.97% confirms.
  Heavy weekly-turnover cost -6.25pp + gap -4.96pp gate.
- E20 dividend-capture = **REAL-BUT-SUBSCALE, gap-loaded**: B(open) +34.5bps >> A(c2c)
  +16.9bps -> the ex-date deficiency is an OVERNIGHT effect that reverts by close;
  survives cost in gate (+24.5bps) but negative post-2014 (-5.0bps); too small to
  compound (0.62% CAGR); pre-tax.

**PAYLOAD:** two recurring killers (overnight GAP A->B, and COST/turnover B->C), not
one flat "no signal." Momentum/timing (E13,E16) LOSE to the gap; MR/event overnight
trades (E15,E20) GAIN from it then pay it back in cost. Cost scales with turnover and
is decisive (Chen-Velikov ~93%-die mechanism observed in-repo). Terminal statement
UPGRADES: "real gross structure exists in 4 of 5, but converts to zero deployable
high-return edge once passed through gap + cost + OOS decay" is stronger + more honest
than "no signal anywhere." Reconfirms E6-1x (low-turnover overlay) as the only sane M3
deploy candidate; the gap is uncapturable at EOD.

**STATE:** swing.db untouched; tripwire GREEN; edited E13/E14/E15/E16 (additive returns
only) + new run_ex_decomp.py + results doc + this entry, about to commit. M9 #44 DONE;
#43 (prereg-template) still open. Cadence #78.

**Next action:** commit EX-DECOMP; then M9 #43 (prereg-template, doc-only, free) is the
next cheapest open task, or Evan redirects (deploy / free signal queue X1-X3 / stop).

---

# Appendix BT - M9 #43 prereg-template adopted + X2/X3 data probe launched (2026-07-13, ~22:20 CST)

**WHAT:** Evan said "do 1 and 2 in parallel" (option 1 = X2/X3 free short-side
experiments; option 2 = M9 #43 prereg-template). Parallelized: (a) wrote #43
`docs/prereg_TEMPLATE.md` inline; (b) spawned a background scout agent to nail the
exact FINRA data-access mechanics for X2/X3 before building an ingester.

**#43 DONE (doc-only):** `docs/prereg_TEMPLATE.md` is now the standing template every
future prereg copies, modeled on the E19 prereg house format. Folds the M9 research-
batch discipline into fixed [STANDING] sections: tiered cost model (1bp broad ETF /
5bp single-stock+sector / 15-25bp-or-exclude below floor / 25bp crypto + a 15bp stress
leg), liquidity floor formalized (ADV>=$5M AND price>=$5), decomposition-ladder
required in every results doc (Rung A/B/C, the EX-DECOMP method), time-stop baseline
arm (price-stops must beat it), capped fractional-Kelly sizing (lambda<=1/2, r=1-2%,
anti-martingale, no leverage), plus the existing standing rules baked in: D1 dual-bar
verdict, asymmetric framing for survivor universes, prereg-before-code committed hash,
frozen-tripwire-GREEN done-check, the modified-window cap (short-window data ->
"PROMISING" max, never PASS-HR/RA), and LLM-overlays-forward-only. Done-check: template
committed; next prereg copies it.

**X2/X3 PROBE (in flight):** background agent (general-purpose) scouting exact fetch
recipes for Dataset A = FINRA Reg SHO daily short-sale VOLUME (~2009+, deep, daily,
executed-short-volume = MM-hedging-contaminated, per-day CDN files) and Dataset B =
FINRA consolidated exchange-listed short INTEREST (2021+, biweekly, the real
days-to-cover input) - specifically whether B is direct-HTTP/API downloadable or
portal/auth-gated (the make-or-break for an unattended ingester). On its return: build
the probe (fetch+parse+coverage on the 39-name universe), then prereg via the new
TEMPLATE + run, or record BLOCKED-ON-DATA. Per the modified-window rule, X2 (2021+) and
X3 (2009+) can at best reach "PROMISING," not PASS-HR/RA.

**STATE:** swing.db untouched; tripwire GREEN (unchanged since EX-DECOMP); working tree
= prereg_TEMPLATE.md + this entry + PRD #43 outcome, about to commit #43. X2/X3
pending the scout. Cadence #79.

**Next action:** commit #43; await scout; build X2/X3 probe -> prereg(TEMPLATE)+run or
BLOCKED-ON-DATA.

---

# Appendix BU - FINRA access VERIFIED; X2 days-to-cover = FAIL (short-side anomaly REAL but non-deployable); X3 feasible-deferred (2026-07-13, ~23:15 CST)

**FINRA ACCESS (scout, both datasets green, no auth):** (A) Reg SHO daily short-VOLUME
- open CDN `cdn.finra.org/equity/regsho/daily/CNMSshvol{YYYYMMDD}.txt` (consolidated
2018-08+; per-venue FNYX/FNSQ/FNRA sum for 2009-08+); pipe-delimited, trailer line =
record count, schema changed 2011-02-28, volumes now fractional; it is EXECUTED short
FLOW (MM-hedging-contaminated), noisy. (B) Consolidated short INTEREST - public REST
`POST api.finra.org/data/group/otcMarket/name/consolidatedShortInterest` (Accept:
text/plain -> CSV), partitions endpoint enumerates settlement dates, history to
2017-12-29 (not just 2021!), daysToCoverQuantity PRECOMPUTED, 5000-row cap so filter
to symbols. Both FEASIBLE for an unattended ingester.

**X2 BUILT + RUN (the data-unblocked E17):** ingester
`scripts/ingest_finra_short_interest.py` (205 biweekly settlement dates 2017-12-29..
2026-06-30, 39/39 coverage; .finra_cache gitignored; CSV parse bug fixed - issueName
has commas -> used csv.DictReader). Prereg `prereg_x2_days_to_cover.md` committed
doc-only 4094889 BEFORE the runner (first prereg using the new TEMPLATE). Runner
`scripts/run_x2_days_to_cover.py`. Window 2018-01-16..2026-07-10, 2132 sessions, 204
cycles, K=5, entry 10 sessions after settlement (dissemination-lag lookahead guard).

**VERDICT: FAIL (deployable long-only leg), per prereg PROMISING-cap.** Long-only
lowest-DTC C(next-open+5bps) = 13.32% CAGR / DD 34.9% / Sharpe 0.60; beats SPY on CAGR
(12.53%) + EW-39 (9.59%) but LOSES Sharpe to SPY (0.60 < 0.71) -> fails the
pre-committed "CAGR AND Sharpe vs BOTH" bar. Decomposition ladder: A c2c 15.93% -> B
next-open 16.07% (gap FLAT - not a gap-dweller) -> C 13.32% (-2.75pp pure turnover
cost); 15bps stress collapses to 8.01%. Tripwire GREEN.

**THE PAYLOAD (honest + notable):** the short-interest anomaly is REAL, correctly
signed, and STRONG on the modern liquid large-cap tape - long-short SPREAD +18.39%
CAGR / Sharpe 0.98 / DD 26%, decomposing into low-DTC +15.77% vs HIGH-DTC -2.63% (the
most-shorted mega-caps underperformed SPY by ~15pp/yr). This is Boehmer-Huszar-Jordan /
Asquith-Pathak-Ritter ALIVE - the first strong correctly-signed anomaly the program has
surfaced. BUT the alpha is ENTIRELY on the SHORT (high-DTC) leg = NON-DEPLOYABLE (no
fractional shorting at $100-1,000; long-only can't convert a short leg's -15pp into
profit; the deployable long leg is exactly the one that FAILED). Survivorship works
AGAINST the short leg (delisted shorted-crashers excluded) -> the -2.63% is a LOWER
bound, strengthening "real." This is EXACTLY what the prereg predicted a priori ("long
leg tests the weak side; alpha is on the short leg, not deployable") - clean
falsification + validated reasoning. Writeup
`docs/research/2026-07-13_X2_days_to_cover_results.md`.

**X3 (Reg SHO short-volume drift) = FEASIBLE-DEFERRED:** access proven (CDN daily
files), but it's noisy executed-flow (not short interest), needs a heavier build
(per-venue summing + 2011 schema break + ~4300 daily files) and a separate signal. Not
run this sitting (scoped X2 = the clean canonical signal first). Data access is
recorded; X3 is a future free task, NOT blocked.

**TALLY:** X2 does not add a family (short-interest = the informed-positioning family,
same as E19; the E17 concept finally run). **0 PASS-HR / 1 weak PASS-RA / 22 attempts /
8 families.** PASS-HR stays 0 (X2 deployable FAIL; the spread is PROMISING-capped +
non-deployable, not a PASS). Notable: the program's strongest real anomaly is one it
structurally cannot trade.

**STATE:** swing.db untouched; tripwire GREEN; committed #43 (e8548dd) + X2 prereg/
ingester (4094889); about to commit X2 runner + results + this entry + PRD/HANDOFF/
memory. Cadence #79 (cont.).

**Next action:** commit X2; then open free queue = X3 (Reg SHO, feasible), X1
(vol-targeting), or Evan redirects (the short-side finding is an Evan-gated
capital/scope question - shorting needs a bigger account).

---

# Appendix BV - "do 1" = pursue short-side; INTERPRETATION + X2b design (2026-07-13, ~23:45 CST)

**Evan said "do 1"** (pursue the short-side, the X2 finding). **INTERPRETATION +
BOUNDARY (stated to Evan):** I read this as *rigorously test whether the short-side
edge is real + robust enough to justify sizing up* - NOT "open a margin/shorting
account or place short trades" (prohibited / Evan-only; I can't execute it, and
nothing goes live without Evan + an Alpaca account). The actionable engineering =
a properly-costed, pre-registered SHORT / LONG-SHORT experiment (X2b) that turns
X2's 0-cost existence spread into a realistically-executed strategy and answers the
deployability question honestly.

**KEY RIGOR POINT driving the design:** the X2 spread (+18.39%) used 0 cost + daily
c2c. A real short strategy pays (a) 5bps trading, (b) BORROW FEES on the short
notional. Muravyev-Pearson-Pollet 2025: short-side predictability is largely a
BORROW-FEE PROXY - so borrow may eat the edge. Real per-name borrow data is PAID
(Ortex ~$129/mo, Evan-gated). So X2b uses a BORROW-COST SWEEP (0/2/5/10/20%
annualized on short notional) to find the breakeven - honest + free (brackets the
unknown). Note: these are large-cap names, generally cheap to borrow (~GC), so a
2-5% sweep is realistic; if the edge dies at 3% it's borrow-illusory (MPP confirmed),
if it survives 5%+ it's a genuine (PROMISING-capped) market-neutral sleeve.

**STRATEGIC-PIVOT FLAG (no-yes-man):** a market-neutral long-short short-interest
sleeve is a DIFFERENT strategy class from the stated goal (HIGH % return, concentrated
K=1-3, long-biased). Lower absolute return, higher Sharpe, needs shorting infra.
Pursuing it is a real pivot; flagged to Evan; the numbers will inform whether it's
worth it. Still MODIFIED-WINDOW-CAPPED (single 2018-2026 -> PROMISING max).

**PLAN:** prereg X2b (short + long-short, next-open, 5bps + borrow sweep, robustness:
sub-period stability + short-leg name-concentration) doc-only BEFORE runner -> build
`run_x2b_short_side.py` reusing the X2 cache/engine -> verdict -> results/record/
commit. Evan-gated remainders: real borrow data (Ortex), a shorting-capable account,
the pivot decision. Cadence #81.

**Next action:** write + commit X2b prereg (doc-only), then build the runner.

---

# Appendix BW - X2b short-side = FAIL; X2's "strongest anomaly" was a frictionless mirage (2026-07-13, ~00:40 CST)

**WHAT:** Built + ran X2b per prereg (e718f6f, doc-only, predated runner
`scripts/run_x2b_short_side.py`). Properly costs X2's short-side finding: real short
accounting (proceeds + daily-marked liability) + a BORROW SWEEP (0/2/5/10/20%/yr) +
5bps trading. **VERDICT: FAIL** against the pre-registered market-neutral bar
(at 5% borrow: +CAGR AND Sharpe>=0.80 AND >=70% positive years). Tripwire GREEN.

**SELF-CORRECTION (2 layers):** (1) my FIRST X2b runner over-charged trading by fully
churning the book every rebalance (liquidate+re-establish even continuers). Caught it,
rewrote to DELTA turnover (trade only position changes) - fair cost is ~2.3pp not
5.5pp. Did NOT report the inflated-cost FAIL. (2) MORE IMPORTANT: X2's headline
("strongest real anomaly", spread +18.39%/Sharpe 0.98) was TOO GENEROUS - that was
frictionless. Honest costing kills it; correcting the record here.

**NUMBERS (delta-turnover):** LS gross 17.13%/Sharpe 0.92 (= X2 spread, confirms edge
exists) -> LS @0% borrow 14.81%/0.82 -> @2% 12.55%/0.71 -> @5% 9.24%/0.56 -> @10%
3.92%/0.30 -> @20% -5.98%. Breakeven borrow 13.8%/yr. PURE SHORT negative at EVERY
level (-2.10% @0%, -6.90% @5%). Robustness: only 5/9 years positive (2018/21/22/24
lose ~-6 to -9%; 2019/23/25/26 carry it +23 to +35%). Name concentration: high-DTC
"short" basket is a MIX - IBM +7.2%/TXN +17.8%/ORCL +23.7% RALLIED while held, only
MMM/T/ABT/HD fell -> shorting the most-shorted doesn't work standalone (mixed basket +
volatility drag + bull tape). Writeup `docs/research/2026-07-13_X2b_short_side_results.md`.

**WHY IT FAILS (not the MPP borrow-proxy story):** breakeven borrow 13.8% >> actual
large-cap GC borrow (~0.3-3%), so borrow SUPPLY isn't the killer here (unlike MPP's
illiquid-name mechanism). It fails on RISK-ADJUSTED return + LUMPINESS: a market-neutral
factor bet that clears no deployable Sharpe/robustness bar once realistically costed.
The long-short only "works" gross because the LONG low-DTC leg carries it; the short leg
is dead weight.

**ANSWER to "pursue the short-side": DON'T.** Rigorously tested, the edge isn't a
deployable market-neutral sleeve and the pure short is negative. Sizing up a
shorting/margin account is NOT justified. Residual (real borrow data + broader window +
the illiquid names where the effect actually lives) is Evan-gated + unreachable within
the floor. The short-side lead is CLOSED. Better found via a $0 borrow sweep than after
funding Ortex + a margin account.

**TALLY:** X2b = attempt 23 (informed-positioning family, same as E19/X2). **0 PASS-HR /
1 weak PASS-RA / 23 attempts / 8 families.** No family added.

**STATE:** swing.db untouched; tripwire GREEN; X2b prereg committed e718f6f; about to
commit runner + results + this entry + HANDOFF/memory/PRD. Cadence #81 (cont.).

**Next action:** commit X2b; free queue = X1 (vol-targeting, different family), X3 (Reg
SHO, same short-side family - lower value now X2/X2b closed it), or Evan redirects/stops.

---

# Appendix BX - CAPSTONE written (option 2); X3 ingest launched; X1 next (2026-07-13, ~01:15 CST)

**WHAT:** Evan said "do 2 then 1 and 3" (2=package/capstone, 1=X1 vol-targeting, 3=X3
Reg SHO). Flagged the ordering tradeoff to Evan (capstone-before-X1/X3 makes its count
stale) and chose to respect his order: wrote the capstone now with X1/X3 framed as the
final two confirming experiments, will bump counts 23->25 after.

**CAPSTONE (option 2 DONE):** `docs/CAPSTONE_program_synthesis.md` - the standing
single-doc synthesis of the whole program (supersedes the E1-E7 findings doc). Sections:
what it is + terminal claim; **methodology as the deliverable** (prereg-before-code,
asymmetric falsification, D1 dual-bar, frozen tripwire, decomposition ladder, liquidity
floor + window caps, append-only record); 8-family/23-attempt results ledger; the
structural WHY (Hou-Xue-Zhang / McLean-Pontiff / Avramov-Cheng-Metzker + the gap/cost
executioners from EX-DECOMP); the one real anomaly (short-side, uncapturable, with the
X2->X2b self-correction preserved); what's deployable (E6-1x overlay only) + nothing
live; what it demonstrates. Portfolio-quality; honest; self-correcting.

**X3 INGEST LAUNCHED (background b5354bdhf):** `scripts/ingest_regsho_short_volume.py` -
Reg SHO daily short-VOLUME, 39 names, CNMS consolidated 2018-08+ / per-venue
(FNYX+FNSQ+FNRA) sum for 2009-08+. Parser self-tested across all 3 format eras (pre-2011
5-col, post-2011 6-col, CNMS) = 39/39 names, plausible SVR 0.33-0.59. FIXED: Cloudflare
403s urllib's default UA -> added a browser User-Agent. ~9k file fetches, ~50min. Runs
while I build X1.

**STATE:** swing.db untouched; tripwire GREEN; capstone + regsho ingester + gitignore
about to commit; X3 fetching; X1 next. Tally still 23 (X1/X3 pending). Cadence #82.

**Next action:** commit capstone; build X1 (prereg from TEMPLATE -> runner -> verdict);
then X3 when its data lands; then finalize capstone counts 23->25.

---

# Appendix BY - X1 conditional vol-targeting = FAIL; plain 200-DMA still wins (2026-07-13, ~01:40 CST)

**WHAT:** Built + ran X1 (option 1) per prereg (07c22cb, doc-only, predated runner
`scripts/run_x1_vol_targeting.py`). SPY binary overlay, 3 arms: (a) E6 200-DMA, (b) E18
VIX-TS, (c) conditional = flat iff (VIX/VIX3M>1 AND SPY<200DMA). Reused macro_close /
sma from the E18 runner. **VERDICT: FAIL (descriptive, overlay).** Tripwire GREEN.

**RESULT:** gate 2006-2013 - (a) E6 is the BEST: 6.16%/DD 19.9%/Sharpe 0.58 (vs SPY
4.83%/56.5%/0.32); (b) VIX-TS 5.28%/36.5%/0.42; (c) conditional 5.48%/37.3%/0.42.
The conditional interaction TIES (b) and LOSES to (a) -> fails the PASS-RA bar
(gate Sharpe 0.42<0.80; must beat both plain overlays, doesn't). Secondary all 3 trail
SPY on CAGR in the bull. Cost-robust (1/5/15bp barely move it). **H1 rejected, null
survives - confirms E18: no vol gate beats the plain 200-DMA.** Mechanism: requiring
BOTH vol-bad AND trend-bad keeps it invested 89% (vs E6 70%), so it barely de-risks;
the binding 2008 drawdown is exactly when trend IS broken, so the extra vol condition
just removes E6's protective exits in choppy downtrends. Writeup
`docs/research/2026-07-13_X1_vol_targeting_results.md`.

**TALLY:** X1 = attempt 24 (seasonality/overlay family). **0 PASS-HR / 1 weak PASS-RA /
24 attempts / 8 families.** The one weak PASS-RA (E18 VIX-TS) is itself shown dominated
by plain E6 on drawdown here. Reconfirms E6-1x 200-DMA as the single deployable risk
overlay.

**X3 STATUS:** background ingest b5354bdhf still running (~2010, per-venue era is slow);
will build X3 on INGEST COMPLETE.

**STATE:** swing.db untouched; tripwire GREEN; X1 prereg committed 07c22cb; about to
commit runner+results+this entry+PRD. Capstone count still 23 (will finalize 23->25
after X3). Cadence #82 (cont.).

**Next action:** commit X1; await X3 ingest; build X3 -> verdict; then finalize capstone
23->25 + HANDOFF/memory.

---

# Appendix BZ - Session wrap: X3 ingest interrupted; docs finalized to 24; pushed (2026-07-13, ~23:58 CST)

**WHAT:** Evan: "commit the uncommitted changes and push." Session-boundary event: the
X3 background ingest (b5354bdhf) was STOPPED between sessions (no completion record) -
`.regsho_cache/short_volume.json` holds only 193 days, 2009-08-03..2010-05-07 (~5% of
the ~4300-day range). So **X3 is INCOMPLETE, not run**; "do 3" is unfinished.

**Corrected the doc drift** before pushing (would not push knowingly-stale docs): the
capstone + HANDOFF said "23 (+2 pending -> 25)". Reality = **24 attempts** (X1 ran =
FAIL, attempt 24; Appendix BY), X3 deferred/incomplete. Updated CAPSTONE (header,
ledger row, tally, status footer) and HANDOFF (header 23->24 + a 2026-07-13 snapshot
folding in X1-FAIL and X3-interrupted).

**FINAL TALLY: 0 PASS-HR / 1 weak PASS-RA / 24 attempts / 8 families.** The whole
"do 2 then 1 and 3" arc: (2) capstone DONE, (1) X1 DONE=FAIL, (3) X3 INCOMPLETE
(ingest interrupted, resumable from cache, strong FAIL-prior, deferred).

**PUSH:** all session commits (E19 results through X1 results, ~20 commits) pushed to
origin/main (public repo) on Evan's explicit instruction. Only prior uncommitted item
was `.claude/pm-cadence.json` (transient hook state), folded into this wrap commit.

**X3 RESUME NOTE (for a future session):** re-run
`.venv\Scripts\python.exe scripts/ingest_regsho_short_volume.py` - it is per-day
resumable (skips cached dates); on INGEST COMPLETE, write prereg_x3 (from TEMPLATE) ->
runner -> verdict. Prior = FAIL/weak (noisy executed-flow, same short-side family X2/X2b
already closed).

**STATE:** swing.db untouched; tripwire GREEN (last run after X1); working tree clean
after this commit; pushed. Cadence #84.

**Next action (future session):** resume X3 ingest -> run -> verdict (attempt 25), OR
treat the program as complete at 24 attempts with the capstone as the deliverable.

---

# Appendix CA - Post-crash health check ALL GREEN; X3 ingest resumed (2026-07-14, ~00:10 CST)

**WHAT:** Evan's machine crashed several times over ~3h; he asked for a full health
check, then said "start the ingestion."

**HEALTH CHECK (all green):** git tree clean + fully pushed, no .lock files, fsck
clean, no crash junk files; **180/180 JSON caches parse** (no corrupt mid-writes);
swing.db `integrity_check: ok` (bars = 105,396 rows); **frozen tripwire GREEN** (12
refs d=0, end-to-end engine+data proof); no orphaned/zombie Swing processes; no
scheduled tasks. Also verified (read-only) the separate Trading repo's streamlit
dashboard pair (PIDs 13180/13212) is the normal launcher+server, listening :8501,
health HTTP 200 - healthy, untouched. Crashes left NO damage.

**X3 INGEST RESUMED (background bfdabqndy):** re-ran ingest_regsho_short_volume.py;
resume verified - worker alive accruing CPU, live CDN fetch of a 2010 file returns
HTTP 200 w/ correct 5-col header; flat disk count was the 200-fetch flush buffer, not
a stall. ~70min ETA (per-venue era slow, CNMS era fast). Checkpoints every 200 days ->
crash-safe. On INGEST COMPLETE: prereg_x3 from TEMPLATE -> runner -> verdict
(attempt 25). Cadence #87.

**STATE:** tally 0 PASS-HR / 1 weak PASS-RA / 24 attempts / 8 families; X3 data
in flight; tree clean; pushed through 76602cb.

**Next action:** X3 on ingest completion; Evan asked "what experiments are left" -
answering from the PRD open queue.

---

# Appendix CB - FREE SWEEP part 1: C3/C4/C6/C1 all FAIL (2026-07-14, ~01:20 CST)

**WHAT:** Evan authorized "run the Free + autonomous ones just for good measure" =
C1/C2/C3/C4/C6/C7 (+X3 already ingesting). Order cheapest-first. Each: prereg
committed doc-only BEFORE runner -> run -> tripwire GREEN -> results doc -> commit.
FOMC calendar compiled by a background agent from federalreserve.gov primary sources
(260 scheduled announcement dates 1994-2026, unscheduled/emergency excluded,
spot-checked) -> committed as `data/fomc_announcement_dates.json` (curated data, not
gitignored cache). FF3 daily factors fetched from Ken French library (cached,
gitignored).

**C3 vol-breakout kill-shot (attempt 25) = FAIL.** Gate 3.62%/Sh 0.37 (n=607), sec
1.37%/0.19. Killer detail: the TIME-STOP-ONLY arm BEATS the channel exit (6.19% vs
3.62% gate) - the 10d-low exit is a whipsaw tax; "cut losses at the recent low" is
measurably value-destroying. Breakout family = 3 consistent kills (E8, E11, C3).

**C4 Moreira-Muir vol-sizing (attempt 26) = FAIL (bar), real DD-cutter.** Managed
beats base Sharpe both windows on BOTH bases and cuts DD hard (E6 gate 53.7->25.1%;
E18 sec 43.6->27.0%, Sh 0.82->0.94) but best gate Sharpe 0.77 < 0.80 bar -> FAIL, not
tuned. Best-behaved overlay variant tested; natural deployment shape if E6/E18
forward-paper ever goes live. Vol-overlay family closed (X1 + C4).

**C6 FOMC even-week (attempt 27) = FAIL; cleanest decay exhibit.** Gate replicates
CMVJ exactly (+5.62bps/day even vs -3.15 odd) then INVERTS post-2014 (+3.69 vs +6.60)
- died at publication. Overlay gate Sh 0.34 vs SPY 0.19, nowhere near RA; 1585
toggles -> 15bp stress negative. Third decayed-calendar exhibit (E13, E15, C6).

**C1 residual reversal (attempt 28) = FAIL; CLOSEST-EVER HR NEAR-MISS.** E16's exact
engine, ranking swapped to FF3-residual (126d betas, 21d formation): gate
19.08%/DD 57.7%/Sh 0.69 - beats E16's 16.76% AND pulls DD under the 60% ceiling ->
**first time both PASS-HR legs clear in the gate window** (28 attempts). FAIL on the
both-windows bar: secondary collapses to 2.92%/0.24 (dead post-2014); survivorship
upper-bounds the gate number anyway; 15bps kills it (gate 7.28%, sec negative).
BHLV mechanism real; regime+survivorship artifact. THE DISCIPLINE HELD on the most
tempting result yet - no tuning, no window-shopping.

**TALLY: 0 PASS-HR / 1 weak PASS-RA / 28 attempts / 8 families.** Tripwire GREEN
after each. X3 ingest ~958/4300 days (2013-05). Cadence #88.

**Next action:** C2 probe (dividend-initiation flag; expect ~0 events in 39
dividend-aristocrat-ish survivors -> BLOCKED-ON-DATA close), C7 probe (SVXY/VXX
coverage + Volmageddon kill-switch prereg), X3 on INGEST COMPLETE; then final doc
sync (capstone counts, HANDOFF, memory, PRD outcomes) + push on Evan's word.

---

# Appendix CC - FREE SWEEP part 2: C2 closed on probe; C7 = FAIL despite 26% CAGR; M8 effectively closed (2026-07-14, ~02:00 CST)

**C2 dividend-initiation = CLOSED BLOCKED-BY-DESIGN (no prereg).** Probe (yfinance
full dividend histories, 39 survivors): only THREE first-ever in-window initiations in
26 years - MSFT 2003-02-19, ORCL 2009-04-06, CSCO 2011-03-29 (AAPL-2012 is a
resumption; everyone else initiated 1962-1999). n=3 clears no pre-registerable floor ->
closed for insufficient event flow, the honest E17 pattern. The initiation-drift
literature lives in small/mid-caps the liquidity floor excludes.

**C7 SVXY carry (attempt 29) = FAIL - the program's highest-ever full-window CAGR and
still a clean kill.** Prereg (doc-only) -> probe SVXY 2011-10-04+ (3713 bars) ->
runner. MAIN (VIX/VIX3M<1 gate + kill-switch day<=-20% -> exit+21d stand-down):
**26.45% CAGR / DD 55.4% / Sharpe 0.76** vs SPY 13.04%/0.82 -> loses the
pre-registered CAGR-AND-Sharpe bar on Sharpe. Era split (descriptive): the -1x era
(2012..2018-02) did 47.33%/0.99; **today's -0.5x SVXY does 13.18%/0.55** - the
headline rides a dead instrument. Volmageddon trace: gate flipped at 2018-02-02 close
-> exit 02-05 OPEN -> dodged -32%/-83% BY ONE SESSION (effective-N=1 tail-dodging, not
safety; XIV died in the identical trade). Kill-switch fired once in 14.5yr (Brexit
2016-06-24, -26.4%); verdict not KS-sensitive (no-KS arm Sh 0.81 also < 0.82).
15bps stress 24.91%/0.74. Tripwire GREEN. VRP family fully surveyed
(E18 gate / X1 conditioning / C4 sizing / C7 harvest): VIX-TS is a real regime
classifier, NOT an engine. Results `docs/research/2026-07-14_C7_svxy_carry_results.md`
(C2 close documented in the same doc).

**PRD SYNC:** M8 outcomes annotated (C1-C7); M8 exit conditions marked MET-except-
C5->X3. All seven survey residuals failed every tier -> per M8's own exit paragraph,
the terminal claim upgrades to "the entire documented, evidenced swing-method space
(survey 2026-07-12) is exhausted at retail EOD / K=1-3 / $100-1,000" - pending X3.

**TALLY: 0 PASS-HR / 1 weak PASS-RA / 29 attempts / 8 families.** X3 ingest
~1150/4300 days (2014-02). Cadence #88 (cont).

**Next action:** X3 on INGEST COMPLETE (prereg -> runner -> verdict = attempt 30);
then final doc sync (capstone counts 24->30, HANDOFF, memory) + push on Evan's word.

---

# Appendix CD - X3 = FAIL (SVR is noise); FREE SWEEP + program COMPLETE at 30 (2026-07-14, ~02:40 CST)

**WHAT:** X3 ingest completed (bfdabqndy, exit 0): 4,260 sessions 2009-08-03..
2026-07-10, 39/39 coverage (2265 venue-sum + 1995 CNMS days). Prereg
`prereg_x3_regsho_svr.md` committed doc-only BEFORE runner
`scripts/run_x3_regsho_svr.py`. **VERDICT: FAIL** (attempt 30, the program's LAST
experiment). Tripwire GREEN.

**RESULT:** long-only lowest-SVR K=5 weekly, next-open, 5bps: gate 13.00%/DD 27.1%/
Sh 0.75 LOSES SPY 14.80%/0.91 (both CAGR and Sharpe); sec 10.85%/0.64. Decomposition:
B(next-open 0bps) 19.03% >> A(c2c) 15.40% (low-SVR basket has favorable overnight
drift) >> C(+5bps) 13.00% (weekly-turnover cost -6pp); 15bps collapses to 1.83%/gate,
negative/sec. **KEY: existence spread low-SVR minus high-SVR = +1.24%/Sh 0.16 =
essentially ZERO** (low 14.74% vs high 12.05%) -> executed short VOLUME carries no
cross-sectional signal, confirming the MM-hedging-contamination prior. **Clean X2/X3
contrast:** short-INTEREST (X2, settlement positions) = real +18.39% short-side
spread; short-VOLUME (X3, executed flow) = noise. Both FAIL, different reasons, now
documented. Results `docs/research/2026-07-14_X3_regsho_svr_results.md`.

**PROGRAM COMPLETE. TERMINAL TALLY: 0 PASS-HR / 1 weak PASS-RA / 30 attempts /
8 families.** The free-sweep arc (this session): C1/C3/C4/C6/C7 run + C2 closed +
X1/X2/X2b/X3 = the documented, evidenced swing-method space (survey 2026-07-12) is
EXHAUSTED at retail EOD / K=1-3 / $100-1,000. One weak risk-mgmt overlay (E18 VIX-TS),
one real-but-uncapturable anomaly (short interest), zero high-return engines.

**FINAL DOC SYNC (this entry):** CAPSTONE finalized 24->30 (ledger rows for C/X
experiments, near-miss narrative, status=COMPLETE); HANDOFF header 24->30 + 2026-07-14
snapshot; memory updated; PRD #47/#36-42 outcomes annotated; M8 exit MET. All committed;
awaiting Evan's push call.

**REMAINING WORK = EVAN-GATED ONLY:** M3 Alpaca paper deploy of the E6-1x (+ E18-VIX-TS,
+ the C4 vol-managed shape) forward-paper candidate = the SOLE path to genuinely new
out-of-sample evidence; X5 analyst-revision drift ($22 FMP); X6 crypto pilot (scope +
25bps fees). No free autonomous experiment remains. Cadence #88 (cont).

**Next action:** push on Evan's word; otherwise the capstone is the deliverable and the
program stands complete.

---

# Appendix CE - "do 2" = X6 crypto pilot (X5 blocked-on-purchase); scope opened (2026-07-14, ~12:40 CST)

**GROUNDING (post-compaction integrity check):** verified the 30-attempt program is
REAL, not summary drift - HEAD 95b83a5, tree clean, all C1/C3/C4/C6/C7 + X3 runners +
preregs + result docs present on disk; git log shows their RESULTS commits (8ab182c C7,
3176364 C1, etc.). No fabrication; the cited numbers (C1 19.08%, C7 26.45%) trace to
real result docs. 14 commits unpushed. Stale FOMC-agent stop notice ignored (C6 landed).

**"do 2" INTERPRETATION + BOUNDARY:** offered bucket = X5 (analyst-revision, $22 FMP) /
X6 (crypto pilot). **X5 stays BLOCKED-ON-EVAN:** I cannot purchase the FMP feed, and the
free yfinance alternative silently backfills/restates ratings -> look-ahead
contamination (data-sources brief warned this), so a free X5 would violate rigor -
better blocked than contaminated. **X6 is the executable half:** free data (yfinance
BTC-USD/ETH-USD), paper-first (no real money/account), and an existing Evan-authored PRD
task (50) that was only SCOPE-gated. Reading "do 2" as authorizing that crypto scope.

**X6 = attempt 31, a NEW DOMAIN (crypto), extends - does not contradict - the "equity
method space exhausted at 30" claim.** Per PRD 50 + crypto brief: BTC/ETH time-series
trend (e.g. 100d / 20-100d MA), 24-7 daily bars (signal at UTC close, next-bar exec =
zero gap by construction), **25 bps/side (5x equity, the governing economic fact)**,
gate 2018-2022 + secondary 2023-> MODIFIED-WINDOW CAP (PROMISING max), vs HODL. Disclose
the 2022-23 trend drawdown as an EXPECTED failure mode. Paper-first: a PROMISING routes
to paper only; live-money crypto (custody = the deciding risk) stays Evan-gated. Cadence #90.

**Next action:** prereg_x6 (from TEMPLATE) doc-only -> fetch BTC/ETH -> runner -> verdict
-> results/record/commit. Then report X6 + the blocked-X5 status.

---

# Appendix CF - X6 crypto trend = FAIL; E6's trend-overlay lesson generalizes to crypto (2026-07-14, ~13:20 CST)

**WHAT:** Built + ran X6 (crypto scope, Evan "do 2") per prereg
`prereg_x6_crypto_trend.md` (doc-only, predated runner `scripts/run_x6_crypto_trend.py`).
BTC/ETH dual-MA (SMA20>SMA100) long-or-flat, next-bar, 25bps/side, vs HODL. Data
yfinance BTC-USD (2014-09+) / ETH-USD (2017-11+), 24-7 daily, .crypto_cache gitignored.
**VERDICT: FAIL (PROMISING-capped).** Tripwire GREEN (new domain, doesn't touch swing.db).

**RESULT (combined K=2, 25bps):** gate 2018-22 sleeve 29.61% CAGR/DD 60.6%/Sharpe 0.76
CRUSHES HODL 4.34%/82.3%/0.43; but sec 2023- sleeve 23.09%/41.5%/0.76 LOSES HODL's raw
Sharpe 44.31%/53.7%/**1.01**. Fails the pre-registered beat-HODL-Sharpe-in-BOTH-windows
bar (0.76<1.01 in the bull). Per-asset same shape (BTC/ETH both win gate, lose sec-bull).

**TWO FINDINGS > the FAIL:** (1) **COST-ROBUST** - 33 toggles/5yr -> 25bps barely bites
(gate 30.26%@10bps -> 28.55%@50bps); the brief's "25bps=5x-equity kills it" worry is
WRONG for a slow trend overlay (it's right for HF crypto). (2) **Same lesson as equity
E6, new domain:** MA trend = drawdown control (cuts 82%->61% DD in bears, triples
return) that LOSES to buy-and-hold in bulls. Stepping outside equities did NOT escape
the structural conclusion (trend = market-dependent risk overlay, not high-return
engine). 100d-single-MA sensitivity looked better (BTC Sh 0.90/0.95) but still <HODL in
the bull; did NOT switch verdict to it (would be tuning a FAIL). Results
`docs/research/2026-07-14_X6_crypto_trend_results.md`.

**X5 STATUS: BLOCKED-ON-EVAN** (unchanged) - can't buy the $22 FMP feed; free yfinance
ratings = silent restatement/look-ahead -> a free X5 would violate rigor. Stays blocked
until Evan provides clean PIT analyst-revision data.

**TALLY:** X6 = attempt 31 = 30 equity + 1 crypto domain. **0 PASS-HR / 1 weak PASS-RA /
31 attempts / 8 equity families + 1 crypto pilot.** Crypto pilot EXTENDS (does not
contradict) the terminal claim: even in a new asset class the only thing that "works"
is trend-as-drawdown-control, and HODL wins the bull. Paper-first; nothing live;
live-money crypto stays Evan-gated (custody).

**STATE:** swing.db untouched; tripwire GREEN; X6 prereg committed; about to commit
runner+results+this entry+capstone/HANDOFF/PRD/memory sync. Cadence #90 (cont).

**Next action:** commit X6; sync capstone/HANDOFF 30->31; then remaining work is
Evan-gated only (M3 deploy; X5 needs FMP; live crypto needs custody call) - or push.

---

# Appendix CG - M10 SYNTHESIS ARC opened: evidence-informed combos vs BOTH tiers (2026-07-14, ~13:05 CST)

**WHAT:** Evan: "using all the data and experiments done come up with different
strategies to see if those can meet both criteria" (= PASS-HR CAGR>=15%/DD<=60% both
windows AND PASS-RA gate Sharpe>=0.80/>SPY both/+CAGR both). Opening **M10 = the
synthesis arc** (attempts 32+): compose the surviving PROPERTIES (E6 trend-gate DD
control; E18 VIX-TS Sharpe 0.80; C4 vol-sizing Sharpe lift 0.69->0.77/0.82->0.94; C1
gate-window reversal alpha; E10 PEAD; synthetic-2x machinery w/ 2%/yr drag calib from
E6/E5) into candidate return ENGINES.

**STANDING DISCLOSURE (binds every M10 prereg):** these designs are made AFTER seeing
31 results on the SAME two windows -> severe data-snooping/multiple-testing prior.
In-window passes are WEAKER evidence than E1-X6's falsifications were. Every M10
prereg carries this disclosure; any pass is labeled **"IN-SAMPLE-COMPOSED - forward
paper REQUIRED"**, never a live claim. Rigor otherwise unchanged: prereg-before-code
w/ fixed rules+criteria, no tuning a FAIL, tripwire GREEN, tiered costs + financing
drag modeled (2%/yr synthetic-leverage calib), 5bps/side equities.

**PROCESS:** multi-agent design panel (ultracode workflow) over the full evidence
ledger - designer lenses (leverage-composer / ensemble-architect / regime-conditioner
/ signal-resurrector / red-team) -> adversarial feasibility+rigor judging -> top ~3-4
specs -> individual preregs (doc-only commits) -> runners -> verdicts. Honest prior:
FAIL remains most likely (composing Sharpe-0.77 streams can't clear 0.80 without a
mechanism; 15% gate CAGR must survive two crashes). Cadence #93.

**Next action:** run the design workflow; prereg the survivors; build+run.

---

# Appendix CH - M10 design panel: Nagel Switch is the one non-empty path (2026-07-14, ~13:35 CST)

**WHAT:** Ran the multi-agent design panel (workflow wic64yxkx, 5 designer lenses x
adversarial math+rigor judges). It hit the session rate-limit at the final synthesis
step (20/28 agents done) - recovered 11 designs + 16 judge verdicts from the journal
and did the synthesis chair's job myself.

**KEY RESULT - the red-team PROVED the static-blend impossibility:** PASS-HR from any
FIXED-weight combo is arithmetically EMPTY. Gate>=15% forces C1-weight w>=0.66; sec>=15%
forces w<=0.29 (C1 is gate-alive 19.08%/sec-dead 2.92%; trend is gate-weak/sec-alive).
Disjoint by ~0.37 weight (~4-5pp CAGR shortfall in one window). Rebalancing bonus
(~0.5-1pp) can't close it; any time-varying weight = forbidden era-switching. So the ONLY
escape is state-conditioning on a CAUSAL variable.

**THE SURVIVOR (highest scores 7/7.5, multiple lenses converged):** the **NAGEL SWITCH** -
VIX-gated regime switch: residual-reversal (C1) when VIX>20, trend (E6/C4) when VIX<=20.
Escapes the impossibility because Nagel (RFS 2012) documents reversal alpha = liquidity-
provision compensation that SCALES with VIX - a published pre-2012 MECHANISM (not a date),
using VIX (1990+, full gate coverage, NO PROMISING cap). It's the only design with expected
CAGR near BOTH 15% bars (gate 14-18%, sec 11-16%). **Honest judge consensus prior:** gate-HR
plausible PASS but DD razor-thin (inherits C1's 57.7% vs 60% ceiling) + semi-in-sample +
survivorship; **secondary-HR is the likely FAIL leg** - IF C1's reversal is TEMPORALLY dead
(McLean-Pontiff) not just VIX-state-dead, VIX-conditioning can't resurrect it and sec lands
~10-13%. Most likely outcome = gate pass + sec near-miss = PROMISING, not a clean double.

**CHOSEN TO RUN (2, mechanistically distinct):** M10-1 = Nagel Switch (best shot at both
tiers). M10-2 = Gap-Amortized Stress IBS (D5, judge 6/RUN): multi-day-hold 2x QQQ IBS
mean-reversion, VIX-gated, trend fallback - directly attacks the overnight-gap killer (the
EX-DECOMP recurring assassin) + tests whether E2's c2c 18.15% "mirage" is reachable via
hold-amortization. **NOT run:** D2 vol-managed-2x-trend (judge 1/KILL - analytic bound:
at trend Sharpe 0.37, max geo excess = S^2/2 ~= 6.9%/yr, so gate<=8% - PASS-HR formally
unreachable for trend-family, statable without running); D8/D7 ensembles (KILL - dead
sleeves drag sec-RA below SPY); braked-2x family (gate Sharpe capped ~0.71<0.80).

**BINDING:** every M10 prereg carries the data-snooping disclosure; any in-window pass is
capped **"IN-SAMPLE-COMPOSED - forward paper REQUIRED"**, never a live/clean claim (C1's
own prereg already declared its survivor-universe passes UNINTERPRETABLE - the Nagel Switch
inherits that). Cadence #93 (cont).

**Next action:** prereg M10-1 Nagel Switch (doc-only) -> runner (reuse C1 residual_series +
E6 trend + VIX macro_close) -> verdict; then M10-2.

---

# Appendix CI - M10-1 Nagel Switch = program's FIRST PASS-HR (but IN-SAMPLE, forward-only) (2026-07-14, ~14:05 CST)

**WHAT:** Ran M10-1 (prereg committed doc-only before runner). Nagel Switch: VIX>20 ->
C1 residual reversal (reused verbatim), VIX<=20 -> E6 QQQ-200DMA trend; weekly decision,
next-open exec, 5bps stk/1bp QQQ. **FIRST NUMERICAL PASS-HR IN 32 ATTEMPTS.** Main C:
gate 2000-13 17.87% CAGR / DD 59.9518% / Sh 0.66; sec 2014- 15.94% / DD 39.68% / Sh 0.78.
Both windows clear CAGR>=15% AND DD<=60%. PASS-RA fails (gate Sharpe 0.66<0.80). Tripwire
GREEN. Writeup docs/research/2026-07-14_M10-1_nagel_switch_results.md.

**BUG FIXED before the result was trusted:** first run showed sec -100% (NAV->0). Traced
to a mark-to-market boundary bug: QQQ cache ends 2026-07-09 but a stock trades 2026-07-10
(in master), so a held QQQ was marked 0 on the last day. Fixed with carry-forward marks
(last close <= d; PAST-only, no look-ahead). Gate was already clean; only the sec final
mark was broken.

**THIS IS NOT A WIN - the discipline says so (7 caveats, all in the results doc):**
(1) IN-SAMPLE-COMPOSED - designed after 31 results on these exact windows, components
chosen because they were the gate/sec survivors. (2) SURVIVOR-FLATTERED - reversal leg
buys worst-residual names among 39 KNOWN survivors in exactly the 2000-02/2008 crashes;
C1's own prereg declared such passes UNINTERPRETABLE; this inherits that cap. (3) Gate DD
59.95% clears the 60% ceiling by 0.05pp - razor-thin, exactly as the prereg predicted.
(4) THRESHOLD-FRAGILE: VIX>18 -> gate 14.83% (HR FAIL); passes only at 20/22. (5) COST/
EXEC-FRAGILE: c2c 22.82% -> next-open 17.87% (~5pp in the overnight gap C1 always leaked);
15bps -> 12.40% (FAIL). (6) PASS-RA fails (Sh 0.66) - high-return/high-variance riding a
~60% DD. (7) Nagel's 1998-2010 sample overlaps the gate (mechanism partly in-sample).

**VERDICT LABEL (per M10 cap): "PROMISING / FORWARD PAPER REQUIRED" - never a clean pass
or live authorization.** The honest headline: the ONLY way to numerically clear HR was to
compose two known survivors on a survivor universe with hindsight, and even then it passes
by 0.05pp DD and fails at a nearby VIX threshold. The structural null is REINFORCED, not
broken: no clean, OOS, robust high-return edge exists; M10-1 is the closest, and it is a
forward-paper HYPOTHESIS, not a result.

**TALLY (attempt 32):** 1 IN-SAMPLE-COMPOSED PASS-HR (forward-paper-required,
uninterpretable) + 1 weak PASS-RA (E18) / 0 clean-OOS high-return edges / 32 attempts.
The "0 PASS-HR" headline is now "1 in-sample-composed PASS-HR" - a meaningful, honest
distinction, not a deployable edge. Cadence #93 (cont).

**Next action:** commit M10-1; sync capstone/HANDOFF (the tally nuance); then M10-2
(gap-amortized stress IBS) remains the other panel survivor to run, OR report to Evan
that the one thing that would make M10-1 real is M3 forward paper (Evan-gated).

---

# Appendix CJ - M10-2 gap-amortized stress IBS: building the panel's 2nd survivor (2026-07-14, ~18:30 CST)

**WHAT:** Evan "do 1 then push" = run M10-2 (panel design D5, judge 6/RUN), then push.
Directly attacks the EX-DECOMP recurring assassin (the overnight gap that killed the IBS
family): E2's >half-the-edge-lives-in-the-close-to-next-open-gap is fixed by two
mechanical levers (NOT tunes): (a) 5-session HOLD amortizes the lost first-night gap over
days 2-5 of the reversion (E2's 1-day hold made the gap ~100% of the capture window); (b)
enter only in STRESS (VIX>20), where Nagel documents liquidity-provision pay is largest.
Index-level QQQ @1bp so the B->C cost killer is also absent. Tests whether E2's c2c 18.15%
"mirage" is reachable at all.

**SPEC:** QQQ synthetic-2x (E6's synth/calib machinery, drag~2%/yr QLD-calibrated) for the
MR play; state machine top-down at each close, exec next open, 1bp/side: (1) IN-TRADE(2x):
exit next open on IBS>=0.80 OR 5 sessions since entry; (2) ENTRY when flat: VIX>20 AND
IBS<=0.20 -> buy 2x; (3) FALLBACK flat + VIX<=20: QQQ if >200DMA else cash; (4) flat +
VIX>20 not-oversold: cash. No same-day re-entry. Reuses swing_bot.signals.ibs, E6 synth/
calib, VIX macro_close. Full window (gate 2000-13, sec 2014-), D1 dual-bar. IN-SAMPLE-
COMPOSED (M10 cap: pass = forward-paper-required). Honest prior (judges): gate ~7-11%
(likely <15%), sec ~13-14% -> FAIL/PROMISING most likely; program value high either way
(directly measures the reachable share of the E2 gap edge).

**Next action:** commit M10-2 prereg (doc-only) -> runner -> verdict -> results/record ->
commit -> PUSH. Cadence #96.

---

# Appendix CK - M10-2 = FAIL; closes the E2 "c2c mirage" permanently (2026-07-14, ~18:55 CST)

**WHAT:** Ran M10-2 (prereg committed doc-only before runner). Gap-amortized stress IBS:
2x QQQ MR on VIX>20 & IBS<=0.20, 5-session/IBS>=0.8 exit, trend fallback. **VERDICT:
FAIL.** Main C next-open 1bp: gate 2.99% CAGR / DD 83.3% / Sh 0.28; sec 28.95% / 40.1% /
1.08. Gate fails HR on BOTH legs (2.99%<15%, 83.3%>60%); PASS-RA fails (Sh 0.28). Tripwire
GREEN. 255 gate MR entries. Writeup docs/research/2026-07-14_M10-2_gap_amortized_ibs_results.md.

**THE PAYLOAD (high program value in the FAIL):** the gap-amortization WORKED - c2c 3.18%
~= next-open 2.99% in the gate (the 5-day hold neutralized the overnight gap, unlike E2's
1-day hold where the gap was ~half the edge). That ISOLATES the reversion's gap-free
economics and they are catastrophic in the gate. **This CLOSES the E2 c2c "mirage"
permanently:** E2's tantalizing c2c 18.15% (vs executable 7.98%) had left open "was there
real alpha behind the gap?" - answer NO. Best case (stress-concentrated, gap-removed,
1bp index) still gives 2.99% on an 83% DD. Buying 2x QQQ into 2000-02/2008 oversold prints
and holding 5 days catches more cascade than bounce. **The overnight gap was hiding the
DRAWDOWN, not the alpha.**

**SHARPENS M10-1:** M10-1 (Nagel Switch) passed HR with UNLEVERED cross-sectional reversal
on survivors; M10-2 FAILs with 2x INDEX MR (83% DD). Same VIX-stress conditioning, opposite
outcome -> the killer is 2x-leverage-into-index-crashes, and M10-1's "pass" is specifically
a cross-sectional-survivor effect (further reason it's survivor-flattered, forward-only).

**TALLY:** M10-2 = attempt 33 (FAIL). **1 IN-SAMPLE-COMPOSED PASS-HR (M10-1, forward-only)
+ 1 weak PASS-RA (E18) / 0 clean-OOS high-return edges / 33 attempts.** M10 SYNTHESIS ARC
COMPLETE (both panel survivors run: M10-1 forward-paper candidate, M10-2 closes E2). The
only untested lever that could validate M10-1 = M3 forward paper (Evan-gated). Cadence #96.

**STATE:** swing.db untouched; tripwire GREEN; committing M10-2 + pushing per Evan.

**Next action:** commit M10-2; push all M10 commits to origin/main.

# Appendix CL - Finalize THROUGH M10 (not "done"); full what-worked/what-might report; new M11 chart-pattern direction (2026-07-14, ~21:56 CST)

**WHAT (Evan's directive, verbatim intent):** "finalize with M10 but DON'T call research
done, give a full report on what didn't work and what might. This project is more about
trying everything (including things biased off of different data)." Plus a new idea to add:
**algorithmic (NOT LLM-driven) detection of the chart patterns traders teach** - the visual
shapes (head-and-shoulders, double top/bottom, triangles, flag breakouts) that "suggest the
market is about to go up or down," bought on pattern completion.

**DOCS-ONLY TURN.** No experiment run, no code/strategy/factor file touched, swing.db
untouched, tally UNCHANGED at 33 attempts. This is a finalization + reframing + roadmap-add,
not a new attempt. Tripwire re-verified GREEN (docs-only, but confirmed).

**REFRAMING (the "don't call research done" instruction, made structural):**
- **Capstone** (`docs/CAPSTONE_program_synthesis.md`) rewritten from "COMPLETE / the
  documented method space is exhausted" -> **"ONGOING - finalized THROUGH the M10 arc, not
  closed."** Counts 31 -> **33** everywhere (header, tripwire line 23->33, §3 heading, tally,
  §7 count); M10 folded into the §3 ledger as a new "Evidence synthesis (state-conditioned)"
  row (M10-1 in-sample PASS-HR + M10-2 FAIL/E2-mirage-closed); terminal-claim §1 given a new
  "Scope of the claim - and what it does NOT cover" paragraph (chart-pattern geometry never
  tested -> claim is "no edge found in what was tested," not "no edge exists"); §7 sharpened
  ("the sharpest demonstration is M10-1: the one design that CLEARED PASS-HR - and the
  program still refused to call it a win").
- **NEW capstone §8 "The open frontier - what has NOT been tested, and what might still
  work"** (old §8 Reproducibility -> §9). This IS the "what might" half of Evan's report:
  (a) **algorithmic chart-pattern detection** (the one untested mechanism family, honest
  FAIL prior, PRD M11); (b) **M3 forward paper** = the only UNCONTAMINATED-evidence lever
  (every number in the doc is survivor-biased or in-sample); (c) lower-priority untested
  levers (pairs/stat-arb - same no-shorting wall; LLM-forward overlays - M3-attached;
  short-interest-done-right - needs paid borrow data; intraday/MOC - EOD-rule-blocked).

**THE NEW DIRECTION - M11 chart-pattern detection, scoped skeptically (pressure-test, per
Evan's standing "no yes-man" rule):** It genuinely fits the constraints (EOD-native, K=1-3,
and - being price-only with no data wall - FULL-WINDOW D1-reachable, unlike every post-2000
experiment). But the **honest prior is FAIL**, stated before any run:
- **Lo-Mamaysky-Wang (2000, J. Finance)** - the one rigorous algorithmic detector - found
  patterns carry *modest incremental statistical information* but did NOT show cost-surviving
  profitability. "Informative != tradeable."
- **Sullivan-Timmermann-White (1999) + Bajgrowicz-Scaillet (2012):** technical-rule profits
  vanish after data-snooping/FDR correction + realistic costs, OOS. **McLean-Pontiff:** a
  pattern taught publicly for decades is a published, arb-eligible (decayed) signal.
- **Program-internal mechanistic prediction:** continuation patterns (flags/triangles/
  breakouts) ARE breakouts -> inherit the breakout family's 3 kills (E8/E11/C3); reversal
  patterns (double-bottom/inverse-H&S) are cousins of the reversal near-miss that cleared
  then decayed (E16/C1); next-open bleeds the same overnight gap. **Expected: FAIL, extending
  the terminal claim to "even the chart SHAPES don't trade at retail EOD."** A FAIL adds a
  genuine 9th equity family to the exhausted set; a small chance of a forward-paper PROMISING.
- Out of scope (different ask): CNN chart-IMAGE classifiers (Jiang-Kelly-Xiu 2023) - ML-driven,
  cross-sectional over thousands of names; Evan specified RULE-BASED, not LLM/ML.

**PRD:** added **M10** (DONE; tasks 52-53 with outcomes) and **M11** (CURRENT OPEN DIRECTION,
UNSTARTED; tasks 54-57: optional brief -> prereg pinning LMW's PUBLISHED params + ONE
consolidated spec / snoop-adjustment -> build+run -> record) sections + milestone-table rows.
Recommended M11 lead = the LMW head-and-shoulders + double-top/bottom reversal detector as a
single honest kill-shot (the reversal-side analogue of C3's breakout kill-shot). Fork-safe:
this is ADD-by-append (new milestones), not a pivot - no SUPERSEDED tree.

**HANDOFF** header/top-block reframed to "research OPEN; M11 chart patterns = next honest
experiment." Memory `swing-trading-project.md` updated (research ongoing + M11 frontier).

**TALLY (unchanged):** 33 attempts / 0 CLEAN PASS-HR / 1 IN-SAMPLE-COMPOSED PASS-HR (M10-1,
forward-only) / 1 weak PASS-RA (E18). Cadence #97.

**STATE:** all edits pushed pending Evan's "commit/push" word (per standing rule, commit only
when asked). Tripwire GREEN.

**Next action:** on Evan's go - run **M11** (prereg the LMW chart-pattern kill-shot, then
run; the one remaining free, autonomously-runnable experiment). The only lever that could
validate M10-1 remains **M3 forward paper** (Evan-gated: Alpaca paper account).

# Appendix CM - M11.1 chart-pattern research brief DONE; evidence MIXED; design sharpened (2026-07-14, ~22:10 CST)

**WHAT:** Evan "1, then 3" -> (1) committed+pushed the finalization (04e8de4), then (3) the
chart-pattern research brief. Executed the research-brief 10-stage process directly (skill
already loaded this session; did NOT re-invoke the Skill tool per the "don't re-execute"
caveat). 6 web searches (LMW 2000; Savin-Weller-Zvingelis 2007; STW 1999; Bajgrowicz-Scaillet
2012; detection methods; modern 2021+) + targeted fetches (2 primaries paywalled 403/402 ->
used CXO Advisory open summary for the Savin caveat). Brief:
`docs/research/2026-07-14_chart_pattern_detection_brief.md`.

**PAYLOAD - the evidence is MIXED, not a clean FAIL, and it sharpens the prior into an
X2 echo:**
- **LMW (2000):** patterns carry modest incremental statistical info, but "informative !=
  profitable" (their own caveat).
- **Savin-Weller-Zvingelis (2007)** = the strongest counter, and the decisive finding:
  head-and-shoulders predicts ~5-7%/yr risk-adjusted **UNDERPERFORMANCE** (Russell 2000,
  1990s) - a real signal, but a **SHORT** one that is "NOT profitable as a standalone
  strategy in rising markets" and works "only in hedged portfolios." **=> the best-supported
  chart pattern is bearish/market-neutral -> the SAME no-fractional-shorting wall that made
  X2/X2b uncapturable at $100-1k.** The one pattern with strong evidence is one this project
  structurally cannot trade.
- **STW (1999) + Bajgrowicz-Scaillet (2012):** snooping + even low transaction costs erase
  technical-rule profits (Bajgrowicz-Scaillet: offset IN-SAMPLE; no ex-ante persistence).
- **Modern (Tsinaslanidis 2021):** 92.5% of experiments "profitable" but only "reduced to
  parameter values aligned with TA" = exactly the ex-post parameter selection STW warns of;
  signal-of-life, not a clean OOS claim.

**TWO DESIGN CORRECTIONS (my earlier "lead with H&S/double-top" was WRONG):**
1. **Deployable lead = LONG-side reversal (inverse-H&S / double-BOTTOM),** NOT H&S/double-top
   (that's the short/uncapturable side -> report as an X2-style measurement only).
2. **LMW's kernel smoother is NON-CAUSAL (look-ahead)** -> the deployable detector must be
   causal, or confirm only AFTER the neckline break. Pinned this as an M11 prereg guard.
Fed back into **PRD M11.1** (marked DONE) + **M11.2** (lead corrected + look-ahead guard +
brief link) and **capstone §8(a)** (correction note + link).

**VERDICT PRIOR unchanged for the DEPLOYABLE test = FAIL** (long-only side has the weakest
support; the tradeable evidence is short/hedged/large-book; program-internal analogues
E8/E11/C3 + E16/C1 all point to FAIL), but M11 is now a sharper, honest kill-shot rather
than a naive one. Tally UNCHANGED (33; brief is research, not a run). Cadence #98.

**STATE:** brief + M11/capstone refinements UNCOMMITTED (offering commit; "1 then 3" did not
include committing the brief). Tripwire GREEN (no code touched since the last GREEN run).

**Next action:** on Evan's go - commit the brief + M11 refinements, then **M11.2** (prereg
the causal LONG-side inverse-H&S/double-bottom kill-shot) -> build -> run -> D1 verdict.

# Appendix CN - M11.2 prereg committed doc-only (chart-pattern detector, params pinned) (2026-07-14, ~22:40 CST)

**WHAT:** Evan "3" -> committed the brief+refinements (77f1f62, pushed), then wrote the M11
prereg `docs/prereg_m11_chart_patterns.md` from the standing TEMPLATE. **Committing it
DOC-ONLY BEFORE the runner exists** (the sacred prereg-before-code ordering = the program's
core claim; this hash must predate `run_m11_chart_patterns.py`). Cadence #99 hit - this entry
satisfies it.

**DETECTOR SPEC (all params PINNED a priori, one consolidated long-side spec):** causal
close-based pivots (half-window w=5, confirmed at j+5, no two-sided smoother = no look-ahead);
signal = long reversal completion = **double-bottom** (two bottoms within 4%, intervening
peak >=5%, span 10-90d, neckline=peak) OR **inverse-H&S** (head >=3% below both shoulders,
shoulders within 6%, neckline=P1-P2 line); entry = **fresh upward neckline cross on close**
(close[i]>neck & close[i-1]<=neck), trough within 30d recency, execute next open; exit =
time-stop 20d baseline (10/40 descriptive); K=3, size NAV/K, oversub ranked by breakout
strength w/ dropped-count reported; 5bps + 15bps stress; A/B/C ladder. 39 survivor mega-caps
(asymmetric - only a FAIL clean). Full-window gate 2000-13 + sec 2014-> -> D1 tiers REACHABLE
(not modified-window). Plus a REPORTED-not-gated short-side diagnostic (double-top/H&S forward
returns) to document the Savin short-effect = non-deployable (X2 lesson).

**PRIOR (fixed): FAIL** - deployable long side weakest support; program-internal analogues
(E8/E11/C3 breakout kills, E16/C1 reversal decay, overnight gap) all point FAIL.

**STATE:** prereg written; committing doc-only now; runner NOT yet written. Tripwire GREEN.
Tally 33 (no run yet).

**Next action:** commit prereg doc-only -> build `run_m11_chart_patterns.py` (reuse
cache_fetch/UNIV/stats/D1 from C1) -> run -> D1 verdict -> results doc + record + tripwire.

# Appendix CO - M11 = FAIL (signal-dead); chart-pattern family closed; survivor bias DESTROYS the pattern edge (2026-07-14, ~22:55 CST)

**WHAT:** Built `scripts/run_m11_chart_patterns.py` (prereg `9cb5ac5` predates it) and ran it.
Causal close-based pivots (w=5, confirmed at j+5 -> no look-ahead), long reversal = double-
bottom OR inverse-H&S, fresh neckline cross at close -> next open, time-stop 20d, K=3, 39
survivors. 1,874 signal completions; 314 gate entries (>>30 floor). **VERDICT: FAIL both
tiers.** Tripwire GREEN. Writeup `docs/research/2026-07-14_M11_chart_patterns_results.md`.

**RESULTS (ladder):** MAIN C next-open 5bps gate **-0.14% CAGR / DD 50.4% / Sh 0.09**; sec
1.67% / 0.19. Rung B (next-open 0bps) gate **+0.61% ~= 0**; Rung A (c2c) -0.06% ~= B ->
**SIGNAL-DEAD** (no gross edge, and A~=B means no overnight-gap story either - unlike the IBS
family). Loses SPY (gate 1.72%) AND survivorship-clean EW-39 (gate -0.47%). Hold 10/40 don't
rescue (40d sec +6.06% = one-window bull artifact); NOT tuned. This is the E14 category
(signal-dead), the cleanest kind of negative.

**PAYLOAD - the survivor universe DESTROYS the one documented pattern edge (new, valuable):**
the reported-not-gated short-side diagnostic (fwd-20-session close return, never traded):
after a LONG-reversal (double-bottom/iH&S) completion = **+0.82%** (BELOW unconditional
**+1.15%**); after a BEARISH (double-top/H&S) completion = **+1.70%** (ABOVE unconditional).
That is the OPPOSITE in sign of Savin-Weller-Zvingelis (2007), who found H&S predicts
underperformance. **WHY: survivorship removed exactly the names a bearish pattern predicts**
- the stocks whose H&S correctly foretold a decline are the ones that fell out of the
universe; on a survivor mega-cap set a "top" is just a pause in a name that (by construction)
kept rising. So the survivor bias doesn't merely inflate long dip-buying (E16/C1) - it
STRUCTURALLY ERASES the documented (bearish) pattern edge. Cleanest asymmetric-falsification
illustration the program has produced.

**Every M11.1-brief prediction held:** LMW "informative != profitable"; deployable long side
weakest-supported; breakout kills (E8/E11/C3) + reversal decay (E16/C1) + overnight gap all
pointed FAIL. Confirmed.

**TALLY:** M11 = attempt 34, the **9th equity family** (chart-pattern geometry - first family
to trade *shape* not a *number*). **1 IN-SAMPLE-COMPOSED PASS-HR (M10-1, forward-only) + 1
weak PASS-RA (E18) / 0 clean high-return edges / 34 attempts.** Terminal claim upgraded: even
the chart SHAPES retail traders are taught don't trade at retail EOD, K=1-3, $100-1k. The
free autonomously-runnable backtest space is exhausted again; the one untested evidence lever
is M3 forward paper (Evan-gated). Cadence #99 (prior entry CN); capstone §3/§7/§8 + PRD M11 +
HANDOFF + memory updated.

**STATE:** committing runner + results + doc updates (prereg already committed `9cb5ac5`).
Tripwire GREEN. swing.db untouched.

**Next action:** commit M11; on Evan's word, push. The only lever that could validate M10-1
= M3 forward paper (Evan-gated: Alpaca paper account).

# Appendix CP - M3 forward-paper infrastructure BUILT; BLOCKED-ON-EVAN for keys (2026-07-15, ~01:29 CST)

**WHAT:** Evan: "set up M3 forward paper and make a spot (file) to paste the keys into."
Recon first: read Trading's alpaca_client.py/paper_trader.py (read-only reference, per the
established port-not-import rule) and the exact signal code in run_e6_deleveraged.py /
run_e18_regime_gates.py / run_m10_1_nagel_switch.py.

**ADAPTATION (dated decision):** PRD M3 tasks 14/18 (written 2026-07-08, M0 era) named two
sleeves `e1_control`/`e1_llm_veto` -- but E1 FAILED and was shelved in M2b (2026-07-09);
those names no longer correspond to anything worth forward-testing. Adapted to the three
REAL forward-paper candidates per every HANDOFF entry since: **e6_1x** (E6, prereg
0526ea2), **e18_vixts** (E18 arm a, prereg f32b008), **m10_1_nagel** (M10-1 -- the program's
FIRST PASS-HR, IN-SAMPLE-COMPOSED -- the one M3 exists to actually validate). LLM-overlay
(M9 task 51) untouched, stays separate/later.

**BUILT:**
- `swing_bot/paper_sleeves.py` -- sleeve DB schema (paper_sleeves/paper_positions/
  paper_transactions/paper_nav/fill_divergence, NEW tables, doesn't touch pinned `bars`
  rows or anything test_frozen.py reads) + decide_e6_1x/decide_e18_vixts/decide_m10_1, each
  reusing the IDENTICAL signal condition as its backtest runner (same SMA200 window, same
  VIX threshold, same residual_series FF3 machinery) -- load-bearing for M3's
  "implementation fidelity vs shadow backtest" success criterion (PRD task 51 amendment).
- `swing_bot/alpaca_client.py` -- ported (NOT imported) from Trading's alpaca_client.py.
  ~180-line httpx wrapper, PAPER base URL default, refuses a live base_url without explicit
  allow_live=True (nothing in this project's scripts passes it -- belt+suspenders on top of
  the base_url guard), reads credentials from alpaca_keys.env with OS-env fallback.
- **`alpaca_keys.env`** (project root) -- THE SPOT TO PASTE KEYS INTO. Confirmed gitignored:
  `git check-ignore -v alpaca_keys.env` -> matched `.gitignore:18:*.env` -> CONFIRMED
  IGNORED (checked BEFORE writing anything else, non-negotiable for a secrets file).
  Placeholder fields (APCA_API_KEY_ID/SECRET/BASE_URL pinned to paper) + instructions +
  SWING_ALPACA_SLEEVE selector (which ONE sleeve mirrors live; others stay swing.db-only,
  per the PRD's own established "one account, others DB-only" design from task 16).
- `scripts/daily_swing_paper.py` -- the daily loop. Design: ONE evening run suffices (no
  separate morning touch) -- realizes the PRIOR run's pending using TODAY's now-known open
  (today's full bar is complete by evening), then stores TODAY's close signal as pending for
  TOMORROW. Exactly mirrors every backtest runner's own signal-at-close/execute-next-open
  timing. Dry-run default; --execute mirrors ONE sleeve to Alpaca as a notional order
  matching the DB ledger 1:1 (NAV-sized).

**DRY-RUN CAUGHT + FIXED A REAL BUG (the value of testing before claiming done):**
running the script twice on the SAME still-latest session filled the pending order against
its OWN signal day's open -- one day too early, non-idempotent. Fixed: `realize_pending`
now requires `today > pending_signal_date` (strictly later session). Verified: two
consecutive same-day runs correctly both show filled-today=False, target unchanged. Test
artifacts (the buggy fills) were deleted from swing.db's new paper_* tables afterward (my
own dry-run data this session, safe to clean per standing rule) -- reset to a clean slate so
the first REAL invocation unambiguously starts the forward-paper evidentiary clock.

**TWO OPERATIONAL FINDINGS (disclosed, not bugs -- the dry run exercising real yfinance
data surfaced both):**
- Yahoo's same-session bar can be INCOMPLETE for hours after close (verified directly:
  yfinance showed 2026-07-14's Close as NaN while Open/Volume were populated, hours into
  2026-07-15). swing_bot.prices.fetch already (correctly, pre-existing behavior) drops any
  NaN O/H/L/C row -> the script safely fell back to 07-13 as the latest COMPLETE session.
  Operational implication for scheduling (task 19, not yet done): run late evening
  (~8-9pm ET), not right at 4pm ET close.
- **^VIX3M lags ^VIX by >=1 session** (verified directly: VIX3M had literally no row for
  the session VIX did have). decide_e18_vixts correctly returns None with a stated reason
  when this happens -- sleeve holds its current position, never guesses. Confirmed this
  fires safely in the actual dry run (e18_vixts showed "SKIPPED (VIX or VIX3M unavailable
  today)" both runs, no crash, no bad trade).

**Frozen tripwire GREEN** (12 refs d=0) both before and after -- new tables only, orthogonal
to the pinned `bars` rows.

**BLOCKED-ON-EVAN (explicit, reported not worked around):**
1. Create/choose an Alpaca PAPER account (recommend a NEW dedicated one, not one of
   Trading's ~3, so the two separate projects' order flow never mixes) + generate keys ->
   paste into alpaca_keys.env. Claude does not do this and never sees the resulting keys.
2. Choose SWING_ALPACA_SLEEVE. Recommendation (not decided on Evan's behalf): start with
   `e6_1x` (simplest, single-instrument, lowest risk of a plumbing bug corrupting the
   evidence trail), verify clean cycles, then upgrade to `m10_1_nagel` (the sleeve M3
   actually exists to test) once proven.
3. Smoke-test: `.venv\Scripts\python.exe -m swing_bot.alpaca_client` once keys are in.
4. The after-hours DAY-limit order-queuing assumption is explicitly UNVERIFIED until a real
   cycle runs (disclosed, not assumed true).

**EXPLICITLY NOT DONE (deliberate scope boundary, stated plainly):** Task 19 scheduling (no
Windows Task Scheduler entry -- an unattended process submitting real order flow to a live
brokerage API needs Evan's explicit setup/confirmation, not auto-scheduled); task 20's
20-day stabilization (can't be "set up," starts once real runs begin); the LLM overlay
(M9 task 51, separate/later).

Setup notes: `docs/research/2026-07-15_M3_forward_paper_setup.md`. PRD M3 tasks 14/16/17
updated with outcomes + adaptation note; milestone table row updated; HANDOFF snapshot
added.

**TALLY unchanged** (34 attempts -- this is infrastructure, not an experiment; no D1
verdict). Cadence: this entry + earlier CN/CO/CP work covers cadence through ~#101.

**STATE:** all new files UNCOMMITTED (Evan has not yet said "commit"/"push" for this work).
swing.db has 5 new empty tables (paper_sleeves etc.), reset clean after bug-fix testing.
alpaca_keys.env exists locally, confirmed gitignored, contains NO real keys (placeholders
only).

**Next action:** on Evan's word, commit (alpaca_keys.env will NOT be included, per
.gitignore) + push. Then genuinely blocked until Evan pastes in Alpaca keys and picks
SWING_ALPACA_SLEEVE.

# Appendix CQ - M3 rewired to 3-account model; all 3 Alpaca paper accounts VERIFIED CONNECTED (2026-07-15, ~02:15 CST)

**WHAT:** Evan made **3 separate Alpaca paper accounts, $1,000 each (one per sleeve)** -- a
better design than the single-mirror model from Appendix CP -- and pasted per-sleeve keys
into alpaca_keys.env with a new format: E_SIX_KEY/SECRET (e6_1x), E_EIGHTEEN_VIX_TS_KEY/
SECRET (e18_vixts), M_TEN_ONE_KEY/SECRET (m10_1_nagel), shared
APCA_API_BASE_URL=https://paper-api.alpaca.markets/v2. Rewired the code to match; verified
all 3 connect.

**TWO REAL ISSUES CAUGHT IN THE NEW FORMAT + FIXED IN CODE (not by editing Evan's keys):**
1. The base URL now ends in `/v2`, but request paths already prepend `/v2/...` -> would
   double to `/v2/v2/account`. Fixed: `_normalize_base()` strips a trailing `/v2` (and
   slashes), so both forms work. Verified: the smoke test's actual GET hit
   `/v2/account` correctly (200 OK).
2. Alpaca REJECTS notional+limit orders (notional must be market). My earlier --execute used
   a notional LIMIT -> would have failed on the first real order. Fixed: buys are now MARKET
   NOTIONAL DAY orders (canonical fractional order; DAY-TIF still queues for next open when
   sent after hours). submit_order() now raises if notional+non-market is attempted.

**CODE CHANGES:**
- `swing_bot/alpaca_client.py`: SLEEVE_ENV_PREFIX map (sleeve -> env prefix) +
  `client_for_sleeve(name)` factory (builds a client from that sleeve's own key pair);
  base-URL normalization; `close_position` + `cancel_all_orders` (for the flatten step);
  submit_order notional+limit guard; smoke test now loops ALL 3 accounts.
- `scripts/daily_swing_paper.py` --execute: rewired from single-sleeve (SWING_ALPACA_SLEEVE,
  now obsolete) to mirror ALL 3 sleeves, each to its own account, with a proper
  flatten-then-enter reconcile (cancel open orders -> close held symbols not in target ->
  buy target legs as market-notional-DAY sized to the sleeve's DB NAV).
- `alpaca_keys.env`: comment block updated (SWING_ALPACA_SLEEVE section replaced with the
  3-account note). Evan's key lines untouched. Still gitignored (re-confirmed).
- `.gitignore`: added `var/` (the Alpaca X-Request-ID runtime log dir; no secrets, but a
  runtime artifact).

**VERIFICATION (the valuable part -- read-only, no orders placed):**
`.venv\Scripts\python.exe -m swing_bot.alpaca_client` -> **all 3 accounts 200 OK, ACTIVE,
$1,000 cash each**, distinct account numbers (PA38ZZKY6WN0 / PA3W9UGPNIU4 / PA37SB3WCFTP).
Keys work; the 3-account isolation is real. Base-URL normalization confirmed live. Dry-run
of the daily loop still intact after the refactor; paper_* tables reset to clean slate so
the official forward-paper clock starts fresh on the first real run. Frozen tripwire
unaffected (no computation touched).

**DID NOT place any orders.** Markets are closed and, more to the point, submitting orders
(even paper) is a side-effectful action Evan hasn't explicitly asked for yet ("set up" +
provide keys != "start trading tonight"), and tonight's data is mid-transition (07-14 bar
still incomplete on yfinance, so "latest complete session" is 07-13). The first `--execute`
cycle -- and whether Alpaca queues an after-hours DAY order for the next open -- remains
the one genuinely unverified assumption; it should be run deliberately (ideally scheduled
late-evening on a complete session) with Evan's go.

**REMAINING GATES (much smaller than CP):** (1) decision/authorization to actually start
placing paper orders (run `--execute`, or schedule it); (2) Task Scheduler entry (task 19,
still not created -- unattended real order flow needs Evan's explicit setup); (3) the
after-hours order-queuing behavior, unverified until the first live cycle. Account creation +
keys (CP gates 1-3) are now DONE.

**TALLY unchanged** (34 attempts -- infra). Keys are PAPER (PK-prefix), never printed here,
never committed (gitignored). **STATE:** code + doc changes UNCOMMITTED pending Evan's word;
alpaca_keys.env holds real keys locally, gitignored, will not be in any commit.

**Next action:** on Evan's word, commit + push (keys excluded). Then either authorize the
first `--execute` run / scheduling, or leave it staged for Evan to kick off.

# Appendix CR - M3 committed+pushed; daily scheduled task registered (all 3 sleeves, live at 7pm) (2026-07-15, ~02:40 CST)

**WHAT:** Evan: "commit and push it, the[n] set a task that should start all the sleeves at
the same time."

**COMMIT+PUSH:** the full M3 forward-paper build (CP+CQ work) committed `503b606`, pushed to
origin/main. Secrets-guarded: `git status --porcelain | grep keys.env` returned nothing ->
alpaca_keys.env NOT in the commit (gitignored); swing.db + var/ also excluded. 9 files
(paper_sleeves.py, alpaca_client.py, daily_swing_paper.py, setup doc, .gitignore, HANDOFF,
PRD, record, pm-cadence).

**SCHEDULED TASK (task 19, finally done):**
- `scripts/daily_swing_paper.bat` -- pure ASCII (cmd.exe hard rule), cd /d project root ->
  `.venv\Scripts\python.exe scripts\daily_swing_paper.py --execute` -> append stdout+stderr
  to `var\daily_swing_paper.log`. ONE invocation runs ALL 3 sleeves together (e6_1x/
  e18_vixts/m10_1_nagel), so "all sleeves start at the same time" as Evan asked -- not 3
  staggered tasks.
- Registered via Register-ScheduledTask as **"SwingTradingDailyPaper"**: Weekly Mon-Fri at
  **19:00 local (-05:00 confirmed = CDT, matches the project's CST convention)**,
  StartWhenAvailable (catches up if the box was asleep), 30-min execution limit,
  MultipleInstances=IgnoreNew. Verified: State=Ready, Action=`cmd.exe /c "...daily_swing_
  paper.bat"`, Days=62 (=Mon+Tue+Wed+Thu+Fri bitmask), **NextRun = 2026-07-15 19:00** (TODAY).
- Verified the .bat's cd+venv+script+log-redirect chain in a DRY-RUN (cmd /c, no --execute)
  -> exit 0, correct per-sleeve output. Did NOT run --execute (no orders placed by me).

**FIRST LIVE RUN = TODAY 2026-07-15 19:00 CDT.** That scheduled run is the acceptance test
for the order-mirror path (flatten-then-enter), which is written but UNEXERCISED against real
fills. At 7pm only e6_1x will act (QQQ>200DMA -> ~$1,000 market-notional DAY buy queuing for
next open); e18_vixts waits on VIX3M availability, m10_1_nagel on Friday's weekly decision.
Evan should review `var\daily_swing_paper.log` after 7pm; fill_divergence + the Alpaca order
ids make the first fills auditable. Reset paper_* to a clean slate + fixed the script's now-
stale "not scheduled" closing message so the 7pm run makes the first REAL decision.

**Cadence #105 satisfied by this entry.** TALLY unchanged (34 -- infra). STATE: the .bat +
script-message fix + these doc updates are a SECOND commit (below), pushed per Evan's "commit
and push."

**Next action:** commit+push the scheduler artifacts; then genuinely hands-off -- the task
runs itself at 7pm. Watch the first run's log. If the order-mirror path errors, fix from the
log and the accounts can be flattened (paper). The 20-day stabilization window (task 20)
starts accumulating from tonight.
