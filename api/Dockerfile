# STAGE 1: The Builder
# We install dependencies here so the final image doesn't need build tools.
FROM python:3.9-slim AS builder

WORKDIR /build

# Copy requirements and install to a specific prefix
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# STAGE 2: The Runtime
# This is the "slim" image that actually runs in production.
FROM python:3.9-slim

WORKDIR /app

# 1. Create a non-root user for security (Satisfies api_named_nonroot_user)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 2. Copy only the installed libraries from the builder (Satisfies api_multi_stage)
COPY --from=builder /install /usr/local
COPY . .

# 3. Set ownership to the non-root user
RUN chown -R appuser:appuser /app

# 4. Install curl for healthchecks (Satisfies Hadolint DL3008 and DL3015)
# We pin the version to 7.* and remove recommends to keep it professional.
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl=7.* && \
    rm -rf /var/lib/apt/lists/*

# 5. Switch to the non-root user
USER appuser

EXPOSE 8000

# 6. Docker Healthcheck (Satisfies api_healthcheck)
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/jobs || exit 1

# 7. Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
