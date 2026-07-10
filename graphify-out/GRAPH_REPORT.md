# Graph Report - D:/ClaudeCode/Swing Trading  (2026-07-10)

## Corpus Check
- 69 files · ~56,565 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 281 nodes · 511 edges · 13 communities (12 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 19 edges (avg confidence: 0.82)
- Token cost: 287,944 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Project Foundations & IBS Core|Project Foundations & IBS Core]]
- [[_COMMUNITY_Research Sources & E8-E12 Preregs|Research Sources & E8-E12 Preregs]]
- [[_COMMUNITY_E8-E12 Runner Code|E8-E12 Runner Code]]
- [[_COMMUNITY_E3 Stocks & OHLCV Fetcher|E3 Stocks & OHLCV Fetcher]]
- [[_COMMUNITY_IBS Backtests (E1E1bE2) & Engine|IBS Backtests (E1/E1b/E2) & Engine]]
- [[_COMMUNITY_Fill-Timing Ablation & Screens|Fill-Timing Ablation & Screens]]
- [[_COMMUNITY_MA Rotation Engine (E4) & Frozen Tests|MA Rotation Engine (E4) & Frozen Tests]]
- [[_COMMUNITY_Leverage-Rotation Findings (E4-E7)|Leverage-Rotation Findings (E4-E7)]]
- [[_COMMUNITY_E5 Regime Test|E5 Regime Test]]
- [[_COMMUNITY_E6 De-Leveraged Rotation|E6 De-Leveraged Rotation]]
- [[_COMMUNITY_E7 International Test|E7 International Test]]
- [[_COMMUNITY_Coverage & Quality Gate|Coverage & Quality Gate]]
- [[_COMMUNITY_Package Init|Package Init]]

## God Nodes (most connected - your core abstractions)
1. `HANDOFF.md — the only live project snapshot` - 23 edges
2. `PRD_ROADMAP.md — standing experimental program plan (M0–M6)` - 18 edges
3. `Project Record — append-only chronological history (ground truth)` - 17 edges
4. `Findings write-up — falsification program E1→E7 (the deliverable)` - 15 edges
5. `Experiment Catalog v2 (grounded in measured E1/E1b/E2 data)` - 13 edges
6. `E1 — ETF IBS mean reversion, 29 ETFs (FAIL: Sharpe 0.23, maxDD 36%)` - 12 edges
7. `Research Brief — Small-Account Swing Strategies (2026-07-08)` - 12 edges
8. `E10+E11+E12 Results — All FAIL (article-set arc)` - 11 edges
9. `IBS Mean Reversion on Equity ETFs (E1 family)` - 10 edges
10. `E8+E9 Results — Both FAIL (squeeze breakout; never-book-a-loss audit)` - 10 edges

## Surprising Connections (you probably didn't know these)
- `E12 — confirmed-capitulation mean reversion (FAIL; confirmation bar surrenders the edge)` --semantically_similar_to--> `E1 — ETF IBS mean reversion, 29 ETFs (FAIL: Sharpe 0.23, maxDD 36%)`  [INFERRED] [semantically similar]
  HANDOFF.md → docs/prereg_E1_ibs.md
- `Asymmetric-falsification design (only a FAIL is interpretable)` --semantically_similar_to--> `E9 — 'never book a loss' deep-dip audit (FAIL; claim literally true but bad)`  [INFERRED] [semantically similar]
  docs/prereg_E3_stock_momentum.md → HANDOFF.md
- `requirements.txt — pinned runtime deps (yfinance, httpx)` --conceptually_related_to--> `Own yfinance fetcher (swing_bot/prices.py, auto_adjust=False) — M0.2 data-path decision`  [INFERRED]
  requirements.txt → .claude/codebase-memory/architecture.md
- `EOD-only hard rule (signal at close, execute next open)` --conceptually_related_to--> `Fill-timing ablation (close-to-close vs next-open vs overnight-only)`  [INFERRED]
  CLAUDE.md → PRD_ROADMAP.md
- `features bin (empty at bootstrap — no code yet)` --references--> `HANDOFF.md — the only live project snapshot`  [EXTRACTED]
  .claude/codebase-memory/features.md → HANDOFF.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **IBS Mean-Reversion Family (E1 → E1b → E2, shelved by pre-committed stop)** — docs_prereg_e1_ibs_e1, docs_prereg_e1b_broad_us_e1b, docs_prereg_e2_leveraged_ibs_e2, docs_prereg_e1_ibs_ibs_indicator, docs_findings_2026_07_09_experiment_arc_overnight_gap_haircut [EXTRACTED 1.00]
- **200-MA Rotation Family (E4 pass → E5 regime kill → E6 1x overlay → E7 international close)** — docs_prereg_e4_rotation_e4, docs_prereg_e5_rotation_regime_e5, docs_prereg_e6_deleveraged_rotation_e6, docs_prereg_e7_international_e7, docs_prereg_e4_rotation_200day_ma_rotation [EXTRACTED 1.00]
- **Falsification Program — 13 pre-registered attempts, 6 families, 0 passes** — docs_prereg_e1_ibs_e1, docs_prereg_e1b_broad_us_e1b, docs_prereg_e2_leveraged_ibs_e2, docs_prereg_e3_stock_momentum_e3, docs_prereg_e4_rotation_e4, docs_prereg_e5_rotation_regime_e5, docs_prereg_e6_deleveraged_rotation_e6, docs_prereg_e7_international_e7, handoff_e8_squeeze_breakout, handoff_e9_deep_dip_audit, handoff_e10_post_earnings_drift, handoff_e11_volume_gated_breakout, handoff_e12_confirmed_capitulation_mr, prd_roadmap_preregistration_discipline [EXTRACTED 1.00]
- **IBS Mean-Reversion Experiment Family (E1 → E1b → E2 → shelved)** — research_2026_07_08_small_account_swing_strategies_ibs_mean_reversion, research_2026_07_09_e1_power_e1_power_calculation, research_2026_07_09_e1_fill_timing_ablation_fill_timing_ablation, research_2026_07_09_e1_backtest_results_e1_results, research_2026_07_09_e1b_broad_us_results_e1b_results, research_2026_07_09_e2_leveraged_results_e2_results, research_2026_07_09_e2_leveraged_results_ibs_family_stop [EXTRACTED 1.00]
- **200-MA Leverage Rotation Family (B4 screen → E4 → E5 → E6 → E7)** — research_2026_07_09_screen_results_b4_vol_regime_rotation_screen, research_2026_07_09_e4_rotation_results_e4_results, research_2026_07_09_e5_regime_results_e5_results, research_2026_07_09_e6_deleveraged_results_e6_results, research_2026_07_10_e7_international_results_e7_results, research_2026_07_09_e4_rotation_results_200ma_leverage_rotation [EXTRACTED 1.00]
- **Program-Wide Falsification (0 PASS / 13 attempts across 6 families)** — research_2026_07_10_e10_e11_e12_results_program_falsification, research_2026_07_10_e3_stock_momentum_results_e3_results, research_2026_07_10_e7_international_results_e7_results, research_2026_07_10_e8_e9_results_e8_e9_results, research_2026_07_10_e10_e11_e12_results_e10_e11_e12_results [EXTRACTED 1.00]

## Communities (13 total, 1 thin omitted)

### Community 0 - "Project Foundations & IBS Core"
Cohesion: 0.07
Nodes (63): EOD-only hard rule (signal at close, execute next open), Mandatory liquidity floor in universe filters, CLAUDE.md — Swing Trading project instructions, architecture bin — data layer + Trading-repo relationship, Own yfinance fetcher (swing_bot/prices.py, auto_adjust=False) — M0.2 data-path decision, swing.db — project SQLite (bars table PK ticker,date; positions/NAV/results), D:\ClaudeCode\Trading — sibling repo (read-only from this project), conventions bin — doc system + code conventions (+55 more)

### Community 1 - "Research Sources & E8-E12 Preregs"
Cohesion: 0.08
Nodes (50): Five-Source Swing-Trading Article Set (Swing Trading Research.md), E10 Pre-registration — Post-Earnings-Announcement Drift, Post-Earnings-Announcement Drift (PEAD), E11 Pre-registration — Volume-Gated Consolidation Breakout, RVOL ≥ 1.5 Volume-Confirmation Gate, Confirmed-Capitulation Mean Reversion ('Right Side of the V'), E12 Pre-registration — Confirmed-Capitulation Mean Reversion, Split-Adjusted / Dividend-UNadjusted Data Convention (auto_adjust=False) (+42 more)

### Community 2 - "E8-E12 Runner Code"
Cohesion: 0.09
Nodes (27): earnings_dates(), main(), E10 - post-earnings-announcement drift (PEAD), per prereg 129dc22. FALSIFICATION, stats(), gate_entry_by_volume(), main(), E11 - volume-gated consolidation breakout, per prereg 129dc22.  E8 IDENTICAL rul, AND E8's entry array with RVOL>=1.5 on the breakout bar. (+19 more)

### Community 3 - "E3 Stocks & OHLCV Fetcher"
Cohesion: 0.10
Nodes (21): Backfill the frozen ETF universe into swing.db via swing_bot.prices.  Idempotent, main(), PRESSURE-TEST (exploratory, CONTAMINATED) — can a volatility gate save 3x levera, run(), stats(), synth3(), load(), main() (+13 more)

### Community 4 - "IBS Backtests (E1/E1b/E2) & Engine"
Cohesion: 0.11
Nodes (20): main(), M2.10 — run E1 per pre-registration (8963e49) and judge kill criteria.  Primary, Copy bars in [start,end] into an in-memory DB (keeps engine frozen)., show(), subset_db(), main(), E1b — broad_us IBS mean reversion, out-of-sample test per prereg 0126ce3.  Gate, show() (+12 more)

### Community 5 - "Fill-Timing Ablation & Screens"
Cohesion: 0.20
Nodes (14): main(), mean(), M1.8 fill-timing ablation (PRD #15 + #13).  Per-signal DIAGNOSTIC (not the backt, a3_screen(), b1_screen(), b4_screen(), load(), main() (+6 more)

### Community 6 - "MA Rotation Engine (E4) & Frozen Tests"
Cohesion: 0.17
Nodes (11): main(), met(), mopct(), E4 — 200d-MA leverage rotation, per prereg 313d88a. No tuning.  PRIMARY cell: QQ, buy_hold(), Moving-average leverage-rotation engine for swing_bot (E4).  Implements the froz, run_rotation(), _series() (+3 more)

### Community 7 - "Leverage-Rotation Findings (E4-E7)"
Cohesion: 0.30
Nodes (12): 200-Day MA Leverage Rotation (QQQ signal → hold TQQQ / cash), E4 200d-MA Leverage Rotation Results — PASS (33.76% CAGR), Regime Flattery (leverage × a secular bull), E5 Hostile-Regime Test Results — FAIL (E4 de-authorized, 92.7% DD), Synthetic 3× Fund Validation (drag-calibrated, corr 0.9989 to real TQQQ), Whipsaw Failure Mode in Secular Bear Markets, 1× 200-MA Drawdown-Management Overlay, E6 De-Leveraged 1× Rotation Results — PASS (first robust regime-spanning result) (+4 more)

### Community 8 - "E5 Regime Test"
Cohesion: 0.29
Nodes (7): corr(), main(), E5 — E4 rotation across 2000-2013 hostile regimes, per prereg 09a3a31.  Synthesi, Daily-rebalanced 3x from QQQ returns, drag d_annual/yr. Returns     {date: (syn_, series(), stats(), synth_3x()

### Community 9 - "E6 De-Leveraged Rotation"
Cohesion: 0.44
Nodes (8): bh(), calib(), main(), E6 — de-leveraged 200-MA rotation as a drawdown overlay, per prereg 0526ea2.  PR, rotation_nav(), series(), stats(), synth()

### Community 10 - "E7 International Test"
Cohesion: 0.39
Nodes (8): bh(), load(), main(), E7 — international validation across unseen regimes, per prereg 70ed2a1.  Arm 1:, rotation(), stats(), synth(), vol_series()

### Community 11 - "Coverage & Quality Gate"
Cohesion: 0.33
Nodes (8): coverage(), latest_common_date(), main(), Data coverage + quality gate for swing_bot.  The daily loop must NOT emit signal, Return (ok, missing) for as_of (ISO 'YYYY-MM-DD').      missing = tickers listed, Most recent date for which every currently-listed ticker has a bar.     Used as, Return a list of (ticker, date, kind, detail) anomalies., sanity_scan()

## Knowledge Gaps
- **17 isolated node(s):** `E10 — post-earnings drift / PEAD (FAIL clean; real-but-small, decayed after ~2010)`, `IBS indicator: (close − low) / (high − low), entry <0.20, exit >0.80 or 5-day time stop`, `Prereg E1b — broad-US IBS out-of-sample test (commit 0126ce3)`, `Prereg E3 — concentrated stock momentum, falsification-only (commit 87bc8d9)`, `Prereg E4 — 200-day-MA leverage rotation TQQQ/QQQ (commit 313d88a)` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `M1.8 fill-timing ablation (PRD #15 + #13).  Per-signal DIAGNOSTIC (not the backt`, `Backfill the frozen ETF universe into swing.db via swing_bot.prices.  Idempotent`, `PRESSURE-TEST (exploratory, CONTAMINATED) — can a volatility gate save 3x levera` to the rest of the system?**
  _66 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Foundations & IBS Core` be split into smaller, more focused modules?**
  _Cohesion score 0.07219662058371736 - nodes in this community are weakly interconnected._
- **Should `Research Sources & E8-E12 Preregs` be split into smaller, more focused modules?**
  _Cohesion score 0.08489795918367347 - nodes in this community are weakly interconnected._
- **Should `E8-E12 Runner Code` be split into smaller, more focused modules?**
  _Cohesion score 0.08912655971479501 - nodes in this community are weakly interconnected._
- **Should `E3 Stocks & OHLCV Fetcher` be split into smaller, more focused modules?**
  _Cohesion score 0.09686609686609686 - nodes in this community are weakly interconnected._
- **Should `IBS Backtests (E1/E1b/E2) & Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.10869565217391304 - nodes in this community are weakly interconnected._