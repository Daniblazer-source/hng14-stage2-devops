import redis
import time
import os
import signal
import sys

# Environment variables (Docker-friendly)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis client (consistent with API behavior)
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# -----------------------------
# Graceful shutdown handling
# -----------------------------
def handle_sigterm(*args):
    print("Worker shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)


# -----------------------------
# Ensure Redis is ready before processing
# -----------------------------
def wait_for_redis():
    while True:
        try:
            r.ping()
            print("Connected to Redis ✔")
            break
        except redis.exceptions.ConnectionError:
            print("Waiting for Redis...")
            time.sleep(2)


# -----------------------------
# Job processor
# -----------------------------
def process_job(job_id):
    try:
        print(f"Processing job {job_id}")

        # Simulate work
        time.sleep(2)

        # Update status in Redis
        r.hset(f"job:{job_id}", "status", "completed")

        print(f"Job completed: {job_id}")

    except Exception as e:
        print(f"Job failed {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")


# -----------------------------
# Main worker loop
# -----------------------------
def run_worker():
    wait_for_redis()

    while True:
        try:
            job = r.brpop("job", timeout=5)

            if job:
                _, job_id = job
                process_job(job_id)

        except redis.exceptions.ConnectionError:
            print("Redis connection lost. Retrying...")
            time.sleep(2)

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_worker()
