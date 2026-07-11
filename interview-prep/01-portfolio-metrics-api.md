# 01 — Portfolio Metrics API

- **Repo**: `art-gh-frg-portfolio-metrics-api`
- **Stack**: FastAPI 0.122, Python 3.11, Pandas, Snowflake, AWS EKS, Pytest
- **Your Role**: Backend owner — designed and built the service end-to-end.

## Snapshot (30-second pitch)
"I built the Portfolio Metrics API — a FastAPI service that powers real-time portfolio analysis for Capital Group portfolio managers. It serves portfolio summaries with forecasted market values, lets managers create what-if scenarios by changing assumptions like exit P/E, and returns SEDOL-level financial detail. It pulls fundamentals from Snowflake and the firm's Equity Holdings API, does the heavy numerical work in Pandas, and runs on EKS behind an OKTA-secured gateway. The interesting engineering was making a data-heavy analytical workload feel interactive."

- **Key numbers to quote consistently**: 13 endpoints; 5+ institutional portfolios; multi-year (1-5yr) projections; sub-second responses for cached/warm paths, single-digit seconds for full scenario recomputation.

---

## STAR Story — "Make heavy financial modelling feel real-time"

- **Situation**: Portfolio managers were doing scenario analysis in giant Excel models. Every "what if we assume a different exit P/E for these 40 holdings" meant re-keying data and waiting. It was slow, error-prone, and impossible to share.
- **Task**: Build a backend that serves portfolio summaries and lets managers modify assumptions and instantly see recalculated forecasted returns — without the Excel bottleneck — for 5+ institutional portfolios.
- **Action**:
  - Designed a FastAPI service with 13 endpoints split into three groups: metadata (`/get_max_available_date`, `/get_available_stock_list`, `/get_portfolio_scenario_metadata`), analysis (`/get_portfolio_summary`, `/get_calculated_portfolio_summary`, `/get_portfolio_summary_of_summaries`, `/get_sedol_details`), and mutations (`/create_portfolio_copy`, `/create_scenario_copy`, `/update_assumptions_metadata`, `/delete_scenario`, `/delete_portfolio`).
  - Sourced fundamentals from Snowflake (S&P XpressFeed data) using key-pair authentication; the private key is stored in S3 and downloaded + cached once via `lru_cache`, never baked into the image.
  - Added a startup warmup using FastAPI's Lifespan context manager to pre-warm the Snowflake connection in a background thread, so the first user request doesn't pay the cold-connection cost.
  - Wrote a custom timing middleware that stamps every request with a request-id and logs duration with adaptive log levels (fast 2xx at `DEBUG`, anything over 10s or 5xx at `WARNING`+), so slow endpoints surface themselves in logs.
  - Did all numerical work in Pandas, with careful NaN/Inf sanitisation before serializing to JSON (Pandas re-introduces NaN from None, which is invalid JSON — a real bug I fixed).
  - Containerised with a multi-stage Docker build and deployed to EKS via Helm, configuring from ConfigMaps and secrets from AWS Secrets Manager.
  - Backed it with a pytest suite (unit + integration) using FastAPI's TestClient.
- **Result**: Managers now run scenarios interactively through a React UI instead of Excel. Response times dropped from "rebuild the spreadsheet" (minutes) to single-digit seconds, and sub-second on warm metadata paths. Scenario state is persisted, so analysis is shareable and reproducible.

---

## Technical Deep-Dive

### Architecture
```
React UI —-HTTP-—> FastAPI (EKS pod) —-> Snowflake (XpressFeed fundamentals)
                                     ——> CG Equity Holdings API (positions)
                                     ——> AWS S3 (Snowflake private key, reference data)
                                     ——> Pandas compute layer (forecasts, weighting, valuations)
```

### Endpoint Groups (13 endpoints)
- **Metadata (GET)**:
  - `/get_max_available_date`
  - `/get_available_stock_list`
  - `/get_portfolio_scenario_metadata`
- **Analysis (POST)**:
  - `/get_portfolio_summary`
  - `/get_calculated_portfolio_summary`
  - `/get_portfolio_summary_of_summaries`
  - `/get_sedol_details`
  - `/get_all_available_scenarios`
- **Mutations**:
  - `/create_portfolio_copy` (POST)
  - `/create_scenario_copy` (POST)
  - `/update_assumptions_metadata` (POST)
  - `/delete_scenario` (DELETE)
  - `/delete_portfolio` (DELETE)

### Key Design Decisions & Why

1. **Why FastAPI (not Flask/Django)?**
   - Native async/await — several endpoints do I/O to Snowflake + the Holdings API; async lets a worker serve other requests while waiting on the DB.
   - Pydantic request models give free validation and typed request bodies (`PortfolioRequest`, `ChangedAssumptionRequest`, etc.) — bad payloads are rejected at the boundary with a 422, not deep in the compute code.
   - Auto-generated OpenAPI/Swagger — the frontend team consumed the contract directly.
   - *Alternative considered*: Flask (used elsewhere). Rejected here because this service is I/O-bound and benefits from async + typed models; Flask would need extra libraries for the same.

2. **Why key-pair auth for Snowflake + S3-hosted key + `lru_cache`?**
   - Why not bake the key into the image? Secrets in images leak. S3 + IAM keeps the key out of the build and lets Ops rotate it without a redeploy — no rotating password in env vars.
   - Why `lru_cache`? We retrieve and parse the key once per container startup, avoiding a network roundtrip to S3 on every request.

3. **Why a startup warmup via lifespan?**
   - The first Snowflake connection is expensive (auth handshake, warehouse spin-up). Doing it lazily means the first user eats a multi-second cold start.
   - I pre-warm it at app startup in a background thread (`asyncio.to_thread`) so the event loop isn't blocked and the pod is "warm" before it starts taking traffic.

4. **Why a custom timing middleware with adaptive log levels?**
   - In an analytical API, some endpoints are legitimately slow. Logging everything at INFO drowns the signal. My middleware logs fast success at `DEBUG` and only escalates slow (>10s) or error responses to `WARNING`/`ERROR` — so the logs are the performance dashboard.
   - It also injects a `request-id` into a context var so every log line for one request is correlatable — essential when debugging in CloudWatch across concurrent requests.

5. **The NaN/Inf serialisation bug (great "attention to detail" story)**:
   - Financial data has gaps — Pandas produces `NaN`/`inf`. `df.to_dict()` keeps them, and `NaN`/`Infinity` are not valid JSON — some clients silently break.
   - I sanitise every record after `to_dict()`, converting non-finite floats to `None`. Subtle, but it's the difference between a chart rendering and a blank screen.

6. **Business rule in code — CASH always last, everything else alphabetical**:
   - Small thing that shows domain empathy: I split cash vs non-cash rows, sort non-cash alphabetically, then concat cash at the end — because that's how PMs read a holdings table.

---

## Code Samples

### 1. Startup Warmup — Lifespan Context (`app/main.py`)
```python
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application startup: pre-warming Snowflake connection...")
    # Run the blocking Snowflake connection warmup off the event loop
    await asyncio.to_thread(warmup_snowflake_connection)
    yield
    logging.info("Application shutting down.")

app = FastAPI(title="Portfolio Metrics API", version="1.0.0", lifespan=lifespan)
```

### 2. Snowflake Key-pair Auth (`app/utilities/snowflake_functions.py`)
```python
import os
import tempfile
from importlib import import_module
from functools import lru_cache
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

@lru_cache(maxsize=1) # download + parse happen once, not per request
def _get_snowflake_private_key_bytes() -> bytes:
    s3_client = import_module("quanthub.util").s3_appdata_client_qh
    sf_key_dir = tempfile.mkdtemp()
    sf_key = os.path.join(sf_key_dir, "sf_dev_key.p8")
    try:
        s3_client.download_object(key=SNOWFLAKE_PRIVATE_KEY_S3_KEY, local_path=sf_key)
        with open(sf_key, "rb") as key_file:
            p_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )
        return p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    finally:
        if os.path.exists(sf_key):
            os.remove(sf_key)
        if os.path.exists(sf_key_dir):
            os.rmdir(sf_key_dir) # never leave the private key on disk
```

### 3. NaN/Inf Bug Sanitization (`app/routers/application_router.py`)
```python
import math

summary_records = summary_df.to_dict(orient="records")
summary_records = [
    {
        k: (None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v)
        for k, v in row.items()
    }
    for row in summary_records
]
```

### 4. Custom Timing Middleware (`app/middleware/timing_middleware.py`)
```python
import logging
import time

async def dispatch(self, request, call_next):
    request_id = set_request_id() # correlate every log line for one request
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    
    if elapsed > 10: # slow -> surface it
        log_level = logging.WARNING
    elif response.status_code >= 500:
        log_level = logging.ERROR
    else:
        log_level = logging.DEBUG # fast 2xx stays quiet -> logs ARE the perf dashboard
        
    request_logger.log(
        log_level,
        "%s %s — %.0fms",
        request.method,
        request.url.path,
        elapsed * 1000
    )
    return response
```

---

## Likely Follow-up Q&A

- **Q: How do you keep a Pandas-heavy endpoint from blocking the event loop?**
  - **A**: CPU-bound Pandas work does block the loop. For the truly heavy paths, I keep request bodies small, push as much filtering as possible into the SQL/Snowflake query so Pandas gets a smaller frame, and offload blocking I/O and connection work to threads (`asyncio.to_thread`). If load grew, the next step would be a process pool or moving heavy pre-computation into the nightly cronjob.
- **Q: How is the API secured?**
  - **A**: It sits behind the platform's OKTA-authenticated ingress proxy on EKS; `/health` is the only open path. Secrets (Snowflake key location, DB credentials) are mounted from AWS Secrets Manager via SecretProviderClass, never hardcoded. CORS is configured at the app level.
- **Q: How did you test a service that depends on Snowflake?**
  - **A**: Unit tests target the pure functions (calculations, column mappings, weighting) using fixture DataFrames without hitting the network. Integration tests use FastAPI's `TestClient` and mock the database layer to assert on status codes, response shape, and error handling.
- **Q: What happens when a scenario doesn't exist?**
  - **A**: The custom-flags lookup raises `ValueError`, which I translate to a `404 Not Found` with a clear details message — I never leak a raw 500 or stack trace. Boundary errors are handled explicitly.
- **Q: How would you scale this to 10x the portfolios?**
  - **A**: (1) Move full-portfolio recomputation to the nightly cronjob and serve pre-computed frames; (2) add a Redis cache for `get_portfolio_summary` keyed by `(portfolio, date, scenario)` — the same pattern I used on the Holding Analyzer; (3) horizontally scale pods on EKS; (4) push more aggregation into Snowflake.
- **Q: Why store scenario state server-side instead of in the UI?**
  - **A**: Scenarios must be shareable and reproducible — a PM creates a scenario, a colleague opens it later. Server-side persistence makes that possible and keeps the UI thin.

---

## 2-minute pitch (for "tell me about a project")
"Portfolio managers at Capital Group were stuck doing scenario analysis in massive Excel models — slow, error-prone, un-shareable. I built the Portfolio Metrics API to replace that. It’s a FastAPI service on EKS with 13 endpoints; it serves portfolio summaries with forecasted market values, lets managers change assumptions like exit P/E and instantly see recalculated returns, and drills down to SEDOL-level financials. Data comes from Snowflake — I used key-pair auth with the private key in S3, cached once per process, so no secrets are baked into the Docker image. I pre-warm the Snowflake connection at startup so the first user doesn't pay the cold-start penalty, and I wrote a timing middleware with adaptive log levels so slow endpoints surface themselves in our monitoring. The trickiest bug was NaN/Inf values silently breaking JSON serialization for charts — I sanitised every record before serialising. The service is covered by a pytest unit and integration suite, and deployed via Helm. The outcome: PMs now do interactive, shareable scenario analysis in seconds instead of rebuilding spreadsheets."
