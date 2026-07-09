"""Frozen tradeable ETF universe for swing_bot.

FROZEN 2026-07-08. Changing membership requires a NEW dated decision recorded
in the project record (per PRD_ROADMAP M0.3). Do not add/remove tickers ad hoc.

Composition: broad US index ETFs + the 11 SPDR sector funds + a liquid
single-country / regional set. Rationale: the IBS mean-reversion edge (E1) is
best-evidenced on liquid equity-index ETFs (Pagonidis 2013) and liquid
country ETFs (arXiv 2306.12434); a broader-but-still-liquid basket also raises
the number of independent daily signals, which is the binding statistical-power
constraint for this small-capital program (see research brief 2026-07-08).

`data_start` is each ticker's FIRST available yfinance bar (auto_adjust=False),
fetched empirically 2026-07-08 — NOT an invented inception date. For these
long-lived funds it is the start of usable price history.

Liquidity: at $100-1,000 capital, depth is a non-issue (the least-liquid
member, EWG, had ~$47M/day median dollar volume at the 2026-07-08 probe —
orders of magnitude above any order size here); the real friction is the
bid-ask spread. MIN_MEDIAN_DOLLAR_VOL is a forward guard against future
degradation, enforced by the coverage/quality gate (M0.4), not here.
"""
from collections import namedtuple

ETF = namedtuple("ETF", ["ticker", "name", "group", "data_start", "reason"])

# 20-day median dollar-volume floor for live eligibility (guard only; every
# current member clears it by a wide margin). Enforcement lives in M0.4.
MIN_MEDIAN_DOLLAR_VOL = 20_000_000

UNIVERSE = [
    # --- broad US ---
    ETF("SPY", "S&P 500", "broad_us", "1993-01-29",
        "Most liquid US equity ETF; core IBS index instrument (Pagonidis)"),
    ETF("QQQ", "Nasdaq-100", "broad_us", "1999-03-10",
        "Large-cap growth/tech index; high-liquidity IBS instrument"),
    ETF("DIA", "Dow Jones Industrial Average", "broad_us", "1998-01-20",
        "Blue-chip 30 index; adds a distinct large-cap tape"),
    ETF("IWM", "Russell 2000 small-cap", "broad_us", "2000-05-26",
        "Small-cap index; higher-vol tape for MR signal diversity"),

    # --- SPDR sector funds (S&P 500 GICS sectors) ---
    ETF("XLE", "Energy sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLF", "Financials sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLK", "Technology sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLV", "Health Care sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLI", "Industrials sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLY", "Consumer Discretionary sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLP", "Consumer Staples sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLU", "Utilities sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLB", "Materials sector", "spdr_sector", "1998-12-22",
        "SPDR sector fund; sector-level MR signal"),
    ETF("XLRE", "Real Estate sector", "spdr_sector", "2015-10-08",
        "SPDR sector fund (launched 2015); shorter history"),
    ETF("XLC", "Communication Services sector", "spdr_sector", "2018-06-19",
        "SPDR sector fund (launched 2018); shorter history"),

    # --- country / regional (iShares MSCI unless noted) ---
    ETF("EWJ", "MSCI Japan", "country_intl", "1996-03-18",
        "Liquid single-country ETF; IBS validated on country ETFs (arXiv)"),
    ETF("EWZ", "MSCI Brazil", "country_intl", "2000-07-14",
        "Liquid single-country ETF; higher-vol EM tape"),
    ETF("EWG", "MSCI Germany", "country_intl", "1996-03-18",
        "Liquid single-country ETF; developed Europe"),
    ETF("EWU", "MSCI United Kingdom", "country_intl", "1996-03-18",
        "Liquid single-country ETF; developed Europe"),
    ETF("EWA", "MSCI Australia", "country_intl", "1996-03-18",
        "Liquid single-country ETF; developed APAC"),
    ETF("EWC", "MSCI Canada", "country_intl", "1996-03-18",
        "Liquid single-country ETF; developed N. America"),
    ETF("EWH", "MSCI Hong Kong", "country_intl", "1996-03-18",
        "Liquid single-country ETF; developed APAC"),
    ETF("EWW", "MSCI Mexico", "country_intl", "1996-03-18",
        "Liquid single-country ETF; EM Latin America"),
    ETF("EWT", "MSCI Taiwan", "country_intl", "2000-06-23",
        "Liquid single-country ETF; EM Asia"),
    ETF("EWY", "MSCI South Korea", "country_intl", "2000-05-12",
        "Liquid single-country ETF; EM Asia"),
    ETF("INDA", "MSCI India", "country_intl", "2012-02-03",
        "Liquid single-country ETF; EM Asia (launched 2012)"),
    ETF("FXI", "China large-cap", "country_intl", "2004-10-08",
        "Liquid China large-cap ETF; EM Asia"),
    ETF("EEM", "MSCI Emerging Markets", "country_intl", "2003-04-14",
        "Broad EM basket; regional MR signal"),
    ETF("EFA", "MSCI EAFE (developed ex-US)", "country_intl", "2001-08-27",
        "Broad developed-ex-US basket; regional MR signal"),
]


# --- E2 leveraged universe (FROZEN 2026-07-09, record Appendix S) ---------
# DELIBERATELY a separate list, NOT appended to UNIVERSE: the E1 frozen-
# regression refs pin full-UNIVERSE backtest output, so growing UNIVERSE
# would silently flip the tripwire RED and break E1's reproducibility.
# E2 (PRD M2b) runs on THIS list. 3x long wrappers of underlyings where the
# IBS edge was validated OOS (E1b: broad US indices). data_start = first
# yfinance bar, fetched empirically 2026-07-09 — not invented.
LEVERAGED = [
    ETF("TQQQ", "ProShares UltraPro QQQ (3x Nasdaq-100)", "leveraged",
        "2010-02-11",
        "3x wrapper of QQQ, strongest E1b/ablation underlying; $5.1B/day"),
    ETF("UPRO", "ProShares UltraPro S&P 500 (3x)", "leveraged",
        "2009-06-25",
        "3x wrapper of SPY (core validated IBS instrument); $0.4B/day"),
    ETF("SPXL", "Direxion Daily S&P 500 Bull 3X", "leveraged",
        "2008-11-05",
        "Second 3x S&P wrapper (Direxion); $0.5B/day"),
    ETF("SOXL", "Direxion Daily Semiconductor Bull 3X", "leveraged",
        "2010-03-11",
        "3x semis — highest-vol liquid 3x fund; $10.9B/day"),
    ETF("TNA", "Direxion Daily Small Cap Bull 3X", "leveraged",
        "2008-11-19",
        "3x wrapper of IWM-class small caps (E1b universe member); $0.4B/day"),
]


def tickers(group=None):
    """All tickers, or those in one group (broad_us / spdr_sector /
    country_intl)."""
    return [e.ticker for e in UNIVERSE if group is None or e.group == group]


def by_ticker(ticker):
    for e in UNIVERSE:
        if e.ticker == ticker:
            return e
    raise KeyError(ticker)
