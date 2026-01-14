# Research Notes — Combined hyperscaler capex (Q4 2025)

## Resolution mechanics
- Metric: combined capex for Microsoft (MSFT), Alphabet (GOOG), Amazon (AMZN) for quarter ending 2025-12-31.
- Definition: cash outflows for purchases/additions to PP&E net of PP&E inflows (proceeds/incentives), multiplied by -1 (so reported as a positive “capex”).

## Primary sources used
- SEC XBRL companyfacts API (for cash-flow line items):
  - MSFT: https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json
  - GOOG: https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json
  - AMZN: https://data.sec.gov/api/xbrl/companyfacts/CIK0001018724.json

## Tags used in SEC data
- MSFT: `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment`
- GOOG: `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` (quarterly values sometimes derived from YTD in filings)
- AMZN: `us-gaap:PaymentsToAcquireProductiveAssets` (proxy for “Purchases of property and equipment”)

## Netting PP&E inflows (Amazon)
- Amazon’s cash flow often includes “Proceeds from property and equipment sales and incentives”.
- This inflow is small vs purchases (order of ~$0.8–$1.8B recently) but is included in the question definition.
- The scripts use the prompt’s recent inflow examples as anchors and treat unknown quarters with a conservative stochastic adjustment.

## Crowd signal (from screenshot prompt)
- Community median ~89.45B, with IQR ~[84.76B, 95.07B].

## Key drivers to watch
- AI/data-center acceleration vs capacity constraints (power, chips, construction).
- Cloud demand seasonality and “year-end budget exhaust” effects in Q4.
- Any shifts toward leases/financing vs cash capex (matters because the question is cash PP&E outflows).
