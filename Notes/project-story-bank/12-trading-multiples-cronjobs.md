# 12 — Trading Multiples Cronjobs

- **Repo**: `qrt-gh-frg-trading-multiples-cronjobs`
- **Stack**: Python, Capital IQ (quanthub market_data), Pandas, NumPy, AWS S3, EKS CronJob
- **Your Role**: Built the data pipelines that feed the trading-multiples dashboards.

## Snapshot (30-second pitch)
"Cronjobs that pull historical trading-multiples data (P/E, P/B, dividend yield, EV/EBIT) for semiconductor (Foundry & Fab) and gaming companies from Capital IQ, transform it in Pandas, and land it in S3 for the Company Trading Multiples dashboard to render. It's the batch data layer behind an interactive Plotly Dash app."

---

## STAR Story — "Feed the dashboard fresh multiples every day, hands-off"

- **Situation**: Analysts needed daily-refreshed trading multiples for semiconductor and gaming companies to do valuation analysis, but the data had to come from Capital IQ and be aligned to business month-end dates.
- **Task**: Automate the daily data pull, transformation, and S3 hand-off so the dashboard always has current data with zero manual effort.
- **Action**:
  - Built separate pulls per universe (`SemiConductorDataPull.py`, `GamingDataPull.py`) plus a production entrypoint (`semi_main_prod.py`) using the firm's Capital IQ market-data package (`quanthub.market_data.api.capital_iq`).
  - Configured the QH data environment (`AWS_CLUSTER=QH`) and computed month-end business dates with Pandas offsets (`BMonthEnd`) so multiples align to reporting periods.
  - Transformed and cleaned in Pandas/NumPy, then wrote results to S3 for the dashboard to read.
  - Kept local vs prod entrypoints (`run_semi_local.py` vs `semi_main_prod.py`) and test variants (`test_semi_prod.py`) so I could validate a run locally before it hit the scheduled job.
- **Result**: The dashboard renders daily-fresh multiples for semis and gaming with no manual pulls — analysts open the app and the data is current.

---

## Technical Deep-Dive & Why

1. **Why split by universe (semi vs gaming)?**
   - Different company lists, indices, and quirks. Separate pulls mean one universe failing doesn't block the other, and each is independently testable.

2. **Why local + prod entrypoints?**
   - Data pulls are expensive and easy to get subtly wrong. A local entrypoint lets me validate transformations against a sample before committing to the scheduled prod run.

3. **Why S3 as the hand-off (not a DB)?**
   - The consumer is a stateless Dash app that reads point-in-time snapshots; S3 objects are cheap, versionable, and trivial for the app to load — no DB connection management in the dashboard tier.

4. **Why business-month-end dates?**
   - Valuation multiples are compared at consistent reporting points; aligning to business month-ends avoids comparing a mid-month snapshot against a period close.

---

## Code Samples

### Configure the QH Capital IQ data environment and pull (`application-source/semi_main_prod.py`, abridged)
```python
import os, sys, warnings, logging
from pandas.tseries.offsets import BMonthEnd
from quanthub.market_data.api import capital_iq as ciq  # firm's Capital IQ market-data package

warnings.filterwarnings("ignore")
os.environ["AWS_CLUSTER"] = "QH"  # point the data package at the QH cluster
os.environ["USER"] = "quy"

def blockPrint():  # silence the chatty library
    sys.stdout = open(os.devnull, "w")

blockPrint()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("art-gh-frg-trading-multiples-semiconductor-logger")
```

**Talking point**: The pattern is the same as my other pipelines — extract (Capital IQ), transform (Pandas), load (S3) — with local entrypoints for validation before committing to the scheduled job.

---

## Likely Follow-up Q&A

- **Q: Where does the data come from at render time?**
  - **A**: S3 snapshots produced by these cronjobs. The dashboard reads pre-computed data, never calls Capital IQ live — so even if Capital IQ is slow or down, the latest snapshot still renders.

- **Q: How do you handle Capital IQ rate limits or downtime?**
  - **A**: The pull runs once per day (off-peak), not per user request. If it fails, the previous day's snapshot is still in S3 and the dashboard still works — the email alert tells ops to investigate.

- **Q: What's the reusable pattern across all your Dash apps?**
  - **A**: `app.py` / `app_local.py` entrypoints, layout/controls/callbacks split, `support_functions` for data + per-dimension logic, S3-backed data from cronjobs, OKTA at the ingress, and per-user tracking. Consistency across apps makes them easy to hand over and maintain.
