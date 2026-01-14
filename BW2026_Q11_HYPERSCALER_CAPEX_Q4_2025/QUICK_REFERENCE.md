# QUICK REFERENCE — Hyperscaler capex (Q4 2025)

Question: What will be the combined capex for Microsoft, Alphabet and Amazon during Q4 2025? (cash outflows for PP&E purchases/additions net of PP&E inflows; sign-converted)

As-of: 2026-01-13

## Forecast (USD billions)
- p5: 78.8
- p25: 84.4
- p50: 89.2
- p75: 93.9
- p95: 101.1

## Anchors (from question prompt)
- Q4 2024: 56.132
- Q1 2025: 58.197
- Q2 2025: 70.893
- Q3 2025: 77.575

## How to reproduce
- Fetch SEC series: `python3 BW2026_Q11_HYPERSCALER_CAPEX_Q4_2025/capex_data_fetch.py`
- Base rates: `python3 BW2026_Q11_HYPERSCALER_CAPEX_Q4_2025/base_rate_calc.py`
- Model: `python3 BW2026_Q11_HYPERSCALER_CAPEX_Q4_2025/quant_model.py`

## Monitoring
- Run: `python3 BW2026_Q11_HYPERSCALER_CAPEX_Q4_2025/monitor_hyperscaler_capex.py`
- Update triggers:
  - New MSFT/GOOG/AMZN filings containing quarter-ended 2025-12-31 cash-flow capex inputs
  - Company earnings releases that materially revise capex expectations or show unusually high cash investment line items
