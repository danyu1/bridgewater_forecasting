import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

superbowl_data = [
    (1967, 'I', 22.6),
    (1968, 'II', 36.8),
    (1969, 'III', 36.0),
    (1970, 'IV', 39.4),
    (1971, 'V', 39.9),
    (1972, 'VI', 44.2),
    (1973, 'VII', 42.7),
    (1974, 'VIII', 41.6),
    (1975, 'IX', 42.4),
    (1976, 'X', 42.3),
    (1977, 'XI', 44.4),
    (1978, 'XII', 47.2),
    (1979, 'XIII', 47.1),
    (1980, 'XIV', 46.3),
    (1981, 'XV', 44.4),
    (1982, 'XVI', 49.1),
    (1983, 'XVII', 48.6),
    (1984, 'XVIII', 46.4),
    (1985, 'XIX', 46.4),
    (1986, 'XX', 48.3),
    (1987, 'XXI', 45.8),
    (1988, 'XXII', 41.9),
    (1989, 'XXIII', 43.5),
    (1990, 'XXIV', 39.0),
    (1991, 'XXV', 41.9),
    (1992, 'XXVI', 40.3),
    (1993, 'XXVII', 45.1),
    (1994, 'XXVIII', 45.5),
    (1995, 'XXIX', 41.3),
    (1996, 'XXX', 46.0),
    (1997, 'XXXI', 43.3),
    (1998, 'XXXII', 44.5),
    (1999, 'XXXIII', 40.2),
    (2000, 'XXXIV', 43.3),
    (2001, 'XXXV', 40.4),
    (2002, 'XXXVI', 40.4),
    (2003, 'XXXVII', 40.7),
    (2004, 'XXXVIII', 41.4),
    (2005, 'XXXIX', 41.1),
    (2006, 'XL', 41.6),
    (2007, 'XLI', 42.6),
    (2008, 'XLII', 43.1),
    (2009, 'XLIII', 42.0),
    (2010, 'XLIV', 45.0),
    (2011, 'XLV', 46.0),
    (2012, 'XLVI', 47.1),
    (2013, 'XLVII', 46.4),
    (2014, 'XLVIII', 46.7),
    (2015, 'XLIX', 47.5),
    (2016, '50', 46.6),
    (2017, 'LI', 45.3),
    (2018, 'LII', 43.1),
    (2019, 'LIII', 41.4),
    (2020, 'LIV', 42.0),
    (2021, 'LV', 38.4),
    (2022, 'LVI', 37.9),
    (2023, 'LVII', 40.7),
    (2024, 'LVIII', 43.5),
    (2025, 'LIX', 41.7),
]

years = np.array([d[0] for d in superbowl_data])
ratings = np.array([d[2] for d in superbowl_data])

print("="*70)
print("SUPER BOWL LX HOUSEHOLD RATING FORECAST ANALYSIS")
print("="*70)

print("\n" + "="*70)
print("STEP 1: INTAKE & QUESTION ANALYSIS")
print("="*70)
print("""
Question: What percentage of US households will watch Super Bowl LX?
Type: CONTINUOUS (requires percentile distribution)
Close Date: February 8, 2026
Resolution: Nielsen Media Research HHLD Rating
Resolution Deadline: March 14, 2026

Key Metric: Household Rating (% of TV-owning households watching)
NOT: Total viewers (which grows with population)
NOT: Household share (% of TVs in use watching)
""")

print("\n" + "="*70)
print("STEP 2: BASE RATE ANALYSIS")
print("="*70)

all_mean = np.mean(ratings)
all_std = np.std(ratings)
all_median = np.median(ratings)
print(f"\nAll-Time Statistics (1967-2025, n={len(ratings)}):")
print(f"  Mean: {all_mean:.2f}%")
print(f"  Median: {all_median:.2f}%")
print(f"  Std Dev: {all_std:.2f}%")
print(f"  Range: {np.min(ratings):.1f}% - {np.max(ratings):.1f}%")

recent_10 = ratings[-10:]
recent_10_years = years[-10:]
print(f"\nLast 10 Years Statistics (2016-2025, n=10):")
print(f"  Mean: {np.mean(recent_10):.2f}%")
print(f"  Median: {np.median(recent_10):.2f}%")
print(f"  Std Dev: {np.std(recent_10):.2f}%")
print(f"  Range: {np.min(recent_10):.1f}% - {np.max(recent_10):.1f}%")

recent_5 = ratings[-5:]
print(f"\nLast 5 Years Statistics (2021-2025, n=5):")
print(f"  Mean: {np.mean(recent_5):.2f}%")
print(f"  Median: {np.median(recent_5):.2f}%")
print(f"  Std Dev: {np.std(recent_5):.2f}%")
print(f"  Range: {np.min(recent_5):.1f}% - {np.max(recent_5):.1f}%")

modern_era = ratings[years >= 2000]
modern_years = years[years >= 2000]
print(f"\nModern Era Statistics (2000-2025, n={len(modern_era)}):")
print(f"  Mean: {np.mean(modern_era):.2f}%")
print(f"  Median: {np.median(modern_era):.2f}%")
print(f"  Std Dev: {np.std(modern_era):.2f}%")

print("\n" + "="*70)
print("STEP 3: TIME SERIES ANALYSIS")
print("="*70)

slope_all, intercept_all, r_all, p_all, se_all = stats.linregress(years, ratings)
print(f"\nLinear Trend (All-Time):")
print(f"  Slope: {slope_all:.4f}% per year")
print(f"  R-squared: {r_all**2:.4f}")
print(f"  P-value: {p_all:.4f}")
print(f"  2026 Prediction: {intercept_all + slope_all * 2026:.2f}%")

slope_mod, intercept_mod, r_mod, p_mod, se_mod = stats.linregress(modern_years, modern_era)
print(f"\nLinear Trend (2000-2025):")
print(f"  Slope: {slope_mod:.4f}% per year")
print(f"  R-squared: {r_mod**2:.4f}")
print(f"  2026 Prediction: {intercept_mod + slope_mod * 2026:.2f}%")

slope_10, intercept_10, r_10, p_10, se_10 = stats.linregress(recent_10_years, recent_10)
print(f"\nLinear Trend (Last 10 Years):")
print(f"  Slope: {slope_10:.4f}% per year")
print(f"  R-squared: {r_10**2:.4f}")
print(f"  2026 Prediction: {intercept_10 + slope_10 * 2026:.2f}%")

n = len(modern_era)
x_mean = np.mean(modern_years)
ss_x = np.sum((modern_years - x_mean)**2)
residuals = modern_era - (intercept_mod + slope_mod * modern_years)
mse = np.sum(residuals**2) / (n - 2)
se_pred = np.sqrt(mse * (1 + 1/n + (2026 - x_mean)**2 / ss_x))
pred_2026 = intercept_mod + slope_mod * 2026
print(f"\nPrediction Interval (Modern Era Trend):")
print(f"  Point Estimate: {pred_2026:.2f}%")
print(f"  95% CI: [{pred_2026 - 1.96*se_pred:.2f}%, {pred_2026 + 1.96*se_pred:.2f}%]")

def ema(data, span):
    alpha = 2 / (span + 1)
    result = np.zeros_like(data, dtype=float)
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = alpha * data[i] + (1 - alpha) * result[i-1]
    return result

ema_5 = ema(ratings, 5)
ema_10 = ema(ratings, 10)
print(f"\nExponential Moving Averages (at 2025):")
print(f"  EMA-5: {ema_5[-1]:.2f}%")
print(f"  EMA-10: {ema_10[-1]:.2f}%")

ar1_coef = np.corrcoef(ratings[:-1], ratings[1:])[0, 1]
print(f"\nAR(1) Analysis:")
print(f"  Autocorrelation (lag 1): {ar1_coef:.4f}")

ar_slope, ar_intercept, _, _, _ = stats.linregress(ratings[:-1], ratings[1:])
ar1_pred = ar_intercept + ar_slope * ratings[-1]
print(f"  AR(1) Prediction: {ar1_pred:.2f}%")

print("\n" + "="*70)
print("STEP 4: MONTE CARLO SIMULATION")
print("="*70)

n_simulations = 100000

np.random.seed(42)
mc_results_recent = np.random.normal(np.mean(recent_10), np.std(recent_10), n_simulations)

base_mean = np.mean(recent_5)
base_std = np.std(recent_5)
mc_results_recent5 = np.random.normal(base_mean, base_std * 1.3, n_simulations)

trend_pred = intercept_mod + slope_mod * 2026
trend_uncertainty = se_pred
mc_results_trend = np.random.normal(trend_pred, trend_uncertainty, n_simulations)

model_choice = np.random.choice([0, 1, 2], n_simulations, p=[0.35, 0.35, 0.30])
mc_results_ensemble = np.where(
    model_choice == 0, mc_results_recent,
    np.where(model_choice == 1, mc_results_recent5, mc_results_trend)
)

print(f"\nMonte Carlo Results (n={n_simulations:,} simulations)")
print("\nModel 1: Recent 10-Year Distribution")
print(f"  Median: {np.median(mc_results_recent):.2f}%")
print(f"  90% CI: [{np.percentile(mc_results_recent, 5):.2f}%, {np.percentile(mc_results_recent, 95):.2f}%]")

print("\nModel 2: Recent 5-Year Distribution (widened)")
print(f"  Median: {np.median(mc_results_recent5):.2f}%")
print(f"  90% CI: [{np.percentile(mc_results_recent5, 5):.2f}%, {np.percentile(mc_results_recent5, 95):.2f}%]")

print("\nModel 3: Trend Extrapolation")
print(f"  Median: {np.median(mc_results_trend):.2f}%")
print(f"  90% CI: [{np.percentile(mc_results_trend, 5):.2f}%, {np.percentile(mc_results_trend, 95):.2f}%]")

print("\nEnsemble Model (35% recent-10, 35% recent-5, 30% trend)")
print(f"  Median: {np.median(mc_results_ensemble):.2f}%")
print(f"  Mean: {np.mean(mc_results_ensemble):.2f}%")
print(f"  Std Dev: {np.std(mc_results_ensemble):.2f}%")

print("\n" + "="*70)
print("STEP 5: EVIDENCE ADJUSTMENTS")
print("="*70)

print("""
FACTORS PUSHING UP:
  + Bad Bunny halftime show (Spanish-language audience growth) | Strength: WEAK | +0.3%
  + No Chiefs/repeat fatigue (new storylines) | Strength: WEAK | +0.2%
  + NFL regular season ratings up in 2025-26 | Strength: WEAK | +0.2%
  + Super Bowl LIX set record for viewers | Strength: WEAK | +0.1%

FACTORS PUSHING DOWN:
  - Less "starpower" without Mahomes/Kelce/Swift effect | Strength: MODERATE | -0.5%
  - Younger, less-known quarterbacks likely | Strength: WEAK | -0.2%
  - Continued cord-cutting (offset by streaming/OOH) | Strength: WEAK | -0.2%
  - 2022 low (37.9%) shows downside risk exists | Strength: WEAK | -0.1%

NET ADJUSTMENT: +0.8% - 1.0% = -0.2%

Note: Adjustments are small because household ratings have been remarkably 
stable (38-47% range in modern era despite massive changes in TV landscape).
The factors largely offset each other.
""")

net_adjustment = -0.2

print("\n" + "="*70)
print("STEP 6: EXTERNAL SIGNALS")
print("="*70)

print("""
METACULUS COMMUNITY (403 forecasters):
  - Community median revealed next week
  - Current shown range: ~38.8% to 46.3%
  - Sample predictions from comments:
    * grainmumy: 41.2% (40.5-41.8) based on 10-year historical average
    * SandroAVL: 41.5% (40.9-42.1) using Monte Carlo model

PREDICTION MARKETS:
  - No direct prediction market found for household rating
  - Markets exist for game outcomes but not viewership metrics

EXPERT ANALYSIS (from comments):
  - kk27: Notes offsetting factors (Bad Bunny boost vs less starpower)
  - Historical stability noted by multiple forecasters
  - Consensus around 40-42% range
""")

print("\n" + "="*70)
print("STEP 7: ENSEMBLE CALCULATION")
print("="*70)

base_rate_estimate = np.mean(recent_10)
time_series_estimate = intercept_mod + slope_mod * 2026
crowd_estimate = 41.2
evidence_adjusted = base_rate_estimate + net_adjustment

print(f"\nComponent Estimates:")
print(f"  Base Rate (10-year mean): {base_rate_estimate:.2f}%")
print(f"  Time Series (trend): {time_series_estimate:.2f}%")
print(f"  Crowd (Metaculus): {crowd_estimate:.2f}%")
print(f"  Evidence-Adjusted: {evidence_adjusted:.2f}%")

weights = {
    'base_rate': 0.30,
    'time_series': 0.25,
    'crowd': 0.25,
    'adjusted': 0.20
}

final_point = (
    weights['base_rate'] * base_rate_estimate +
    weights['time_series'] * time_series_estimate +
    weights['crowd'] * crowd_estimate +
    weights['adjusted'] * evidence_adjusted
)

print(f"\nEnsemble Calculation:")
print(f"  Base Rate × 0.30 = {base_rate_estimate:.2f} × 0.30 = {base_rate_estimate * 0.30:.2f}")
print(f"  Time Series × 0.25 = {time_series_estimate:.2f} × 0.25 = {time_series_estimate * 0.25:.2f}")
print(f"  Crowd × 0.25 = {crowd_estimate:.2f} × 0.25 = {crowd_estimate * 0.25:.2f}")
print(f"  Adjusted × 0.20 = {evidence_adjusted:.2f} × 0.20 = {evidence_adjusted * 0.20:.2f}")
print(f"  -"*30)
print(f"  WEIGHTED AVERAGE: {final_point:.2f}%")

print("\n" + "="*70)
print("STEP 8: FINAL DISTRIBUTION")
print("="*70)

final_mean = final_point
final_std = np.std(recent_10) * 1.15

np.random.seed(42)
final_distribution = np.random.normal(final_mean, final_std, n_simulations)

percentiles = {
    '5th': np.percentile(final_distribution, 5),
    '25th': np.percentile(final_distribution, 25),
    '50th': np.percentile(final_distribution, 50),
    '75th': np.percentile(final_distribution, 75),
    '95th': np.percentile(final_distribution, 95)
}

print(f"\nFinal Distribution Parameters:")
print(f"  Mean: {final_mean:.2f}%")
print(f"  Std Dev: {final_std:.2f}% (widened by 1.15× for overconfidence)")

print(f"\nFinal Percentile Estimates:")
print(f"  5th percentile (floor):  {percentiles['5th']:.2f}%")
print(f"  25th percentile:         {percentiles['25th']:.2f}%")
print(f"  50th percentile (median):{percentiles['50th']:.2f}%")
print(f"  75th percentile:         {percentiles['75th']:.2f}%")
print(f"  95th percentile (ceiling):{percentiles['95th']:.2f}%")

print("\n" + "="*70)
print("CREATING VISUALIZATIONS...")
print("="*70)

fig = plt.figure(figsize=(16, 14))

ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(years, ratings, 'b-o', markersize=4, linewidth=1, label='Actual Rating')
ax1.axhline(y=np.mean(ratings), color='gray', linestyle='--', alpha=0.5, label=f'All-time Mean ({np.mean(ratings):.1f}%)')
ax1.axhline(y=np.mean(recent_10), color='green', linestyle='--', alpha=0.7, label=f'10-Year Mean ({np.mean(recent_10):.1f}%)')

trend_years = np.array([2000, 2026])
trend_vals = intercept_mod + slope_mod * trend_years
ax1.plot(trend_years, trend_vals, 'r--', alpha=0.7, label='Linear Trend (2000+)')

ax1.axvline(x=2026, color='orange', linestyle=':', alpha=0.8)
ax1.scatter([2026], [final_mean], color='red', s=150, zorder=5, marker='*', label=f'Forecast ({final_mean:.1f}%)')

ax1.fill_between([2025.5, 2026.5], percentiles['5th'], percentiles['95th'], alpha=0.2, color='red')
ax1.fill_between([2025.5, 2026.5], percentiles['25th'], percentiles['75th'], alpha=0.3, color='red')

ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Household Rating (%)', fontsize=11)
ax1.set_title('Super Bowl Household Ratings (1967-2025) with 2026 Forecast', fontsize=12, fontweight='bold')
ax1.legend(loc='lower left', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1965, 2028)
ax1.set_ylim(20, 55)

ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(years[-15:], ratings[-15:], 'b-o', markersize=6, linewidth=2, label='Actual Rating')
ax2.axhline(y=np.mean(recent_10), color='green', linestyle='--', alpha=0.7, label=f'10-Year Mean ({np.mean(recent_10):.1f}%)')

ax2.axvline(x=2026, color='orange', linestyle=':', alpha=0.8)
ax2.scatter([2026], [final_mean], color='red', s=200, zorder=5, marker='*', label=f'Forecast ({final_mean:.1f}%)')

ax2.fill_between([2025.5, 2026.5], percentiles['5th'], percentiles['95th'], alpha=0.2, color='red', label='90% CI')
ax2.fill_between([2025.5, 2026.5], percentiles['25th'], percentiles['75th'], alpha=0.3, color='red', label='50% CI')

for i, (yr, rating) in enumerate(zip(years[-15:], ratings[-15:])):
    ax2.annotate(f'{rating:.1f}', (yr, rating), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8)

ax2.set_xlabel('Year', fontsize=11)
ax2.set_ylabel('Household Rating (%)', fontsize=11)
ax2.set_title('Recent Super Bowl Ratings (2011-2025) with 2026 Forecast', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(2010, 2027)
ax2.set_ylim(35, 50)

ax3 = fig.add_subplot(2, 2, 3)
ax3.hist(final_distribution, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')

for pct_name, pct_val in percentiles.items():
    if pct_name == '50th':
        ax3.axvline(x=pct_val, color='red', linewidth=2, label=f'Median: {pct_val:.1f}%')
    elif pct_name in ['5th', '95th']:
        ax3.axvline(x=pct_val, color='orange', linestyle='--', linewidth=1.5, 
                   label=f'{pct_name}: {pct_val:.1f}%' if pct_name == '5th' else None)
        if pct_name == '95th':
            ax3.axvline(x=pct_val, color='orange', linestyle='--', linewidth=1.5)

ax3.axvline(x=percentiles['5th'], color='orange', linestyle='--', linewidth=1.5, label=f'5th/95th: {percentiles["5th"]:.1f}%/{percentiles["95th"]:.1f}%')
ax3.axvline(x=percentiles['95th'], color='orange', linestyle='--', linewidth=1.5)

ax3.set_xlabel('Household Rating (%)', fontsize=11)
ax3.set_ylabel('Probability Density', fontsize=11)
ax3.set_title('Forecast Distribution for Super Bowl LX', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right', fontsize=9)
ax3.grid(True, alpha=0.3)

ax4 = fig.add_subplot(2, 2, 4)
decades = {
    '1970s': ratings[(years >= 1970) & (years < 1980)],
    '1980s': ratings[(years >= 1980) & (years < 1990)],
    '1990s': ratings[(years >= 1990) & (years < 2000)],
    '2000s': ratings[(years >= 2000) & (years < 2010)],
    '2010s': ratings[(years >= 2010) & (years < 2020)],
    '2020s': ratings[years >= 2020]
}

decade_names = list(decades.keys())
decade_means = [np.mean(d) for d in decades.values()]
decade_stds = [np.std(d) for d in decades.values()]

x_pos = np.arange(len(decade_names))
bars = ax4.bar(x_pos, decade_means, yerr=decade_stds, capsize=5, color='steelblue', alpha=0.7, edgecolor='navy')

ax4.axhline(y=final_mean, color='red', linestyle='--', linewidth=2, label=f'2026 Forecast ({final_mean:.1f}%)')

for i, (mean, std) in enumerate(zip(decade_means, decade_stds)):
    ax4.annotate(f'{mean:.1f}%', (i, mean + std + 1), ha='center', fontsize=10, fontweight='bold')

ax4.set_xticks(x_pos)
ax4.set_xticklabels(decade_names, fontsize=10)
ax4.set_ylabel('Household Rating (%)', fontsize=11)
ax4.set_title('Average Household Rating by Decade', fontsize=12, fontweight='bold')
ax4.legend(loc='upper right', fontsize=9)
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim(35, 50)

plt.tight_layout()
plt.savefig('/home/claude/superbowl_forecast_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Main visualization saved!")

fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

ax = axes[0, 0]
years_yoy = years[1:]
yoy_changes = np.diff(ratings)
colors = ['green' if x >= 0 else 'red' for x in yoy_changes]
ax.bar(years_yoy, yoy_changes, color=colors, alpha=0.7, edgecolor='white')
ax.axhline(y=0, color='black', linewidth=1)
ax.axhline(y=np.mean(yoy_changes), color='blue', linestyle='--', label=f'Mean Change: {np.mean(yoy_changes):.2f}%')
ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Year-over-Year Change (%)', fontsize=10)
ax.set_title('Year-over-Year Rating Changes', fontsize=11, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
lags = range(1, 11)
autocorrs = [np.corrcoef(ratings[:-lag], ratings[lag:])[0, 1] for lag in lags]
ax.bar(lags, autocorrs, color='steelblue', alpha=0.7, edgecolor='navy')
ax.axhline(y=0, color='black', linewidth=1)
ax.axhline(y=1.96/np.sqrt(len(ratings)), color='red', linestyle='--', alpha=0.5, label='95% CI bounds')
ax.axhline(y=-1.96/np.sqrt(len(ratings)), color='red', linestyle='--', alpha=0.5)
ax.set_xlabel('Lag (years)', fontsize=10)
ax.set_ylabel('Autocorrelation', fontsize=10)
ax.set_title('Autocorrelation Function', fontsize=11, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.hist(modern_era, bins=15, density=True, alpha=0.5, color='blue', label='Historical (2000-2025)', edgecolor='navy')
x_range = np.linspace(35, 50, 100)
historical_pdf = stats.norm.pdf(x_range, np.mean(modern_era), np.std(modern_era))
forecast_pdf = stats.norm.pdf(x_range, final_mean, final_std)
ax.plot(x_range, historical_pdf, 'b-', linewidth=2, label=f'Historical Fit (μ={np.mean(modern_era):.1f})')
ax.plot(x_range, forecast_pdf, 'r-', linewidth=2, label=f'Forecast (μ={final_mean:.1f})')
ax.axvline(x=41.7, color='green', linestyle=':', linewidth=2, label='2025 Actual (41.7%)')
ax.set_xlabel('Household Rating (%)', fontsize=10)
ax.set_ylabel('Probability Density', fontsize=10)
ax.set_title('Historical vs Forecast Distribution', fontsize=11, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
models = ['Base Rate\n(10-yr mean)', 'Time Series\n(trend)', 'Crowd\n(Metaculus)', 'Evidence\nAdjusted', 'FINAL\nENSEMBLE']
estimates = [base_rate_estimate, time_series_estimate, crowd_estimate, evidence_adjusted, final_point]
weights_list = [0.30, 0.25, 0.25, 0.20, 1.0]
colors = ['steelblue', 'steelblue', 'steelblue', 'steelblue', 'red']

bars = ax.bar(models, estimates, color=colors, alpha=0.7, edgecolor='navy')
for i, (est, w) in enumerate(zip(estimates, weights_list)):
    weight_text = f'w={w:.2f}' if i < 4 else ''
    ax.annotate(f'{est:.1f}%\n{weight_text}', (i, est + 0.3), ha='center', fontsize=9, fontweight='bold')

ax.axhline(y=final_point, color='red', linestyle='--', alpha=0.5)
ax.set_ylabel('Household Rating (%)', fontsize=10)
ax.set_title('Model Estimates Comparison', fontsize=11, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(38, 44)

plt.tight_layout()
plt.savefig('/home/claude/superbowl_detailed_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Detailed analysis visualization saved!")

print("\n" + "="*70)
print("FINAL FORECAST SUMMARY")
print("="*70)
print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    SUPER BOWL LX HOUSEHOLD RATING                    ║
║                         FINAL FORECAST                               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   Percentile Distribution:                                           ║
║   ───────────────────────────────────────────────────────────────    ║
║                                                                      ║
║     5th percentile (floor):    {percentiles['5th']:>6.2f}%                              ║
║    25th percentile:            {percentiles['25th']:>6.2f}%                              ║
║    50th percentile (MEDIAN):   {percentiles['50th']:>6.2f}%  ◄── POINT ESTIMATE         ║
║    75th percentile:            {percentiles['75th']:>6.2f}%                              ║
║    95th percentile (ceiling):  {percentiles['95th']:>6.2f}%                              ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Key Reasoning:                                                      ║
║  • Historical stability: Ratings have stayed 38-47% since 2000      ║
║  • Recent trend: Slight decline from 2010s peak (avg 45.4%)         ║
║  • 2020s average: 40.4% with high variance (37.9-43.5%)             ║
║  • 2025 result (41.7%) was above recent average                     ║
║  • Factors largely offsetting (Bad Bunny up, less starpower down)   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Confidence: MEDIUM                                                  ║
║  Models Used: Base Rate, Time Series, Crowd, Evidence-Adjusted       ║
╚══════════════════════════════════════════════════════════════════════╝
""")

print("\n" + "="*70)
print("PRE-MORTEM: WHY I COULD BE WRONG")
print("="*70)
print("""
1. UPSIDE RISK: Bad Bunny effect stronger than expected
   - Spanish-language viewership has grown significantly
   - Could push toward 43-44% range
   - Likelihood: MEDIUM

2. DOWNSIDE RISK: Continued structural decline in linear TV
   - 2022's 37.9% showed floor can be lower
   - Could drop to 38-39% range
   - Likelihood: LOW-MEDIUM

3. UPSIDE RISK: Compelling playoff narratives emerge
   - New teams/players create buzz
   - Could exceed 2024's 43.5%
   - Likelihood: LOW

4. MEASUREMENT CHANGE: Nielsen methodology updates
   - OOH and streaming measurement continues evolving
   - Could shift numbers in either direction
   - Likelihood: LOW
""")

print("\n" + "="*70)
print("UPDATE TRIGGERS")
print("="*70)
print("""
| Event                                    | New Estimate Direction |
|------------------------------------------|------------------------|
| Bills or Rams make Super Bowl            | → +0.5% (more starpower)|
| Two small-market/lesser-known teams      | → -0.5%                |
| Major celebrity performance addition     | → +0.3%                |
| Bad weather forecast for game day        | → +0.2% (more indoor)  |
| Community median revealed (<40% or >43%) | → Adjust toward crowd  |
""")

print("\nAnalysis complete! Check the generated visualizations.")
