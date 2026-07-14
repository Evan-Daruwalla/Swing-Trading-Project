"""Ingest FINRA consolidated exchange-listed short interest for the 39-name
survivor universe (X2 / E17-modern, PRD M9 task 46).

Public FINRA REST API, no auth (scout-verified 2026-07-13, record Appendix BU):
  partitions: GET  /partitions/group/otcMarket/name/consolidatedShortInterest
  data:       POST /data/group/otcMarket/name/consolidatedShortInterest
Biweekly settlement dates back to 2017-12-29; daysToCoverQuantity is PRECOMPUTED
(shares short / ADV). Filter to the 39 symbols per date (<39 rows, no paging).

DATA NOTE: this is SETTLEMENT-date short interest (point-in-time as-of settle);
public dissemination lags ~8-9 business days -> the RUNNER enters on a lagged
date, NOT the settlement date (lookahead guard lives in the runner, not here).
Cache is gitignored (.finra_cache/short_interest.json). No swing.db writes.
"""
import csv
import io
import json
import time
import urllib.request
from pathlib import Path

BASE = "https://api.finra.org"
GROUP = "otcMarket"
NAME = "consolidatedShortInterest"
CACHE = Path("D:/ClaudeCode/Swing Trading/.finra_cache")
CACHE.mkdir(exist_ok=True)
OUT = CACHE / "short_interest.json"

UNIV = ("MSFT INTC CSCO ORCL IBM AAPL QCOM TXN ADBE JPM BAC WFC C GS AXP "
        "JNJ PFE MRK UNH ABT XOM CVX SLB COP KO PEP MCD WMT HD NKE PG "
        "BA HON MMM CAT GE T VZ DIS").split()


def _get(path):
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def _post_csv(path, body):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode()


def parse_csv(text):
    # proper CSV: issueName can contain commas inside quotes
    if not text.strip():
        return []
    return list(csv.DictReader(io.StringIO(text)))


def main():
    part = _get(f"/partitions/group/{GROUP}/name/{NAME}")
    dates = sorted(p["partitions"][0] for p in part["availablePartitions"])
    print(f"partitions: {len(dates)} settlement dates {dates[0]}..{dates[-1]}")

    cache = json.loads(OUT.read_text()) if OUT.exists() else {}
    symfilter = {"compareFilters": [
        {"fieldName": "symbolCode", "fieldValue": s, "compareType": "EQUAL"}
        for s in UNIV]}
    for i, d in enumerate(dates):
        if d in cache:
            continue
        body = {"limit": 100,
                "compareFilters": [{"fieldName": "settlementDate",
                                    "fieldValue": d, "compareType": "EQUAL"}],
                "orFilters": [symfilter]}
        rows = parse_csv(_post_csv(f"/data/group/{GROUP}/name/{NAME}", body))
        cache[d] = {r["symbolCode"]: {
            "dtc": float(r["daysToCoverQuantity"] or 0),
            "short": float(r["currentShortPositionQuantity"] or 0),
            "adv": float(r["averageDailyVolumeQuantity"] or 0)}
            for r in rows if r.get("symbolCode")}
        if i % 20 == 0 or d == dates[-1]:
            print(f"  {d}: {len(cache[d])}/39 names  ({i+1}/{len(dates)})", flush=True)
        OUT.write_text(json.dumps(cache))
        time.sleep(0.3)
    OUT.write_text(json.dumps(cache))
    ncov = [len(cache[d]) for d in dates]
    print(f"INGEST COMPLETE: {len(dates)} dates cached; coverage "
          f"min {min(ncov)} / max {max(ncov)} / mean {sum(ncov)/len(ncov):.1f} of 39")


if __name__ == "__main__":
    main()
