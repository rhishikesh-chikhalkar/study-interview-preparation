# 10 — CG Data Cronjob (XpressFeed → Databricks migration flagship)

- **Repo**: `art-gh-frg-cg-data-cronjob`
- **Stack**: Python, Databricks SQL (M2M OAuth), LASR, Snowflake, AWS S3, Pandas, EKS CronJob
- **Your Role**: Built the data pipeline and led its migration from XpressFeed to Databricks.

> There's a `~BACKUP/art-gh-frg-cg-data-cronjob_main_before-databricks/` in the workspace — literal proof this was a migration. Strong "modernise a data pipeline" story.

## Snapshot (30-second pitch)
"A set of daily data pipelines feeding downstream FRG apps — holdings-analyzer data, CRGI/CWI T10 files, and dashboard triggers. The headline engineering was migrating the data source from S&P XpressFeed to Databricks, which meant implementing Databricks' native machine-to-machine OAuth client-credentials auth with token caching, and validating the new numbers matched the old."

---

## STAR Story — "Migrate a production data pipeline onto Databricks without breaking the numbers"

- **Situation**: The pipeline sourced data via XpressFeed. The firm was standardising on Databricks as the governed data platform.
- **Task**: Re-platform the pipeline onto Databricks SQL, authenticate securely, and prove parity before cutover — keeping the old version as a rollback.
- **Action**:
  - Built a Databricks client using the native M2M OAuth client-credentials flow: POST client credentials to the Databricks OIDC token endpoint (`/oidc/v1/token`), get an access token, and cache it with a 60-second pre-expiry buffer so it refreshes before expiry rather than failing mid-query.
  - Implemented the credentials provider to satisfy `databricks-sql-connector` 4.x's `ExternalAuthProvider` protocol (header-factory pattern), and honoured the corporate CA bundle (`SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`) for TLS against internal endpoints.
  - Organised jobs cleanly: `jobs/` (holdings-analyzer pipeline, CRGI/CWI T10 generation, dashboard triggers, `dbx_connectivity_test`), `utilities/` (databricks/lasr/xf clients, position processor, s3_io, scheduler, email alerts), and `tools/` (cache loader, schema exporter).
  - Kept XpressFeed and LASR clients side by side during migration to compare outputs and prove parity, and wrote tests (`test_dbx_client`, `test_benchmark_snowflake`, `test_earnings_actuals`).
  - Preserved the email-alert status reporting and S3 archival (`archive/lasr_data_{date}`).
  - Kept the pre-Databricks version archived as an instant rollback path.
- **Result**: The pipeline runs on Databricks with secure token-managed auth, validated to match the prior XpressFeed output, with the old version retained for rollback and daily email/S3 audit intact.

---

## Technical Deep-Dive & Why

1. **Why M2M OAuth (client-credentials) not a personal access token?**
   - A cronjob is a service, not a person. Client-credentials gives it its own identity with a short-lived, auto-refreshed token — no long-lived PAT to leak or rotate manually. Client id/secret come from secrets, not code.

2. **Why a 60-second pre-expiry token refresh buffer?**
   - If a token expires mid-query, the query fails. Refreshing 60 seconds before actual expiry ensures a long query never fails mid-flight.

3. **Why keep the old repo as `_before-databricks`?**
   - Rollback. If prod broke post-cutover, revert to a known-good pipeline in minutes.

4. **Why archive each run to S3 with a dated key + a stable current key?**
   - Consumers read the stable current key; the dated archive gives point-in-time reproducibility and audit trail.

---

## Code Samples

### Native M2M OAuth (client-credentials) with pre-expiry token refresh (`cronjob/utilities/databricks_client.py`, abridged)
```python
class _DatabricksM2MCredentialsProvider:
    """A cronjob is a service, not a person — machine-to-machine OAuth."""

    def _refresh_token(self) -> str:
        resp = requests.post(
            f"{self._host}/oidc/v1/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,  # from Secrets, never in code
                "scope": "all-apis",
            },
            timeout=30,
            verify=CA_BUNDLE_PATH or True,  # honour the corporate CA bundle for TLS
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        # 60-second buffer: refresh BEFORE actual expiry so a long query never fails mid-flight
        self._token_expiry = time.time() + data["expires_in"] - 60
        return self._token
```

---

## Likely Follow-up Q&A

- **Q: How did you prove the Databricks numbers matched XpressFeed?**
  - **A**: Kept both clients live during migration and diffed outputs over production date ranges — any difference was investigated (including non-determinism — see project 11). Cutover only after parity held.

- **Q: What broke or surprised you in the migration?**
  - **A**: Auth was the first hurdle — connector 4.x needs the `ExternalAuthProvider` header-factory protocol, and internal TLS needs the corporate CA bundle. On data, subtle ordering/currency differences produced tiny diffs that had to be understood before trusting the source.

- **Q: How is the cronjob scheduled and monitored?**
  - **A**: Kubernetes CronJob on EKS; each run emails a status table (source, latest date, comments) and archives to S3. Failures are visible via the alert + pod logs, and jobs are re-runnable per date.

- **Q: Why Databricks over Snowflake/XpressFeed for this?**
  - **A**: Firm-wide standardisation on Databricks + Unity Catalog/LASR as the governed data platform — one lineage, one access model. My job was to move safely onto it, not to pick it.
