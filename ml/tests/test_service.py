from fastapi.testclient import TestClient
import pytest

from service import create_app
from test_prediction import model_path


def test_health_and_predict(model_path):
    with TestClient(create_app(model_path)) as client:
        assert client.get("/health").json()["modelLoaded"] is True
        response = client.post("/predict", json={"history": ["ROCK", "PAPER", "SCISSORS"]})
        assert response.status_code == 200
        assert response.json()["predictedMove"] == "ROCK"
        assert response.json()["confidence"] == 1


@pytest.mark.parametrize("payload", [
    {}, {"history": []}, {"history": ["ROCK"] * 4},
    {"history": ["ROCK", "PAPER", "BAD"]},
    {"history": ["ROCK"] * 3, "playerMove": "SCISSORS"},
    {"history": "ROCK"},
])
def test_validation(model_path, payload):
    with TestClient(create_app(model_path)) as client:
        assert client.post("/predict", json=payload).status_code == 422


def test_unavailable_model_returns_503(tmp_path):
    with TestClient(create_app(tmp_path / "missing.joblib")) as client:
        assert client.get("/health").status_code == 503
        response = client.post("/predict", json={"history": ["ROCK"] * 3})
        assert response.status_code == 503
        assert "missing.joblib" not in response.text
