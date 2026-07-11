# ATS Resume

## RHISHIKESH CHIKHALKAR — Senior Backend Engineer

Pune, India | rhishichikhalkar21@gmail.com | +91-9049329866 | LinkedIn: [add-url] | GitHub: [add-url] | Portfolio: [add-url]

---

## PROFESSIONAL SUMMARY

Senior Backend Engineer with 4.5+ years of experience designing, developing, and optimizing scalable backend systems and data pipelines for enterprise financial applications. Expertise in Python, FastAPI, Flask, and PostgreSQL, with a strong record of building RESTful APIs, microservices, and ETL pipelines deployed on AWS using Docker, Kubernetes, and CI/CD automation. Skilled in cloud-native architecture, caching, authentication and authorization, data engineering, and test-driven development. Proven ability to convert manual, spreadsheet-driven workflows into fast, secure, automated services.

---

## TECHNICAL SKILLS

**Programming Languages:** Python, SQL

**Backend and APIs:** FastAPI, Flask, Flask-RESTX, RESTful API design, asynchronous programming, Pydantic, OpenAPI, Swagger, microservices

**Data and ETL:** Pandas, NumPy, SQLAlchemy, Snowflake, Databricks, Apache Airflow, S&P Capital IQ, XpressFeed, ETL pipelines, data modeling

**Databases and Caching:** PostgreSQL, MySQL, Redis, query optimization, indexing

**Cloud and DevOps:** AWS (S3, EKS, ECR, Athena, CodeBuild, CodePipeline, Secrets Manager), Docker, Kubernetes, Helm, GitHub Actions, CI/CD

**Authentication and Security:** OAuth2, OpenID Connect (OIDC), OKTA, JWT, JWKS, RBAC, Active Directory group authorization, Snyk, Wiz

**Testing:** Pytest, Unittest, unit testing, integration testing, test-driven development (TDD), FastAPI TestClient

**Frontend:** React, TypeScript, Plotly Dash, AG Grid

**Tools and Platforms:** Ruff, Git, Postman, Lens, Aptakube, CloudWatch, Databricks

---

## PROFESSIONAL EXPERIENCE

### Infosys Limited — Digital Specialist Engineer

**December 2021 — Present** | Pune, India | Client: Capital Group (Financials Research Group)

- Designed, developed, and maintained FastAPI-based microservices for financial portfolio analytics, including a Portfolio Metrics API with 13 endpoints serving real-time portfolio summaries and scenario-based forecasted returns.
- Architected and integrated RESTful APIs with third-party financial data providers, including Snowflake, S&P Capital IQ, XpressFeed, and the CG Equity Holdings API, to automate portfolio metric calculation and reporting.
- Developed a Flask REST API to automate daily report generation and on-demand regeneration for any target date, serving 20+ stakeholders through scheduled and user-triggered Apache Airflow pipelines.
- Implemented Redis caching for AWS S3-hosted reference data in a Dash application, reducing data retrieval latency from approximately 3 seconds to 0.5 seconds and eliminating redundant S3 fetch calls on every page load.
- Optimized PostgreSQL queries, indexing strategies, and database schemas, improving API response times by approximately 40 percent for large-scale financial datasets.
- Designed and maintained ETL pipelines using Python, Pandas, and SQLAlchemy to automate data ingestion, transformation, and reporting, processing 500,000+ records daily across Snowflake, Databricks, and S3.
- Led the migration of a production data pipeline from XpressFeed to Databricks, implementing native machine-to-machine OAuth (client-credentials authentication) with automatic token refresh, and validating output parity source-by-source before cutover with a retained rollback path.
- Investigated and resolved cross-source data non-determinism in cluster-valuation reports by proving the variance, diagnosing query-plan, partitioning, and currency tie-break causes, and enforcing deterministic ordering, making reports reproducible across runs.
- Implemented OAuth2 and OpenID Connect (OKTA) authentication and role-based access control (RBAC), including JWT validation against the identity provider JWKS endpoint (signature, expiry, audience, and issuer verification) and Active Directory group-based authorization.
- Enforced secure secrets management, sourcing keys and credentials from AWS Secrets Manager and S3 at runtime and never embedding secrets in Docker images or source code.
- Containerized backend services using multi-stage Docker builds and deployed applications on AWS EKS Kubernetes clusters using Helm, with Deployments for APIs and CronJobs for batch workloads.
- Built and maintained CI/CD pipelines using AWS CodeBuild, AWS CodePipeline, and GitHub Actions across 10+ applications, APIs, and cron jobs, enforcing quality gates including automated tests, Prisma container scanning, and Nexus IQ dependency scanning to prevent unstable code from reaching production.
- Developed comprehensive Pytest-based unit and integration test suites covering APIs, business logic, and the PostgreSQL data layer using fixtures, mocks, and the FastAPI TestClient.
- Built a custom timing middleware with request identifiers and adaptive log levels, and cron job email alerting; used CloudWatch, Lens, and Aptakube for production monitoring and incident investigation, reducing issue resolution time by approximately 30 percent.
- Mentored 3 junior engineers on backend development best practices, introduced Ruff for linting and formatting, and established security scanning workflows using Snyk for application dependencies and Wiz for container security.

---

## SELECTED PROJECTS

### Portfolio Metrics API | FastAPI, Snowflake, Pandas, AWS EKS, Pytest
- Built a real-time portfolio analytics and scenario-modelling service with 13 endpoints for portfolio summaries, SEDOL-level financial detail, and multi-year forecasted returns.

### CRGI PM Dashboard | Flask, Python, Jupyter, Airflow, Snowflake, AWS S3
- Productionized notebook analytics into an Airflow DAG generating 3 daily Excel reports for 20+ stakeholders with zero manual touchpoints; Flask API for on-demand regeneration of any target date.

### CG Data Pipeline (Databricks Migration) | Python, Databricks, LASR, AWS S3
- Migrated daily production data pipelines from XpressFeed to Databricks using machine-to-machine OAuth, with parity validation and rollback safety.

### CRGI Equity Yield Lab | FastAPI, XpressFeed, Pandas, AWS S3
- Built a SEDOL screening tool that enriches uploaded SEDOL lists with market data and streams back a multi-sheet Excel report filtered by investment criteria.

### Holding Analyzer | Plotly Dash, Redis, AWS S3
- Delivered a Redis caching layer that reduced dashboard load latency approximately 6 times, from 3 seconds to 0.5 seconds.

---

## EDUCATION

**Bachelor of Engineering, Computer Science** | Shivaji University | June 2016 — June 2020

---

## CERTIFICATIONS AND AWARDS

- Google Certified Engineer — Associate Cloud Engineer
- Infosys Certified Applied Generative AI Professional
- Python for Data Engineering and API Development (Internal Training)
- **Platinum Club Member — Infosys Ltd (FY 2025-26):** Among the top 3 percent of employees for performance, leadership, and technical excellence.
