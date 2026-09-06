# performance — Swing Trading

- 2026-07-08: empty — no code yet. **Superseded 2026-09-05 below.**
- 2026-09-05 (F3 sweep, record FN, measured on this machine with a warm
  `.e8e9_cache`): `run_e8_squeeze.py` **2.2 s** per full run (29 ETFs, 2000→);
  E9/E11/E12 comparable; `run_c3_vol_breakout.py` **~60 s per arm** (it runs
  five rung/arm variants); E20 and X9 each under 10 s. **One complete F3 sweep
  — 8 experiments × 2 arms × 2 repeats for determinism = 32 runs — finished
  in under 5 minutes.** `liquidity_mask` over 29 series × ~6,500 bars adds no
  measurable time. The cost that dominates is a COLD cache: `cache_fetch`
  retries on a 20/40/60/80 s ladder per ticker on a miss.
- 2026-09-05: `test_frozen` (12 pinned refs + 17 invariants against the real
  `bars` table) runs in well under a minute; it was run eight times this
  session without being the bottleneck once.
