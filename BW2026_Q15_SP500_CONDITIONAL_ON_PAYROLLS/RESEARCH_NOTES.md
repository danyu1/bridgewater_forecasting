# Research Notes — Payrolls threshold and S&P 500 conditional

## Resolution sources
- Parent: PAYEMS (Total Nonfarm Payrolls, seasonally adjusted) from FRED for Dec 2025 and Feb 2026.
- Child: S&P 500 closing value on 2026-03-13 from Yahoo Finance (fallback to another credible source).

## Data sources used in scripts
- FRED PAYEMS CSV: https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS
- S&P 500 proxy history for modeling: Stooq SPX close CSV: https://stooq.com/q/d/l/?s=^spx&i=d

## Notes
- PAYEMS is in thousands; parent threshold is (Feb − Dec) < 100.
- The child question is conditional on the parent; scripts simulate a joint scenario and output two separate S&P 500 percentile forecasts.
- The conditional equity-impact calibration uses a 7-trading-day window after an approximate payroll release date (first Friday of next month) as a proxy for the information arrival before the 2026-03-13 resolution date.
