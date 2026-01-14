# AI Industry Layoffs Forecast
## Will layoffs.fyi report ≥100 AI industry layoffs between Jan 12 - Mar 13, 2026?

---

# ╔══════════════════════════════════════════════════════════════════╗
# ║                     FINAL FORECAST: 32%                          ║
# ╚══════════════════════════════════════════════════════════════════╝

**Confidence:** Medium  
**Date:** January 12, 2026  
**Close Date:** February 28, 2026  
**Resolution Date:** March 14, 2026

---

## Resolution Criteria (CRITICAL)

This question is about layoffs **IN** the AI industry (companies classified as "AI" on layoffs.fyi), **NOT** about layoffs caused by AI at other companies.

- Filter layoffs.fyi by Industry = "AI"
- Count total people laid off between Jan 12 - Mar 13, 2026
- Threshold: ≥100 people → YES

---

## Base Rate Analysis

### Historical Data (2025)

| Metric | Value | Source |
|--------|-------|--------|
| Total AI industry layoffs 2025 | ~800 | Question background |
| xAI September event | ~500 | TechCrunch, Business Insider |
| Other AI companies | ~300 | Calculated |
| Monthly rate (ex-xAI) | ~25 | 300/12 |

### Expected in 60-Day Window

| Scenario | Expected Layoffs | P(≥100) |
|----------|------------------|---------|
| Full 2025 rate (incl. xAI) | 131 | ~99% |
| Ex-xAI rate only | 49 | ~0% |
| **Monte Carlo (lumpy model)** | **63 (median)** | **~25%** |

**Key insight:** The distribution is LUMPY, not uniform. Without a "big event," we expect 40-70 layoffs. With one big event, we could easily exceed 100.

---

## Quantitative Model Results

### Monte Carlo Simulation (n=100,000)

**Model assumptions:**
- Base rate: 30 people/month (Q1 adjusted, Poisson)
- Big event probability: 25% (one 50-500 person event in Q1)
- Big event size: 60% chance of 50-150, 40% chance of 150-500

**Results:**
```
P(≥100) = 25.0%
Mean: 107.6
Median: 63.0
90% CI: [49, 383]
```

### Sensitivity Analysis

| Scenario | P(≥100) |
|----------|---------|
| Pessimistic (quiet period) | 7% |
| Base case | 16% |
| Q1 seasonal boost | 24% |
| Active period | 26% |

---

## Community Forecasts

| Forecaster | Estimate | Reasoning |
|------------|----------|-----------|
| Rgoger7 | 70% | Low threshold, lumpy batches |
| ksurapaneni | 25% | Historical base rate |
| SandroAVL | 20% | Monte Carlo, growth mode for frontier labs |
| **Average** | **38%** | |

**Note:** Wide disagreement suggests high uncertainty. Rgoger7 appears to be an outlier.

---

## Ensemble Calculation

| Model | Estimate | Weight | Contribution |
|-------|----------|--------|--------------|
| Monte Carlo (Q1 adjusted) | 25% | 0.35 | 8.8% |
| ksurapaneni base rate | 25% | 0.20 | 5.0% |
| Q1-adjusted base rate | 29% | 0.15 | 4.3% |
| SandroAVL Monte Carlo | 20% | 0.15 | 3.0% |
| Rgoger7 | 70% | 0.15 | 10.5% |
| **TOTAL** | | | **31.6%** |

**Rounded final estimate: 32%**

---

## Key Factors

### Factors INCREASING Probability (+8%)

| Factor | Adjustment | Reasoning |
|--------|------------|-----------|
| Low threshold | +2% | Only 100 people; one medium event hits it |
| Q1 seasonality | +3% | Companies restructure after holidays |
| Lumpy distribution | +2% | Single event can tip outcome |
| AI bubble concerns | +1% | Some startups may struggle |

### Factors DECREASING Probability (-5%)

| Factor | Adjustment | Reasoning |
|--------|------------|-----------|
| Frontier labs in growth | -3% | OpenAI, Anthropic, Google hiring |
| 0 AI layoffs YTD 2026 | -1% | Quiet start to year |
| xAI event non-repeatable | -1% | Was a strategic pivot, not distress |

---

## Key Uncertainties

**The question really comes down to: Will there be at least one significant layoff event at an AI company?**

| Scenario | Probability | Outcome |
|----------|-------------|---------|
| No big event | 75% | ~50 layoffs → **NO** |
| One medium event (50-150) | 15% | ~100-150 → **Could go either way** |
| One large event (150+) | 10% | ~200+ → **YES** |

### Companies to Watch

| Company | Risk Level | Notes |
|---------|------------|-------|
| Stability AI | Medium-High | Financial struggles, leadership changes |
| Scale AI | Medium | Already cut 14% in July 2025 |
| Character.AI | Medium | Post-Google talent acquisition |
| AI startups (various) | Medium | Runway concerns |
| OpenAI, Anthropic | Low | Growth mode |
| xAI | Low | Already restructured in Sept 2025 |

---

## Pre-Mortem Analysis

**Assume my forecast is WRONG. Why?**

1. **I'm too low:**
   - Major AI company announces surprise restructuring
   - AI funding crunch hits multiple startups
   - Unknown struggling AI company shuts down
   - Q1 seasonality stronger than I estimated

2. **I'm too high:**
   - AI industry remains in growth mode throughout Q1
   - No single company has a major layoff event
   - Layoffs.fyi classification is narrower than I assumed

---

## Update Triggers

| Event | New Estimate |
|-------|--------------|
| Any AI company announces 30+ layoffs | → 50% |
| Major AI company restructuring | → 65% |
| By Feb 15 with <30 cumulative | → 25% |
| AI funding crunch news | → +10% |
| Stability AI shutdown/major cuts | → +15% |
| February ends with <50 cumulative | → 20% |

---

## Monitoring Plan

### Weekly Checks
- [ ] layoffs.fyi AI industry filter
- [ ] TechCrunch layoffs tracker
- [ ] AI startup news (TechCrunch, The Information)

### Sources
- layoffs.fyi (resolution source)
- trueup.io/layoffs
- TechCrunch tech layoffs tracker

---

## Validation Checklist

- [x] Probability between 5-95%? ✓ (32%)
- [x] Within reasonable range of community? ✓ (38% avg)
- [x] Model accounts for lumpy distribution? ✓ (Monte Carlo)
- [x] Considered Q1 seasonality? ✓ (adjusted upward)
- [x] Checked current 2026 data? ✓ (0 YTD)
- [x] Identified key uncertainty? ✓ (big event probability)

---

## Summary

**Final Forecast: 32%**

The key insight is that AI industry layoffs on layoffs.fyi are **lumpy**, not uniform. In 2025, xAI's 500-person layoff in September accounted for ~62% of all AI industry layoffs. Without such a "big event," we'd expect only 40-70 layoffs in a 60-day window—well below the 100 threshold.

The question is essentially: **What's the probability of at least one significant layoff event (50+ people) at an AI company in Q1 2026?**

Given:
- Frontier AI labs (OpenAI, Anthropic) are in growth mode
- Q1 is peak layoff season
- Some AI startups may struggle with runway
- The threshold is relatively low (100 people)

I estimate a 32% probability of YES, slightly higher than the quantitative base rate (~25%) to account for Q1 seasonality and the low threshold.

---

*Analysis conducted: January 12, 2026*
*Model: Monte Carlo simulation with lumpy event modeling*
*Sources: layoffs.fyi, TechCrunch, trueup.io, community forecasts*
