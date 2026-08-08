# Connecting React (Vercel) to Flask API (Render) & Fixing CORS

Comprehensive study notes and 5 YOE interview Q&As for connecting a React SPA deployed on
Vercel to a Python Flask REST API microservice deployed on Render, managing CORS policies,
configuring Vercel rewrites, and implementing production-grade end-to-end connectivity.

---

## 1. Structured Notes

### Fullstack Architecture Overview

In a decoupled cloud architecture, the React frontend and Flask API backend run on separate
domains and deployment platforms:

```text
+------------------------------------+           +------------------------------------+
| Vercel Global Edge CDN             |           | Render Cloud Platform              |
| https://study-interview-prepar...  |           | https://flask-rag-api-191y...      |
|                                    |           |                                    |
| +--------------------------------+ |  HTTP     | +--------------------------------+ |
| | React SPA (Vite/CRA)           | |  POST     | | Gunicorn WSGI Master Process   | |
| | - AiAssistant Component        | | --------> | | - Flask App Factory (create_app) | |
| | - Dynamic VITE_API_URL         | | <-------- | | - CORS Preflight & Response    | |
| +--------------------------------+ |  JSON     | +--------------------------------+ |
+------------------------------------+           +------------------------------------+
```

- **Frontend Platform (Vercel)**: `https://study-interview-preparation.vercel.app`
- **Backend Platform (Flask on Render)**: `https://flask-rag-api-191y.onrender.com`
- **Backend Platform (Go on Render)**: `https://render-go-service-txtm.onrender.com`
- **Communication Protocol**: Asynchronous HTTP/HTTPS API calls using `fetch` or `axios`.

---

## Understanding CORS (Cross-Origin Resource Sharing)

### Same-Origin Policy (SOP)
Browsers enforce SOP to prevent malicious sites from reading sensitive data from another site.
An origin is defined by the tuple `(Scheme, Host, Port)`.

- `https://my-app.vercel.app` (Origin A)
- `https://flask-api.onrender.com` (Origin B)

Because the hosts differ, requests from Origin A to Origin B are cross-origin.

### Simple Requests vs Preflighted Requests
Browsers issue a preflight `OPTIONS` HTTP request before sending the actual request if:
1. HTTP method is `PUT`, `DELETE`, `PATCH`, or custom methods.
2. Custom HTTP headers are included (e.g., `Authorization`).
3. `Content-Type` is not one of `application/x-www-form-urlencoded`, `multipart/form-data`, or
   `text/plain` (e.g., `application/json`).

```text
Browser                           Render Flask API
   |                                    |
   | --- OPTIONS /ask ----------------> |  (Preflight Request)
   |     Access-Control-Request-Method  |
   |                                    |
   | <-- 200 OK ----------------------- |  (Preflight Response)
   |     Access-Control-Allow-Origin    |
   |     Access-Control-Allow-Methods   |
   |                                    |
   | --- POST /ask (JSON Body) -------> |  (Actual Request)
   | <-- 200 OK (JSON Response) ------- |  (Actual Response)
```

---

## Two Integration Strategies

### Strategy 1: Direct CORS Configuration in Flask (Recommended for Decoupled APIs)

Configure Flask to return explicit CORS headers on all HTTP responses and preflight `OPTIONS`.

#### Flask Implementation (`__init__.py`):

```python
from typing import Any, Optional
from flask import Flask, request


def create_app() -> Flask:
    app = Flask(__name__)

    @app.before_request
    def handle_options() -> Optional[Any]:
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = (
                "Content-Type,Authorization"
            )
            response.headers["Access-Control-Allow-Methods"] = (
                "GET,PUT,POST,DELETE,OPTIONS"
            )
            response.headers["Access-Control-Max-Age"] = "86400"
            return response
        return None

    @app.after_request
    def add_cors_headers(response: Any) -> Any:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type,Authorization"
        )
        response.headers["Access-Control-Allow-Methods"] = (
            "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    return app
```

---

### Strategy 2: Vercel Reverse Proxy Rewrites (Bypasses Browser CORS)

Vercel can act as a reverse proxy, mapping relative paths (`/api/*`) on the frontend domain
directly to the Render backend URL. Because the browser calls the same domain
(`https://my-app.vercel.app/api/ask`), browser CORS restrictions do not apply.

#### `vercel.json` Setup:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://flask-rag-api-191y.onrender.com/:path*"
    },
    {
      "source": "/go-api/:path*",
      "destination": "https://render-go-service-txtm.onrender.com/:path*"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## Dynamic Environment Variables in React (Vite)

In Vite React applications, environment variables must begin with `VITE_`.

```javascript
// src/config/api.js
export const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  "https://flask-rag-api-191y.onrender.com"
).replace(/\/$/, "");
```

- Local Dev `.env.local`: `VITE_API_URL=http://localhost:5001`
- Vercel Production Settings: `VITE_API_URL=https://flask-rag-api-191y.onrender.com`

---

## Common Pitfalls & Solutions

1. **Cold Starts on Render Free Tier**:
   - *Problem*: Render spins down free tier instances after 15 minutes of inactivity. First
     request takes 30-50 seconds to respond.
   - *Fix*: Show a friendly loading indicator in React and implement retry logic.

2. **Mixed Content Error (HTTP vs HTTPS)**:
   - *Problem*: Vercel app served over HTTPS tries to fetch from `http://render-api.com`.
   - *Fix*: Always use HTTPS URLs for production Render backends.

3. **Missing Preflight Handler**:
   - *Problem*: Flask returns 405 Method Not Allowed for `OPTIONS` requests.
   - *Fix*: Explicitly intercept `OPTIONS` in Flask `@app.before_request`.

---

# Interview Questions & Answers (5 YOE IT Professional)

## 1. Conceptual / Theoretical

### Question:
Explain how browser Same-Origin Policy (SOP) and Cross-Origin Resource Sharing (CORS) interact
when a React SPA on Vercel attempts a `POST` request with a JSON payload to a Flask API on
Render. Why is a preflight request sent, and what specific headers determine success?

### Answer:
Browser SOP dictates that scripts running in a browser origin (`https://my-app.vercel.app`) cannot
read responses from a different origin (`https://flask-api.onrender.com`) unless the remote server
explicitly grants permission via CORS headers.

When the React app makes a `POST` request with `Content-Type: application/json`, the request fails
the criteria for a "Simple Request". The browser automatically halts the primary payload and issues
an HTTP `OPTIONS` preflight request containing:
- `Origin: https://my-app.vercel.app`
- `Access-Control-Request-Method: POST`
- `Access-Control-Request-Headers: content-type`

The Flask API on Render must respond to this `OPTIONS` preflight with an HTTP 200/204 status and
the following headers:
- `Access-Control-Allow-Origin: https://my-app.vercel.app` (or `*`)
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

Only after receiving a valid preflight response will the browser transmit the actual `POST` JSON.

### Follow-up Questions:
- What happens if the server returns `Access-Control-Allow-Origin: *` when the request includes
  `credentials: "include"` (cookies/session headers)?
  *(Answer: The browser rejects the response for security reasons. When credentials are included,
  `Access-Control-Allow-Origin` MUST be an explicit origin matching `Origin`, not a wildcard `*`).*

---

## 2. Practical / Scenario-Based

### Question:
You deploy a Vite React app to Vercel and a Flask API to Render. In development (`localhost`),
everything works. In production, fetching `/ask` throws:
`Access to fetch at 'https://api.onrender.com/ask' from origin 'https://app.vercel.app' has been
blocked by CORS policy: Response to preflight request doesn't pass access control check: It does
not have HTTP ok status.`
How do you diagnose and resolve this issue?

### Answer:

**Diagnosis**:
1. Open Browser DevTools Network tab and inspect the failing `OPTIONS /ask` request.
2. Check the response status code. Status 405 Method Not Allowed or 500 Internal Server Error
   indicates the backend Flask app is not handling HTTP `OPTIONS` requests on that route.
3. Check response headers. If `Access-Control-Allow-Origin` is absent, CORS headers are missing.

**Resolution**:
1. In Flask, ensure an `@app.before_request` hook intercepts `request.method == "OPTIONS"` and
   returns an HTTP 200 response with required CORS headers immediately.
2. Alternatively, use `flask-cors` (`CORS(app, resources={r"/*": {"origins": "*"}})`).
3. Alternatively, configure Vercel reverse proxy rewrites in `vercel.json` to proxy `/api/*` to
   Render, eliminating cross-origin browser requests altogether.

### Follow-up Questions:
- Why might CORS errors appear in browser console even when the error is actually a 500 Python
  exception in Flask?
  *(Answer: If Flask crashes during request processing without running `@app.after_request` or custom
  error handlers, the error response lacks CORS headers, causing the browser to report a CORS error
  instead of the underlying 500).*

---

## 3. Coding / Implementation

### Question:
Write a clean, production-ready custom React hook `useFlaskApi` that sends queries to a Flask
RAG API, handles dynamic base URL selection (`VITE_API_URL`), manages loading/error states, and
gracefully handles preflight/CORS network failures.

### Answer:

```javascript
import { useState, useCallback } from "react";

const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  "https://flask-rag-api-prod.onrender.com"
).replace(/\/$/, "");

export const useFlaskApi = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const askQuestion = useCallback(async (question) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        const errPayload = await response.json().catch(() => ({}));
        throw new Error(
          errPayload.error || `Server responded with status ${response.status}`
        );
      }

      const result = await response.json();
      setData(result);
      return result;
    } catch (err) {
      const isCorsOrNetwork =
        err.name === "TypeError" && err.message === "Failed to fetch";
      const message = isCorsOrNetwork
        ? "CORS or Network failure connecting to Flask API."
        : err.message;
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { askQuestion, data, isLoading, error };
};
```

---

## 4. System Design / Architecture

### Question:
Design a secure, enterprise-grade architecture for connecting a Vercel-hosted React frontend to a
multi-region backend microservices ecosystem (including Flask APIs on Render). Address CORS security,
API gateway routing, rate limiting, and zero-trust authentication.

### Answer:

### Architecture Blueprint

```text
+-----------------------------------------------------------------------------------+
|                           REACT SPA (VERCEL EDGE CDN)                             |
|                           https://app.enterprise.com                              |
+-----------------------------------------------------------------------------------+
                                         |
                       HTTPS API Requests (JWT Auth Header)
                                         v
+-----------------------------------------------------------------------------------+
|                        CLOUD API GATEWAY / REVERSE PROXY                          |
|                        - Enforces Strict CORS Origin White-list                    |
|                        - Global Rate Limiting & Web Application Firewall (WAF)    |
|                        - Centralized JWT Validation & Token Introspection          |
+-----------------------------------------------------------------------------------+
                                   /           \
               Routed via Private VPC          Routed via Cloudflare Tunnel
                                 /               \
                                v                 v
        +-------------------------------+  +-------------------------------+
        | Flask RAG API (Render)        |  | Go Search Microservice        |
        | - Internal Microservice       |  | - High-throughput Service     |
        +-------------------------------+  +-------------------------------+
```

### Architectural Key Pillars:
1. **API Gateway Layer**: Introduce an API Gateway (e.g., Cloudflare Workers, AWS API Gateway, or
   Kong) between Vercel and Render.
2. **CORS Governance**: Handle CORS centrally at the Gateway level using strict domain whitelist
   validation instead of configuring wildcard CORS inside individual Flask apps.
3. **Zero-Trust Auth**: Enforce JWT Bearer Tokens. The React frontend obtains tokens from OAuth2/OIDC
   providers (e.g., Auth0/Clerk). The Gateway validates tokens before forwarding requests to Flask.
4. **Preflight Cache Optimization**: Set `Access-Control-Max-Age: 86400` at the Gateway to allow
   browsers to cache CORS preflights for 24 hours, reducing latency and infrastructure costs.
