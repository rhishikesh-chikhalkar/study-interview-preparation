# 11 — Cluster Call Cronjobs (data-correctness investigation)

- **Repo**: `qrt-qh-frg-cluster-call-cronjobs`
- **Stack**: Python, Databricks SQL, XpressFeed, Pandas, S3, EKS CronJob
- **Your Role**: Built three cluster-analysis cronjobs and led a deep data-correctness investigation.

## Snapshot (30-second pitch)
"Built three cluster-analysis cronjobs for holdings reports (CII FIG, CRGI FIG, CRGI Consumer). Beyond the pipelines themselves, I did a serious data-correctness investigation — comparing Databricks vs XpressFeed outputs, proving a source of non-determinism, and diagnosing currency tie-breaking and table-partitioning effects. It's my 'I don't just ship, I make sure the numbers are right' story."

---

## STAR Story — "Two data sources disagreed — I found out why"

- **Situation**: While moving cluster-call jobs onto Databricks, the Databricks output didn't perfectly match XpressFeed for some securities. In finance, an unexplained diff is a blocker — someone could trade on a wrong number.
- **Task**: Explain every discrepancy between the two sources and make the pipeline deterministic and trustworthy before cutover.
- **Action**:
  - Built comparison harnesses (`test_compare_dbx_xf`, `test_compare_dbx_xf_fig`) diffing the two sources over the same universe and dates.
  - Proved non-determinism in a query (`prove_nondeterminism.py`) — the same query could return different tie-broken rows across runs.
  - Diagnosed currency tie-breaking (`inspect_currency_ties.py`): when a security had multiple currency rows, the "winner" wasn't deterministic without an explicit tie-break rule.
  - Investigated table partitioning and query plans (`inspect_table_partitioning.py`, `explain_query.py`, `dump_plans.py`) to understand why row order/selection varied.
  - Built a folded/optimised template (`build_and_validate_optimized.py`, `validate_prod.py`, `validate_tiebreak.py`) that adds deterministic ordering + tie-break rules, and validated it against production ranges (`validate_cii_range`, `validate_new_prod.py`).
  - Organised throwaway analysis in a `.scratch/` folder, separate from the production `cronjob/` code.
- **Result**: Every diff was explained and eliminated: the queries became deterministic (stable tie-breaking + explicit ordering), so cluster reports are reproducible run-to-run and match the trusted source. Cutover proceeded with evidence.

---

## Technical Deep-Dive & Why

1. **Why was the query non-deterministic?**
   - SQL without an explicit `ORDER BY` returns rows in an engine-arbitrary order. When you pick "one row per group" (e.g. one estimate per company/year), partitioning and parallelism can return a different row each run — and a currency tie could flip between runs and silently change a valuation.

2. **Why ROW_NUMBER() with a fully specified tie-break?**
   - Every `ORDER BY` clause exists to remove one source of non-determinism: preferred estimate source → reporting currency → deterministic currency order → estimate value descending. The same input always yields the same chosen row.

3. **Why a `.scratch/` folder?**
   - Investigation scripts are throwaway — they shouldn't pollute the production codebase. Keeping them separate makes the repo clean while preserving the investigative trail.

---

## Code Samples

### The determinism fix — explicit ROW_NUMBER() tie-break so the "chosen" row is stable every run (`.scratch/build_estimates_folded.py`, abridged)
```sql
ROW_NUMBER() OVER (
    PARTITION BY es.ciq_company_id, es.fiscal_year,
        CASE
            WHEN es.estimate_id IN (100179, 100173, 160284, 100278) THEN 'PE'
            WHEN es.estimate_id = 104055 THEN 'PB'
            WHEN es.estimate_id = 104111 THEN 'ROE'
            WHEN es.estimate_id = 100208 THEN 'DPS'
            WHEN es.estimate_id = 114220 THEN 'REV'
        END
    ORDER BY
        CASE es.estimate_id                -- 1. preferred source estimate first
            WHEN 100173 THEN 1 WHEN 100179 THEN 2
            WHEN 100278 THEN 3 WHEN 100284 THEN 4
            ELSE es.estimate_id
        END,
        CASE WHEN es.currency_iso_code      -- 2. prefer the reporting currency
            = es.exchange_currency THEN 0 ELSE 1
        END,
        es.currency_iso_code,               -- 3. deterministic currency order
        es.estimate_value DESC              -- 4. final deterministic tie-break
) AS est_rn
```

**Talking point**: Before this, "pick one estimate per company/year" relied on the engine's arbitrary row order — the source of non-determinism I proved and diagnosed.

---

## Likely Follow-up Q&A

- **Q: How do you make a SQL result deterministic?**
  - **A**: `ORDER BY` a unique/stable key, and for "one row per group" use a window function (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY <explicit tie-break>)`) with a fully specified tie-break, so the same input always yields the same chosen row.

- **Q: How did you prove it was non-deterministic and not just wrong?**
  - **A**: Ran the identical query repeatedly and captured differing outputs for the same inputs (`prove_nondeterminism.py`), then correlated with query plans/partitioning — reproducing the variance on demand is the proof.

- **Q: What did you validate before trusting the new pipeline?**
  - **A**: Parity against XpressFeed over production date ranges, plus tie-break and folded-template validation scripts, before any cutover — same discipline as the CG Data migration (project 10).
