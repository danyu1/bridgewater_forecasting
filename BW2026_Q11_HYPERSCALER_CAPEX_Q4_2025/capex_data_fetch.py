import csv
import json
import os
import re
from datetime import datetime

import requests

UA = "bridgewater-forecasting (SEC XBRL fetch; contact: research@example.com)"

COMPANIES = {
    "MSFT": {"cik": "0000789019", "name": "Microsoft", "payments_tag": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "GOOG": {"cik": "0001652044", "name": "Alphabet", "payments_tag": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "AMZN": {"cik": "0001018724", "name": "Amazon", "payments_tag": "PaymentsToAcquireProductiveAssets"},
}


def q_from_end_date(end):
    y, m, _ = end.split("-")
    y = int(y)
    m = int(m)
    if m <= 3:
        q = 1
    elif m <= 6:
        q = 2
    elif m <= 9:
        q = 3
    else:
        q = 4
    return y, q


def fetch_companyfacts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    r = requests.get(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}, timeout=60)
    r.raise_for_status()
    return r.json()


def extract_quarterly_payments(facts, tag):
    us = facts.get("facts", {}).get("us-gaap", {})
    if tag not in us:
        return {}
    units = us[tag].get("units", {})
    if "USD" not in units:
        return {}
    items = units["USD"]

    by_end = {}
    by_frame = {}
    for it in items:
        end = it.get("end")
        val = it.get("val")
        if end is None or val is None:
            continue
        frame = it.get("frame")
        start = it.get("start")
        form = it.get("form")
        fp = it.get("fp")
        if frame and re.match(r"CY\d{4}Q[1-4]$", frame):
            by_frame[frame] = {"end": end, "val": float(val), "start": start, "form": form, "fp": fp, "frame": frame}
        if frame and re.match(r"CY\d{4}$", frame) and end.endswith("-12-31"):
            by_frame[frame] = {"end": end, "val": float(val), "start": start, "form": form, "fp": fp, "frame": frame}
        if start and start.endswith("-01-01") and fp in ["Q2", "Q3"]:
            by_end.setdefault(end, []).append({"start": start, "end": end, "val": float(val), "form": form, "fp": fp, "frame": frame})

    out = {}
    for frame, rec in by_frame.items():
        y = int(frame[2:6])
        if frame.endswith(("Q1", "Q2", "Q3", "Q4")):
            q = int(frame[-1])
        else:
            q = 0
        out[(y, q)] = rec

    for end, recs in by_end.items():
        y, q = q_from_end_date(end)
        if (y, q) in out:
            continue
        recs = sorted(recs, key=lambda r: r["val"])
        out[(y, q)] = recs[-1]

    return out


def derive_quarters_from_ytd(qmap):
    out = {}
    for (y, q), rec in qmap.items():
        out[(y, q)] = rec["val"]

    years = sorted(set(y for (y, q) in out))
    for y in years:
        q1 = out.get((y, 1))
        q2_ytd = out.get((y, 2))
        q3_ytd = out.get((y, 3))
        if q1 is not None and q2_ytd is not None and (y, 2) in out and qmap.get((y, 2), {}).get("start", "").endswith("-01-01"):
            out[(y, 2)] = q2_ytd - q1
        if q2_ytd is not None and q3_ytd is not None and (y, 3) in out and qmap.get((y, 3), {}).get("start", "").endswith("-01-01"):
            out[(y, 3)] = q3_ytd - q2_ytd

    return out


def main():
    folder = os.path.dirname(__file__)
    out_csv = os.path.join(folder, "capex_history_quarterly.csv")
    out_json = os.path.join(folder, "research_snapshot.json")

    all_rows = []
    snap = {"as_of_utc": datetime.utcnow().isoformat(), "sources": {}}

    for ticker, meta in COMPANIES.items():
        facts = fetch_companyfacts(meta["cik"])
        qmap = extract_quarterly_payments(facts, meta["payments_tag"])
        qvals = derive_quarters_from_ytd(qmap)

        snap["sources"][ticker] = {
            "cik": meta["cik"],
            "payments_tag": meta["payments_tag"],
            "n_quarters_extracted": len(qvals),
        }

        for (y, q), val in qvals.items():
            all_rows.append({"ticker": ticker, "year": y, "quarter": q, "payments_usd": float(val)})

    all_rows.sort(key=lambda r: (r["year"], r["quarter"], r["ticker"]))
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "year", "quarter", "payments_usd"])
        w.writeheader()
        w.writerows(all_rows)

    with open(out_json, "w") as f:
        json.dump(snap, f, indent=2)

    print(json.dumps({"rows": len(all_rows), "min": all_rows[0] if all_rows else None, "max": all_rows[-1] if all_rows else None}, indent=2))


if __name__ == "__main__":
    main()
