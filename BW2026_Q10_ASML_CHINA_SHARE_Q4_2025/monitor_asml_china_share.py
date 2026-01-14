import json
import os
import re
from datetime import datetime

import requests
from pypdf import PdfReader
import io

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def find_presentation_pdf(fin_results_url):
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


def extract_china_share(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join([(p.extract_text() or "") for p in reader.pages])
    m = re.search(r"Region\s*\(ship\s*[- ]?to\s*[- ]?location\).*?China\s*(\d{1,2})\s*%", text, flags=re.I | re.S)
    if m:
        return int(m.group(1))
    idx = text.lower().find("ship to location")
    if idx >= 0:
        window = text[idx : idx + 1200]
        m2 = re.search(r"China\s*(\d{1,2})\s*%", window, flags=re.I)
        if m2:
            return int(m2.group(1))
    return None


def load_state(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_run_utc": None, "last_value": None, "last_pdf": None, "last_page": None}


def save_state(path, state):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def main():
    folder = os.path.dirname(__file__)
    state_path = os.path.join(folder, "monitor_state.json")
    state = load_state(state_path)
    report = {"timestamp_utc": datetime.utcnow().isoformat(), "alerts": []}

    fin_url = "https://www.asml.com/en/investors/financial-results/q4-2025"
    report["financial_results_url"] = fin_url

    pdf_url = None
    china = None
    try:
        r = requests.get(fin_url, headers={"User-Agent": UA}, timeout=60)
        report["financial_results_status"] = r.status_code
        if r.status_code == 200:
            pdf_url = find_presentation_pdf(fin_url)
            report["presentation_pdf"] = pdf_url
            if pdf_url:
                pdf = requests.get(pdf_url, headers={"User-Agent": UA}, timeout=120).content
                china = extract_china_share(pdf)
                report["china_share_pct"] = china
                report["status"] = "parsed" if china is not None else "parse_failed"
            else:
                report["status"] = "presentation_not_found"
        else:
            report["status"] = "not_available"
    except Exception as e:
        report["error"] = str(e)
        report["status"] = "error"

    if china is not None and (state.get("last_value") != china or state.get("last_pdf") != pdf_url):
        report["alerts"].append({"type": "value_update", "prev": {"value": state.get("last_value"), "pdf": state.get("last_pdf")}, "new": {"value": china, "pdf": pdf_url}})

    state["last_run_utc"] = report["timestamp_utc"]
    state["last_value"] = china
    state["last_pdf"] = pdf_url
    state["last_page"] = fin_url
    save_state(state_path, state)

    day = datetime.utcnow().date().isoformat()
    md_path = os.path.join(folder, f"MONITORING_REPORT_{day}.md")
    lines = []
    lines.append(f"# Monitoring Report — ASML China share (Q4 2025)\n\nDate (UTC): {day}\n")
    lines.append(f"- Financial results page: {fin_url}\n- Status: {report.get('status')}\n- Presentation PDF: {pdf_url}\n- Extracted China share: {china}\n")
    if report["alerts"]:
        lines.append("## Alerts\n" + "\n".join([f"- {a['type']}: {json.dumps(a, ensure_ascii=False)}" for a in report["alerts"]]) + "\n")
    else:
        lines.append("## Alerts\n- None\n")
    with open(md_path, "w") as f:
        f.write("\n".join(lines))

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
