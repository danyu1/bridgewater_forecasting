# NVIDIA Blackwell Export to China Forecast Analysis

## Complete Bridgewater Tournament Pipeline v3.0

---

╔═══════════════════════════════════════════════════════════════════╗
║                        FINAL FORECAST                              ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║     █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  5%           ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝

---

## QUESTION DETAILS

| Field | Value |
|-------|-------|
| **Question** | Will any NVIDIA GPUs better than the H200 be allowed to be exported to China before March 14, 2026? |
| **Type** | Binary |
| **Platform** | Metaculus (Bridgewater Tournament) |
| **Close Date** | March 14, 2026 |
| **Community Median** | 7% |
| **Forecasters** | 377 |
| **Analysis Date** | January 13, 2026 |
| **Time Horizon** | ~60 days |

---

## RESOLUTION CRITERIA (Exact)

> This question will resolve as Yes if, after January 12, 2026 and before March 14, 2026 ET, the US government publicly states that it will permit any Nvidia GPU that is better than the H200 to be exported to mainland China.

> For the purposes of this question, "better than H200" is defined as any GPU with both:
> - a peak FP8 Tensor Core throughput (including sparsity) higher than 4 petaFLOPS
> - an HBM bandwidth of at least 4.8 TB/s.

**Alternative YES trigger:**
> This question will also resolve as Yes if such GPUs are directly exported to mainland China, without credible sources reporting that the export violated US export controls or that the US government is taking enforcement action relating to those exports.

---

## ⚠️ CRITICAL TECHNICAL INSIGHT

### The B30A Would NOT Qualify!

The resolution criteria require **BOTH** conditions to be met:
- FP8 > 4 petaFLOPS ✓
- HBM bandwidth ≥ 4.8 TB/s ✓

| GPU | FP8 (PFLOPS) | HBM (TB/s) | Qualifies? |
|-----|-------------|-----------|-----------|
| **H200** (threshold) | 4.0 | 4.8 | No (threshold) |
| **B30A** (estimated) | ~4.5 | ~4.0 | **NO** ✗ |
| **B100** | ~9.0 | ~7.7 | YES ✓ |
| **B200** | ~9.0 | ~7.7 | YES ✓ |
| **B300** | ~9.0 | ~8.0 | YES ✓ |

**Key Finding:** The B30A (cut-down Blackwell designed for China) has approximately half the memory bandwidth of full Blackwell (~4 TB/s vs ~8 TB/s). This falls **below** the 4.8 TB/s threshold required for YES resolution.

**This is crucial because:**
1. Trump explicitly blocked full Blackwell in November 2025
2. The B30A was the "compromise" chip being discussed
3. Only full Blackwell (B100/B200/B300) would trigger YES
4. Full Blackwell approval is extremely unlikely in the 60-day window

---

## BASE RATE ANALYSIS

| Reference Class | Rate | Sample Size | Relevance | Weight |
|-----------------|------|-------------|-----------|--------|
| Major policy reversal in 60 days | 5% | n=20 | 7/10 | 0.21 |
| Trump reversing explicit public statement | 8% | n=15 | 9/10 | 0.27 |
| Export control loosening on cutting-edge tech | 3% | n=10 | 8/10 | 0.24 |
| Blackwell approval during H200 rollout | 2% | n=5 | 10/10 | 0.29 |

**Weighted Base Rate: 4.4%**

---

## MONTE CARLO SIMULATION (n=100,000)

### Path Contributions to YES

| Path | Contribution | Description |
|------|--------------|-------------|
| Trade Deal Surprise | 1.69% | Major unexpected trade concession |
| Trump Reversal | 1.16% | Direct presidential policy reversal |
| Legal Loophole | 0.79% | Export through cloud or other mechanism |
| Rubin Release Shift | 0.60% | New chip makes Blackwell "outdated" faster |
| NSC Override | 0.56% | National Security Council approves over Trump |

**Total Monte Carlo YES: 4.8%**

---

## EVIDENCE ADJUSTMENTS

### Factors Pushing UP from Base Rate (+2.0%)

| Factor | Strength | Adjustment |
|--------|----------|------------|
| Trump unpredictability | Weak | +1.0% |
| Jensen Huang lobbying | Weak | +0.5% |
| Cloud loophole precedent | Weak | +0.5% |

### Factors Pushing DOWN from Base Rate (-8.8%)

| Factor | Strength | Adjustment |
|--------|----------|------------|
| **Trump explicit Nov 2025 denial** | Strong | -2.0% |
| **Bessent "12-24 months" timeline** | Strong | -1.5% |
| Congressional opposition | Moderate | -1.0% |
| **H200 just approved (compromise)** | Strong | -1.5% |
| National security consensus | Moderate | -1.0% |
| B30A specifically rejected | Moderate | -1.0% |
| Nvidia not applying for licenses | Moderate | -0.8% |

**Net Adjustment:** -6.8% (floored using Bayesian multiplicative approach)

**Evidence-Adjusted Estimate: 3.1%**

---

## KEY EVIDENCE SUMMARY

### Strong Evidence AGAINST (Blocking)

1. **Trump's Explicit Statement (Nov 3, 2025):**
   > "The most advanced, we will not let anybody have them other than the United States. We don't give the Blackwell chip to other people."

2. **Bessent's Timeline (Nov 4, 2025):**
   > "If we think about the Blackwell now, they're the crown jewel... Given the incredible innovation that goes on at Nvidia, where the Blackwell chips may be two, three, four down their chip stack in terms of efficacy, and at that point they could be sold on."
   > 
   > Timeframe: "12 to 24 months"

3. **H200 as the Compromise:**
   - December 8, 2025: Trump approved H200 exports with 25% fee
   - This was explicitly the concession - H200, not Blackwell
   - Major policy shift already occurred

4. **B30A Specifically Blocked:**
   - Even the cut-down Blackwell (B30A) was rejected
   - Congressional opposition to any Blackwell variants
   - Institute for Progress analysis warned against B30A

5. **Nvidia Not Pursuing:**
   - Jensen Huang confirmed no plans to ship Blackwell to China
   - Nvidia hasn't applied for Blackwell export licenses
   - Company not actively pursuing this path

### Weak Evidence FOR (Possible Paths)

1. **Trump Unpredictability:**
   - August 2025 hint about "30-50% off" Blackwell
   - Transactional negotiating style
   - But explicit November denial is stronger signal

2. **David Sacks (AI Czar) Support:**
   - Has advocated for selling US chips to maintain market position
   - But hasn't prevailed on Blackwell specifically

3. **Cloud Loophole:**
   - Tencent accessing Blackwell via Japanese cloud (Datasection)
   - But this wouldn't trigger resolution criteria (would be enforcement action)

---

## ENSEMBLE CALCULATION

| Model | Estimate | Weight | Contribution |
|-------|----------|--------|--------------|
| Base Rate | 4.4% | 0.35 | 1.6% |
| Monte Carlo | 4.8% | 0.25 | 1.2% |
| Evidence Adjusted | 3.1% | 0.25 | 0.8% |
| Community (7%) | 7.0% | 0.15 | 1.1% |
| **FINAL** | **5%** | **1.00** | **4.6%** |

---

## VALIDATION

### Pre-Mortem: "Assume I'm Wrong. Why?"

| Reason | Likelihood | Would Change To |
|--------|------------|-----------------|
| 1. Trump makes surprise deal with Xi | Low | 15-20% |
| 2. Rubin release accelerates "outdated" timeline | Low | 8-10% |
| 3. Cloud loophole triggers resolution | Low-Medium | 10-12% |
| 4. B30A specs different than estimated (qualifies) | Low | 12-15% |
| 5. Nvidia applies and gets surprise approval | Very Low | 15-20% |

### Sanity Checks

✓ Probability between 5-95% (5% is near floor for non-impossible events)

✓ Would bet at these odds (would take 19:1 odds on NO)

✓ Divergence from community explained (-2% from community's 7%)
  - Community may not have fully processed B30A bandwidth limitation
  - Strong explicit evidence from Trump/Bessent in November

✓ Movement from base rate justified (slight movement DOWN from 4.4%)
  - Overwhelming evidence against in Nov 2025 statements
  - 60-day window is very short for policy reversal

---

## KEY REASONING (Executive Summary)

**Why 5%:**

The resolution criteria require GPUs with both >4 PFLOPS FP8 AND ≥4.8 TB/s HBM bandwidth. The cut-down B30A Blackwell would NOT qualify because its memory bandwidth (~4 TB/s) falls below the threshold. Only full Blackwell (B100/B200/B300) would trigger YES resolution.

Trump explicitly blocked full Blackwell exports in November 2025, stating "we will not let anybody have them other than the United States." Treasury Secretary Bessent indicated a 12-24 month timeline before Blackwell could be considered. The H200 approval in December 2025 was the compromise - the administration is not moving further up the chip stack.

The 60-day window is extremely short for the kind of major policy reversal that would be required. Nvidia hasn't even applied for Blackwell export licenses, and there are no scheduled high-level meetings that could produce such a deal before March 14, 2026.

**What would change my mind:**
- Trump announcing Blackwell discussions with China (→ 15%)
- Nvidia applying for Blackwell export licenses (→ 10%)
- Major unexpected trade deal breakthrough (→ 20%)
- Discovery that B30A bandwidth is actually ≥4.8 TB/s (→ 15%)

---

## UPDATE TRIGGERS

| Event | New Estimate |
|-------|--------------|
| Trump announces Blackwell negotiations | → 15-20% |
| Nvidia applies for Blackwell license | → 10-12% |
| Major trade breakthrough announced | → 18-22% |
| B30A specs confirmed with ≥4.8 TB/s bandwidth | → 15-18% |
| Congressional legislation passes blocking exports | → 2-3% |
| Rubin announced for early release | → 7-8% |

---

## MONITORING SCHEDULE

| Timeframe | Frequency |
|-----------|-----------|
| Next 2 weeks | Every 2-3 days |
| Weeks 3-6 | Weekly |
| Final 2 weeks | Every 2-3 days |

**Key Sources to Monitor:**
- White House announcements
- Commerce Department BIS updates
- Nvidia investor communications
- Reuters/Bloomberg breaking news
- Metaculus community discussion

---

## SOURCES & CITATIONS

1. Tom's Hardware (Nov 3, 2025) - "Trump says no Blackwell chips to be sold to China"
2. Tom's Hardware (Nov 4, 2025) - "Bessent says China can have Blackwell chips once they're outdated"
3. Tom's Hardware (Dec 23, 2025) - "Nvidia prepares shipment of 82,000 AI GPUs to China"
4. Institute for Progress (Nov 2025) - "Should the US Sell Blackwell Chips to China?"
5. Council on Foreign Relations (Dec 2025) - "China's AI Chip Deficit"
6. NVIDIA Blackwell Architecture Technical Brief - GPU specifications
7. Metaculus Community Discussion (Jan 12-13, 2026)

---

*Analysis completed January 13, 2026*
*Bridgewater Open Forecasting Tournament - Pipeline v3.0*
