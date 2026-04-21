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

# FIX: Use environment variables with fallbacks to the Docker service name
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Added decode_responses=True so Redis returns strings instead of bytes
r = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    decode_responses=True
)

@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        # Push to the 'job' list for the worker to pick up
        r.lpush("job", job_id)
        # Set the initial status in a hash
        r.hset(f"job:{job_id}", "status", "queued")
        return {"job_id": job_id}
    except Exception as e:
        # If Redis is down, this helps debug in the container logs
        print(f"Redis Error: {e}")
        return {"error": "Internal Server Error"}, 500

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
        if not status:
            return {"error": "not found"}
        # No .decode() needed because of decode_responses=True
        return {"job_id": job_id, "status": status}
    except Exception as e:
        print(f"Redis Error: {e}")
        return {"error": "Internal Server Error"}, 500
