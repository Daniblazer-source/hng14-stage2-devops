import pytest
from fastapi.testclient import TestClient
from main import app
import fakeredis

# Initialize TestClient
client = TestClient(app)

# Mock Redis using fakeredis
@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_r = fakeredis.FakeRedis(decode_responses=True)
    # Patch the redis client in main.py
    monkeypatch.setattr("main.r", fake_r)

def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_get_job_not_found():
    response = client.get("/jobs/non-existent-id")
    # UPDATED: Now expects 404 to match the new HTTPException logic
    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

def test_get_job_status():
    # First, create a job manually in the mocked redis
    import main
    job_id = "test-uuid"
    main.r.hset(f"job:{job_id}", "status", "completed")
    
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json() == {"job_id": job_id, "status": "completed"}
