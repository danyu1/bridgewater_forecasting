import csv
import json
import math
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
    needed = [(ticker, year, 1), (ticker, year, 2), (ticker, year, 3)]
    if any(k not in qmap for k in needed):
        return None
    return annual_map[(ticker, year)] - qmap[needed[0]] - qmap[needed[1]] - qmap[needed[2]]


def to_b(val_usd):
    return val_usd / 1e9


def fit_lognormal_from_p25_p50_p75(p25, p50, p75):
    z = 0.6744897501960817
    sigma = (math.log(p75) - math.log(p25)) / (2 * z)
    mu = math.log(p50)
    return mu, sigma


def main():
    folder = os.path.dirname(__file__)
    rows = load_series(os.path.join(folder, "capex_history_quarterly.csv"))
    qmap, annual_map = build_maps(rows)

    def get_payments(t, y, q):
        if (t, y, q) in qmap:
            return qmap[(t, y, q)]
        if t in ["GOOG", "AMZN"] and q == 4:
            v = derive_q4_from_annual(qmap, annual_map, t, y)
            if v is not None:
                return v
        return None

    def amazon_inflow_known_b(y, q):
        known = {
            (2024, 4): 1.782,
            (2025, 1): 0.764,
            (2025, 2): 0.815,
            (2025, 3): 0.867,
        }
        return known.get((y, q), None)

    tickers = ["MSFT", "GOOG", "AMZN"]
    years = sorted(set(y for (_, y, q, _) in rows if q != 0))

    ratio_total = []
    ratio_company = {t: [] for t in tickers}
    for y in years:
        q3 = {t: get_payments(t, y, 3) for t in tickers}
        q4 = {t: get_payments(t, y, 4) for t in tickers}
        if all(q3[t] is not None and q4[t] is not None and q3[t] > 0 for t in tickers):
            inflow_q3 = amazon_inflow_known_b(y, 3) if amazon_inflow_known_b(y, 3) is not None else 1.0
            inflow_q4 = amazon_inflow_known_b(y, 4) if amazon_inflow_known_b(y, 4) is not None else 1.0
            total_q3 = to_b(q3["MSFT"]) + to_b(q3["GOOG"]) + to_b(q3["AMZN"]) - inflow_q3
            total_q4 = to_b(q4["MSFT"]) + to_b(q4["GOOG"]) + to_b(q4["AMZN"]) - inflow_q4
            if total_q3 > 0:
                ratio_total.append(float(total_q4 / total_q3))
            for t in tickers:
                ratio_company[t].append(float(to_b(q4[t]) / to_b(q3[t])))

    ratio_total = np.array(ratio_total, dtype=float)
    for t in tickers:
        ratio_company[t] = np.array(ratio_company[t], dtype=float)

    q3_current = {"MSFT": 19.394, "GOOG": 23.953, "AMZN_gross": 35.095, "AMZN_inflow": 0.867}
    q3_total = q3_current["MSFT"] + q3_current["GOOG"] + q3_current["AMZN_gross"] - q3_current["AMZN_inflow"]

    inflow_hist = [v for v in [amazon_inflow_known_b(2024, 4), amazon_inflow_known_b(2025, 1), amazon_inflow_known_b(2025, 2), amazon_inflow_known_b(2025, 3)] if v is not None]
    inflow_hist = np.array(inflow_hist, dtype=float)
    inflow_mu = float(np.mean(inflow_hist))
    inflow_sd = float(np.std(inflow_hist, ddof=1)) if len(inflow_hist) > 1 else 0.3
    inflow_sd = max(inflow_sd, 0.25)

    rng = np.random.default_rng(42)
    n = 300000

    if len(ratio_total) == 0:
        ratio_total = np.array([1.12], dtype=float)
    ratio_total_s = rng.choice(ratio_total, size=n, replace=True)
    ratio_total_s = ratio_total_s * np.clip(rng.normal(1.03, 0.02, size=n), 0.95, 1.12)
    comp_total = q3_total * ratio_total_s

    ratios_ms = ratio_company["MSFT"] if len(ratio_company["MSFT"]) else np.array([1.05])
    ratios_gg = ratio_company["GOOG"] if len(ratio_company["GOOG"]) else np.array([1.10])
    ratios_az = ratio_company["AMZN"] if len(ratio_company["AMZN"]) else np.array([1.15])

    ms_q4 = q3_current["MSFT"] * rng.choice(ratios_ms, size=n, replace=True) * np.clip(rng.normal(1.02, 0.02, size=n), 0.95, 1.10)
    gg_q4 = q3_current["GOOG"] * rng.choice(ratios_gg, size=n, replace=True) * np.clip(rng.normal(1.05, 0.03, size=n), 0.90, 1.18)
    az_gross_q4 = q3_current["AMZN_gross"] * rng.choice(ratios_az, size=n, replace=True) * np.clip(rng.normal(1.03, 0.025, size=n), 0.92, 1.14)
    inflow_q4 = np.clip(rng.normal(inflow_mu, inflow_sd, size=n), 0.0, None)
    comp_company = ms_q4 + gg_q4 + az_gross_q4 - inflow_q4

    mu_c, sigma_c = fit_lognormal_from_p25_p50_p75(84.76, 89.45, 95.07)
    comp_crowd = np.exp(rng.normal(mu_c, sigma_c, size=n))

    accel = rng.random(n) < 0.20
    comp_accel = np.clip(comp_company + accel * rng.normal(7.0, 3.0, size=n), 0.0, None)

    weights = np.array([0.15, 0.25, 0.50, 0.10], dtype=float)
    weights = weights / weights.sum()
    u = rng.random(n)
    cdf = np.cumsum(weights)
    out = np.empty(n, dtype=float)
    out[u < cdf[0]] = comp_total[u < cdf[0]]
    m1 = (u >= cdf[0]) & (u < cdf[1])
    out[m1] = comp_company[m1]
    m2 = (u >= cdf[1]) & (u < cdf[2])
    out[m2] = comp_crowd[m2]
    out[u >= cdf[2]] = comp_accel[u >= cdf[2]]

    out = np.clip(out, 0.0, None)

    pct = {
        "p5": float(np.percentile(out, 5)),
        "p25": float(np.percentile(out, 25)),
        "p50": float(np.percentile(out, 50)),
        "p75": float(np.percentile(out, 75)),
        "p95": float(np.percentile(out, 95)),
    }

    out_json = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "target": "Combined capex for MSFT+GOOG+AMZN in quarter ending 2025-12-31 (USD billions)",
        "current_inputs": q3_current,
        "historical_ratio_counts": {"total_q4_over_q3": int(len(ratio_total)), "msft": int(len(ratio_company["MSFT"])), "goog": int(len(ratio_company["GOOG"])), "amzn": int(len(ratio_company["AMZN"]))},
        "amazon_inflow_assumption": {"mean_b": inflow_mu, "sd_b": inflow_sd, "known_points_b": inflow_hist.tolist()},
        "crowd_anchor": {"p25": 84.76, "p50": 89.45, "p75": 95.07, "lognormal_mu": mu_c, "lognormal_sigma": sigma_c},
        "ensemble_weights": {"total_ratio": float(weights[0]), "company_ratio_sum": float(weights[1]), "crowd_lognormal": float(weights[2]), "acceleration_tail": float(weights[3])},
        "forecast_percentiles_b": pct,
        "forecast_mean_b": float(out.mean()),
        "components_mean_b": {"total_ratio": float(comp_total.mean()), "company_ratio_sum": float(comp_company.mean()), "crowd": float(comp_crowd.mean()), "accel_tail": float(comp_accel.mean())},
    }

    with open(os.path.join(folder, "forecast_output.json"), "w") as f:
        json.dump(out_json, f, indent=2)

    with open(os.path.join(folder, "forecast_percentiles.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["percentile", "value_b"])
        for k in ["p5", "p25", "p50", "p75", "p95"]:
            w.writerow([k, pct[k]])

    plt.figure(figsize=(9, 5))
    plt.hist(out, bins=70, color="sienna", alpha=0.85, density=True)
    for x in pct.values():
        plt.axvline(x, color="black", linestyle="--", linewidth=1)
    plt.title("Forecast distribution: combined hyperscaler capex (Q4 2025)")
    plt.xlabel("Capex (USD billions)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "forecast_distribution.png"), dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4))
    comp_labels = ["Total ratio", "Company sum", "Crowd", "Accel tail"]
    comp_means = [out_json["components_mean_b"]["total_ratio"], out_json["components_mean_b"]["company_ratio_sum"], out_json["components_mean_b"]["crowd"], out_json["components_mean_b"]["accel_tail"]]
    plt.bar(comp_labels, comp_means, color=["#4c78a8", "#f58518", "#54a24b", "#e45756"])
    plt.ylabel("Mean (USD billions)")
    plt.title("Component means")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "company_forecast_bars.png"), dpi=150)
    plt.close()

    print(json.dumps(out_json, indent=2))


if __name__ == "__main__":
    main()
