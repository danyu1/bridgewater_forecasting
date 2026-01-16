import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
N = 200000

cut_mean = 0.06
cut_sd = 0.03
cut_p = np.clip(rng.normal(cut_mean, cut_sd, N), 0, 1)
cut_event_prob = 1 - (1 - cut_p) ** 2

launch_mean = 0.06
launch_sd = 0.03
launch_p = np.clip(rng.normal(launch_mean, launch_sd, N), 0, 1)
launch_cut_prob = 0.35
launch_event_prob = launch_p * launch_cut_prob

combined_prob = 1 - (1 - cut_event_prob) * (1 - launch_event_prob)

print("mean", float(np.mean(combined_prob)))
print("median", float(np.median(combined_prob)))
print("p5", float(np.percentile(combined_prob, 5)))
print("p95", float(np.percentile(combined_prob, 95)))

plt.figure(figsize=(8,5))
plt.hist(combined_prob, bins=50, color="steelblue", alpha=0.8)
plt.title("Monte Carlo Probability Distribution (YES)")
plt.xlabel("Probability")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("mc_probability_distribution.png", dpi=150)
plt.close()

labels = ["2023-03","2023-11","2024-05","2025-08","2025-11","2025-12"]
inputs = [30.0,10.0,2.5,1.25,1.25,1.75]
outputs = [60.0,30.0,10.0,10.0,10.0,14.0]

plt.figure(figsize=(9,5))
plt.plot(labels, inputs, marker="o", label="Input $/1M")
plt.plot(labels, outputs, marker="o", label="Output $/1M")
plt.axhline(1.25, color="gray", linestyle="--")
plt.axhline(1.75, color="gray", linestyle=":")
plt.axhline(10.0, color="gray", linestyle="--")
plt.axhline(14.0, color="gray", linestyle=":")
plt.title("OpenAI API Price History (approx)")
plt.xlabel("Release")
plt.ylabel("USD per 1M tokens")
plt.legend()
plt.tight_layout()
plt.savefig("price_history.png", dpi=150)
plt.close()
