import csv
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


def write_text(path, s):
    with open(path, "w", newline="") as f:
        f.write(s)


def parse_fred_csv(text):
    reader = csv.DictReader(text.splitlines())
    fns = reader.fieldnames or []
    if not fns:
        return []
    date_key = "DATE" if "DATE" in fns else ("observation_date" if "observation_date" in fns else fns[0])
    val_key = [k for k in fns if k != date_key][0]
    rows = []
    for row in reader:
        d = row.get(date_key)
        v = row.get(val_key)
        if d is None or v is None:
            continue
        v = v.strip()
        if v == "" or v == ".":
            continue
        rows.append((d, float(v)))
    return rows


def parse_stooq_csv(text):
    reader = csv.DictReader(text.splitlines())
    rows = []
    for row in reader:
        d = row.get("Date")
        c = row.get("Close")
        if d is None or c is None:
            continue
        c = c.strip()
        if c == "" or c == "0":
            continue
        rows.append((d, float(c)))
    return rows


def main():
    folder = os.path.dirname(__file__)
    pay_txt = fetch_payems_fred()
    spx_txt = fetch_spx_stooq()

    write_text(os.path.join(folder, "payems_fred.csv"), pay_txt)
    write_text(os.path.join(folder, "sp500_stooq.csv"), spx_txt)

    pay = parse_fred_csv(pay_txt)
    spx = parse_stooq_csv(spx_txt)

    snap = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "payems_last": pay[-1] if pay else None,
        "spx_last": spx[-1] if spx else None,
    }
    with open(os.path.join(folder, "research_snapshot.json"), "w") as f:
        json.dump(snap, f, indent=2)

    print(json.dumps(snap, indent=2))


if __name__ == "__main__":
    main()
