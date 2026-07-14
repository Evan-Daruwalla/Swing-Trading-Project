# C4 — Moreira-Muir vol-targeting sizing overlay: RESULTS

**Swing Trading project · 2026-07-14 (CST) · Evan Daruwalla**

**Prereg:** `prereg_c4_vol_sizing.md` (doc-only, predates runner). **Runner:**
`scripts/run_c4_vol_sizing.py`. **Verdict: FAIL** (pre-registered bar; descriptive).
Frozen tripwire GREEN.

## TL;DR

Scaling the two surviving overlays by w = min(1, 15%/σ₂₀d) **improves both
directionally but clears no bar.** E6 base: gate Sharpe 0.24→0.37, gate maxDD
53.7%→25.1%. E18 base: gate Sharpe 0.69→0.77 (< the 0.80 bar), gate DD 29.7%→21.9%,
secondary Sharpe 0.82→0.94 with DD 43.6%→27.0%. Every managed arm beats its unmanaged
base on Sharpe in both windows — but the pre-registered PASS-RA bar requires gate
Sharpe ≥ 0.80 and the best managed arm reaches 0.77. **FAIL, not tuned.** Honest read:
Moreira-Muir vol-sizing is a real drawdown-cutter on these sleeves (contra the strong
Cederburg prior), but it cannot turn a sub-0.8-Sharpe overlay into a passing one, and
it costs return (E6 secondary CAGR 14.81%→12.32%). Descriptive (few independent stress
episodes); overlay class — irrelevant to the high-return goal either way.

## Results (QQQ, 1 bp/side, band 0.05)

| base / arm | gate CAGR/DD/Sh | secondary CAGR/DD/Sh | trades |
|---|---|---|---:|
| E6 unmanaged | 2.67% / 53.7% / 0.24 | 14.81% / 24.1% / 0.93 | 173 |
| **E6 vol-managed** | 3.63% / **25.1%** / 0.37 | 12.32% / 23.0% / 0.94 | 704 |
| E18 unmanaged | 10.55% / 29.7% / 0.69 | 13.80% / 43.6% / 0.82 | 305 |
| **E18 vol-managed** | 9.58% / **21.9%** / **0.77** | 12.46% / **27.0%** / **0.94** | 945 |
| QQQ buy-hold | −0.53% / 83.0% / 0.14 | 18.45% / 35.6% / 0.90 | — |

Stress (E6-managed gate): 5 bp 3.33%/0.34; 15 bp 2.59%/0.28 (4–5× the trades of the
unmanaged arm makes it cost-sensitive).

**Verdict:** E6-managed gate Sharpe 0.37 < 0.80 → fail; E18-managed 0.77 < 0.80 →
fail. **FAIL** (both bases; bar not relaxed post-hoc).

## Interpretation

The overlay does exactly what Moreira-Muir claims — sheds vol where vol clusters — and
the drawdown improvements are large and consistent. But (1) the absolute Sharpe bar is
missed, (2) return is sacrificed (managed arms trail unmanaged CAGR in the bull), and
(3) turnover triples-to-quintuples, making the improvement cost-fragile. As a
*descriptive* matter this is the best-behaved overlay variant the program has tested
(E18-managed: Sharpe ≥ 0.77/0.94 both windows, DD ≤ 27% everywhere) and would be the
natural *deployment shape* if the E6/E18 forward-paper candidate ever goes live — but
it earns no tier and changes no conclusion. With X1 + C4, the vol-overlay family is
closed: conditioning fails outright, continuous sizing improves but not enough.

## Reproduction
`.venv\Scripts\python.exe scripts/run_c4_vol_sizing.py`; tripwire GREEN.

## Sources
Moreira-Muir (2017 JF); Cederburg-O'Doherty-Wang-Yan (2020 JFE); X1 results
(2026-07-13); E18 results (2026-07-11).
