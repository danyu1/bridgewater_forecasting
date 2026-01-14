# Bridgewater Open Forecasting Tournament
## Complete Step-by-Step Pipeline v3.0

**Tournament Dates:** Official scoring begins January 12, 2026  
**Key insight:** Not every question needs Monte Carlo. Be realistic about which methods apply.

---

# QUICK START: THE 5 MODELS (CORRECTED)

These are your **distinct, non-redundant** estimation methods:

| Model | What It Is | Always Use? | Weight |
|-------|------------|-------------|--------|
| **Base Rate** | Historical frequency in reference class | ✅ YES | 0.30 |
| **Structural Model** | Fermi decomposition OR simulation (when applicable) | When question decomposes | 0.25 |
| **Statistical Model** | ML, regression, time series (when data exists) | When you have data | 0.20 |
| **Crowd/Market** | Community median, prediction markets | When available | 0.25 |

**REMOVED (were redundant):**
- ~~"Adjusted estimate"~~ → This is just base rate + adjustments, not separate
- ~~"Gut check / Intuition"~~ → This informs your weights, not a separate estimate

---

# THE REALISTIC PIPELINE

## For EVERY Question (Tier 1 - Always Do This)

```
┌─────────────────────────────────────────────────────────────┐
│  MINIMUM VIABLE PIPELINE (works for any question)          │
│                                                             │
│  1. INTAKE (5 min)                                          │
│     → Read resolution criteria carefully                    │
│     → Identify question type                                │
│                                                             │
│  2. BASE RATE (15 min)                                      │
│     → Find reference class                                  │
│     → Calculate: successes / total opportunities            │
│     → Document source                                       │
│                                                             │
│  3. EVIDENCE ADJUSTMENT (10 min)                            │
│     → List factors that push UP from base rate              │
│     → List factors that push DOWN from base rate            │
│     → Apply Bayesian reasoning                              │
│                                                             │
│  4. EXTERNAL SIGNALS (10 min)                               │
│     → Check Metaculus community median                      │
│     → Check prediction markets if they exist                │
│     → Search recent news                                    │
│                                                             │
│  5. COMBINE (5 min)                                         │
│     → Weighted average of available estimates               │
│                                                             │
│  6. VALIDATE (10 min)                                       │
│     → Pre-mortem: "Why might I be wrong?"                   │
│     → Sanity checks                                         │
│                                                             │
│  7. SUBMIT (5 min)                                          │
│     → Log in tracker, submit to Metaculus                   │
│     → Set update triggers                                   │
│                                                             │
│  TOTAL: ~60 minutes                                         │
└─────────────────────────────────────────────────────────────┘
```

## Additional Methods (Tier 2 - When Applicable)

```
┌─────────────────────────────────────────────────────────────┐
│  ADD THESE WHEN THE QUESTION STRUCTURE ALLOWS               │
│                                                             │
│  FERMI DECOMPOSITION (add 15 min)                           │
│     → Use when: Question involves multiple steps/components │
│     → Example: "Will X AND Y AND Z all happen?"             │
│     → Break into: P(A) × P(B|A) × P(C|A,B)                  │
│                                                             │
│  MONTE CARLO SIMULATION (add 15 min)                        │
│     → Use when: Can estimate uncertainty on components      │
│     → Same as Fermi, but with probability distributions     │
│     → Gives you confidence intervals                        │
│                                                             │
│  REFERENCE CLASS WITH FEATURES (add 15 min)                 │
│     → Use when: Have historical cases with measurable       │
│       features similar to your question                     │
│     → Weight by similarity to current case                  │
│                                                             │
│  TIME SERIES (add 10 min)                                   │
│     → Use when: Forecasting a NUMERIC value with history    │
│     → Example: GDP growth, stock prices, temperatures       │
└─────────────────────────────────────────────────────────────┘
```

---

# STEP-BY-STEP PROTOCOL

## ⏱️ STEP 1: INTAKE (5 minutes)

**Read the question THREE times:**
- First: Get the gist
- Second: Find EXACT resolution criteria
- Third: Identify edge cases

**Document:**
```
□ What triggers YES resolution?
□ What triggers NO resolution?  
□ Resolution source?
□ Close date?
□ Edge cases / ambiguities?
```

**Classify question type:**
- Binary → Single probability
- Continuous → Distribution (percentiles)
- Multiple Choice → Probabilities for each option
- Conditional → P(Y|X), assume X is true

---

## ⏱️ STEP 2: BASE RATE (15 minutes)

**This is the most important step.** Research shows "comparison classes" (base rates) was the ONLY training element significantly correlated with better forecasts.

### 2.1 Define Reference Class

Ask: "What category of events is this an example of?"

**Be specific.** Narrow > Broad.

### 2.2 Calculate Base Rate

```
Base Rate = (# times this type of event occurred) / (# opportunities)
```

### 2.3 Document

```
Reference class: _______________________
Base rate: _____%
Sample size: n = ____
Source: _______________________
```

### 2.4 Data Sources

| Domain | Sources |
|--------|---------|
| Politics | FiveThirtyEight, Wikipedia election data |
| Economics | FRED, World Bank, IMF |
| Science/Tech | Clinical trial databases, company track records |
| Business | SEC filings, deal databases |
| General | Our World in Data, Statista |

---

## ⏱️ STEP 3: CAN I USE STRUCTURAL MODELS? (Decision Point)

**Ask yourself:**

```
□ Can this question be broken into sub-components?
  → If YES: Use Fermi decomposition (go to 3A)
  → If NO: Skip to Step 4

□ Can I estimate uncertainty on those components?
  → If YES: Add Monte Carlo simulation (go to 3B)
  → If NO: Just use Fermi point estimates
```

### 3A: FERMI DECOMPOSITION (when applicable)

**Break into components:**

Example: "Will SpaceX land Starship on Mars by 2030?"

```
P(success) = P(dev ready) × P(launch|ready) × P(transit|launch) × P(land|transit)
```

**Estimate each:**

| Component | Low | Mid | High |
|-----------|-----|-----|------|
| Dev ready by 2029 | 30% | 45% | 60% |
| Launch given ready | 60% | 75% | 85% |
| Transit success | 70% | 80% | 90% |
| Landing success | 35% | 50% | 65% |

**Combine:** 0.45 × 0.75 × 0.80 × 0.50 = **13.5%**

### 3B: MONTE CARLO (when applicable)

```python
from quantitative_forecasting import fermi_decomposition

components = [
    {'name': 'dev_ready', 'low': 0.30, 'mid': 0.45, 'high': 0.60},
    {'name': 'launch', 'low': 0.60, 'mid': 0.75, 'high': 0.85},
    {'name': 'transit', 'low': 0.70, 'mid': 0.80, 'high': 0.90},
    {'name': 'landing', 'low': 0.35, 'mid': 0.50, 'high': 0.65}
]

result = fermi_decomposition(components, combination='chain')
# Returns estimate with confidence interval
```

**Output:** Structural estimate = ___% [CI: ___% - ___%]

---

## ⏱️ STEP 4: EVIDENCE ADJUSTMENT (10 minutes)

**List factors that move you AWAY from base rate:**

| Factor | Direction | Strength | Adjustment |
|--------|-----------|----------|------------|
| __________ | ↑ | Weak/Mod/Strong | +___% |
| __________ | ↑ | Weak/Mod/Strong | +___% |
| __________ | ↓ | Weak/Mod/Strong | -___% |
| __________ | ↓ | Weak/Mod/Strong | -___% |

**Adjustment guidelines:**
- Weak evidence: ±1-5%
- Moderate evidence: ±5-15%
- Strong evidence: ±15-25%

**To justify moving from base rate, you need:**
1. Evidence that the usual process will FAIL
2. Evidence that a different outcome will result

**Calculate:** Adjusted = Base rate + sum(adjustments) = ___%

---

## ⏱️ STEP 5: EXTERNAL SIGNALS (10 minutes)

### Check community/markets:

| Source | Value | Date |
|--------|-------|------|
| Metaculus community median | ___% | ____ |
| Prediction market (if exists) | ___% | ____ |
| Expert consensus (if found) | ___% | ____ |

### Recent news impact:
- Direction: ↑ / ↓ / Neutral
- Magnitude: Small / Medium / Large

---

## ⏱️ STEP 6: BUILD ENSEMBLE (5 minutes)

### Combine your AVAILABLE estimates:

**If you used structural models:**

| Model | Estimate | Weight |
|-------|----------|--------|
| Base Rate | ___% | 0.30 |
| Fermi/Monte Carlo | ___% | 0.25 |
| Crowd/Market | ___% | 0.25 |
| Adjusted (from evidence) | ___% | 0.20 |

**If structural models didn't apply:**

| Model | Estimate | Weight |
|-------|----------|--------|
| Base Rate | ___% | 0.40 |
| Adjusted (from evidence) | ___% | 0.30 |
| Crowd/Market | ___% | 0.30 |

**Calculate weighted average:**

```
Final = Σ (estimate × weight) = ___%
```

---

## ⏱️ STEP 7: VALIDATE (10 minutes)

### Pre-Mortem

**Assume you're WRONG. Why?**

```
Reason 1: _________________________________
  → Should I adjust? Y/N  → New estimate: ___%

Reason 2: _________________________________
  → Should I adjust? Y/N  → New estimate: ___%

Reason 3: _________________________________
  → Should I adjust? Y/N  → New estimate: ___%
```

### Sanity Checks

```
□ Is probability between 5% and 95%?
□ Would I bet real money at these odds?
□ If different from community, can I explain why?
□ Did I move >20% from base rate? (Need strong justification)
```

### Final Forecast: ___%

---

## ⏱️ STEP 8: SUBMIT & MONITOR (5 minutes)

### Log in tracker:
- Question ID, title, type
- Final probability
- Base rate used
- Models used
- Key reasoning

### Submit to Metaculus

### Set update triggers:

| Event | New Estimate |
|-------|--------------|
| If _________ happens | → ___% |
| If _________ happens | → ___% |

### Set review schedule:
- < 1 week out: Daily
- 1-4 weeks: Every 2-3 days
- 1-3 months: Weekly
- 3+ months: Bi-weekly

---

# QUESTION TYPE DECISION TREE

## Which methods apply to MY question?

```
START
│
├─► Is this a multi-step process?
│   Examples: "Will X develop AND launch AND succeed?"
│   │
│   ├─► YES → Use Fermi + Monte Carlo
│   └─► NO → Continue
│
├─► Do I have historical data with features?
│   Examples: Elections with polling, M&A deals with characteristics
│   │
│   ├─► YES → Use Reference Class with similarity weighting
│   └─► NO → Continue
│
├─► Am I forecasting a NUMBER over time?
│   Examples: GDP, temperature, prices
│   │
│   ├─► YES → Use Time Series
│   └─► NO → Continue
│
├─► Is there a prediction market or crowd forecast?
│   │
│   ├─► YES → Include in ensemble
│   └─► NO → Continue
│
└─► DEFAULT: Base Rate + Evidence Adjustment + Crowd
    This is totally fine! Most questions are like this.
```

---

# EXAMPLES BY QUESTION TYPE

## Example A: Multi-Step Technical Question ✅ Full Pipeline

**Question:** "Will SpaceX achieve orbital refueling by July 2026?"

**Methods that apply:**
- ✅ Base Rate (SpaceX timeline accuracy)
- ✅ Fermi (decompose into milestones)
- ✅ Monte Carlo (uncertainty on milestones)
- ✅ Crowd (check community)

**Weights:** 0.30 base + 0.25 structural + 0.25 crowd + 0.20 adjusted

---

## Example B: Single Event, Hard to Decompose ⚠️ Limited Pipeline

**Question:** "Will Russia-Ukraine ceasefire happen by end of 2026?"

**Methods that apply:**
- ✅ Base Rate (historical conflict resolutions)
- ❌ Fermi (components aren't independent)
- ❌ Monte Carlo (can't estimate distributions)
- ✅ Crowd (check markets/community)

**Weights:** 0.40 base + 0.30 adjusted + 0.30 crowd

---

## Example C: Numeric Forecast ✅ Time Series

**Question:** "What will US CPI inflation be in December 2026?"

**Methods that apply:**
- ✅ Base Rate (historical inflation ranges)
- ✅ Time Series (historical trend)
- ✅ Crowd (market expectations, TIPS spreads)
- ❌ Fermi (not a multi-step event)

**Weights:** 0.25 base + 0.35 time series + 0.25 market + 0.15 adjusted

---

# HONEST ASSESSMENT

## When Quantitative Methods Help Most:
- Technical/scientific questions with clear milestones
- Questions with rich historical data
- Numeric forecasts with time series
- Multi-step processes

## When Quantitative Methods Help Least:
- One-off political/social events
- Questions about human decisions
- Novel situations with no precedent
- Short-term event timing

## The Minimum Is Still Quantitative:

Even for "hard to model" questions, you're still doing math:
- Base rate = counting historical events
- Bayesian update = likelihood ratios
- Ensemble = weighted average

**Don't fake precision with Monte Carlo when base rate + Bayes is more honest.**

---

# CALIBRATION TRAINING

Before the tournament, complete calibration training:

| Resource | URL |
|----------|-----|
| Calibrate Your Judgment | https://programs.clearerthinking.org/calibrate_your_judgment.html |
| Metaculus Tutorials | https://www.metaculus.com/tutorials/ |

**Goal:** 100+ practice questions to calibrate your confidence levels.

---

# FINAL CHECKLIST

```
For every question:

□ INTAKE
  □ Understood resolution criteria
  □ Identified question type

□ BASE RATE
  □ Found reference class
  □ Calculated rate
  □ Documented source

□ STRUCTURAL MODEL (if applicable)
  □ Decomposed into components
  □ Estimated each component
  □ Combined appropriately

□ EVIDENCE
  □ Listed factors up/down
  □ Applied adjustments

□ EXTERNAL
  □ Checked community
  □ Checked markets (if exist)

□ ENSEMBLE
  □ Combined available estimates
  □ Used appropriate weights

□ VALIDATE
  □ Pre-mortem complete
  □ Sanity checks passed

□ SUBMIT
  □ Logged in tracker
  □ Submitted to Metaculus
  □ Set triggers and review schedule
```

---

*Pipeline v3.0 - Updated January 11, 2026*
*Key changes: Removed redundant models, added method applicability guidance*
