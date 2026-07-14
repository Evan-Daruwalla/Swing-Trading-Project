# X3 — Reg SHO daily short-volume drift: RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_x3_regsho_svr.md` (doc-only, predates runner). **Runner:**
`scripts/run_x3_regsho_svr.py`. **Verdict: FAIL.** Frozen tripwire GREEN. The
program's final experiment (attempt 30).

## TL;DR

Executed short-**volume** carries essentially **no** cross-sectional signal — the
clean counterpoint to X2. The long-only lowest-SVR leg (K=5, weekly, next-open, 5 bps,
4,260 sessions 2009–2026) posts gate 13.00% CAGR / Sharpe 0.75 and secondary
10.85% / 0.64 — **losing to SPY on both CAGR and Sharpe** (gate SPY 14.80% / 0.91).
And the existence spread (low-SVR minus high-SVR) is **+1.24% / Sharpe 0.16** — the
two baskets returned 14.74% vs 12.05%, statistically indistinguishable. Whatever gross
lift the long leg shows is a least-shorted-large-cap beta tilt, not a short-volume
edge. This **confirms the ingest-time warning**: SVR is market-maker-hedging
microstructure noise, not informed shorting — where X2's short-**interest** spread was
a real +18.39% (short-side), X3's short-**volume** spread is ~0. Costs finish it
(15 bps → gate 1.83%, secondary negative). Reg SHO drift closed; the informed-
positioning family is complete.

## Results (2009-08-03 → 2026-07-10; 883 weekly cycles; K=5)

| leg | gate 2009–13 | secondary 2014– |
|---|---|---|
| **long C (next-open, 5bps)** | **13.00% / DD 27.1% / Sh 0.75** | 10.85% / 33.3% / 0.64 |
| long B (next-open, 0bps) | 19.03% / 24.6% / 1.03 | 16.79% / 29.7% / 0.92 |
| long A (c2c, 0bps) | 15.40% / 30.4% / 0.87 | 14.47% / 33.3% / 0.81 |
| long 15bps | 1.83% / 32.1% / 0.19 | −0.17% / 46.8% / 0.09 |
| SPY-BH | 14.80% / — / 0.91 | 11.98% / — / 0.74 |
| EW-39-BH | 11.34% / — / 0.68 | 13.97% / — / 0.78 |
| **spread low−high SVR** | **+1.24% / Sharpe 0.16** (low +14.74% vs high +12.05%) | |

**Verdict:** long-only C loses SPY on CAGR (13.00 < 14.80) and Sharpe (0.75 < 0.91) in
the gate → **FAIL** the PROMISING bar (883 cycles ≫ 30 floor; spread sign nominally
positive but economically ~0).

## Interpretation

- **SVR is noise; the near-zero spread is the whole story.** A real informed-shorting
  signal would separate the low- and high-SVR baskets; here they are within
  ~2.7 pp/yr at Sharpe 0.16. Executed short volume is dominated by wholesaler/MM hedge
  prints (SVR sits 25–52% for *everyone*), so ranking on it sorts on microstructure,
  not information — exactly the contamination flagged at ingest.
- **The clean X2/X3 contrast is the payload.** Same family, same universe, same
  machinery: short **interest** (X2, settlement positions) carries a real, correctly-
  signed, short-side anomaly (+18.39% spread) that nonetheless fails to be *tradeable*
  (X2b); short **volume** (X3, executed flow) carries essentially no cross-sectional
  signal at all. Both route to FAIL, for different and now-documented reasons.
- **Execution note:** next-open (B, 19.03%) beat c2c (A, 15.40%) here — the low-SVR
  basket had favorable overnight drift — but the 5 bps weekly-turnover cost (B→C
  −6 pp) and 15 bps stress erase it regardless.

## Program close

X3 completes the informed-positioning family (E19 insider, X2/X2b short-interest, X3
short-volume) and the M8 survey sweep. **Terminal tally: 0 PASS-HR / 1 weak PASS-RA /
30 pre-registered attempts / 8 families.** The entire documented, evidenced
swing-method space surveyed 2026-07-12 is now exhausted at retail EOD, K=1–3,
$100–1,000 — with no robust high-return edge, one weak risk-management overlay
(VIX-TS), and one real anomaly (short interest) that is structurally uncapturable.

## Reproduction
`.venv\Scripts\python.exe scripts/run_x3_regsho_svr.py`; tripwire GREEN (12 refs d=0).
Data: `scripts/ingest_regsho_short_volume.py` (`.regsho_cache/`, gitignored).

## Sources
Boehmer-Jones-Zhang (2008 JF); Diether-Lee-Werner (2009 RFS); FINRA Reg SHO daily
files (record Appendix BU); X2 / X2b results (2026-07-13).
