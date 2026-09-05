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
degradation.

WHERE IT IS ACTUALLY ENFORCED — corrected 2026-08-06 (audit #3). This docstring
used to say "enforced by the coverage/quality gate (M0.4)". That was FALSE:
coverage_gate.py contains no reference to MIN_MEDIAN_DOLLAR_VOL and never has.
CLAUDE.md calls the floor mandatory in any universe filter, so the honest status
is UNENFORCED almost everywhere:
  * ENFORCED  daily_swing_paper.py:~570, the M10-1 39-name residual ranking --
              the only place the live loop picks individual stocks. Note this
              branch is gated on VIX > 20 and has never executed (VIX 15-16 for
              the whole live period), so the floor has never actually run.
  * NOT enforced  universe_m12.py (142 names; feeds M12 and the V1 harness),
              run_e10_earnings_drift.UNIV (39 names), this ETF list.
Extending it to the backtest universes would move recorded results, so it needs
its own pre-registration rather than a quiet patch.

NAV (finding-things map): exports `UNIVERSE` (the frozen ETF list) + `ETF`
namedtuple + `MIN_MEDIAN_DOLLAR_VOL`. Imported by swing_bot.{backtest,
coverage_gate, test_frozen} and runners run_e18_regime_gates, run_e1/e1b/e2,
run_c3, run_e20, run_ex_decomp, ... (the 39-name survivor list used by M10-1
lives in run_e10_earnings_drift.UNIV, NOT here — this is the ETF universe).
"""
from collections import namedtuple

ETF = namedtuple("ETF", ["ticker", "name", "group", "data_start", "reason"])

# 20-day median dollar-volume floor. CLAUDE.md calls this floor MANDATORY in
# any universe filter.
#
# CORRECTED 2026-09-05 (F3, record FG): this said "guard only; every current
# member clears it by a wide margin". That was a present-tense snapshot read
# as a property of the series, and it is false as history -- **26 of the 29
# members have breached this floor at some point**, on 28,776 of 179,055
# ticker-sessions (16.07%). Worst: EWZ 2000-10-30 at $3,619, which is
# 0.0002x the floor. Top breachers by session count: EWU 2,886, EWG 2,231,
# EWC 1,898, EWA 1,809, EWH 1,677, EWW 1,468, XLY 1,453, XLP 1,416.
#
# The value and the 20-session window were set at M0.4 and are NOT tuned.
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


def median_dollar_volume(dates, close, vol, n=20, asof=None):
    """Median close*volume over the last `n` sessions up to and including `asof`.
    Past-only -- never looks beyond `asof`. Returns None when fewer than
    max(5, n//2) sessions carry usable close AND volume -- i.e. LIQUIDITY IS
    UNKNOWN, not "known adequate".

    (2026-09-05, finding 4) This docstring used to instruct callers NOT to treat
    the name as illiquid on missing data alone, and the one caller obeyed it by
    testing `adv is not None and adv < FLOOR` -- which waved every data-starved
    name straight past the floor CLAUDE.md calls mandatory. Callers must now
    FAIL CLOSED on None: exclude the name, because a feed gap, a halt, or thin
    history is exactly the condition under which the floor matters most.
    """
    ds = [d for d in dates if asof is None or d <= asof][-n:]
    vals = [close[d] * vol[d] for d in ds
            if close.get(d) is not None and vol.get(d)]
    if len(vals) < max(5, n // 2):
        return None
    vals.sort()
    m = len(vals) // 2
    return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2.0


def is_liquid(dates, close, vol, asof=None, n=20, floor=None):
    """Is this name eligible under the liquidity floor as of `asof`? -> bool.

    THE single eligibility predicate; F3 (2026-09-05) exists because the floor
    above was enforced NOWHERE in the research runners while CLAUDE.md called it
    mandatory. Fails closed: unmeasurable volume returns False, matching the
    live loop's screen in scripts/daily_swing_paper.py (record FK). A feed gap,
    a halt, or thin history is exactly the condition under which the floor
    matters most, so "unknown" is never read as "fine".

    `floor` defaults to MIN_MEDIAN_DOLLAR_VOL; it is a parameter only so a
    caller can PROVE the guard fires (a floor no name can clear), never so a
    runner can pick its own threshold.
    """
    adv = median_dollar_volume(dates, close, vol, n=n, asof=asof)
    if adv is None:
        return False
    return adv >= (MIN_MEDIAN_DOLLAR_VOL if floor is None else floor)


def liquidity_mask(bars, n=20, floor=None, close_ix=5, vol_ix=7):
    """Per-bar eligibility under the liquidity floor -> list[bool], aligned to
    `bars` by index.

    Added 2026-09-05 for F3 (prereg_f3_liquidity_floor_etf_scope.md). The
    research runners screen candidates through this BEFORE ranking them, which
    is the point CLAUDE.md's "mandatory in any universe filter" was previously
    true nowhere: until today the floor was enforced only in the live M10-1
    stress screen, and 26 of the 29 ETFs in UNIVERSE breach it at some point.

    Past-only at every index: mask[i] uses bars[..i] and never a later bar, so
    it cannot leak future liquidity into a historical decision. FAILS CLOSED --
    an index with too few usable bars behind it is False, matching is_liquid()
    and the live loop (record FK).

    `bars` is the cached-bar layout shared by prices.fetch and
    run_e8_squeeze.cache_fetch: (ticker, date, o, h, l, c, adj, vol), hence the
    close_ix=5 / vol_ix=7 defaults; they are parameters only so a caller with a
    different tuple can say so, never so a runner can point them elsewhere.
    """
    out = []
    need = max(5, n // 2)
    floor_v = MIN_MEDIAN_DOLLAR_VOL if floor is None else floor
    for i in range(len(bars)):
        vals = []
        for b in bars[max(0, i - n + 1):i + 1]:
            c, v = b[close_ix], b[vol_ix]
            if c is not None and v:
                vals.append(c * v)
        if len(vals) < need:
            out.append(False)
            continue
        vals.sort()
        m = len(vals) // 2
        med = vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2.0
        out.append(med >= floor_v)
    return out


def tickers(group=None):
    """All tickers, or those in one group (broad_us / spdr_sector /
    country_intl)."""
    return [e.ticker for e in UNIVERSE if group is None or e.group == group]


def by_ticker(ticker):
    for e in UNIVERSE:
        if e.ticker == ticker:
            return e
    raise KeyError(ticker)
