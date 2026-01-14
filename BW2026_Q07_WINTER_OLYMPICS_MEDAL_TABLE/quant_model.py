import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
n = 100000

def sample_trunc_norm(mu, sigma, size):
    x = rng.normal(mu, sigma, size)
    return np.clip(x, 0, None)

mus = {
    "Norway":15,
    "Germany":12,
    "United States":9,
    "Canada":8,
    "Italy":5,
    "Other":9
}
sigmas = {
    "Norway":2,
    "Germany":2.5,
    "United States":2,
    "Canada":2,
    "Italy":1.5,
    "Other":3
}

samples = {k: sample_trunc_norm(mus[k], sigmas[k], n) for k in mus}
countries = list(mus.keys())

gold_matrix = np.vstack([samples[c] for c in countries]).T
winners = []
for row in gold_matrix:
    top = np.max(row)
    idxs = np.where(row == top)[0]
    if len(idxs) == 1:
        winners.append(countries[idxs[0]])
    else:
        subset = [countries[i] for i in idxs]
        winners.append(sorted(subset)[0])
win_counts = {c:0 for c in countries}
for w in winners:
    win_counts[w] += 1
win_probs = {k: v/n for k,v in win_counts.items()}

print("Winner probabilities:")
for k,v in win_probs.items():
    print(f"{k}: {v*100:.1f}%")

fig, ax = plt.subplots(figsize=(10,6))
for c in countries:
    ax.hist(samples[c], bins=40, alpha=0.4, label=c, density=True)
ax.set_xlabel("Gold medals")
ax.set_ylabel("Density")
ax.set_title("Gold Medal Distribution Samples")
ax.legend()
plt.tight_layout()
plt.savefig("gold_distribution.png", dpi=150)

fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.bar(win_probs.keys(), [win_probs[c]*100 for c in win_probs.keys()], color="steelblue")
ax2.set_ylabel("Win Probability (%)")
ax2.set_title("Simulated Medal-Table Win Probabilities")
plt.tight_layout()
plt.savefig("winner_share.png", dpi=150)
