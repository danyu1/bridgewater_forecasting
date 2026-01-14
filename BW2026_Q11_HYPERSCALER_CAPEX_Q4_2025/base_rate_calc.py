import csv
import json
import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


def load_series(path):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((row["ticker"], int(row["year"]), int(row["quarter"]), float(row["payments_usd"])))
    return rows


def build_maps(rows):
    q = {}
    annual = {}
    for ticker, year, quarter, val in rows:
        if quarter == 0:
            annual[(ticker, year)] = val
        else:
            q[(ticker, year, quarter)] = val
    return q, annual


def derive_q4_from_annual(qmap, annual_map, ticker, year):
    if (ticker, year, 4) in qmap:
        return qmap[(ticker, year, 4)]
    if (ticker, year) not in annual_map:
        return None
    total = annual_map[(ticker, year)]
    needed = [(ticker, year, 1), (ticker, year, 2), (ticker, year, 3)]
    if any(k not in qmap for k in needed):
        return None
    return total - qmap[needed[0]] - qmap[needed[1]] - qmap[needed[2]]


def to_b(val_usd):
    return val_usd / 1e9


def main():
    folder = os.path.dirname(__file__)
    rows = load_series(os.path.join(folder, "capex_history_quarterly.csv"))
    qmap, annual_map = build_maps(rows)

    tickers = ["MSFT", "GOOG", "AMZN"]
    years = sorted(set(y for (_, y, q, _) in rows if q != 0))

    def get_payments(t, y, q):
        if (t, y, q) in qmap:
            return qmap[(t, y, q)]
        if t in ["GOOG", "AMZN"] and q == 4:
            v = derive_q4_from_annual(qmap, annual_map, t, y)
            if v is not None:
                return v
        return None

    def amazon_inflow_b(y, q):
        known = {
            (2024, 4): 1.782,
            (2025, 1): 0.764,
            (2025, 2): 0.815,
            (2025, 3): 0.867,
        }
        return known.get((y, q), 1.0)

    def total_capex_b(y, q):
        ms = get_payments("MSFT", y, q)
        gg = get_payments("GOOG", y, q)
        az = get_payments("AMZN", y, q)
        if ms is None or gg is None or az is None:
            return None
        total = to_b(ms) + to_b(gg) + to_b(az) - amazon_inflow_b(y, q)
        return float(total)

    totals = []
    for y in years:
        for q in [1, 2, 3, 4]:
            v = total_capex_b(y, q)
            if v is not None:
                totals.append((y, q, v))
    totals.sort()

    ratios = []
    for y in sorted(set(y for y, q, v in totals)):
        v3 = next((v for yy, qq, v in totals if yy == y and qq == 3), None)
        v4 = next((v for yy, qq, v in totals if yy == y and qq == 4), None)
        if v3 is None or v4 is None or v3 <= 0:
            continue
        ratios.append({"year": y, "q4_over_q3": float(v4 / v3), "q3": float(v3), "q4": float(v4)})

    q3_2025 = 77.575
    rng = np.random.default_rng(42)
    rvals = np.array([r["q4_over_q3"] for r in ratios], dtype=float)
    if len(rvals) == 0:
        rvals = np.array([1.12], dtype=float)
    n = 200000
    sampled_ratio = rng.choice(rvals, size=n, replace=True)
    base_total = q3_2025 * sampled_ratio

    out = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "definition": "Combined capex (MSFT+GOOG+AMZN) for quarter ending 2025-12-31; capex is PP&E cash outflows net of PP&E proceeds/incentives (Amazon adjustment)",
        "inputs": {"q3_2025_total_capex_b": q3_2025, "amazon_inflow_assumption_other_quarters_b": 1.0},
        "q4_over_q3_history": ratios,
        "base_rate_total_q4_2025_b": {
            "mean": float(base_total.mean()),
            "p5": float(np.percentile(base_total, 5)),
            "p25": float(np.percentile(base_total, 25)),
            "p50": float(np.percentile(base_total, 50)),
            "p75": float(np.percentile(base_total, 75)),
            "p95": float(np.percentile(base_total, 95)),
        },
    }

    with open(os.path.join(folder, "base_rate_output.json"), "w") as f:
        json.dump(out, f, indent=2)

    if totals:
        xs = np.arange(len(totals))
        labels = [f"{y}Q{q}" for y, q, _ in totals]
        ys = [v for _, _, v in totals]
        plt.figure(figsize=(11, 4.5))
        plt.plot(xs, ys, marker="o", color="steelblue")
        plt.xticks(xs, labels, rotation=60, ha="right")
        plt.ylabel("Capex (USD billions)")
        plt.title("Combined capex (historical, reconstructed)")
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "capex_history.png"), dpi=150)
        plt.close()

    plt.figure(figsize=(9, 5))
    plt.hist(base_total, bins=60, color="teal", alpha=0.85, density=True)
    for x in [out["base_rate_total_q4_2025_b"]["p25"], out["base_rate_total_q4_2025_b"]["p50"], out["base_rate_total_q4_2025_b"]["p75"]]:
        plt.axvline(x, color="black", linestyle="--", linewidth=1)
    plt.title("Base rate distribution: Q4 total from Q4/Q3 seasonal ratios")
    plt.xlabel("Total capex (USD billions)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "base_rate_distribution.png"), dpi=150)
    plt.close()

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
