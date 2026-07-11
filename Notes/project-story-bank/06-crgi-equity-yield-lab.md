# 06 — CRGI Equity Yield Lab API

- **Repo**: `art-gh-frg-crgi-equity-yield-lab`
- **Stack**: FastAPI, XpressFeed (S&P Capital IQ), Pandas, AWS S3, EKS
- **Your Role**: Built the SEDOL screening and enrichment API end-to-end.

## Snapshot (30-second pitch)
"A FastAPI service that turns a manual equity-screening workflow into one upload. Analysts upload a CSV of SEDOLs, the API enriches each with market data from XpressFeed — dividend yield, market cap, EPS growth — cross-references CG-held positions from S3, applies investment-criteria filters, and streams back a multi-sheet Excel workbook with Included, All, and Unrecognized SEDOLs. One upload replaces hours of manual lookups."

---

## STAR Story — "Turn a manual equity-screening workflow into one upload"

- **Situation**: Analysts screened equities for yield ideas by hand — looking up each SEDOL's yield, market cap, EPS growth, and whether CG already held it, then filtering in Excel. Slow and inconsistent.
- **Task**: Automate the whole enrichment-and-filter pipeline into a single upload-to-download API.
- **Action**:
  - Built a `POST /uploadSEDOLs` endpoint that accepts a CSV, reads it into Pandas, and enriches via XpressFeed calls:
    - `get_pricedivyld(SEDOL)` — price & dividend yield
    - `get_companyestimates(ticker, exchange)` — CompanyId & currency
    - `get_epsgrowth(CompanyId)` — FY1/FY2/FY3 EPS growth
    - Cross-reference CG-held positions pulled from S3.
  - Applied a central `filter_logic` that tags each row with `include` + the criteria it met (dividend yield, market cap, EPS-growth thresholds).
  - Separated results into three Excel sheets (Included / All / Unrecognized SEDOLs) so analysts see both the picks and the SEDOLs the system couldn't resolve.
  - Streamed the workbook back via `StreamingResponse` with a timestamped filename; added `/health` for Kubernetes probes.
- **Result**: A screening pass that took an analyst significant manual effort became a single CSV upload returning a ready-to-use, auditable Excel workbook.

---

## Technical Deep-Dive & Why

1. **Why return three sheets including "Unrecognized SEDOLs"?**
   - Data quality transparency. Hiding unmatched SEDOLs would make the analyst trust a report that silently dropped rows. Surfacing them builds trust and lets them fix inputs.

2. **Why stream the file (`StreamingResponse` from `BytesIO`)?**
   - No temp files on disk, no cleanup, and it works cleanly in a stateless EKS pod. The workbook is built in memory and streamed straight to the client with the correct spreadsheet media type and a `Content-Disposition` attachment header.

3. **Why centralise `filter_logic`?**
   - The include/exclude criteria are the business rules — keeping them in one function (returning both the decision and why) makes the logic testable and auditable, and the `criteria` column explains every inclusion.

4. **Why enrich in discrete steps with `apply(..., result_type="expand")`?**
   - Each external call returns multiple fields; expanding them into typed columns keeps the DataFrame tidy and each enrichment independently debuggable.

---

## Code Samples

### One upload → enrich → filter → multi-sheet Excel, streamed back (`app/main.py`, abridged)
```python
@app.post("/uploadSEDOLs")
async def upload(file: UploadFile = File(...)):
    df = pd.read_csv(BytesIO(await file.read()))
    df = df.merge(get_pricedivyld(df["SEDOL"]), how="left", on="SEDOL")
    unrecognized = df[df["tickerSymbol"].isna()]  # SEDOLs don't silently drop
    df = df.dropna(subset=["tickerSymbol"])

    # each enrichment returns several fields -> expand into typed columns
    df[["CompanyId", "Currency"]] = df.apply(
        lambda r: get_companyestimates(r.tickerSymbol, r.exchangeSymbol),
        axis=1, result_type="expand")
    df[["EpsGrowthFY1", "EpsGrowthFY2", "EpsGrowthFY3"]] = df.apply(
        lambda r: get_epsgrowth(r.CompanyId), axis=1, result_type="expand")
    df["CGheld"] = df["SEDOL"].isin(get_positions()["SEDOL"])

    # central business rule: returns the decision AND why it was included
    df[["include", "criteria"]] = df.apply(
        lambda r: filter_logic(r), axis=1, result_type="expand")

    output = BytesIO()
    with pd.ExcelWriter(output) as writer:
        df[df.include].to_excel(writer, "Included Items", index=False)
        df.to_excel(writer, "All Items", index=False)
        unrecognized.to_excel(writer, "Unrecognized SEDOLs", index=False)

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=CRGI_Equity_Yield_Lab.xlsx"}
    )
    # stream from memory, no temp file
```

---

## Honest Caveats

- The current enrichment uses row-wise `apply` calling XpressFeed per row — repeated lookups. This is a great "how would you make it faster" interview question. Answer: batch the lookups, cache repeats, parallelise (I/O-bound), or pre-compute in a nightly job for large uploads.

---

## Likely Follow-up Q&A

- **Q: How do you handle SEDOLs XpressFeed can't resolve?**
  - **A**: They're kept — not silently dropped — they go into a dedicated "Unrecognized SEDOLs" sheet so the analyst knows exactly which inputs didn't match and can fix the input.

- **Q: This does per-row API calls — doesn't that scale badly?**
  - **A**: Yes, for large uploads it would. The fix is to batch the lookups (XpressFeed supports multi-SEDOL queries), cache repeated tickers, or for very large lists, make it a background job. I optimised for shipping a correct, readable first version — and I know exactly how I'd scale it.

- **Q: Why not just give analysts a Jupyter notebook?**
  - **A**: An API is shareable, governed, and reproducible — anyone can upload the same CSV and get the same result. A notebook is personal and manual. This is a single-purpose tool.
