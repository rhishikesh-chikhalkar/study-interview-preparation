---
name: nodejs-express-standards
description: Use when writing, reviewing, or debugging Node.js and Express backend services. Covers middleware, request handling, streaming, error management, and production anti-patterns.
---

# Node.js & Express Production Standards

Production-grade Node.js/Express standards for backend services.

---

## 1. Middleware & Request Handling

- **Security Headers**: Always validate internal secrets and auth headers in a dedicated middleware or early in the controller.
- **Input Sanitization**: Trim and validate all query parameters and body fields before use.
- **Graceful Failures**: Return appropriate HTTP status codes (400 for bad input, 401/403 for auth, 404 for missing resources, 502 for upstream failures).

---

## 2. Streaming & Large Data

- **Memory Safety**: Use `stream.pipe()` or event-based data handling for large files (e.g., video streaming) to avoid buffering issues.
- **Lifecycle Management**: Always listen for the `close` event on the request object to destroy upstream streams and prevent memory leaks.
- **Range Support**: Implement `Accept-Ranges: bytes` and handle `206 Partial Content` correctly for media streaming.

---

## 3. Error Management & Logging

- **Structured Error Responses**: Always return JSON errors in the format `{ error: "Message" }`.
- **Upstream Resilience**: Handle timeouts and "error" events from external libraries by evicting sessions and returning 502/504.
- **Manual Eviction**: Provide logic to clear cached sessions/tokens when an upstream error suggests authentication failure.

---

## 4. Strict Discipline & Anti-Patterns (FAANG-Level)

- **Stop Using `any`**: TypeScript safety is mandatory. No untyped code allowed.
- **No Inline Logic**: Extract complex logic into variables or utility functions.
- **No Monoliths**: Break large modules into smaller, focused files immediately.
- **No Hardcoding**: Use constants or environment variables for all magic values and URLs.
