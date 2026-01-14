import csv
import json
import os
from bisect import bisect_left
from datetime import datetime, date, timedelta

import numpy as np
import matplotlib.pyplot as plt


def read_fred_csv(path):
    with open(path) as f:
        r = csv.DictReader(f)
        fns = r.fieldnames or []
        date_key = "DATE" if "DATE" in fns else ("observation_date" if "observation_date" in fns else fns[0])
        val_key = [k for k in fns if k != date_key][0]
        rows = []
        for row in r:
            d = row.get(date_key)
            v = row.get(val_key)
            if d is None or v is None:
                continue
            v = v.strip()
            if v == "" or v == ".":
                continue
            rows.append((d, float(v)))
    return rows


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


def month_key(date_str):
    y, m, _ = date_str.split("-")
    return int(y) * 12 + int(m)


def ym_from_key(k):
    y = k // 12
    m = k % 12
    if m == 0:
        y -= 1
        m = 12
    return y, m


def monthly_series_from_daily(daily_rows):
    out = {}
    for d, v in daily_rows:
        y, m, _ = d.split("-")
        out[(int(y), int(m))] = v
    ks = sorted(out.keys())
    return [(f"{y:04d}-{m:02d}", out[(y, m)]) for (y, m) in ks]


def compute_payroll_2m_changes(payems_rows):
    ks = [month_key(d) for d, _ in payems_rows]
    vals = np.array([v for _, v in payems_rows], dtype=float)
    out = []
    for i in range(2, len(vals)):
        out.append((ks[i], float(vals[i] - vals[i - 2])))
    return out


def first_friday(y, m):
    d = date(y, m, 1)
    while d.weekday() != 4:
        d += timedelta(days=1)
    return d


def log_return_on_k_trading_days(dates, closes, start_date, k):
    i = bisect_left(dates, start_date)
    if i >= len(dates):
        return None
    j = i + k
    if j >= len(dates):
        return None
    return float(np.log(closes[j] / closes[i]))


def main():
    folder = os.path.dirname(__file__)
    payems = read_fred_csv(os.path.join(folder, "payems_fred.csv"))
    spx_daily = read_stooq_close(os.path.join(folder, "sp500_stooq.csv"))

    payroll_2m = compute_payroll_2m_changes(payems)
    payroll_vals = np.array([c for _, c in payroll_2m], dtype=float)

    p0 = float(np.mean(payroll_vals < 100.0))
    last_10y = payroll_vals[-120:] if len(payroll_vals) >= 120 else payroll_vals
    p1 = float(np.mean(last_10y < 100.0))

    monthly_changes = np.diff(np.array([v for _, v in payems], dtype=float))
    recent = monthly_changes[-36:] if len(monthly_changes) >= 36 else monthly_changes
    mu = float(np.mean(recent))
    sd = float(np.std(recent, ddof=1)) if len(recent) > 1 else 40.0
    sd = max(sd, 20.0)
    rng = np.random.default_rng(42)
    n = 250000
    d = rng.normal(mu, sd, size=(n, 2)).sum(axis=1)
    p2 = float(np.mean(d < 100.0))

    parent_p = 0.30 * p0 + 0.30 * p1 + 0.40 * p2

    spx_monthly = monthly_series_from_daily(spx_daily)
    sp_m = np.array([v for _, v in spx_monthly], dtype=float)
    sp_r_1m = np.diff(np.log(sp_m))

    pay_map = {k: v for k, v in payroll_2m}
    months = [month_key(d + "-01") for d, _ in spx_monthly]
    ind_1m = []
    aligned_1m = []
    for i in range(len(months) - 1):
        k_m = months[i]
        if k_m not in pay_map:
            continue
        ind_1m.append(pay_map[k_m] < 100.0)
        aligned_1m.append(float(sp_r_1m[i]))

    ind_1m = np.array(ind_1m, dtype=bool)
    aligned_1m = np.array(aligned_1m, dtype=float)
    mu_all_1m = float(np.mean(aligned_1m))
    sd_all_1m = float(np.std(aligned_1m, ddof=1)) if len(aligned_1m) > 1 else 0.05
    mu_yes_1m = float(np.mean(aligned_1m[ind_1m])) if np.any(ind_1m) else mu_all_1m
    sd_yes_1m = float(np.std(aligned_1m[ind_1m], ddof=1)) if np.sum(ind_1m) > 2 else sd_all_1m
    mu_no_1m = float(np.mean(aligned_1m[~ind_1m])) if np.any(~ind_1m) else mu_all_1m
    sd_no_1m = float(np.std(aligned_1m[~ind_1m], ddof=1)) if np.sum(~ind_1m) > 2 else sd_all_1m

    dates = [date.fromisoformat(d) for d, _ in spx_daily]
    closes = np.array([v for _, v in spx_daily], dtype=float)

    ind_7d = []
    aligned_7d = []
    for k_m, chg in payroll_2m:
        y, mth = ym_from_key(k_m)
        yy = y
        mm = mth + 1
        if mm == 13:
            yy += 1
            mm = 1
        start = first_friday(yy, mm)
        r7 = log_return_on_k_trading_days(dates, closes, start, 7)
        if r7 is None:
            continue
        ind_7d.append(chg < 100.0)
        aligned_7d.append(r7)

    ind_7d = np.array(ind_7d, dtype=bool)
    aligned_7d = np.array(aligned_7d, dtype=float)
    mu_all_7d = float(np.mean(aligned_7d))
    sd_all_7d = float(np.std(aligned_7d, ddof=1)) if len(aligned_7d) > 1 else 0.02
    mu_yes_7d = float(np.mean(aligned_7d[ind_7d])) if np.any(ind_7d) else mu_all_7d
    sd_yes_7d = float(np.std(aligned_7d[ind_7d], ddof=1)) if np.sum(ind_7d) > 2 else sd_all_7d
    mu_no_7d = float(np.mean(aligned_7d[~ind_7d])) if np.any(~ind_7d) else mu_all_7d
    sd_no_7d = float(np.std(aligned_7d[~ind_7d], ddof=1)) if np.sum(~ind_7d) > 2 else sd_all_7d

    out = {
        "as_of_utc": datetime.utcnow().isoformat(),
        "parent": {
            "p_lt_100k_base_long": p0,
            "p_lt_100k_last_10y": p1,
            "p_lt_100k_sim_recent": p2,
            "p_lt_100k_weighted": parent_p,
            "recent_monthly_change_mu": mu,
            "recent_monthly_change_sd": sd,
        },
        "spx_conditional_1m_log_return": {
            "mu_all": mu_all_1m,
            "sd_all": sd_all_1m,
            "mu_yes": mu_yes_1m,
            "sd_yes": sd_yes_1m,
            "mu_no": mu_no_1m,
            "sd_no": sd_no_1m,
            "n_aligned": int(len(aligned_1m)),
            "n_yes": int(np.sum(ind_1m)),
            "n_no": int(np.sum(~ind_1m)),
        },
        "spx_conditional_7bd_log_return": {
            "mu_all": mu_all_7d,
            "sd_all": sd_all_7d,
            "mu_yes": mu_yes_7d,
            "sd_yes": sd_yes_7d,
            "mu_no": mu_no_7d,
            "sd_no": sd_no_7d,
            "n_aligned": int(len(aligned_7d)),
            "n_yes": int(np.sum(ind_7d)),
            "n_no": int(np.sum(~ind_7d)),
            "definition": "log return from approx payroll release date (first Friday next month) to 7 trading days later",
        },
    }

    with open(os.path.join(folder, "base_rate_output.json"), "w") as f:
        json.dump(out, f, indent=2)

    plt.figure(figsize=(9, 5))
    plt.hist(payroll_vals, bins=90, color="steelblue", alpha=0.85)
    plt.axvline(100.0, color="red", linewidth=2)
    plt.title("PAYEMS 2-month change distribution (thousands)")
    plt.xlabel("2-month change (k jobs)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "payroll_change_dist.png"), dpi=150)
    plt.close()

    xs = ["All", "YES (<100k)", "NO (>=100k)"]
    means = [mu_all_7d, mu_yes_7d, mu_no_7d]
    plt.figure(figsize=(8, 4))
    plt.bar(xs, means, color=["#4c78a8", "#e45756", "#54a24b"])
    plt.title("S&P 500 7-trading-day log return: conditional means")
    plt.ylabel("Mean log return")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "sp500_return_conditional.png"), dpi=150)
    plt.close()

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
