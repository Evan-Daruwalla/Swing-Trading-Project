"""swing_bot — systematic swing-trading experiment package.

Separate project from D:\\ClaudeCode\\Trading (read-only reference only).
See PRD_ROADMAP.md for the execution plan and HANDOFF.md for current state.

Data convention: any price this package reads from Trading's price_cache or
fetches itself is SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED (yfinance
auto_adjust=False). Every price-touching module restates this in its header.
"""
from pathlib import Path

# ONE home for the project DB path (PRD M13.6, FH low). It was defined
# identically in prices.py and paper_sleeves.py -- two definitions that could
# drift apart with nothing to catch it. It lives HERE rather than in either
# module because the alternative, having paper_sleeves import prices, would drag
# yfinance into the paper-ledger module that costs.py, test_frozen and
# prove_divergence_census.py all import; a yfinance import failure would then
# take out the ledger. This file imports no submodule, so there is no cycle.
DB_PATH = Path(__file__).resolve().parent.parent / "swing.db"
