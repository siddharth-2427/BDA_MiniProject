from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ONLINE"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data

def test_pipeline_status():
    response = client.get("/pipeline/status")
    assert response.status_code == 200
    data = response.json()
    assert "is_running" in data

def test_datasets_list():
    response = client.get("/datasets")
    assert response.status_code == 200
    assert "raw_datasets" in response.json()
