import pytest
from fastapi.testclient import TestClient
from main import app, r
import fakeredis

# Create a mock Redis client
mock_redis = fakeredis.FakeRedis()

# Override the real redis client in the app with our mock
@pytest.fixture(autouse=True)
def setup_redis(monkeypatch):
    monkeypatch.setattr("main.r", mock_redis)

client = TestClient(app)

def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_get_job_not_found():
    response = client.get("/jobs/non-existent-id")
    assert response.status_code == 200 # App returns 200 with error msg
    assert response.json() == {"error": "not found"}

def test_get_job_status():
    # Pre-populate mock redis
    job_id = "test-123"
    mock_redis.hset(f"job:{job_id}", "status", "completed")
    
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
