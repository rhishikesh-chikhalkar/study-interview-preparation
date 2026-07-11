# CRGI Equity Yield Lab

06 — CRGI Equity Yield Lab API

Snapshot

STAR story — “Turn a manual equity-screening workflow into one upload"

Situation. Analysts screened equities for yield ideas by hand — looking up each SEDOL's yield, market cap, EPS growth, and whether CG already held it, then filtering in Excel. Slow and inconsistent.

Task. Automate the whole enrichment-and-filter Pipeline into a single upload-to-download API.

Action.

* Builta POST /uploadSEDOLs endpoint that accepts a CSV, reads it into Pandas from an
° get_pricedivyld(SEDOL)) — price & dividend yield, : 2
° get _companyestimates(ticker, exchange) — CompanyId & currency,
° get_epsgrowth(Companyid)) > FY1/FY2/FY3 EPS growth.
° cross-reference CG-held positions pulled from $3. : = =


* Applied a central fFilter_logic that tags each row with include + the iret it wet (dividend yield, market cap, EPS-growth thresholds).
* Separated results into three Excel sheets (Included / All / Unrecognized SEDOLs) so analysts see both the picks and the SEDOLs the system couldn't resolve.
* Streamed the workbook back via StreamingResponse with a timestamped filename: added ‘/health for Kubernetes probes.

Result. A screening pass that took an analyst significant manual effort became a single CSV upload returning a ready-to-use, auditable Excel workbook.

Technical deep-dive & why

* Why return three sheets including “Unrecognized SEDOLs”? Data quality transparency. Hiding unmatched SEDOLs would make the analyst trust a report that silently dropped rows. Surfacing them builds trust
them fix inputs. il U sal

* Why stream the file (StreamingResponse from BytesI0)? No temp files on disk, no cleanup, and it works cleanly in a stateless EKS pod. The workbook is built in memory and streamed straight to the
the correct spreadsheet media type and a Content—Disposition attachment header. iL

* Why centralise filter_logic ? The include/exclude criteria are the business rules — keeping them in one function (returning both the decision and why) makes the logic testable and auditable, and the
column explains every inclusion.

* Why enrich in discrete steps with apply(... , Tesult_type="expand") ? Each external call returns multiple fields; expanding them into typed columns keeps the DataFrame tidy and ead ennchert
independently debuggable. = ; i

ee ee ee eee



Technical deep-dive & why ‘i

Why retum three sheets including “Unrecognized SEDOLs"? Data quality transparency. Hiding unmatched SEDOLs would make the analyst trust a feport that silently dropped rows. Surfacing them builds trust and lets

them fix inputs,

Why stream the file (StreamingResponse from BytesIO)? No temp files on disk, no cleanup, and it works cleanly in a stateless EKS Pod. The workbook is built in memory and streamed straight to the client with
the correct spreadsheet media type anda Content—Disposition attachment header. 2 = ali
Why centralise filter_logic? The include/exclude criteria are the business rules — keeping them in one function (returning both the decision and why) makes the logic testable and auditable, and the leriteria ir
column explains every inclusion. y

Why enrich in discrete steps with apply(..., result
independently debuggable.

) ? Each external call returns multiple fields; expanding them into typed columns keeps the DataFrame tidy and each enrichment =

Code samples (real, extracted from the repo) : | : : = int

One upload — enrich — filter — multi-sheet Excel, streamed back (app/main.py, abridged)


@app. post ("/uploadSEDOLs" )
async def upload(file: UploadFile = File(...)): es

df = pd. read_csv(BytesIO(await file.read())) ‘
df = dt .merge(get_pricedivyld(df["SEDOL"1), how="left", on="SEDOL")
unrecognized = df ldf["tickerSymbol"].isna()] = # Necks don't silently drop
df = df.dropna(subset=["tickerSymbol"]) te os

# each enrichment returns several fields —> expand into ty, ed column
af{["CompanyId", "Currency"]] = df.apply( = 6
lambda r: get_companyestimates(r.tickerSymbol, r.exchangeSymbol),
axis=1, result_type="expand")
df(["EpsGrowthFY1", "“EpsGrowthFY2", "EpsGrowthFY3"]] = if a
lambda r: get_epsgrowth(r-CompanyId), axis=1, resu]
df["CGheld"] = df["SEDOL"].isin(get_positions()["SEDOL

# central business rule: returns the decision AND why it we included

df(["include", “criteria"]] = df.apply(lambda r: filter_logic(r), axis-1, result_type="expand")

output = BytesI0()
with pd.ExcelWriter(output) as writer:
df[df.include].to_excel(writer, "Included Items", index=False)
df.to_excel(writer, "All Items", index=False) :
unrecognized.to_excel(writer, "Unrecognized SEDOLs", index=False)

output.seek(0)
return StreamingResponse(

output,
media_type="application/vnd.openxmlformats—of ficedocument. spreadsheetml.sheet",

headers={"Content—-Disposition": “attachment; filename=CRGI Equity Yield Lab.xlsx"})

# stream from memory, no temp file




Honest caveats to be cy for

* The current enrichment uses row-wise apply calling XpressFeed perrow—
repeated lookups. This is a great “how would ey make it ite al 1

Likely follow- “up Q&A

Q: How do you handle SEDOLs XpressFeed can't resolve? A hey're: cropped
the input. E

iS. NaN ut not silently — they go into a dedicated “Unrecognized SEDOLs” sheet: so

purpose tool.
