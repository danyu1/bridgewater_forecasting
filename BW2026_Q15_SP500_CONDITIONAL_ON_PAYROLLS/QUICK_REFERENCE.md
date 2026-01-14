# QUICK REFERENCE — Conditional S&P 500 on 2026-03-13

As-of: 2026-01-14

## Parent (for context)
- P( PAYEMS(Feb 2026) − PAYEMS(Dec 2025) < 100k ) ≈ 12% (simulation) / 15% (base-rate blend)

## Child forecasts (S&P 500 close on 2026-03-13)
Given YES (<100k jobs):
- p5 6168 | p25 6664 | p50 7034 | p75 7424 | p95 8027

Given NO (>=100k jobs):
- p5 6187 | p25 6669 | p50 7027 | p75 7404 | p95 7983

## Reproduce
- `python3 BW2026_Q15_SP500_CONDITIONAL_ON_PAYROLLS/analysis_runner.py`

## Monitor
- `python3 BW2026_Q15_SP500_CONDITIONAL_ON_PAYROLLS/monitor_payrolls_sp500.py`
