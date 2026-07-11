# Cluster Call Cronjobs

Situation. While moving cluster-call jobs onto Databricks, the Databricks output didn't perfectly match XpressFeed for some securities. In finance, an unexplained diff is a blocker —

11 — Cluster Call Cronjobs (data-correctness investigation)

| Repo: qrt-qh-frg-cluster-call—cronjobe - stack: Python,

Snapshot

XpressFeed outputs, proving a source of non-determinism, and dia

STAR story — "Two data sources disagreed — | found out why"

© > [ egict

Built three cluster-analysis cronjobs and led a deep data-correctness investigation.

Databricks SQL XpressFeed, Pandas, $3, EKS CronJob Your role:

ings reports (Cll FIG, CRGI FIG, CRGI Consumer). Beyond the pipelines themselves, | did a Serious data-correctness investigation — comparing Databricks vs

gnosing currency tie-breaking and table-partitioning effects. It's my ‘I don’t Just ship, | make sure the numbers are right’ story.”

someone could trade on a wrong number.

Task. Explain every discrepancy between the two sources and make the pipeline deterministic and trustworthy before cutover.

Action.

Result. Every diff was explained and eliminated: the queries became deterministic (stable tetbreal

Built comparison harnesses ( test_compare_dbx_xf, test_compare dbx_xf fig) diffing the two sources over the same universe and dates.
ins — and traced it to missing deterministic ordering.

Proved non-determinism in a query (prove _nondeterminism -Py ) — the same query could return different tie-broken rows across ru
" j

breaking (inspect_currency ties! Py ): when a security had multiple currency rows, the “winner” wasn't deterministic without an explicit tie-break rule.

ex lain query «py, dump_plans-py) to understand why row order/selection varied.

Diagnosed currency tie-!
ded! prod. py. validate _tiebreak. Py) that adds deterministic ordering + tie-break rules, and validated it

Investigated table partitioning and query plans (inspect_table_partitionifg. py.
Built a folded/optimised template ( build_and_validate_optimized.py, Val. jate_
against production ranges (validate _cii range, validate!new_prod.py).

Organised throwaway analysis ina .scratch/ folder, separate from the production cronjob/ code.

king + explicit ordering), so cluster reports are reproducible run-to-run and match the trusted source. Cutover proceeded with
ft <


evidence.

Technical deep-dive & why tc a

Code samples (real, extracted from the repo)

The determinism fix — explicit ROW_NUMBER() tie-break so the “chosen” row is stable every run ( -Seratch/build estimates folded ipy, abridged)
ROW_NUMBER() OVER (

PARTITION BY es.ciq_company_id, es.fiscal_year,
CASE

WHEN es.estimate_id IN (100179, 100173,

WHEN es.estimate_id = 104055 THEN 'PB!

WHEN eS.estimate_id = 104111 THEN 'ROE!

WHEN es.estimate_id = 100208 THEN "DPS'

WHEN es.estimate_id 114220 THEN 'REV'

160284, 100278) THEN ‘PE!


END
ORDER BY
CASE es.estimate_id = — 1. preferred source estimate first
WHEN 100173 THEN 1 WHEN 100179 THEN 2

WHEN 106278 THEN 3 WHEN 100284 THEN 4
ELSE es.estimate_id

END,

CASE WHEN es.currency_iso_code
THEN 0 ELSE 1 END,

es.currency_iso_code,

es.estimate_value DESC
) AS est_rn

= es.exchange currency — 2. prefer the reporting currency

deterministic currency order
final deterministic tie—break

Before this, “pick one estimate Per company/year" relied on the engine's arbitrary row ord. Oa
source of non-determinism | proved and diagnosed.

a7 is Ei Alte “


Likely follow-up Q&A

Q: How do you make a SQL result deterministic? A: ORDER BY a unique/stable key, and for

break>) ) with a fully specified tie-break, so the same input always yields the same chosen row.

Q: How did you prove it was non-deterministic and not just wrong? A: Ran the identical query repeatedly and captured differing out
plans/partitioning — reproducing the variance on demand is the proof.

Q: What did you validate before trusting the new pipeline? A: Parity against XpressFeed over production date ranges, plus tie-break and folded-tem
Data migration (project 10).



rency tie could flip between runs and silently change a valuation. Every ORDER BY’ clause here exists to remove one

puts for the same inputs (prove _nondeterminism. Py). then correlated with query

plate validation scripts, before any cutover — same discipline as the cG ;



“one row per group” use a window function (ROW_NUMBER() OVER (PARTITION BY Gd ORDER BY <explicit tie=
