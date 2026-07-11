# 16 — BRZ App

- **Repo**: `qra-gh-frg-brz-app`
- **Stack**: Plotly Dash, Plotly, Pandas, AWS S3, EKS
- **Your Role**: Built a multi-dimensional analytics dashboard.

## Snapshot (30-second pitch)
"A Plotly Dash analytics dashboard that slices a business dataset along multiple dimensions — by category and by product, with additional cuts (the CEP/CLA analysis modules). Each analysis dimension is its own module, composed into one dashboard, reading from S3 with per-user tracking."

---

## STAR Story — "One dashboard, many analytical cuts, kept maintainable"

- **Situation**: Stakeholders wanted to analyse the same dataset from several angles — by category, by product, and other dimensions — in one place, without a tangle of copy-pasted chart code.
- **Task**: Build a dashboard that supports multiple analysis dimensions while staying maintainable as more cuts are added.
- **Action**:
  - Split each analysis dimension into its own module under `support_functions/` (`by_category.py`, `by_product.py`, `cep.py`, `cla.py`), each owning its transforms and figures.
  - Kept the standard Dash layout/controls/callbacks split and a shared `load_data.py` reading from S3, so all dimensions consume one consistent data source.
  - Added per-user tracking (`tracker.py`) and a Jinja `templates/` layer for shared presentation.
  - Kept `app_local.py` for local iteration vs `app.py` for deployment.
- **Result**: A single dashboard offering multiple analytical views, structured so a new dimension is a new module, not a rewrite.

---

## Technical Deep-Dive & Why

1. **Why one module per analysis dimension?**
   - Separation of concerns and extensibility. Each dimension (category/product/etc.) has its own aggregation and charts; isolating them means changing one cut can't break another, and adding a cut is additive. This is the maintainability lesson from building several Dash apps.

2. **Why the shared `load_data` + S3 pattern?**
   - Every dimension analyses the same underlying data; loading it once in a shared module guarantees consistency across views and one place to cache.

3. **Why templates + tracker?**
   - Templates keep repeated presentation DRY; tracking gives usage insight and an audit trail — consistent with the other FRG dashboards.

---

## Likely Follow-up Q&A

- **Q: How would you add a new analysis dimension?**
  - **A**: Add a new module under `support_functions/` implementing that cut's transform + figures, register it in the layout/callbacks, and it reuses the shared data loader. No changes to existing dimensions.

- **Q: How do you keep multiple heavy views performant?**
  - **A**: Load and cache the shared frame once; each dimension slices/aggregates from it in its callback rather than reloading raw data. If a cut is expensive, pre-compute it in the pipeline tier.

- **Q: What's the reusable pattern across all your Dash apps?**
  - **A**: `app.py` / `app_local.py` entrypoints, layout/controls/callbacks split, `support_functions` for data + per-dimension logic, S3-backed data from cronjobs, OKTA at the ingress, and per-user tracking. Consistency across apps makes them easy to hand over and maintain.
