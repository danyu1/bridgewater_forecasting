# COMPLETE FORECAST ANALYSIS
## Question: What will be the S&P Global US Manufacturing PMI for February 2026?

Date: 01/13/2026  
Question ID: BW2026_Q09_US_MANUFACTURING_PMI_FEB_2026  
Type: Continuous (numeric value)  
Resolution source: S&P Global US Manufacturing PMI final (not flash)  

----------------------------------------------------------------
STEP 1: INTAKE & RESOLUTION MECHANICS
----------------------------------------------------------------
Exact resolution: “This question will resolve as the value of the S&P Global US Manufacturing PMI for February 2026.” (final value; annul if unavailable by Mar 16, 2026)

Edge cases:
1) Flash vs final: only the final value counts.
2) Data discontinuation/unavailability: question annuls if final value not available by 2026-03-16.

Key uncertainties:
1) Near-term macro shock between now and the Feb reference month (financial conditions, policy, geopolitics).
2) Whether the current divergence between S&P Global PMI (>50) and ISM (<50) persists or mean-reverts.
3) Typical month-to-month volatility: PMI is “sticky”, but can still swing 2–5 pts in downturns.

----------------------------------------------------------------
STEP 2: BASE RATES (REFERENCE CLASSES)
----------------------------------------------------------------
Known anchors (S&P Global):
- Nov 2025 final: 52.2 (`spglobal_us_mfg_pmi_2025_11_final.pdf`)
- Dec 2025 final: 51.8 (`spglobal_us_mfg_pmi_2025_12_final.pdf`)

Proxy series used for base rates:
- ISM Manufacturing PMI long history (Investing.com event 173; `ism_pmi_history.csv`) as a proxy for volatility and mean-reversion.

Two base-rate views (both proxy-based, shifted to S&P Global scale using Nov/Dec offset):
1) Unconditional February reference-class (Feb across years since 2000): centered high (p50 ≈ 56.9) because it mixes expansions and booms; not very relevant given the current ISM level is ~48.
2) Conditional “2 months ahead given today-like ISM” (|ISM_t − 47.9| ≤ 1.0; then look ahead 2 months): p50 ≈ 51.9; tighter and more relevant to the current regime (`base_rate_output.json`).

Offset calibration (S&P – ISM):
- Nov 2025: 52.2 − 48.2 = +4.0
- Dec 2025: 51.8 − 47.9 = +3.9
Working assumption: mean offset ≈ +4.0 with conservative sd floored at 0.8.

----------------------------------------------------------------
STEP 3: STRUCTURAL / QUANTITATIVE MODEL
----------------------------------------------------------------
Goal: Produce a distribution for Feb 2026 S&P Global PMI.

Model components (proxy-based):
1) ISM AR(1) two-step forecast to Feb 2026 + (S&P–ISM) offset uncertainty.
2) Persistence from last observed S&P Global (Dec 2025 = 51.8), adjusted by simulated ISM two-step change and additional noise.
3) Seasonal February prior (ISM Feb distribution) + offset, downweighted.

Fit (ISM, monthly >= 2000):
- AR(1): a ≈ 0.926, b ≈ 3.85, residual sd ≈ 1.85 (`forecast_output.json`)

Ensemble weights:
- AR(1)+offset 0.55, persistence 0.30, seasonal 0.15 (`forecast_output.json`)

----------------------------------------------------------------
STEP 4: EVIDENCE ADJUSTMENT (INSIDE VIEW)
----------------------------------------------------------------
Short horizon note:
- The question is only ~2 months ahead from the latest known reading (Dec 2025), so persistence/mean-reversion dominates; big moves require unusual shocks.

Directional factors:
- ISM is in contraction territory (Dec 2025 = 47.9), which increases downside tail risk.
- S&P Global is still modestly expansionary (Dec 2025 = 51.8), suggesting the “true” Feb outcome may remain >50 absent a shock.

Net effect:
- Keep the median modestly above 52, but maintain a meaningful left tail (<50 roughly ~17%).

----------------------------------------------------------------
STEP 5: EXTERNAL SIGNALS (CROWD)
----------------------------------------------------------------
Metaculus crowd snippets from prompt:
- nikakovskaya: 52.2 (51–53)
- ts1: 51.8 (50.4–53.1)
- SandroAVL: 49.2 (emphasized downside risk)

Crowd central tendency appears near ~52 with a minority emphasizing a <50 tail.

----------------------------------------------------------------
STEP 6: ENSEMBLE & FINAL DISTRIBUTION
----------------------------------------------------------------
Final forecast distribution (from `quant_model.py`):
- p5: 48.1
- p25: 50.8
- p50: 52.8
- p75: 54.9
- p95: 59.7

Tail probabilities (useful for Metaculus bins):
- P(PMI < 49): 9.4%
- P(PMI < 50): 16.7%
- P(PMI > 56): 16.7%

----------------------------------------------------------------
STEP 7: VALIDATION / PRE-MORTEM
----------------------------------------------------------------
Main ways this forecast is wrong:
1) Downside shock: a rapid deterioration in orders/production pushes both ISM and S&P sharply down → Feb S&P PMI < 50 becomes much more likely (30–50%).
2) “Divergence break”: S&P-ISM offset collapses (e.g., S&P drops toward ISM) → distribution shifts left by ~2–4 points.
3) Rebound: inventory rebuilding / easing financial conditions lift manufacturing → Feb S&P PMI in mid/high-50s becomes more likely.

Sanity checks:
- Centered near recent S&P levels (51.8–52.2) with realistic month-to-month volatility.
- Keeps a non-trivial contraction tail consistent with ISM <50.

----------------------------------------------------------------
STEP 8: UPDATE TRIGGERS
----------------------------------------------------------------
Increase forecast (shift distribution right):
- New S&P PMI print rises materially (>+1.0) with broad component improvement.
- New ISM print rises toward/above 50 and is confirmed by new orders/employment details.

Decrease forecast (shift distribution left):
- New ISM print falls further (<47) or shows sharp new-orders decline.
- Macro shock: tightening financial conditions, abrupt tariff/supply disruption, or other negative demand shock.
- Evidence that S&P-ISM offset is shrinking (S&P falls toward ISM).

----------------------------------------------------------------
FINAL FORECAST (ENTER THESE ON METACULUS)
----------------------------------------------------------------
p5 48.1 | p25 50.8 | p50 52.8 | p75 54.9 | p95 59.7
