# Pre-registration — X3: Reg SHO daily short-volume drift

**Written 2026-07-14 (CST), BEFORE any runner code. Committed doc-only; this hash
predates the runner. PRD M9 task 47 (= M8 C5; Evan authorized the free sweep
2026-07-14). Written against `docs/prereg_TEMPLATE.md`. MODIFIED-WINDOW CAP →
best verdict = PROMISING.**

## Provenance and prior

Boehmer-Jones-Zhang (2008) / Diether-Lee-Werner (2009): heavily-shorted stocks
underperform (~1.16%/20d in BJZ). **Reg SHO daily short-VOLUME** is the free, deep
(2009+) proxy — but it is *executed* short flow, heavily contaminated by market-maker
/ internalizer hedging (a short print is created whenever a wholesaler fills a retail
buy then covers), so the short-volume ratio SVR = ShortVolume/TotalVolume routinely
sits 25–52% even for lightly-shorted names (confirmed in the ingested data). **H1:**
long the lowest-SVR names outperforms. **H0 (expected):** SVR is microstructure noise,
not informed shorting; the long-only leg is the weak side; and X2/X2b already showed
the *clean* short-interest signal fails once costed. **Prior: near-certain FAIL** —
noisier signal than X2, same family, same liquidity-floor exclusion of where the effect
lives.

## Data (probed + ingested 2026-07-14)

- **FINRA Reg SHO daily short-volume**, 39 survivor large-caps, ingested by
  `scripts/ingest_regsho_short_volume.py`: **4,260 sessions 2009-08-03 → 2026-07-10,
  39/39 coverage every day** (CNMS consolidated 2018-08+; FNYX+FNSQ+FNRA venue-sum for
  2009-08→2018-07). Cached SVR per name per day (`.regsho_cache/`, gitignored). Prices
  `.e8e9_cache` (split-adj, div-UNADJ). No swing.db writes.
- **Lookahead guard:** the daily file publishes EOD; the signal uses SVR **through the
  week-end session** and enters at the **next session's open** (1-session lag).

## Exact rules (fixed a priori)

- **Signal:** at each ISO-week-end session, rank the 39 by **trailing-5-session mean
  SVR** (smooths the daily microstructure noise).
- **Deployable long-only leg:** hold the **K=5 LOWEST-mean-SVR** names, equal-weight,
  enter next open, full weekly rebalance; **5 bps/side**; NAV/K; $1,000 start.
- **Existence spread (non-deployable, reported):** low-K minus high-K, frictionless
  close-to-close, to test the documented sign. Flagged existence-only (shorting
  constraints + the alpha is on the high-SVR short leg, per X2b).
- **Time-stop baseline:** weekly rebalance IS the time stop; no price stop.

## Windows and verdict [MODIFIED-WINDOW CAP + asymmetric]

- **Gate 2009-08 → 2013-12** (Reg SHO floor; partial overlap with the standard hostile
  gate). **Secondary 2014→.** Per the modified-window rule the gate is short + the data
  floor post-dates 2000 → **best achievable = PROMISING; PASS-HR/RA NOT claimable.**
  Floor ≥ 30 rebalances.
- **PROMISING** iff the long-only leg beats **both** SPY-BH AND EW-39 on **CAGR AND
  Sharpe** in both windows AND the existence spread carries the documented (low−high)
  positive sign. **FAIL** otherwise. **Asymmetric:** survivor universe → a FAIL is
  clean; a PROMISING is forward-only.

## Results-doc requirements
Long-only leg vs SPY-BH + EW-39, both windows; decomposition ladder A/B/C; existence
spread sign; 15 bps stress; explicit comparison to X2 (short-INTEREST) and X2b;
tripwire GREEN.

## Disclosed limitations
Executed-flow ≠ short interest (MM-hedging contamination — the core reason for the FAIL
prior); survivorship; short gate + post-2000 floor → PROMISING-capped; long-only tests
the weak leg; venue-sum vs CNMS methodology change at 2018-08 (disclosed, both are
exchange-listed consolidations).
