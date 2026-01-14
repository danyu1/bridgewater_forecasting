import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

january_mom = {
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

mom_2025 = {
    'Jan': -0.45,
    'Feb': -0.97,
    'Mar': -0.20,
    'Apr': -0.46,
    'May': 0.79,
    'Jun': 0.00,
    'Jul': 0.46,
    'Aug': 0.52,
    'Sep': -0.13,
    'Oct': -0.13,
    'Nov': 0.71,
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('India WPI Monthly Inflation Forecast Analysis - January 2026', fontsize=14, fontweight='bold')

ax1 = axes[0, 0]
years = list(january_mom.keys())
values = list(january_mom.values())
colors = ['#2ecc71' if v > 0 else '#e74c3c' for v in values]
bars = ax1.bar(years, values, color=colors, edgecolor='black', alpha=0.8)
ax1.axhline(y=np.mean(values), color='blue', linestyle='--', linewidth=2, label=f'Mean: {np.mean(values):.2f}%')
ax1.axhline(y=np.median(values), color='orange', linestyle='-.', linewidth=2, label=f'Median: {np.median(values):.2f}%')
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel('MoM Change (%)', fontsize=10)
ax1.set_title('Historical January WPI MoM Changes (Dec→Jan)', fontsize=11)
ax1.legend(loc='upper right')
ax1.set_ylim(-2.5, 1.5)
for bar, val in zip(bars, values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05 if val > 0 else bar.get_height() - 0.15,
             f'{val:.2f}', ha='center', va='bottom' if val > 0 else 'top', fontsize=8)

ax2 = axes[0, 1]
months = list(mom_2025.keys())
values_2025 = list(mom_2025.values())
colors_2025 = ['#2ecc71' if v > 0 else '#e74c3c' for v in values_2025]
bars2 = ax2.bar(months, values_2025, color=colors_2025, edgecolor='black', alpha=0.8)
ax2.axhline(y=np.mean(values_2025), color='blue', linestyle='--', linewidth=2, label=f'Mean: {np.mean(values_2025):.2f}%')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.set_xlabel('Month', fontsize=10)
ax2.set_ylabel('MoM Change (%)', fontsize=10)
ax2.set_title('2025 WPI MoM Pattern (Current Regime)', fontsize=11)
ax2.legend(loc='upper left')
ax2.set_ylim(-1.2, 1.0)

ax3 = axes[1, 0]
np.random.seed(42)
jan_values = list(january_mom.values())
jan_mean = np.mean(jan_values)
jan_std = np.std(jan_values, ddof=1)
simulations = np.random.normal(jan_mean, jan_std, 100000)
ax3.hist(simulations, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
x_range = np.linspace(-3, 2.5, 200)
pdf = stats.norm.pdf(x_range, jan_mean, jan_std)
ax3.plot(x_range, pdf, 'r-', linewidth=2, label='Normal fit')
ax3.axvline(x=0.13, color='green', linestyle='-', linewidth=3, label='Ensemble: 0.13%')
ax3.axvline(x=np.percentile(simulations, 5), color='purple', linestyle=':', linewidth=2, label=f'5th %ile: {np.percentile(simulations, 5):.2f}%')
ax3.axvline(x=np.percentile(simulations, 95), color='purple', linestyle=':', linewidth=2, label=f'95th %ile: {np.percentile(simulations, 95):.2f}%')
ax3.set_xlabel('MoM Change (%)', fontsize=10)
ax3.set_ylabel('Density', fontsize=10)
ax3.set_title('Monte Carlo Distribution (January Model)', fontsize=11)
ax3.legend(loc='upper right', fontsize=8)
ax3.set_xlim(-3, 2.5)

ax4 = axes[1, 1]
models = ['January\nBase Rate', 'All-Months\nBase Rate', '2025\nRegime', 'Crowd\n(nikakovskaya)', 'Crowd\n(SandroAVL)', 'ENSEMBLE']
estimates = [0.06, 0.235, -0.06, 0.27, 0.30, 0.13]
weights = [0.25, 0.20, 0.25, 0.15, 0.15, 1.0]
colors_model = ['#3498db', '#9b59b6', '#e67e22', '#27ae60', '#16a085', '#e74c3c']
bars4 = ax4.barh(models, estimates, color=colors_model, edgecolor='black', alpha=0.8)
for bar, est, w in zip(bars4, estimates, weights):
    width = bar.get_width()
    weight_str = f'(w={w:.2f})' if w < 1 else '(FINAL)'
    ax4.text(max(width, 0) + 0.02, bar.get_y() + bar.get_height()/2, 
             f'{est:.2f}% {weight_str}', va='center', fontsize=9)
ax4.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
ax4.axvline(x=0.13, color='red', linestyle='--', linewidth=2, alpha=0.7)
ax4.set_xlabel('MoM Change (%)', fontsize=10)
ax4.set_title('Model Ensemble Comparison', fontsize=11)
ax4.set_xlim(-0.2, 0.6)

plt.tight_layout()
plt.savefig('/home/claude/wpi_forecast_visualization.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

fig2, ax = plt.subplots(figsize=(12, 6))

final_forecast = {
    'p5': -1.69,
    'p25': -0.62,
    'median': 0.13,
    'p75': 0.88,
    'p95': 1.95
}

percentiles = [5, 25, 50, 75, 95]
values_pct = [final_forecast['p5'], final_forecast['p25'], final_forecast['median'], 
              final_forecast['p75'], final_forecast['p95']]

ax.fill_between([0, 1], final_forecast['p5'], final_forecast['p95'], alpha=0.2, color='steelblue', label='90% CI')
ax.fill_between([0, 1], final_forecast['p25'], final_forecast['p75'], alpha=0.4, color='steelblue', label='50% CI')
ax.axhline(y=final_forecast['median'], color='red', linewidth=3, label=f'Median: {final_forecast["median"]}%')

ax.axhline(y=0.27, color='green', linestyle='--', linewidth=2, alpha=0.7, label='nikakovskaya: 0.27%')
ax.axhline(y=0.30, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='SandroAVL: 0.30%')

ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-2.5, 2.5)
ax.set_ylabel('MoM Inflation Rate (%)', fontsize=12)
ax.set_title('India WPI January 2026 Monthly Inflation Forecast\nwith Confidence Intervals', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.set_xticks([])

text_box = f"""FORECAST SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━
Median:     {final_forecast['median']:.2f}%
5th %-ile:  {final_forecast['p5']:.2f}%
25th %-ile: {final_forecast['p25']:.2f}%
75th %-ile: {final_forecast['p75']:.2f}%
95th %-ile: {final_forecast['p95']:.2f}%
━━━━━━━━━━━━━━━━━━━━━━━
90% CI: [{final_forecast['p5']:.2f}%, {final_forecast['p95']:.2f}%]"""

ax.text(1.15, 0.5, text_box, transform=ax.transAxes, fontsize=10, verticalalignment='center',
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('/home/claude/wpi_forecast_summary.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Visualizations saved!")
print("  - wpi_forecast_visualization.png")
print("  - wpi_forecast_summary.png")
