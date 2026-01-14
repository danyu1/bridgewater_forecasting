import json
import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_spglobal_latest_from_home():
    url = "https://r.jina.ai/http://www.pmi.spglobal.com/?language=en"
    text = requests.get(url, timeout=30).text
    m = re.search(r"United States\s+MANUFACTURING PMI\s+([A-Za-z]{3})\s*:\s*([0-9]{2}\.\d)", text)
    if not m:
        return None
    return {"ref_month_label": m.group(1), "value": float(m.group(2))}


def fetch_ism_latest_released():
    url = "https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173"
    html = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="eventHistoryTable173")
    if not table or not table.tbody:
        return None
    for tr in table.tbody.find_all("tr"):
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(tds) < 5:
            continue
        actual = (tds[2] or "").strip()
        if not actual or actual in ["-", ""]:
            continue
        try:
            actual_v = float(actual)
        except Exception:
            continue
        return {"release_label": tds[0], "time": tds[1], "actual": actual_v, "forecast": tds[3], "previous": tds[4]}
    return None


def load_state(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"spglobal_latest": None, "ism_latest": None}


def save_state(path, state):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def fmt_change(old, new):
    if old is None or new is None:
        return None
    try:
        return float(new) - float(old)
    except Exception:
        return None


def main():
    folder = os.path.dirname(__file__)
    state_path = os.path.join(folder, "monitor_state.json")
    state = load_state(state_path)
    report = {"timestamp_utc": datetime.utcnow().isoformat(), "alerts": []}

    sp = fetch_spglobal_latest_from_home()
    ism = fetch_ism_latest_released()
    report["spglobal_latest"] = sp
    report["ism_latest"] = ism

    prev_sp = (state.get("spglobal_latest") or {}).get("value")
    prev_ism = (state.get("ism_latest") or {}).get("actual")
    sp_chg = fmt_change(prev_sp, sp["value"] if sp else None)
    ism_chg = fmt_change(prev_ism, ism["actual"] if ism else None)

    if sp and (state.get("spglobal_latest") != sp):
        report["alerts"].append({"type": "spglobal_update", "prev": state.get("spglobal_latest"), "new": sp})
    if ism and (state.get("ism_latest") != ism):
        report["alerts"].append({"type": "ism_update", "prev": state.get("ism_latest"), "new": ism})

    if sp_chg is not None and abs(sp_chg) >= 0.7:
        report["alerts"].append({"type": "spglobal_large_move", "delta": sp_chg})
    if ism_chg is not None and abs(ism_chg) >= 0.7:
        report["alerts"].append({"type": "ism_large_move", "delta": ism_chg})

    state["spglobal_latest"] = sp
    state["ism_latest"] = ism
    state["last_run_utc"] = report["timestamp_utc"]
    save_state(state_path, state)

    day = datetime.utcnow().date().isoformat()
    md_path = os.path.join(folder, f"MONITORING_REPORT_{day}.md")
    lines = []
    lines.append(f"# Monitoring Report (US Manufacturing PMI)\\n\\nDate (UTC): {day}\\n")
    if sp:
        lines.append(f"## S&P Global latest\\n- Ref month: {sp['ref_month_label']}\\n- Value: {sp['value']}\\n")
    else:
        lines.append("## S&P Global latest\\n- Unavailable\\n")
    if ism:
        lines.append(
            f"## ISM latest released\n- Release: {ism['release_label']}\n- Actual: {ism['actual']}\n- Forecast: {ism['forecast']}\n- Previous: {ism['previous']}\n"
        )
    else:
        lines.append("## ISM latest released\\n- Unavailable\\n")
    if report["alerts"]:
        lines.append(
            "## Alerts\n"
            + "\n".join([f"- {a['type']}: {json.dumps(a, ensure_ascii=False)}" for a in report["alerts"]])
            + "\n"
        )
    else:
        lines.append("## Alerts\\n- None\\n")
    with open(md_path, "w") as f:
        f.write("\n".join(lines))

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
