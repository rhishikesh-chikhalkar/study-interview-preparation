# Quantamental Portfolio Data API

05 — Quantamental Portfolio Data API


- **Stack**: Flask 2.1 + Flask-RESTX, Flask-OIDC (OKTA), Tornado, Pandas, Boto3/S3, Flask-Compress, EKS
- **Your Role**: Built the API that acts as a secure, division-controlled bridge between Excel tools and S3.

Excel tools and $3.

Snapshot

“A Flask API that acts as a secure, division-controlled bridge between Capital Grou and delete CSVs; access is scoped
a it)

p's Quantamental Excel models and $3 data storage. Analysts’ Excel/VBA tools call it to upload, retrieve,
investment division (CWI, CRGI, CII, CFIL, ALL) with OKTA auth and AD-group authorization, and every action is tracked via the QuantHub tracker API for audit."

STAR story — “Let Excel talk to S3 — safely and with an audit trail"

Situation. Analysts wanted their Excel Quantamental models to read/wnite shared data, but giving Excel direct $3 credentials is a security and governance nightmare — no per-division control, no audit.

Task. Provide a secure API layer so Excel tools access only their division's data, with authentication and full activity tracking.

Action.

* Built division-scoped endpoints (CWI/ CRGI/ CII / CFI / All), each mapping to a structured S3 prefix, so a division can’t read another's data.

* Secured with OKTA OIDC (Flask-OIDC) and AD-group authorization per division. is

* Implemented upload / retrieve / delete of CSVs to/from $3 with Boto3, designed to be callable from VBA (simple, VBA-friendly request/response contracts).
Added user-activity tracking via the QuanHub tracker AP! on each call — an audit trail of who did what. ;

* Enabled Flask-Compress for large CSV payloads and served via Tornado.

Result. Excel models securely read/write shared data with no embedded AWS credentials, each division sees only its own data, and every access is auditable.

Technical deep-dive & why

* Why an API in front of S3 instead of direct S3 access from Excel? Three reasons: (1) no credentials in Excel — the API holds them server-side via IAM/secrets; (2) authorization — division scoping enforced centrally;

(3) auditability — every call is tracked. Direct S3 gives you none of these.
* Why division-based endpoints? Explicit division scoping is simpler and safer than a generic “path” parameter that could be abused to reach another division's prefix.
* Why track every action? This is regulated financial data; who-touched-what is a compliance requirement, not a nice-to-have.
* Why VBA-friendly contracts? The consumers are Excel tools — keeping request/response shapes simple means the VBA side stays maintainable.

Code samples (real, extracted from the repo)

Division scoping enforced server-side — you cannot write into another division's folder ( app/app.py. abridged)

def put_data(df_json, division, file_key):


’ Code eaniples (real, extracted from the repo) Mh : i
Division scoping enforced server-side — you cannot write into another division’ ‘s folder

Ta Wa

File. key = ‘rite key. secant
if file_key[0] == '/':
file_key =" + file key 2
if division not in file_key.split( : =
file_key = "/" + division + "/" + file_key
s3_key = Default. _Path + file Key = =

| if not 83. | key. endswith(*.csv"): ae =

role s pd.read_json(io.StringIO(af_json), « ora r split") i 3 -

| # cross—check the DATA's own division code against the requested division ie

if “investmentdivisioncode" in df.columns and division != "All": uF ih :
file_division_codes = df({"investmentdivisioncode"].dropna(). drop_duplicates(). tolist() (an : lf

file_divisions = [divisions _mappingle] for c in file_division _codes] ; i = ie

if not (len(file_divisions) == 1 and division in file _divisions

raise ValueError(f"{file_ divisions} cannot be loaded into {

ivision) folder") Ee

esv_buffer = io.StringI0(); df.to_csv(csv_buffer, index=False) 2 =) a
$3_resource.Object(BUCKET_NAME, s3_key) - put (Body=csv_buffer.getvalue())
return {"File Saved Successfully to ": file_key} 2 i :

| Talking point: authorization is enforced twice — the path is pinned to the caller's division, and the file's own

Likely follow- “up Q&A

Q: How do you stop division A from reading division B's data? A: The endpoint itself is bound to a division and its S3 prefix. and the caller's OKTA/AD group is checked against that divi:

that could traverse to another prefix.

Q: How is this different from the Quantamental Portfolio API (project 04)? A: 04 generates dashboards and triggers Airflow. This one (05) is the data plane — a thin, secure CRUD bridge bD

division scoping and audit. Different responsibilities, shared auth pattern.

Q: What about concurrent writes to the same CSV? A: Writes are per-division, per-file and last-write-wins at the object level; for the models’ usage pattern (one owner per division meet
I'd add object versioning on the $3 bucket and optimistic checks.

