# 13 — CRGI RP Summaries Dashboard

- **Repo**: `qrt-qh-crgi-rp-summaries`
- **Stack**: Plotly Dash, Python 3.11, Pandas, AWS S3, OKTA, EKS
- **Your Role**: Built the multi-fund analytics dashboard.

## Snapshot (30-second pitch)
"A Plotly Dash dashboard that gives CRGI's research group a single comparative view across multiple funds — fund performance, sector/industry breakdowns, top/bottom holdings, Top-10 securities tracking, and PM rankings, with dynamic filtering by fund. Data comes from S3 snapshots with real-time refresh, secured with OKTA auth and per-user tracking."

---

## STAR Story — "One dashboard to compare many funds"

- **Situation**: CRGI's research group tracked many funds' performance, sector exposures, and top holdings across scattered spreadsheets — no single comparative view.
- **Task**: Build an interactive, access-controlled dashboard that unifies multi-fund analytics and refreshes automatically.
- **Action**:
  - Built a Dash app with the standard layout/controls/callbacks structure (`layout.py`, `controls.py`, `callbacks.py`) and data loading in `support_functions/load_data.py`.
  - Rendered fund performance, sector/industry breakdowns, Top-10 securities across funds, and PM rankings, with dynamic filtering by fund.
  - Sourced data from S3 (populated by the cronjobs) with real-time refresh, so the dashboard reflects the latest daily data without redeploys.
  - Secured with OKTA auth + role-based access, and added user tracking (`track_usage.py`) for usage analytics, plus client-side PDF/image export (jsPDF, html2canvas) so PMs can export views.
- **Result**: CRGI gets one comparative, always-current view across funds with governed access — replacing manual spreadsheet assembly.

---

## Technical Deep-Dive & Why

1. **Why Dash (not the React micro-frontend)?**
   - Dash lets me build data-dense analytical dashboards in pure Python, reusing the same Pandas transforms as the pipelines. For research/analytics UIs with lots of Plotly charts and a Python-first team, it's far faster to build than a bespoke React app.

2. **Why read from S3 instead of a DB?**
   - The cronjobs already land governed daily snapshots in S3; the dashboard reads those directly — no DB tier to run, and point-in-time snapshots are naturally reproducible.

3. **Why client-side export (jsPDF/html2canvas)?**
   - PMs live in PowerPoint/PDF. Rendering the export in the browser avoids a server-side headless-render service and keeps exports instant.

4. **Why user tracking?**
   - Usage analytics justify the tool and highlight which views matter — and give an audit trail on a regulated research tool.

---

## Code Samples

### Load S3 snapshots into DataFrames once, then compose every view (`app/support_functions/load_data.py`, abridged)
```python
class LoadData:
    def __init__(self):
        data_obj = self.get_s3_object()  # positions snapshot from S3
        self.amcap_df = pd.read_csv(io.BytesIO(data_obj["Body"].read()))
        self.base_date = pd.to_datetime(
            self.amcap_df["PositionDate"]
        ).dt.strftime("%Y-%m-%d")

        # master config (fund list, RP names, column order) read straight from S3 Excel
        obj = utils.s3_cgdata_client.get_object(
            Bucket=BUCKET_NAME,
            Key=FILE_PATH + "/MasterFundRPCRGI.xlsx"
        )
        master_data = pd.read_excel(
            io.BytesIO(obj["Body"].read()),
            sheet_name="Sheet1",
            engine="openpyxl"
        )

        # pre-build every fund's tables ONCE at load time; callbacks just slice these
        for fund_name, report_name in zip(self.fund_names, self.report_names):
            dfs = utils.generate_dataframes(fund_name)  # sector/industry/issuer/PM rankings
            self.fund_layout[fund_name] = dfs
```

**Talking point**: The app reads pre-computed S3 snapshots (produced by the cronjobs) and pre-builds all fund tables at load time, so interactive callbacks only slice in-memory frames — no live data pulls on click.

---

## Likely Follow-up Q&A

- **Q: How does "real-time refresh from S3" work in Dash?**
  - **A**: The data-loading layer reads the latest S3 snapshot (cached appropriately); when the cronjob lands new data, the next load/refresh picks it up. It's "fresh as of last batch", which is what daily research data needs — not tick-level streaming.

- **Q: How do you keep a chart-heavy Dash app responsive?**
  - **A**: Do the heavy aggregation once in the data layer (Pandas), cache the loaded frames, and keep callbacks lightweight — filter/slice pre-computed frames rather than recomputing from raw on every interaction. (Where needed, the Redis pattern from project 09 applies.)

- **Q: How is access controlled?**
  - **A**: OKTA authentication at the platform ingress with role-based access, so only authorized CRGI research users reach it; usage is tracked per user.
