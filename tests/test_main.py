import pytest
from fastapi.testclient import TestClient
from api.main import app
import fakeredis


client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_r = fakeredis.FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr("api.main.r", fake_r)


def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_get_job_status():
    res = client.post("/jobs")
    job_id = res.json()["job_id"]
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"


def test_health_check():
    response = client.get("/jobs/invalid-id")
    assert response.status_code == 404
