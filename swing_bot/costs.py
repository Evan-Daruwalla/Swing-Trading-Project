"""Measured round-trip friction, per prereg_v1_cost_model_and_validation_harness.md
(committed doc-only as ec51b91, before this file existed).

THE POINT: friction is a MEASURED quantity here, never an assumed constant. The
brief's F4 is blunt about why -- Bajgrowicz & Scaillet found in-sample TA
performance "completely offset by low transaction costs", and this project's own
X9 lost 70% of capital while 87.4% of its trades converged. A strategy must clear
its own friction before it clears any benchmark, so a wrong friction number
invalidates every downstream verdict.

DATA CONVENTION: all prices are SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED
(auto_adjust=False), matching swing_bot/prices.py and every other consumer.
`fill_divergence.sim_price` is a next-open fill under that same convention.

FAIL-LOUD CONTRACT (prereg section 2.2): with fewer than MIN_FILLS_FOR_ESTIMATE
observations this module RAISES. It does not fall back to a constant, does not
interpolate, and does not return a default with a warning -- a silent default is
how an assumption gets reported as a measurement. A caller may pass an explicit
assumed_bps=, and every result then carries friction_source="ASSUMED".
"""
from __future__ import annotations

import sqlite3
import statistics
from dataclasses import dataclass, field

from swing_bot.paper_sleeves import DB_PATH

MIN_FILLS_FOR_ESTIMATE = 20      # pre-registered, prereg section 2.2


class InsufficientFillData(RuntimeError):
    """Raised when friction cannot be MEASURED. Never caught internally to
    substitute a default -- that would defeat the entire contract."""


@dataclass
class FrictionEstimate:
    median_bps: float
    mean_bps: float
    p90_bps: float
    n_fills: int
    friction_source: str                      # "MEASURED" | "ASSUMED"
    instrument_class: str
    samples: list = field(default_factory=list)

    def __str__(self):
        tag = "" if self.friction_source == "MEASURED" else "  <-- NOT MEASURED"
        return ("friction[%s] median %.2f bps / mean %.2f / p90 %.2f  (n=%d, %s)%s"
                % (self.instrument_class, self.median_bps, self.mean_bps,
                   self.p90_bps, self.n_fills, self.friction_source, tag))


def _ro_conn(db_path=DB_PATH):
    return sqlite3.connect("file:%s?mode=ro" % str(db_path).replace("\\", "/"),
                           uri=True)


def load_measured_fills(db_path=DB_PATH, instrument_class="all"):
    """Signed friction in bps for every resolved fill in `fill_divergence`.

    Sign convention: POSITIVE = the fill was WORSE than the simulation assumed.
    fill_divergence rows are entries (buys), so alpaca_price > sim_price is an
    adverse fill. A sell-side table would need the sign flipped; there is no
    side column today, which is recorded as a limitation rather than assumed away.
    """
    conn = _ro_conn(db_path)
    try:
        rows = conn.execute(
            "SELECT ticker, date, sim_price, alpaca_price FROM fill_divergence "
            "WHERE alpaca_price IS NOT NULL AND sim_price > 0").fetchall()
    finally:
        conn.close()
    out = []
    for tk, d, sim, alp in rows:
        out.append({"ticker": tk, "date": d,
                    "bps": (alp - sim) / sim * 10000.0})
    return out


def estimate_friction(db_path=DB_PATH, instrument_class="all",
                      min_fills=MIN_FILLS_FOR_ESTIMATE, assumed_bps=None):
    """MEASURED friction, or RAISE.

    Pass assumed_bps=<n> to proceed on an explicit assumption; the returned
    estimate is then tagged friction_source="ASSUMED" so no downstream report can
    present it as a measurement.
    """
    if assumed_bps is not None:
        return FrictionEstimate(float(assumed_bps), float(assumed_bps),
                                float(assumed_bps), 0, "ASSUMED",
                                instrument_class, [])
    fills = load_measured_fills(db_path, instrument_class)
    n = len(fills)
    if n < min_fills:
        raise InsufficientFillData(
            "friction is NOT MEASURABLE for instrument_class=%r: %d fill(s) "
            "available, %d required.\n"
            "  Refusing to substitute a default -- an assumed constant reported "
            "as a measurement is exactly what this module exists to prevent.\n"
            "  To proceed on an explicit assumption, pass assumed_bps=<n>; the "
            "result will be tagged friction_source='ASSUMED'.\n"
            "  To fix properly: let the live paper loop accumulate fills in "
            "swing.db:fill_divergence." % (instrument_class, n, min_fills))
    vals = sorted(f["bps"] for f in fills)
    return FrictionEstimate(
        median_bps=statistics.median(vals),
        mean_bps=statistics.fmean(vals),
        p90_bps=vals[min(len(vals) - 1, int(0.9 * len(vals)))],
        n_fills=n, friction_source="MEASURED",
        instrument_class=instrument_class, samples=vals)


def round_trip_bps(est: FrictionEstimate) -> float:
    """Round trip = entry + exit. Uses the MEDIAN, not the mean: the current
    sample's mean is dominated by a single -85.7 bps outlier that is a documented
    discipline break (an intraday fire, record DE), not spread."""
    return 2.0 * est.median_bps
