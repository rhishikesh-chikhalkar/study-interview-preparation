# 03 — Portfolio Metrics UI

- **Repo**: `art-gh-frg-portfolio-metrics-ui`
- **Stack**: React, TypeScript, AG Grid, Mantine, CRACO + Module Federation, SCSS
- **Your Role**: Built/owned the frontend that consumes the Portfolio Metrics API.

## Snapshot
"I also owned the frontend that consumes my API — full-stack ownership, not a claim to be a frontend specialist."

---

## STAR Story — "Give PMs a spreadsheet-grade editing experience on the web"

- **Situation**: The API made scenario modelling possible, but PMs expected an Excel-grade grid: inline editing, custom cell renderers, sorting, loading/no-rows overlays.
- **Task**: Deliver a responsive editable grid that talks to the API and fits inside the QuantHub micro-frontend shell.
- **Action**:
  - Used AG Grid with custom cell renderers (`CompanyNameCellRenderer`, `WidgetCellRenderer`), typed column definitions, and custom loading/no-rows overlays.
  - Structured the app into components (`AssumptionTable`, `ColumnsSettings`, `ClonePortfolioModal`, `DeletePortfolioDialog`, `Chart/LineChart`, `Header`, `HealthCheck`) with typed API service functions.
  - Packaged it as a Module Federation micro-frontend (CRACO config) so it loads inside the shared platform shell rather than shipping as a standalone SPA.
  - Split bootstrap (`bootstrap.tsx`) from App to satisfy Module Federation's async boundary, wrapped in `BrowserRouter` and `React.StrictMode`.
- **Result**: PMs edit assumptions inline and see recalculated numbers, matching the Excel workflow they came from — but shareable, versioned via scenarios, and integrated into the platform.

---

## Technical Deep-Dive & Why

- **Why Module Federation / micro-frontend?**
  - The firm runs a single shared container/shell application. Module Federation lets us deploy the portfolio metrics UI independently without rebuilding the shell, keeping our release cadence separate.
- **Why TypeScript?**
  - The API returns typed financial records; TS types mirror the Pydantic response models so a shape change surfaces at compile time, not as a runtime blank chart.
- **Why split `bootstrap.tsx` from index?**
  - Module Federation requires an async boundary before the shared React instance loads; the dynamic import bootstrap pattern is the standard way to satisfy that.

---

## Code Samples

### The Module Federation async boundary — mounts the app under a shared React container (`app/src/bootstrap.tsx`)
```tsx
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App";

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById("root")
);
```

- **Talking point**: `index.tsx` does a dynamic `import("./bootstrap")`, which creates the async boundary. This allows the host shell to resolve and load shared dependencies (like React) before mounting this remote app.

---

## Likely Follow-up Q&A

- **Q: How do you keep frontend types in sync with the backend?**
  - **A**: The API is FastAPI, so it publishes an OpenAPI schema; the TS service-layer types mirror the Pydantic models. A breaking API change immediately flags compile-time errors in the service functions.
- **Q: How do you handle loading and empty states in the grid?**
  - **A**: Custom AG Grid `LoadingOverlay` and `NoRowsOverlay` components plus a shared React state trigger them during API requests, providing visual feedback instead of a frozen table.
- **Q: What's the trade-off of a micro-frontend?**
  - **A**: You gain independent deploys and a shared shell, but you take on deployment/dependency sharing complexity (shared React version, remote loading failures). A shared React version configuration manages singletons, and a health-check component surfaces remote/backend issues early.
