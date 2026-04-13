from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_predictions():
    response = client.get("/predictions/")
    assert response.status_code == 200
    assert "predictions" in response.json()
