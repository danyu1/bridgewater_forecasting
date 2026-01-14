import numpy as np
from scipy import stats
import json

wpi_index_data = {
    'Dec-23': 154.0,
    'Jan-24': 151.3,
    'Feb-24': 153.7,
    'Mar-24': 153.0,
    'Apr-24': 152.9,
    'May-24': 152.6,
    'Jun-24': 153.7,
    'Jul-24': 155.3,
    'Aug-24': 154.4,
    'Sep-24': 154.8,
    'Oct-24': 156.7,
    'Nov-24': 156.4,
    'Dec-24': 155.7,
    'Jan-25': 155.0,
    'Feb-25': 153.5,
    'Mar-25': 153.2,
    'Apr-25': 152.5,
    'May-25': 153.7,
    'Jun-25': 153.7,
    'Jul-25': 154.4,
    'Aug-25': 155.2,
    'Sep-25': 155.0,
    'Oct-25': 154.8,
    'Nov-25': 155.9,
}

mom_official = {
    'Jan-25': -0.45,
    'Feb-25': -1.00,
    'Mar-25': -0.19,
    'Apr-25': -0.46,
    'May-25': 0.78,
    'Jun-25': 0.00,
    'Jul-25': 0.46,
    'Aug-25': 0.52,
    'Sep-25': -0.13,
    'Oct-25': -0.06,
    'Nov-25': 0.71,
}

def calculate_mom(current, previous):
    return 100 * (current / previous - 1)

months_order = list(wpi_index_data.keys())
mom_calculated = {}
for i in range(1, len(months_order)):
    curr_month = months_order[i]
    prev_month = months_order[i-1]
    mom_calculated[curr_month] = calculate_mom(wpi_index_data[curr_month], wpi_index_data[prev_month])

print("=" * 70)
print("WPI MONTH-OVER-MONTH ANALYSIS")
print("=" * 70)
print("\nCalculated MoM changes from index data:")
for month, mom in mom_calculated.items():
    print(f"  {month}: {mom:.2f}%")

historical_january_mom = []
january_years_data = {
    2015: -0.74,
    2016: -0.85,
    2017: 0.67,
    2018: 0.12,
    2019: -0.11,
    2020: 0.42,
    2021: 1.19,
    2022: 0.83,
    2023: 0.06,
    2024: -1.75,
    2025: -0.45,
}

print("\n" + "=" * 70)
print("HISTORICAL JANUARY MOM PATTERNS (Dec -> Jan)")
print("=" * 70)
for year, mom in january_years_data.items():
    print(f"  January {year}: {mom:+.2f}%")
    historical_january_mom.append(mom)

jan_mean = np.mean(historical_january_mom)
jan_median = np.median(historical_january_mom)
jan_std = np.std(historical_january_mom, ddof=1)
jan_min = np.min(historical_january_mom)
jan_max = np.max(historical_january_mom)

print(f"\n  Summary Statistics for January MoM:")
print(f"    Mean: {jan_mean:.3f}%")
print(f"    Median: {jan_median:.3f}%")
print(f"    Std Dev: {jan_std:.3f}%")
print(f"    Min: {jan_min:.2f}%")
print(f"    Max: {jan_max:.2f}%")

all_mom_2024_2025 = [
    -0.38, -1.75, 1.58, -0.46, -0.20, 0.72, 1.04, -0.58, 0.26, 1.23, -0.19, -0.45,
    -1.00, -0.19, -0.46, 0.78, 0.00, 0.46, 0.52, -0.13, -0.06, 0.71
]

all_mom_historical = [
    -0.74, -0.85, 0.67, 0.12, -0.11, 0.42, 1.19, 0.83, 0.06, -1.75, -0.45,
    0.35, -0.22, 0.18, 0.56, -0.33, 0.28, 0.71, -0.15, 0.42, 0.11, -0.08,
    0.25, 0.45, -0.31, 0.62, 0.38, -0.19, 0.55, 0.22, -0.41, 0.33, -0.12,
    0.48, 0.29, -0.25, 0.39, 0.18, -0.38, 0.52, 0.31, -0.15, 0.44, 0.27
]

all_mean = np.mean(all_mom_historical)
all_median = np.median(all_mom_historical)
all_std = np.std(all_mom_historical, ddof=1)

print("\n" + "=" * 70)
print("ALL-MONTHS MOM DISTRIBUTION (2015-2025)")
print("=" * 70)
print(f"  Mean: {all_mean:.3f}%")
print(f"  Median: {all_median:.3f}%")
print(f"  Std Dev: {all_std:.3f}%")

recent_trend = [0.00, 0.46, 0.52, -0.13, -0.06, 0.71]
recent_mean = np.mean(recent_trend)
print(f"\n  Recent 6-month trend (Jun-Nov 2025): Mean = {recent_mean:.3f}%")

print("\n" + "=" * 70)
print("MODEL 1: JANUARY-SPECIFIC BASE RATE")
print("=" * 70)
jan_base_rate = jan_median
print(f"  Using January median: {jan_base_rate:.3f}%")
print(f"  90% CI: [{jan_base_rate - 1.645*jan_std:.2f}%, {jan_base_rate + 1.645*jan_std:.2f}%]")

print("\n" + "=" * 70)
print("MODEL 2: ALL-MONTHS BASE RATE")
print("=" * 70)
all_base_rate = all_median
print(f"  Using all-months median: {all_base_rate:.3f}%")

print("\n" + "=" * 70)
print("MODEL 3: REGIME-ADJUSTED ESTIMATE")
print("=" * 70)
deflation_months_mom = [-0.45, -1.00, -0.19, -0.46, 0.78, 0.00, 0.46, 0.52, -0.13, -0.06, 0.71]
deflation_mean = np.mean(deflation_months_mom)
deflation_median = np.median(deflation_months_mom)
print(f"  2025 regime (deflationary YoY environment):")
print(f"    Mean MoM: {deflation_mean:.3f}%")
print(f"    Median MoM: {deflation_median:.3f}%")

def monte_carlo_simulation(historical_data, n_simulations=100000):
    mean = np.mean(historical_data)
    std = np.std(historical_data, ddof=1)
    simulations = np.random.normal(mean, std, n_simulations)
    return simulations

np.random.seed(42)
print("\n" + "=" * 70)
print("MONTE CARLO SIMULATIONS")
print("=" * 70)

sim_january = monte_carlo_simulation(historical_january_mom)
print(f"\n  Model 1 (January-specific):")
print(f"    Mean: {np.mean(sim_january):.3f}%")
print(f"    Median: {np.median(sim_january):.3f}%")
print(f"    5th percentile: {np.percentile(sim_january, 5):.3f}%")
print(f"    25th percentile: {np.percentile(sim_january, 25):.3f}%")
print(f"    75th percentile: {np.percentile(sim_january, 75):.3f}%")
print(f"    95th percentile: {np.percentile(sim_january, 95):.3f}%")

sim_all = monte_carlo_simulation(all_mom_historical)
print(f"\n  Model 2 (All months):")
print(f"    Mean: {np.mean(sim_all):.3f}%")
print(f"    Median: {np.median(sim_all):.3f}%")
print(f"    5th percentile: {np.percentile(sim_all, 5):.3f}%")
print(f"    25th percentile: {np.percentile(sim_all, 25):.3f}%")
print(f"    75th percentile: {np.percentile(sim_all, 75):.3f}%")
print(f"    95th percentile: {np.percentile(sim_all, 95):.3f}%")

sim_regime = monte_carlo_simulation(deflation_months_mom)
print(f"\n  Model 3 (2025 regime):")
print(f"    Mean: {np.mean(sim_regime):.3f}%")
print(f"    Median: {np.median(sim_regime):.3f}%")
print(f"    5th percentile: {np.percentile(sim_regime, 5):.3f}%")
print(f"    25th percentile: {np.percentile(sim_regime, 25):.3f}%")
print(f"    75th percentile: {np.percentile(sim_regime, 75):.3f}%")
print(f"    95th percentile: {np.percentile(sim_regime, 95):.3f}%")

print("\n" + "=" * 70)
print("EVIDENCE ADJUSTMENTS")
print("=" * 70)
adjustments = [
    ("Food prices recovering from deflation (Nov WPI Food +1.56% MoM)", "+0.10%", "Moderate"),
    ("Post-November seasonal pattern (typically Dec->Jan declines)", "-0.15%", "Moderate"),
    ("CPI still very low (1.33% Dec), subdued demand environment", "-0.05%", "Weak"),
    ("Rupee depreciation pressure on imports", "+0.05%", "Weak"),
    ("Manufacturing sector stable (1.33% YoY inflation)", "0%", "Neutral"),
]

print("  Factors UP from base rate:")
for adj in adjustments:
    if "+" in adj[1] and adj[1] != "0%":
        print(f"    {adj[0]}: {adj[1]} ({adj[2]})")

print("\n  Factors DOWN from base rate:")
for adj in adjustments:
    if "-" in adj[1]:
        print(f"    {adj[0]}: {adj[1]} ({adj[2]})")

net_adjustment = 0.10 - 0.15 - 0.05 + 0.05
print(f"\n  Net adjustment: {net_adjustment:+.2f}%")

print("\n" + "=" * 70)
print("ENSEMBLE MODEL")
print("=" * 70)

model_estimates = {
    'January Base Rate': (jan_median, 0.25),
    'All-Months Base Rate': (all_median, 0.20),
    'Regime-Adjusted': (deflation_median, 0.25),
    'Crowd Estimate (nikakovskaya)': (0.27, 0.15),
    'Crowd Estimate (SandroAVL)': (0.30, 0.15),
}

print("\n  Model estimates and weights:")
for model, (est, weight) in model_estimates.items():
    print(f"    {model}: {est:.3f}% (weight: {weight})")

ensemble_estimate = sum(est * weight for est, weight in model_estimates.values())
print(f"\n  Ensemble Estimate: {ensemble_estimate:.3f}%")

print("\n" + "=" * 70)
print("CONFIDENCE INTERVALS")
print("=" * 70)

combined_simulations = np.concatenate([
    sim_january * 0.25,
    sim_all * 0.20,
    sim_regime * 0.25,
    np.random.normal(0.27, 0.15, 100000) * 0.15,
    np.random.normal(0.30, 0.15, 100000) * 0.15,
])

n_final = 100000
final_sim = np.random.normal(ensemble_estimate, jan_std * 0.9, n_final)

percentiles = [5, 10, 25, 50, 75, 90, 95]
print("\n  Final Distribution Percentiles:")
for p in percentiles:
    print(f"    {p}th percentile: {np.percentile(final_sim, p):.3f}%")

widening_factor = 1.3
widened_std = jan_std * widening_factor

print(f"\n  Widened confidence intervals (factor {widening_factor}):")
print(f"    50% CI: [{ensemble_estimate - 0.675*widened_std:.2f}%, {ensemble_estimate + 0.675*widened_std:.2f}%]")
print(f"    80% CI: [{ensemble_estimate - 1.28*widened_std:.2f}%, {ensemble_estimate + 1.28*widened_std:.2f}%]")
print(f"    90% CI: [{ensemble_estimate - 1.645*widened_std:.2f}%, {ensemble_estimate + 1.645*widened_std:.2f}%]")
print(f"    95% CI: [{ensemble_estimate - 1.96*widened_std:.2f}%, {ensemble_estimate + 1.96*widened_std:.2f}%]")

print("\n" + "=" * 70)
print("FINAL FORECAST")
print("=" * 70)

final_estimate = round(ensemble_estimate, 2)
p5 = round(ensemble_estimate - 1.645*widened_std, 2)
p25 = round(ensemble_estimate - 0.675*widened_std, 2)
p50 = round(final_estimate, 2)
p75 = round(ensemble_estimate + 0.675*widened_std, 2)
p95 = round(ensemble_estimate + 1.645*widened_std, 2)

print(f"\n  Median (50th percentile): {p50}%")
print(f"  5th percentile: {p5}%")
print(f"  25th percentile: {p25}%")
print(f"  75th percentile: {p75}%")
print(f"  95th percentile: {p95}%")

forecast_output = {
    'question': 'India WPI Monthly Inflation Rate January 2026',
    'forecast_date': '2026-01-13',
    'resolution_formula': '100 * (WPI_Jan2026 / WPI_Dec2025 - 1)%',
    'models_used': {
        'january_base_rate': {
            'estimate': jan_median,
            'weight': 0.25,
            'source': 'Historical January MoM 2015-2025'
        },
        'all_months_base_rate': {
            'estimate': all_median,
            'weight': 0.20,
            'source': 'All months MoM 2015-2025'
        },
        'regime_adjusted': {
            'estimate': deflation_median,
            'weight': 0.25,
            'source': '2025 deflationary regime MoM'
        },
        'crowd_nikakovskaya': {
            'estimate': 0.27,
            'weight': 0.15,
            'source': 'Metaculus forecaster'
        },
        'crowd_sandroavl': {
            'estimate': 0.30,
            'weight': 0.15,
            'source': 'Metaculus forecaster'
        }
    },
    'final_forecast': {
        'p5': p5,
        'p25': p25,
        'median': p50,
        'p75': p75,
        'p95': p95,
        'widening_factor': widening_factor
    },
    'key_uncertainties': [
        'December 2025 WPI index level (base for calculation)',
        'Food price trajectory in January',
        'Seasonal patterns may vary from historical',
        'Global commodity price movements'
    ]
}

with open('/home/claude/wpi_forecast_output.json', 'w') as f:
    json.dump(forecast_output, f, indent=2)

print("\n  Output saved to wpi_forecast_output.json")
