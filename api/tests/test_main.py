import pytest
from fastapi.testclient import TestClient
import fakeredis
import os
import sys

# This allows the test to find main.py in the parent folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, r

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_r = fakeredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr("main.r", fake_r)

def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_get_job_not_found():
    response = client.get("/jobs/non-existent-id")
    assert response.status_code == 404

def test_get_job_status():
    import main
    job_id = "test-uuid"
    main.r.hset(f"job:{job_id}", "status", "completed")
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
