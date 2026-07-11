# Trading Multiples Cronjobs

= A SEI BN ES nae |

Si ae eee A OTYOOS ING. |X ey
4 0

12 — Trading Multiples Cronjobs

Repo: qrt—gh-f: rq-trading-multiples“eronjobs + Stack: Python, Capital 1Q (quanthub market_data), Pandas, NumPy, AWS S3, EKS CronJob Your role: Built the data Pipelines that feed the trading-multiples
dashboards.

Snapshot

“Cronjobs that pull historical trading-multiples data (P/E, P/B, dividend yield, EV/EBIT) for semiconductor (Foundry & Fab) and gaming companies from Capital IQ, transform it in Pandas, and land it in S3 for the Company

Trading Multiples dashboard to render. It's the batch data layer behind an interactive Plotly Dash app.”

STAR story — "Feed the dashboard fresh multiples every day, hands-off"

Task. Automate the daily data pull, transformation, and $3 hand-off so. the dashboard always has current data with zero manual effort.

Action. i p
i j
° Built separate pulls per universe (SemiConductorDataPull. py . GamingdataPull spy) plus a production entrypoint (Semi_main prod py) using the firm's Capital 1Q market-data package
= r
(quanthub.market_data.api. capital iq). 2 =
* Configured the QH data environment (AWS_CLUSTER=QH) and computed month-end business da
* Transformed and cleaned in Pandas/NumPy, then wrote results to S3 for the dashboard to read.
* Kept local vs prod entrypoints ( run_semi_local.py vs semi_mai -Brodipy) and test variants (test Semi prod. Py) so | could validate a run locally before it hit the scheduled job.

tes with Pandas offsets (BMonthEnd) so multiples align to reporting periods.

Result. The dashboard renders daily-fresh multiples for semis and gaming with no manual pulls — aes open the app and the data is current.

Technical deep-dive & why :% | 4 | SEsvisricie a

* Why split by universe (semi vs gaming)? Different company lists, indices, and quirks. Separate pulls mean one universe failing doesn’t block the other, and each is independently testable. i
gainst a sample before committing to the scheduled prod run. iu

Why local + prod entrypoints? Data pulls are expensive and easy to get subtly wrong. A local entrypoint lets me validate transformations a
Why S3 as the hand-off (not a DB)? The consumer is a stateless Dash app that reads point-in-time snapshots; $3 objects are cheap, versionable, and trivial for the app to load — no DB connection management Wo tes

dashboard tier.
Why business-month-end dates? Valuation multiples are compared at consistent reporting points; aligning to business month-ends avoids comparing a mid-month snapshot against a period close.

Code samples (real, extracted from the repo) gs

Configure the QH Capital IQ data environment and pull, quietly (appl ication—source/semi_main. prod. py. abridged)




* why business-month-end aates? Valuation muitipies are Compared at consistent feporting points;

aligni

Code samples (real, extracted from the repo)

Configure the QH Capital IQ data environment and pull, quietly (application Solrce/ semi maih prod, Bi Sbriggecy

import os, SyS, warnings, logging
from Pandas .tseries offsets import BMonthEnd _
| from quanthub.market_data.api import Capital iq as ciq

# firm's Capital IQ Market—data package

warnings. filterwarnings( "ignore")
os.environ["AWS_CLUSTER"] == "QH"
Os-environ["USER"] = "Quy"

# point the data package at the QH cluster

def blockPrint(): ae # silence the chatty library i
Sys-stdout = open(os.devnull, “w") : :

blockPrint() 5 a \

fogging. basicContig(1evel=logging. INFO, format="%(asctime) s oe %(leveIname)s tt %(message)s")
logger = Hasing-Getlogger (“art-ah-frg “eraging mul tip las Semieoniiuctar “Iogéa) =| 2

for a scheduled job.

SH Q sea
