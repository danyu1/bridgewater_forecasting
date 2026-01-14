import csv
import json
import math
import os
from datetime import datetime, date

import numpy as np
import matplotlib.pyplot as plt


def read_stooq_close(path):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            d = row.get("Date")
            c = row.get("Close")
            if d is None or c is None:
                continue
            c = c.strip()
            if c == "" or c == "0":
                continue
            rows.append((d, float(c)))
    rows.sort()
    return rows


def busdays_between(d0, d1):
    a = np.datetime64(d0)
    b = np.datetime64(d1)
    return int(np.busday_count(a, b))


def pct(x):
    return {
        "p5": float(np.percentile(x, 5)),
        "p25": float(np.percentile(x, 25)),
        "p50": float(np.percentile(x, 50)),
        "p75": float(np.percentile(x, 75)),
        "p95": float(np.percentile(x, 95)),
    }


def main():
    folder = os.path.dirname(__file__)
    base = json.load(open(os.path.join(folder, "base_rate_output.json")))

    spx = read_stooq_close(os.path.join(folder, "sp500_stooq.csv"))
    s0 = float(spx[-1][1])
    today = date.fromisoformat(spx[-1][0])
    target = date(2026, 3, 13)
    days = max(1, busdays_between(today.isoformat(), target.isoformat()))

    prices = np.array([v for _, v in spx], dtype=float)
    rets = np.diff(np.log(prices))
    rets = rets[-1260:] if len(rets) > 1260 else rets
    mu_d = float(np.mean(rets))
    sd_d = float(np.std(rets, ddof=1)) if len(rets) > 1 else 0.01
    sd_d = max(sd_d, 0.003)

    m = base["parent"]["recent_monthly_change_mu"]
    s = base["parent"]["recent_monthly_change_sd"]

    cond = base["spx_conditional_7bd_log_return"]
    mu_all = cond["mu_all"]
    sd_all = cond["sd_all"]
    mu_yes = cond["mu_yes"]
    sd_yes = cond["sd_yes"]
    mu_no = cond["mu_no"]
    sd_no = cond["sd_no"]

    rng = np.random.default_rng(42)
    n = 500000

    d_pay = rng.normal(m, s, size=(n, 2)).sum(axis=1)
    is_yes = d_pay < 100.0

    base_lr = rng.normal(mu_d * days, sd_d * math.sqrt(days), size=n)

    r_all = rng.normal(mu_all, sd_all, size=n)
    r_group = np.empty(n, dtype=float)
    r_group[is_yes] = rng.normal(mu_yes, sd_yes, size=int(np.sum(is_yes)))
    r_group[~is_yes] = rng.normal(mu_no, sd_no, size=int(np.sum(~is_yes)))
    delta = r_group - r_all

    lr = base_lr + delta
    st = s0 * np.exp(lr)

    st_yes = st[is_yes]
    st_no = st[~is_yes]

    out = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "spx_last": {"date": spx[-1][0], "value": s0},
        "target_date": target.isoformat(),
        "horizon_busdays": days,
        "daily_log_return": {"mu": mu_d, "sd": sd_d, "n": int(len(rets))},
        "payroll_sim": {"mu_monthly": m, "sd_monthly": s},
        "conditional_shock": {"type": "7_trading_day_return", "mu_all": mu_all, "sd_all": sd_all, "mu_yes": mu_yes, "sd_yes": sd_yes, "mu_no": mu_no, "sd_no": sd_no},
        "parent_prob_yes_sim": float(np.mean(is_yes)),
        "child_percentiles_yes": pct(st_yes),
        "child_percentiles_no": pct(st_no),
    }

    with open(os.path.join(folder, "forecast_output.json"), "w") as f:
        json.dump(out, f, indent=2)

    out_cond = {
        "parent_prob_yes": out["parent_prob_yes_sim"],
        "sp500_on_2026_03_13_given_yes": out["child_percentiles_yes"],
        "sp500_on_2026_03_13_given_no": out["child_percentiles_no"],
    }
    with open(os.path.join(folder, "conditional_forecasts.json"), "w") as f:
        json.dump(out_cond, f, indent=2)

    with open(os.path.join(folder, "forecast_percentiles.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["branch", "p5", "p25", "p50", "p75", "p95"])
        y = out["child_percentiles_yes"]
        n0 = out["child_percentiles_no"]
        w.writerow(["YES"] + [y[k] for k in ["p5", "p25", "p50", "p75", "p95"]])
        w.writerow(["NO"] + [n0[k] for k in ["p5", "p25", "p50", "p75", "p95"]])

    plt.figure(figsize=(10, 5))
    plt.hist(st_no, bins=90, alpha=0.45, density=True, label="NO (>=100k jobs)", color="#54a24b")
    plt.hist(st_yes, bins=90, alpha=0.45, density=True, label="YES (<100k jobs)", color="#e45756")
    plt.title("S&P 500 close on 2026-03-13 (conditional on payrolls)")
    plt.xlabel("S&P 500")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "sp500_forecast_conditional.png"), dpi=150)
    plt.close()

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
