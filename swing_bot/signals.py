"""Signal primitives for swing_bot.

Only pure, deterministic primitives live here. Strategy logic (entry/exit
thresholds, position rules) is NOT here — that is E1, built in M2 against a
committed pre-registration doc.

IBS (Internal Bar Strength) = (close - low) / (high - low). Guards the
zero-range case (high == low) discovered in M0.4 (XLRE's illiquid early
bars): returns None so callers SKIP that ticker-day rather than divide by
zero. See .claude/codebase-memory/gotchas.md.

NAV (finding-things map): the only symbol here is `ibs()`. Imported by
swing_bot.backtest (E1 entry/exit) and swing_bot.test_frozen; scripts
ablation_fill_timing, run_m10_2_gap_amortized_ibs, screens_20260709. Strategy
thresholds are NOT here — they live in backtest.py (E1) and the runners.
"""


def ibs(high, low, close):
    """Internal Bar Strength in [0, 1], or None when the bar has no range
    (high <= low) — undefined, caller must skip."""
    if high <= low:
        return None
    return (close - low) / (high - low)
