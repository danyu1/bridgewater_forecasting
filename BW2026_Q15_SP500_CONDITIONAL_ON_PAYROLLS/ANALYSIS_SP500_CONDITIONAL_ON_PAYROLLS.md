# COMPLETE FORECAST ANALYSIS
## Question: What will be the closing value of the S&P 500 on March 13, 2026, conditional on payroll growth?

Date: 01/14/2026
Question ID: BW2026_Q15_SP500_CONDITIONAL_ON_PAYROLLS
Type: Conditional + Continuous

----------------------------------------------------------------
STEP 1: INTAKE & RESOLUTION MECHANICS
----------------------------------------------------------------
Parent resolution (binary):
- YES if PAYEMS(Feb 2026) − PAYEMS(Dec 2025) < 100 (thousand), using seasonally adjusted FRED values.
- The question will most probably use the initial estimate for Feb 2026 and the revised estimate for Dec 2025 as published in the Feb 2026 Employment Situation.

Child resolution (continuous):
- S&P 500 close on 2026-03-13 (Yahoo Finance close unless unusable).

Edge cases:
1) Parent uses revisions; a large Dec revision can flip the outcome.
2) Child relies on a single close print; minor source discrepancies are usually negligible at the index level.

Key uncertainties:
1) Whether payroll momentum slows sharply across Jan–Feb 2026.
2) Whether a <100k two‑month gain would be priced primarily as “growth scare” (risk‑off) or “Fed put” (risk‑on).
3) Baseline equity volatility over ~2 months.

----------------------------------------------------------------
STEP 2: BASE RATES
----------------------------------------------------------------
Parent (PAYEMS 2-month change <100k):
- Long-run base rate from historical PAYEMS 2‑month changes.
- Recent-regime simulation using the last 36 months of monthly PAYEMS changes.

Child (conditional S&P 500 effect):
- A proxy calibration using historical S&P 500 (SPX) close data (Stooq) and PAYEMS.
- We estimate the distribution of S&P 500 log returns over an event window meant to mimic “post-payroll-release to March 13”: 7 trading days after an approximate release date.

----------------------------------------------------------------
STEP 3: QUANTITATIVE MODEL
----------------------------------------------------------------
Data inputs (local snapshots):
- PAYEMS last observed (as-of fetch): 2025-12 level in `payems_fred.csv`.
- SPX last observed (as-of fetch): latest close in `sp500_stooq.csv`.

Simulation:
1) Parent: simulate Jan and Feb monthly payroll changes using a recent normal approximation; parent YES if (Jan+Feb) < 100.
2) Baseline S&P 500 path: simulate log return from the latest close to 2026-03-13 using recent daily log-return mean and volatility.
3) Conditional adjustment: add a scenario-dependent shock equal to (R_cond − R_all), where R_cond is drawn from the historical 7‑trading‑day return distribution under the parent condition and R_all is the unconditional draw.

----------------------------------------------------------------
STEP 4: FINAL FORECASTS
----------------------------------------------------------------
Parent probability (context):
- Simulation P(YES) ≈ 12% (`forecast_output.json`)
- Base-rate blend P(YES) ≈ 15% (`base_rate_output.json`)

Child forecasts (S&P 500 close on 2026-03-13):
- Given YES (<100k jobs): p5 6168 | p25 6664 | p50 7034 | p75 7424 | p95 8027
- Given NO (>=100k jobs): p5 6187 | p25 6669 | p50 7027 | p75 7404 | p95 7983

----------------------------------------------------------------
STEP 5: VALIDATION / PRE-MORTEM
----------------------------------------------------------------
Main ways this is wrong:
1) Regime break: a <100k two‑month gain coincides with a sharp drawdown (risk premium spike) larger than implied by historical averages.
2) Policy dominance: weak payrolls trigger strong easing expectations and equities rally materially more than modeled.
3) Data mismatch: SPX proxy history differs from Yahoo close conventions; should be small but could matter for tight scoring.

Sanity checks:
- Conditional distributions are close because the historical payroll-growth signal has weak average effect on near-term index levels; uncertainty mostly comes from baseline equity volatility.

----------------------------------------------------------------
STEP 6: UPDATE TRIGGERS
----------------------------------------------------------------
Parent:
- Large revisions to Dec 2025 payroll level.
- Surprise Jan 2026 payroll print and/or revisions that materially change the implied two-month trajectory.

Child:
- Volatility regime shift (sustained move in daily vol).
- Clear market repricing of labor-growth sensitivity (e.g., a sequence of weak labor prints producing consistent equity selloffs).

Monitoring:
- `monitor_payrolls_sp500.py` writes daily monitoring reports and tracks last-seen values.
