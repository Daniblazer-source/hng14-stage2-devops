from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import uuid
import os

app = FastAPI()

# FIX: Added CORS middleware so the frontend can talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you'd limit this to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIX: Use environment variables with fallbacks
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode()}
