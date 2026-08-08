FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy package specs
COPY pyproject.toml .
COPY README.md .
COPY src/ src/

# Build wheel package
RUN uv build --wheel -o /app/dist

FROM python:3.12-slim-bookworm AS runner

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

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

CMD gunicorn --bind 0.0.0.0:${PORT:-5001} wsgi:app

