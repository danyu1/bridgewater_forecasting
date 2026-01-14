import numpy as np
import matplotlib.pyplot as plt

games = [
    'Indiana Jones And\nThe Great Circle',
    'Sword of the Sea',
    'Helldivers 2',
    'Star Wars Outlaws',
    'Avatar: Frontiers\nof Pandora'
]

my_forecast = [0.33, 0.25, 0.22, 0.12, 0.08]
community = [0.233, 0.212, 0.233, 0.170, 0.152]

composers = [
    'Gordy Haab',
    'Austin Wintory',
    'Wilbert Roget II',
    'Johnson & Roget II',
    'Pinar Toprak'
]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Grammy 2026 - Best Video Game Soundtrack Prediction', fontsize=14, fontweight='bold')

ax1 = axes[0, 0]
x = np.arange(len(games))
width = 0.35

bars1 = ax1.bar(x - width/2, [p*100 for p in my_forecast], width, label='My Forecast', color='#2ecc71', edgecolor='black')
bars2 = ax1.bar(x + width/2, [p*100 for p in community], width, label='Community', color='#3498db', edgecolor='black', alpha=0.7)

ax1.set_ylabel('Probability (%)', fontsize=10)
ax1.set_title('Forecast Comparison: My Model vs Community', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(games, fontsize=8)
ax1.legend()
ax1.set_ylim(0, 45)

for bar, val in zip(bars1, my_forecast):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.0%}', 
             ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2 = axes[0, 1]
colors = ['#2ecc71', '#9b59b6', '#e74c3c', '#3498db', '#f39c12']
explode = (0.05, 0, 0, 0, 0)
wedges, texts, autotexts = ax2.pie(my_forecast, explode=explode, labels=games, colors=colors,
                                    autopct='%1.0f%%', startangle=90, 
                                    wedgeprops=dict(edgecolor='black'))
ax2.set_title('Final Forecast Distribution', fontsize=11)

ax3 = axes[1, 0]
factors = ['Prior Grammy Win', 'Williams Style', 'Orchestral Score', 'Abbey Road Recording', 'No Vote Split']
indiana_jones = [1.0, 1.0, 1.0, 1.0, 1.0]
sword_of_sea = [0.0, 0.0, 0.7, 1.0, 1.0]
helldivers = [0.0, 0.0, 0.8, 0.0, 0.0]

x = np.arange(len(factors))
width = 0.25

ax3.barh(x - width, indiana_jones, width, label='Indiana Jones', color='#2ecc71')
ax3.barh(x, sword_of_sea, width, label='Sword of the Sea', color='#9b59b6')
ax3.barh(x + width, helldivers, width, label='Helldivers 2', color='#e74c3c')

ax3.set_xlabel('Factor Score (0-1)', fontsize=10)
ax3.set_yticks(x)
ax3.set_yticklabels(factors, fontsize=9)
ax3.set_title('Key Factor Comparison (Top 3 Candidates)', fontsize=11)
ax3.legend(loc='lower right')
ax3.set_xlim(0, 1.2)

ax4 = axes[1, 1]
years = ['2023', '2024', '2025', '2026\n(Predicted)']
winners = [
    "Assassin's Creed\nValhalla: Dawn\nof Ragnarok",
    "Star Wars Jedi:\nSurvivor",
    "Wizardry:\nProving Grounds",
    "Indiana Jones And\nThe Great Circle"
]
winner_composers = ['Stephanie Economou', 'Barton & Haab', 'Winifred Phillips', 'Gordy Haab (33%)']
colors_hist = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71']

bars = ax4.barh(years, [1, 1, 1, 0.33], color=colors_hist, edgecolor='black')
for i, (bar, winner, composer) in enumerate(zip(bars, winners, winner_composers)):
    ax4.text(0.05, bar.get_y() + bar.get_height()/2, f'{winner}\n({composer})', 
             va='center', ha='left', fontsize=8, color='white' if i < 3 else 'black')

ax4.set_xlabel('Win Probability', fontsize=10)
ax4.set_title('Past Winners + 2026 Prediction', fontsize=11)
ax4.set_xlim(0, 1.1)

plt.tight_layout()
plt.savefig('/home/claude/grammy_forecast_visualization.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

fig2, ax = plt.subplots(figsize=(12, 6))

games_short = ['Indiana Jones', 'Sword of Sea', 'Helldivers 2', 'Star Wars Outlaws', 'Avatar']
y_pos = np.arange(len(games_short))

ax.barh(y_pos, [p*100 for p in my_forecast], color=['#2ecc71', '#9b59b6', '#e74c3c', '#3498db', '#f39c12'],
        edgecolor='black', height=0.6)

for i, (prob, game, composer) in enumerate(zip(my_forecast, games_short, composers)):
    ax.text(prob*100 + 1, i, f'{prob:.0%} - {composer}', va='center', fontsize=10)

ax.set_yticks(y_pos)
ax.set_yticklabels(games_short, fontsize=11)
ax.set_xlabel('Win Probability (%)', fontsize=12)
ax.set_title('Grammy 2026 Best Video Game Soundtrack - Final Forecast\n(68th Annual Grammy Awards - February 1, 2026)', 
             fontsize=13, fontweight='bold')
ax.set_xlim(0, 50)

text_box = """KEY FACTORS:
━━━━━━━━━━━━━━━━━━━━━
• Gordy Haab won 2024 Grammy
• Abbey Road orchestral recording
• John Williams style emulation
• Vote splitting hurts Roget II
  (nominated for 2 games)
• 100% of past winners: orchestral
━━━━━━━━━━━━━━━━━━━━━"""

ax.text(0.98, 0.5, text_box, transform=ax.transAxes, fontsize=9, 
        verticalalignment='center', horizontalalignment='right',
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('/home/claude/grammy_forecast_summary.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Visualizations saved!")
print("  - grammy_forecast_visualization.png")
print("  - grammy_forecast_summary.png")
