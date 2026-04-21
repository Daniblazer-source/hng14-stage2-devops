FROM python:3.9-slim AS builder

WORKDIR /app
# Note: If worker doesn't have requirements.txt, you can manually install redis
# RUN pip install --user redis
COPY requirements.txt* . 
RUN if [ -f requirements.txt ]; then pip install --user --no-cache-dir -r requirements.txt; else pip install --user redis; fi

FROM python:3.9-slim

WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

# Worker healthcheck: Since there's no port, we check if the process is alive
HEALTHCHECK --interval=30s --timeout=3s \
  CMD pgrep -f "python worker.py" || exit 1

CMD ["python", "worker.py"]
