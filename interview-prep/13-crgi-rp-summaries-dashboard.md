# CRGI RP Summaries Dashboard


13 — CRGI RP Summaries Dashboard

[| Repo: qrt“qh-croi-rp-Summariés - stack:

Plotly Dash, Python 3.11, Pandas, AWS S3, OKTA, EKS Your role: Built the multi-fund analytics dashboard.

Snapshot

sector/industry breakdowns, top/bottom holdings, Top-10 securities tracking,

STAR story — "One dashboard to compare many funds"

Situation. CRGI's research group tracked many funds’ Performance, sector exposures, and top holdings across scattered spreadsheets — no single comparative view.

Task. Build an interactive, access-controlled dashboard that unifies multi-fund analytics and refreshes automatically.

Action.

Built a Dash app with the standard layout/controls/callbacks structure (1
Rendered fund performance, sector/industry breakdowns, Top-

* Sourced data from $3 (populated by the cronjobs) with real
* Secured with OKTA auth + role-based access,

ayout py, controls -Py, callbacks py) and data loading in support_functions/load_data_py.
10 securities across funds, and PM rankings, with dynamic filtering by fund.

-time refresh, so th dashboard feflects the latest daily data without tedeploys.
and added user tracking (track_usage)

Py) for usage analytics, plus client-side PDF/image export (jsPDF, html2canvas) so PMs can export views.

Result. CRGI gets one comparative, always-current view across funds with governed access —

feplacing manual spreadsheet assembly.

Technical deep-dive & why ‘ ms

Why Dash (not the React micro-frontend)? Dash lets me build data-dense analytical das boards in pure Python, Teusing the same Pandas transforms as the Pipelines. For research/analytics Uls with lots of Plotly
charts and a Python-first team, it’s far faster to build than a bespoke React app. _ a

Why read from S3 instead of a DB? The cronjobs already land governed daily sna
* Why client-side export (jsPDF/htmi2canvas)? PMs live in PowerPoint/PDF. Rend
© Why user tracking? Usage analytics justify the tool and highlight which views ma

pshots in $3; the dashboard reads those directly — no DB tier to run, and point-in-time snapshots are naturally reproducible.
ering the export in the browser avoids a server-side headless-render service and keeps exports instant.
itter — and give an audit trail on a regulated research tool.

Code samples (real, extracted from the repo)

Load $3 snapshots into DataFrames once, then compose every view ( app/support_functions/load_ data. Py. abridged)

class LoadData: ay
def __init (self): =
data_obj = self.get_s3_object() # positions snapshot from $3




class LoadData: 7 : 2 =. — 5 "
def __init_ (self):
data_obj = self.get_s3_object()

self.amcap_df = pd.read_csy
self.base date =

; _ # positions snapshot from s3 a
(10-BytesI0(data_obj{"Body"] read())) Le =

pd.to_datetime(self.amcap_df["PositionDate"]).dt.strftime("%Y-%m-%d")
# master config (fund list,
obj = utils.s3_cgdata client
Master data =

RP names, column order) read straight from $3 Excel .
-get_object (Bucket-BUCKET_NAME, Key=FILE PATH + "/MasterFundRPCRGL.x1sx") yl
pd-read_excel (io. BytesI0(obj{ "Body"].read()), sheet_name="Sheet1", engine="openpyx1")

# pre-build every fund's tables ONCE at load time; callbacks just slice these e! iN
for fund_name, Yreport_name in zip(self.fund_names, ‘self. report_names) : z i 2

dfs = utils.generate_dataframes(fund_name) # sector/industry/issuer/PM rankings
self.fund_layout[ fund_name] = dfs 7 ee 4 :

| Talking point: the app reads pre-computed $3 snapshots (produced by the cronjol

all fund tables at load time, so interactive callbacks only slice in-memory frames — no live data pulls on click.

Likely follow-up Q&A 8S 4


Q: How does “real-time refresh from $3” work in Dash? A: The data-loadin.

ig layer reads the latest S3 snapshot (cached appropnately);
last-batch", which is what daily research data needs — not tick-level streamin

; when the cronjob lands new data, the next load/refresh picks it up. It's “

Q: How do you keep a chart-heavy Dash app responsive? A: Do the heavy aggregation once in th

e data layer (Pandas), cache the loaded frames,
recomputing from raw on every interaction. (Where needed, the Redis pattern from project 09 appli

ies.)

and keep callbacks lightweight — filter/slice Pre-computed frames rather

Q: How is access controlled? A: OKTA authentication at the platform ingress with role-based access, so only authorized CRGI research users Teach it usage is tracked per user.
