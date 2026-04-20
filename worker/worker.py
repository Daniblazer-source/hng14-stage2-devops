import redis
import time
import os
import signal

# FIX: Use environment variables for container networking
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")

# Professional touch: Basic signal handling for "graceful" shutdown
def handle_sigterm(*args):
    print("Worker shutting down gracefully...")
    exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

while True:
    try:
        job = r.brpop("job", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id.decode())
    except redis.exceptions.ConnectionError:
        print("Waiting for Redis...")
        time.sleep(2)
