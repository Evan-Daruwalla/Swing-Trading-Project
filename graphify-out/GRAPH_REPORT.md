# Graph Report - .  (2026-07-15)

## Corpus Check
- 161 files · ~169,492 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 381 nodes · 589 edges · 25 communities (24 shown, 1 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]

## God Nodes (most connected - your core abstractions)
1. `cache_fetch()` - 28 edges
2. `AlpacaClient` - 18 edges
3. `win()` - 10 edges
4. `report()` - 10 edges
5. `macro_close()` - 9 edges
6. `AlpacaError` - 9 edges
7. `main()` - 8 edges
8. `main()` - 8 edges
9. `main()` - 8 edges
10. `client_for_sleeve()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `client_for_sleeve()`  [EXTRACTED]
  scripts/daily_swing_paper.py → swing_bot/alpaca_client.py
- `main()` --calls--> `residual_series()`  [INFERRED]
  scripts/daily_swing_paper.py → scripts/run_c1_residual_reversal.py
- `main()` --calls--> `cache_fetch()`  [INFERRED]
  scripts/run_c1_residual_reversal.py → scripts/run_e8_squeeze.py
- `main()` --calls--> `report()`  [INFERRED]
  scripts/run_c1_residual_reversal.py → scripts/run_x6_crypto_trend.py
- `main()` --calls--> `report()`  [INFERRED]
  scripts/run_c3_vol_breakout.py → scripts/run_x6_crypto_trend.py

## Import Cycles
- None detected.

## Communities (25 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (42): main(), M2.10 — run E1 per pre-registration (8963e49) and judge kill criteria.  Primary, Copy bars in [start,end] into an in-memory DB (keeps engine frozen)., show(), subset_db(), main(), E1b — broad_us IBS mean reversion, out-of-sample test per prereg 0126ce3.  Gate, show() (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (33): load(), main(), C3 - consolidated volatility-breakout kill-shot, per prereg prereg_c3_vol_breako, Per-ticker: entry_sig[i]=True if signal at close i; exit uses 10d low., run(), signals(), gate_entry_by_volume(), main() (+25 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (15): Any, Path, AlpacaClient, AlpacaError, client_for_sleeve(), _load_keys_file(), _normalize_base(), Thin Alpaca Trading API client (PAPER by default), ported from D:\\ClaudeCode\\T (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (25): RuntimeError, main(), C6 - even-week FOMC-cycle overlay (CMVJ 2019), per prereg prereg_c6_fomc_cycle.m, stats(), main(), E14 - diversified sector momentum, per prereg f922f1f.  Top-3 of the 11 SPDR sec, stats(), classify_opportunistic() (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (16): Backfill the frozen ETF universe into swing.db via swing_bot.prices.  Idempotent, divs(), main(), E20 - dividend capture, per prereg d0642ad.  Buy close before ex-date, sell ex-d, stats(), coverage(), latest_common_date(), main() (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (18): main(), C4 - Moreira-Muir vol-targeting sizing overlay, per prereg prereg_c4_vol_sizing., stats(), main(), C7 - SVXY short-vol carry gated by VIX term structure, per prereg prereg_c7_svxy, stats(), fred_series(), macro_close() (+10 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (11): decide_e18_vixts(), decide_e6_1x(), decide_m10_1(), init_sleeve(), M3 forward-paper sleeve tracking: DB schema + per-sleeve signal decisions.  Thre, Verbatim copy of run_e18_regime_gates.sma (avoids importing a scripts/     modul, qqq_close_series: chronological list of QQQ closes ending at 'today'.     Target, Target = 100% QQQ iff VIX/VIX3M < 1.0, else cash. (E18 arm (a), prereg     f32b0 (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (16): main(), mean(), M1.8 fill-timing ablation (PRD #15 + #13).  Per-signal DIAGNOSTIC (not the backt, bh(), calib(), main(), E6 — de-leveraged 200-MA rotation as a drawdown overlay, per prereg 0526ea2.  PR, rotation_nav() (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.24
Nodes (11): classify(), e20_rungs(), main(), make_c2c(), pct(), EX-DECOMP (M9 #44) - execution/signal decomposition ladder on closed FAILs.  DIA, CAGR-based, benchmark-relative. a/b/c/null are gate-window CAGRs., Wrap a cache_fetch so each bar's open := prior close (c2c execution). (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.32
Nodes (10): main(), X7 - HYG:IEF credit-appetite regime gate, per prereg prereg_x7_credit_gate.md (c, a3_screen(), b1_screen(), b4_screen(), load(), main(), IN-SAMPLE SCREENS (2026-07-09) — hypothesis-GENERATING, NOT verdicts.  Three one (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.27
Nodes (10): fresh_ff3(), isoweek_str(), main(), mark_nav(), M3 forward-paper daily loop, per PRD M3 (task 14, adapted 2026-07-15 from the st, close_px: {ticker: close_price_today}., Always-fresh Ken French daily-factor fetch for live use -- deliberately     NOT, fill_open: {ticker: open_price_today}. Liquidates every current     position (se (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (8): ff3_daily(), isoweek(), main(), C1 - FF3-stripped residual reversal, per prereg prereg_c1_residual_reversal.md (, Per name: residual formation value at each index (or None)., residual_series(), main(), M10-1 - Nagel Switch: VIX-gated residual reversal / trend rotation. Per prereg p

### Community 12 - "Community 12"
Cohesion: 0.22
Nodes (9): detect(), detect_short(), main(), pivots(), M11 - Algorithmic chart-pattern detection (long-side reversal), per prereg prere, Bearish mirror (double-top / H&S), fresh DOWNWARD neckline cross. For the     re, Causal alternating swing highs/lows on close. Each pivot at idx j is     known o, Long reversal completion at bar i using pivots confirmed by i. Returns     break (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (9): form4_list(), get(), main(), parse_pbuys(), E19 ingestion (per prereg ebf54a4): SEC EDGAR Form-4 -> open-market insider PURC, (accession_nodash, primaryDocument, filingDate) for every Form-4., Return list of P-purchase (acquired) non-derivative transactions., raw_url() (+1 more)

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (7): corr(), main(), E5 — E4 rotation across 2000-2013 hostile regimes, per prereg 09a3a31.  Synthesi, Daily-rebalanced 3x from QQQ returns, drag d_annual/yr. Returns     {date: (syn_, series(), stats(), synth_3x()

### Community 15 - "Community 15"
Cohesion: 0.31
Nodes (7): earnings_dates(), main(), E10 - post-earnings-announcement drift (PEAD), per prereg 129dc22. FALSIFICATION, stats(), main(), E15 - earnings-announcement premium, per prereg 9b0aeb3.  Buy at open 5 sessions, stats()

### Community 16 - "Community 16"
Cohesion: 0.39
Nodes (8): bh(), load(), main(), E7 — international validation across unseen regimes, per prereg 70ed2a1.  Arm 1:, rotation(), stats(), synth(), vol_series()

### Community 17 - "Community 17"
Cohesion: 0.39
Nodes (7): build(), main(), per_year(), X2b - short-side / long-short days-to-cover, borrow-costed. Per prereg prereg_x2, mode 'ls' (dollar-neutral 1x/1x) or 'short' (1x short). Share-based with     rea, sim(), stats()

### Community 18 - "Community 18"
Cohesion: 0.53
Nodes (5): _get(), main(), parse_csv(), _post_csv(), Ingest FINRA consolidated exchange-listed short interest for the 39-name survivo

### Community 19 - "Community 19"
Cohesion: 0.47
Nodes (5): fetch(), main(), parse(), Ingest FINRA Reg SHO daily short-VOLUME for the 39 survivor large-caps (X3, PRD, Accumulate {sym: [shortvol, totalvol]} into acc from one venue file.

### Community 20 - "Community 20"
Cohesion: 0.53
Nodes (5): main(), PRESSURE-TEST (exploratory, CONTAMINATED) — can a volatility gate save 3x levera, run(), stats(), synth3()

### Community 21 - "Community 21"
Cohesion: 0.47
Nodes (5): main(), E13 - turn-of-the-month overlay, per prereg 0324196.  Long SPY on TOM-days (last, TOM-day = last trading day of its month OR first 3 trading days., stats(), tom_flags()

### Community 22 - "Community 22"
Cohesion: 0.60
Nodes (4): load(), main(), E3 — concentrated stock momentum, per prereg 87bc8d9. FALSIFICATION-ONLY: a FAIL, stats()

### Community 23 - "Community 23"
Cohesion: 0.50
Nodes (3): isoweek(), main(), X3 - Reg SHO daily short-volume drift, per prereg prereg_x3_regsho_svr.md (commi

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cache_fetch()` connect `Community 1` to `Community 3`, `Community 4`, `Community 5`, `Community 8`, `Community 9`, `Community 11`, `Community 12`, `Community 15`, `Community 17`, `Community 21`, `Community 23`?**
  _High betweenness centrality (0.369) - this node is a cross-community bridge._
- **Why does `AlpacaError` connect `Community 2` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `client_for_sleeve()` connect `Community 2` to `Community 10`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `cache_fetch()` (e.g. with `main()` and `load()`) actually correct?**
  _`cache_fetch()` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `win()` (e.g. with `main()` and `main()`) actually correct?**
  _`win()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `report()` (e.g. with `main()` and `main()`) actually correct?**
  _`report()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `macro_close()` (e.g. with `main()` and `main()`) actually correct?**
  _`macro_close()` has 6 INFERRED edges - model-reasoned connections that need verification._