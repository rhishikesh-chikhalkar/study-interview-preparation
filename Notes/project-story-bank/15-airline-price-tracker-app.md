# 15 — Airline Price Tracker App

- **Repo**: `qra-qh-frg-airline-price-tracker-app`
- **Stack**: Plotly Dash, Plotly, Pandas, AWS S3, client-side JS (jsPDF/html2canvas), EKS
- **Your Role**: Built the tracking dashboard, including a custom data parser and client-side PDF export.

## Snapshot (30-second pitch)
"A Plotly Dash dashboard that tracks and visualises airline pricing data. It has a dedicated data parser that normalises the raw pricing feed into analysis-ready frames, reads from S3, and offers client-side PDF/image export of any view (jsPDF + html2canvas) so analysts can share snapshots."

---

## STAR Story — "Track airline prices and make any view shareable"

- **Situation**: Airline pricing data arrived in a raw form that wasn't directly chart-ready, and analysts wanted to visualise trends and export specific views.
- **Task**: Build a dashboard that parses the raw feed, visualises pricing trends, and lets users export views to PDF.
- **Action**:
  - Wrote a dedicated parser (`data/parser.py`) to transform the raw pricing feed into clean, analysis-ready DataFrames — isolating messy parsing from the visualisation code.
  - Built the Dash app (layout/controls/callbacks) reading data via `support_functions/load_data.py` from S3, with shared `utils.py` helpers.
  - Added client-side export using bundled JS libraries (jsPDF, html2canvas, canvg) so users export the current view to PDF/image directly in the browser.
  - Kept local vs deployed entrypoints (`app_local.py` vs `app.py`) for fast local iteration.
- **Result**: Analysts get a clean, interactive view of airline pricing trends and can export any view to PDF instantly — no manual data wrangling.

---

## Technical Deep-Dive & Why

1. **Why a separate parser module?**
   - Raw feeds are messy; isolating parsing (`data/parser.py`) from layout/callbacks keeps the transform independently testable and stops parsing bugs from tangling with UI logic. Single responsibility.

2. **Why client-side PDF export?**
   - It renders the exact on-screen view without a server-side headless browser, so exports are instant and the server stays stateless — ideal for EKS.

3. **Why local vs prod entrypoints?**
   - `app_local.py` runs against local/sample data for quick iteration; `app.py` is the deployed configuration. Faster feedback loop without touching prod config.

4. **Why S3-backed?**
   - Same pattern as the other dashboards — a pipeline lands snapshots in S3, the app just reads them and stays fast and stateless.

---

## Likely Follow-up Q&A

- **Q: What was the hardest part — the charts or the data?**
  - **A**: The data. Raw pricing feeds have inconsistent formats/gaps; the parser does the real work (normalising, typing, handling missing points) so the visualisation layer receives clean frames.

- **Q: How does client-side export actually work?**
  - **A**: html2canvas rasterises the DOM node of the current view to a canvas, and jsPDF wraps that image into a PDF the browser downloads — all client-side, no server round-trip.

- **Q: How would you productionise the parser further?**
  - **A**: Move it into the cronjob tier so parsing happens once offline (like the other pipelines), unit-test it against fixture feeds, and land clean parquet/CSV in S3 so the dashboard does zero parsing at render time.
