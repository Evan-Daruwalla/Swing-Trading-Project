# E3 results — concentrated stock momentum: VERDICT = FAIL (clean) (2026-07-10)

Per pre-registration `87bc8d9`. **No tuning.** Read via asymmetric
falsification (prereg §0): a FAIL is CLEAN; a PASS would have been
uninterpretable. **It failed — cleanly, and badly.**

## Setup

39 survivor large-caps (fetched 39/39), hold top K=3 by trailing 63-day
return, rebalance every 10 trading days, next-open fills, 5 bps/side. The
universe carries survivorship + lookahead bias that can only INFLATE results
(§0) — so the failure below is a lower-bound-flattering result that still lost.

## Results

| window | E3 CAGR | %/mo | maxDD | Sharpe | EW-universe buy-hold | SPY buy-hold |
|---|---|---|---|---|---|---|
| **2000–2013 (gate)** | **6.27%** | +0.51% | 61.8% | 0.36 | 7.10% | 1.72% |
| 2014–2026 | 4.79% | +0.39% | 54.0% | 0.31 | **14.94%** | 11.91% |
| 2000–2026 | 5.51% | +0.45% | 61.8% | 0.33 | 10.69% | 6.37% |

## Kill criteria (2000–2013 gate)

| # | criterion | got | result |
|---|---|---|---|
| 1 | CAGR ≥ 15% | 6.27% | **FAIL** |
| 2 | maxDD ≤ 65% | 61.8% | PASS |

### E3 VERDICT: FAIL — clean. The stock-momentum avenue is closed.

## Why this is a strong, clean close (not a marginal miss)

1. **It failed the return bar by a wide margin** — 6.27% vs the 15%
   requirement, *with* survivorship + lookahead + a favorable universe all
   working in its favor. There is no "but it was close" hedge.
2. **Momentum was WORSE than doing nothing.** Concentrated momentum
   underperformed a simple equal-weight buy-and-hold of its OWN (biased,
   survivor) universe in every window — catastrophically in 2014–2026 (4.79%
   vs 14.94%). The momentum *selection itself destroyed value*: picking the
   top-3 recent winners every two weeks did worse than just holding all 39.
3. **The falsification logic holds tight.** A biased universe can only help;
   it helped, and momentum still lost. So the failure is interpretable in a
   way a pass never could have been. (A single pre-registered spec was tested;
   per program discipline, hunting for a momentum parameterization that passes
   would be hindsight fishing — not done.)

## Interpretation & honest caveats

- The stock avenue is **closed for a backtested high-return claim**: a
  concentrated short-horizon momentum strategy fails even bias-flattered.
- What is NOT claimed: that NO stock strategy could ever work. Only forward
  live paper (survivorship-free) could test that, and it is Evan/Alpaca-gated
  and slow. But the prior after this result is poor.
- The 2000–2013 numbers still under-count company deaths (survivorship);
  reality was worse than 6.27%.

## Disposition

E3 joins mean reversion (E1/E1b/E2) and leverage rotation (E4/E5/E7) as an
honestly falsified family. **All three plausible routes to a high-return,
robust, executable retail edge — index mean reversion, leveraged trend, and
concentrated stock momentum — have now failed pre-registered tests.** Nothing
went live. The search is comprehensively closed; what remains is deployment of
a modest risk-management survivor (E6, Evan-gated) or accepting the
falsification program as the deliverable.
