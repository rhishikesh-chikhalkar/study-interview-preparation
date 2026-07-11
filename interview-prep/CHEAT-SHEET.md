# Interview Cheat Sheet

Interview Cheat Sheet — skim this right before you walk in

You: Backend Engineer, ~4.5 yrs - Python, FastAPI, Flask, PostgreSQL AWS (EKS/S3), Snowflake/Databricks One-line intro: “/ build production backend services and data pipelines for a financial research group at Capital Group —
FastAPI/Flask APIs and Python ETL on AWS EKS that turn manual Excel workflows into fast, secure, automated tools.”

Your 2 flagship stories (lead with these)

ve A— Design breadth: Portfolio Metrics API

* What: FastAPI service, 13 endpoints, real-time portfolio scenario modelling for PMs.

* STAR one-liner: PMs did scenario analysts in giant Excel models = | built a FastAPIl service that ‘serves summaries and recalcutates forecasted returns when they change assumptions like exit P/E — scenario analysis went from
rebuilding spreadsheets to single-digit seconds, shareable + reproducible. =

* 3 technical hooks: (1) Snowflake key-pair auth, private key in S3, cached once via iru_cache — no secrets in image: (2) startup warmup via lifespan so first user doesn’t eat cold-start (G) NaN/Inf — None
sanitisation because NaN is invalid JSON and silently broke charts.

vw B— Measurable impact (pick one):

* Redis caching (Holding Analyzer): Dash app hit S3 every page load (~3s) — added a shai ed Redis cache with expiry aligned to the daily data refresh (10am Pacific) + ~3s to ~0.5s, killed redundant $3 reads. Hook: shared

cache (pods), connection pool, invalidation aligned to data. = Hi
* Databricks migration (CG Data Cronjob): Migrated a prod pipeline XpressFeed — Databricks — implemented M2M OAuth (client-credentials, 60s token-refresh buffer), ran both sources in parallel to prove parity, kept old

version for rollback. Hook: prove parity before cutover. : i =

60-second answers to the questions you WILL get

Question Your answer in one breath
Why FastAPI over Flask? Async for |/O-bound Snowflake/API calls, Pydantic validation at the boundary, auto OpenAP! for the frontend. Flask where the estate/OKTA-OIDC standard needed it. = =
How do you cache:+ Redis (shared across pods), connection pool, expireat aligned to the daily refresh — max hit-rate and freshness vs a blind TTL. Fallback to $3 on miss/Redis-down. a =

invalidate? Sie come ee
JWT validated against IdP JWKS (signature + exp + audience + issuer), ‘roles required dependency for RBAC. OKTA OIDC for Flask apps with AD-group authz. No signing secret in

A 2 z =
How is auth done? Sha sche : E

401 vs 4037 401 = no/invalid/expired token (authN). 403 = valid token, missing role claim (authZ).
near 0% ster Indexes on WHERE/JOIN/ORDER columns, pushed aggregation into SQL, selected only needed columns: found slow queries with EXPLAIN ANALYZE. Measured via before/after ee
how? : i =

Unit = pure calc functions w/ fixture DataFrames (no network). Integration = FastAPI| TestClient + mocked data layer, asserting 422/404/500 mapping. Mock Snowflake/S3 for

How do you test?

determinism. : gel i


“60-second a answers to the questions y you WILL get

Why FastAPIl over Liesnah! ‘i payne for l/O-bound !Snowfa/AP calls, Pydanti validation a at the Boundary a auto 0 Open oe the frontend, Flak ‘where ‘the cara oc standar
How do you cache + 5 re “
invalidate? weds (shared ecruss ods connection Pool,

401 vs eee!

Pestgresol 4 40% fate. —

how?

How do you test? Unit = pure calc functions wif fixtue DataFrames {no network). Integration = = ey i

determinism. = i :

Docker/EKS? Multistage builds (Snail distroless runtime — exec-form Mo) Desloyments for APIs, Crontobs fae batch, secrets via AWS Secrets Manager, config via Config Mapeitiela
Recurring architecture a i i : ji ie
decision? Split batch tier from serving tier — heavy plfcomputer run offline into $3; APls/dashboards read bee co npured data — fast, resilient, rate-limit-safe.

= aN

Signature one- -liners (drop these to sound senior)

“The worst bug in analytics is the same metric computed two different ways — so the cronjob and the API import the same calculation code. One source of truth.”
“| don't refresh the cache on an arbitrary clock; | invalidate it aligned to when the data actually changes.” i
“On a data-source migration the cardinal rule is prove parity — | ran both sources side by side and diffed before cutover, and kept the old version for rollback.” =
* “A service is not a person — a cronjob gets its own identity via M2M OAuth with short-lived auto-refreshed tokens, not a tong-lived PAT.”
* “SQL without an explicit order isn't deterministic — | made tie-breaks explicit so reports are reproducible run-to-run.” (cluster-call investigation)
* "Secrets never live in the image — private keys in $3/Secrets Manager, pulled at runtime, cached once."

Numbers - — say them consistently, defend them honestly :

Metric Say it as If pushed 2 i 5 i
3s > 0.55 Redis cache on Holding Analyzes “observed load timing before/after, ~6x" ‘
~40% faster queries at a PostgreSQL indexing + SQL-side aggregation tiger. explain the + mechanism, "measured a response times ‘
SO0K+ hecards/day ETL pipelines it's the e dally pip pipeline yolume i:

20+ stakeholders, 3 daily files, O manual touchpoints © CRGI PM Dashboard Airtow DAG + Flask on- Bemeah tegep


on Holding Analyzer

~40% faster queries mi * PostareSaL indexing + SQL-side aggregation f

~ S00K# Tecords/day eS = ETL pipelines =

20+ stakeholders, 3 daily We O manual touchpoints cRGI PM Dashboard

~30% faster incident resolution.

Watch-outs (don't get caught)

* Oversight Governance API is Java/Spring Boot, not Python — only mention as palate exposure, don’t claim you built it. (Gee 18.)
* Equity Yield Lab does one XpressFeed call per row — if asked to optimise: batch the lookups, cache -Tepeats, parallelise (I/O-1 bound), or make it a dees oru job for big uploads.
* Dash apps — pitch as “Python-native analytics dashboards,” and your value is the clean modular architecture + data pipeline behind them, not front-end wizardry.

* Your resume is backend-first — if a frontend question goes deep, pivot: “| owned the UI that consumes my API for full-stack « abe but my. aoGa. is paced and data"

30-second close (when they ask “anything you're proud of?")

“I take manual, error-prone Excel-and- -spreadsheet workflows in a financial research group and turn them into fast, secure, automated services — FastAPI/Flask APIs and Python pipelines on EKS. The pattern:
separating the heavy offline computation from a thin, fast serving layer, backed by a proper testing suite. My flagship win was the Holding Analyzer dashboard's load from 3 seconds to half a second
invalidated in sync with the data's daily refresh."

Full detail per Project: 00-INDEX.md - Rapid-fire tech screen: 99-cross-cutting-themes.md
