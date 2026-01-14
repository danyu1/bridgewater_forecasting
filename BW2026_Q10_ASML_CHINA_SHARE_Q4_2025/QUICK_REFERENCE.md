# QUICK REFERENCE — ASML China share (Q4 2025)

Question: What percentage of ASML's net system sales will be to China in Q4 2025? (ship-to location; reported in investor presentation; rounded to nearest whole % if needed)

As-of: 2026-01-13

## Forecast (percentiles, %)
- p5: 22.0
- p25: 28.3
- p50: 32.2
- p75: 41.5
- p95: 50.9

## Anchors (given / verified)
- Q3 2025: 42% (ASML Q3 2025 investor presentation; `research_snapshot.json`)
- Q2 2025: 27% (Metaculus background table)
- Q1 2025: 27% (Metaculus background table)
- Q4 2024: 27% (ASML Q4 FY2024 investor presentation text-extractable)
- Q3 2024: 47% (Metaculus background table)
- Q2 2024: 49% (Metaculus background table)
- Q1 2024: 49% (Metaculus background table)
- Q4 2023: 39% (Metaculus background table)

## How to reproduce
- Refresh scrapeable ASML IR points: `python3 BW2026_Q10_ASML_CHINA_SHARE_Q4_2025/asml_data_fetch.py`
- Base rates: `python3 BW2026_Q10_ASML_CHINA_SHARE_Q4_2025/base_rate_calc.py`
- Quant model: `python3 BW2026_Q10_ASML_CHINA_SHARE_Q4_2025/quant_model.py`

## Monitoring
- Run: `python3 BW2026_Q10_ASML_CHINA_SHARE_Q4_2025/monitor_asml_china_share.py`
- Trigger: ASML posts Q4 2025 results / investor presentation on or around 2026-01-28
