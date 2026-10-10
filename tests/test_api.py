from fastapi.testclient import TestClient

from app.main import app
from app.services.model_service import model_service

client = TestClient(app)


def test_models_endpoint_lists_dense():
    if not model_service._loaded:
        model_service.load()

    response = client.get("/api/models")

    assert response.status_code == 200
    assert "dense" in response.json()["models"]