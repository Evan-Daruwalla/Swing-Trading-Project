"""Frozen large-cap equity universe for M12 (constraint-relaxation factorial).

FROZEN 2026-08-03. Changing membership requires a NEW dated decision recorded in
the project record (same rule as swing_bot/universe.py, per PRD M0.3). This module
is SEPARATE from universe.py's frozen 29-ETF set, which is untouched and still
backs the frozen-regression tripwire.

WHY IT EXISTS: M12 tests whether CONCENTRATION binds (K=3 vs K=20). K=20 is only a
meaningful sort if the universe is large enough -- top-20 of the previous 39-name
set is half the universe. At 142 names, top-20 is a 14% sort.

SELECTION RULE, declared before the probe ran: a US large-cap with a real bar on or
before 1999-01-04, so the 2000-2013 GATE window has a full 252-session 12-1 momentum
formation available from its first day. Candidates were assembled sector-spread so a
top-20 ranking cannot be a single-sector artifact by construction.

`data_start` is each ticker's FIRST ACTUAL BAR (auto_adjust=False), fetched
empirically 2026-08-03 -- NOT an invented inception date.

SURVIVORSHIP -- READ THIS BEFORE INTERPRETING ANY RESULT: these are companies that
still trade TODAY. The universe is biased IN THE STRATEGY'S FAVOUR, so under this
project's asymmetric-falsification rule **only a FAIL is clean**; a PASS is
uninterpretable and routes to forward paper, never to a live claim.

EXCLUDED, and why (honest record): NVDA (first bar 1999-01-22) and STX (2002-12-11)
missed the pre-declared cutoff -- NVDA by 18 days. Dropping NVDA, the era's most
famous momentum survivor, REDUCES survivorship flattery; the rule was applied as
written rather than bent for a name that would have helped. BK, MMC, MRO, HES, K and
GPS are excluded as a DATA-SOURCE limitation, not a judgement: yfinance returns
"possibly delisted / no timezone found" for them on every retry.
"""
from collections import namedtuple

Stock = namedtuple("Stock", ["ticker", "sector", "data_start"])

# ticker, sector, data_start (empirical first bar)
UNIVERSE_M12 = (
    Stock("DIS", "discret", "1990-01-02"),
    Stock("DRI", "discret", "1995-05-09"),
    Stock("F", "discret", "1990-01-02"),
    Stock("HD", "discret", "1990-01-02"),
    Stock("HOG", "discret", "1990-01-02"),
    Stock("LOW", "discret", "1990-01-02"),
    Stock("MCD", "discret", "1990-01-02"),
    Stock("NKE", "discret", "1990-01-02"),
    Stock("ROST", "discret", "1990-01-02"),
    Stock("SBUX", "discret", "1992-06-26"),
    Stock("TGT", "discret", "1990-01-02"),
    Stock("TJX", "discret", "1990-01-02"),
    Stock("YUM", "discret", "1997-09-17"),
    Stock("APA", "energy", "1990-01-02"),
    Stock("COP", "energy", "1990-01-02"),
    Stock("CVX", "energy", "1990-01-02"),
    Stock("DVN", "energy", "1990-01-02"),
    Stock("EOG", "energy", "1990-01-02"),
    Stock("HAL", "energy", "1990-01-02"),
    Stock("OXY", "energy", "1990-01-02"),
    Stock("SLB", "energy", "1990-01-02"),
    Stock("VLO", "energy", "1990-01-02"),
    Stock("WMB", "energy", "1990-01-02"),
    Stock("XOM", "energy", "1990-01-02"),
    Stock("AFL", "financials", "1990-01-02"),
    Stock("ALL", "financials", "1993-06-03"),
    Stock("AON", "financials", "1990-01-02"),
    Stock("AXP", "financials", "1990-01-02"),
    Stock("BAC", "financials", "1990-01-02"),
    Stock("C", "financials", "1990-01-02"),
    Stock("COF", "financials", "1994-11-16"),
    Stock("JPM", "financials", "1990-01-02"),
    Stock("PNC", "financials", "1990-01-02"),
    Stock("SCHW", "financials", "1990-01-02"),
    Stock("STT", "financials", "1990-01-02"),
    Stock("TROW", "financials", "1990-01-02"),
    Stock("TRV", "financials", "1990-01-02"),
    Stock("USB", "financials", "1990-01-02"),
    Stock("WFC", "financials", "1990-01-02"),
    Stock("ABT", "health", "1990-01-02"),
    Stock("AMGN", "health", "1990-01-02"),
    Stock("BAX", "health", "1990-01-02"),
    Stock("BDX", "health", "1990-01-02"),
    Stock("BIIB", "health", "1991-09-17"),
    Stock("BMY", "health", "1990-01-02"),
    Stock("BSX", "health", "1992-05-19"),
    Stock("CAH", "health", "1990-01-02"),
    Stock("CI", "health", "1990-01-02"),
    Stock("CVS", "health", "1990-01-02"),
    Stock("GILD", "health", "1992-01-22"),
    Stock("HUM", "health", "1990-01-02"),
    Stock("JNJ", "health", "1990-01-02"),
    Stock("LLY", "health", "1990-01-02"),
    Stock("MCK", "health", "1994-11-10"),
    Stock("MDT", "health", "1990-01-02"),
    Stock("MRK", "health", "1990-01-02"),
    Stock("PFE", "health", "1990-01-02"),
    Stock("SYK", "health", "1990-01-02"),
    Stock("UNH", "health", "1990-01-02"),
    Stock("BA", "industrial", "1990-01-02"),
    Stock("CAT", "industrial", "1990-01-02"),
    Stock("CSX", "industrial", "1990-01-02"),
    Stock("DE", "industrial", "1990-01-02"),
    Stock("DOV", "industrial", "1990-01-02"),
    Stock("EMR", "industrial", "1990-01-02"),
    Stock("ETN", "industrial", "1990-01-02"),
    Stock("FDX", "industrial", "1990-01-02"),
    Stock("GD", "industrial", "1990-01-02"),
    Stock("GE", "industrial", "1990-01-02"),
    Stock("HON", "industrial", "1990-01-02"),
    Stock("ITW", "industrial", "1990-01-02"),
    Stock("LMT", "industrial", "1990-01-02"),
    Stock("MMM", "industrial", "1990-01-02"),
    Stock("NOC", "industrial", "1990-01-02"),
    Stock("NSC", "industrial", "1990-01-02"),
    Stock("PH", "industrial", "1990-01-02"),
    Stock("ROK", "industrial", "1990-01-02"),
    Stock("RTX", "industrial", "1990-01-02"),
    Stock("SWK", "industrial", "1990-01-02"),
    Stock("UNP", "industrial", "1990-01-02"),
    Stock("APD", "materials", "1990-01-02"),
    Stock("ECL", "materials", "1990-01-02"),
    Stock("FCX", "materials", "1995-07-10"),
    Stock("MLM", "materials", "1994-02-17"),
    Stock("NEM", "materials", "1990-01-02"),
    Stock("NUE", "materials", "1990-01-02"),
    Stock("PPG", "materials", "1990-01-02"),
    Stock("SHW", "materials", "1990-01-02"),
    Stock("VMC", "materials", "1990-01-02"),
    Stock("AMT", "reits", "1998-02-27"),
    Stock("BXP", "reits", "1997-06-18"),
    Stock("O", "reits", "1994-10-18"),
    Stock("PSA", "reits", "1990-01-02"),
    Stock("SPG", "reits", "1993-12-14"),
    Stock("VTR", "reits", "1997-05-05"),
    Stock("CAG", "staples", "1990-01-02"),
    Stock("CL", "staples", "1990-01-02"),
    Stock("CLX", "staples", "1990-01-02"),
    Stock("CPB", "staples", "1990-01-02"),
    Stock("GIS", "staples", "1990-01-02"),
    Stock("HSY", "staples", "1990-01-02"),
    Stock("KMB", "staples", "1990-01-02"),
    Stock("KO", "staples", "1990-01-02"),
    Stock("MO", "staples", "1990-01-02"),
    Stock("PEP", "staples", "1990-01-02"),
    Stock("PG", "staples", "1990-01-02"),
    Stock("STZ", "staples", "1992-03-17"),
    Stock("SYY", "staples", "1990-01-02"),
    Stock("WMT", "staples", "1990-01-02"),
    Stock("AAPL", "tech", "1990-01-02"),
    Stock("ADBE", "tech", "1990-01-02"),
    Stock("ADI", "tech", "1990-01-02"),
    Stock("AMAT", "tech", "1990-01-02"),
    Stock("AMD", "tech", "1990-01-02"),
    Stock("AMZN", "tech", "1997-05-15"),
    Stock("CSCO", "tech", "1990-02-16"),
    Stock("EBAY", "tech", "1998-09-24"),
    Stock("GLW", "tech", "1990-01-02"),
    Stock("HPQ", "tech", "1990-01-02"),
    Stock("IBM", "tech", "1990-01-02"),
    Stock("INTC", "tech", "1990-01-02"),
    Stock("KLAC", "tech", "1990-01-02"),
    Stock("LRCX", "tech", "1990-01-02"),
    Stock("MSFT", "tech", "1990-01-02"),
    Stock("MSI", "tech", "1990-01-02"),
    Stock("MU", "tech", "1990-01-02"),
    Stock("ORCL", "tech", "1990-01-02"),
    Stock("QCOM", "tech", "1991-12-13"),
    Stock("TXN", "tech", "1990-01-02"),
    Stock("WDC", "tech", "1990-01-02"),
    Stock("T", "telecom", "1990-01-02"),
    Stock("VZ", "telecom", "1990-01-02"),
    Stock("AEP", "utilities", "1990-01-02"),
    Stock("D", "utilities", "1990-01-02"),
    Stock("DUK", "utilities", "1990-01-02"),
    Stock("ED", "utilities", "1990-01-02"),
    Stock("EXC", "utilities", "1990-01-02"),
    Stock("NEE", "utilities", "1990-01-02"),
    Stock("PEG", "utilities", "1990-01-02"),
    Stock("SO", "utilities", "1990-01-02"),
    Stock("SRE", "utilities", "1998-06-29"),
    Stock("XEL", "utilities", "1990-01-02"),
)

TICKERS = tuple(s.ticker for s in UNIVERSE_M12)
assert len(TICKERS) == len(set(TICKERS)), "duplicate ticker in frozen universe"
assert len(TICKERS) == 142, "frozen universe size changed -- needs a dated decision"
