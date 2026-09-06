# features — Swing Trading

- 2026-08-13 (record EO): no longer empty. Three mechanical sleeves run live in
  paper since 2026-07-15, each its own $1,000 Alpaca PAPER account: `e6_1x`
  (QQQ vs its 200-DMA), `e18_vixts` (VIX/VIX3M term-structure gate),
  `m10_1_nagel` (VIX>20 → C1 residual reversal, else E6 trend; weekly, Fridays).
  Decision functions live in `swing_bot/paper_sleeves.py`, each reusing the
  IDENTICAL condition as its backtest runner. Orchestrator:
  `scripts/daily_swing_paper.py`. Nothing has passed the high-return bar —
  these are forward EVIDENCE, not validated edges.
- 2026-07-08: empty — no code yet. Candidate strategies under evaluation are
  listed in HANDOFF.md; none implemented.

- Reviewed 2026-09-05: the three sleeves are unchanged; e6_1x has 31 NAV marks against its peers' 36 (holes acknowledged permanent, record FL); the research runners now enforce the liquidity floor (F3, record FN); the live loop has a feed-clock defect open as PRD M13.1 (record FP).
