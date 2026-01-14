# Research Notes — US Manufacturing PMI (Feb 2026)

## Primary sources (resolution)
- S&P Global PMI press releases (PDF content):
  - Dec 2025 final (release dated 2026-01-02): `spglobal_us_mfg_pmi_2025_12_final.pdf`
  - Nov 2025 final (release dated 2025-12-02): `spglobal_us_mfg_pmi_2025_11_final.pdf`

## Proxy time series used for quantitative work
- ISM Manufacturing PMI history (long-run monthly series, used as a proxy for dynamics/volatility):
  - Investing.com event page: https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173
  - Raw scrape: `ism_event_history_raw.csv`
  - Clean monthly series: `ism_pmi_history.csv`

## Why a proxy is used
- The question resolves on S&P Global’s series, but a full historical time series for S&P Global US Manufacturing PMI was not reliably available via a simple public CSV pull in this repo.
- The model therefore uses ISM as a proxy for near-term dynamics and adds an empirically observed offset using the two latest months where both are known (Nov/Dec 2025).

## Metaculus crowd snippets (from prompt)
- nikakovskaya: 52.2 (51–53)
- ts1: 51.8 (50.4–53.1)
- SandroAVL: 49.2 (noted tail risk below 49)
