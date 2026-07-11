# Interview Preparation — Project Story Bank

Owner: Rhishikesh Chikhalkar (Senior Backend Engineer — Python, FastAPI, Flask, PostgreSQL, AWS). Target level: Senior.

How to use: Each file below is one project. Every file follows the same structure so you can rehearse consistently:

1. Snapshot — one-line pitch, stack, your role, scale.
2. STAR story — Situation, Task, Action, Result (behavioural rounds).
3. Technical deep-dive — architecture, key decisions, why this approach and not the alternatives.
4. Likely follow-up Q&A — the questions an interviewer will actually ask, with strong answers.
5. 30-second and 2-minute pitch — for "walk me through a project you're proud of".

Everything here is grounded in the real code in this workspace. When you quote a number (latency, record counts, users), keep it consistent with what you say elsewhere.

## Project Index

| File | Project | Stack | Headline Story |
| :--- | :--- | :--- | :--- |
| [01-portfolio-metrics-api.md](01-portfolio-metrics-api.md) | Portfolio Metrics API | FastAPI, Pandas, EKS | Real-time portfolio scenario modelling: async + startup warmup; Snowflake key-pair auth |
| [02-portfolio-metrics-cronjob.md](02-portfolio-metrics-cronjob.md) | Portfolio Metrics Cronjob | Python, Snowflake, S3 | Daily pre-computation pipeline feeding the API |
| [03-portfolio-metrics-ui.md](03-portfolio-metrics-ui.md) | Portfolio Metrics UI | React, TypeScript, AG Grid, Module Federation | Editable financial grid micro-frontend |
| [04-quantamental-portfolio-api.md](04-quantamental-portfolio-api.md) | Quantamental Portfolio API | Flask, OKTA, S3 | Excel dashboard generation + authentication bridge |
| [05-quantamental-portfolio-data.md](05-quantamental-portfolio-data.md) | Quantamental Portfolio Data API | Flask, OKTA, S3 | RBAC bridge between Excel and S3 |
| [06-crgi-equity-yield-lab.md](06-crgi-equity-yield-lab.md) | CRGI Equity Yield Lab | FastAPI, XpressFeed, Pandas | SEDOL screening for yield scenarios |
| [07-company-forecast-api.md](07-company-forecast-api.md) | Company Forecast API | FastAPI, Snowflake | exit-PE-driven forecast scenarios |
| [08-energy-dashboard-api.md](08-energy-dashboard-api.md) | Energy Dashboard API | FastAPI, JWT/JWKS, RBAC | Token-verification middleware |
| [09-holding-analyzer.md](09-holding-analyzer.md) | Holding Analyzer | Dash, Redis, S3 | Gaining story, Redis caching |
| [10-cg-data-cronjob.md](10-cg-data-cronjob.md) | CG Data Cronjob | Python, Databricks, S3 | Xpressfeed -> Databricks migration (M2M OAuth) |
| [11-cluster-call-cronjobs.md](11-cluster-call-cronjobs.md) | Cluster Call Cronjobs | Python, Databricks, XpressFeed | Data correctness / non-determinism investigation |
| [12-trading-multiples-cronjobs.md](12-trading-multiples-cronjobs.md) | Trading Multiples Cronjobs | Python, Capital IQ, S3 | Capital IQ data extraction & multiples pipeline |
| [13-crgi-rp-summaries-dashboard.md](13-crgi-rp-summaries-dashboard.md) | CRGI RP Summaries Dashboard | Dash, OKTA, S3 | Multi-fund analytics dashboard |
| [14-company-trading-app.md](14-company-trading-app.md) | Company Trading Multiples App | Dash, Plotly, S3 | Interactive multiples + Excel/Word export |
| [15-airline-price-tracker-app.md](15-airline-price-tracker-app.md) | Airline Price Tracker | Dash, Plotly, S3 | Client-side PDF export dashboard |
| [16-brz-app.md](16-brz-app.md) | BRZ App | Dash, Plotly | Category/product analytics dashboard |
| [17-crgi-pm-dashboard.md](17-crgi-pm-dashboard.md) | CRGI PM Dashboard | Flask, Jupyter, Airflow, Snowflake, S3 | Automated daily reporting pipeline |
| [18-oversight-governance-api.md](18-oversight-governance-api.md) | Oversight Governance API | Java Spring Boot, PostgreSQL | Platform governance service |
| [99-cross-cutting-themes.md](99-cross-cutting-themes.md) | Cross-cutting Themes | Docker, EKS, CI/CD, Testing, Security | Achievements that span every repo |

## Quick Links

- [CHEAT-SHEET.md](CHEAT-SHEET.md) — one-page skim for right before you walk in.
- [BEHAVIORAL-STAR-BANK.md](BEHAVIORAL-STAR-BANK.md) — 8 behavioral stories + prompt—story mapping.
- [99-cross-cutting-themes.md](99-cross-cutting-themes.md) — rapid-fire tech-screen answers.

## How to run your prep

- **Behavioural round** — read [BEHAVIORAL-STAR-BANK.md](BEHAVIORAL-STAR-BANK.md), rehearse 6-8 stories.
- **System design / technical deep-dive** — read the "Technical deep-dive" + "Why this approach" sections.
- **Rapid-fire tech screen** — read [99-cross-cutting-themes.md](99-cross-cutting-themes.md) (Docker, testing, caching, auth, CI/CD).
- **Right before you walk in** — skim [CHEAT-SHEET.md](CHEAT-SHEET.md).
- **Before every interview** — skim this index and pick your two flagship stories:
  - **Flagship A (breadth + design)**: Portfolio Metrics API ([01](01-portfolio-metrics-api.md)).
  - **Flagship B (impact + measurable win)**: Holding Analyzer Redis caching ([09](09-holding-analyzer.md)) or CG data migration ([10](10-cg-data-cronjob.md)).

## A note on honesty

These stories are written from your real code. Interviewers probe hard — only claim what you can defend. Where a number is an estimate (e.g. “40% faster”), be ready to explain how you measured it (timing middleware logs, before/after latency, CloudWatch). If you didn't measure it, say “approximately, based on observed response times” rather than inventing precision.
