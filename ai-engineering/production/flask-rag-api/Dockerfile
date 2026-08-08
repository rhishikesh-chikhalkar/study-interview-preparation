# Multi-stage Production Dockerfile for Flask RAG API
FROM python:3.10-slim AS builder

WORKDIR /app

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy package specs
COPY pyproject.toml .
COPY README.md .
COPY src/ src/

# Build wheel package
RUN uv build --wheel -o /app/dist

# Final production runtime stage
FROM python:3.10-slim AS runner

WORKDIR /app

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5001 \
    FLASK_ENV=production

# Install built wheel
COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl

# Copy application startup code
COPY wsgi.py Procfile ./

# Non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]
