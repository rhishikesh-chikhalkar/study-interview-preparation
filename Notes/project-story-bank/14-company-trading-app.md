# 14 — Company Trading Multiples App

- **Repo**: `qra-gh-frg-company-trading-app`
- **Stack**: Plotly Dash 2.15, Plotly 5.5, Python, Pandas, AWS S3, EKS
- **Your Role**: Built the interactive multiples dashboard (front end for the trading-multiples cronjobs).

## Snapshot (30-second pitch)
"A Plotly Dash app that lets analysts explore historical valuation multiples (P/E, P/B, dividend yield, EV/EBIT) for semiconductor and gaming companies, compare them against sector indices, and export charts/tables to Excel and Word for research notes. It reads pre-computed data from S3 — the serving tier for the trading-multiples cronjobs."

---

## STAR Story — "Give analysts an interactive multiples explorer with exports"

- **Situation**: Analysts needed to explore historical valuation multiples for semis and gaming companies and compare them against sector indices, then drop the results into Excel/Word for research notes.
- **Task**: Build an interactive dashboard with flexible time ranges, index comparisons, and native Excel/Word export.
- **Action**:
  - Built a Dash app (layout/controls/callbacks) with company-specific charts and selectable time ranges (YTD, 1Y, 5Y, 10Y, All).
  - Added index comparisons (Asia Foundry, Memory Foundry, SemiCap Equipment, Asia Gaming) so a company's multiple is seen against its peer index.
  - Implemented Excel and Word exports so a chart/table becomes a research artifact in one click.
  - Read daily-refreshed data from S3 (from the cronjobs), keeping the UI fast by never calling Capital IQ live.
  - Added helper/tracker modules (`helper_functions.py`, `tracker.py`) for shared logic and usage tracking.
- **Result**: Analysts explore multiples interactively and export straight to Excel/Word — the tool replaced manual data assembly and is integrated into their research workflow.

---

## Technical Deep-Dive & Why

1. **Why a separate app from the cronjobs?**
   - Batch tier (cronjobs) and serving tier (dashboard) deploy independently. A pipeline failure doesn't take down the app — the last good S3 snapshot still renders. Each layer scales independently.

2. **Why server-generated Excel/Word (vs client export)?**
   - These exports are structured documents (formatted tables, multiple sheets/sections), not just a screenshot — generating them server-side with the underlying data gives analysts a real, editable artifact.

3. **Why configurable time ranges + index overlays?**
   - Valuation analysis is inherently relative — over time and vs peers. Making range and index first-class controls means analysts can do their comparative analysis directly instead of building their own charts.

---

## Likely Follow-up Q&A

- **Q: Where does the data come from at render time?**
  - **A**: S3 snapshots produced by the trading-multiples cronjobs. The dashboard reads pre-computed data — no live Capital IQ calls — so even if Capital IQ is slow, the latest snapshot still renders.

- **Q: How do you keep this app and the cronjobs consistent?**
  - **A**: The app reads exactly what the cronjob writes to S3 — same columns, same schema. The cronjob is the single source of truth for the data; the app is a read-only consumer.

- **Q: How would you add a new company universe?**
  - **A**: Add a new pull module in the cronjobs (same pattern as semi/gaming), land it in S3, and add a tab/filter in the dashboard. The architecture is designed for this — one cronjob per universe, one shared dashboard.
