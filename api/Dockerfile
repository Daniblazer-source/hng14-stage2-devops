# Stage 1: builder
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.9-slim
WORKDIR /app

# Create the named non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appuser /app

# Ensure the non-root user can find the installed packages
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import socket; s = socket.socket(); s.connect(('localhost', 8000))" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]