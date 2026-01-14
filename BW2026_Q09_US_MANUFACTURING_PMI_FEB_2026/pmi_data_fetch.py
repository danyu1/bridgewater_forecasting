import csv
import re
import time
import io
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
MONTH_MAP = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}


def _clean(s):
    if s is None:
        return ""
    return str(s).replace("\x00", "").replace("\u0000", "").replace("\xa0", " ").strip()


def fetch_spglobal_pdfs(out_dir):
    pdfs = {
        "spglobal_us_mfg_pmi_2025_12_final.pdf": "https://www.pmi.spglobal.com/Public/Home/PressRelease/7ca2ebfa9cce4c768e0cf449ba966293",
        "spglobal_us_mfg_pmi_2025_11_final.pdf": "https://www.pmi.spglobal.com/Public/Home/PressRelease/7c2acaf676064c92bab19610524887d3",
    }
    headers = {
        "User-Agent": UA,
        "Accept": "application/pdf,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.pmi.spglobal.com/",
        "Origin": "https://www.pmi.spglobal.com",
    }
    s = requests.Session()
    for filename, url in pdfs.items():
        r = s.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        with open(f"{out_dir}/{filename}", "wb") as f:
            f.write(r.content)


def extract_spglobal_values(pdf_path):
    reader = PdfReader(pdf_path)
    text = "\n".join([(p.extract_text() or "") for p in reader.pages])
    m = re.search(r"recorded\s+(\d{2}\.\d)\s+in\s+December", text, flags=re.I)
    if m:
        return {"ref_year": 2025, "ref_month": 12, "value": float(m.group(1)), "source": pdf_path}
    m = re.search(r"recorded\s+(\d{2}\.\d)\s+in\s+November", text, flags=re.I)
    if m:
        return {"ref_year": 2025, "ref_month": 11, "value": float(m.group(1)), "source": pdf_path}
    return None


def fetch_investing_history(event_attr_id, event_url):
    more_url = "https://www.investing.com/economic-calendar/more-history"
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

    html = s.get(event_url, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id=f"eventHistoryTable{event_attr_id}")
    if not table:
        raise RuntimeError("history table not found")

    def parse_rows(tbody):
        out = []
        for tr in tbody.find_all("tr"):
            rid = tr.get("id", "")
            m = re.match(r"historicEvent_(\d+)", rid)
            if not m:
                continue
            hist_id = int(m.group(1))
            ts = tr.get("event_timestamp")
            tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
            if len(tds) < 5:
                continue
            out.append(
                {
                    "hist_id": hist_id,
                    "event_attr_id": int(tr.get("event_attr_id") or tr.get("event_attr_ID") or event_attr_id),
                    "event_timestamp": _clean(ts),
                    "release_label": _clean(tds[0]),
                    "time": _clean(tds[1]),
                    "actual": _clean(tds[2]),
                    "forecast": _clean(tds[3]),
                    "previous": _clean(tds[4]),
                }
            )
        return out

    rows = parse_rows(table.tbody)
    headers_xhr = {"X-Requested-With": "XMLHttpRequest", "Referer": event_url, "User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    seen = {r["hist_id"] for r in rows}

    while True:
        oldest = rows[-1]
        payload = {
            "eventID": str(oldest["hist_id"]),
            "event_attr_ID": str(event_attr_id),
            "event_timestamp": oldest["event_timestamp"],
            "is_speech": "0",
        }
        r = s.post(more_url, data=payload, headers=headers_xhr, timeout=30)
        r.raise_for_status()
        j = r.json()
        html_rows = j.get("historyRows", "")
        has_more = bool(j.get("hasMoreHistory"))
        if not html_rows:
            break
        frag = BeautifulSoup("<table><tbody>" + html_rows + "</tbody></table>", "html.parser")
        new = parse_rows(frag.tbody)
        new = [x for x in new if x["hist_id"] not in seen]
        if not new:
            break
        for x in new:
            seen.add(x["hist_id"])
        rows.extend(new)
        if not has_more:
            break
        time.sleep(0.15)

    return rows


def event_rows_to_month_series(rows):
    series = []
    for r in rows:
        label = r["release_label"]
        m = re.search(r"\(([^)]+)\)", label)
        ref = m.group(1).strip() if m else None
        rel = re.sub(r"\s*\([^)]+\)\s*", "", label).strip()
        rel_parts = rel.split()
        if len(rel_parts) < 3 or not ref:
            continue
        rel_mon = MONTH_MAP.get(rel_parts[0], None)
        rel_day = int(rel_parts[1].strip(","))
        rel_year = int(rel_parts[2])
        ref_mon = MONTH_MAP.get(ref[:3], None)
        if not rel_mon or not ref_mon:
            continue
        ref_year = rel_year
        if rel_mon == 1 and ref_mon == 12:
            ref_year = rel_year - 1
        if rel_mon == 2 and ref_mon == 12:
            ref_year = rel_year - 1
        actual = r["actual"]
        if not actual or actual in ["-", ""]:
            continue
        try:
            val = float(actual)
        except Exception:
            continue
        series.append({"ref_year": ref_year, "ref_month": ref_mon, "value": val, "release_date": f"{rel_year:04d}-{rel_mon:02d}-{rel_day:02d}"})

    uniq = {(s["ref_year"], s["ref_month"]): s for s in series}
    return sorted(uniq.values(), key=lambda s: (s["ref_year"], s["ref_month"]))


def main():
    out_dir = "BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026"
    fetch_spglobal_pdfs(out_dir)

    sp_vals = []
    for p in [f"{out_dir}/spglobal_us_mfg_pmi_2025_11_final.pdf", f"{out_dir}/spglobal_us_mfg_pmi_2025_12_final.pdf"]:
        v = extract_spglobal_values(p)
        if v:
            sp_vals.append(v)

    with open(f"{out_dir}/spglobal_known_points.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ref_year", "ref_month", "value", "source"])
        w.writeheader()
        for r in sp_vals:
            w.writerow(r)

    ism_event_url = "https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173"
    ism_rows = fetch_investing_history(173, ism_event_url)
    with open(f"{out_dir}/ism_event_history_raw.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ism_rows[0].keys()))
        w.writeheader()
        w.writerows(ism_rows)

    ism_series = event_rows_to_month_series(ism_rows)
    with open(f"{out_dir}/ism_pmi_history.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ref_year", "ref_month", "value", "release_date"])
        w.writeheader()
        w.writerows(ism_series)


if __name__ == "__main__":
    main()
