# DIRECTORY — Swing Trading

The tree map. Created 2026-09-05 (PRD M13.7, record FL): the memory system
prescribes this bin past ~15 files and this repo has **208 tracked files**, so
it went five weeks without one.

**Every count below is grepped, not eyeballed.** Reproduce them all:

```bash
git -c core.quotePath=false ls-files | wc -l                                  # 208 total
git -c core.quotePath=false ls-files | awk -F/ 'NF==1{print "(root)"} NF>1{print $1}' | sort | uniq -c | sort -rn
git -c core.quotePath=false ls-files docs | awk -F/ 'NF==2{print "docs/(root)"} NF>2{print "docs/"$2}' | sort | uniq -c
git ls-files 'scripts/run_*.py' | wc -l                                       # 39 runners
git ls-files 'scripts/prove_*.py' | wc -l                                     # 5 proofs
git ls-files 'docs/prereg*' | wc -l                                           # 44 preregs
```

`core.quotePath=false` matters: the record's filename contains an em dash, and
without it git quotes the path and `awk -F/` counts it as its own directory (a
first pass here reported 105 docs + a phantom `"docs` bucket instead of 107).

## Counts at 2026-09-05 (208 tracked at HEAD; **210 by 2026-09-06**)

**Tense warning, found by the 2026-09-06 landing-check:** these were counted from `git ls-files`, which sees only what is TRACKED. This file and `disclosure.md` were untracked when it ran, so an earlier version of this heading said "0 untracked" while being one of the two untracked files. A count taken from inside its own change set is stale the moment it lands - re-derive after committing, not before.

| path | files | what lives there |
|---|---|---|
| `docs/` | **107** | 51 at root + 56 in `research/` |
| `scripts/` | **59** at 2026-09-06 (58 at 2026-09-05; `prove_torn_write.py` added) | 55 `.py` + `daily_swing_paper.bat` + `git-hooks/pre-commit` + `.gitkeep` |
| `swing_bot/` | **14** | the importable package: engines, ledger, guards, tripwire |
| `.claude/` | **15** (13 at the 2026-09-05 HEAD) | codebase-memory bins + `pm-cadence.json`; DIRECTORY.md and disclosure.md are the two not yet tracked |
| (root) | **9** | see below |
| `graphify-out/` | **6** | the knowledge-graph build outputs (cache is gitignored) |
| `data/` | **1** | `fomc_announcement_dates.json` |

## Root (9 files)

`CLAUDE.md` · `HANDOFF.md` (the ONLY live snapshot — read first) ·
`PRD_ROADMAP.md` · `README.md` (public-facing) · `requirements.txt` ·
`requirements.lock` · `.gitignore` · `.gitattributes` ·
`clean_ledger_2026-08-25.py` (kept because record FJ references it — do not
delete without Evan).

## `swing_bot/` — the package (14 files)

`__init__.py` also holds `DB_PATH`, the single home for the project DB path
since 2026-09-05 (M13.6); `prices.py` and `paper_sleeves.py` re-export it.
Core: `prices.py` (own yfinance fetcher → `swing.db bars`) · `backtest.py` (the
PINNED engine — `liq=None` is the pinned path) · `paper_sleeves.py` (the M3
ledger + per-sleeve signal logic) · `alpaca_client.py` (broker) ·
`universe.py` (frozen universe + the liquidity floor and `median_dollar_volume`
beside it) · `trading_calendar.py` (the independent clock, NEW 2026-09-05) ·
`costs.py` · `test_frozen.py` (the tripwire).

## `scripts/` — 39 runners, 5 proofs, 1 orchestrator

- **`daily_swing_paper.py`** is THE live orchestrator (+ its `.bat`, fired by
  the Windows task `SwingTradingDailyPaper`, weekdays 19:00 CT). Never run it
  by hand in a dev session.
- **`run_*.py` (39)** — one per pre-registered experiment. `run_e8_squeeze.py`
  owns `cache_fetch`, the repo's real shared data layer for the experiment
  jungle.
- **`prove_*.py` (5)** — standalone proofs, each runnable with no network and
  no DB: `prove_cache_guard` 8/8 · `prove_refusal_gate` 10/10 ·
  `prove_liquidity_floor` 11/11 · `prove_feed_clock` 18/18 ·
  `prove_divergence_census` 16/16.
- `probe_feed_publication.py` — the M13.2 timing instrument (hand-run).

## `docs/` — 107 files

- **`Project Record — Full Chronological History.md`** — append-only ground
  truth, 9,781 lines / 177 appendices at HEAD (9,998 / 179 on disk with FV and FW uncommitted). Appended ONLY via
  `~/.claude/skills/project-memory/append-record-entry.js`.
- **44 `prereg_*`** — one per pre-registered experiment, always committed
  DOC-ONLY before any runner code.
- **`research/` (56)** — the results write-up per experiment.
- Cross-cutting: `CAPSTONE_program_synthesis.md`,
  `findings_2026-07-09_experiment_arc.md`, `M12_constraint_relaxation_plan.md`,
  `trial_log.json` + `trial_log_notes.md`.

## Not in git (see `.gitignore`)

`.venv/` · `swing.db` (+ journal/wal/shm) · `.e8e9_cache/` (292 files at
2026-09-05) · `var/` (M3 runtime logs) · `alpaca_keys.env` (via `*_keys.env`
and `*.env`) · the various `.<source>_cache/` research caches ·
`graphify-out/cache/`. See `disclosure.md` for what that boundary is protecting.
