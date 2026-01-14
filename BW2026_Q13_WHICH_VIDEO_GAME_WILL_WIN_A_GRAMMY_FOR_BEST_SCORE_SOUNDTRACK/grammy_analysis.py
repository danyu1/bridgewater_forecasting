import numpy as np
import json

nominees = {
    'Avatar: Frontiers of Pandora - Secrets of the Spires': {
        'composer': 'Pinar Toprak',
        'community_prob': 0.152,
        'factors': {
            'prior_winner': 0,
            'prior_nominations': 0,
            'orchestral_score': 1,
            'franchise': 1,
            'original_ip': 0,
            'expansion_dlc': 1,
            'vote_splitting': 0,
            'abbey_road_recording': 0,
            'williams_style': 0,
            'industry_buzz': 0.3
        }
    },
    'Helldivers 2': {
        'composer': 'Wilbert Roget II',
        'community_prob': 0.233,
        'factors': {
            'prior_winner': 0,
            'prior_nominations': 0,
            'orchestral_score': 0.8,
            'franchise': 0,
            'original_ip': 1,
            'expansion_dlc': 0,
            'vote_splitting': 1,
            'abbey_road_recording': 0,
            'williams_style': 0,
            'industry_buzz': 0.8
        }
    },
    'Indiana Jones And The Great Circle': {
        'composer': 'Gordy Haab',
        'community_prob': 0.233,
        'factors': {
            'prior_winner': 1,
            'prior_nominations': 1,
            'orchestral_score': 1,
            'franchise': 1,
            'original_ip': 0,
            'expansion_dlc': 0,
            'vote_splitting': 0,
            'abbey_road_recording': 1,
            'williams_style': 1,
            'industry_buzz': 0.9
        }
    },
    'Star Wars Outlaws: Wild Card & A Pirate\'s Fortune': {
        'composer': 'Cody Matthew Johnson & Wilbert Roget II',
        'community_prob': 0.170,
        'factors': {
            'prior_winner': 0,
            'prior_nominations': 0,
            'orchestral_score': 1,
            'franchise': 1,
            'original_ip': 0,
            'expansion_dlc': 1,
            'vote_splitting': 1,
            'abbey_road_recording': 0,
            'williams_style': 0.5,
            'industry_buzz': 0.5
        }
    },
    'Sword of the Sea': {
        'composer': 'Austin Wintory',
        'community_prob': 0.212,
        'factors': {
            'prior_winner': 0,
            'prior_nominations': 4,
            'orchestral_score': 0.7,
            'franchise': 0,
            'original_ip': 1,
            'expansion_dlc': 0,
            'vote_splitting': 0,
            'abbey_road_recording': 1,
            'williams_style': 0,
            'industry_buzz': 0.7
        }
    }
}

weights = {
    'prior_winner': 0.20,
    'prior_nominations': 0.05,
    'orchestral_score': 0.15,
    'franchise': 0.05,
    'original_ip': 0.05,
    'expansion_dlc': -0.10,
    'vote_splitting': -0.15,
    'abbey_road_recording': 0.10,
    'williams_style': 0.15,
    'industry_buzz': 0.10
}

past_winners = {
    2023: {
        'game': "Assassin's Creed Valhalla: Dawn of Ragnarok",
        'composer': 'Stephanie Economou',
        'type': 'expansion',
        'orchestral': True,
        'franchise': True
    },
    2024: {
        'game': 'Star Wars Jedi: Survivor',
        'composer': 'Stephen Barton & Gordy Haab',
        'type': 'full_game',
        'orchestral': True,
        'franchise': True
    },
    2025: {
        'game': 'Wizardry: Proving Grounds of the Mad Overlord',
        'composer': 'Winifred Phillips',
        'type': 'full_game',
        'orchestral': True,
        'franchise': False
    }
}

print("=" * 70)
print("GRAMMY 2026 - BEST VIDEO GAME SOUNDTRACK ANALYSIS")
print("=" * 70)

print("\n" + "=" * 70)
print("PAST WINNERS ANALYSIS")
print("=" * 70)
for year, data in past_winners.items():
    print(f"\n{year}: {data['game']}")
    print(f"  Composer: {data['composer']}")
    print(f"  Type: {data['type']}, Orchestral: {data['orchestral']}, Franchise: {data['franchise']}")

franchise_wins = sum(1 for w in past_winners.values() if w['franchise'])
orchestral_wins = sum(1 for w in past_winners.values() if w['orchestral'])
print(f"\nBase rates from 3 past winners:")
print(f"  Franchise win rate: {franchise_wins}/3 = {franchise_wins/3:.1%}")
print(f"  Orchestral win rate: {orchestral_wins}/3 = {orchestral_wins/3:.1%}")

print("\n" + "=" * 70)
print("FACTOR-BASED SCORING")
print("=" * 70)

base_prob = 0.20
scores = {}

for game, data in nominees.items():
    adjustment = 0
    print(f"\n{game} ({data['composer']})")
    print("-" * 50)
    
    for factor, value in data['factors'].items():
        factor_contribution = weights[factor] * value
        adjustment += factor_contribution
        if abs(factor_contribution) > 0.01:
            print(f"  {factor}: {value} × {weights[factor]:.2f} = {factor_contribution:+.3f}")
    
    raw_score = base_prob + adjustment
    scores[game] = max(0.05, min(0.95, raw_score))
    print(f"  Base: {base_prob:.2f} + Adjustment: {adjustment:+.3f} = Raw: {raw_score:.3f}")

total_score = sum(scores.values())
normalized_probs = {game: score/total_score for game, score in scores.items()}

print("\n" + "=" * 70)
print("NORMALIZED MODEL PROBABILITIES")
print("=" * 70)

for game, prob in sorted(normalized_probs.items(), key=lambda x: -x[1]):
    community = nominees[game]['community_prob']
    diff = prob - community
    print(f"\n{game}:")
    print(f"  Model: {prob:.1%}")
    print(f"  Community: {community:.1%}")
    print(f"  Difference: {diff:+.1%}")

print("\n" + "=" * 70)
print("VOTE SPLITTING ANALYSIS")
print("=" * 70)

roget_combined = nominees['Helldivers 2']['community_prob'] + nominees["Star Wars Outlaws: Wild Card & A Pirate's Fortune"]['community_prob']
sw_key = "Star Wars Outlaws: Wild Card & A Pirate's Fortune"
print(f"\nWilbert Roget II is nominated for BOTH:")
print(f"  Helldivers 2: {nominees['Helldivers 2']['community_prob']:.1%}")
print(f"  Star Wars Outlaws: {nominees[sw_key]['community_prob']:.1%}")
print(f"  Combined if no splitting: {roget_combined:.1%}")
print(f"\nThis vote splitting likely benefits Indiana Jones and Sword of the Sea")

print("\n" + "=" * 70)
print("ENSEMBLE MODEL")
print("=" * 70)

model_weight = 0.50
community_weight = 0.50

ensemble = {}
for game in nominees:
    model_prob = normalized_probs[game]
    community_prob = nominees[game]['community_prob']
    ensemble[game] = model_weight * model_prob + community_weight * community_prob

total_ensemble = sum(ensemble.values())
ensemble = {game: prob/total_ensemble for game, prob in ensemble.items()}

print("\nEnsemble (50% Model + 50% Community):")
for game, prob in sorted(ensemble.items(), key=lambda x: -x[1]):
    print(f"  {game}: {prob:.1%}")

print("\n" + "=" * 70)
print("KEY INSIGHTS")
print("=" * 70)

print("""
1. INDIANA JONES AND THE GREAT CIRCLE (Strongest candidate)
   + Gordy Haab won in 2024 (Star Wars Jedi: Survivor)
   + Recording Academy loves John Williams-style orchestral music
   + Recorded at Abbey Road Studios with full orchestra
   + No vote splitting issues
   + Would be first 2-time winner in category history

2. SWORD OF THE SEA (Strong artistic contender)
   + Austin Wintory: First VG composer ever Grammy-nominated (Journey 2013)
   + 4x Grammy nominated in this category
   + Highly respected in the industry
   - Has never won despite multiple nominations

3. HELLDIVERS 2 (Popular but disadvantaged)
   + Very popular game with strong buzz
   + Original IP with distinctive sound
   - Vote splitting with Star Wars Outlaws (same composer)
   - Less orchestral/prestige than competitors

4. STAR WARS OUTLAWS (Franchise power but limited)
   + Star Wars has won before (2024)
   + Orchestra sound the Academy likes
   - Just expansion DLC content
   - Vote splitting with Helldivers 2

5. AVATAR (Least likely)
   + Major franchise
   - Just expansion DLC
   - Least industry buzz
   - Pinar Toprak has no prior nominations
""")

final_forecast = {
    'Indiana Jones And The Great Circle': 0.33,
    'Sword of the Sea': 0.25,
    'Helldivers 2': 0.22,
    "Star Wars Outlaws: Wild Card & A Pirate's Fortune": 0.12,
    'Avatar: Frontiers of Pandora - Secrets of the Spires': 0.08
}

print("\n" + "=" * 70)
print("FINAL FORECAST")
print("=" * 70)

for game, prob in sorted(final_forecast.items(), key=lambda x: -x[1]):
    print(f"  {game}: {prob:.0%}")

output = {
    'question': 'Grammy 2026 Best Video Game Soundtrack',
    'type': 'multiple_choice',
    'forecast_date': '2026-01-13',
    'resolution_date': '2026-02-01',
    'final_forecast': final_forecast,
    'key_factors': {
        'prior_winner_advantage': 'Gordy Haab won 2024, strong precedent',
        'vote_splitting': 'Wilbert Roget II nominated twice, votes split',
        'academy_preference': 'Strong preference for orchestral Williams-style',
        'wintory_streak': 'Austin Wintory 4x nominated, never won new category'
    }
}

with open('/home/claude/grammy_forecast_output.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\nOutput saved to grammy_forecast_output.json")
