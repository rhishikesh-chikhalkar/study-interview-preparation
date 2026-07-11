# 07 — Company Forecast API

- **Repo**: `art-gh-frg-company-forecast-api`
- **Stack**: FastAPI, Snowflake, Pandas, AWS EKS
- **Your Role**: Built the forecast scenario API.

## Snapshot (30-second pitch)
"A FastAPI service that powers exit-PE-driven forecast scenarios for company-level analysis. It lets analysts model how different exit P/E assumptions affect forecasted returns for individual companies, pulling fundamentals from Snowflake and computing projections in Pandas. It's the company-level complement to the portfolio-level Portfolio Metrics API."

---

## STAR Story — "Give analysts company-level what-if scenarios"

- **Situation**: Analysts needed to model exit-PE-driven forecasts at the individual company level — what happens to projected returns if we assume a different terminal P/E for this company?
- **Task**: Build a service that takes exit-P/E assumptions and returns computed forecasted returns.
- **Action**:
  - Built a FastAPI service that accepts company identifiers and exit-P/E assumptions.
  - Sourced fundamentals from Snowflake (same data layer pattern as the Portfolio Metrics API).
  - Computed multi-year forecasted returns in Pandas based on the provided assumptions.
  - Deployed on EKS with the standard Docker/Helm/CI/CD pattern used across all FRG services.
- **Result**: Analysts run company-level scenario analysis through the API instead of manual Excel calculations, with consistent methodology and shareable results.

---

## Technical Deep-Dive & Why

1. **Why a separate service from the Portfolio Metrics API?**
   - The Portfolio Metrics API operates at the portfolio level (summaries across holdings). This service operates at the individual company level. Separation keeps each focused and independently deployable.

2. **Why the same Snowflake + Pandas pattern?**
   - Consistency with the rest of the FRG API estate — same auth (Snowflake key-pair), same compute layer (Pandas), same deployment (EKS). Reduces cognitive load and makes the codebase maintainable.

---

## Likely Follow-up Q&A

- **Q: How does this relate to the Portfolio Metrics API?**
  - **A**: Portfolio Metrics works at the portfolio level (aggregating across all holdings); this works at the single-company level. They share the same Snowflake data source and similar computation patterns, but serve different analytical workflows.

- **Q: How would you scale this for many concurrent analysts?**
  - **A**: The same approach as the Portfolio Metrics API — pre-compute daily-stable data in a batch tier, cache hot results, and scale EKS pods horizontally. The service is stateless.
