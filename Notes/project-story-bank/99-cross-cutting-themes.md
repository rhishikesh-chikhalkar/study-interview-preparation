# 99 — Cross-Cutting Themes (the rapid-fire tech screen)

These are the resume bullets and skills that span every repo — the questions you'll get in a tech screen regardless of which project comes up. Each theme has: the claim, the real evidence, the why, and the follow-ups.

---

## 1. Docker & AWS EKS deployment

**Claim**: "Containerised backend services with Docker and deployed on AWS EKS."

**Evidence**: Every repo has `helm-chart/`, `codebuild/`, and a multi-stage `Dockerfile`. Services run as EKS Deployments; batch jobs run as Kubernetes CronJobs; config via ConfigMaps; secrets via AWS Secrets Manager (SecretProviderClass).

**Why multi-stage Docker?** A builder stage compiles/installs dependencies; the runtime stage copies only what's needed — smaller, more secure images (no build tools, fewer CVEs). The firm uses Chainguard base images which are distroless — so CMD must be exec form (`["python", "-m", "..."]`), not shell form, because there's no shell at runtime.

**Follow-ups:**
- **Q: Deployment vs CronJob — when each?** Long-running services (APIs) = Deployment; scheduled batch (data pipelines, reports) = CronJob with retries and history.
- **Q: How do secrets reach the pod?** AWS Secrets Manager → SecretProviderClass (CSI) + mounted as env; never in the image or ConfigMap. Non-sensitive config (hosts, ports, flags) → ConfigMap/Helm values.
- **Q: How do you roll back?** Helm rollback / redeploy previous image tag; for data jobs, re-run the prior known-good (and I keep archived prior versions, e.g. the pre-Databricks cronjob).

---

## 2. CI/CD (AWS CodeBuild / CodePipeline, GitHub Actions)

**Claim**: "Built CI/CD pipelines across 10+ apps/APIs/cron jobs, enforcing quality gates."

**Evidence**: `codebuild/buildspec_*.yml` per repo (build-develop, build-release, deploy-develop, deploy-prod); Prisma/Twistlock container scanning; Sonatype IQ/Nexus dependency scanning.

**Why quality gates?** Block unstable/vulnerable code from prod automatically — security scans (Prisma for containers, Nexus IQ for dependencies), tests, and build success are gates, not suggestions.

**Follow-ups:**
- **Q: Dev → Prod with no QA?** Correct — this estate is Dev → Prod. So gates and tests carry more weight, and prod deploys are deliberate.
- **Q: What triggers a build?** Merge to the relevant branch (develop/release) triggers CodeBuild → image build + scan + deploy to the target EKS cluster.

---

## 3. PostgreSQL optimisation

**Claim**: "Optimised PostgreSQL queries, indexing, and schemas — ~40% faster API responses."

**Evidence / how to defend the 40%**: Be ready to explain the mechanism: added indexes on columns used in WHERE/JOIN/ORDER BY, avoided N+1 queries, selected only needed columns, and pushed aggregation into SQL instead of doing it in Pandas. Measured via before/after response times (the timing middleware in the Portfolio Metrics API logs durations).

**Why these techniques?**
- Indexing turns a sequential scan into an index seek on selective predicates — the single biggest win.
- Push aggregation into SQL so less data crosses the wire and Pandas gets a smaller frame.
- Select only needed columns — narrower rows, less I/O.

**Follow-ups:**
- **Q: Downside of indexes?** They cost write time and storage — index for read patterns, not blindly.
- **Q: Composite index order?** Most-selective / leftmost-used-in-predicate first; match the query's filter+sort shape.
- **Q: How do you find a slow query?** EXPLAIN ANALYZE — look for sequential scans on big tables, bad row estimates, and expensive sorts; add/adjust indexes accordingly. (I did exactly this style of analysis on Databricks in the cluster-call investigation — `explain_query.py`.)

---

## 4. Caching (Redis) — the 3s → 0.5s win

**Claim**: "Implemented Redis caching for S3-hosted reference data, 3s → 0.5s, eliminating redundant S3 fetches."

**Evidence**: `art-gh-frg-holding-analyzer/redis_cache.py` — pooled Redis connection, keys that expire at 10am Pacific next day (aligned to the daily data refresh), feature-flag toggle. See project 09 for the full story.

**Why Redis + time-aligned expiry?** Redis is shared across EKS pods/workers (in-process cache isn't); expiring aligned to the data's real refresh maximises hit-rate and freshness vs a blind TTL.

**Follow-ups:** Cache invalidation strategy, cache-stampede handling, Redis-down fallback — all covered in [09-holding-analyzer.md](09-holding-analyzer.md).

---

## 5. Authentication & Authorization

**Claim**: "Implemented OAuth2-based auth (OKTA) and RBAC."

**Evidence — you have three real patterns:**
1. **JWT + JWKS (FastAPI)**: Energy Dashboard API — `VerifyToken` class with `PyJWKClient`, validates signature/exp/audience/issuer, `roles_required` dependency for RBAC. See [08](08-energy-dashboard-api.md).
2. **OKTA OIDC (Flask)**: Quantamental Portfolio API — Flask-OIDC redirect/callback, AD-group authorization, secrets built into a temp config at runtime. See [04](04-quantamental-portfolio-api.md)/[05](05-quantamental-portfolio-data.md).
3. **Platform ingress auth**: Dash apps sit behind OKTA at the ingress with role-based access.

**Why JWKS over shared secrets?** Asymmetric keys, no signing secret to leak, key rotation just works.

**Follow-ups:** 401 vs 403 (authN vs authZ), key rotation, RBAC granularity — all covered in [08-energy-dashboard-api.md](08-energy-dashboard-api.md).

---

## 6. Testing (Pytest, unit + integration)

**Claim**: "Comprehensive pytest unit and integration suites covering APIs, business logic, and the PostgreSQL data layer."

**Evidence**: `tests/unit` + `tests/integration`, `conftest.py` with fixtures, FastAPI TestClient, SQLite in-memory for DB tests, mocked external data sources.

**Why this split?** Unit tests target pure functions (calculations, mappings) with fixture DataFrames — they pin the maths. Integration tests hit endpoints via TestClient and assert contracts and error handling (422 on bad input, 404 on missing entity, 500 mapping). Mocking externals keeps tests fast, deterministic, and CI-runnable without credentials and never flakes on a network blip.

**Follow-ups:**
- **Q: TDD?** The team follows RED → GREEN → REFACTOR: tests are committed before implementation.
- **Q: How do you test numeric correctness?** Known-input fixtures with exact expected output — the tests are the spec for the financial calculations.

---

## 7. Observability & production monitoring

**Claim**: "Used CloudWatch, Lens, Aptakube for monitoring/debugging; reduced resolution time ~30%."

**Evidence**: Custom timing middleware (Portfolio Metrics API) with request-ids and adaptive log levels; structured logging; email alerts on every cronjob run (status table with data source + latest date); `dbx_connectivity_test` job.

**Why adaptive log levels + request-ids?** In an analytical API some endpoints are legitimately slow — logging everything at INFO hides the signal. Fast success → DEBUG; slow (>10s)/errors → WARNING+. Request-ids make concurrent requests correlatable in CloudWatch.

**Why email alerts on batch jobs?** CronJobs fail silently by default; a daily status email is the cheapest observability that gives business users confidence data is fresh.

**Follow-ups:** Lens/Aptakube are Kubernetes dashboards for pod status/logs/exec on EKS; CloudWatch for centralised logs/metrics/alarms.

---

## 8. Data engineering / ETL

**Claim**: "ETL pipelines with Python, Pandas, SQLAlchemy; 500K+ records daily."

**Evidence**: The cronjob repos — Snowflake/Databricks/Capital IQ extraction, Pandas transformation, S3/PostgreSQL loading, business-date alignment, archival with dated + current keys.

**Why the read/compute/serve split?** Every one of my apps separates a batch tier (heavy pulls + compute offline into S3) from a serving tier (API/dashboard reads pre-computed data). Result: fast, resilient UIs and ratelimit-safe data access. This is the single most repeated architectural decision across the portfolio.

**Follow-ups:** Idempotency (re-runnable per date), parity validation on source migration (project 10), determinism (project 11).

---

## 9. Mentoring & code quality

**Claim**: "Mentored 3 junior engineers; introduced Ruff; established Snyk/Wiz security workflows."

**Talking points**: Introduced Ruff for linting/formatting/import-ordering (one fast tool replacing several); established review practices; set up Snyk (app dependencies) and Wiz (container security) scanning; wrote the FastAPI/PostgreSQL best-practice conventions the team follows (layered router→service→db, Pydantic at the boundary, no secrets in images).

**Why Ruff?** One Rust-fast tool for lint + format + import sort — consistent style with near-zero CI time, less bikeshedding in reviews.

---

## The two stories to lead with

1. **Design breadth**: Portfolio Metrics API ([01](01-portfolio-metrics-api.md)) — architecture, async, auth, the NaN/JSON bug, offline/online split.
2. **Measurable impact**: Either the Redis 3s→0.5s win ([09](09-holding-analyzer.md)) or the XpressFeed→Databricks migration with parity validation ([10](10-cg-data-cronjob.md)).

Have both ready; pick based on whether the interviewer wants design or impact.
