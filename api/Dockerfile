# Stage 1: Build
FROM python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .

# Create a virtualenv and install dependencies there
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the entire virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Ensure permissions and set PATH to use the venv
RUN chown -R appuser:appuser /app
ENV PATH="/opt/venv/bin:$PATH"
USER appuser

EXPOSE 8000

# Using the socket check we discussed to avoid 'curl' issues
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import socket; s = socket.socket(); s.connect(('localhost', 8000))" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
