"""E19 ingestion (per prereg ebf54a4): SEC EDGAR Form-4 -> open-market
insider PURCHASES (code P, acquired) for the 39 survivor large-caps.

Resumable: caches per-ticker P-buy events to .edgar_cache/{ticker}.json;
skips tickers already cached. Rate-limited ~7/s (SEC asks <10/s). Former-CIK
map recovers XOM/DIS pre-reorg history. Parses RAW Form-4 XML (not the XSL
render). ~104k documents total -> hours; run in background.

No swing.db writes. Data feeds run_e19_insider.py.

NAV (finding-things map): imports no project modules (self-contained).
Imported by: no other module (standalone runner).
"""
import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import httpx
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Swing-Trading-Research evan.research@example.com"}
CACHE = Path("D:/ClaudeCode/Swing Trading/.edgar_cache")
CACHE.mkdir(exist_ok=True)
UNIV = ("MSFT INTC CSCO ORCL IBM AAPL QCOM TXN ADBE JPM BAC WFC C GS AXP "
        "XOM CVX COP SLB PG KO PEP WMT MCD HD NKE DIS JNJ PFE MRK ABT UNH "
        "GE CAT BA MMM HON T VZ").split()
# former CIKs for names whose current CIK misses pre-reorg history (probed)
FORMER = {"XOM": ["0000034088"], "DIS": ["0001001039"]}
DELAY = 0.14   # ~7 req/s


def get(url, tries=4):
    for k in range(tries):
        try:
            r = httpx.get(url, headers=UA, timeout=30, follow_redirects=True)
            if r.status_code == 200:
                return r
            if r.status_code in (403, 429):
                time.sleep(2 + 3 * k)          # back off on throttle
        except Exception:
            time.sleep(1 + k)
        time.sleep(DELAY)
    return None


def ticker_ciks(tmap, t):
    ciks = []
    if t in tmap:
        ciks.append(tmap[t])
    ciks += FORMER.get(t, [])
    return ciks


def form4_list(cik):
    """(accession_nodash, primaryDocument, filingDate) for every Form-4."""
    out = []
    r = get(f"https://data.sec.gov/submissions/CIK{cik}.json")
    if not r:
        return out, None
    j = r.json()
    blocks = [j["filings"]["recent"]]
    for fm in j["filings"].get("files", []):
        time.sleep(DELAY)
        rr = get(f"https://data.sec.gov/submissions/{fm['name']}")
        if rr:
            blocks.append(rr.json())
    for b in blocks:
        for i in range(len(b["form"])):
            if b["form"][i] == "4":
                out.append((b["accessionNumber"][i].replace("-", ""),
                            b["primaryDocument"][i], b["filingDate"][i]))
    return out, j.get("name")


def parse_pbuys(xml_text, filing_date):
    """Return list of P-purchase (acquired) non-derivative transactions."""
    try:
        root = ET.fromstring(xml_text)
    except Exception:
        return []
    def strip(tag):
        return tag.split("}")[-1]
    owner = None
    for e in root.iter():
        if strip(e.tag) == "rptOwnerCik":
            owner = (e.text or "").strip(); break
    buys = []
    for txn in root.iter():
        if strip(txn.tag) != "nonDerivativeTransaction":
            continue
        code = tdate = ad = shares = price = None
        for e in txn.iter():
            tg = strip(e.tag)
            if tg == "transactionCode":
                code = (e.text or "").strip()
            elif tg == "transactionDate":
                for c in e.iter():
                    if strip(c.tag) == "value":
                        tdate = (c.text or "").strip()
            elif tg == "transactionAcquiredDisposedCode":
                for c in e.iter():
                    if strip(c.tag) == "value":
                        ad = (c.text or "").strip()
            elif tg == "transactionShares":
                for c in e.iter():
                    if strip(c.tag) == "value":
                        shares = (c.text or "").strip()
            elif tg == "transactionPricePerShare":
                for c in e.iter():
                    if strip(c.tag) == "value":
                        price = (c.text or "").strip()
        if code == "P" and ad == "A":
            buys.append(dict(owner=owner, tdate=tdate, fdate=filing_date,
                             shares=shares, price=price))
    return buys


def raw_url(cik, acc, primary):
    doc = primary.split("/")[-1] if primary.startswith("xsl") else primary
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"


def main():
    r = get("https://www.sec.gov/files/company_tickers.json")
    tmap = {row["ticker"]: str(row["cik_str"]).zfill(10)
            for _, row in r.json().items()}
    for t in UNIV:
        cf = CACHE / f"{t}.json"
        if cf.exists():
            print(f"{t}: cached, skip", flush=True)
            continue
        pbuys, nfiled, nfetch = [], 0, 0
        for cik in ticker_ciks(tmap, t):
            lst, name = form4_list(cik)
            nfiled += len(lst)
            print(f"{t} CIK {cik} ({name}): {len(lst)} Form-4", flush=True)
            for acc, primary, fdate in lst:
                time.sleep(DELAY)
                rr = get(raw_url(cik, acc, primary))
                nfetch += 1
                if rr and ("ownershipDocument" in rr.text):
                    pbuys += parse_pbuys(rr.text, fdate)
                if nfetch % 500 == 0:
                    print(f"  {t}: {nfetch}/{nfiled} fetched, "
                          f"{len(pbuys)} P-buys so far", flush=True)
        cf.write_text(json.dumps(pbuys))
        print(f"{t}: DONE {nfetch} fetched -> {len(pbuys)} P-buys cached",
              flush=True)
    print("INGEST COMPLETE", flush=True)


if __name__ == "__main__":
    main()
