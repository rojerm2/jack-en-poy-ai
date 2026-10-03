import joblib
import pandas as pd
import pytest

from src.dataset.dataset_generator import generate_dataset
from src.prediction import ModelUnavailable, Predictor
from src.training import train


@pytest.fixture
def model_path(tmp_path):
    raw = tmp_path / "history.csv"
    pd.DataFrame({"playerMove": ["ROCK", "PAPER", "SCISSORS"] * 40}).to_csv(raw, index=False)
    data = tmp_path / "data.csv"
    generate_dataset(raw, data)
    output = tmp_path / "model.joblib"
    train(data, output)
    return output


def test_prediction_uses_last_three_and_has_probabilities(model_path):
    predictor = Predictor(model_path)
    prediction = predictor.predict(["SCISSORS", "ROCK", "PAPER", "SCISSORS"])
    assert prediction["predictedMove"] == "ROCK"
    assert prediction["confidence"] == 1
    assert sum(prediction["probabilities"].values()) == 1
    assert prediction["historyLength"] == 3
    assert prediction == predictor.predict(["ROCK", "PAPER", "SCISSORS"])


@pytest.mark.parametrize("history", [[], ["ROCK"], ["ROCK", "PAPER", "BAD"], "ROCK", ["ROCK"] * 101])
def test_rejects_invalid_history(model_path, history):
    with pytest.raises(ValueError):
        Predictor(model_path).predict(history)


def test_missing_and_corrupt_models(tmp_path):
    path = tmp_path / "missing.joblib"
    with pytest.raises(ModelUnavailable):
        Predictor(path)
    path.write_bytes(b"bad model")
    with pytest.raises(ModelUnavailable):
        Predictor(path)


def test_rejects_incompatible_artifact(model_path):
    artifact = joblib.load(model_path)
    artifact["windowSize"] = 4
    joblib.dump(artifact, model_path)
    with pytest.raises(ModelUnavailable):
        Predictor(model_path)
