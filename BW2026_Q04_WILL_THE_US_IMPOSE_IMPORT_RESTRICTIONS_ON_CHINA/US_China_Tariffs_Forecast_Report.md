# Bridgewater Open Forecasting Tournament
## Comprehensive Forecast Analysis

---

# Question: Will the US impose any new import restriction upon China before March 14, 2026?

**Analysis Date:** January 13, 2026  
**Question Close Date:** March 14, 2026  
**Time Horizon:** ~60 days

---

# ╔═══════════════════════════════════════════════════════════════╗
# ║                     FINAL FORECAST: 42%                        ║
# ╚═══════════════════════════════════════════════════════════════╝

**Confidence:** Medium  
**Community Median:** 38%  
**Divergence from Community:** +4% (within reasonable range)

---

## RESOLUTION CRITERIA (Verbatim)

> This question will resolve as Yes if, before March 14, 2026 ET, the United States announces any new tariff, import quota, or import ban upon China, or harshens existing restrictions, according to credible sources.

**Key Constraints:**
- Must **specifically mention China** (not incidental)
- "Harshens existing restrictions" = increase in tariff rates, tighter quota, expansion of bans, or removal of exemptions
- Export restrictions do NOT count
- Antidumping/countervailing duty (AD/CVD) orders DO qualify (per admin clarification)

---

## CURRENT SITUATION SUMMARY

### US-China Trade Status (as of Jan 13, 2026):
- **1-Year Trade Truce** in effect since November 10, 2025 (Busan Summit deal)
- Current general tariff rate on China: **~47.5%** (down from peak of 145%)
- Section 301 exclusions extended until November 10, 2026
- Maritime/shipbuilding Section 301 actions suspended for 1 year
- China suspended rare earth export controls

### Breaking Developments (past 24 hours):
- **January 12, 2026:** Trump announced 25% tariff on countries doing business with Iran
  - Does NOT directly qualify (doesn't specifically mention China)
  - However, signals willingness to escalate despite truce
  - China has responded with strong rhetoric

### Pending Uncertainties:
- **Supreme Court IEEPA Decision:** Expected any day (possibly this week)
  - Kalshi: 28% chance tariffs survive
  - Polymarket: 25% chance tariffs survive
  - If struck down, administration may reimpose under different authority

---

## BASE RATE ANALYSIS

### Reference Class 1: US-China Trade Actions During Truces (2018-2026)
- During Phase One period (Jan 2020 - Jan 2025): ~3-4 China-specific actions per year
- Monthly probability: ~25-35%
- 2-month probability: **~40-50%**

### Reference Class 2: AD/CVD Orders on China
- US typically issues 30-50 AD/CVD orders per year
- Significant portion target China
- 2-month probability of at least one new China-specific order: **~30-40%**

### Reference Class 3: Trade Actions During Truces Generally
- Historical pattern shows "tighten and relax" cycles
- Formal truces reduce but don't eliminate new actions
- Base rate during truces: **~30-40%**

**Weighted Base Rate: 35%**

---

## MONTE CARLO SIMULATION RESULTS

**Parameters:** n = 100,000 simulations with truce-adjusted probabilities

### Path Contributions to YES Resolution:

| Path | Probability | Description |
|------|-------------|-------------|
| AD/CVD Orders | 25.1% | Routine antidumping/CVD orders on Chinese goods |
| Iran Escalation | 13.3% | Iran tariff evolves to specifically target China |
| SCOTUS Trigger | 12.6% | Court ruling triggers China-specific reimposition |
| Section 301/232 | 11.1% | New investigation leads to China-specific action |
| Trade Tensions | 10.8% | General escalation leads to new restriction |
| Exemption Removal | 7.0% | Section 301 exclusion removed |

**Monte Carlo Point Estimate: 55.2%**

*Note: Monte Carlo naturally gives higher estimates due to multiple independent paths. Weighted appropriately in ensemble.*

---

## EVIDENCE ADJUSTMENT

### Factors Pushing UP from Base Rate:

| Factor | Adjustment | Rationale |
|--------|------------|-----------|
| AD/CVD routine process | +5% | These orders are continuous and specifically target China |
| Iran tariff signal | +4% | Shows willingness to act despite truce |
| Trump unpredictability | +3% | "Tighten and relax" pattern well-documented |
| SCOTUS uncertainty | +4% | Could trigger reimposition under different authority |
| Phase One investigation | +2% | Ongoing Section 301 process could yield action |
| **Total UP** | **+18%** | |

### Factors Pushing DOWN from Base Rate:

| Factor | Adjustment | Rationale |
|--------|------------|-----------|
| 1-year trade truce | -4% | Clear commitment from Busan summit |
| April summit diplomacy | -2% | Trump scheduled to visit Beijing |
| Midterm sensitivity | -1% | Administration aware of inflation concerns |
| China rare earth leverage | -1% | Deterrent to unilateral escalation |
| **Total DOWN** | **-8%** | |

**Evidence-Adjusted Estimate: 35% + 18% - 8% = 45%**

---

## EXTERNAL SIGNALS

### Prediction Markets/Forecasting Platforms:

| Source | Estimate | Notes |
|--------|----------|-------|
| **Metaculus Community** | 38% | 379 forecasters, stable over past day |
| **Polymarket (related)** | 25% | Chance IEEPA tariffs survive SCOTUS |
| **Kalshi (related)** | 28% | Chance IEEPA tariffs survive SCOTUS |

### Expert Commentary Summary:
- Most analysts expect SCOTUS to limit or strike down IEEPA tariffs
- Administration officials (Bessent) have indicated alternative authorities available
- Trade experts note "thin trust" around truce after Iran tariff announcement

---

## ENSEMBLE CALCULATION

| Model | Estimate | Weight | Contribution |
|-------|----------|--------|--------------|
| Base Rate | 35% | 0.35 | 12.2% |
| Monte Carlo | 55% | 0.20 | 11.0% |
| Evidence-Adjusted | 45% | 0.25 | 11.2% |
| Community/Market | 38% | 0.20 | 7.6% |
| **ENSEMBLE** | | **1.00** | **42%** |

---

## VALIDATION

### Pre-Mortem: Why I Could Be Wrong

1. **Truce is stronger than I estimate** (→ 30-35%)
   - Diplomatic momentum toward April summit may prevent any action
   - Administration genuinely committed to stability
   - Likelihood: Medium

2. **AD/CVD timing uncertainty** (→ 35-38%)
   - Orders may not fall within this specific 2-month window
   - Definition of "new" restriction may be narrower than assumed
   - Likelihood: Medium

3. **Iran tariff doesn't evolve** (→ 38-40%)
   - Remains a broad policy without China-specific designation
   - Legal challenges prevent implementation
   - Likelihood: Medium-High

4. **Underestimating escalation risk** (→ 50-55%)
   - Trump's unpredictability could break truce
   - China retaliation could trigger US counter-action
   - SCOTUS ruling could trigger immediate reimposition
   - Likelihood: Low-Medium

### Sanity Checks:
- ✓ Probability between 5% and 95%
- ✓ Would bet at these odds
- ✓ Divergence from community explained (+4% due to breaking news and AD/CVD process)
- ✓ Movement from base rate justified (+7% with documented evidence)

---

## UPDATE TRIGGERS

| Event | Action |
|-------|--------|
| **SCOTUS rules against IEEPA** | Increase to 48-52% |
| **Iran tariff specifically names China** | Increase to 65-70% |
| **New AD/CVD order on China announced** | Resolve YES immediately |
| **Major diplomatic breakthrough** | Decrease to 28-32% |
| **China retaliatory action** | Increase to 50-55% |
| **Trump-Xi phone call scheduled** | Decrease to 35-38% |

---

## MONITORING SCHEDULE

- **Daily:** Check Supreme Court opinion releases, USTR announcements
- **Weekly:** Check Commerce Department AD/CVD notices, Federal Register
- **Every 3 days:** Full reassessment with updated news search

**Next Review:** January 16, 2026

---

## KEY REASONING SUMMARY

The probability of YES (42%) reflects a balance between:

1. **The formal 1-year trade truce** agreed at Busan in October 2025, which creates diplomatic constraints on major escalatory actions

2. **The routine AD/CVD process** which continues regardless of high-level diplomacy and represents the most likely path to YES

3. **Breaking news uncertainty** from the Iran tariff announcement, which doesn't directly qualify but signals willingness to act

4. **The imminent Supreme Court decision** on IEEPA tariffs, which could trigger a new round of China-specific actions

The 4% divergence above community reflects my assessment that the AD/CVD process and recent Iran tensions are slightly underweighted by the crowd.

---

## SOURCES CITED

1. White House Fact Sheet: US-China Economic and Trade Deal (November 1, 2025)
2. USTR: Section 301 Exclusion Extensions (November 26, 2025)
3. CNBC: Trump Iran Tariff Announcement (January 12, 2026)
4. Yale Budget Lab: State of US Tariffs (October 30, 2025)
5. Tax Foundation: Trump Tariffs Economic Impact (Updated January 13, 2026)
6. PIIE: US-China Tariff Chart (Updated regularly)
7. Metaculus Community Discussion (January 12-13, 2026)

---

*Analysis completed: January 13, 2026*  
*Forecast by: Claude (Bridgewater Tournament Pipeline v3.0)*
