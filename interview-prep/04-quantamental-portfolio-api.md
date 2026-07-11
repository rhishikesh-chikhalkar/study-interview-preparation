# Quantamental Portfolio API

04 — Quantamental Portfolio API ae 7

Repo: art-gh-frg-quantamental-portfolio-api |- Stack: Flask 2.0 + Flask-RESTX, Flask-OIDC (OKTA), Tornado (WSG)), Pandas, XlsxWriter, Boto3/S3, Airflow, EKS Your role: Built the API that generates portfolio
i i :

dashboards and triggers construction workflows. ‘ Hi =
! iy \

Snapshot

“A Flask REST API that generates Excel portfolio- management dashboards for the CWI/CRGI/CIl investment teams. It combines CG Equity Holdings, S&P XpressFeed fundamentals, and S&P 500 index data into multi-sheet Excel
reports, lets teams upload/download override files to $3, and triggers Airflow DAGs to kick off portfolio-construction workflows. It's OKTA-secured with AD-group authorization and served via Tornado.”

STAR story — “Automate the analysts' Excel dashboard and wire it to the pipeline"

Situation. FRG investment teams manually assembled Portfolio dashboards from several data sources and hand-managed override files — tedious and inconsistent across divisions.
Task. Build a secure API that generates the dashboard on demand, manages overrides centrally, and can trigger the downstream construction pipeline. i
Action. an :

* Built a Flask + Flask-RESTX AP! (auto Swagger docs) served by Tornado as the WSGI container.

* Integrated three data sources — CG Equity Holdings API, XpressFeed CiQ fundamentals, and S&P 500 index — and produced multi-sheet Excel output with XlsxWriter.
* Implemented OKTA OIDC auth with Flask-OIDC, building the OKTA client-secrets JSON config at runtime from env vars into a temp file (nothing sensitive in the image), plus an Okta UsersClient for user lookups and AD-

group-based authorization. he
* Added S3 override management (upload/download Portfolio Overrides.xlsx) with secure_filename.
* Added a scheduler integration to trigger Airflow DAGs so a dashboard action can launch the portfolio-construction workflow.

ename handling for uploads.

* Enabled Flask-Compress to shrink large Excel/JSON responses over the wire.

Result. Teams generate consistent dashboards on demand instead of assembling them by hand, overrides live in one governed S3 location, and the API bridges directly into the Airflow pipeline.

Technical deep-dive & why

° Why Flask + Flask-RESTX here (vs FastAPI elsewhere)? This service is request/response and document-generation heavy, and it lived in a Flask-standard estate with OKTA via Flask-OIDC. RESTX gives Swagger + request

parsing. Consistency with the existing division services mattered more than async here.
* Why build the OKTA config JSON at runtime? The client secret and URIs are environment-specific and sensitive, Writing them to a temp file at startup keeps secrets out of source and the image, and lets the same build”

run in dev and prod with different env.
* Why AD-group authorization? Divisions (CWI/CRGI/CIl) must only see their own data. Mapping OKTA group membership to access is the firm's standard and avoids a bespoke permission store. |,

* Why Tornado as the server? It's the platform-standard WSGI container for these Flask apps and handles the concurrency profile (mostly I/O + report generation) well.
* Why secure_filename on uploads? Uploaded override filenames are untrusted input — this prevents path traversal when the file is written to S3/temp.

Code samples (real, extracted from the repo)

Build the OKTA client-secrets JSON at runtime from env vars — no secrets in source/image (app/app. py), abridged)

okta_dict = {
"web": {
client_id": os.environ["client_id"],
client_secret": os-environ["client_secret"],
“auth_uri": os-environ["auth_uri"],
"token_uri": os.environ["token_uri"],
"issuer": os.environ["issuer"],
userinfo_uri": os.environ["userinfo_uri"],
"redirect_uris": [f https://{os-environ[ ‘ingress hostname! ]}/oidc/callback"]

okta_file = os-.path. Join(tempfile. mkdtemp(),
with open(okta_file, "w") as f:

"okta_config. json")
json.dump(okta_dict, f)

# written to a temp file, never committed
app-config[ "OIDC_CLIENT_SECRETS"] = okta file
app.config[ “OIDC_SCOPES"] = ["openid", "email", "profile"]
Gide = OpenIDConnect (app)

# Flask-OIDC handles redirect/callback
okta_client = UsersClient(OKTA_BASE_URL, API _TOKEN)

Safe upload handling (app/app-py)

from werkzeug.utils import secure_filename
filename = secure_filename(uploaded. filename)

Likely follow-up Q&A

users client / token claims) to authorize the division-specific action.

# strips path-traversal (../) from untrusted input

Q: How does OKTA OIDC actually flow here? A: Flask-OIDC handles the OpenID Connect redirect/callback (/oidc/callback); after login the user gets an ID-token cookie. | then check the user's AD groups Keg SLE

Q: Generating big Excel files can be slow/memory-heavy — how did you handle it? A: Write to an in memory BytesIO with XisxWriter,

scheduled builds, the heavy construction is pushed to the Airflow DAG rather than done inline.

Q: Why trigger Airflow instead of doing the work in the request? A: Portfolio construction is long-running and orchestrated with dependencies/retries. Airflow is built for that; the API Just triggers the DAG and returns,
keeping the request fast and the workflow observable.

stream it back as an attachment, and enable Flask-Compress. For very large or
