# WHICH FORECASTING METHOD SHOULD I USE?
## A Realistic Decision Guide

---

## The Honest Truth

**Not every question can be Monte Carlo'd.** Here's when each method actually works:

---

## DECISION TREE

```
START: What kind of question is this?
│
├─► Can I break it into independent sub-components?
│   │
│   ├─► YES → Use FERMI DECOMPOSITION + MONTE CARLO
│   │         Example: "Will X launch AND succeed AND land?"
│   │         P(success) = P(launch) × P(success|launch) × P(land|success)
│   │
│   └─► NO → Continue below
│
├─► Do I have historical data with similar cases?
│   │
│   ├─► YES, with features → Use LOGISTIC REGRESSION or REFERENCE CLASS
│   │         Example: "Will this M&A deal close?"
│   │         Historical deals with features: size, sector, regulatory
│   │
│   ├─► YES, simple count → Use BASE RATE only
│   │         Example: "Will incumbent win?" → Historical incumbent win rate
│   │
│   └─► NO → Continue below
│
├─► Is this a time-series/quantity question?
│   │
│   ├─► YES → Use TIME SERIES FORECASTING
│   │         Example: "What will GDP be in Q3?"
│   │
│   └─► NO → Continue below
│
├─► Is there a prediction market or crowd forecast?
│   │
│   ├─► YES → Include CROWD/MARKET in ensemble
│   │
│   └─► NO → Continue below
│
└─► FALLBACK: Base Rate + Bayesian Updates only
              This is fine! Many questions are like this.
```

---

## METHOD APPLICABILITY BY QUESTION TYPE

### ✅ METHODS THAT (ALMOST) ALWAYS WORK

| Method | When It Works | Effort |
|--------|---------------|--------|
| **Base Rate** | Almost always - find ANY reference class | Low |
| **Bayesian Updating** | Whenever you get new evidence | Low |
| **Crowd/Market** | Whenever others have forecasted | Low |

### ⚠️ METHODS THAT SOMETIMES WORK

| Method | Requirements | Example Questions |
|--------|--------------|-------------------|
| **Fermi Decomposition** | Question decomposes into steps | Multi-step processes, timelines |
| **Monte Carlo** | Can estimate uncertainty on components | Same as Fermi, plus uncertainty |
| **Reference Class with Features** | Historical cases + measurable features | Elections, business outcomes |

### ❌ METHODS THAT RARELY WORK

| Method | Why It Often Fails |
|--------|-------------------|
| **ML Models** | Need lots of structured historical data - rare for forecasting |
| **Time Series** | Only for numeric quantities with history |
| **Complex Simulations** | Garbage in, garbage out - don't fake precision |

---

## REALISTIC EXAMPLES

### Example 1: "Will Russia and Ukraine reach a ceasefire by end of 2026?"

**Can I decompose?** 
- Sort of... but the components aren't independent
- P(both sides want ceasefire) × P(terms agreed) × P(implementation)?
- These are all correlated and hard to estimate separately
- **Verdict: Fermi is WEAK here**

**Do I have historical data?**
- Some comparable conflicts exist
- But each conflict is unique
- **Verdict: Base rate is MODERATE - use broad reference class**

**What actually works:**
```
Models to use:
1. Base Rate: Historical ceasefire rates in similar conflicts (~30%?)
2. Crowd/Market: Check prediction markets
3. Bayesian updates: As news develops

Models to SKIP:
- Monte Carlo (can't reliably estimate components)
- ML (not enough comparable data points)
```

---

### Example 2: "Will SpaceX achieve orbital refueling by July 2026?"

**Can I decompose?**
- YES! Clear technical milestones
- P(Starship reliable) × P(tanker ready) × P(rendezvous works) × P(transfer works)
- **Verdict: Fermi WORKS**

**Historical data?**
- SpaceX track record on timelines
- Historical first-attempt success rates for novel space tech
- **Verdict: Good base rates available**

**What actually works:**
```
Models to use:
1. Base Rate: SpaceX timeline accuracy + space tech first attempts
2. Fermi: Decompose into technical milestones
3. Monte Carlo: Run simulation with uncertainty on each milestone
4. Crowd: Check Metaculus community

Full quantitative pipeline applies here!
```

---

### Example 3: "Will the Fed cut rates in March 2026?"

**Can I decompose?**
- Not really - it's a single committee decision
- **Verdict: Fermi doesn't help**

**Historical data?**
- YES! Fed has long history of rate decisions
- Features: inflation rate, unemployment, prior guidance
- **Verdict: Could use logistic regression IF you have the data**

**What actually works:**
```
Models to use:
1. Base Rate: Historical Fed rate cuts given similar conditions
2. Market: Fed funds futures literally price this
3. Bayesian updates: As economic data releases

Models to SKIP:
- Monte Carlo (nothing to simulate)
- Fermi (doesn't decompose)
```

---

### Example 4: "Will [Specific Person] win [Specific Award] in 2026?"

**Can I decompose?**
- Not meaningfully
- **Verdict: Fermi doesn't help**

**Historical data?**
- Limited - awards are idiosyncratic
- **Verdict: Weak base rates**

**What actually works:**
```
Models to use:
1. Base Rate: Very rough (prior winners' characteristics)
2. Crowd: If others have forecasted
3. Bayesian updates: As nominations/news emerge

This is a LOW-QUANTITATIVE question - and that's okay!
Most of your edge comes from information gathering, not modeling.
```

---

## THE MINIMUM VIABLE QUANTITATIVE PIPELINE

For questions where fancy methods don't apply, you still have:

```
1. BASE RATE (always quantitative)
   - Find reference class
   - Count: successes / total
   - This is a NUMBER

2. BAYESIAN UPDATES (always quantitative)
   - Prior: your base rate
   - Likelihood ratio: how diagnostic is new evidence?
   - Posterior: updated probability
   - This is MATH

3. CROWD/MARKET (when available)
   - Other people's probability estimates
   - This is a NUMBER

4. ENSEMBLE
   - Weighted average of available estimates
   - This is MATH
```

**You don't need Monte Carlo to be quantitative.** Base rates + Bayes + ensemble IS quantitative.

---

## WHEN TO USE EACH METHOD: QUICK REFERENCE

| Question Characteristic | Use This Method |
|------------------------|-----------------|
| Multi-step process | Fermi + Monte Carlo |
| Technical milestones | Fermi + Monte Carlo |
| Historical similar events | Reference Class / Base Rate |
| Prediction market exists | Include market price |
| Forecasting a NUMBER | Time series |
| Rich historical dataset with features | Logistic regression |
| Single event, hard to decompose | Base rate + Bayes + Crowd |
| Completely novel situation | Wide uncertainty, base rate of similar-ish things |

---

## DON'T FAKE PRECISION

**Bad:** "I'll run Monte Carlo with made-up distributions to seem rigorous"

**Good:** "This question doesn't decompose well, so I'm using base rate + crowd + Bayesian updates. My estimate has wide uncertainty."

**The goal is accuracy, not the appearance of sophistication.**

---

## SUMMARY: YOUR REALISTIC TOOLKIT

**Tier 1 - Use on EVERY question:**
- Base rate from reference class
- Bayesian updating as evidence arrives
- Crowd/market signals when available
- Weighted ensemble of estimates

**Tier 2 - Use when question structure allows:**
- Fermi decomposition (multi-step events)
- Monte Carlo simulation (when you can estimate component uncertainty)
- Reference class with similarity weighting (when you have comparable cases)

**Tier 3 - Use rarely, when data permits:**
- Logistic regression (need structured historical data)
- Time series (only for numeric forecasts with history)

Most Metaculus questions will use **Tier 1 + maybe one Tier 2 method.** That's fine!
