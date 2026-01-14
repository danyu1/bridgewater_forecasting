import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json

np.random.seed(42)

utilities_data = {
    "NextEra Energy": {
        "ticker": "NEE",
        "earnings_date": "2026-01-27",
        "market_cap_b": 156,
        "existing_capex_plan_b": 205,
        "data_center_exposure": "medium",
        "already_announced_2025": False,
        "prob_low": 0.25,
        "prob_mid": 0.35,
        "prob_high": 0.45,
        "notes": "Largest US utility, Jan 27 earnings, $185-225B capex plan 2025-2032"
    },
    "Southern Company": {
        "ticker": "SO",
        "earnings_date": "2026-02-12",
        "market_cap_b": 95,
        "existing_capex_plan_b": 76,
        "data_center_exposure": "high",
        "already_announced_2025": True,
        "prob_low": 0.15,
        "prob_mid": 0.22,
        "prob_high": 0.30,
        "notes": "Already increased by $13B in July 2025, Georgia Power 50% capacity increase approved"
    },
    "Duke Energy": {
        "ticker": "DUK",
        "earnings_date": "2026-02-13",
        "market_cap_b": 95,
        "existing_capex_plan_b": 87,
        "data_center_exposure": "high",
        "already_announced_2025": True,
        "prob_low": 0.10,
        "prob_mid": 0.18,
        "prob_high": 0.25,
        "notes": "Already announced $10B increase Feb 2025, next plan could be $95-100B"
    },
    "PG&E": {
        "ticker": "PCG",
        "earnings_date": "2026-02-06",
        "market_cap_b": 43,
        "existing_capex_plan_b": 73,
        "data_center_exposure": "high",
        "already_announced_2025": False,
        "prob_low": 0.15,
        "prob_mid": 0.25,
        "prob_high": 0.35,
        "notes": "10 GW data center pipeline, $73B 5-year plan, California regulatory environment"
    },
    "Entergy": {
        "ticker": "ETR",
        "earnings_date": "2026-02-05",
        "market_cap_b": 37,
        "existing_capex_plan_b": 41,
        "data_center_exposure": "high",
        "already_announced_2025": False,
        "prob_low": 0.18,
        "prob_mid": 0.28,
        "prob_high": 0.38,
        "notes": "$41B capex plan, 7-12 GW data center pipeline, Google West Memphis deal"
    },
    "FirstEnergy": {
        "ticker": "FE",
        "earnings_date": "2026-02-18",
        "market_cap_b": 25,
        "existing_capex_plan_b": 28,
        "data_center_exposure": "medium",
        "already_announced_2025": False,
        "prob_low": 0.10,
        "prob_mid": 0.18,
        "prob_high": 0.25,
        "notes": "$28B Energize365 program, 15 GW additional load by 2035"
    },
    "Exelon": {
        "ticker": "EXC",
        "earnings_date": "2026-02-12",
        "market_cap_b": 44,
        "existing_capex_plan_b": 38,
        "data_center_exposure": "medium",
        "already_announced_2025": False,
        "prob_low": 0.08,
        "prob_mid": 0.15,
        "prob_high": 0.22,
        "notes": "T&D utility, less direct generation exposure"
    },
    "PPL Corp": {
        "ticker": "PPL",
        "earnings_date": "2026-02-20",
        "market_cap_b": 26,
        "existing_capex_plan_b": 17,
        "data_center_exposure": "high",
        "already_announced_2025": False,
        "prob_low": 0.12,
        "prob_mid": 0.20,
        "prob_high": 0.28,
        "notes": "11 GW data center agreements, $5B threshold may be challenging"
    },
    "CenterPoint": {
        "ticker": "CNP",
        "earnings_date": "2026-02-20",
        "market_cap_b": 24,
        "existing_capex_plan_b": 47,
        "data_center_exposure": "medium",
        "already_announced_2025": False,
        "prob_low": 0.10,
        "prob_mid": 0.18,
        "prob_high": 0.25,
        "notes": "Texas exposure, growing data center interest in Houston area"
    },
    "Other Utilities": {
        "ticker": "OTHER",
        "earnings_date": "2026-02-15",
        "market_cap_b": 100,
        "existing_capex_plan_b": 150,
        "data_center_exposure": "medium",
        "already_announced_2025": False,
        "prob_low": 0.08,
        "prob_mid": 0.15,
        "prob_high": 0.22,
        "notes": "Aggregate of smaller utilities (Ameren, Evergy, WEC, etc.)"
    }
}

def monte_carlo_any_announcement(utilities, n_simulations=100000):
    results = []
    utility_triggers = {name: 0 for name in utilities.keys()}
    
    for _ in range(n_simulations):
        any_announced = False
        for name, data in utilities.items():
            prob = np.random.triangular(data['prob_low'], data['prob_mid'], data['prob_high'])
            if np.random.random() < prob:
                any_announced = True
                utility_triggers[name] += 1
        results.append(1 if any_announced else 0)
    
    results = np.array(results)
    trigger_probs = {name: count / n_simulations for name, count in utility_triggers.items()}
    
    return {
        'probability': np.mean(results),
        'std': np.std(results),
        'ci_5': np.percentile(results, 5),
        'ci_95': np.percentile(results, 95),
        'utility_contribution': trigger_probs,
        'n_simulations': n_simulations
    }

def sensitivity_analysis(utilities, n_simulations=50000):
    sensitivities = {}
    
    base_result = monte_carlo_any_announcement(utilities, n_simulations)
    base_prob = base_result['probability']
    
    for target_utility in utilities.keys():
        modified_utilities = {}
        for name, data in utilities.items():
            if name == target_utility:
                modified_utilities[name] = {**data, 'prob_low': 0, 'prob_mid': 0.001, 'prob_high': 0.001}
            else:
                modified_utilities[name] = data.copy()
        
        result = monte_carlo_any_announcement(modified_utilities, n_simulations)
        sensitivities[target_utility] = base_prob - result['probability']
    
    return sensitivities

def calculate_base_rate():
    announcements_2025 = [
        {"date": "2025-02-12", "utility": "Dominion Energy", "increase_b": 7},
        {"date": "2025-02-13", "utility": "Duke Energy", "increase_b": 10},
        {"date": "2025-07-30", "utility": "AEP", "increase_b": 16},
        {"date": "2025-10-29", "utility": "NiSource", "increase_b": 7},
        {"date": "2025-10-31", "utility": "Xcel Energy", "increase_b": 15},
        {"date": "2025-12-04", "utility": "DTE Energy", "increase_b": 6.5}
    ]
    
    total_2025 = len(announcements_2025)
    q1_announcements = sum(1 for a in announcements_2025 if a['date'].startswith('2025-01') or a['date'].startswith('2025-02'))
    
    question_window_days = 59
    year_days = 365
    
    uniform_expected = total_2025 * (question_window_days / year_days)
    
    q1_rate = q1_announcements / total_2025 if total_2025 > 0 else 0
    
    return {
        'total_2025_announcements': total_2025,
        'q1_2025_announcements': q1_announcements,
        'q1_share_of_total': q1_rate,
        'window_days': question_window_days,
        'uniform_expected': uniform_expected,
        'announcements': announcements_2025
    }

def bayesian_update(prior, likelihood_if_true, likelihood_if_false):
    prior_odds = prior / (1 - prior)
    likelihood_ratio = likelihood_if_true / likelihood_if_false
    posterior_odds = prior_odds * likelihood_ratio
    posterior = posterior_odds / (1 + posterior_odds)
    return posterior

print("=" * 70)
print("BRIDGEWATER FORECASTING TOURNAMENT - UTILITY CAPEX ANALYSIS")
print("=" * 70)
print("\nQuestion: Will any US electric utility announce $5B+ capex increase")
print("          citing data center demand between Jan 13 - Mar 12, 2026?")
print("=" * 70)

print("\n" + "=" * 70)
print("BASE RATE ANALYSIS")
print("=" * 70)
base_rate = calculate_base_rate()
print(f"\n2025 Announcements meeting criteria: {base_rate['total_2025_announcements']}")
print(f"Q1 2025 Announcements: {base_rate['q1_2025_announcements']} ({base_rate['q1_share_of_total']:.1%} of total)")
print(f"\nQuestion window: {base_rate['window_days']} days")
print(f"Expected announcements (uniform distribution): {base_rate['uniform_expected']:.2f}")

print("\nHistorical announcements:")
for a in base_rate['announcements']:
    print(f"  {a['date']}: {a['utility']} - ${a['increase_b']}B increase")

print("\n" + "=" * 70)
print("MONTE CARLO SIMULATION")
print("=" * 70)

n_sims = 100000
results = monte_carlo_any_announcement(utilities_data, n_sims)

print(f"\nSimulations run: {n_sims:,}")
print(f"\n{'='*50}")
print(f"  PROBABILITY OF AT LEAST ONE ANNOUNCEMENT: {results['probability']:.1%}")
print(f"{'='*50}")
print(f"\nStandard Deviation: {results['std']:.3f}")

print("\n" + "-" * 50)
print("Individual Utility Contribution to YES Resolution:")
print("-" * 50)
sorted_contrib = sorted(results['utility_contribution'].items(), 
                        key=lambda x: x[1], reverse=True)
for name, prob in sorted_contrib:
    print(f"  {name:20} | {prob:.1%}")

print("\n" + "=" * 70)
print("SENSITIVITY ANALYSIS")
print("=" * 70)
sensitivities = sensitivity_analysis(utilities_data)
print("\nImpact on probability if each utility is removed:")
print("-" * 50)
sorted_sens = sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)
for name, impact in sorted_sens:
    print(f"  {name:20} | -{impact:.1%}")

print("\n" + "=" * 70)
print("ENSEMBLE FORECAST")
print("=" * 70)

base_rate_estimate = 0.55
monte_carlo_estimate = results['probability']
crowd_estimate = 0.75
adjusted_estimate = 0.70

weights = {
    'base_rate': 0.30,
    'monte_carlo': 0.30,
    'crowd': 0.25,
    'adjusted': 0.15
}

ensemble = (
    base_rate_estimate * weights['base_rate'] +
    monte_carlo_estimate * weights['monte_carlo'] +
    crowd_estimate * weights['crowd'] +
    adjusted_estimate * weights['adjusted']
)

print(f"\nModel Estimates:")
print(f"  Base Rate (2025 pattern):     {base_rate_estimate:.1%} (weight: {weights['base_rate']:.0%})")
print(f"  Monte Carlo Simulation:       {monte_carlo_estimate:.1%} (weight: {weights['monte_carlo']:.0%})")
print(f"  Metaculus Community:          {crowd_estimate:.1%} (weight: {weights['crowd']:.0%})")
print(f"  Evidence-Adjusted:            {adjusted_estimate:.1%} (weight: {weights['adjusted']:.0%})")
print(f"\n{'='*50}")
print(f"  ENSEMBLE FORECAST: {ensemble:.1%}")
print(f"{'='*50}")

output = {
    'final_forecast': round(ensemble * 100, 1),
    'monte_carlo_estimate': round(results['probability'] * 100, 1),
    'base_rate_estimate': round(base_rate_estimate * 100, 1),
    'crowd_estimate': round(crowd_estimate * 100, 1),
    'utility_probabilities': {k: round(v * 100, 1) for k, v in results['utility_contribution'].items()},
    'sensitivities': {k: round(v * 100, 2) for k, v in sensitivities.items()},
    'base_rate_data': base_rate
}

with open('/home/claude/forecast_output.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print("\n\nResults saved to forecast_output.json")
