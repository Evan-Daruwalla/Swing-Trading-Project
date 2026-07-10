# Pre-registration — E10: Post-earnings-announcement drift (catalyst continuation)

**Written 2026-07-10, BEFORE any runner code. Committed doc-only; this hash
predates the runner, per program discipline.**

## Provenance and framing

The one "real edge" named independently by THREE sources in the swing-trading
article set (`C:\Users\evan.EVANFREDY\Downloads\Swing Trading Research.md`):
TD's "5% post-earnings drift then fade," SMB's "Power Play day-2
continuation," and the ex-Trillium trader's "continuation with a catalyst."
All describe **post-earnings-announcement drift (PEAD)** — a documented
academic anomaly. It is a SINGLE-STOCK phenomenon (ETFs have no earnings), so
E10 inherits E3's survivorship + lookahead problem and therefore E3's
**asymmetric-falsification** framing: the universe's biases can only INFLATE
the result, so **only a FAIL is interpretable**; a PASS is uninterpretable
and routes to forward live paper (survivorship-free), on a poor prior.

## Universe and data

- **Same 39 survivor large-caps as E3** (explicitly biased; see E3 prereg
  `87bc8d9`): MSFT INTC CSCO ORCL IBM AAPL QCOM TXN ADBE JPM BAC WFC C GS AXP
  XOM CVX COP SLB PG KO PEP WMT MCD HD NKE DIS JNJ PFE MRK ABT UNH GE CAT BA
  MMM HON T VZ.
- Earnings DATES from yfinance `get_earnings_dates(limit=100)` — reaches
  ~2001–2002 for these names (probed 2026-07-10; 100-row cap → the 2000–2001
  slice is missing, disclosed). Announcement dates are historical fact (low
  contamination). The estimate/surprise columns are **NOT used** — the signal
  is price-based only, so restatement of estimates cannot contaminate it.
- OHLCV: yfinance `auto_adjust=False` (split-adjusted, dividend-UNADJUSTED),
  live fetch; **no writes to swing.db**. EOD only.

## Exact rules (fixed a priori)

- For each earnings announcement at timestamp E: let **r** = the first full
  trading session STRICTLY AFTER E (never the announcement bar itself → no
  lookahead). **Reaction** = close_r / close_(session before r) − 1.
- **Entry signal** if reaction ≥ **+3%** (a positive surprise revealed by
  price — the drift trigger; 3% fixed a priori from the 2–5% gaps the sources
  cite). Buy at the open of the session AFTER r. Max K=3 concurrent; if more
  signals than free slots, rank by reaction descending.
- **Exit**: hold exactly **40 trading days** (the classic PEAD drift horizon),
  then sell next open. **No stop** — a stop would confound the drift
  measurement this experiment exists to make.
- Sizing $1,000, size = min(cash, NAV/3); 5 bps/side. Open positions at data
  end marked to last close and flagged.

## Windows and gates (kill-criteria — any miss = FAIL)

- **Gate 2000-01-01 → 2013-12-31** (data effectively ~2001.5 on): CAGR ≥ 15%
  AND NAV maxDD ≤ 65% (single-stock DD ceiling, matching E3). Interpretability
  floor n_trades ≥ 20; fewer → INCONCLUSIVE.
- **Secondary 2014 → data end**, reported always. Benchmarks: equal-weight
  buy-hold of the 39 names, and SPY.
- No parameter changed after results. A FAIL (bias-flattered) closes PEAD for
  this program; a PASS routes to forward paper only.

## Disclosed limitations

- Survivorship + lookahead bias (E3 lesson) — the whole reason for the
  falsification-only reading.
- 100-row earnings cap → history starts ~2001–2002, not 2000.
- Dividend-UNADJUSTED closes understate multi-week holds slightly (biases
  against, not for).
