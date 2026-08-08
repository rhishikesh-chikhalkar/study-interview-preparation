# Render Go Production Web Service

Production-grade, industry-standard Go microservice configured for single-binary deployment
to Render PaaS platform. Implemented using Go's built-in `net/http` standard library, `log/slog`
structured JSON logging, dynamic `$PORT` binding, multi-stage Docker containerization, and graceful
shutdown handling.

---

## Technical Stack & Architecture

- **Language Runtime**: Go 1.25 (Standard Library Only)
- **Application Server**: Built-in `net/http` HTTP Server
- **Structured Logging**: Standard library `log/slog` (JSON handler to stdout)
- **PaaS Platform**: Render Web Service
- **Containerization**: Multi-stage Docker build (`golang:1.25-alpine` -> `alpine:latest`)
- **Concurrency & Safety**: Mutex-protected thread-safe in-memory task repository

---

## Project Layout

```text
render-go-service/
├── .dockerignore                # Exclusions for Docker build context
├── .env.example                 # Environment variables configuration template
├── Dockerfile                   # Multi-stage static compilation container definition
├── Makefile                     # Automation tasks (run, test, build, docker-build)
├── README.md                    # Service setup & deployment documentation
├── go.mod                       # Go module dependencies file
├── render.yaml                  # Render Infrastructure Blueprint
├── cmd/
│   └── api/
│       └── main.go              # Application entrypoint & HTTP server lifecycle
└── internal/
    ├── config/                  # Strongly-typed environment variables parser
    ├── handler/                 # HTTP handlers (/healthz, /readyz, /api/v1/tasks)
    ├── middleware/              # Production middleware (logging, CORS, recovery, auth)
    ├── model/                   # Domain entities and JSON DTOs
    └── service/                 # Business logic and in-memory storage layer
```

---

## Local Development & Testing

### 1. Running Unit Tests

Run unit tests covering HTTP handlers and business logic layer:

```bash
make test
```

### 2. Running Service Locally

Start the HTTP server on `http://localhost:8080`:

```bash
make run
```

### 3. API Verification Commands (cURL)

#### Liveness Probe (`/healthz`)
```bash
curl -i http://localhost:8080/healthz
```

#### Readiness Probe (`/readyz`)
```bash
curl -i http://localhost:8080/readyz
```

#### List Tasks (`GET /api/v1/tasks`)
```bash
curl -i http://localhost:8080/api/v1/tasks
```

#### Create Task (`POST /api/v1/tasks`)
```bash
curl -i -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Deploy to Render","description":"Test live URL on Render PaaS"}'
```

#### Get Task by ID (`GET /api/v1/tasks/{id}`)
```bash
curl -i http://localhost:8080/api/v1/tasks/task-1
```

---

## Step-by-Step Render Deployment Guide

### Option 1: Render Dashboard Deployment (UI)

1. Push your repository to GitHub.
2. Log into [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Web Service**.
3. Select your GitHub repository.
4. Configure service parameters:
   - **Name**: `render-go-service`
   - **Root Directory**: `golang/.production/render-go-service`
   - **Environment**: `Docker`
   - **Region**: Oregon (US West) or closest region
   - **Branch**: `main`
5. Advanced Configuration:
   - **Health Check Path**: `/healthz`
   - Add Environment Variables:
     - `ENV`: `production`
     - `API_KEY`: `your-production-secret-key` (optional)
6. Click **Create Web Service**. Render will execute the multi-stage Docker build and start the
   container binding automatically to the dynamic `$PORT`.

### Option 2: Render Blueprint Deployment (`render.yaml`)

1. In Render Dashboard, click **Blueprints** -> **New Blueprint Instance**.
2. Connect your GitHub repository. Render detects `render.yaml` and provisions the web service automatically.

---

## Testing Live Render URL

Once deployed, Render provides a unique URL (e.g. `https://render-go-service-xyz.onrender.com`).

Verify live deployment using cURL:

```bash
# 1. Test Live Healthz Endpoint
curl -i https://<your-render-app>.onrender.com/healthz

# 2. Test Live Task Creation
curl -i -X POST https://<your-render-app>.onrender.com/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Verify Render Live URL","description":"Success!"}'

# 3. Test Live Task Listing
curl -i https://<your-render-app>.onrender.com/api/v1/tasks
```
