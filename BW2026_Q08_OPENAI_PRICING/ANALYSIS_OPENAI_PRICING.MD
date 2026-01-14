# COMPLETE FORECAST ANALYSIS
## Question: Will OpenAI API token prices fall before March 14, 2026?

DATE: 2026-01-13
Question ID: BW2026_Q08_OPENAI_PRICING
Type: Binary
Platform: Metaculus (Bridgewater Tournament)
Close Date: 2026-02-28
Resolution Date: 2026-03-14

==================================================================
FINAL FORECAST
==================================================================
YES: 14%
NO:  86%
==================================================================

==================================================================
QUESTION DETAILS
==================================================================
Resolution Criteria (verbatim):
This question will resolve as Yes if, before March 14, 2026 ET, the standard on-demand OpenAI API Pricing lists any regular-sized GPT-5 or later model as having either:
- an input price below $1.25 per 1 million tokens, or
- an output price below $10 per 1 million tokens
or the latest regular-sized GPT model as having either
- an input price below $1.75 per 1 million tokens, or
- an output price below $14 per 1 million tokens

Regular-sized GPT model: model name contains "gpt-5" or "gpt-6" and does not contain "mini", "nano", "small", or "lite".
Standard on-demand pricing excludes batch/flex/cached-input discounts, promos, fine-tunes, or reseller pricing.

Edge cases:
- Any price move below thresholds triggers YES.
- New GPT-5.x or GPT-6 release with sub-threshold price triggers YES.
- Latest model rule applies to the most recently released regular-sized model and its variants.

==================================================================
RESEARCH SUMMARY
==================================================================
- OpenAI pricing pages returned HTTP 403 in this environment; pricing checks rely on question background and news RSS headlines.
- Google News RSS shows no fresh (last 7 days) reporting of GPT-5 on-demand price cuts.
- Historical pattern: deep cuts with major releases (GPT-4 -> 4 Turbo -> 4o -> GPT-5), followed by flat then higher pricing at GPT-5.2.
- No close or exact prediction markets found in Polymarket; Manifold only tangential markets.
- Metaculus crowd from screenshot and comments appears near 15%.

==================================================================
BASE RATE ANALYSIS
==================================================================
Reference Class 1: Major GPT releases with on-demand price cuts
  Rate: 18.7% | Sample: 3 cuts across 29 months | Source: OpenAI release history
Reference Class 2: GPT-5.x period since Aug 2025 with no cuts
  Rate: 5% floor | Sample: 2 transitions | Source: Metaculus background info
Reference Class 3: Any pricing change rate * fraction that were cuts
  Rate: 15.7% | Sample: 5 changes across 33 months | Source: OpenAI release history
Weighted Base Rate: 13.8% (rounded 14%)

==================================================================
STRUCTURAL MODEL
==================================================================
Method: Monte Carlo hazard model
Assumptions:
- Monthly probability of a cut to existing GPT-5.x pricing is ~0.06 (sd 0.03)
- Two-month window modeled as 1 - (1 - p)^2
- New GPT-5.x or GPT-6 launch before Mar 14 has mean probability 0.06 (sd 0.03)
- If launch occurs, 35% chance pricing is below the thresholds

Results (n=200,000):
- Mean: 13.5%
- Median: 13.5%
- 90% CI: [4.1% - 22.5%]

==================================================================
EVIDENCE ADJUSTMENTS
==================================================================
Factors UP:
+ Prices are exactly at the 1.75/14 boundary, tiny cut triggers YES (+2%, weak)
+ Competitive pricing pressure narratives in 2025 (+2%, weak)

Factors DOWN:
- GPT-5.2 raised prices to 1.75/14, signaling premium stance (-3%, moderate)
- GPT-6 release before deadline viewed as unlikely (-2%, weak/moderate)
- IPO margin protection incentive (-1%, weak)

Net Adjustment: -2%
Evidence-Adjusted Estimate: 12%

==================================================================
EXTERNAL SIGNALS
==================================================================
Polymarket: No close or exact market found in first 200 active markets.
Manifold: Only tangential markets (pricing structure, GPT-5 pricing) with no direct probabilities.
Metaculus: Exact question present, screenshot indicates crowd ~15%.

Crowd Analysis: Short horizon plus recent price increase keeps crowd low but non-zero.

==================================================================
ENSEMBLE CALCULATION
==================================================================
| Model             | Estimate | Weight | Contribution |
|------------------|----------|--------|--------------|
| Base Rate         | 14%      | 0.30   | 4.2%         |
| Structural (MC)   | 13.5%    | 0.25   | 3.4%         |
| Evidence-Adjusted | 12%      | 0.20   | 2.4%         |
| Crowd/Market      | 15%      | 0.25   | 3.8%         |
| ENSEMBLE          |          | 1.00   | 13.8%        |

Final: 14%

==================================================================
VALIDATION
==================================================================
Pre-Mortem (Why I Could Be Wrong):
1) OpenAI announces a small cut to gpt-5.2 to defend developer share (medium)
2) Surprise gpt-5.3 or gpt-6 release priced below threshold (low)
3) Competitive price war escalates sharply after a major rival cut (medium)

Sanity Checks:
- Probability in 5-95% range: Yes
- Would bet at these odds: Yes
- Divergence from crowd explained: Yes (aligned)
- Base rate movement justified: Yes
- Recent news checked: Yes
- Prediction markets checked: Yes

==================================================================
KEY REASONING (Executive Summary)
==================================================================
The latest GPT-5 pricing sits exactly on the resolution boundary, so even a modest cut resolves YES. However, GPT-5.2 increased prices, and a new flagship launch before March 14 is unlikely. Balancing historical price-cut cadence against short-horizon margin protection yields a low but non-zero probability.

==================================================================
UPDATE TRIGGERS AND MONITORING
==================================================================
- Pricing page shows any regular-sized GPT-5/6 below thresholds -> update to 100% YES
- Announced gpt-5.3 or gpt-6 with pricing details -> re-run model (likely +5 to +12 pts)
- Major competitor cuts flagship API pricing by >=25% -> +5 to +8 pts
- OpenAI announces infra cost breakthrough or developer pricing program -> +3 to +5 pts
- IPO timeline announced with no pricing move by late Feb -> -2 to -4 pts

Review Schedule: Weekly until Feb 10, then every 2-3 days

==================================================================
SOURCES AND CITATIONS
==================================================================
[1] OpenAI API pricing page (blocked in this environment) https://platform.openai.com/docs/pricing (accessed 2026-01-13)
[2] OpenAI pricing page (blocked in this environment) https://openai.com/pricing (accessed 2026-01-13)
[3] OpenAI blog: Introducing GPT-5.1 for developers (RSS link) https://news.google.com/rss/articles/CBMiXEFVX3lxTE5FcTU2YTlVR193Vk1JTktaSlRHRlc2dE00TGw1bnl4NnlKaFN1TENRX0FBWGpPWFlvQ1JBcWJjT3h5dnJ1Rk9TcHFlSkJLQnhBT19aRTI1elQ0UG5w?oc=5
[4] Microsoft Azure blog: Introducing GPT-5.2 in Microsoft Foundry https://news.google.com/rss/articles/CBMitgFBVV95cUxPUHZEY09QNmcycnJEXzFCcXY5YmVlZ2lhOTRMTFRZa3F1bGthemJVTi1rMmtCdGQzc1k5RDVyY3JsNkl5UXlra192R2NNemtKWHNFX2RFWWxTd0Jfb2l5ZFhWUmEtcXdwQjRTVE9XTmdURmowUGFIQWpqbGR5T1RfaFJnaGtlalpIRzcxNHhDa2pXQjRfX3pXcEw1U3lWSzVuVFBmclB1MDdpOFJlTUpxSDU2VTlaQQ?oc=5
[5] TechCrunch: OpenAI priced GPT-5 so low, it may spark a price war https://news.google.com/rss/articles/CBMijwFBVV95cUxNSUdoWERxbVIzVnVxSjhITWlzVjIzaUNMa0hYN3Z4dlE2YXAxNmtDU1NhRks1MXIyLWxOWEZtYk9CRGp1anF3QmxMd0lBajJUN3ZWWW16YUtBZEY5WE9yYS00Y3dkZlE1ZTZRUGJlaFpvVm1UdkRmVFUzektUNnQ2ZkdvYVNnWGFQam52eEhGWQ?oc=5
[6] VentureBeat: OpenAI slashes prices for GPT-4.1, igniting AI price war https://news.google.com/rss/articles/CBMiakFVX3lxTE1qXzVlUWFEMEFIZ09vSkhYZ3paaEJ1WVNBX3VNWVBjNXJoNkp4OTN1azNzclFNbHEtc1dZWDhGUVhKVlJRbGNRMWlnZzhNVGlVVmgxZzNIb0diLUJKc1VTcHBjVFp6REZyNHc?oc=5
[7] Anthropic: Claude Opus 4.5 pricing cut (RSS link) https://news.google.com/rss/articles/CBMiyAFBVV95cUxNNDRnQlFwakMwczZnMkxuNmVvVTExa0xHMDFWT3o4VkdJb1ZBOWI5NmhMU1BYTERsZ2FlUkdOVTNRcmRtemhHRXFoX0dlTmtVeUVZUmhmd0l3enpzRmtVODBrUkR2Smpmc0ZKNFFIQWdKakhZYktKZFBCV1RTSGFPeFNZZzhvVWd2MzFnU1lpZlhTT1RLNkVacUlHYldVRy1HRm9jUWt2T1J5WnNwcEdheU5GTkJxVmhFcWQzcVFaa1A5dUx1eEZqMw?oc=5
