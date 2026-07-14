# Pre-registration TEMPLATE — <E##: strategy name>

> **This is the standing template every new experiment copies (M9 #43, adopted
> 2026-07-13, record Appendix BT).** Copy this file to
> `docs/prereg_e##_<slug>.md`, fill every `<...>`, DELETE this quote block and
> the ▸ notes, then **commit doc-only BEFORE writing any runner code** — that
> commit hash is the prereg and must predate the runner. Sections marked
> **[STANDING]** are fixed policy: do not weaken them per-experiment; only fill
> their `<...>` blanks. If a standing rule genuinely cannot apply, say so
> explicitly in Disclosed Limitations with a dated reason — never silently drop it.

**Written <YYYY-MM-DD> (CST), BEFORE any backtest runner code. Committed
doc-only; this hash predates the runner.** <PRD task ref; who authorized>.
D1 dual-bar verdict<, + asymmetric framing if survivor/biased universe>.

## Provenance and prior

<Primary source(s) with the specific documented effect size — e.g. "Author
(Journal Year): <signal> earns ~X bps/mo abnormal.">. State the working
hypothesis and its rival/null. **State the honest prior** given the program's
base rate (currently 0 PASS-HR / 1 weak PASS-RA / 21 attempts / 8 families):
what verdict do you expect and why. Never retrofit this after results.

▸ If the universe is survivor-biased or the signal uses any lookahead the live
  strategy won't have, add the **[STANDING] asymmetric-falsification clause**:
  "Survivorship/bias can only HELP → **only a FAIL is clean**; a PASS is
  UNINTERPRETABLE and routes to forward paper, never a live claim."

## Data (probed <YYYY-MM-DD>)

- **Source & access:** <feed, endpoint/loader, how fetched>. **Probe-first
  discipline [STANDING]:** for any NEW data source, confirm fetch + parse +
  coverage on the universe BEFORE this prereg; if messy or thin, record
  BLOCKED-ON-DATA and stop (the E17/E19 pattern). Cache is gitignored; the
  runner does **no swing.db writes** and honors read-only on Trading's caches.
- **Adjustment convention [STANDING]:** state it — `.e8e9_cache` /
  `price_cache` are split-adjusted, dividend-UNADJUSTED (`auto_adjust=False`).
  Every price consumer honors this; note it in the runner header.
- **Point-in-time / lookahead:** <how entry timing avoids lookahead; e.g.
  filing-date not transaction-date; as-of dates frozen; no restated
  fundamentals>. yfinance fundamentals are restated → never build a
  fundamentals time-series signal on them and call the backtest honest.
- **Universe & liquidity floor [STANDING]:** <universe>. Floor is **mandatory**:
  **ADV ≥ $5M AND price ≥ $5** at the decision date (at $100–1,000, spread/
  slippage dominate). Participation cap is declared **non-binding at this AUM**
  but stated for the record.

## Exact rules (fixed a priori)

- **Signal:** <precise, codifiable entry condition — no fuzzy pattern logic>.
- **Entry/exit:** signal at close, **execute next open** [STANDING EOD rule —
  no intraday logic until an intraday data source exists]. Hold <N sessions>,
  exit at open. **K = <1–5>** concurrent; oversubscription tie-break = <rule>.
- **Sizing [STANDING defaults]:** capped **fractional-Kelly, λ ≤ ½** (never
  full Kelly), OR fixed-risk **r = 1–2% of NAV per trade**; **anti-martingale
  only** (never average down a loser); **no leverage** unless the experiment
  IS a leverage test with a pre-committed regime stop. Freeze λ / r / size rule
  here; changing it after results is tuning. Default here: <size = min(cash,
  NAV/K); λ=__ / r=__>.
- **Time-stop baseline [STANDING]:** the primary exit is a **time stop** (hold
  N sessions). Any price-stop / trailing-stop variant is an ADDITIONAL arm that
  must BEAT the time-stop-only arm to be adopted — report both. (Stops interact
  with the overnight gap; a naive stop is not free.)
- **Costs [STANDING tiered model]:** charge per side by instrument —
  **1 bp/side** broad-index ETFs (SPY/QQQ/DIA/IWM), **5 bps/side** single
  stocks & sector ETFs, **15–25 bps/side or EXCLUDE** anything below the
  liquidity floor; **crypto = 25 bps/side** (Alpaca taker). Also report a
  **15 bps/side stress leg** alongside the headline so cost-fragility is visible.
  State the tier used: <tier + bps>.

## Windows and verdict [STANDING D1 dual-bar]

- **Gate <2000-01-01 → 2013-12-31>** (hostile regime; use the widest the data
  supports). **Secondary <2014 → end>.** Floor: ≥ <20–30> entries in the gate.
- **PASS-HR:** net CAGR ≥ **15%** AND maxDD ≤ **60%**, BOTH windows.
- **PASS-RA:** gate **Sharpe ≥ 0.80** AND > benchmark buy-hold in BOTH windows
  AND positive CAGR in BOTH. Benchmark(s): <SPY-BH and/or EW-universe>.
- **FAIL:** neither. **All three outcomes are fixed here, before the run.**
  No parameter changes after results; a FAIL is never re-tuned into a pass.
- **Modified-window cap [STANDING]:** if the data forces a window that can't
  cover 2000–2013 (e.g. FINRA SI 2021+, Reg SHO 2009+, crypto ~2015+), fix that
  reduced window a priori, disclose the lost confidence, and **cap the best
  achievable verdict at "PROMISING — needs forward confirmation."** A
  short-window result may NOT claim PASS-HR or PASS-RA.
- **LLM overlays are forward-only [STANDING]:** any LLM-scored signal is a
  treatment arm on the M3 live-paper control, NEVER a historical backtest
  (training-cutoff look-ahead makes LLM backtests dishonest).

## Results-doc requirements [STANDING] (the runner's results doc MUST include)

- **Decomposition ladder** for the headline result: **Rung A** frictionless
  close-to-close 0 bps / **Rung B** next-open 0 bps / **Rung C** next-open +
  tiered cost. Report all three so the reader sees whether any edge is
  signal-real, gap-dwelling, or cost-gated (the EX-DECOMP method, record
  Appendix BS).
- The D1 verdict with the fixed criteria echoed; the benchmark comparison; the
  entry count vs floor; and the **frozen tripwire GREEN** (`.venv\Scripts\
  python.exe -m swing_bot.test_frozen`, 12 refs d=±0.0000pp) run AFTER the
  experiment — the standing definition-of-done, additive to the record entry.

## Disclosed limitations

- <Survivorship / lookahead / short-window / coverage gaps / data-quality
  hazards — everything a skeptic would raise, stated up front. This section is
  load-bearing: the honesty of the whole program lives here.>
