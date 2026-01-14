import csv
import json
import os
import re
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from pypdf import PdfReader

MONTH_FULL = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def load_ism_series(path, start_year=2000):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            y = int(row["ref_year"])
            if y < start_year:
                continue
            rows.append((y, int(row["ref_month"]), float(row["value"])))
    rows.sort()
    return rows


def extract_spglobal_value_for_month(pdf_path, ref_month):
    month_name = MONTH_FULL[ref_month]
    reader = PdfReader(pdf_path)
    text = "\n".join([(p.extract_text() or "") for p in reader.pages])
    m = re.search(rf"(?:registered|recorded)\s+(\d{{2}}\.\d)\s+in\s+{month_name}", text, flags=re.I)
    if m:
        return float(m.group(1))
    idx = text.lower().find(month_name.lower())
    if idx >= 0:
        window = text[max(0, idx - 200) : idx + 200]
        m2 = re.search(r"(\\d{2}\\.\\d)", window)
        if m2:
            v = float(m2.group(1))
            if 30 <= v <= 70:
                return v
    return None


def fit_ar1(values):
    x = np.asarray(values[:-1], dtype=float)
    y = np.asarray(values[1:], dtype=float)
    a = float(np.cov(x, y, bias=True)[0, 1] / np.var(x))
    b = float(y.mean() - a * x.mean())
    resid = y - (a * x + b)
    sigma = float(resid.std())
    return a, b, sigma


def simulate_ar1(a, b, sigma, last_value, steps, n, rng):
    s = np.full(n, float(last_value), dtype=float)
    for _ in range(steps):
        s = a * s + b + rng.normal(0, sigma, size=n)
    return s


def mixture_sample(components, weights, rng):
    weights = np.asarray(weights, dtype=float)
    weights = weights / weights.sum()
    n = len(components[0])
    u = rng.random(n)
    out = np.empty(n, dtype=float)
    cdf = np.cumsum(weights)
    start = 0.0
    for i, stop in enumerate(cdf):
        mask = (u >= start) & (u < stop)
        out[mask] = components[i][mask]
        start = stop
    out[u >= cdf[-1]] = components[-1][u >= cdf[-1]]
    return out


def main():
    folder = os.path.dirname(__file__)
    rng = np.random.default_rng(42)
    n = 300000

    ism_rows = load_ism_series(os.path.join(folder, "ism_pmi_history.csv"), start_year=2000)
    ism_values = np.array([v for _, _, v in ism_rows], dtype=float)
    ism_map = {(y, m): v for y, m, v in ism_rows}
    ism_last = float(ism_values[-1])

    sp_nov = extract_spglobal_value_for_month(os.path.join(folder, "spglobal_us_mfg_pmi_2025_11_final.pdf"), 11)
    sp_dec = extract_spglobal_value_for_month(os.path.join(folder, "spglobal_us_mfg_pmi_2025_12_final.pdf"), 12)
    sp_last = sp_dec if sp_dec is not None else (sp_nov if sp_nov is not None else 52.0)

    offsets = []
    if sp_nov is not None and (2025, 11) in ism_map:
        offsets.append(sp_nov - ism_map[(2025, 11)])
    if sp_dec is not None and (2025, 12) in ism_map:
        offsets.append(sp_dec - ism_map[(2025, 12)])
    offsets = np.array(offsets, dtype=float)
    off_mu = float(offsets.mean()) if len(offsets) else 4.0
    off_sd = float(offsets.std(ddof=1)) if len(offsets) > 1 else 1.0
    off_sd = max(off_sd, 0.8)

    a, b, sigma = fit_ar1(ism_values)
    ism_feb = simulate_ar1(a, b, sigma, ism_last, steps=2, n=n, rng=rng)

    feb_hist = np.array([v for y, m, v in ism_rows if m == 2], dtype=float)
    if len(feb_hist) < 10:
        feb_hist = ism_values
    feb_mu = float(feb_hist.mean())
    feb_sd = float(feb_hist.std())
    feb_sd = max(feb_sd, 1.6)

    comp_ar_offset = ism_feb + rng.normal(off_mu, off_sd, size=n)
    comp_persist = sp_last + (ism_feb - ism_last) + rng.normal(0, 1.1, size=n)
    comp_seasonal = rng.normal(feb_mu, feb_sd, size=n) + rng.normal(off_mu, off_sd, size=n)

    ensemble = mixture_sample([comp_ar_offset, comp_persist, comp_seasonal], weights=[0.55, 0.30, 0.15], rng=rng)
    ensemble = np.clip(ensemble, 30, 70)

    percentiles = {
        "p5": float(np.percentile(ensemble, 5)),
        "p25": float(np.percentile(ensemble, 25)),
        "p50": float(np.percentile(ensemble, 50)),
        "p75": float(np.percentile(ensemble, 75)),
        "p95": float(np.percentile(ensemble, 95)),
    }
    tail_probs = {
        "p_lt_49": float(np.mean(ensemble < 49.0)),
        "p_lt_50": float(np.mean(ensemble < 50.0)),
        "p_gt_56": float(np.mean(ensemble > 56.0)),
    }

    out = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "target": "S&P Global US Manufacturing PMI (Feb 2026 final)",
        "inputs": {"spglobal_known": {"2025-11": sp_nov, "2025-12": sp_dec}, "spglobal_last": sp_last, "ism_last": ism_last},
        "offset_assumption": {"mean": off_mu, "sd": off_sd, "raw": offsets.tolist()},
        "ism_ar1": {"a": a, "b": b, "sigma": sigma},
        "ensemble_weights": {"ar_offset": 0.55, "persistence": 0.30, "seasonal": 0.15},
        "forecast_percentiles": percentiles,
        "tail_probs": tail_probs,
        "forecast_mean": float(ensemble.mean()),
    }

    with open(os.path.join(folder, "forecast_output.json"), "w") as f:
        json.dump(out, f, indent=2)

    with open(os.path.join(folder, "forecast_percentiles.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["percentile", "value"])
        for k in ["p5", "p25", "p50", "p75", "p95"]:
            w.writerow([k, percentiles[k]])

    years = np.array([y + (m - 1) / 12.0 for y, m, _ in ism_rows], dtype=float)
    plt.figure(figsize=(10, 5))
    plt.plot(years, ism_values, color="steelblue", linewidth=1)
    plt.axhline(50, color="gray", linestyle="--", linewidth=1)
    plt.title("ISM Manufacturing PMI (proxy) History")
    plt.xlabel("Year")
    plt.ylabel("PMI")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "ism_history.png"), dpi=150)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.hist(ensemble, bins=75, color="slateblue", alpha=0.85, density=True)
    for x in percentiles.values():
        plt.axvline(x, color="black", linestyle="--", linewidth=1)
    plt.title("Forecast Distribution: S&P Global US Manufacturing PMI (Feb 2026)")
    plt.xlabel("PMI")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "forecast_distribution.png"), dpi=150)
    plt.close()

    labels = ["AR(1)+offset", "Persistence", "Seasonal"]
    means = [float(comp_ar_offset.mean()), float(comp_persist.mean()), float(comp_seasonal.mean())]
    plt.figure(figsize=(8, 4))
    plt.bar(labels, means, color=["#4c78a8", "#f58518", "#54a24b"])
    plt.axhline(50, color="gray", linestyle="--", linewidth=1)
    plt.title("Component Means (PMI)")
    plt.ylabel("PMI")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "component_means.png"), dpi=150)
    plt.close()

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
