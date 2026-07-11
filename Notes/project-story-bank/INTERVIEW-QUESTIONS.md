# Interview Questions Bank — with model answers

---

## 1. Python & Language

- **Q: `list` vs `tuple` vs `set` — when each?**
  - **A**: Lists for ordered mutable sequences; tuples for immutable records or dictionary keys; sets for O(1) membership tests and deduplication — e.g. "is this SEDOL held?" checks.

- **Q: How does Python handle concurrency? What's the GIL?**
  - **A**: The GIL lets only one thread execute Python bytecode at a time, so threads don't help for CPU-bound work. For I/O-bound work (network calls, DB queries) I use asyncio/threads; for CPU-bound Pandas work I keep frames small or push compute to the batch tier / a process pool.

- **Q: Generators vs lists — why care?**
  - **A**: Generators are lazy and memory-efficient — they yield one item at a time. For large data extracts I stream rather than materialize everything, avoiding memory blowups.

- **Q: What are `@lru_cache` pitfalls?**
  - **A**: It caches on argument identity and holds references (memory), isn't thread-safe for the compute step by default, and is per-process (not shared across pods). For my Snowflake key, per-process is fine and it's perfect; for cross-pod caching I use Redis instead.

---

## 2. FastAPI / API Design

- **Q: Why FastAPI over Flask/Django?**
  - **A**: Native async/await for I/O-bound work, Pydantic validation at the boundary, auto OpenAPI/Swagger for the frontend. Flask where the estate/OKTA-OIDC standard required it.

- **Q: How does Pydantic help you?**
  - **A**: Typed request/response models validate and coerce input at the edge and document the contract. Each operation gets its own model (`PortfolioRequest`, `ChangedAssumptionRequest`), so invalid data never reaches business logic.

- **Q: Sync vs async endpoint — how do you decide?**
  - **A**: Async when the handler awaits I/O (DB, HTTP, S3) so the worker serves others while waiting. For blocking libraries I offload with `asyncio.to_thread`. Doing CPU-heavy Pandas work in an async handler blocks the loop — I avoid that.

- **Q: How do you structure a FastAPI app?**
  - **A**: Layered: thin routers (parse, call, shape response, map errors) → services/utilities (business logic, no framework dependency) → db layer. Business logic is unit-testable without HTTP.

- **Q: A request to Snowflake takes 8 seconds. How do you keep the API responsive?**
  - **A**: Push filtering/aggregation into SQL so Pandas gets a small frame; pre-compute the daily-stable parts in a nightly cronjob and have the API read those; cache hot results in Redis; warm the connection at startup; scale pods horizontally since the service is stateless.

- **Q: How do you handle errors so you don't leak internals?**
  - **A**: Map domain errors to precise HTTP codes — e.g. a missing portfolio raises `ValueError` which I translate to 404, not a 500 stack trace. Auth failures are 401 (authN) vs 403 (authZ). A global handler standardizes the rest.

---

## 3. Caching (your flagship — expect depth)

- **Q: Why did you add Redis and not just an in-memory dict?**
  - **A**: The Dash app runs multiple workers/pods on EKS. An in-process dict isn't shared, so each worker would still hit S3. Redis gives one warm copy shared across all.

- **Q: Walk me through the 3s→0.5s win.**
  - **A**: The app fetched S3 reference data on every page load (~3s). I added a Redis cache with a pooled connection, keyed by data type, with expiry aligned to the next-day 10am Pacific refresh. On hit → skip S3 + parse → ~0.5s. On miss → fall back to S3 and populate cache. Result: ~0.5s, ~6x faster, and no redundant S3 reads.

- **Q: Cache invalidation — the hard part. What's your strategy?**
  - **A**: Time-based aligned to the data's actual daily refresh (`expireat` 10am Pacific next day). This maximises hit-rate and freshness, unlike a blind 1-hour TTL that either serves stale data or refetches needlessly. Plus explicit `delete` for manual busting.

- **Q: Cache stampede — many users hit a cold key at once?**
  - **A**: With daily data I pre-warm the cache right after the upstream refresh lands (a scheduled load). Otherwise, a short lock / single-flight around the S3 fetch prevents every worker refetching simultaneously.

---

## 4. PostgreSQL

- **Q: How did you get ~40% faster?**
  - **A**: Added indexes on columns used in WHERE/JOIN/ORDER BY, avoided N+1 queries, pushed aggregation into SQL instead of Pandas, and selected only needed columns. Measured via before/after response times (timing middleware).

- **Q: Downside of indexes?**
  - **A**: They slow writes and cost storage. Index for actual read patterns, not blindly. Composite index column order should match the query's most-selective/leftmost predicate.

- **Q: How do you prevent SQL injection?**
  - **A**: Parameterized queries / ORM bindings — never string-format user input into SQL. Validate at the boundary with Pydantic too.

- **Q: How do you make a SQL result deterministic? (your cluster-call story)**
  - **A**: `ORDER BY` a unique key; for "one row per group" use `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY <explicit tie-break>)`. Without it, partitioning/parallelism can return a different row each run — which silently changes a valuation.

---

## 5. Data Engineering / ETL

- **Q: Describe an ETL pipeline you built.**
  - **A**: Extract from Snowflake/Databricks/Capital IQ → transform in Pandas (clean, derive fields, align to business month-ends) → load to S3/PostgreSQL with dated archive + a stable "current" key, email status alerts, and idempotent per-date re-runs.

- **Q: How do you make a pipeline idempotent?**
  - **A**: Parameterize by date and make writes replace-per-date, so re-running a date produces the same result — no duplicates, safe recovery from a transient failure.

- **Q: You migrated XpressFeed→Databricks. How did you de-risk it?**
  - **A**: Ran both sources in parallel and diffed outputs to prove parity over production date ranges before cutover; kept the old pipeline archived for instant rollback; preserved the daily email/S3 audit trail.

- **Q: Batch vs stream — how did you choose?**
  - **A**: The data refreshes daily and consumers need "as-of-last-batch" correctness, so batch (Kubernetes CronJobs) is right — simpler, cheaper, reproducible. Streaming would be over-engineering for daily research data.

- **Q: How would you scale a pipeline processing 500K→50M records/day?**
  - **A**: Push transforms into the warehouse (Databricks/SQL) instead of Pandas in memory, process in partitions, parallelize independent steps, write columnar (parquet) to S3, and separate extract/transform/load so each scales independently.

---

## 6. Authentication & Security

- **Q: Explain OAuth2/OIDC as you implemented it.**
  - **A**: Users authenticate with OKTA; the app receives a JWT. For Flask apps, Flask-OIDC handles the redirect/callback and I check AD-group claims for authorization. For FastAPI, I validate the bearer JWT against the IdP's JWKS.

- **Q: How do you validate a JWT properly?**
  - **A**: Fetch the signing key by `kid` from the IdP's JWKS endpoint (`PyJWKClient`), then verify signature, expiry, audience, and issuer. Checking audience+issuer stops a token minted for another app being reused here.

- **Q: 401 vs 403?**
  - **A**: 401 = not authenticated (no/invalid/expired token). 403 = authenticated but not authorized (valid token, missing required role/group).

- **Q: Why JWKS instead of a shared secret?**
  - **A**: The IdP signs with rotating asymmetric keys and publishes public keys; I hold no signing secret and key rotation "just works" without redeploying.

- **Q: How do you manage secrets?**
  - **A**: Never in code or images. Sourced from AWS Secrets Manager (SecretProviderClass) and S3 at runtime, cached once. The Snowflake private key lives in S3, pulled and deleted from temp after loading.

- **Q: OWASP concerns in your APIs?**
  - **A**: Injection (parameterized queries + Pydantic), broken auth (JWKS validation, RBAC), sensitive data exposure (no secrets in images, TLS, no PII in logs), and dependency/container CVEs (Snyk + Wiz in CI).

---

## 7. Testing & Quality

- **Q: How do you test a service that depends on Snowflake/S3?**
  - **A**: Unit tests target pure functions with fixture DataFrames (no network). Integration tests use FastAPI TestClient with mocked data layers, asserting status codes and error handling (422/404/500). Mocking externals keeps tests deterministic and CI-runnable without credentials.

- **Q: What's your TDD cycle?**
  - **A**: RED (write a failing test) → GREEN (minimal code to pass) → REFACTOR (clean up, keep tests green). Tests are committed before implementation.

- **Q: How do you test numeric correctness?**
  - **A**: Known-input fixtures with exact expected output — the tests are the spec for the financial calculations.

---

## 8. Cloud, Docker & Kubernetes

- **Q: Why multi-stage Docker?**
  - **A**: Builder stage installs dependencies; runtime stage copies only what's needed — smaller, more secure image. Distroless base means exec-form CMD (no shell).

- **Q: Deployment vs CronJob in Kubernetes?**
  - **A**: Long-running services = Deployment (always running, scaled horizontally). Scheduled batch = CronJob with retries and job history.

---

## 9. System Design & Architecture

- **Q: How do you keep two systems (batch + API) consistent?**
  - **A**: Share the exact calculation/mapping code as an imported module — one source of truth. No second implementation to drift.

- **Q: How would you add real-time collaboration on scenarios?**
  - **A**: Persist scenarios server-side (already done), add optimistic concurrency (version per scenario), and push updates via WebSockets — last-write-wins with version checks or a merge prompt.

- **Q: Recurring architecture decision?**
  - **A**: Split batch tier from serving tier — heavy pull/compute runs offline into S3; APIs/dashboards read pre-computed data — fast, resilient, rate-limit-safe.

---

## 10. Behavioral (see [BEHAVIORAL-STAR-BANK.md](BEHAVIORAL-STAR-BANK.md) for full stories)

| Prompt | Story |
| :--- | :--- |
| Tell me about your biggest impact | Redis 3s→0.5s |
| A hard problem you solved | Data non-determinism investigation |
| A risky change you owned | Databricks migration with parity validation |
| A subtle bug | NaN/Inf breaking JSON charts |
| Mentoring/influence | Ruff + conventions + security workflows |
| A failure / would-do-differently | Per-row XpressFeed calls in Equity Yield Lab; would batch |

---

## 11. Questions to ask the interviewer

- How is work split between feature delivery and platform/reliability work?
- What does your deployment pipeline and on-call look like? How do you catch regressions before prod?
- How do you handle data-correctness/validation for numbers the business depends on?
- What's the biggest technical challenge the team is facing this quarter?
- How do you support growth from senior toward staff/architect level here?
