"""Backfill the frozen ETF universe into swing.db via swing_bot.prices.

Idempotent (INSERT OR REPLACE). Run from the project root with the venv:
    .venv\\Scripts\\python.exe -m scripts.backfill_universe

Prices are split-adjusted, dividend-UNADJUSTED (auto_adjust=False), matching
the project convention. Default history start 2014-01-01 (plenty for E1).

NAV (finding-things map): imports swing_bot (prices, universe). Imported by:
no other module (standalone runner).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from swing_bot import prices, universe

START = "2014-01-01"


def main():
    conn = prices.connect()
    total = 0
    print(f"{'ticker':7}{'rows':>8}{'min':>12}{'max':>12}")
    print("-" * 39)
    for t in universe.tickers():
        n = prices.backfill(conn, t, start=START)
        total += n
        cov = prices.coverage(conn, t)
        print(f"{t:7}{cov[0]:>8}{cov[1]:>12}{cov[2]:>12}")
    print("-" * 39)
    print(f"{len(universe.UNIVERSE)} tickers, {total} rows written to "
          f"{prices.DB_PATH}")


if __name__ == "__main__":
    main()
