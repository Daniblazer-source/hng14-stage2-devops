from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import uuid
import os

app = FastAPI()

# CORS (allow frontend to communicate with API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables (Docker-friendly)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis client
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Create a job
@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())

        # Push job to queue
        r.lpush("job", job_id)

        # Store job status
        r.hset(f"job:{job_id}", "status", "queued")

        return {"job_id": job_id}

    except Exception as e:
        print(f"Redis Error (create_job): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get job status
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")

        if not status:
            raise HTTPException(status_code=404, detail="Job not found")

        return {
            "job_id": job_id,
            "status": status
        }

    except HTTPException:
        # Re-raise known HTTP errors
        raise
    except Exception as e:
        print(f"Redis Error (get_job): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
