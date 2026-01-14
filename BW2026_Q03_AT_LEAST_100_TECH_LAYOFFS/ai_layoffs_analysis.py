#!/usr/bin/env python3
"""
AI Industry Layoffs Forecast Analysis
======================================

Question: Will layoffs.fyi report at least 100 AI industry layoffs 
between January 12 and March 13, 2026?

Key insight: This is about layoffs IN the AI industry (companies like xAI, OpenAI)
NOT layoffs CAUSED BY AI at other companies.
"""

import numpy as np
from scipy import stats
import json

# =============================================================================
# HISTORICAL DATA (from research)
# =============================================================================

# 2025 AI Industry layoffs on layoffs.fyi
AI_LAYOFFS_2025 = {
    "total": 800,  # Per the question background
    "xai_september": 500,  # Major outlier event
    "other_ai_companies": 300,  # ~800 - 500
}

# 2026 YTD (as of Jan 12)
AI_LAYOFFS_2026_YTD = 0  # Per comments: "no major AI pure play companies"

# Question parameters
QUESTION_WINDOW_DAYS = 60  # Jan 12 to Mar 13, 2026
THRESHOLD = 100  # People laid off

# =============================================================================
# BASE RATE ANALYSIS
# =============================================================================

print("=" * 70)
print("AI INDUSTRY LAYOFFS FORECAST ANALYSIS")
print("=" * 70)

# Method 1: Simple annual rate extrapolation
print("\n### METHOD 1: Annual Rate Extrapolation ###")

# Using full 2025 rate (includes xAI event)
full_rate_daily = AI_LAYOFFS_2025["total"] / 365
expected_full = full_rate_daily * QUESTION_WINDOW_DAYS
print(f"2025 daily rate (full): {full_rate_daily:.2f} people/day")
print(f"Expected in 60 days (full rate): {expected_full:.1f}")

# Excluding xAI outlier
ex_xai_rate_daily = AI_LAYOFFS_2025["other_ai_companies"] / 365
expected_ex_xai = ex_xai_rate_daily * QUESTION_WINDOW_DAYS
print(f"2025 daily rate (ex-xAI): {ex_xai_rate_daily:.2f} people/day")
print(f"Expected in 60 days (ex-xAI rate): {expected_ex_xai:.1f}")

# =============================================================================
# POISSON MODEL
# =============================================================================

print("\n### METHOD 2: Poisson Model ###")

# Model 1: Using full 2025 rate
lambda_full = expected_full
p_ge_100_full = 1 - stats.poisson.cdf(99, lambda_full)
print(f"Poisson (lambda={lambda_full:.1f}): P(>=100) = {p_ge_100_full:.1%}")

# Model 2: Using ex-xAI rate
lambda_ex = expected_ex_xai
p_ge_100_ex = 1 - stats.poisson.cdf(99, lambda_ex)
print(f"Poisson (lambda={lambda_ex:.1f}): P(>=100) = {p_ge_100_ex:.1%}")

# =============================================================================
# MONTE CARLO WITH LUMPY EVENTS
# =============================================================================

print("\n### METHOD 3: Monte Carlo with Lumpy Events ###")

def simulate_ai_layoffs(n_simulations=100000):
    results = []
    
    for _ in range(n_simulations):
        total_layoffs = 0
        
        # 1. Base steady-state layoffs (small events)
        base_rate_monthly = 25
        base_layoffs = np.random.poisson(base_rate_monthly * 2)
        total_layoffs += base_layoffs
        
        # 2. Probability of "big event" (50+ people)
        p_big_event = 0.20
        
        if np.random.random() < p_big_event:
            big_event_size = int(np.random.lognormal(mean=4.5, sigma=0.7))
            big_event_size = min(big_event_size, 600)
            big_event_size = max(big_event_size, 50)
            total_layoffs += big_event_size
        
        results.append(total_layoffs)
    
    return np.array(results)

np.random.seed(42)
sim_results = simulate_ai_layoffs(100000)

p_ge_100_mc = np.mean(sim_results >= 100)
mean_layoffs = np.mean(sim_results)
median_layoffs = np.median(sim_results)
p5, p25, p75, p95 = np.percentile(sim_results, [5, 25, 75, 95])

print(f"Monte Carlo Results (n=100,000):")
print(f"  P(>=100) = {p_ge_100_mc:.1%}")
print(f"  Mean: {mean_layoffs:.1f}")
print(f"  Median: {median_layoffs:.1f}")
print(f"  90% CI: [{p5:.0f}, {p95:.0f}]")

# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

print("\n### METHOD 4: Sensitivity Analysis ###")

scenarios = [
    ("Pessimistic (quiet period)", 0.10, 20),
    ("Base case", 0.20, 25),
    ("Optimistic (active period)", 0.30, 30),
    ("Q1 seasonal boost", 0.25, 35),
]

print("\nScenario Analysis:")
for name, p_big, base_monthly in scenarios:
    sim = []
    for _ in range(50000):
        total = np.random.poisson(base_monthly * 2)
        if np.random.random() < p_big:
            total += int(np.random.lognormal(4.5, 0.7))
        sim.append(total)
    prob = np.mean(np.array(sim) >= 100)
    print(f"  {name}: P(>=100) = {prob:.1%}")

# =============================================================================
# COMMUNITY FORECASTS
# =============================================================================

print("\n### COMMUNITY FORECASTS ###")

community = {
    "Rgoger7": 0.70,
    "ksurapaneni": 0.25,
    "SandroAVL": 0.20,
}

community_avg = np.mean(list(community.values()))
print("Individual forecasts:")
for name, prob in community.items():
    print(f"  {name}: {prob:.0%}")
print(f"Community average: {community_avg:.1%}")

# =============================================================================
# FINAL ENSEMBLE
# =============================================================================

print("\n" + "=" * 70)
print("ENSEMBLE FORECAST")
print("=" * 70)

estimates = {
    "Poisson (full 2025 rate)": p_ge_100_full,
    "Poisson (ex-xAI rate)": p_ge_100_ex,
    "Monte Carlo (lumpy model)": p_ge_100_mc,
    "Community average": community_avg,
}

weights = {
    "Poisson (full 2025 rate)": 0.15,
    "Poisson (ex-xAI rate)": 0.20,
    "Monte Carlo (lumpy model)": 0.40,
    "Community average": 0.25,
}

print("\nModel Estimates:")
for model, est in estimates.items():
    w = weights[model]
    contrib = est * w
    print(f"  {model}: {est:.1%} x {w:.2f} = {contrib:.1%}")

final_estimate = sum(estimates[m] * weights[m] for m in estimates)
print(f"\n{'='*50}")
print(f"FINAL ENSEMBLE ESTIMATE: {final_estimate:.1%}")
print(f"{'='*50}")

# =============================================================================
# OUTPUT SUMMARY
# =============================================================================

summary = {
    "question": "Will layoffs.fyi report >=100 AI industry layoffs Jan 12 - Mar 13, 2026?",
    "final_forecast": round(final_estimate * 100, 1),
    "confidence": "Medium",
    "key_insight": "Distribution is LUMPY - depends on whether one big event occurs",
    "base_rate_analysis": {
        "2025_ai_layoffs_total": 800,
        "2025_xai_event": 500,
        "2025_other_ai": 300,
        "expected_60_day_ex_xai": round(expected_ex_xai, 1),
    },
    "monte_carlo": {
        "p_ge_100": round(p_ge_100_mc * 100, 1),
        "mean": round(mean_layoffs, 1),
        "median": round(median_layoffs, 1),
    },
    "community_forecasts": {name: f"{p:.0%}" for name, p in community.items()},
}

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(json.dumps(summary, indent=2))
