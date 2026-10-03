import shutil
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from retrain import model_lock, retrain, rollback
from service import create_app
from src.prediction import Predictor
from test_prediction import model_path


def history(tmp_path):
    path = tmp_path / "history.csv"
    pd.DataFrame({"playerMove": ["ROCK", "PAPER", "SCISSORS"] * 40}).to_csv(path, index=False)
    return path


def test_retrain_archive_and_rollback(tmp_path, model_path):
    raw = history(tmp_path)
    before = raw.read_bytes()
    old_version = Predictor(model_path).artifact["modelVersion"]
    report = tmp_path / "report.json"
    result = retrain(raw, model_path, report)
    assert raw.read_bytes() == before
    assert result["generatedSamples"] == 117
    assert report.exists()
    assert Predictor(model_path).artifact["modelVersion"] != old_version
    rollback(result["previousModelArchive"], model_path)
    assert Predictor(model_path).artifact["modelVersion"] == old_version


def test_failed_retrain_preserves_active_model(tmp_path, model_path):
    original = model_path.read_bytes()
    raw = tmp_path / "short.csv"
    pd.DataFrame({"playerMove": ["ROCK"] * 5}).to_csv(raw, index=False)
    with pytest.raises(ValueError):
        retrain(raw, model_path, tmp_path / "report.json")
    assert model_path.read_bytes() == original
    assert not model_path.with_suffix(".lock").exists()


def test_training_lock_rejects_competing_run(model_path):
    with model_lock(model_path):
        with pytest.raises(RuntimeError, match="lock"):
            with model_lock(model_path):
                pass


def test_service_reloads_and_retains_last_good_model(tmp_path, model_path):
    with TestClient(create_app(model_path)) as client:
        old = client.get("/health").json()["modelVersion"]
        new = retrain(history(tmp_path), model_path, tmp_path / "report.json")
        assert client.get("/health").json()["modelVersion"] == new["modelVersion"]
        assert new["modelVersion"] != old
        model_path.write_bytes(b"corrupt replacement")
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["reloadFailed"] is True
        assert health.json()["modelVersion"] == new["modelVersion"]
        assert client.post("/predict", json={"history": ["ROCK", "PAPER", "SCISSORS"]}).status_code == 200


def test_service_recovers_when_first_model_appears(tmp_path, model_path):
    absent = tmp_path / "new.joblib"
    with TestClient(create_app(absent)) as client:
        assert client.get("/health").status_code == 503
        shutil.copyfile(model_path, absent)
        assert client.get("/health").status_code == 200
