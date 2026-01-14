import csv
import json
import math
import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


def load_points(path):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((int(row["year"]), int(row["quarter"]), float(row["china_share_pct"])))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def inv_logit(z):
    return 1 / (1 + np.exp(-z))


def fit_ar1(z):
    x = z[:-1]
    y = z[1:]
    X = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    a = float(beta[0])
    b = float(beta[1])
    resid = y - (a + b * x)
    sigma = float(resid.std(ddof=2)) if len(resid) > 2 else float(resid.std()) if len(resid) > 0 else 0.2
    sigma = max(sigma, 0.25)
    return a, b, sigma


def main():
    folder = os.path.dirname(__file__)
    points_path = os.path.join(folder, "china_share_points.csv")
    if not os.path.exists(points_path):
        raise SystemExit("run base_rate_calc.py first")

    rows = load_points(points_path)
    y = np.array([v for _, _, v in rows], dtype=float)
    last = float(y[-1])

    rng = np.random.default_rng(42)
    n = 300000

    z = logit(y / 100.0)
    a, b, sigma = fit_ar1(z)
    z_last = float(z[-1])
    z_next = a + b * z_last + rng.normal(0, sigma, size=n)
    comp_ar1 = 100.0 * inv_logit(z_next)

    band = 7.0
    next_vals = []
    for i in range(len(y) - 1):
        if abs(y[i] - last) <= band:
            next_vals.append(y[i + 1])
    next_vals = np.array(next_vals, dtype=float)
    if len(next_vals) >= 2:
        comp_nn = rng.choice(next_vals, size=n, replace=True) + rng.normal(0, 1.5, size=n)
    else:
        comp_nn = rng.normal(last, 5.0, size=n)

    recent = y[-4:] if len(y) >= 4 else y
    mu_recent = float(recent.mean())
    sd_recent = float(recent.std(ddof=1)) if len(recent) > 1 else 3.5
    sd_recent = max(sd_recent, 4.0)
    comp_recent = rng.normal(mu_recent, sd_recent, size=n)

    import_mu = 30.0
    import_sd = 2.5
    comp_import = rng.normal(import_mu, import_sd, size=n)

    weights = np.array([0.25, 0.15, 0.35, 0.25], dtype=float)
    weights = weights / weights.sum()
    u = rng.random(n)
    cdf = np.cumsum(weights)
    out = np.empty(n, dtype=float)
    out[u < cdf[0]] = comp_ar1[u < cdf[0]]
    m1 = (u >= cdf[0]) & (u < cdf[1])
    out[m1] = comp_nn[m1]
    m2 = (u >= cdf[1]) & (u < cdf[2])
    out[m2] = comp_recent[m2]
    out[u >= cdf[2]] = comp_import[u >= cdf[2]]

    out = np.clip(out, 0.0, 100.0)

    pct = {
        "p5": float(np.percentile(out, 5)),
        "p25": float(np.percentile(out, 25)),
        "p50": float(np.percentile(out, 50)),
        "p75": float(np.percentile(out, 75)),
        "p95": float(np.percentile(out, 95)),
    }

    out_json = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "target": "ASML net system sales share to China in Q4 2025 (%)",
        "last_observed": {"period": f"{rows[-1][0]}Q{rows[-1][1]}", "china_share_pct": last},
        "ar1_logit_fit": {"a": a, "b": b, "sigma": sigma, "n_points": int(len(y))},
        "nearest_neighbor_transitions": {"band": band, "n_hist_transitions": int(len(next_vals))},
        "import_anchor": {"mean": import_mu, "sd": import_sd},
        "ensemble_weights": {"ar1_logit": float(weights[0]), "nearest_neighbor": float(weights[1]), "recent_mean": float(weights[2]), "import_anchor": float(weights[3])},
        "forecast_percentiles": pct,
        "forecast_mean": float(out.mean()),
    }

    with open(os.path.join(folder, "forecast_output.json"), "w") as f:
        json.dump(out_json, f, indent=2)

    with open(os.path.join(folder, "forecast_percentiles.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["percentile", "value"])
        for k in ["p5", "p25", "p50", "p75", "p95"]:
            w.writerow([k, pct[k]])

    plt.figure(figsize=(9, 5))
    plt.hist(out, bins=60, color="sienna", alpha=0.85, density=True)
    for x in pct.values():
        plt.axvline(x, color="black", linestyle="--", linewidth=1)
    plt.title("Forecast distribution: ASML China share of net system sales (Q4 2025)")
    plt.xlabel("China share (%)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "forecast_distribution.png"), dpi=150)
    plt.close()

    comps = [comp_ar1, comp_nn, comp_recent, comp_import]
    labels = ["AR(1) logit", "Transitions", "Recent mean", "Import anchor"]
    means = [float(c.mean()) for c in comps]
    plt.figure(figsize=(8, 4))
    plt.bar(labels, means, color=["#4c78a8", "#f58518", "#54a24b", "#e45756"])
    plt.ylabel("Mean (%)")
    plt.title("Component means")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "component_means.png"), dpi=150)
    plt.close()

    print(json.dumps(out_json, indent=2))


if __name__ == "__main__":
    main()
