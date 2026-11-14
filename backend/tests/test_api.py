# tests/test_api.py

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_datasets():

    response = client.get("/datasets")

    assert response.status_code == 200