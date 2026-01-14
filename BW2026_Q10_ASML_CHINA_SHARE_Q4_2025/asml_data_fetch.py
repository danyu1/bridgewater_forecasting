import csv
import io
import json
import os
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_sitemap_urls():
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    xml = s.get("https://www.asml.com/sitemap-1.xml", timeout=60).text
    urls = re.findall(r"<loc>(.*?)</loc>", xml)
    qpages = [u for u in urls if "/en/investors/financial-results/q" in u and re.search(r"/q[1-4]-20\d\d$", u)]
    def key(u):
        m = re.search(r"/(q[1-4])-(20\d\d)$", u)
        q = int(m.group(1)[1])
        y = int(m.group(2))
        return (y, q)
    return sorted(qpages, key=key)


def find_investor_presentation_pdf(fin_results_url):
    html = requests.get(fin_results_url, headers={"User-Agent": UA}, timeout=60).text
    pdfs = re.findall(r"https?://[^\s\"']+\.pdf", html)
    pdfs = list(dict.fromkeys(pdfs))
    preferred = []
    for u in pdfs:
        name = u.lower()
        if "presentation" in name and "investor" in name and ("relations" in name or "ir" in name):
            preferred.append(u)
    if preferred:
        return preferred[0]
    for u in pdfs:
        if "presentation" in u.lower():
            return u
    return None


def extract_china_share_from_presentation_pdf(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join([(p.extract_text() or "") for p in reader.pages])
    idx = text.lower().find("region (ship to location)")
    if idx < 0:
        idx = text.lower().find("ship to location")
    if idx < 0:
        return None
    window = text[idx : idx + 800]
    m = re.search(r"China\s*(\d{1,2})\s*%", window, flags=re.I)
    if m:
        return int(m.group(1))
    m2 = re.search(r"China\s*(\d{1,2})\b", window, flags=re.I)
    if m2:
        v = int(m2.group(1))
        if 0 <= v <= 100:
            return v
    return None


def infer_quarter_from_url(url):
    m = re.search(r"/(q[1-4])-(20\d\d)$", url)
    if not m:
        return None
    q = int(m.group(1)[1])
    y = int(m.group(2))
    return y, q


def main():
    folder = os.path.dirname(__file__)
    out_csv = os.path.join(folder, "asml_china_share_history.csv")
    out_json = os.path.join(folder, "research_snapshot.json")
    urls = fetch_sitemap_urls()

    rows = []
    sources = []
    for fin_url in urls:
        yq = infer_quarter_from_url(fin_url)
        if not yq:
            continue
        y, q = yq
        if (y, q) > (2025, 3):
            continue
        pdf_url = find_investor_presentation_pdf(fin_url)
        if not pdf_url:
            sources.append({"quarter": f"{y}Q{q}", "financial_results_url": fin_url, "error": "presentation_pdf_not_found"})
            continue
        try:
            r = requests.get(pdf_url, headers={"User-Agent": UA}, timeout=120)
            r.raise_for_status()
            share = extract_china_share_from_presentation_pdf(r.content)
            if share is None:
                sources.append({"quarter": f"{y}Q{q}", "financial_results_url": fin_url, "presentation_pdf": pdf_url, "error": "china_share_not_found_in_pdf"})
                continue
            rows.append({"year": y, "quarter": q, "china_share_pct": share})
            sources.append({"quarter": f"{y}Q{q}", "financial_results_url": fin_url, "presentation_pdf": pdf_url, "china_share_pct": share})
        except Exception as e:
            sources.append({"quarter": f"{y}Q{q}", "financial_results_url": fin_url, "presentation_pdf": pdf_url, "error": str(e)})
        time.sleep(0.15)

    rows = sorted(rows, key=lambda r: (r["year"], r["quarter"]))
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "quarter", "china_share_pct"])
        w.writeheader()
        w.writerows(rows)

    snap = {"as_of_utc": datetime.utcnow().isoformat(), "n_points": len(rows), "sources": sources}
    with open(out_json, "w") as f:
        json.dump(snap, f, indent=2)

    print(json.dumps({"n_points": len(rows), "min": rows[0] if rows else None, "max": rows[-1] if rows else None}, indent=2))


if __name__ == "__main__":
    main()
