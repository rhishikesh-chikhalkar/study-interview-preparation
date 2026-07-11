# Cross-cutting Themes

! IS |. So gat tests catry more weight, an de
What triggers a build? Merge to the relevant branch (develop/release) triggers CodeBuild + image build + sean


Postg SQL optimisation

Claim: "Optimised PostgreSQL queries, indexing,

and schemas — ~40% faster API responses.”

_ Evidence / how to defend the 40%:
instead of doing it in Pandas, Measuri

R BY, avoided N+1 queries, selected only needed colu
letrics API logs durations), od ies

Be ready to explain the mechanism: added indexes on cc
ed via before/after response times (the timing middleware

_ Why these techniques?

* Indexing turns a sequential scan into an index seek on Selective predicates — the single biggest
* Push aggregation into SQL so less data crosses the wire and Pandas gets a smaller frame. 4
* Select only needed columns — narrower rows, less I/O, :

Follow-ups:

Databricks in the cluster-call investigation — ‘explain query. d ins spy.) :
© Q: Downside of indexes? They cost write time and stora

ge — index for read patterns, not blindly. 12 : =
* Q: Composite index order? Most-selective / leftmost-used-in-predicate first; match the query's filter+sort shape.

* Q How do you find a slow query? EXPLAIN ANALYZE — look for Sequential scans on big tables bad row estimates, and expensive sorts: add/adjust indexes accordingly. (I did exactly this style o

4. Caching (Redis) — the 3s — 0.5s win

Claim: "Implemented Redis caching for S3-hosted reference data, 3s > 0.5s, eliminating redundant $3 fetches."

Evidence: art—gh-frg-holding"analyzer/redis cache lpy — pooled Redis connection, keys tha
story. 4

reat’ 10am Pacific next day (aligned to the daily data refresh), feature-flag toggle. See

i NU
Why Redis + time-aligned expiry? Redis is shared across EKS pods/workers (in-process cache isn't); expiring aligned to the data's real refresh maximises hit-rate and freshness vs a blind TT

ll == ll
Follow-ups: cache invalidation strategy, cache-stampede handling, Redis-down fallback — all covered in 09-holding-analyzer.md,

5. Authentication & Authorization a aa EEL UE! ti

Claim: "Implemented OAuth2-based auth (OKTA) and RBAC.”

Evidence — you have three real patterns:

1. JWT + JWKS (FastAPI): energy—dashboard
2. OKTA OIDC (Flask): quantamental-—portfolio-api/
3. Platform ingress auth: Dash apps sit behind OKTA at the ingre

Py. , validates signature/exp/ audience/issuer, roles _r, quired dependency for RBAC. See 08.

Flask-OIDC tedirect/callback. AD-group authorization, secrets built into a temp config at runtime. See 04/05,
SS with tole-based access,

Why JWKS over shared secrets? Asymmetric, 1

Follow-ups: 401 vs 403 (authN vs authZ), key rotation,

6. Testing (Pytest, unit + integration)

Claim:

“Comprehensive pytest unit and integration suites covering APIs,

business logic, and the PostgreSQL data layer” ‘ " ;
Evidence: 'tests/unit + testS/integration, conftest. py with fixtures, FastAPI Te

SQLite in-memory for DB tests, mocked external data sources.
mappings) with fixture DataFrame:

ig entity, 500 mapping).

Why this split? Unit tests target pure functions (calculations,

pin the maths. Integration tests hit endpoints via TestC
contracts and error handling (422 on bad input. 404 on missin : =

i 5)
in Cl withi

out credentials and never flakes on a network blip. F

Follow-ups:

Q: TDD? The team follows RED — GREEN — REFACTOR: tests are committed before Mapl
* Q: How do you test numeric correctness? Known-input fixtures with exact expected outpt

1. Observability & production monitoring: | 4%, 1.

Claim: “Used CloudWatch, Lens, Aptakube for monitoring/debugging; reduced resolution time ~30%." Ms ie $

Evidence: Custom timing middleware (Portfolio Metrics API) with request-ids and adaptive log levels; structured logging;
dbx_connectivity_test job.

email alerts on every cronjob run (status table with data source + latest date);

Why adaptive log levels + request-ids? In an analytical API some endpoints are legitimately slow — logging everything at INFO hides the signal. Fast success + DEBUG: slow (>10s)/errors = WARNING+. Request-ids make
concurrent requests correlatable in CloudWatch.

Why email alerts on batch jobs? Cron Jobs fail silently by default; a daily status email is the cheapest observability that gives business users confidence data is fresh.

Follow-ups: Lens/Aptakube are Kubemetes dashboards for pod status/logs/exec on EKS; CloudWatch for centralised logs/metrics/alarms.

8. Data engineering / ETL

Claim: “ETL pipelines with Python, Pandas, SQLAlchemy; 500K+ records daily.”

Evidence: the cronjob repos — Snowflake/Databricks/Capital IQ extraction, Pandas transformation, $3/PostgreSQL loading, business-date alignment, archival with dated + current keys. |

Why the read/compute/serve split? Every one of my apps separates a batch tier (heavy pulls + compute offline into $3) from a serving tier (AP|/dashboard reads pre-computed data). Result: fast, resilient Uls and ratelimit-
safe data access. This is the single most repeated architectural decision across the portfolio.

Follow-ups: idempotency (re-runnable per date), parity validation on source migration (project 10), determinism (project 11). iS

9. Mentoring & code quality

Claim: “Mentored 3 junior engineers; introduced Ruff: established Snyk/Wiz security workflows."

Talking points: introduced Ruff for linting/formatting/import-ordering (one fast tool replacing several); established review practices;

set up Snyk (app dependencies) and Wiz (container security) scanning; wrote the
FastAPI/PostgreSQL best-practice conventions the team follows (layered router—service—db, Pydantic at the boundary,

no secrets in images).

Why Ruff? One Rust-fast tool for lint + format + import sort — consistent style with near-zero Cl time, less bikeshedding in reviews.

The two stories to lead with

1. Design breadth: Portfolio Metrics API (01) — architecture, async, auth, the NaN/JSON bug, offline/online split.
2, Measurable impact: either the Redis 3s0.5s win (09) or the XpressFeed—Databricks migration with parity validation (10).

Have both ready; pick based on whether the interviewer wants design or impact.

