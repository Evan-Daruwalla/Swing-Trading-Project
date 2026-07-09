# E1 fill-timing ablation — overnight vs next-open (2026-07-09)

**PRD task M1.8 (#15 + #13).** Run AFTER the M1.7 pre-registration commit
(`8963e49`) — returns are now permitted. Question: how much of the IBS<0.20
edge lives in the overnight gap (close → next open) that the executable
next-open loop forfeits?

**Method:** per-signal DIAGNOSTIC, not the strategy. On every IBS<0.20 signal
at close of day T, the 1-day-forward return under four timings (gross of
costs, bps):
- `c2c` = close[T+1]/close[T]−1 — published basis (enter at close T)
- `overnight` = open[T+1]/close[T]−1 — the gap Model A forfeits
- `intraday` = close[T+1]/open[T+1]−1 — buy-open/sell-close, day T+1
- `nopen1d` = open[T+2]/open[T+1]−1 — executable 1-day (enter open T+1)

This is a raw per-signal average with overlapping signals — NOT the K=5,
exit-rule strategy return (that is M2). Source: `swing.db`, 17,558 signals.

## Pooled and per-group (mean, bps)

| scope | n | c2c | overnight | intraday | nopen1d |
|---|---|---|---|---|---|
| broad_us | 2303 | 14.4 | 7.8 | 6.6 | 11.2 |
| spdr_sector | 6614 | 10.3 | 5.5 | 4.7 | 8.0 |
| country_intl | 8641 | 12.2 | 6.5 | 5.7 | 6.1 |
| **POOLED** | **17558** | **11.8** | **6.3** | **5.4** | **7.5** |

- **Overnight is 54% of the close-to-close edge** (6.3 / 11.8). The council's
  concern was real: over half the idealized IBS effect is in the post-signal
  gap.
- **But next-open execution keeps ~64%** of it: +7.5 bps vs +11.8 bps c2c
  (haircut 4.3 bps). The executable edge is positive pooled — it does not
  vanish, it is roughly cut by a third.
- `nopen1d` (7.5) exceeds pure `intraday` (5.4) because IBS reversion
  continues into the following overnight — the executable entry catches a
  second night.

## Per-ticker executable edge (nopen1d, bps) — the split matters

Strong executable edge: **XLK 25.9, QQQ 21.6, XLC 18.9, EWY 19.4, INDA 11.1,
SPY 10.0, EEM 10.1, EWZ 10.2**. Weak/negative executable edge (mostly
country, edge is overnight-only): **EWA −0.9, EWC −0.5, EWH ~0.0, EWU 0.1,
EWG 1.0, EFA 1.7, XLRE 1.8, XLP 2.0, XLU 2.8, XLE 3.0**.

This validates the M0.3 decision to report `country_intl` separately: many
single-country ETFs' IBS edge is a stale-NAV/overnight artifact that a
next-open loop cannot harvest. broad_us retains the most (14.4 → 11.2).

## Decision + implication for M2

- **Primary fill model = next-open (Model A)** — as already pre-registered
  (`8963e49` §5). The ablation quantifies the haircut: ~36% of the c2c edge
  lost pooled, more in country ETFs.
- **HONEST RISK FLAG for M2:** +7.5 bps gross per signal (1-day) is THIN
  against the pre-registered **10 bps round-trip cost** — a 1-day-hold view
  would be net-negative. E1's survival hinges on whether the multi-day hold
  (exit at IBS>0.80 or 5 days) captures materially MORE reversion than one
  day. The 1-day ablation is a LOWER BOUND on per-trade gross, not the
  strategy return. M2 resolves it.
- **No rule changes.** The universe and parameters are frozen (`8963e49`).
  The per-group data hints the edge concentrates in broad/tech names, but
  narrowing the universe would be a NEW pre-registration, not an edit to
  this experiment. E1 runs as specified; if it FAILS, that is the result.
