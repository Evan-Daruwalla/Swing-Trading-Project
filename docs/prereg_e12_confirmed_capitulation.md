# Pre-registration — E12: Confirmed-capitulation mean reversion ("right side of the V")

**Written 2026-07-10, BEFORE any runner code. Committed doc-only; this hash
predates the runner.**

## Provenance and how it differs from E1

The ex-Trillium trader's headline mean-reversion method (his $10M Nikkei
trade): do NOT buy an oversold dip directly — wait for a **capitulation
volume climax** after a sharp extended drop, then buy **"the right side of the
V" when the trend breaks** upward, trailing on prior daily-bar lows. SMB's
"backside" setups share the wait-for-confirmation logic.

This is **distinct from E1 (IBS)**, which buys the dip AT the close while it is
still falling. E12's novelty is the **confirmation gate**: a volume-climax
capitulation PLUS a confirmed upside reversal before any entry — designed to
sidestep the falling-knife problem that (partly) sank the IBS family. New
mechanism → legitimate new experiment, not an IBS retune. Prior: modest.

## Universe, data

- Frozen 29-ETF universe; data reused from `.e8e9_cache/` (gitignored); **no
  swing.db writes**. EOD only: signal at close, execute next open.

## Exact rules (fixed a priori)

- **Arm a capitulation** at day j when BOTH: close_j ≤ 0.85 × max(close[j−10 …
  j]) (≥15% off the trailing 10-day high — a sharp extended drop) AND
  volume_j ≥ 1.5 × mean(volume[j−20 … j−1]) (RVOL ≥ 1.5 climax). The armed
  state persists up to **5 trading days** after j.
- **Entry trigger** at day t while armed: close_t > high_(t−1) (first close
  above the prior day's high = confirmed upside reversal, the "right side of
  the V"). Buy next open; disarm. K=3; if oversubscribed, rank by deepest
  drop (lowest close/max10 first).
- **Exit**: close_t < low_(t−1) (undercuts prior day's low — the prior-bar-low
  trailing stop) OR 40-bar max hold. Sell next open.
- Sizing $1,000, min(cash, NAV/3); 5 bps/side. Open positions at data end
  marked to last close and flagged.

## Windows and gates (any miss = FAIL)

- **Gate 2000–2013:** CAGR ≥ 15% AND maxDD ≤ 60%. Interpretability floor
  n_trades ≥ 30; below → INCONCLUSIVE.
- **Secondary 2014 → end:** overall PASS also needs CAGR ≥ 15% & maxDD ≤ 60%.
- No tuning after results. A FAIL closes the confirmed-capitulation idea.

## Disclosed limitations

- ETFs only (single stocks = survivorship trap). ETFs are less volatile than
  the small-caps the pros use, so capitulation signals are rarer — the
  n_trades floor guards interpretability.
- The "right side of the V" is inherently an intraday judgment for the pros;
  close_t > high_(t−1) is the honest EOD proxy, disclosed as a simplification.
- Dividend-UNADJUSTED closes; staggered ETF inception.
