# CG Data Cronjob

10 — GG Data Cronjob (XpressFeed — Databricks migration flagship)
Repo: art-gh-frg-cg-data-cronjob * Stack: Python, Databricks SQL (M2M OAuth), LASR, Snowflake, AWS S3, Pandas, EKS CronJob Your role: Built the data pipeline and led its migration from XpressFeed to
Databricks.

There's a ~BACKUP/qrt—gh=frg-cg-data=exonj ob main =be foreld itabrit 5/ in the workspace — literal proof this was a migration. Strong “modernise a data Pipeline” story. i

Snapshot

holdings-analyzer data, CRGI/CWIT10 files, and dashboard triggers. The headline engineering was migrating the data source from S&P XpressFeed to

“A set of daily data pipelines feeding downstream FRG apps —
and validating the new numbers matched the old.”

Databricks, which meant implementing Databricks’ native machine-to-machine OAuth client-credentials auth with token caching,

STAR story — "Migrate a Production data pipeline onto Databricks without breaking the numbers"

Situation. The pipeline sourced data via XpressFeed. The firm was standardising on Databi ic


Task. Re-platform the pipeline onto Databricks SQL. authenticate securely, and poate Parity before cutover — keeping the old version as a rollback.

* Builta \databricks client using the native M2M OAuth client-credentials flow: POST: BRGSH VARS

apis), gets an access token, and caches it with a 60-second pre-expiry buffer so it refreshes before expiry rather than failing mid-query.

* Implemented the credentials provider to satisfy databricks—sql-connector) 4x's ExtérnalAuthProvider protocol (header-factory pattern), and honoured the corporate CA bundle

(SSL_CERT_FILE/ REQUESTS_CA_BUNDLE) for TLS against internal endpoints. 4 ze
* Organised jobs cleanly: jobs/ (holdings-analyzer pipeline, CRGI/CWI T10 generation, dashboard triggers, dbx_connectivity_test ), utilities/ (databricks/lasr/xf clients, Position processor, s3_io, scheduler,

email alerts), and tools/ (cache loader, schema exporter).
* Kept XpressFeed and LASR clients side by side during migration to compare outputs and prove parity, and wrote tests (test_dbx client. test_benchmark snowflake, test earnings actuals).

° Preserved the email-alert status reporting and S3 archival (archive/lasr_ data {date}.

trade on. The numbers cannot change silently.

Action. Za

client credential to the Databricks OIDC token endpoint ( /oidc/V1/tokén.

* Kept the pre-Databricks version archived as an instant rollback path.

Result. The pipeline runs on Databricks with secure token-managed auth, validated to match the prior XpressFeed output, with the old version retained for rollback and daily email/S3 audit intact.

Technical deep-dive & why 1


Why M2M OAuth (client-credentials) not a personal access token? A cronjob is a service, not a person. Client-credentials

or rotate manually, Client id/secret come from secrets, not code.

back out instantly if they diverged.
* Why keep the old repo as _before-databricks ? Rollback. If prod broke post-cutover, revert

* Why archive each run to S3 with a dated key + a stable current key? Consumers read the stable current key; the dated archive gives point-

Code samples (real, extracted from the repo)

person. Client-credentials gives it its own identity with a short-lived, auto-

to a known-good pipeline in minutes.

Native M2M OAuth (client-credentials) with pre-expiry token refresh (cronjob/uti

class _DatabricksM2MCredentialsProvider:
"""A cronjob is a service,

def _refresh_token(self) —> str:
resp = requests. post(

f"{self._host}/oidc/v1/token",

data={
"grant_type": “client_credentials",
"client_id": self._client_id,
"client_secret": self._client_secret, #
"scope": "all—apis", =

timeout=36,
verify=CA_BUNDLE PATH or True,
resp.raise_for_status()
data = resp. json() ! a
self._token = data["
# 60-second buffer:
self._token_expiry
return self._token

access_token"] j
Fefresh BEFORE actual expiry so a tong
time.time() + data["expires in"] — 60

Likely follow-up Q&A F

query automatically.

: zi Ue
Q How did you prove the Databricks numbers matched XpressFeed? A: Kept both clients li
breaking and non-determinism — See project 11). Cutover only after parity held, _ 2

Q: What broke or surprised you in the migration? A: Auth was the first hurdle — connector 4.x needs the
subtle ordering/currency differences produced tiny diffs that had to be

Q: How is the cronjob scheduled and monitored? A: Kubernetes Cronlob on EKS; each run emails a status

runnable per date.

Q: Why Databricks over Snowflake/XpressFeed for this? A: Firm-wide standardisation on Databricks + Unity Catalog/LASR as the governed data platform

not to pick it.

# machine-to-machine,

_ # from Secrets, never in code

# honour the corporate CA bundle for TLS

guery never fails mid-flight

understood before trusting the source.

no user

ExternalAuthProvider header-factory protocol, and intemal TLS needs the corporate CA bundle. On data,

re.

table (source, latest date, comments) and archives to S3. Failures are visible via the alert + pod logs, and jobs are

— one lineage. one access model. My job was to move safely onto it,
