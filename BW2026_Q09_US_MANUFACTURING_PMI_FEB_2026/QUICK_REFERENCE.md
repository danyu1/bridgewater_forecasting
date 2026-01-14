# QUICK REFERENCE — US Manufacturing PMI (Feb 2026)

Question: What will be the S&P Global US Manufacturing PMI for February 2026? (final, not flash)

As-of: 2026-01-13

## Forecast (percentiles)
- p5: 48.1
- p25: 50.8
- p50: 52.8
- p75: 54.9
- p95: 59.7

## Useful tail probabilities (from simulation)
- P(PMI < 49): 9.4%
- P(PMI < 50): 16.7%
- P(PMI > 56): 16.7%

## Anchors
- S&P Global US Manufacturing PMI: Nov 2025 = 52.2; Dec 2025 = 51.8 (official PDFs in folder)
- ISM Manufacturing PMI: Dec 2025 = 47.9 (proxy history via Investing.com event 173)

## How to reproduce
- Run full pipeline: `python3 BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026/pmi_analysis.py`
- Base rates only: `python3 BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026/base_rate_calc.py`
- Model only: `python3 BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026/quant_model.py`

## Monitoring
- Run: `python3 BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026/monitor_pmi.py`
- Update triggers:
  - New S&P Global US Manufacturing PMI release (month or value changes)
  - New ISM release with large move (>= 0.7 pts) or any move that changes cycle narrative (crossing 50)
  - Large divergence between ISM and S&P (offset shifts materially from ~4 pts)
