# Company Trading Multiples App


a nl mbt

14 — Company Trading Multiples App

| Repo: qra-gh-frg-company—trading-app “Stack: Plotly Dash 2.15, Plotly 5.5, Python, Pandas, AWS $3, EKS Your role: Built the interactive multiples dashboard (front end for the trading-multiples cronjobs), Ll

Snapshot

STAR story — "Give analysts an interactive multiples explorer with exports"

Situation. Analysts needed to explore historical valuation multiples for semis and gaming companies and compare them against sector indices and then drop the results into Excel/Word for research notes.

Task. Build an interactive dashboard with flexible time Tanges, index comparisons, and native Excel/Word export.
Action.

* Built a Dash app (layout/controls/callbacks) with company-specific charts and selectable time ranges (YTD, 1Y, 5Y, 10Y, All).

* Added index comparisons (Asia Foundry, Memory Foundry, SemiCap Equipment, Asia Gaming) so a company's multiple is seen against ifs peer index.

* Implemented Excel and Word exports so a chart/table becomes a research artifact in one click. = Sai
* Read daily-refreshed data from S3 (from the cronjobs), keeping the UI fast by never calling Capital IQ live. =
* Added helper/tracker modules (helper functions. py, tracker -py) for shared logic and usage tracking. 25

Result. Analysts explore multiples interactively and export straight to Excel/Word — the to:

Technical deep-dive & why

and each layer deploys independently. ‘i oe
Why server-generated Excel/Word (vs client export)? These exports are structured documents (formatted tables, multiple sheets/sections), not just a screenshot — generating them server-side with the underlying data

gives analysts a real, editable artifact.

* Why configurable time ranges + index ‘overlays? Valuation analysis is inherently relative

multiple sheets/sections), not

Likely follow-up Q&A | : E — “

— over time and vs peers. Making range and index first-class controls

Q: Where does the data come from at render time? A: S3 Snapshots produced

by the trading-multiples cronjobs. The dashboard reads pre-comp
snapshot still renders. = % : 22
