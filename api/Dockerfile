# STAGE 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# STAGE 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local
COPY . .

# Set ownership to the non-root user
RUN chown -R appuser:appuser /app

# Install curl for healthchecks. 
# We use 'ignore=DL3008' because Debian Trixie versions change rapidly, 
# making hard-coded version pinning (e.g., curl=7.x) break the build.
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Switch to the non-root user
USER appuser

EXPOSE 8000

# Docker Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/jobs || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
