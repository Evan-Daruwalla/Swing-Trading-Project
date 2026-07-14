"""Ingest FINRA Reg SHO daily short-VOLUME for the 39 survivor large-caps
(X3, PRD M9 task 47). Scout-verified access, record Appendix BU.

CNMS consolidated file for 2018-08-01+; per-venue sum (FNYX+FNSQ+FNRA) for
2009-08-03..2018-07-31 (exchange-listed consolidation). Pipe-delimited, header
row, TRAILER line (record count) skipped; schema gained ShortExemptVolume on
2011-02-28 (read by header, not position); volumes may be fractional. 403 = no
file that day (weekend/holiday) -> skip. Signal stored = short-volume ratio
SVR = ShortVolume/TotalVolume per name per day (executed short FLOW - MM-hedging
contaminated, per BU; NOT short interest).

Resumable per-day (skips cached dates). Cache gitignored
(.regsho_cache/short_volume.json). No swing.db writes.
"""
import datetime as dt
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

CACHE = Path("D:/ClaudeCode/Swing Trading/.regsho_cache")
CACHE.mkdir(exist_ok=True)
OUT = CACHE / "short_volume.json"
BASE = "https://cdn.finra.org/equity/regsho/daily"
CNMS_FLOOR = "20180801"
VENUES = ("FNYX", "FNSQ", "FNRA")     # exchange-listed consolidation pre-2018

UNIV = set(("MSFT INTC CSCO ORCL IBM AAPL QCOM TXN ADBE JPM BAC WFC C GS AXP "
            "JNJ PFE MRK UNH ABT XOM CVX SLB COP KO PEP MCD WMT HD NKE PG "
            "BA HON MMM CAT GE T VZ DIS").split())


UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}   # Cloudflare 403s default UA


def fetch(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("latin-1")
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None


def parse(text, acc):
    """Accumulate {sym: [shortvol, totalvol]} into acc from one venue file."""
    lines = text.splitlines()
    if len(lines) < 2:
        return
    hdr = lines[0].split("|")
    try:
        si, sh, tv = hdr.index("Symbol"), hdr.index("ShortVolume"), hdr.index("TotalVolume")
    except ValueError:
        return
    n = len(hdr)
    for ln in lines[1:]:
        f = ln.split("|")
        if len(f) != n:                 # trailer / malformed
            continue
        s = f[si]
        if s not in UNIV:
            continue
        try:
            a = acc.setdefault(s, [0.0, 0.0])
            a[0] += float(f[sh]); a[1] += float(f[tv])
        except ValueError:
            continue


def main():
    cache = json.loads(OUT.read_text()) if OUT.exists() else {}
    d = dt.date(2009, 8, 3)
    end = dt.date(2026, 7, 10)
    got = miss = 0
    while d <= end:
        if d.weekday() < 5:                          # weekdays only
            key = d.isoformat()
            ymd = d.strftime("%Y%m%d")
            if key not in cache:
                acc = {}
                if ymd >= CNMS_FLOOR:
                    t = fetch(f"{BASE}/CNMSshvol{ymd}.txt")
                    if t:
                        parse(t, acc)
                else:
                    for v in VENUES:
                        t = fetch(f"{BASE}/{v}shvol{ymd}.txt")
                        if t:
                            parse(t, acc)
                        time.sleep(0.15)
                if acc:
                    cache[key] = {s: round(a[0] / a[1], 6)
                                  for s, a in acc.items() if a[1] > 0}
                    got += 1
                else:
                    miss += 1
                if (got + miss) % 200 == 0:
                    OUT.write_text(json.dumps(cache))
                    print(f"  {key}: got {got} miss {miss} "
                          f"(cached {len(cache)})", flush=True)
                time.sleep(0.15)
        d += dt.timedelta(days=1)
    OUT.write_text(json.dumps(cache))
    days = sorted(cache)
    cov = [len(cache[k]) for k in days] or [0]
    print(f"INGEST COMPLETE: {len(days)} days {days[0]}..{days[-1]}; "
          f"coverage min {min(cov)}/max {max(cov)}/mean {sum(cov)/len(cov):.1f} of 39")


if __name__ == "__main__":
    main()
