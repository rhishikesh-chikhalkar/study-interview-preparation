# Resume

## Rhishikesh Chikhalkar

**Senior Backend Engineer**

Pune, India · rhishichikhalkar21@gmail.com · +91-9049329866 · [LinkedIn] · [GitHub] · [Portfolio]

---

## Summary

Senior Backend Engineer with 4.5+ years of experience designing, building, and optimizing scalable backend systems and data platforms for enterprise financial applications. Deep expertise in Python, FastAPI, Flask, PostgreSQL, and AWS. Proven track record of building RESTful APIs, microservices, and ETL pipelines deployed on AWS using Docker, Kubernetes, and CI/CD automation. Skilled in cloud-native architecture, caching, authentication and authorization, data engineering, and test-driven development. Proven ability to convert manual, spreadsheet-driven workflows into fast, secure, automated services.

---

## Core Skills

| Category | Technologies |
| :--- | :--- |
| Languages | Python, SQL |
| Backend / APIs | FastAPI, Flask, Flask-RESTX, REST, async/await, Pydantic, OpenAPI/Swagger, microservices |
| Data & ETL | Pandas, NumPy, SQLAlchemy, Snowflake, Databricks, Apache Airflow, S&P Capital IQ, XpressFeed, ETL pipelines, data modeling |
| Databases & Caching | PostgreSQL, MySQL, Redis, query optimization, indexing |
| Cloud & DevOps | AWS (S3, EKS, ECR, Athena, CodeBuild/CodePipeline, Secrets Manager), Docker, Kubernetes, Helm, GitHub Actions, CI/CD |
| Auth & Security | OAuth2/OIDC (OKTA), JWT, JWKS, RBAC, AD-group authorization, Snyk, Wiz |
| Testing | Pytest (unit + integration), Unittest, TDD (RED–GREEN–REFACTOR), FastAPI TestClient |
| Frontend (working) | React, TypeScript, Plotly Dash, AG Grid |
| Tooling | Ruff, Git, Postman, Lens, Aptakube, CloudWatch |

---

## Professional Experience

### Infosys Limited — Digital Specialist Engineer

**Dec 2021 — Present** · Pune, India (client: Capital Group — Financials Research Group)

#### APIs & Microservices

- Designed and built FastAPI microservices for portfolio analytics — including a Portfolio Metrics API (13 endpoints) that serves real-time portfolio summaries with instantly recalculated forecasted returns.
- Architected RESTful integrations with third-party financial data providers (Snowflake/XpressFeed, S&P Capital IQ, CG Equity Holdings API) to automate portfolio metric calculation and reporting.
- Built portfolio summaries and lets managers run what-if scenarios (e.g. exit-P/E changes).
- Built a Flask REST API that automated daily report generation and on-demand regeneration for any target date, serving 20+ stakeholders via scheduled and user-triggered Airflow pipelines.

#### Performance & Optimization

- Implemented Redis caching (shared, connection-pooled, invalidation aligned to the data's daily refresh) for S3-hosted reference data in a Dash app, cutting data-retrieval latency from ~3s to ~0.5s and eliminating redundant S3 fetches on every page load.
- Optimized PostgreSQL queries, indexing, and schemas (index tuning, SQL-side aggregation, column pruning) improving API response times by ~40% on large financial datasets.

#### Data Engineering

- Designed and maintained ETL pipelines (Python, Pandas, SQLAlchemy) automating ingestion, transformation, and reporting of 500K+ records daily across Snowflake, Databricks, and S3.
- Migrated a production data pipeline from XpressFeed to Databricks, implementing native machine-to-machine OAuth (client-credentials with pre-expiry token refresh) and validating output parity source-by-source before cutover, with a retained rollback path.
- Investigated and resolved cross-source data non-determinism in cluster-valuation reports by proving the variance, diagnosing query-plan/partitioning and currency tie-break causes, and enforcing deterministic ordering — making reports reproducible run-to-run.

#### Security

- Implemented OAuth2/OIDC (OKTA) authentication and RBAC across services — JWT validation against IdP JWKS (signature, expiry, audience, issuer) with a reusable `roles_required` dependency, and AD-group authorization for division-scoped data access.
- Enforced no-secrets-in-image practices: keys/creds sourced from AWS Secrets Manager and S3 at runtime and cached once, never baked into builds.

#### Cloud, DevOps & CI/CD

- Containerized services with multi-stage Docker and deployed on AWS EKS via Helm (Deployments for APIs, CronJobs for batch), with config in ConfigMaps and secrets via SecretProviderClass.
- Built and maintained CI/CD pipelines (AWS CodeBuild/CodePipeline, GitHub Actions) across 10+ apps, APIs, and cron jobs, enforcing quality gates (tests, Prisma container scans, Nexus IQ dependency scans) to keep unstable code out of production.

#### Quality, Monitoring & Mentoring

- Wrote comprehensive pytest unit and integration suites (business logic, APIs, PostgreSQL layer) using fixtures, mocks, and FastAPI TestClient.
- Built a custom timing middleware (request-ids + adaptive log levels) and cronjob email alerting; used CloudWatch, Lens, and Aptakube for monitoring and incident investigation, reducing resolution time by ~30%.
- Mentored 3 junior engineers; introduced Ruff for linting/formatting/imports and established security-review workflows (Snyk for app dependencies, Wiz for container security) and FastAPI/PostgreSQL conventions.

---

## Selected Projects

### Portfolio Metrics API — FastAPI, Snowflake, Pandas, AWS EKS, Pytest

Real-time portfolio analytics and scenario-modelling service for portfolio managers.

- 13 endpoints for portfolio summaries, SEDOL-level financial detail, and scenario CRUD; multi-year (1–5yr) forecasts.
- Snowflake key-pair auth with the private key in S3, downloaded and cached once per process; startup connection warmup via FastAPI Lifespan to remove first-request cold-start.
- Custom timing middleware and rigorous NaN/Inf→null JSON sanitization for reliable chart rendering.

### CRGI PM Dashboard — Flask, Python, Jupyter, Airflow, Snowflake, AWS S3

Automated daily portfolio performance & risk reporting for Capital Research Global Investors.

- Productionized notebook analytics into an Airflow DAG generating 3 daily Excel reports with zero manual touchpoints; Flask API for on-demand regeneration of any target date.

### CG Data Pipeline (Databricks migration) — Python, Databricks, LASR, S3

Daily pipelines feeding holdings analysis and T10 files; led the XpressFeed→Databricks migration with M2M OAuth, parity validation, and rollback safety.

### CRGI Equity Yield Lab — FastAPI, XpressFeed, Pandas, S3

SEDOL screening tool: upload a SEDOL list, enrich with market data (yield, market cap, EPS growth, CG-held flag), filter by investment criteria, stream back a multi-sheet Excel report.

### Holding Analyzer — Plotly Dash, Redis, S3

Holdings dashboard; delivered the Redis caching layer that cut load latency ~6x (3s→0.5s).

---

## Education

**Bachelor of Engineering, Computer Science** — Shivaji University · Jun 2016 — Jun 2020

---

## Certifications & Awards

- Google Certified Engineer — Associate Cloud Engineer
- Infosys Certified Applied Generative AI Professional
- Python for Data Engineering & API Development (Internal Training)
- **Platinum Club Member — Infosys Ltd (FY 2025-26)** — top 3% of employees for performance, leadership, and technical excellence.

---

*All metrics (3s→0.5s, ~40%, ~30%, 500K+/day) are observed/approximate from production timing and pipeline volume; happy to explain how each was measured.*
