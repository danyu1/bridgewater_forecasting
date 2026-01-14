# COMPLETE FORECAST ANALYSIS
## Question: What percentage of ASML's net system sales will be to China in Q4 2025?

Date: 01/13/2026  
Question ID: BW2026_Q10_ASML_CHINA_SHARE_Q4_2025  
Type: Continuous (% value)  
Resolution source: ASML Q4 2025 investor presentation (Region / ship-to location)  

----------------------------------------------------------------
STEP 1: INTAKE & RESOLUTION MECHANICS
----------------------------------------------------------------
Exact resolution: “reported percentage of ASML's net system sales made to China in the fourth quarter of 2025” (ship-to location; expected in the Q4 2025 investor presentation).

Key mechanics:
- Use the value reported by ASML in the investor presentation slide deck for Q4 2025.
- If ASML does not post the information there, use other credible sources (e.g., ASML SEC filings).
- If necessary, published data will be rounded to the nearest whole percentage point.

Edge cases:
1) If multiple “China %” figures exist (e.g., total net sales vs net system sales), only the “net system sales” region (ship-to location) figure counts.
2) If the presentation is image-only and the value is not text-searchable, manual reading may be required; monitor script attempts extraction but may fail.

Key uncertainties:
1) Whether Q3 2025’s very high China share (42%) is a transient pull-forward spike or a durable regime shift.
2) Export controls / licensing affecting shipment timing and mix.
3) EUV share and non-China demand (Taiwan/Korea/US) changing the denominator and mechanically moving China share.

----------------------------------------------------------------
STEP 2: BASE RATES (REFERENCE CLASSES)
----------------------------------------------------------------
Observed recent history (Q4 2023–Q3 2025) used as the primary reference class:
- Q4 2023: 39%
- Q1 2024: 49%
- Q2 2024: 49%
- Q3 2024: 47%
- Q4 2024: 27%
- Q1 2025: 27%
- Q2 2025: 27%
- Q3 2025: 42%

Notes on sourcing:
- The sequence above is taken from the Metaculus background table, with Q3 2025 (42%) and Q4 2024 (27%) additionally verifiable via text extraction from ASML’s investor presentation PDFs.

Base-rate statistics (limited sample):
- Unconditional mean ≈ 38.4, median ≈ 40.5, sd ≈ 10.0 (`base_rate_output.json`)
- Recent 4-quarter mean (Q4 2024–Q3 2025) ≈ 30.8 (`base_rate_output.json`)
- Quarter-to-quarter change range: -20 to +15 points (`base_rate_output.json`)

Interpretation:
- The short history shows a clear “low regime” (27% for three quarters) punctuated by a sharp spike to 42% in Q3 2025.
- A naive unconditional base rate overweights the earlier high regime (47–49%) and is less relevant than the recent regime and transition behavior.

----------------------------------------------------------------
STEP 3: STRUCTURAL / QUANTITATIVE MODEL
----------------------------------------------------------------
Goal: A distribution for Q4 2025 China share (% of net system sales).

Ensemble components (`quant_model.py`):
1) AR(1) on logit-transformed shares (captures bounded dynamics; small-sample).
2) Nearest-neighbor transitions: resample next-quarter shares from historical quarters with similar prior share (±7 pts) + noise.
3) Recent-mean model: normal around the last 4-quarter mean with conservative sd.
4) Import anchor: normal around ~30% with modest sd, reflecting the “imports imply ~30%” argument in comments (weakly weighted).

Weights:
- AR(1) 0.25, transitions 0.15, recent mean 0.35, import anchor 0.25 (`forecast_output.json`)

----------------------------------------------------------------
STEP 4: EVIDENCE ADJUSTMENT (INSIDE VIEW)
----------------------------------------------------------------
Inside-view drivers (qualitative):
- Pull-forward risk: customers in China may accelerate purchases to get ahead of additional restrictions, supporting elevated shares.
- Mix shift risk: if EUV and high-end tools (mostly non-China) dominate Q4 shipments, China share can drop even if China demand is strong.
- Mean reversion: the series shows large reversals (e.g., 47% → 27% from Q3 to Q4 2024), so a decline from 42% is plausible.

Net effect:
- Center the median in the low-30s (between the 27% low regime and the 42% spike), with a wide upper tail (possibility of sustained pull-forward).

----------------------------------------------------------------
STEP 5: EXTERNAL SIGNALS (CROWD)
----------------------------------------------------------------
Commenter benchmarks from prompt:
- Leo.li123: ~29.5% (27.5–31.3)
- Hasham: ~34.3% (27.6–40.1)

These are consistent with “mid-30s central tendency, wide uncertainty”.

----------------------------------------------------------------
STEP 6: FINAL DISTRIBUTION (ENTER THESE ON METACULUS)
----------------------------------------------------------------
Final forecast percentiles:
- p5: 22.0
- p25: 28.3
- p50: 32.2
- p75: 41.5
- p95: 50.9

----------------------------------------------------------------
STEP 7: VALIDATION / PRE-MORTEM
----------------------------------------------------------------
Main ways this forecast is wrong:
1) Sustained pull-forward continues: China stays near 40–50% again → distribution should shift right (median ~40).
2) Abrupt clampdown or licensing delays: China share returns toward ~20–27% → distribution should shift left (median ~25–28).
3) Denominator effect: non-China system sales surge (Taiwan/Korea) → China share falls even if China shipments are flat.

Sanity checks:
- Median sits between the low regime (27%) and the spike (42%).
- Wide tails reflect observed quarter-to-quarter swings.

----------------------------------------------------------------
STEP 8: UPDATE TRIGGERS
----------------------------------------------------------------
Update upward:
- Evidence of another pre-buying surge (policy rumors, distributor commentary, accelerated shipments).
- Q4 2025 disclosures show China share remains elevated (>=40%) in preliminary/credible reports.

Update downward:
- New export control tightening or licensing delays specific to DUV tools.
- Company commentary pointing to shipment deferrals to China or stronger non-China system shipment concentration.

Monitoring:
- `monitor_asml_china_share.py` checks for the `q4-2025` results page and tries to extract “China xx%” from the investor presentation PDF.

