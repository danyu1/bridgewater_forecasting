import json
import os
import re
from datetime import datetime

import requests

UA = "bridgewater-forecasting (monitor; contact: research@example.com)"

COMPANIES = {
    "MSFT": {"cik": "0000789019", "tag": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "GOOG": {"cik": "0001652044", "tag": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "AMZN": {"cik": "0001018724", "tag": "PaymentsToAcquireProductiveAssets"},
}


def fetch_companyfacts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    r = requests.get(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}, timeout=60)
    r.raise_for_status()
    return r.json()


def find_fact(facts, tag, frame=None, end=None, start=None, fp=None):
    us = facts.get("facts", {}).get("us-gaap", {})
    if tag not in us:
        return None
    units = us[tag].get("units", {})
    if "USD" not in units:
        return None
    items = units["USD"]
    best = None
    for it in items:
        if frame is not None and it.get("frame") != frame:
            continue
        if end is not None and it.get("end") != end:
            continue
        if start is not None and it.get("start") != start:
            continue
        if fp is not None and it.get("fp") != fp:
            continue
        best = it
    return best


def load_state(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_run_utc": None, "last_seen": {}}


def save_state(path, state):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def main():
    folder = os.path.dirname(__file__)
    state_path = os.path.join(folder, "monitor_state.json")
    state = load_state(state_path)
    report = {"timestamp_utc": datetime.utcnow().isoformat(), "alerts": [], "values": {}}

    target_year = 2025
    target_q = 4
    frame_q4 = f"CY{target_year}Q{target_q}"
    end_q4 = "2025-12-31"

    for ticker, meta in COMPANIES.items():
        facts = fetch_companyfacts(meta["cik"])
        tag = meta["tag"]

        q4 = find_fact(facts, tag, frame=frame_q4)
        if q4 is None:
            q4 = find_fact(facts, tag, end=end_q4, start="2025-10-01")

        ytd_q3 = find_fact(facts, tag, end="2025-09-30", start="2025-01-01")
        fy = find_fact(facts, tag, frame=f"CY{target_year}", end=end_q4) or find_fact(facts, tag, end=end_q4, start="2025-01-01")

        derived_q4 = None
        if q4 is None and ytd_q3 is not None and fy is not None:
            try:
                derived_q4 = float(fy.get("val")) - float(ytd_q3.get("val"))
            except Exception:
                derived_q4 = None

        val = None
        mode = None
        if q4 is not None:
            val = float(q4.get("val"))
            mode = "direct"
        elif derived_q4 is not None:
            val = float(derived_q4)
            mode = "derived_from_fy_minus_ytd_q3"

        report["values"][ticker] = {
            "mode": mode,
            "capex_payments_usd": val,
            "q4_fact": {k: q4.get(k) for k in ["start", "end", "frame", "form", "fp", "filed", "accn", "val"]} if q4 is not None else None,
            "ytd_q3_fact": {k: ytd_q3.get(k) for k in ["start", "end", "frame", "form", "fp", "filed", "accn", "val"]} if ytd_q3 is not None else None,
            "fy_fact": {k: fy.get(k) for k in ["start", "end", "frame", "form", "fp", "filed", "accn", "val"]} if fy is not None else None,
        }

        prev = state.get("last_seen", {}).get(ticker, {})
        if val is not None and (prev.get("capex_payments_usd") != val or prev.get("mode") != mode):
            report["alerts"].append({"type": "capex_update", "ticker": ticker, "prev": prev, "new": {"mode": mode, "capex_payments_usd": val}})

        state.setdefault("last_seen", {})[ticker] = {"mode": mode, "capex_payments_usd": val}

    state["last_run_utc"] = report["timestamp_utc"]
    save_state(state_path, state)

    day = datetime.utcnow().date().isoformat()
    md_path = os.path.join(folder, f"MONITORING_REPORT_{day}.md")
    lines = []
    lines.append(f"# Monitoring Report — Hyperscaler capex (Q4 2025)\n\nDate (UTC): {day}\n")
    for t, v in report["values"].items():
        lines.append(f"## {t}\n- Mode: {v['mode']}\n- Capex payments (USD): {v['capex_payments_usd']}\n")
    if report["alerts"]:
        lines.append("## Alerts\n" + "\n".join([f"- {a['type']}: {json.dumps(a, ensure_ascii=False)}" for a in report["alerts"]]) + "\n")
    else:
        lines.append("## Alerts\n- None\n")
    with open(md_path, "w") as f:
        f.write("\n".join(lines))

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
