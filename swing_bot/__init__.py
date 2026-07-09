"""swing_bot — systematic swing-trading experiment package.

Separate project from D:\\ClaudeCode\\Trading (read-only reference only).
See PRD_ROADMAP.md for the execution plan and HANDOFF.md for current state.

Data convention: any price this package reads from Trading's price_cache or
fetches itself is SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED (yfinance
auto_adjust=False). Every price-touching module restates this in its header.
"""
