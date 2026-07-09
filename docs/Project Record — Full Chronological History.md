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
