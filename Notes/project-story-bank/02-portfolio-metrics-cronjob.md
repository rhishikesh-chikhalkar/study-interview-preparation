# 02 — Portfolio Metrics Cronjob

- **Repo**: `art-gh-frg-portfolio-metrics-cronjob`
- **Stack**: Python, Snowflake, Pandas, AWS S3, EKS CronJob
- **Your Role**: Built the daily batch pipeline that pre-computes data for the Portfolio Metrics API.

## Snapshot
"This is the batch counterpart to the Portfolio Metrics API. It runs daily on a Kubernetes CronJob, pulls the latest positions and fundamentals from Snowflake, computes the heavy portfolio metrics once, and lands the results so the API can serve them fast. It's the ‘do the expensive work offline’ half of the design — and it emails a status report each run."

---

## STAR Story — "Move the expensive work out of the request path"

- **Situation**: Some portfolio computations are heavy (multi-year forecasts across every holding). Doing them inside the API on every request would make the UI feel sluggish and hammer Snowflake.
- **Task**: Pre-compute the daily-stable data offline so the API only does light, interactive work.
- **Action**:
  - Built a Kubernetes CronJob (`portfolio_metrics_daily.py`) that runs after market data lands.
  - Reused the same utility modules as the API (calculation, column mappings, database and Snowflake functions) so the batch numbers and the live numbers are computed by identical code — no drift between offline and online.
  - Pulled from Snowflake, transformed in Pandas, and persisted results for the API/database.
  - Added email notifications (`email_functions.py`) so ops get a daily success/failure report with the latest data date — failures are visible, not silent.
- **Result**: The API stays responsive because the expensive computation is amortised into one nightly run, and the shared-code approach guarantees consistency between the batch and live paths.

---

## Technical Deep-Dive & Why

- **Why a CronJob, not an in-API scheduler?**
  - Separation of concerns and independent scaling/retries. A batch failure doesn't take down the API; Kubernetes handles scheduling, restarts, and history.
- **Why share utility modules with the API?**
  - The single worst bug in analytics is the same metric computed two different ways. Sharing `calculation_functions`/`column_mappings` means one source of truth. Refactor once, both paths benefit.
- **Why email alerts?**
  - Batch jobs fail silently by default. An HTML status email (data source, latest date, comments) is the cheapest possible observability for a nightly job and gives business users confidence the data is fresh.
- **Idempotency / re-runnability**:
  - The job is designed to be safely re-run for a target date so a transient Snowflake blip can be recovered by re-triggering, not by manual data surgery.

---

## Code Samples

### Daily Job — derive the latest date, pull once, load into the DB (`cronjob/portfolio_metrics_daily.py`, abridged)
```python
def run_portfolio_metrics_daily() -> str:
    portfolio_uid_list = [276710]
    # Heavy pull happens ONCE here (offline) so the API never does it on the request path
    quantamental_data_df = insert_quantamental_data()
    quantamental_data_df = quantamental_data_df.dropna(subset=["price_date"])
    price_date = quantamental_data_df["price_date"].max()
    sedol_list = sorted(quantamental_data_df["sedol"].unique())
    
    xpressfeed_summary_df, trading_item_ids, company_id_to_sedol_mapping = get_xpressfeed_data_from_snowflake(
        sedol_list,
        price_date
    )
    
    insert_xpressfeed_data_into_database(
        portfolio_uid_list,
        sedol_list,
        price_date,
        xpressfeed_summary_df
    )
    # Note the imports are the same utility modules the API uses
```

---

## Likely Follow-up Q&A

- **Q: How do you handle a failed nightly run?**
  - **A**: The job emails failure with context: because it's date-parameterised and idempotent, ops can re-run it for the affected date. Kubernetes keeps job history so we can investigate the failed pod logs.
- **Q: How do you avoid the cronjob and API drifting apart?**
  - **A**: They import the same calculation/mapping utilities. There's no second implementation to keep in sync — that's a deliberate design choice.
- **Q: Why not just cache in the API instead of a batch job?**
  - **A**: Caching helps repeat reads, but the first computation is still expensive and Snowflake-heavy. Pre-computing once nightly is cheaper overall and guarantees low-latency reads all day.
