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


def main():
    folder = os.path.dirname(__file__)
    ism_rows = load_ism_series(os.path.join(folder, "ism_pmi_history.csv"), start_year=2000)
    ism_vals = np.array([v for _, _, v in ism_rows], dtype=float)
    ism_last = float(ism_vals[-1])
    feb_vals = np.array([v for y, m, v in ism_rows if m == 2], dtype=float)
    if len(feb_vals) < 10:
        feb_vals = ism_vals

    ism_map = {(y, m): v for y, m, v in ism_rows}
    sp_nov = extract_spglobal_value_for_month(os.path.join(folder, "spglobal_us_mfg_pmi_2025_11_final.pdf"), 11)
    sp_dec = extract_spglobal_value_for_month(os.path.join(folder, "spglobal_us_mfg_pmi_2025_12_final.pdf"), 12)
    offsets = []
    if sp_nov is not None and (2025, 11) in ism_map:
        offsets.append(sp_nov - ism_map[(2025, 11)])
    if sp_dec is not None and (2025, 12) in ism_map:
        offsets.append(sp_dec - ism_map[(2025, 12)])
    offsets = np.array(offsets, dtype=float)
    off_mu = float(offsets.mean()) if len(offsets) else 4.0
    off_sd = float(offsets.std(ddof=1)) if len(offsets) > 1 else 1.0
    off_sd = max(off_sd, 0.8)

    rng = np.random.default_rng(42)
    n = 250000
    base = rng.choice(feb_vals, size=n, replace=True) + rng.normal(off_mu, off_sd, size=n)
    base = np.clip(base, 30, 70)

    band = 1.0
    future_2m = []
    for i in range(len(ism_rows) - 2):
        v0 = ism_rows[i][2]
        if abs(v0 - ism_last) <= band:
            future_2m.append(ism_rows[i + 2][2])
    future_2m = np.array(future_2m, dtype=float)
    if len(future_2m) >= 20:
        cond = rng.choice(future_2m, size=n, replace=True) + rng.normal(off_mu, off_sd, size=n)
        cond = np.clip(cond, 30, 70)
    else:
        cond = None

    out = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "proxy": {"series": "ISM Manufacturing PMI", "source": "Investing.com event 173", "window_start_year": 2000},
        "offset_points": {
            "2025-11": {"spglobal": sp_nov, "ism": ism_map.get((2025, 11))},
            "2025-12": {"spglobal": sp_dec, "ism": ism_map.get((2025, 12))},
        },
        "offset_assumption": {"mean": off_mu, "sd": off_sd, "raw": offsets.tolist()},
        "ism_feb_stats": {
            "n": int(len(feb_vals)),
            "mean": float(feb_vals.mean()),
            "sd": float(feb_vals.std()),
            "p10": float(np.percentile(feb_vals, 10)),
            "p50": float(np.percentile(feb_vals, 50)),
            "p90": float(np.percentile(feb_vals, 90)),
        },
        "spglobal_feb_base_rate": {
            "mean": float(base.mean()),
            "p5": float(np.percentile(base, 5)),
            "p25": float(np.percentile(base, 25)),
            "p50": float(np.percentile(base, 50)),
            "p75": float(np.percentile(base, 75)),
            "p95": float(np.percentile(base, 95)),
        },
        "conditional_2m_ahead_base_rate": None,
    }
    if cond is not None:
        out["conditional_2m_ahead_base_rate"] = {
            "proxy_filter": {"abs_ism_current_minus_history_leq": band, "ism_current": ism_last},
            "n_hist_points": int(len(future_2m)),
            "mean": float(cond.mean()),
            "p5": float(np.percentile(cond, 5)),
            "p25": float(np.percentile(cond, 25)),
            "p50": float(np.percentile(cond, 50)),
            "p75": float(np.percentile(cond, 75)),
            "p95": float(np.percentile(cond, 95)),
        }

    with open(os.path.join(folder, "base_rate_output.json"), "w") as f:
        json.dump(out, f, indent=2)

    plt.figure(figsize=(9, 5))
    plt.hist(base, bins=70, color="teal", alpha=0.85, density=True)
    for x in [out["spglobal_feb_base_rate"]["p25"], out["spglobal_feb_base_rate"]["p50"], out["spglobal_feb_base_rate"]["p75"]]:
        plt.axvline(x, color="black", linestyle="--", linewidth=1)
    plt.title("Base Rate (Proxy): S&P Global US Manufacturing PMI (Feb)")
    plt.xlabel("PMI")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "base_rate_distribution.png"), dpi=150)
    plt.close()

    if cond is not None:
        plt.figure(figsize=(9, 5))
        plt.hist(cond, bins=70, color="darkslateblue", alpha=0.85, density=True)
        for x in [out["conditional_2m_ahead_base_rate"]["p25"], out["conditional_2m_ahead_base_rate"]["p50"], out["conditional_2m_ahead_base_rate"]["p75"]]:
            plt.axvline(x, color="black", linestyle="--", linewidth=1)
        plt.title("Conditional Base Rate (Proxy): 2 Months Ahead")
        plt.xlabel("PMI")
        plt.ylabel("Density")
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "conditional_base_rate_distribution.png"), dpi=150)
        plt.close()

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
