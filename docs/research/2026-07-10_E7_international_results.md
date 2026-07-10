# E7 results — international validation: BOTH ARMS FAIL (2026-07-10)

Per pre-registration `70ed2a1`. **No tuning.** The clean-data unlock: tested
on genuinely-unseen non-US regimes (Nikkei back to 1985, DAX/FTSE/HSI/ASX).
Local-currency price indices (currency-neutral mechanics; dividends excluded
→ returns understated ~2–3%/yr). The a-priori vol gate (30%) and drag (5%/yr)
were fixed from first principles before any non-US data was seen.

## Arm 1 — does E6's 1× drawdown overlay generalize? FAIL (3/5, need ≥4)

| market | rot CAGR | rot maxDD | rot Sharpe | BH maxDD | BH Sharpe | pass |
|---|---|---|---|---|---|---|
| ^N225 (Japan) | 4.78% | 33.8% | 0.41 | 81.9% | 0.31 | YES |
| ^GDAXI (Germany) | 8.15% | 34.2% | 0.63 | 72.7% | 0.49 | YES |
| ^FTSE (UK) | 1.58% | 51.4% | 0.20 | 52.6% | 0.39 | **no** |
| ^HSI (Hong Kong) | 5.75% | 45.7% | 0.43 | 65.2% | 0.36 | YES |
| ^AXJO (Australia) | 2.45% | 25.1% | 0.30 | 53.9% | 0.43 | **no** |
| ^GSPC (US, cross-check) | 7.20% | 29.6% | 0.66 | 56.8% | 0.60 | YES |

**E6's overlay is REAL but MARKET-DEPENDENT.** It works dramatically in Japan,
Germany, Hong Kong, and the US (big drawdown cuts + higher Sharpe) — including,
notably, **halving the Nikkei's 82% buy-hold drawdown to 34%** through the
worst secular bear on record. But it FAILS in the UK (barely cut drawdown,
52.6→51.4%, and Sharpe fell 0.39→0.20) and Australia (cut drawdown a lot but
Sharpe still fell 0.43→0.30 — whipsaw cost exceeded the drawdown benefit on a
risk-adjusted basis). **Downgrade:** E6 is not a universal law — in choppy
trending markets the timing overlay hurts risk-adjusted return. It is a
useful-in-some-regimes tool, not a robust global one.

## Arm 2 — a-priori vol-gated 3× rotation (the high-return shot): FAIL (all 4)

| market | vg-3× CAGR | %/mo | vg-3× maxDD | plain-3× maxDD | buy-hold-3× CAGR |
|---|---|---|---|---|---|
| ^N225 | 6.93% | 0.56% | 83.3% | 85.1% | −7.38% |
| ^GDAXI | 15.78% | 1.23% | 59.8% | 74.9% | 5.84% |
| ^FTSE | −1.34% | −0.11% | 97.3% | 97.1% | 1.64% |
| ^HSI | *degenerate* | — | — | — | −100% (wiped out) |
| ^AXJO | 1.41% | 0.12% | 68.6% | 68.3% | 4.05% |
| ^GSPC | 14.71% | 1.15% | 71.1% | 70.0% | 13.06% |

| gate | result |
|---|---|
| 1 positive CAGR all 5 | **FAIL** (FTSE −1.34%; HSI degenerate) |
| 2 maxDD ≤ 70% all 5 | **FAIL** (FTSE 97.3%, Nikkei 83.3%) |
| 3 Nikkei CAGR>0 AND DD≤70% | **FAIL** (+6.93% but 83.3% DD) |
| 4 mean CAGR ≥ 15% | **FAIL** (4.55%; ~5.7% excluding degenerate HSI) |

### ARM 2 VERDICT: FAIL — the high-return-AND-robust question is now CLOSED.

Three findings, all damning for leveraged rotation:
1. **The vol gate barely helped.** vg-3× maxDD ≈ plain-3× maxDD in the crash
   markets (Nikkei 83.3 vs 85.1; FTSE 97.3 vs 97.1). The a-priori 30%
   threshold does not catch the drawdowns; leverage + whipsaw survives it.
2. **3× is tail-fatal, not just risky.** The ^HSI synthetic 3× is degenerate
   because the **1987 Hang Seng crash (>33% in one day) drives any 3×
   daily-rebalanced fund to zero permanently.** Buy-hold-3× = −100%. No timing
   overlay can recover from a single-day wipeout. This is a mathematical, not
   statistical, argument against extreme leverage.
3. **Return isn't even there.** Mean CAGR 4.55% across 5 markets — nowhere
   near the 15% high-return bar. The 2014–2026 US result (E4) was a
   coincidence of one favorable regime, not a repeatable edge.

## Bottom line

**This is the clean close the pressure-test (Appendix AE) set up.** The one
credible untested high-return idea — a-priori-vol-gated leverage rotation —
was tested on five genuinely independent, unseen regimes (fixed knobs, no
fitting) and FAILED every gate. The conclusion is no longer "I ran out of US
data"; it is "I found clean data and the idea failed on it." **No
high-return-AND-robust EOD strategy has been found, and this is now backed by
out-of-sample international evidence, not just US in-sample falsification.**
Even the one risk-management survivor (E6, 1×) is market-dependent. The search
is closed with confidence; what remains is deployment of a modest survivor
and the write-up.
