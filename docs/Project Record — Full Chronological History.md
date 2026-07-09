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
