# CRGI PM Dashboard

17 — CRGI PM Dashboard (automated daily reporting)

| Repo/dir: (CWI-PM—-DASHBOARD - Stack: Flask, Python, Jupyter, Airflow, Snowflake, AWS S3, Pandas, XisxWriter Your role: Built the end-to-end automated daily reporting system (this is the resume "CRGI PM Dashboard”
project).

Snapshot

“An automated daily reporting system for Capital Research Global Investors. It pulls from Snowflake, generates Excel feports with portfolio performance and risk analytics for 20+ stakeholders every business day, and exposes a
Flask REST API to regenerate any report on demand for a target date. Three daily report files are produced hands-off via an Airflow DAG — zero manual touchpoints.”

Numbers to quote: 20+ stakeholders, 3 automated daily files, any-date on-demand regeneration, zero manual touchpoints per business day.

STAR story — "Turn a manual daily report into a zero-touch pipeline" &

Situation. CRGI's daily portfolio performance and risk reports were produced manually — someone ran a notebook generated Excel files, and distributed them to 20+ stakeholders every business day. Slow, error-prone, and a
single point of human failure.

Task. Fully automate daily generation and distribution, and allow on-demand regeneration for any past date without manual work.

Action.

; Ince and risk analytics in Pandas, and generate formatted Excel reports (XlsxWriter) landed in $3.
SHBOARD. PROD captures the analytics that were codified).

* Built the end-to-end reporting pipeline in Python: pull portfolio data from Snowflake, compute
* Productionised the analytical Jupyter work into a repeatable pipeline (the notebook WORK_CRGT_PM_f
* Exposed a Flask REST API so any stakeholder can regenerate a report for a target date, eliminating "can you re-run yesterday's?” manual asks.

* Automated 3 daily report files via an Airflow DAG, achieving zero manual touchpoints each business day, with $3 as the distribution/storage layer.

Result. Daily reporting for 20+ stakeholders runs itself; on-demand regeneration for any date is a single API call; manual effort per business day dropped to zero.

* Why Airflow for scheduling? The reports have dependencies and ordering (data must land before compute before file generation before distribution) and need retries + visibility. Airflow models this as a DAG with per-
task retries and a run history — far more robust than a cron script. : : =
* Why also a Flask API for on-demand regeneration? Scheduling handles the daily happy path, but people need to re-run for a past date (data correction, late request). A Paracel API makes that eheeuis: i)

MT al
i om

instead of a manual notebook run — the API and DAG share the same underlying generation code.
* Why productionise the notebook? Jupyter is great for building the analytics but terrible as a production runtime (hidden state, manual execution). Codifying the logic into modules that both ie DAG and API call

removes the human from the loop and makes it testable/reproducible. Se =
* Why Excel + S3 output? Stakeholders consume Excel; $3 gives durable, versioned, access- (arated storage and a natural distribution point. Date-keyed files give point-in-time reproducibility.
* Why Snowflake as source? It's the governed analytical store for the portfolio data; pulling from it (vs scraping upstream systems) gives one consistent, auditable source.

Likely follow-up Q&A

Q: What made this “zero manual touchpoints”? A: The Airflow DAG runs on schedule, pulls Snowflake, computes, generate the 3 Excel files, and lands them in S3 for distribution — no human runs anything. Previously & each
of those steps was manual.

Q: How does on-demand regeneration for an arbitrary date work? A: The Flask endpoint fakes a target date and calls the same generation code the DAG uses, parameterised by date — so a re-run for any historical date is
identical to the scheduled run, just with a different date input. ' e :

Q: How did you go from a notebook to production safely? A: Extract the analytics from the notebook into importable, parameterised functions; drive them from the DAG and API; validate the generated reports against the —

previous manual output before cutover — so stakeholders saw identical numbers, just produced automatically. al

no partial/duplicate reports.

