# Pre-registration — E13: Turn-of-the-month overlay

**Written 2026-07-12, BEFORE any runner code. Committed doc-only; this hash
predates the runner. First experiment of the M7 catalog arc; first to carry
the D1 dual-bar verdict (record Appendix AW).**

## Provenance and prior

McConnell & Xu (2008, *Financial Analysts Journal*): equity returns
concentrate in the ~4-session turn-of-the-month (TOM) window; ~0.45%/mo alpha,
robust in 31/35 countries, persists out-of-sample. **Honest prior:** this is
an OVERLAY, in-market only ~20% of sessions, so PASS-HR (CAGR ≥ 15%) is
near-impossible by construction; **PASS-RA is the only reachable pass** and is
the real question — does concentrating exposure into the TOM window beat SPY
buy-hold on Sharpe?

## Universe, data

- **SPY only.** Data from `.e8e9_cache` (already fetched; split-adjusted,
  dividend-UNADJUSTED). No swing.db writes. EOD: signal at close, execute
  next open.

## Exact rules (fixed a priori)

- Define **TOM-day(d)** = d is the last trading day of its calendar month, OR
  d is among the first 3 trading days of its calendar month (→ the 4-session
  window −1,+1,+2,+3, standard McConnell-Xu definition).
- Target exposure: **long SPY on TOM-days, cash otherwise.**
- Execution (next-open, from close signal): at close of session t, let
  want = TOM-day(t+1). If want and flat → buy at t+1 open. If not want and
  long → sell at t+1 open. (So the position is entered at the open of the
  first TOM session and exited at the open of the first non-TOM session —
  open-to-open capture of the window.)
- 5 bps/side. Full capital in/out (single asset, no K). $1,000 start.

## Windows and D1 verdict (all three labels fixed here)

- **Gate window 2000-01-01 → 2013-12-31.** **Secondary 2014-01-01 → end.**
- **PASS-HR:** net CAGR ≥ 15% AND maxDD ≤ 60% in the gate window, confirmed
  in secondary.
- **PASS-RA:** net Sharpe ≥ 0.80 in the gate window AND Sharpe > SPY
  buy-hold in BOTH windows AND positive net CAGR in both.
- **FAIL:** neither. Interpretability floor: ≥ 30 round-trips in the gate
  window (TOM makes ~12/yr → ~168; floor is a formality).
- Reported alongside: return-per-day-in-market vs SPY's, and % of sessions
  in-market. No parameter changed after results.

## Disclosed limitations

- Dividend-UNADJUSTED SPY understates buy-hold's long-run return by ~1.8%/yr
  (dividends) — this biases the comparison **toward** the overlay slightly on
  CAGR but not on the Sharpe comparison materially; disclosed.
- Single asset, single country, one calendar definition — no robustness grid
  (a grid would be post-hoc tuning; the a-priori window is the test).
