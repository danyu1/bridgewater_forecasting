# COMPLETE FORECAST ANALYSIS
## Question: What will be the combined capex for Microsoft, Alphabet and Amazon during the fourth quarter of 2025?

Date: 01/13/2026  
Question ID: BW2026_Q11_HYPERSCALER_CAPEX_Q4_2025  
Type: Continuous (USD billions)  
Resolution source: each company’s earnings report / SEC filings (cash flow statement)  

----------------------------------------------------------------
STEP 1: INTAKE & RESOLUTION MECHANICS
----------------------------------------------------------------
Resolves as the combined capital expenditures (capex) for MSFT, GOOG, AMZN for the quarter ending 2025-12-31.

Definition used by the question:
- For each company i: capex_i = - (Out_i + In_i)
- Out_i: PP&E purchases/additions (cash outflow; typically shown as a negative number in the cash flow statement)
- In_i: PP&E proceeds/incentives (cash inflow; 0 if not separately reported)

So in practice (in positive “capex” terms): capex ≈ (PP&E payments) − (PP&E proceeds/incentives).

Edge cases:
1) If a company reports only year-to-date cash flow in a filing, quarterly capex can be derived as (FY or YTD Q4) minus (YTD Q3).
2) If Amazon’s “proceeds and incentives” are not separately tagged in XBRL, they may need manual extraction from the cash flow statement.

Key uncertainties:
1) Does the AI/datacenter cash spend keep accelerating into Q4, or does it flatten after the huge 2025 ramp?
2) Q4 seasonality: year-end budget flush vs permitting/power constraints that can delay cash outlays.
3) Mix shift toward leases/financing rather than cash PP&E purchases (matters because the metric is cash PP&E outflows).

----------------------------------------------------------------
STEP 2: BASE RATES (REFERENCE CLASSES)
----------------------------------------------------------------
Recent realized totals from prompt (USD billions):
- Q4 2024: 56.132
- Q1 2025: 58.197
- Q2 2025: 70.893
- Q3 2025: 77.575

Historical seasonality proxy:
- Use SEC cash-flow line items to compute historical combined Q4/Q3 ratios where available.
- Apply those ratios to current Q3 2025 to get a base-rate distribution (`base_rate_calc.py`).

Base-rate result (ratio method; USD billions):
- mean ~86.2, p50 ~87.8, p95 ~93.4 (`base_rate_output.json`)

Interpretation:
- Pure seasonality from past years tends to put Q4 only modestly above Q3.
- This likely underweights the current regime shift (AI/datacenter boom) and the possibility of an unusually strong year-end push.

----------------------------------------------------------------
STEP 3: STRUCTURAL / QUANTITATIVE MODEL
----------------------------------------------------------------
Inputs from SEC XBRL companyfacts (cash-flow tags):
- MSFT: `PaymentsToAcquirePropertyPlantAndEquipment`
- GOOG: `PaymentsToAcquirePropertyPlantAndEquipment` (with quarterly sometimes derived from YTD)
- AMZN: `PaymentsToAcquireProductiveAssets` (proxy for “Purchases of property and equipment”)

Amazon PP&E inflows (proceeds/incentives):
- Treated as a stochastic adjustment anchored to recent examples from the prompt (roughly ~$0.8–$1.8B).

Ensemble components (`quant_model.py`):
1) Total-ratio method: sample historical combined Q4/Q3 ratios and apply to Q3 2025.
2) Company-ratio sum: sample per-company Q4/Q3 ratios and sum company forecasts (minus Amazon inflow).
3) Crowd anchor: lognormal fit to community p25/p50/p75 from the prompt screenshot.
4) Acceleration tail: low-probability upside scenario added to the company-sum component.

Weights:
- total ratio 0.15, company ratio sum 0.25, crowd 0.50, acceleration tail 0.10 (`forecast_output.json`)

----------------------------------------------------------------
STEP 4: EVIDENCE ADJUSTMENT (INSIDE VIEW)
----------------------------------------------------------------
Qualitative considerations pushing higher vs the ratio-only base rate:
- 2025 shows a large step-up in reported cash PP&E spending for all three companies.
- AI/datacenter urgency can create an unusually strong Q4 “flush” (accelerated cash payments before year-end).

Considerations pushing lower:
- Construction/power bottlenecks can delay cash spend even when plans are aggressive.
- Accounting mix: more leasing or vendor financing would reduce cash PP&E outflows for the quarter.

Net effect:
- Keep the center near the crowd median (~89B) while retaining an upside tail into the high-90s / low-100s.

----------------------------------------------------------------
STEP 5: EXTERNAL SIGNALS (CROWD)
----------------------------------------------------------------
From the prompt screenshot:
- Community median ~89.45B; IQR ~[84.76B, 95.07B]

Commenter anchors:
- seekingalpha: ~87B (84.7–90.3)
- ts1: ~91B (86.1–97.1)

----------------------------------------------------------------
STEP 6: FINAL DISTRIBUTION (ENTER THESE ON METACULUS)
----------------------------------------------------------------
Final forecast (USD billions):
- p5: 78.8
- p25: 84.4
- p50: 89.2
- p75: 93.9
- p95: 101.1

----------------------------------------------------------------
STEP 7: VALIDATION / PRE-MORTEM
----------------------------------------------------------------
Main ways this forecast is wrong:
1) Blowout Q4: cash spend accelerates sharply and hits >100B more likely than modeled (tail should be fatter).
2) Delays: power/permitting/construction or supplier constraints defer payments, pulling Q4 closer to Q3 (mid/low-80s).
3) Definition mismatch: filings report capex differently than the prompt’s examples (need to ensure the right cash-flow line items and netting).

Sanity checks:
- Median aligns with crowd median.
- Q4 is generally above Q3 but not assumed to spike unrealistically without a clear catalyst.

----------------------------------------------------------------
STEP 8: UPDATE TRIGGERS
----------------------------------------------------------------
Update upward:
- Earnings releases or filings show exceptionally large cash-flow PP&E purchases vs prior quarter.
- Company commentary indicates accelerated deployment payments before year-end.

Update downward:
- Explicit capex deferral commentary, major project delays, or signs of tightening liquidity/financing.
- Evidence that spending shifted from cash PP&E into leases/financing (reducing this metric).

Monitoring:
- `monitor_hyperscaler_capex.py` checks SEC companyfacts for new quarter-ended 2025-12-31 data and writes a daily monitoring report.

