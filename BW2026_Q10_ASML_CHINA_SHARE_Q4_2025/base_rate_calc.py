import csv
import json
import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


def quarter_to_idx(year, quarter):
    return year * 4 + (quarter - 1)


def idx_to_label(idx):
    year = idx // 4
    q = (idx % 4) + 1
    return f"{year}Q{q}"


def load_manual_points():
    return [
        {"year": 2023, "quarter": 4, "china_share_pct": 39, "source": "metaculus_background"},
        {"year": 2024, "quarter": 1, "china_share_pct": 49, "source": "metaculus_background"},
        {"year": 2024, "quarter": 2, "china_share_pct": 49, "source": "metaculus_background"},
        {"year": 2024, "quarter": 3, "china_share_pct": 47, "source": "metaculus_background"},
        {"year": 2024, "quarter": 4, "china_share_pct": 27, "source": "metaculus_background"},
        {"year": 2025, "quarter": 1, "china_share_pct": 27, "source": "metaculus_background"},
        {"year": 2025, "quarter": 2, "china_share_pct": 27, "source": "metaculus_background"},
        {"year": 2025, "quarter": 3, "china_share_pct": 42, "source": "asml_investor_presentation_q3_2025"},
    ]


def load_scraped_points(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            y = int(row["year"])
            q = int(row["quarter"])
            if (y, q) < (2023, 4):
                continue
            out.append({"year": y, "quarter": q, "china_share_pct": int(row["china_share_pct"]), "source": "asml_ir_scrape"})
    return out


def merge_points(points):
    merged = {}
    for p in points:
        merged[(p["year"], p["quarter"])] = p
    out = list(merged.values())
    out.sort(key=lambda x: (x["year"], x["quarter"]))
    return out


def main():
    folder = os.path.dirname(__file__)
    scraped = load_scraped_points(os.path.join(folder, "asml_china_share_history.csv"))
    points = merge_points(load_manual_points() + scraped)

    out_csv = os.path.join(folder, "china_share_points.csv")
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "quarter", "china_share_pct", "source"])
        w.writeheader()
        w.writerows(points)

    idx = np.array([quarter_to_idx(p["year"], p["quarter"]) for p in points], dtype=int)
    y = np.array([p["china_share_pct"] for p in points], dtype=float)

    diffs = np.diff(y)
    recent = y[-4:] if len(y) >= 4 else y
    last = float(y[-1])

    q = {
        "p5": float(np.percentile(y, 5)),
        "p25": float(np.percentile(y, 25)),
        "p50": float(np.percentile(y, 50)),
        "p75": float(np.percentile(y, 75)),
        "p95": float(np.percentile(y, 95)),
    }

    mu = float(y.mean())
    sd = float(y.std(ddof=1)) if len(y) > 1 else 0.0
    mu_recent = float(recent.mean())
    sd_recent = float(recent.std(ddof=1)) if len(recent) > 1 else 0.0

    band = 5.0
    next_vals = []
    for i in range(len(y) - 1):
        if abs(y[i] - last) <= band:
            next_vals.append(y[i + 1])
    next_vals = np.array(next_vals, dtype=float)
    cond = None
    if len(next_vals) >= 2:
        cond = {
            "abs_prev_minus_last_leq": band,
            "n": int(len(next_vals)),
            "mean": float(next_vals.mean()),
            "p25": float(np.percentile(next_vals, 25)),
            "p50": float(np.percentile(next_vals, 50)),
            "p75": float(np.percentile(next_vals, 75)),
        }

    out = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "series": {"definition": "ASML net system sales to China (% of total net system sales, ship-to location)", "points": len(points)},
        "history_points": [{"period": idx_to_label(quarter_to_idx(p["year"], p["quarter"])), "china_share_pct": int(p["china_share_pct"]), "source": p["source"]} for p in points],
        "unconditional_stats": {"mean": mu, "sd": sd, "quantiles": q},
        "recent_4q_stats": {"mean": mu_recent, "sd": sd_recent},
        "diff_stats": {"mean": float(diffs.mean()) if len(diffs) else 0.0, "sd": float(diffs.std(ddof=1)) if len(diffs) > 1 else 0.0, "min": float(diffs.min()) if len(diffs) else 0.0, "max": float(diffs.max()) if len(diffs) else 0.0},
        "conditional_next_quarter_given_last_band": cond,
        "last_observation": {"period": idx_to_label(int(idx[-1])), "china_share_pct": int(y[-1])},
    }

    with open(os.path.join(folder, "base_rate_output.json"), "w") as f:
        json.dump(out, f, indent=2)

    x = np.arange(len(y))
    labels = [idx_to_label(int(i)) for i in idx]
    plt.figure(figsize=(10, 4.5))
    plt.plot(x, y, marker="o", color="steelblue")
    plt.ylim(0, 60)
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.ylabel("China share of net system sales (%)")
    plt.title("ASML: Net system sales share to China (ship-to location)")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "china_share_history.png"), dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plt.hist(y, bins=max(6, len(y)), color="teal", alpha=0.85)
    plt.axvline(mu, color="black", linestyle="--", linewidth=1)
    plt.title("Historical distribution (limited sample)")
    plt.xlabel("China share (%)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "base_rate_distribution.png"), dpi=150)
    plt.close()

    if len(y) >= 2:
        plt.figure(figsize=(6, 5))
        plt.scatter(y[:-1], y[1:], color="slateblue", alpha=0.9)
        plt.xlabel("Previous quarter China share (%)")
        plt.ylabel("Next quarter China share (%)")
        plt.title("Quarter-to-quarter transitions (limited sample)")
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "transition_scatter.png"), dpi=150)
        plt.close()

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
