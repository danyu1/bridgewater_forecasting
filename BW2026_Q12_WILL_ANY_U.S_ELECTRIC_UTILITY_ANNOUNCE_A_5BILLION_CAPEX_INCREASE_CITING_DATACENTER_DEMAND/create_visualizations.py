import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

np.random.seed(42)

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#1a1a2e'
plt.rcParams['axes.facecolor'] = '#16213e'
plt.rcParams['text.color'] = '#e8e8e8'
plt.rcParams['axes.labelcolor'] = '#e8e8e8'
plt.rcParams['xtick.color'] = '#e8e8e8'
plt.rcParams['ytick.color'] = '#e8e8e8'
plt.rcParams['axes.edgecolor'] = '#4a4a6a'
plt.rcParams['grid.color'] = '#2a2a4a'
plt.rcParams['font.family'] = 'DejaVu Sans'

utilities_data = {
    "NextEra Energy": {"prob_low": 0.25, "prob_mid": 0.35, "prob_high": 0.45, "earnings": "Jan 27"},
    "Entergy": {"prob_low": 0.18, "prob_mid": 0.28, "prob_high": 0.38, "earnings": "Feb 5"},
    "PG&E": {"prob_low": 0.15, "prob_mid": 0.25, "prob_high": 0.35, "earnings": "Feb 6"},
    "Southern Co": {"prob_low": 0.15, "prob_mid": 0.22, "prob_high": 0.30, "earnings": "Feb 12"},
    "PPL Corp": {"prob_low": 0.12, "prob_mid": 0.20, "prob_high": 0.28, "earnings": "Feb 20"},
    "FirstEnergy": {"prob_low": 0.10, "prob_mid": 0.18, "prob_high": 0.25, "earnings": "Feb 18"},
    "Duke Energy": {"prob_low": 0.10, "prob_mid": 0.18, "prob_high": 0.25, "earnings": "Feb 13"},
    "CenterPoint": {"prob_low": 0.10, "prob_mid": 0.18, "prob_high": 0.25, "earnings": "Feb 20"},
    "Exelon": {"prob_low": 0.08, "prob_mid": 0.15, "prob_high": 0.22, "earnings": "Feb 12"},
    "Other": {"prob_low": 0.08, "prob_mid": 0.15, "prob_high": 0.22, "earnings": "Various"}
}

def run_simulation(n_sims=100000):
    results = []
    for _ in range(n_sims):
        any_announced = False
        for name, data in utilities_data.items():
            prob = np.random.triangular(data['prob_low'], data['prob_mid'], data['prob_high'])
            if np.random.random() < prob:
                any_announced = True
                break
        results.append(1 if any_announced else 0)
    return np.array(results)

fig = plt.figure(figsize=(16, 12))
fig.suptitle('Bridgewater Forecasting Tournament: Utility $5B+ Capex Announcement\n(January 13 - March 12, 2026)', 
             fontsize=16, fontweight='bold', color='#00d4ff', y=0.98)

ax1 = plt.subplot(2, 2, 1)
utilities = list(utilities_data.keys())
prob_mids = [utilities_data[u]['prob_mid'] * 100 for u in utilities]
prob_lows = [utilities_data[u]['prob_low'] * 100 for u in utilities]
prob_highs = [utilities_data[u]['prob_high'] * 100 for u in utilities]

errors = [[prob_mids[i] - prob_lows[i] for i in range(len(utilities))],
          [prob_highs[i] - prob_mids[i] for i in range(len(utilities))]]

colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(utilities)))
bars = ax1.barh(utilities, prob_mids, color=colors, edgecolor='#00d4ff', linewidth=0.5)
ax1.errorbar(prob_mids, utilities, xerr=errors, fmt='none', color='#ff6b6b', capsize=3, capthick=1)

ax1.set_xlabel('Probability of $5B+ Announcement (%)', fontweight='bold')
ax1.set_title('Individual Utility Announcement Probability', fontweight='bold', color='#00d4ff')
ax1.set_xlim(0, 50)
ax1.axvline(x=20, color='#ff6b6b', linestyle='--', alpha=0.5, label='20% threshold')

for i, (bar, prob) in enumerate(zip(bars, prob_mids)):
    ax1.text(prob + 1, bar.get_y() + bar.get_height()/2, f'{prob:.0f}%', 
             va='center', fontsize=9, color='#e8e8e8')

ax2 = plt.subplot(2, 2, 2)

simulation_results = run_simulation(100000)
p_any = np.mean(simulation_results) * 100

model_names = ['Base Rate\n(Historical)', 'Monte Carlo\nSimulation', 'Metaculus\nCommunity', 'Evidence\nAdjusted', 'ENSEMBLE']
model_values = [55, p_any, 75, 70, 73]
model_weights = [0.30, 0.30, 0.25, 0.15, 1.0]
model_colors = ['#3498db', '#9b59b6', '#2ecc71', '#f39c12', '#e74c3c']

bars2 = ax2.bar(model_names, model_values, color=model_colors, edgecolor='white', linewidth=1)
ax2.axhline(y=73, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.8)

for bar, val, weight in zip(bars2, model_values, model_weights):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 1, f'{val:.0f}%',
             ha='center', va='bottom', fontweight='bold', fontsize=11, color='#e8e8e8')
    if weight < 1:
        ax2.text(bar.get_x() + bar.get_width()/2., height/2, f'w={weight:.0%}',
                 ha='center', va='center', fontsize=9, color='white', alpha=0.8)

ax2.set_ylabel('Probability (%)', fontweight='bold')
ax2.set_title('Ensemble Model Comparison', fontweight='bold', color='#00d4ff')
ax2.set_ylim(0, 100)
ax2.axhline(y=50, color='#666', linestyle=':', alpha=0.5)

ax3 = plt.subplot(2, 2, 3)

announcements_2025 = [
    ("Feb 12", "Dominion", 7, "Q4'24 Earnings"),
    ("Feb 13", "Duke", 10, "Q4'24 Earnings"),
    ("Jul 30", "AEP", 16, "Q2'25 Earnings"),
    ("Oct 29", "NiSource", 7, "Q3'25 Earnings"),
    ("Oct 31", "Xcel", 15, "Q3'25 Earnings"),
    ("Dec 4", "DTE", 6.5, "Business Update")
]

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_indices = [0, 1, 1, 0, 0, 0, 6, 0, 0, 9, 9, 11]
announcements_per_month = [0, 2, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1]

bars3 = ax3.bar(months, announcements_per_month, color='#3498db', edgecolor='#00d4ff', linewidth=1)
ax3.axvspan(-0.5, 2.5, alpha=0.3, color='#2ecc71', label='Question Window (Jan-Mar 2026)')

ax3.set_xlabel('Month (2025)', fontweight='bold')
ax3.set_ylabel('Number of Announcements', fontweight='bold')
ax3.set_title('2025 Qualifying Announcements by Month', fontweight='bold', color='#00d4ff')
ax3.legend(loc='upper right')

for i, (bar, count) in enumerate(zip(bars3, announcements_per_month)):
    if count > 0:
        ax3.text(bar.get_x() + bar.get_width()/2., count + 0.05, f'{count}',
                 ha='center', va='bottom', fontweight='bold', fontsize=10, color='#e8e8e8')

ax4 = plt.subplot(2, 2, 4)

n_bootstrap = 10000
bootstrap_results = []
for _ in range(n_bootstrap):
    sim = run_simulation(1000)
    bootstrap_results.append(np.mean(sim) * 100)

ax4.hist(bootstrap_results, bins=50, color='#9b59b6', edgecolor='#00d4ff', 
         alpha=0.7, density=True)

mean_val = np.mean(bootstrap_results)
std_val = np.std(bootstrap_results)
ci_5 = np.percentile(bootstrap_results, 5)
ci_95 = np.percentile(bootstrap_results, 95)

ax4.axvline(mean_val, color='#e74c3c', linewidth=2, label=f'Mean: {mean_val:.1f}%')
ax4.axvline(ci_5, color='#f39c12', linestyle='--', linewidth=1.5, label=f'5th %ile: {ci_5:.1f}%')
ax4.axvline(ci_95, color='#f39c12', linestyle='--', linewidth=1.5, label=f'95th %ile: {ci_95:.1f}%')

ax4.set_xlabel('Probability of YES Resolution (%)', fontweight='bold')
ax4.set_ylabel('Density', fontweight='bold')
ax4.set_title('Monte Carlo Distribution (Bootstrap)', fontweight='bold', color='#00d4ff')
ax4.legend(loc='upper left', fontsize=9)

textstr = f'Final Forecast: 73%\n90% CI: [{ci_5:.0f}% - {ci_95:.0f}%]\nn = {n_bootstrap:,} bootstrap iterations'
props = dict(boxstyle='round', facecolor='#2a2a4a', edgecolor='#00d4ff', alpha=0.9)
ax4.text(0.97, 0.97, textstr, transform=ax4.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout(rect=[0, 0.02, 1, 0.95])

final_text = ("FINAL FORECAST: 73%\n"
              "Key Drivers: NextEra (Jan 27), Entergy, PG&E earnings\n"
              "6 announcements in 2025 • 10 major utilities in window")
fig.text(0.5, 0.01, final_text, ha='center', fontsize=11, 
         style='italic', color='#00d4ff', 
         bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='#00d4ff'))

plt.savefig('/home/claude/utility_forecast_analysis.png', dpi=150, 
            facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
print("Chart saved to /home/claude/utility_forecast_analysis.png")

plt.figure(figsize=(14, 6), facecolor='#1a1a2e')

dates = ['Jan 13', 'Jan 20', 'Jan 27', 'Feb 3', 'Feb 10', 'Feb 17', 'Feb 24', 'Mar 3', 'Mar 12']
cumulative_prob = [0, 0.05, 0.35, 0.45, 0.55, 0.68, 0.72, 0.73, 0.73]

ax = plt.gca()
ax.set_facecolor('#16213e')

plt.plot(dates, [p * 100 for p in cumulative_prob], 'o-', 
         color='#00d4ff', linewidth=2.5, markersize=8)

plt.fill_between(dates, 0, [p * 100 for p in cumulative_prob], 
                 alpha=0.3, color='#00d4ff')

key_events = {
    'Jan 27': ('NextEra\nEarnings', 35),
    'Feb 5': ('Entergy', 45),
    'Feb 12': ('Southern/\nExelon', 55),
    'Feb 13': ('Duke', 65)
}

for date, (label, y_pos) in key_events.items():
    idx = dates.index(date) if date in dates else None
    if idx:
        plt.annotate(label, xy=(dates[idx], cumulative_prob[idx] * 100), 
                    xytext=(dates[idx], y_pos + 10),
                    fontsize=9, ha='center', color='#f39c12',
                    arrowprops=dict(arrowstyle='->', color='#f39c12', lw=1))

plt.axhline(y=73, color='#e74c3c', linestyle='--', linewidth=2, label='Final Forecast: 73%')
plt.axhline(y=75, color='#2ecc71', linestyle=':', linewidth=1.5, label='Metaculus Community: 75%')

plt.xlabel('Date (2026)', fontweight='bold', color='#e8e8e8')
plt.ylabel('Cumulative Probability of YES (%)', fontweight='bold', color='#e8e8e8')
plt.title('Expected Probability Over Time with Key Catalyst Events', 
          fontweight='bold', fontsize=14, color='#00d4ff', pad=20)
plt.legend(loc='lower right', facecolor='#2a2a4a', edgecolor='#00d4ff')
plt.ylim(0, 100)

plt.tick_params(colors='#e8e8e8')
ax.spines['bottom'].set_color('#4a4a6a')
ax.spines['top'].set_color('#4a4a6a')
ax.spines['left'].set_color('#4a4a6a')
ax.spines['right'].set_color('#4a4a6a')

plt.tight_layout()
plt.savefig('/home/claude/utility_timeline.png', dpi=150, 
            facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
print("Timeline chart saved to /home/claude/utility_timeline.png")

print("\n" + "="*60)
print("VISUALIZATION COMPLETE")
print("="*60)
