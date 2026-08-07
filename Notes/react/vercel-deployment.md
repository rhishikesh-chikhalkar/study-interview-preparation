# Deploying React Applications to Vercel

## Overview & Core Concepts

Vercel is a global cloud platform designed for static sites and serverless web applications.
It offers zero-configuration deployments for React applications created with Vite, Create
React App, Next.js, and other modern frontend frameworks.

When deploying a React app to Vercel, the platform inspects the repository structure, detects
the build tool, runs the build command (e.g., `npm run build`), and distributes the generated
static assets across Vercel's global Edge Network (CDN).

---

## Step-by-Step Deployment Workflow

### 1. Account Signup and GitHub Connection
1. Visit [Vercel](https://vercel.com) and sign up using your **GitHub** account.
2. Grant Vercel read/write access to your repositories (all repositories or selected ones).
3. Authorize the Vercel GitHub App to enable webhooks for automated deployments.

### 2. Import & One-Click Deployment
1. Navigate to the Vercel Dashboard and click **Add New > Project**.
2. Select the target GitHub repository from the connected account list.
3. Configure project settings:
   - **Framework Preset**: Automatically detected (e.g., Vite, Create React App, Next.js).
   - **Root Directory**: `./` (or subfolder if in a monorepo).
   - **Build Command**: `npm run build` (or `vite build`).
   - **Output Directory**: `dist` (Vite) or `build` (CRA).
   - **Environment Variables**: Add key-value pairs required at build time.
4. Click **Deploy**. Vercel clones the repo, installs dependencies, builds the project, and
   provisions a live deployment URL (e.g., `https://my-app.vercel.app`).

### 3. Vercel CLI Deployment Workflow
For local testing or non-Git pipelines, the Vercel CLI can be used directly:

```bash
# Install Vercel CLI globally or run via npx
npm install -g vercel

# Authenticate and link project
vercel login
vercel link

# Deploy a preview build
vercel

# Deploy directly to production
vercel --prod
```

To sync remote environment variables locally:
```bash
vercel env pull .env.local
```

---

## Client-Side Routing & `vercel.json` Configuration

Single-Page Applications (SPAs) manage routing in the browser. When a user requests a path
like `/dashboard` directly, the server will return a `404 Not Found` error unless configured
to rewrite all requests to `index.html`.

### SPA Rewrite Configuration (`vercel.json`)

Create a `vercel.json` file in the root directory:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://api.example.com/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Advanced `vercel.json` (Security Headers & Caching)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000; includeSubDomains"
        }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## Environment Variables & Scoping

Environment variables in Vercel are assigned to specific target environments:

1. **Production**: Applied to deployments triggered from the main branch.
2. **Preview**: Applied to pull requests and non-production branch pushes.
3. **Development**: Pulled down locally via `vercel env pull`.

### Rules for React Environment Variables
- In Vite, variables must be prefixed with `VITE_` (e.g., `VITE_API_URL`).
- In Create React App, variables must be prefixed with `REACT_APP_`.
- Static React apps embed variables into compiled bundle assets at **build time**, not runtime.
- Never place private secret keys (e.g., database passwords, master API secret keys) inside
  frontend React environment variables.

---

## Preview Deployments & Branching Strategy

- **Pull Request Previews**: Every open PR generates an isolated preview deployment URL.
- **Vercel Bot Integration**: Automatically comments on the PR with preview links and logs.
- **Instant Rollbacks**: Instant point-in-time rollbacks from the Vercel dashboard without
  re-running build pipelines.

---

## Common Pitfalls & Troubleshooting

1. **404 Error on Page Refresh**:
   - Cause: Deep routes requested directly from server without SPA rewrite.
   - Fix: Add rewrite rule to `vercel.json` mapping `/(.*)` to `/index.html`.

2. **Environment Variables Missing in Production**:
   - Cause: Variable names lack required prefix (`VITE_` / `REACT_APP_`) or were not re-built.
   - Fix: Ensure correct prefix and trigger a new deployment to re-compile the bundles.

3. **Wrong Output Directory**:
   - Cause: Mismatch between build command output folder and Vercel project settings.
   - Fix: Standardize on `dist` for Vite or `build` for CRA in project settings or `vercel.json`.

---

## References & Authoritative Sources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel `vercel.json` Reference](https://vercel.com/docs/projects/project-configuration)
- [Vite Static Site Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [React Official Documentation](https://react.dev)

---

# Interview Questions & Answers (5 YOE IT Professional)

## 1. Conceptual / Theoretical

### Question:
How does Vercel's Edge Network distribute static React Single-Page Applications (SPAs)
compared to hybrid framework applications (e.g., Next.js with Server Components)? What
happens during a request for a static asset versus a dynamic route?

### Answer:
For static React SPAs (built with Vite or CRA), Vercel acts as an ultra-low latency Static Site
Host. During the build phase, Vercel executes the bundle step and uploads the resulting
compiled HTML, CSS, JS, and asset files directly to Vercel's global Anycast Edge Network.
Every request to a static SPA is answered directly from the nearest Edge POP cache with HTTP
304/200 responses without triggering any backend function invocation.

For hybrid React applications (e.g., Next.js with App Router), Vercel distinguishes between
three rendering primitives:
1. **Static Assets / Prerendered HTML**: Served directly from Edge storage.
2. **Server-Side Rendered (SSR) Routes**: Routed to regional Serverless Functions or Edge
   Functions that execute Node.js / Web API runtimes on-demand to render HTML dynamically.
3. **Incremental Static Regeneration (ISR)**: Served from CDN cache while stale, while an
   asynchronous background serverless function regenerates the static artifact in the background.

### Follow-up Questions an Interviewer Might Ask:
- How does CDN cache invalidation work on Vercel when a new production deployment is published?
  *(Answer: Vercel uses atomic deployments with instant cache purge via URL versioning and
  deployment IDs).*

---

## 2. Practical / Scenario-Based

### Question:
A team deployed a React SPA using React Router v6 to Vercel. Home page navigations work
smoothly, but when users bookmark or refresh a nested URL like
`https://myapp.vercel.app/users/123`, Vercel returns a `404 Not Found` page. What is the root
cause, and how do you resolve it while ensuring `/api/*` backend proxies remain unaffected?

### Answer:
**Root Cause**:
When a client navigates internally via React Router (e.g., `<Link to="/users/123">`), the
browser updates the address bar using HTML5 History API (`pushState`) without requesting a
new HTML document from the server. However, when the user refreshes or hits
`https://myapp.vercel.app/users/123` directly, the browser sends an HTTP GET request to
Vercel for `/users/123`. Because there is no actual physical file or server endpoint at
`/users/123` in the output directory, Vercel's static asset server returns `404 Not Found`.

**Resolution**:
Add a `vercel.json` file in the project root to configure server rewrites. We must ensure
that backend API requests (e.g., `/api/*`) pass through or rewrite to the backend server, while
all non-API paths rewrite to `/index.html` so the React application can boot up and render the
correct view client-side.

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.production-server.com/api/:path*"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Follow-up Questions an Interviewer Might Ask:
- What is the difference between a rewrite and a redirect in `vercel.json`?
  *(Answer: A rewrite transparently serves content from the destination path keeping the URL
  intact in the browser, whereas a redirect issues an HTTP 301/302 status forcing a client
  address bar URL change).*

---

## 3. Coding / Implementation

### Question:
Write a complete, production-grade `vercel.json` file for a Vite-based React application that:
1. Defines explicit build and framework settings.
2. Enables CORS headers for public API assets under `/static-data/*`.
3. Implements standard web security headers (CSP, HSTS, X-Frame-Options, Content-Type-Options).
4. Sets long-term immutable caching for Vite's hashed assets (`/assets/*`).
5. Handles SPA client-side routing fallback.

### Answer:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=()"
        },
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000; includeSubDomains; preload"
        }
      ]
    },
    {
      "source": "/static-data/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, OPTIONS"
        }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Follow-up Questions an Interviewer Might Ask:
- Why is `max-age=31536000, immutable` safe for assets in `/assets/` but dangerous for
  `/index.html`?
  *(Answer: Modern bundlers like Vite append unique content hashes to filenames in `/assets/`.
  If code changes, the filename changes. `index.html` references those scripts; caching
  `index.html` long-term would prevent users from seeing updates).*

---

## 4. Scenario / CI-CD Integration

### Question:
An enterprise team wants to deploy their React application to Vercel. Compare using Vercel's
native GitHub App integration against triggering deployments via Vercel CLI inside GitHub
Actions pipelines. What are the trade-offs, and when would you mandate GitHub Actions?

### Answer:

- **Native Vercel GitHub App Integration**:
  - *Setup*: Zero configuration; one-click repository linking.
  - *Speed*: Faster (build starts immediately upon Git push).
  - *Quality Gates*: Runs build directly; optional check blocking via Git status.
  - *Governance*: Limited to Vercel account permissions.

- **Vercel CLI in GitHub Actions Pipeline**:
  - *Setup*: Requires custom `.github/workflows/deploy.yml`, token secrets.
  - *Speed*: Slower (spins up GitHub runner before invoking CLI).
  - *Quality Gates*: Enforces multi-stage pipelines (unit tests, Playwright E2E tests, SAST)
    before deploying to Vercel.
  - *Governance*: Centralized compliance (OIDC credentials, secret rotation, approval gates).

**When to choose GitHub Actions over Native Integration**:
1. **Mandatory Quality Gates**: When code must pass extensive integration testing before creating
   even a Preview deployment.
2. **Security & Secrets Isolation**: When deployment secrets must be governed by enterprise
   HashiCorp Vault or GitHub OIDC identity providers instead of permanent Vercel tokens.
3. **Multi-Cloud Synchronization**: When frontend deployment must execute atomically alongside
   database migrations or backend microservices deployments.

### Follow-up Questions an Interviewer Might Ask:
- How do you pass the generated Vercel Preview URL from a Vercel CLI GitHub Action step to
  downstream automated E2E testing jobs?
  *(Answer: Capture stdout of `vercel deploy` or parse `DEPLOYMENT_URL` output variable and
  pass it to subsequent job steps).*

---

## 5. System Design / Architecture

### Question:
Design a zero-downtime, multi-environment deployment strategy on Vercel for a mission-critical
React SPA consuming microservices APIs across Development, Staging, and Production environments.
Include environment variable isolation, feature flagging, and rollback strategies.

### Answer:

### Architecture Blueprint

```
+-----------------------------------------------------------------------------------+
|                                  GITHUB REPOSITORY                                |
+-----------------------------------------------------------------------------------+
       |                                   |                                   |
 (Push to main)                    (PR to main)                   (Push to dev)
       |                                   |                                   |
       v                                   v                                   v
+------------------+              +------------------+              +------------------+
|    PRODUCTION    |              | PREVIEW / STAGING|              |   DEVELOPMENT    |
|   ENVIRONMENT    |              |   ENVIRONMENT    |              |   ENVIRONMENT    |
+------------------+              +------------------+              +------------------+
| VITE_API_URL:    |              | VITE_API_URL:    |              | VITE_API_URL:    |
| api.domain.com   |              | staging.api...   |              | dev.api.domain...|
+------------------+              +------------------+              +------------------+
       |                                   |                                   |
       v                                   v                                   v
+-----------------------------------------------------------------------------------+
|                           VERCEL GLOBAL EDGE NETWORK (CDN)                         |
+-----------------------------------------------------------------------------------+
```

### Key Architectural Pillars:

1. **Environment Parity & Variable Scoping**:
   - Store API endpoints (`VITE_API_URL`), analytics keys (`VITE_ANALYTICS_KEY`), and auth
     config in Vercel Project Settings mapped strictly to Production, Preview, and Development
     targets.
   - Use dynamic runtime feature flagging (e.g., LaunchDarkly or Flagsmith) rather than
     build-time flags so features can be toggled without triggering full Vercel rebuilds.

2. **Branching & Deployment Promotion**:
   - `main` branch pushes automatically trigger **Production Deployments**.
   - PR branches trigger ephemeral **Preview Deployments** linked to Staging API services.
   - Domain alias mapping: `app.domain.com` points to Production `main`; `staging.domain.com`
     points to the `staging` branch.

3. **Zero-Downtime Atomic Swaps & Rollbacks**:
   - Every build on Vercel receives an immutable deployment ID (e.g., `dpl_12345`).
   - Alias switching is atomic at the DNS/CDN routing layer.
   - If a regression occurs post-deployment, trigger an **Instant Rollback** via Vercel Dashboard
     or CLI (`vercel alias set <previous-deployment-id> app.domain.com`), instantly redirecting
     Edge network traffic back to the last known good build artifact in under 1 second.

4. **Monitoring & Performance Budgets**:
   - Enable Vercel Speed Insights and Web Vitals analytics (LCP, FID/INP, CLS).
   - Integrate Sentry for real-time frontend runtime error logging mapped via source maps
     uploaded during Vercel build pipelines.

### Follow-up Questions an Interviewer Might Ask:
- How do you handle CORS policies on backend microservices when Vercel generates dynamic preview
  URLs for every PR?
  *(Answer: Configure backend API CORS middleware to match wildcard regex patterns like
  `https://myapp-*-company.vercel.app` or use Vercel reverse proxy rewrites in `vercel.json` to
  route `/api/*` requests on the same origin).*
