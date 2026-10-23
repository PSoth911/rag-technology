# =============================================================================
# RAG Technology Testing Lab — Technology 26: Docker Containerization
# =============================================================================

# Multi-stage build for optimal image size and security
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

# Install build essentials for C-extensions (psycopg2, tokenizers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Runtime Stage
FROM python:3.12-slim-bookworm AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PORT=8000

# Install runtime dependencies for OpenCV and healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1 \
    libglib2.0-0 \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root application user for container security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY --chown=appuser:appgroup . /app

USER appuser

EXPOSE 8000

# Health check to ensure FastAPI /health is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Launch Uvicorn ASGI server
CMD ["uvicorn", "02-backend.test_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
