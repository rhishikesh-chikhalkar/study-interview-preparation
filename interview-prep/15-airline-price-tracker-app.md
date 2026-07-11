# Airline Price Tracker



15 — Airline Price Tracker App

Repo: gra—qh-frgq-ai Line—price=tracker2app - stack Plotly Dash, Plotly, Pandas, AWS S3, client-side JS (sPDF/htmi2canvas), EKS Your role: Built the tracking dashboard, including 3 custom data parser and _
client-side PDF export. Bs ae

Snapshot

“A Plotly Dash dashboard that tracks and visualises airline Pricing data. It has a dedicated data parser that normalises the raw Pricing feed into analysis-ready frames, reads from 53, and offers client-side PDF/image export of
any view (jsPDF + html2canvas) so analysts can share snapshots." : the

STAR story — "Track airline Prices and make any view shareable"

Situation. Airline pricing data arrived in a raw form that wasn't directly chart-ready, and analysts wanted to visualise trends and export specific views.
Task. Build a dashboard that Parses the raw feed, visualises Pricing trends, and lets users export views to PDF.

Action. = Be

© Wrote a dedicated Parser ( data/parser. py) to transform the Taw pricing feed into clean, analysis-ready DataFrames — isolating messy parsing from the visualisation code. a
° Built the Dash app (layout/controls/callbacks) reading data via’ support_functions/load_dat from $3, with shared Uti1S - py helpers.

* Added client-side export using bundled JS libraries (sPDF, html2canvas, canvg) SO us Ts export the current view to PDF/image directly in the browser.

* Kept local vs deployed entrypoints (app_local_ PY vs ‘app. py) for fast local iteration. i;

Result. Analysts get a clean, interactive view of airline pricing trends and can export any view to PDF instantly — no manual data wrangling.

Technical deep-dive & why bd

* Why a separate parser module? Raw feeds are messy; isolating parsing (data/parser. Py) from layout/callbacks keeps the transform independently testable and stops Parsing bugs from tangling with UI logic. Single

responsibility.
* Why client-side PDF export? It renders the exact on-screen view without a server-side headless browser, so exports are instant and the server stays stateless — ideal for EKS.

* Why local vs prod entrypoints? app_local.py runs against local/sample data for quick iteration; app. py is the deployed configuration. Faster feedback loop without touching prod config.

* Why S3-backed? Same pattern as the other dashboards — a Pipeline lands snapshots in S3, the app just reads them and stays fast and stateless.

Likely follow-up Q&A

— the charts or the data? A: The data. Raw Pricing feeds have inconsistent formats/gaps; the parser does the real work (normalising, typing, handling missing points) so the visualisation layer

Q: What was the hardest part
receives clean frames.
Q: How does client-side export actually work? A: html2canvas rasterises the DOM node of the current view to a canvas, and JsPDF wraps that image into a PDF the browser downloads — all client-side. no server round-trip.

Q: How would you productionise the parser further? A: Move it into the cronjob tier so parsing happens once offline (like the other pipelines), unit-test it against fixture feeds, and land clean parquet/CSV in S3 so the

dashboard does zero parsing at render time.




16 — BRZ App

| Repo: Qra—gh-frg-brz—app - Stack: Plotly Dash, Plotly, Pandas, AWS $3, EKS Your role: Built a multi-dimensional analytics dashboard.

Snapshot

‘A Plotly Dash analytics dashboard that slices a business dataset along multiple dimensions — by category and by product, with additional cuts (the €ep / Cla analysis Modules). Each analysis dimension is its own module,

composed into one dashboard, treading from $3 with Per-user tracking.”

STAR story — "One dashboard, many analytical cuts, kept maintainable"

Situation. Stakeholders wanted to analyse the same dataset from several angles — by category, by product, and other dimensions — in one place, without a tangle of copy-pasted chart code. It

Task. Build a dashboard that supports multiple analysis dimensions while staying maintainable as more cuts are added.

Action.
(by_category.py, by_product.py, cep.py, cla. PY), each owning its transforms and figures.

* Split each analysis dimension into its own module under Support_functions/
¥ Treading from $3, so all dimensions consume one consistent data source.

© Kept the standard Dash layout/controls/callbacks split and a shared load_data. p
* Added per-user tracking (tracker. Py) and a Jinja templates/ layer for shared presentation.
© Kept app_local. PY for local iteration vs app-.py for deployment. fe

structured so a new dimension is a new module not a rewrite.

Technical deep-dive & why

isolating them means changing one cut can’t break another, and

Result. A single dashboard offering multiple analytical views,

category/product/etc.) has its own aggregation and charts;

loading it once in a shared module guarantees consistency across views and one place to cache.
it and an audit trail — consistent with the other FRG dashboards.

Why one module per analysis dimension? Separation of concerns and extensibility. Each it
adding a cut Is additive. This is the maintainability lesson from building several Dash apps.
Why the shared load_data + $3 pattern? Every dimension analyses the same underlying data;

Why templates + tracker? Templates keep repeated presentation DRY; tracking gives usage insigh'

Likely follow-up Q&A
Q: How would you add a new analysis dimension? A: Add a new module under support_functions/ implementing that cut's transform + figures, register it in the layout/callbacks, and it reuses the shared data loader.

No changes to existing dimensions.
Q: How do you keep multiple heavy views performant? A: Load and cache the shared frame once; each dimension slices/aggregates from it in its callback rather than reloading raw data. If a cut is expensive, pre-compute it in

the pipeline tier.

