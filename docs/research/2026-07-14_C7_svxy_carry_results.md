# C7 — SVXY short-vol carry, VIX-TS gated: RESULTS (+ C2 probe close)

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_c7_svxy_carry.md` (doc-only, predates runner). **Runner:**
`scripts/run_c7_svxy_carry.py`. **Verdict: FAIL** (pre-registered PROMISING-capped
bar). Frozen tripwire GREEN. Also records the **C2 probe close** (bottom).

## TL;DR

The gated short-vol carry posts the **highest full-window net CAGR the program has
ever produced — 26.45%** (2012–2026, 55.4% DD, Sharpe 0.76) — and still **FAILS** the
pre-registered bar, on two mutually-reinforcing grounds. (1) **Risk-adjusted it loses
to SPY** (Sharpe 0.76 < 0.82; ~40% vol): the bar required beating SPY on CAGR *and*
Sharpe. (2) The headline is an **artifact of a dead instrument**: SVXY was −1× until
2018-02-27 and −0.5× after; era-split, the −1× years did **47.33%/Sharpe 0.99** while
the deployable-today −0.5× era does **13.18%/0.55** — SPY-like return, half SPY's
Sharpe. The spectacular footnote: the VIX-TS gate **dodged Volmageddon by one
session** (contango flipped false at the 2018-02-02 close → exit at the 02-05 open,
missing the −32% and −83% days) — but that is effective-N = 1 tail-dodging on the
exact event the gate was designed around, and the prereg's own H0 (an EOD bot cannot
reliably gate an overnight cascade) stands. Short-vol carry closed.

## Results (2012-01-03 → 2026-07-13; 178 toggles; 1 kill-switch event)

| arm | CAGR | maxDD | Sharpe |
|---|---:|---:|---:|
| **gated + kill-switch (MAIN)** | **26.45%** | 55.4% | 0.76 |
| gated, no kill-switch | 28.95% | 55.4% | 0.81 |
| MAIN @15 bps | 24.91% | 56.4% | 0.74 |
| SVXY buy-hold | 10.42% | **95.2%** | 0.54 |
| SPY buy-hold | 13.04% | 34.1% | **0.82** |

**Era split (descriptive, post-hoc disclosure):** −1× era (2012→2018-02) 47.33% /
Sharpe 0.99; **−0.5× era (2018-03→) 13.18% / 0.55.**

**Volmageddon trace:** 02-01 +3.0% (contango) → 02-02 −13.2% (contango FALSE at close
→ exit signal) → **exit at 02-05 open** → 02-05 close −32.0%, 02-06 −83.0% avoided.
Kill-switch fired once in 14.5 years (Brexit, 2016-06-24, −26.4%).

**Verdict:** beats SPY on CAGR, loses on Sharpe (0.76 < 0.82) → **FAIL** (floor ok,
178 toggles ≥ 20). The no-kill-switch arm's 0.81 also loses to 0.82 — the verdict is
not kill-switch-sensitive.

## Interpretation

- **The carry is real; the vehicle and the tail price it away.** Gating by contango
  triples SVXY buy-hold's CAGR and halves its DD — the VIX-TS signal genuinely
  separates harvest-time from cascade-time *on average*. But the residual path is
  ~40%-vol with 55% drawdowns, and on today's −0.5× instrument the net carry is
  SPY-like return at half the risk-efficiency.
- **The Volmageddon dodge is not evidence of safety.** One event, one session of
  margin, and the −13.2% day was eaten before the exit. XIV holders in the identical
  trade were terminated. An EOD overlay's protection against an overnight cascade is
  structurally a coin-flip on timing — which is exactly why the prereg capped this at
  PROMISING and why the FAIL closes it.
- **Program-level:** the volatility-risk-premium family (E18 gate → X1 conditioning →
  C4 sizing → C7 harvest) is now fully surveyed: the VIX-TS signal is a real *regime
  classifier* (its one weak PASS-RA stands) but neither an alpha engine nor a safe
  carry harvester at EOD.

## C2 — dividend-initiation drift: probe close (BLOCKED-BY-DESIGN, no prereg)

Per the PRD's probe-first rule: yfinance full dividend histories for the 39 survivors
show **only 3 first-ever in-window initiations in 26 years** — MSFT 2003-02-19,
ORCL 2009-04-06, CSCO 2011-03-29 (all other names initiated 1962–1999; AAPL-2012 is a
*resumption*). n=3 cannot clear any pre-registerable event floor (≥20–30), so no
prereg or runner was written — **closed for insufficient event flow** (the honest E17
pattern). The famous initiation-drift literature lives in broad small/mid-cap
universes the liquidity floor excludes.

## Reproduction
`.venv\Scripts\python.exe scripts/run_c7_svxy_carry.py`; probe in record Appendix CC;
tripwire GREEN.

## Sources
Augustin-Cheng-Van den Bergen (2021) on XIV termination; BIS/variance-premium
literature per the 2026-07-12 survey; Michaely-Thaler-Womack (1995) for C2;
E18/X1/C4 results.
