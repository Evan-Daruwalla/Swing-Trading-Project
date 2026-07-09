# Pre-registration — E2: IBS mean reversion on 3x leveraged ETFs (high-return arm)

**Committed 2026-07-09 (PRD task M2b.2), BEFORE the E2 runner exists and
before any signal-conditioned leveraged-IBS return has been computed. Every
parameter is FIXED; changes require a new dated pre-registration.**

Basis: Evan's 2026-07-09 goal redefinition (record Appendix R — high percent
return, concentrated, losses accepted) + E1b evidence that the IBS edge
persists out-of-sample in broad US indices (holdout Sharpe 0.496, exp
+17.8bps at 5bps/side) — TQQQ/UPRO/SPXL/SOXL/TNA are ~3x wrappers of those
same underlyings. Only the four single-day anomaly checks (record Appendix S)
have been observed on this universe; no strategy returns.

## 1. Hypothesis

The validated broad-US IBS mean-reversion edge, expressed through 3x
leveraged wrappers with concentrated sizing, produces a HIGH net percent
return out-of-sample (2022–2026) — clearing return-centric gates that
1x E1b could not aspire to.

## 2. Universe (fixed)

`swing_bot/universe.LEVERAGED`, frozen 2026-07-09: TQQQ, UPRO, SPXL, SOXL,
TNA. Eligibility: listed (`data_start <= date`) + non-zero-range bar.

## 3. Rules (fixed — E1 mechanics, concentrated sizing)

- Entry: IBS < 0.20 at close of day T (skip high==low). Long-only.
- Exit: first close with IBS > 0.80, OR 5-trading-day time stop.
- **Concentration (Evan's K=1–3): PRIMARY K=2** — capital/2 (50%) per
  position, max 2 concurrent, lowest-IBS-first, ties alphabetical, one
  position per ticker. K=1 and K=3 reported as context (NOT gates).
- No hard stop-loss (same rationale as E1; single-day −35–55% prints are
  possible and accepted — record Appendix S).
- Capital parameter $500 nominal; fractional shares in backtest.

## 4. Fill and cost models (fixed)

- PRIMARY: next-open, 5 bps/side (10 bps round-trip) — conservative for
  these funds (TQQQ/SOXL quoted spreads ~1–2 bps).
- Context (not gates): c2c fill; 0 bps and 10 bps/side sensitivities.

## 5. Evaluation protocol (fixed; same as E1b)

- Train / context: 2014-01-02 .. 2021-12-31.
- **HOLDOUT / gate: 2022-01-01 .. 2026-07-08** — includes the 2022 bear in
  which 3x funds drew down ~80% buy-and-hold: an honest stress window.

## 6. Kill criteria — E2 PASSES only if the HOLDOUT (K=2, next-open,
## 5bps/side) clears ALL (fixed; return-centric per Appendix R)

1. **N:** ≥ 100 closed trades.
2. **Expectancy:** net mean return per trade > 0.
3. **Return (the goal's bar):** net CAGR ≥ 15%/yr on the holdout.
4. **Ruin guard:** max drawdown ≤ 60% (loosened per accepted risk; a
   deeper hole than this ends the compounding experiment).

Sharpe is REPORTED as context, not gated — per the 2026-07-09 goal.

## 7. PRE-COMMITTED STOP (multiplicity guard, per record Appendix Q)

If E2 FAILS, the IBS family — 1x and leveraged — is **SHELVED**. No E2b, no
E1c, no cost-shaved re-runs. Next work would be a different signal family
(E3 design, own pre-registration). This is the third pre-registered test of
the family; it is also the last.

## 8. Live gate (unchanged)

A PASS authorizes nothing live by itself: M3 still requires Evan's explicit
go + an allocated Alpaca paper account.

## 9. No-change clause

Ambiguities resolve to the most literal reading, recorded — never toward
better results. Any substantive change is a new dated pre-registration.
