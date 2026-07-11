# Interview Questions Bank

Interview Questions Bank — with model answers

1. Python & Language | 7 2 : ee

Q: list vs tuple vs set — when each? Lists for ordered mutable sequences;
this SEDOL held?" checks.

Q: How does Python handle concurrency? What's the GIL? The GIL lets only one thread execute Python bytecode at a time, 3
asyncio/threads; for CPU-bound Pandas work I keep frames small or push compute to the batch tier /a process pool. a

© Q Generators vs lists — why care? Generators are lazy and memory-efficient — they yield one item at a time. For large data extracts | stream rather than materialize everything, avoiding memory blowups.

style dependencies for auth.

Q: What are @lru_cache pitfalls? It caches on argument identity and holds references (memory), isn't thread-safe for the compute step by default, and is per-
it's perfect; for cross-pod caching | use Redis instead. = : d

2. FastAPI / API Design 7

Q: Why FastAPI over Flask/Django? Native async/await for 1/O-bound work, Pydantic validation at the bounda

Flask where the estate/OKTA-OIDC standard required it. Ae 8 aS =<

© Q: How does Pydantic help you? Typed request/response models validate and coerce input at the edge and document the contract. Each operation gets its own model (PortfolioRequest. Sa z
ChangedAssumptionRequest), so invalid data never reaches business logic. | = ie

© Q: Sync vs async endpoint — how do you decide? Async when the handler awaits 1/0 (DB, HTTP, $3) so the worker serves others while waiting. For blocking libraries | offload with lasyn

in an async handler blocks the loop — | avoid that. = i

Q: How do you structure a FastAPI app? Layered: thin routers (parse, call, shape response, map errors) > services/utilities (business logic, no framework dependency) — db layer. Business logic is unit-testable
HTTP. ee

Q: A request to Snowflake takes 8 seconds. How do you keep the API responsive? Push filtering/aggregation into SQL so Pandas gets a small frame; pre-compute the daily-stable parts in a nightly cronjob have
API read those; cache hot results in Redis; warm the connection at startup; scale pods horizontally since the service is stateless. ; jee =i

Q: How do you handle errors so you don't leak internals? Map domain errors to precise HTTP codes — €.g. a missing portfolio raises ValUeError which | translate to 404, not a 500 stack trace. Auth failures are
(authN) vs 403 (authZ). A global handler standardizes the rest. 4




(authN) vs 403 (authZ). A global handler standardizes the rest.

3. Caching (your flagship — expect depth) : 4 a

Q: Why did you add Redis and not just an in-memory dict? The Dash app runs multiple

Q: Walk me through the 3s—0.5s win. The app fetched $3 reference data on every
Result: ~0.5s, ~6x faster, and no redundant S3 reads. ss 3 =

Q: Cache invalidation — the hard Part. What's your strategy? Time-based alig
freshness, unlike a blind 1-hour TTL that either serves stale data or refetches need

Q: Cache stampede — many users hit a cold key at once? With daily datz
every worker refetching simultaneously. =

SQL instead of Pandas, and selecting only needed columns. Measured via

nsive sorts then add/adjust indexes to match the

E: = i) =; 7
Q: Downside of indexes? They slow writes and cost storage. Index for actual read patterns, not blindly. Composite index

mn order should match the query's most-selective/leftmost

Q: How do you prevent SQL injection? Parameterized queries / ORM bindings — never string-format user input into Si Validate at the boundary with Pydantic too.

Q: How do you make a SQL result deterministic? (your cluster-call story) ORDER BY a unique key; for “one row per group” use /ROW_|
Without it, partitioning/parallelism can retum a different row each run — which silently changes a valuation.

5. Data Engineering / ETL

© Q: Describe an ETL Pipeline you built. Extract from Snowflake/Databricks/Capital 1Q = transform in Pandas (clean, derive fields, align to business month-ends) — load to S3/PostgreSQL with dated archive + a stable

“current” key, email status alerts, and idempotent per-date re-runs,
© Q: How do you make a Pipeline idempotent? Parameterize by date and make writes replace-per-date, so re-running a date produces the same result — no duplicates, safe recovery from a transient failure.

Q: You migrated XpressFeed—Databricks. How did you de-risk it? Ran both sources in Parallel and diffed outputs to prove parity over production date ranges before cutover; kept the old pipeline archived for instant
rollback; preserved the daily email/S3 audit trail.

Q: Batch vs stream — how did you choose? The data refreshes daily and consumers need “as-of-last-batch” correctness, so batch (Kubernetes CronJobs) is right — simpler, cheaper, reproducible. Streaming would be over-

engineering for daily research data.

Q: How would you scale a pipeline Processing 500K—50M records/day? Push transforms into the warehouse (Databricks/SQL) instead of Pandas in memory, process in partitions, parallelize independent steps, write

columnar (parquet) to $3, and separate extract/transform/load so each scales independently.

6. Authentication & Security a. \. & bs
= = =o = 2 _ ee a —
© Q: Explain OAuth2/O1DC as you implemented it. Users authenticate with OKTA: the app Wecciveny JWT. For Flask apps, Flask-OIDC handles the redirect/callback and | check AD-group claims for authorization. For FastAPI. |
validate the bearer JWT against the IdP’s JWKS. 2 ‘ % %,

Q: How do you validate a JWT Properly? Fetch the signing key by kid from the IdP’s JWks endpoint (PyJWKClient), then verify signature, expiry, audience, and issuer. Checking audience+issuer stops a token minted

for another app being reused here. | ;
Q: 401 vs 403? 401 = not authenticated (nofinvalid/expired token). 403 = authenticated but not authorized (valid token, missing required role/group).

Q: Why JWKS instead of a shared secret? The IdP signs with rotating asymmetric keys and publishes public keys; | hold no signing secret and key rotation “just works" without redeploying.

Q: How do you manage secrets? Never in code or images. Sourced from AWS Secrets Manager (SecretProviderClass) and $3 at runtime, cached once. The Snowflake private key lives in $3, pulled and deleted from temp

after loading.

Q: OWASP concerns in your APIs? Injection (parameterized queries + Pydantic), broken auth (WKS validation, RBAC), sensitive data exposure (no secrets in images, TLS, no Pil in logs), and dependency/container CVEs

(Snyk + Wiz in Cl).

Tal

7. Testing & Quality =e

Q: How do you test a service that depends on Snowflake/S3? Unit tests target pure functions with fixture DataFrames (no network). Integration tests use FastAPI TeStClient with mocked data layers, asserting status

codes and error handling (422/404/500). Mocking externals keeps tests deterministic and Cl-runnable without credentials.

Q: What's your TDD cvcle? RED (wate 2 failing fect) = CREEN fmininciims endo te ence 5. DErA-TAD To


Q: How do you test a service that depends on Snowflake/S3? Unit tests | Rigel pure functions with fieture DataFram
codes and error handling (422/404/500). Mocking externals Roope) tests eclomumetic and Clrunnable without credentials.

es (no network). Integration tests use F.

8. Cloud, Docker & Kubernetes ]

exec form.

© Q: Deployment vs CronJob in Kubernetes? Long-running services = e|
pipelines as CronJobs.

batch compute from the request path, and share calculation code so offline/online numbers can't drift.

Q: How would you add real-time collaboration on scenarios? Persist scenarios server-side (already done), add optimistic concurrency iveisien per scenario), and push updates via WebSockets
last-write-wins with version checks or a merge prompt.

Q: How do you keep two systems (batch : API) consistent? Share the exact calculation/mapping code as an imported module — one source of truth. No second Implementation to drift.

10. Behavioral (see BEHAVIORAL- STAR- BANK.md for full stories) _




10. pee e (see BEHAVIORAL-STAR-BANK.n md Mts full store)

* Tellme about your biggest impact. = Redis 350.55, = 2 = ! jt
* Ahard problem you solved. > Data non- determinism investigation. l = i) =
* Arisky change you owned. — Databnicks migration with panty validation. . | i ay S i= = ki
* Asubtle bug. — NaN/Inf breaking JSON charts. 3 S 2) LE = |Z | : e
* Mentoring/influence. — Ruff + conventions + securityworkflows. === i ti(itsts~—~S e = = =
* A failure / would-do-differently. — > pet TOW Xpressteed calls in ay Yield Lab; would batch. IG ‘ Ie = Y : =

* How is work split between feature delivery and platform/reliability ‘work? : ss z =
* What does your deployment pipeline and on-call look like? How do you catch regressions before prod? A ae ==
* How do you handle data-correctness/validation for numbers the business depends on?
* What's the biggest technical challenge the team is facing this quarter?
How do you support growth from senior toward staff/architect level here?
