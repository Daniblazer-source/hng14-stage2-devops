from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import uuid
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush("job", job_id)
        r.hset(f"job:{job_id}", "status", "queued")
        return {"job_id": job_id}
    except Exception as e:
        print(f"Redis Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
        if not status:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job_id": job_id, "status": status}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Status Fetch Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
