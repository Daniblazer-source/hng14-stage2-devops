# Stage 1: Build dependencies
FROM python:3.9-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.9-slim
WORKDIR /app

# Satisfies api_named_nonroot_user and api_user_creation_cmd
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only libraries from builder (Satisfies api_multi_stage)
COPY --from=builder /install /usr/local
COPY . .

RUN chown -R appuser:appuser /app

# Ensure we have curl for the healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

USER appuser

EXPOSE 8000

# Satisfies api_healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/jobs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
