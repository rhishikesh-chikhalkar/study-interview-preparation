# Connecting Go Microservice to Flask Backend & React Frontend (3-Service Architecture)

Comprehensive study notes and 5 YOE interview Q&As on designing, deploying, and connecting a live 3-service distributed microservice architecture (**React SPA → Flask BFF API → Go Microservice**), covering inter-service HTTP client pooling, Backend-For-Frontend (BFF) patterns, CORS boundaries, timeout propagation, and enterprise observability.

---

## 1. Structured Notes

### 3-Tier Distributed Architecture Overview

In a modern polyglot microservice ecosystem, specialized frameworks are selected based on business and compute requirements:

```text
+-----------------------------------------------------------------------------------+
| FRONTEND TIER (Vercel Edge CDN / Local Vite Dev)                                  |
| React SPA                                                                         |
| - Single Page Application rendering UI & telemetry dashboards                     |
| - Issues HTTPS API requests to Flask Backend Gateway                              |
+-----------------------------------------------------------------------------------+
                                         |
                                         | HTTP/HTTPS (JSON payload, CORS managed)
                                         v
+-----------------------------------------------------------------------------------+
| BACKEND-FOR-FRONTEND TIER (Render PaaS / Local Gunicorn)                         |
| Python Flask API Gateway                                                          |
| - Authenticates client requests & manages CORS preflight                          |
| - Executes application workflow logic & RAG vector search                         |
| - Proxies/Delegates high-concurrency computation to Go Microservice              |
+-----------------------------------------------------------------------------------+
                                         |
                                         | HTTP/HTTPS (Server-to-Server, Internal/Auth Header)
                                         v
+-----------------------------------------------------------------------------------+
| MICROSERVICE COMPUTATION TIER (Render PaaS / Local Go HTTP)                        |
| Go Microservice                                                                   |
| - Compiled, low-latency, multi-threaded Go service                                |
| - High-performance text analytics, word/character counting & task execution      |
| - Structured JSON logging & graceful OS signal shutdown                           |
+-----------------------------------------------------------------------------------+
```

- **Frontend Tier (React)**: `https://study-interview-preparation.vercel.app`
- **Backend Gateway Tier (Flask)**: `https://flask-rag-api-191y.onrender.com`
- **Computation Tier (Go)**: `https://render-go-service-txtm.onrender.com`

---

### Key Architectural Concepts

#### 1. Backend-For-Frontend (BFF) Pattern
Rather than exposing downstream microservices directly to client browsers, the Flask API acts as a BFF gateway:
- **Encapsulation**: Downstream microservice APIs (Go) remain unexposed to public clients.
- **Payload Orchestration**: Flask can aggregate responses from multiple microservices into a single response for React.
- **Protocol & Auth Translation**: Converts public user tokens (e.g. JWT) into internal service-to-service headers (`X-API-Key`).

#### 2. CORS vs Server-to-Server Communication
- **Browser CORS Boundary**: Enforced between Browser (`React`) and Gateway (`Flask`). The browser sends `OPTIONS` preflight requests, requiring Flask to send `Access-Control-Allow-Origin` headers.
- **Server-to-Server Boundary**: Communicated directly between Python (`Flask`) and Go (`Go Microservice`). Browser SOP does NOT apply to server-to-server calls. No `OPTIONS` preflight is needed.

#### 3. Inter-Service HTTP Client Best Practices (`httpx` / `net/http`)
- **Connection Reuse**: Use persistent HTTP client sessions (`httpx.Client()` or `http.Client` in Go) with connection pooling rather than instantiating new sockets per request.
- **Strict Timeouts**: Always set explicit connect and read timeouts (`timeout=5.0`) to avoid downstream thread starvation if Go microservices stall.
- **Context Cancellation**: Pass request contexts down to interrupt downstream calls when upstream clients disconnect.

---

### Python Flask Gateway Implementation (`go_proxy.py`)

```python
import os
from typing import Any
from flask import Blueprint, jsonify, request
import httpx

go_proxy_bp = Blueprint("go_proxy", __name__)
GO_SERVICE_URL = os.getenv("GO_SERVICE_URL", "https://render-go-service-txtm.onrender.com").rstrip("/")
GO_API_KEY = os.getenv("GO_API_KEY", "")

def get_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if GO_API_KEY:
        headers["X-API-Key"] = GO_API_KEY
    return headers

@go_proxy_bp.route("/go-analyze", methods=["POST"])
def go_analyze() -> tuple[Any, int]:
    """Delegate heavy text processing to downstream Go microservice."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    target_url = f"{GO_SERVICE_URL}/api/v1/analyze"

    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(target_url, json={"text": text}, headers=get_headers())
        if resp.status_code == 200:
            result = resp.json()
            result["gateway"] = "Flask RAG Backend API"
            return jsonify(result), 200
        return jsonify({"error": f"Go service error: {resp.text}"}), resp.status_code
    except Exception as err:
        return jsonify({"error": f"Failed to connect to Go service: {err!s}"}), 502
```

---

### Go Microservice High-Performance Handler (`analyze.go`)

```go
package handler

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"
)

type AnalyzeRequest struct {
	Text string `json:"text"`
}

type AnalyzeResponse struct {
	Status         string    `json:"status"`
	WordCount      int       `json:"word_count"`
	CharacterCount int       `json:"character_count"`
	LineCount      int       `json:"line_count"`
	ByteSize       int       `json:"byte_size"`
	Service        string    `json:"service"`
	ProcessedAt    time.Time `json:"processed_at"`
}

type AnalyzeHandler struct{}

func NewAnalyzeHandler() *AnalyzeHandler {
	return &AnalyzeHandler{}
}

func (h *AnalyzeHandler) HandleAnalyze(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		_ = json.NewEncoder(w).Encode(map[string]string{"error": "method not allowed"})
		return
	}

	var req AnalyzeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		_ = json.NewEncoder(w).Encode(map[string]string{"error": "invalid JSON body"})
		return
	}

	text := req.Text
	words := strings.Fields(text)
	resp := AnalyzeResponse{
		Status:         "success",
		WordCount:      len(words),
		CharacterCount: len([]rune(text)),
		LineCount:      strings.Count(text, "\n") + 1,
		ByteSize:       len(text),
		Service:        "Go High-Performance Microservice",
		ProcessedAt:    time.Now().UTC(),
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}
```

---

## 2. Interview Questions & Answers (5 YOE IT Professional)

### 1. Conceptual / Theoretical

#### Question:
In a 3-tier microservice system (React SPA → Flask BFF → Go Microservice), explain why browser CORS restrictions apply to requests from React to Flask, but do NOT apply to HTTP calls made from Flask to Go. How does this impact security and architecture?

#### Answer:
Browser Cross-Origin Resource Sharing (CORS) is a browser security mechanism enforced strictly inside web browser engines (Chrome, Firefox, Safari) based on the Same-Origin Policy (SOP). When JavaScript code running inside a browser at `origin A` (`https://study-interview-preparation.vercel.app`) issues an HTTP request to `origin B` (`https://flask-rag-api-191y.onrender.com`), the browser inspects headers and enforces preflight `OPTIONS` checks.

When the Flask backend processes that request and subsequently executes an HTTP `POST` call to the Go microservice (`https://render-go-service-txtm.onrender.com`), the request is executed by Python's socket interface (`httpx` / `requests`) outside of any browser engine environment. Operating systems and backend runtimes do not enforce browser SOP.

**Architectural Impact**:
1. **Simplified Security Surface**: The Go microservice does not need to expose public CORS headers or allow random origins. It can be isolated inside a private cloud network (VPC / internal Render network) or secured using mutual TLS (mTLS) or secret API key headers (`X-API-Key`).
2. **Reduced Latency**: Inter-service server-to-server calls skip browser preflight `OPTIONS` round-trips entirely.

#### Follow-up Questions:
- How would you secure the Go microservice if it is deployed on a public PaaS like Render?
  *(Answer: Enforce internal secret header validation (`X-API-Key`), require IP whitelisting / private VPC networking, or enforce mTLS between Flask and Go).*

---

### 2. Practical / Scenario-Based

#### Question:
During a spike in traffic, the Go microservice experiences memory pressure and high latency (taking 15 seconds to respond). This causes Flask worker threads (Gunicorn) to hang and exhaust their worker pool, bringing down the entire React application. How do you redesign the Flask → Go communication to prevent cascading failures?

#### Answer:
This scenario represents a classic **cascading failure** caused by unbounded wait times and thread pool exhaustion in the API gateway.

To resolve this, implement the following resilience patterns:

1. **Strict Inter-Service Timeouts**:
   Set aggressive connect and read timeouts on the Flask `httpx.Client(timeout=3.0)`. If Go does not respond within 3 seconds, Flask aborts the HTTP request immediately and returns an HTTP 504 Gateway Timeout or degraded fallback payload to React.

2. **Circuit Breaker Pattern**:
   Integrate a circuit breaker (e.g. `pybreaker` or `tenacity` in Python). If 5 consecutive calls to Go fail or timeout, the breaker trips to `OPEN` state for 30 seconds. Subsequent requests immediately fail fast or return cached/mock responses without calling Go, protecting Flask's Gunicorn worker threads.

3. **Asynchronous Task Queue / Worker Pools**:
   For long-running tasks, convert synchronous REST calls to an asynchronous task pattern (Flask pushes task to Redis / Celery / RabbitMQ, Go worker processes asynchronously, React polls or listens via WebSockets/SSE).

#### Follow-up Questions:
- How would you verify that Gunicorn workers aren't blocked by slow downstream requests?
  *(Answer: Monitor Gunicorn active worker metrics, inspect APM traces via OpenTelemetry, and use asynchronous WSGI servers like `uvicorn` / `gevent` or async Flask).*

---

### 3. Coding / Implementation

#### Question:
Write a resilient Python helper function using `httpx` in Flask that sends a request to the Go microservice with exponential backoff retries for transient errors (502/503), but fails fast on 4xx client errors or timeouts.

#### Answer:

```python
import time
from typing import Any
import httpx


def call_go_microservice_with_retry(
    url: str,
    payload: dict[str, Any],
    api_key: str,
    max_retries: int = 3,
    base_backoff_sec: float = 0.5,
) -> dict[str, Any]:
    """Execute inter-service HTTP POST with exponential backoff retries for 5xx errors."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    last_exception: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            with httpx.Client(timeout=3.0) as client:
                response = client.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                return response.json()

            # Fail fast on client errors (400, 401, 403, 404)
            if 400 <= response.status_code < 500:
                raise RuntimeError(
                    f"Client error from Go service ({response.status_code}): {response.text}"
                )

            # Server error (502, 503, 504) -> log retry
            last_exception = RuntimeError(
                f"Go service error ({response.status_code}): {response.text}"
            )

        except (httpx.TimeoutException, httpx.NetworkError) as err:
            last_exception = err

        if attempt < max_retries:
            sleep_time = base_backoff_sec * (2 ** (attempt - 1))
            time.sleep(sleep_time)

    raise RuntimeError(
        f"Go service call failed after {max_retries} attempts: {last_exception!s}"
    )
```

---

### 4. System Design / Architecture

#### Question:
Design a zero-trust, high-availability architecture for a enterprise system connecting a global React SPA, Python API Gateway, and Go Microservices processing millions of daily events. Address service discovery, telemetry, rate limiting, and failure domain isolation.

#### Answer:

```text
+-----------------------------------------------------------------------------------+
| REACT SPA (Cloudflare CDN / Vercel Edge)                                          |
| Enforces TLS 1.3, CSP policies & JWT client authentication                       |
+-----------------------------------------------------------------------------------+
                                         |
                       HTTPS Requests (Cloudflare WAF Rate Limited)
                                         v
+-----------------------------------------------------------------------------------+
| KUBERNETES INGRESS / KONG API GATEWAY (BFF Layer)                                 |
| - Centralized CORS Termination & OAuth2/OIDC JWT Validation                       |
| - Distributed Rate Limiting via Redis Cluster                                     |
| - Distributed Tracing Header Injection (W3C Trace Context: traceparent)           |
+-----------------------------------------------------------------------------------+
                        /                                   \
      gRPC / HTTP (Internal VPC)                     gRPC / HTTP (Internal VPC)
                      v                                       v
+------------------------------------+      +------------------------------------+
| FLASK / FASTAPI WORKER POOL        |      | GO HIGH-THROUGHPUT MICROSERVICE    |
| - Application Orchestration        |      | - Auto-scaled HPA Pods             |
| - Vector Search / RAG Pipeline     |      | - Worker pools & goroutines        |
| - OpenTelemetry Metrics exporter   |      | - Circuit Breaker & Retry Policies |
+------------------------------------+      +------------------------------------+
```

#### Key Architecture Pillars:
1. **Service Mesh / Private VPC**: Go microservices run in a private Kubernetes cluster / VPC subnets without public ingress endpoints. Inter-service traffic routes over gRPC / HTTP2 with mutual TLS (mTLS) managed by Istio / Linkerd.
2. **Distributed Tracing (OpenTelemetry)**: The API Gateway injects W3C `traceparent` headers into incoming React requests. Flask and Go propagate these headers across HTTP/gRPC boundaries, enabling end-to-end trace visualization in Jaeger or Datadog.
3. **Service Discovery & Load Balancing**: Internal DNS or Consul service discovery dynamically routes Flask calls across auto-scaled Go pod replicas.
4. **Graceful Degradation**: If Go microservices experience outages, Flask returns cached non-critical data or enqueues operations in Kafka/RabbitMQ for asynchronous execution.
