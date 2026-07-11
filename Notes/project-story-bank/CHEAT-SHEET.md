# Interview Cheat Sheet — skim this right before you walk in

## You

**Backend Engineer, ~4.5 yrs** · Python, FastAPI, Flask, PostgreSQL, AWS (EKS/S3), Snowflake/Databricks

**One-line intro**: "I build production backend services and data pipelines for a financial research group at Capital Group — FastAPI/Flask APIs and Python ETL on AWS EKS that turn manual Excel workflows into fast, secure, automated tools."

---

## Your 2 flagship stories (lead with these)

### ⭐ A — Design breadth: Portfolio Metrics API

- **What**: FastAPI service, 13 endpoints, real-time portfolio scenario modelling for PMs.
- **STAR one-liner**: PMs did scenario analysis in giant Excel models → I built a FastAPI service that serves summaries and recalculates forecasted returns when they change assumptions like exit P/E — scenario analysis went from rebuilding spreadsheets to single-digit seconds, shareable + reproducible.
- **3 technical hooks**: (1) Snowflake key-pair auth, private key in S3, cached once via `lru_cache` — no secrets in image; (2) startup warmup via lifespan so first user doesn't eat cold-start; (3) NaN/Inf → None sanitisation because NaN is invalid JSON and silently broke charts.

### ⭐ B — Measurable impact (pick one):

- **Redis caching (Holding Analyzer)**: Dash app hit S3 every page load (~3s) → added a shared Redis cache with expiry aligned to the daily data refresh (10am Pacific) → ~3s to ~0.5s, killed redundant S3 reads. Hook: shared cache (pods), connection pool, invalidation aligned to data.
- **Databricks migration (CG Data Cronjob)**: Migrated a prod pipeline XpressFeed → Databricks — implemented M2M OAuth (client-credentials, 60s token-refresh buffer), ran both sources in parallel to prove parity, kept old version for rollback. Hook: prove parity before cutover.

---

## 60-second answers to the questions you WILL get

| Question | Your answer in one breath |
| :--- | :--- |
| **Why FastAPI over Flask?** | Async for I/O-bound Snowflake/API calls, Pydantic validation at the boundary, auto OpenAPI for the frontend. Flask where the estate/OKTA-OIDC standard needed it. |
| **How do you cache + invalidate?** | Redis (shared across pods), connection pool, `expireat` aligned to the daily refresh — max hit-rate and freshness vs a blind TTL. Fallback to S3 on miss/Redis-down. |
| **How is auth done?** | JWT validated against IdP JWKS (signature + exp + audience + issuer), `roles_required` dependency for RBAC. OKTA OIDC for Flask apps with AD-group authz. No signing secret in the service. |
| **401 vs 403?** | 401 = no/invalid/expired token (authN). 403 = valid token, missing role claim (authZ). |
| **PostgreSQL ~40% faster — how?** | Indexes on WHERE/JOIN/ORDER columns, pushed aggregation into SQL, selected only needed columns; found slow queries with EXPLAIN ANALYZE. Measured via before/after response times. |
| **How do you test?** | Unit = pure calc functions w/ fixture DataFrames (no network). Integration = FastAPI TestClient + mocked data layer, asserting 422/404/500 mapping. Mock Snowflake/S3 for determinism. |
| **Docker/EKS?** | Multi-stage builds (small distroless runtime — exec-form CMD). Deployments for APIs, CronJobs for batch, secrets via AWS Secrets Manager, config via ConfigMaps/Helm. |
| **Recurring architecture decision?** | Split batch tier from serving tier — heavy pull/compute runs offline into S3; APIs/dashboards read pre-computed data — fast, resilient, rate-limit-safe. |

---

## Signature one-liners (drop these to sound senior)

- "The worst bug in analytics is the same metric computed two different ways — so the cronjob and the API import the same calculation code. One source of truth."
- "I don't refresh the cache on an arbitrary clock; I invalidate it aligned to when the data actually changes."
- "On a data-source migration the cardinal rule is prove parity — I ran both sources side by side and diffed before cutover, and kept the old version for rollback."
- "A service is not a person — a cronjob gets its own identity via M2M OAuth with short-lived auto-refreshed tokens, not a long-lived PAT."
- "SQL without an explicit order isn't deterministic — I made tie-breaks explicit so reports are reproducible run-to-run." (cluster-call investigation)
- "Secrets never live in the image — private keys in S3/Secrets Manager, pulled at runtime, cached once."

---

## Numbers — say them consistently, defend them honestly

| Metric | Say it as | If pushed |
| :--- | :--- | :--- |
| 3s → 0.5s | Redis cache on Holding Analyzer | "observed load timing before/after, ~6x" |
| ~40% faster queries | PostgreSQL indexing + SQL-side aggregation | "measured via before/after response times" |
| 500K+ records/day | ETL pipelines | "it's the daily pipeline volume" |
| 20+ stakeholders, 3 daily files, 0 manual touchpoints | CRGI PM Dashboard | "Airflow DAG + Flask on-demand regen" |
| ~30% faster incident resolution | Timing middleware + CloudWatch | "estimate from reduced investigation time" |

---

## Watch-outs (don't get caught)

- Oversight Governance API is Java/Spring Boot, not Python — only mention as polyglot exposure, don't claim you built it. (See [18](18-oversight-governance-api.md).)
- Equity Yield Lab does one XpressFeed call per row — if asked to optimise: batch the lookups, cache repeats, parallelise (I/O-bound), or make it a background job for big uploads.
- Dash apps — pitch as "Python-native analytics dashboards," and your value is the clean modular architecture + data pipeline behind them, not front-end wizardry.
- Your resume is backend-first — if a frontend question goes deep, pivot: "I owned the UI that consumes my API for full-stack ownership, but my depth is backend and data."

---

## 30-second close (when they ask "anything you're proud of?")

"I take manual, error-prone Excel-and-spreadsheet workflows in a financial research group and turn them into fast, secure, automated services — FastAPI/Flask APIs and Python pipelines on EKS. The pattern: separating the heavy offline computation from a thin, fast serving layer, backed by a proper testing suite. My flagship win was cutting the Holding Analyzer dashboard's load from 3 seconds to half a second with Redis caching invalidated in sync with the data's daily refresh."

---

Full detail per project: [00-INDEX.md](00-INDEX.md) · Rapid-fire tech screen: [99-cross-cutting-themes.md](99-cross-cutting-themes.md)
