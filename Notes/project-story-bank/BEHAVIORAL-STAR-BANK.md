# Behavioral / STAR Story Bank — non-technical rounds

These are grounded in your real projects so they're defensible. Each story maps to common behavioral prompts. Rehearse 6-8 until you can tell them in ~90 seconds without notes. Reuse the same core stories across multiple question types — you only need a handful of great ones.

**Format reminder**: Situation (context, brief) → Task (your responsibility) → Action (what you specifically did — use "I", not "we") → Result (outcome + a number if you have one) → Reflection (what you learned). Keep S+T short; spend your time on A+R.

---

## 1. Biggest impact / "most proud of" — Redis caching (Holding Analyzer)

- **S**: A Dash dashboard analysts used daily was slow — it fetched reference data from S3 on every page load, ~3 seconds each time, for data that only changes once a day.
- **T**: I owned making it fast without changing what analysts saw.
- **A**: I added a Redis cache with a pooled connection shared across all the app's pods, and — the key decision — I set the cache to expire aligned to the data's actual daily refresh (10am Pacific) instead of a blind TTL. On a hit we skip both the S3 round-trip and the parse; on a miss we fall back to S3. I also put it behind a feature flag so I could bypass it when debugging data.
- **R**: Load times dropped from ~3s to ~0.5s — roughly 6x — and we eliminated redundant S3 reads all day, cutting cost and load.
- **Reflection**: The insight wasn't "add a cache," it was invalidate aligned to when the data actually changes. Caching is easy; invalidation is where people get it wrong.

---

## 2. Complex problem / debugging — Data non-determinism (Cluster Call cronjobs)

- **S**: While migrating cluster valuation jobs onto Databricks, the new output didn't perfectly match the trusted XpressFeed source for some securities. In finance, an unexplained diff is a hard blocker — people trade on these numbers.
- **T**: Explain every discrepancy and make the pipeline trustworthy before cutover.
- **A**: I built comparison harnesses to diff the two sources over the same universe. I proved the query was non-deterministic — the same query returned different tie-broken rows across runs — by running it repeatedly and capturing the variance. I traced it to missing deterministic ordering plus ambiguous currency tie-breaks, confirmed it via query plans and partitioning, then rewrote the queries with explicit ordering and tie-break rules and validated against production date ranges.
- **R**: Every diff was explained and eliminated: the reports became reproducible run-to-run, and we cut over with evidence instead of hope.
- **Reflection**: "It's probably fine" isn't acceptable for numbers people trade on. You can't fix what you can't explain — so I reproduced the problem on demand first.

---

## 3. Ownership / delivering a big change — XpressFeed → Databricks migration (CG Data cronjob)

- **S**: The firm was standardising on Databricks, so a production data pipeline feeding holdings analysis and T10 files had to move off XpressFeed — but its output feeds tools people rely on.
- **T**: Re-platform it safely, with no silent change to the numbers.
- **A**: I implemented Databricks' machine-to-machine OAuth (client-credentials with a 60-second token-refresh buffer so long queries never fail mid-flight), handled the corporate CA/TLS quirks, and — critically — kept both data sources in parallel and diffed outputs to prove parity before cutover. I kept the pre-Databricks version archived as an instant rollback and preserved the daily email/S3 audit trail.
- **R**: The pipeline runs on Databricks with secure token-managed auth, validated to match the old source, with a rollback path retained.
- **Reflection**: For any migration, parity validation + a rollback plan matter more than the new tech itself.

---

## 4. Attention to detail / a subtle bug others missed — NaN/Inf JSON bug (Portfolio Metrics API)

- **S**: The portfolio charts occasionally rendered blank for certain portfolios, with no obvious error.
- **T**: Find why the frontend intermittently showed nothing.
- **A**: I traced it to financial data gaps producing `NaN`/`Inf` in Pandas — and `NaN`/`Infinity` aren't valid JSON, so some clients silently failed to parse the response. I added a sanitisation step that converts every non-finite float to `null` before serialising each record.
- **R**: Charts render reliably; the failure was invisible in logs but obvious once you knew where to look.
- **Reflection**: The nastiest bugs are the silent ones. I now treat the serialisation boundary as a place data quality must be enforced.

---

## 5. Mentoring / raising the team's bar — Ruff + security workflows

- **S**: Code style was inconsistent across the team and reviews got bogged down in formatting nits; security scanning wasn't standardised.
- **T**: Improve consistency and mentor 3 junior engineers without slowing delivery.
- **A**: I introduced Ruff for linting, formatting, and import-ordering — one fast tool replacing several — so style stopped being a review topic. I set up Snyk for dependency vulnerabilities and Wiz for container security, and I wrote up our FastAPI/PostgreSQL conventions (layered router→service→db, Pydantic at the boundary, no secrets in images) and coached the juniors through them in reviews.
- **R**: Reviews got faster and focused on logic instead of formatting; the juniors ramped onto the conventions; security scanning became a standard gate.
- **Reflection**: Good mentoring is making the right thing the easy default — tooling and written conventions scale better than repeating yourself in every review.

---

## 6. Design decision / trade-off — Batch tier vs serving tier (recurring pattern)

- **S**: Analytical endpoints were tempted to do heavy Snowflake/Capital IQ pulls and computation inline, which made UIs sluggish and hammered rate-limited data sources.
- **T**: Decide where the heavy work should live.
- **A**: I consistently split a batch tier (Kubernetes CronJobs that pull and pre-compute daily into S3) from a serving tier (APIs/dashboards that read pre-computed data). I made the cronjob and API share the exact same calculation code so offline and online numbers can't drift.
- **R**: Fast, resilient UIs; if an upstream source is down, the last good snapshot still serves; and one source of truth for the maths.
- **Reflection**: The trade-off is freshness (data is "as of last batch") for speed and resilience — which is exactly right for daily research data.

---

## 7. Making something self-service / removing yourself as a bottleneck — CRGI PM Dashboard

- **S**: Daily portfolio performance and risk reports for 20+ stakeholders were produced manually by running a notebook and distributing Excel files every business day.
- **T**: Automate it and let people regenerate any date without asking someone to re-run a notebook.
- **A**: I productionised the notebook analytics into importable, parameterised code, drove daily generation of 3 report files through an Airflow DAG, and exposed a Flask API so any stakeholder can regenerate a report for any target date on demand — both paths calling the same generation code.
- **R**: Zero manual touchpoints per business day; on-demand regeneration is one API call.
- **Reflection**: Automating the happy path isn't enough — the on-demand escape hatch is what actually removed the manual asks.

---

## 8. Security-minded decision — Secrets & auth done right

- **S**: Services needed Snowflake keys, DB creds, and OKTA secrets across dev and prod.
- **T**: Handle secrets without ever baking them into images or code.
- **A**: I kept the Snowflake private key in S3, pulled at runtime and cached once; built OKTA config into a temp file from env vars at startup; sourced everything sensitive from AWS Secrets Manager via the platform's secret provider; and validated JWTs fully against the IdP's JWKS (signature, expiry, audience, issuer) rather than trusting a shared secret.
- **R**: No secrets in images or source; key rotation on the IdP/S3 side needs no redeploy.
- **Reflection**: Secrets in an image leak. Pull at runtime, cache once, and let the platform own rotation.

---

## Prompt → which story to use

| If they ask... | Use story |
| :--- | :--- |
| "Tell me about your biggest impact / proudest work" | 1 (Redis) or 3 (Databricks) |
| "A hard technical problem you solved" | 2 (non-determinism) |
| "A time you owned a big/risky change" | 3 (migration) |
| "A subtle bug / attention to detail" | 4 (NaN/JSON) |
| "Leadership / mentoring / influencing without authority" | 5 (Ruff + conventions) |
| "A design decision and its trade-offs" | 6 (batch vs serving) |
| "Improving a process / initiative you drove" | 7 (PM Dashboard automation) |
| "Security / handling sensitive data" | 8 (secrets & auth) |
| "A failure / something that went wrong" | Use 2 or 4, framed as "here's what we found and how I caught/fixed it" |
| "Disagreement / conflict" | Adapt 3 or 6: "I pushed for parity validation / the batch split when there was pressure to just cut over" |

---

## Weak-spot prompts — have an honest answer ready

- **"A time you failed."** Pick a real one with a lesson (e.g. an early assumption in a migration that a parity check caught — "I initially trusted the new source too much; the diff taught me to validate before cutover, which is now my default"). Own it, don't blame, end on the lesson.
- **"Something you'd do differently."** Equity Yield Lab's per-row XpressFeed calls — "It works and is readable, but I'd batch the lookups; I optimised for shipping first, and I know exactly how I'd make it faster."
- **"Where do you want to grow?"** Honest + forward-looking: deeper distributed-systems/scaling work, or broadening from Python into the platform's other stacks.

---

## Delivery tips

- Say "I" for your actions, "we" only for genuine team context. Interviewers score your impact.
- Lead with the result if the story is long: "I cut a dashboard's load from 3s to 0.5s — here's how."
- Have one number per story. If you don't have one, say the qualitative outcome confidently.
- It's fine to reuse the same 3-4 projects across many questions — depth beats breadth.
