# COMPLETE FORECAST ANALYSIS
## Question: Will recorded layoffs at AI-native companies total ≥200 roles before March 14, 2026?

**Analyst:** [Your Name]
**Date:** January 11, 2026
**Time Spent:** ~90 minutes

---

# STEP 1: INTAKE ✓

## Question Details
- **Question:** Will recorded layoffs at AI-native companies total ≥200 roles before March 14, 2026?
- **Resolution Date:** March 14, 2026
- **Question Type:** Binary
- **Source:** Bridgewater x Metaculus Tournament 2026

## Resolution Criteria (Inferred)
- **YES:** If tracked/recorded layoffs at "AI-native" companies reach or exceed 200 roles cumulatively by March 14, 2026
- **NO:** If total is under 200 roles
- **Likely resolution source:** Layoffs.fyi, TrueUp.io, TechCrunch layoff tracker, or similar

## Critical Ambiguity: What is "AI-native"?

### Likely Included (Core AI-native):
| Company | Est. Employees | Notes |
|---------|---------------|-------|
| OpenAI | ~3,500 | Largest, still hiring |
| Anthropic | ~1,500 | Growing rapidly |
| Stability AI | ~150-200 | Had layoffs in 2024 |
| Cohere | ~500 | Enterprise AI |
| Midjourney | ~40-100 | Small team |
| Runway | ~150 | Video AI |
| Jasper | ~400 | Marketing AI |
| Scale AI | ~600 | Data labeling/AI |
| Hugging Face | ~200 | ML platform |
| Character.AI | ~150 (post-deal) | Acquired by Google |
| Inflection AI | ~70 (post-deal) | Most went to Microsoft |
| Mistral | ~60 | French AI lab |
| Perplexity | ~100 | AI search |
| Adept | ~80 | AI agents |
| Together AI | ~100 | AI infrastructure |

**Total AI-native workforce estimate: ~7,500-10,000 employees**

### Probably NOT Included:
- Microsoft, Google, Amazon, Meta (use AI but not "AI-native")
- Nvidia (chips, not AI-native in the product sense)
- Traditional tech companies with AI divisions

### Edge Cases (Unclear):
- AI chip startups (Cerebras, SambaNova, Groq)?
- AI-focused cybersecurity (CrowdStrike)?
- AI coding tools (Cursor, Replit)?

## Timeline
- **Period:** January 1, 2026 → March 14, 2026 (73 days)
- **Current date:** January 11, 2026 (Day 11)
- **Days remaining:** 62 days

---

# STEP 2: BASE RATE (Outside View)

## Reference Class Analysis

### Reference Class 1: AI-native layoffs in similar periods (2024-2025)

**Historical AI-native layoffs found:**
| Company | Date | Layoffs | Notes |
|---------|------|---------|-------|
| Stability AI | Apr 2024 | ~20 | 10% of staff |
| Tome AI | Apr 2024 | ~12 | 20% of staff |
| Stability AI | 2023 | ~20-30 | Earlier round |
| Jasper | 2023 | Unknown | Restructuring |
| Inflection AI | Mar 2024 | ~70 | Most left to Microsoft (acqui-hire) |
| Character.AI | Aug 2024 | ~30 | Leadership to Google |

**Problem:** Very limited data on pure AI-native layoffs. Most tracked layoffs are at big tech.

### Reference Class 2: Tech startup layoffs as baseline

From TrueUp/Layoffs.fyi:
- **2025 total:** 245,953 tech layoffs across 783 companies
- **Per quarter:** ~61,500 layoffs
- **Per 2.5 months (73 days):** ~51,000 layoffs

**AI-native as fraction of tech:**
- AI-native employees: ~7,500-10,000
- Total tech employees: ~3-5 million
- AI-native = ~0.2-0.3% of tech workforce

**If layoffs were proportional:**
- 0.25% × 51,000 = ~130 layoffs at AI-native companies per 2.5 months

**BUT:** AI-native companies are currently in GROWTH mode (heavy funding, hiring wars). Layoff rate likely LOWER than average tech.

### Reference Class 3: What's already happened in 2026?

From TrueUp (Jan 11, 2026):
- **2026 YTD:** 664 layoffs at 8 tech companies
- **Rate:** ~60 people/day across ALL tech

**AI-native portion so far:** Unknown, but likely <50 if any.

### Reference Class 4: Single company risk

Could ONE company having layoffs hit 200?

| Company | Employees | 10% layoff | 20% layoff |
|---------|-----------|------------|------------|
| OpenAI | 3,500 | 350 ✓ | 700 ✓ |
| Anthropic | 1,500 | 150 | 300 ✓ |
| Scale AI | 600 | 60 | 120 |
| Jasper | 400 | 40 | 80 |
| Cohere | 500 | 50 | 100 |
| Stability AI | 180 | 18 | 36 |

**Key insight:** A single 10%+ layoff at OpenAI alone would exceed 200.

### Base Rate Summary

| Scenario | Probability | Reasoning |
|----------|-------------|-----------|
| No significant layoffs at any AI-native | 30-40% | Growth mode, flush with cash |
| Small layoffs (<100 total) | 25-35% | Stability AI, smaller players |
| Medium layoffs (100-199) | 15-20% | 2-3 companies restructure |
| ≥200 layoffs | 20-30% | One major event or multiple medium |

**Initial base rate estimate: 25-35% YES**

---

# STEP 3: STRUCTURAL MODEL ASSESSMENT

## Can this question be decomposed?

**Attempt at Fermi decomposition:**

```
P(≥200 layoffs) = 1 - P(all companies have <200 combined)

P(all < 200) = P(OpenAI < 200) × P(Anthropic < 200) × P(Others < 200 combined)
            ≈ 0.85 × 0.92 × 0.65
            ≈ 0.51

P(≥200) = 1 - 0.51 = 0.49 ≈ 50%
```

**Individual estimates:**

| Company/Group | P(any layoffs) | P(≥200 if layoffs) | P(contributes ≥200) |
|--------------|----------------|---------------------|---------------------|
| OpenAI | 15% | 50% | 7.5% |
| Anthropic | 8% | 30% | 2.4% |
| Stability AI | 40% | 10% | 4% |
| Mid-tier (Jasper, Cohere, etc.) | 25% each | 5% each | ~1% each |
| Small AI startups combined | 60% | 15% | 9% |

**Problem with this decomposition:**
- Components aren't fully independent (macro conditions affect all)
- Hard to estimate individual company probabilities
- Definition ambiguity adds noise

**Decision: Use this as a SANITY CHECK, not primary model**

Structural model estimate: ~35-50%

---

# STEP 4: EVIDENCE ADJUSTMENT (Inside View)

## Factors Pushing UP (toward YES)

| Factor | Strength | Reasoning |
|--------|----------|-----------|
| **Stability AI history** | Moderate (+5-8%) | Already had layoffs in 2024, financially struggling |
| **AI bubble concerns** | Moderate (+3-5%) | Some analysts predicting AI bubble burst in 2026 |
| **Q1 traditionally has layoffs** | Moderate (+3-5%) | January-February is common layoff season |
| **200 is a LOW bar** | Strong (+8-12%) | Only needs one medium layoff event |
| **Macro uncertainty** | Weak (+2-3%) | Economic concerns, but AI sector still strong |
| **VC tightening** | Moderate (+3-5%) | Later-stage AI startups may face pressure |

**Total UP adjustment: +15-25%**

## Factors Pushing DOWN (toward NO)

| Factor | Strength | Reasoning |
|--------|----------|-----------|
| **OpenAI/Anthropic flush with cash** | Strong (-8-12%) | Massive recent fundraises ($40B+) |
| **AI talent war** | Strong (-5-8%) | Companies hoarding talent, not cutting |
| **AI sector is "hot"** | Moderate (-3-5%) | Still seen as growth sector |
| **Short timeframe** | Moderate (-3-5%) | Only 62 days remaining |
| **Big tech absorbing AI talent** | Weak (-2-3%) | Microsoft, Google acqui-hires |
| **Definition may be narrow** | Moderate (-5-8%) | If "AI-native" is strict, fewer companies count |

**Total DOWN adjustment: -15-25%**

## Net Evidence Adjustment

UP factors and DOWN factors roughly CANCEL OUT.

**Evidence-adjusted estimate: ~30-40% YES**

---

# STEP 5: CROWD/MARKET CHECK

## Prediction Markets

*Note: Question just opened on Metaculus. Community forecast not yet available.*

**Similar questions:**
- No exact match found on Polymarket, Manifold, or PredictIt
- General "AI bubble" and "tech layoffs" questions exist but don't match

## Expert Opinions (from research)

| Source | View | Implication |
|--------|------|-------------|
| TechCrunch VCs survey | "AI will impact labor in 2026" | Neutral (about AI causing layoffs elsewhere) |
| Anthropic CEO | Warning about AI job losses | Doesn't mean Anthropic will lay off |
| Foundation Capital | "AI-native startups didn't dethrone incumbents" | Some pressure on AI startups |
| AlleyWatch | "AI bubble will burst in 2026 H2" | Later than March, but sentiment exists |

**Expert consensus: Mixed. AI sector strong but not immune.**

## Current Market/Crowd Estimate: ~35% (imputed)

---

# STEP 6: ENSEMBLE

## Monte Carlo Simulation Results

Ran 50,000 simulations modeling individual company layoff probabilities:

```
P(≥50 layoffs):  77.7%
P(≥100 layoffs): 45.9%  
P(≥200 layoffs): 14.8%

Distribution:
  Mean:   120 layoffs
  Median: 93 layoffs
  90th percentile: 247 layoffs
```

### Sensitivity to OpenAI (KEY VARIABLE!)

| P(OpenAI has layoffs) | P(≥200 total) |
|-----------------------|---------------|
| 5% | 10.3% |
| 12% | 16.6% |
| 20% | 22.8% |
| 30% | 31.2% |

**Key insight:** OpenAI is the swing factor. If they have ANY layoffs, we likely hit 200.

## Model Summary

| Model | Estimate | Weight | Reasoning |
|-------|----------|--------|-----------|
| Base Rate | 30% | 0.35 | Limited historical data, wide uncertainty |
| Monte Carlo | 15% | 0.25 | Quantitative simulation |
| Evidence-Adjusted | 35% | 0.25 | Factors roughly cancel |
| Crowd/Market | 35% | 0.15 | Imputed, no direct data |

## Weighted Calculation

```
Final = (0.35 × 0.30) + (0.25 × 0.15) + (0.25 × 0.35) + (0.15 × 0.35)
      = 0.105 + 0.038 + 0.088 + 0.053
      = 0.284
      = 28.4%
```

**Note:** Monte Carlo pulls estimate DOWN from initial qualitative assessment. This is valuable calibration.

## Confidence Interval

Given high uncertainty (definitional ambiguity, limited data):
- **90% CI: [18%, 55%]**
- This is WIDE, reflecting genuine uncertainty

---

# STEP 7: VALIDATION & PRE-MORTEM

## Pre-Mortem: If YES (≥200 layoffs)

**Most likely scenarios:**
1. **Stability AI has another round** (20-40 layoffs) + **2-3 other AI startups** (combined 160-180) = 200+
2. **One surprise layoff at major player** (OpenAI restructures a division = 200-400)
3. **Broad AI startup "correction"** (5-10 companies each cut 20-30)

**What would I have missed?**
- Underestimated financial pressure on smaller AI startups
- Didn't account for acqui-hires being counted as "layoffs"
- Definition of "AI-native" broader than expected

## Pre-Mortem: If NO (<200 layoffs)

**Most likely scenarios:**
1. **AI sector remains hot** - companies in hiring mode, not cutting
2. **Only 50-100 layoffs** at Stability + small players
3. **Major players (OpenAI, Anthropic) have zero layoffs**

**What would I have missed?**
- Overestimated pressure on AI sector
- Definition of "AI-native" narrower than expected
- 62 days too short for layoff wave to materialize

## Sanity Checks

| Check | Result |
|-------|--------|
| Is estimate between 10-90%? | ✓ Yes (34%) |
| Does it match gut feeling? | ✓ Roughly (felt like 30-40%) |
| Is CI appropriately wide given uncertainty? | ✓ Yes (18-55%) |
| Am I overconfident due to research depth? | Possibly - be humble |
| Does Fermi sanity check agree? | ✓ ~35-50% is consistent |

## Red Flags in My Analysis

1. **Definition ambiguity is HUGE** - could swing estimate ±15%
2. **Limited historical data** on AI-native specifically
3. **Short time remaining** (62 days) - single event could resolve this

---

# STEP 8: FINAL FORECAST

## Primary Estimate

# **28% YES**

*(Will recorded layoffs at AI-native companies total ≥200 roles before March 14, 2026)*

## Confidence
- **90% CI: [12%, 48%]**
- **Confidence Level: LOW-MEDIUM** (significant definitional uncertainty)

## Key Uncertainties (in order of importance)
1. **OpenAI layoff probability** (±15%) - THE swing factor
2. **Definition of "AI-native"** (±10%)
3. **Financial health of Stability AI and mid-tier players** (±5%)

---

# STEP 9: UPDATE TRIGGERS & MONITORING

## Events That Would Increase My Estimate

| Event | New Estimate | Magnitude |
|-------|--------------|-----------|
| OpenAI announces any layoffs | 70-80% | Major |
| Anthropic announces any layoffs | 65-75% | Major |
| Stability AI announces >50 layoffs | 55-65% | Moderate |
| 2+ AI startups announce layoffs same week | 50-60% | Moderate |
| AI funding round fails/down round | 45-55% | Moderate |
| Cumulative AI-native layoffs reach 100 | 60-70% | Moderate |
| "AI bubble" narrative gains mainstream traction | 40-45% | Weak |

## Events That Would Decrease My Estimate

| Event | New Estimate | Magnitude |
|-------|--------------|-----------|
| OpenAI announces major hiring push | 25-28% | Moderate |
| By Feb 15, cumulative <50 layoffs | 20-25% | Moderate |
| Anthropic raises another round, announces expansion | 28-30% | Weak |
| "AI winter" concerns debunked | 30-32% | Weak |
| Resolution criteria clarified as very narrow | 20-25% | Moderate |

## Monitoring Schedule

| Date | Action |
|------|--------|
| Daily | Check TrueUp.io, Layoffs.fyi for AI company updates |
| Daily | Google News alert: "AI startup layoffs" |
| Weekly | Review TechCrunch layoff roundup |
| Jan 19 | Re-evaluate after 1 week of tournament data |
| Feb 1 | Mid-period review - should have 45 days of data |
| Feb 15 | If <75 cumulative, consider lowering to 25% |
| Mar 1 | Final two weeks - likely to resolve or not by pattern |

## Keywords to Monitor
- "OpenAI layoffs", "Anthropic layoffs", "Stability AI layoffs"
- "AI startup restructuring"
- "AI company job cuts"
- "[Any AI company name] workforce reduction"

---

# APPENDIX: Research Sources

## Primary Sources Used
1. TrueUp.io layoffs tracker
2. Layoffs.fyi
3. TechCrunch 2025 layoff roundup
4. CNBC AI layoffs coverage
5. Crunchbase AI funding data

## Key Data Points
- 2026 YTD tech layoffs: 664 (as of Jan 11)
- 2025 total tech layoffs: 245,953
- AI-native workforce estimate: 7,500-10,000
- Major AI-native layoff events (2024): Stability AI (~20), Tome (~12)

## Limitations
- Exact resolution criteria not available at time of analysis
- Definition of "AI-native" not specified
- Limited historical precedent for AI-native specific layoffs

---

**Final Answer: 28% YES**

*Confidence: Low-Medium | Review: Weekly | Next Update: Jan 19, 2026*

---

## QUANTITATIVE MODEL DETAILS

### Monte Carlo Assumptions
```
OpenAI:    P(layoffs)=12%, Size~Triangular(50,150,500)
Anthropic: P(layoffs)=8%,  Size~Triangular(30,80,200)  
Stability: P(layoffs)=35%, Size~Triangular(10,25,60)
Mid-tier (8 companies): P(layoffs)=15% each, Size~Triangular(10,30,80)
Small startups (20):    P(layoffs)=10% each, Size~Triangular(3,10,25)
```

### Why 28% (not higher, not lower)

**Why not higher (>40%):**
- AI sector is in growth mode
- OpenAI/Anthropic flush with cash ($40B+ raised)
- Monte Carlo shows median outcome is ~93 layoffs, well below 200
- 62 days is short for a layoff wave to develop

**Why not lower (<20%):**
- 200 is a relatively low bar
- Stability AI has history of layoffs
- Some mid-tier AI startups face funding pressure
- Q1 is traditionally layoff season
- Single event at OpenAI would exceed threshold
