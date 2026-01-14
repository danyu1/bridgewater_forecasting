import json
import os
from datetime import datetime

import requests


def fetch_text(url):
    r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text


def fetch_payems_fred():
    return fetch_text("https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS")


def fetch_spx_stooq():
    return fetch_text("https://stooq.com/q/d/l/?s=^spx&i=d")


def load_state(path):
    try:
        return json.load(open(path))
    except FileNotFoundError:
        return {"last_payems_last": None, "last_spx_last": None, "last_run_utc": None}


def last_nonempty_line(txt):
    lines = [x for x in txt.strip().splitlines() if x]
    if len(lines) < 2:
        return None
    for line in reversed(lines[1:]):
        if "," in line and not line.endswith(","):
            return line
    return None


def main():
    folder = os.path.dirname(__file__)
    state_path = os.path.join(folder, "monitor_state.json")
    state = load_state(state_path)

    pay_txt = fetch_payems_fred()
    spx_txt = fetch_spx_stooq()

    pay_last = last_nonempty_line(pay_txt)
    spx_last = last_nonempty_line(spx_txt)

    report = {"timestamp_utc": datetime.utcnow().isoformat(), "alerts": [], "payems_last": pay_last, "spx_last": spx_last}

    if state.get("last_payems_last") != pay_last:
        report["alerts"].append({"type": "payems_update", "prev": state.get("last_payems_last"), "new": pay_last})
    if state.get("last_spx_last") != spx_last:
        report["alerts"].append({"type": "spx_update", "prev": state.get("last_spx_last"), "new": spx_last})

    state["last_payems_last"] = pay_last
    state["last_spx_last"] = spx_last
    state["last_run_utc"] = report["timestamp_utc"]
    json.dump(state, open(state_path, "w"), indent=2)

    day = report["timestamp_utc"][:10]
    md_path = os.path.join(folder, f"MONITORING_REPORT_{day}.md")
    lines = []
    lines.append(f"# Monitoring Report — Payrolls & S&P 500\n\nDate (UTC): {day}\n")
    lines.append(f"- PAYEMS last: {pay_last}\n- SPX last: {spx_last}\n")
    if report["alerts"]:
        lines.append("## Alerts\n" + "\n".join([f"- {a['type']}: {json.dumps(a, ensure_ascii=False)}" for a in report["alerts"]]) + "\n")
    else:
        lines.append("## Alerts\n- None\n")
    open(md_path, "w").write("\n".join(lines))

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
