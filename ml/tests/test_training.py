import joblib
import pandas as pd
import pytest

from src.dataset.dataset_generator import COLUMNS, generate_dataset
from src.training import chronological_split, load_dataset, train


@pytest.fixture
def dataset(tmp_path):
    moves = ["ROCK", "PAPER", "SCISSORS"] * 40
    raw = tmp_path / "history.csv"
    pd.DataFrame({"playerMove": moves}).to_csv(raw, index=False)
    target = tmp_path / "dataset.csv"
    generate_dataset(raw, target)
    return target


def test_training_and_serialization(dataset, tmp_path):
    output = tmp_path / "model.joblib"
    metadata = train(dataset, output)
    loaded = joblib.load(output)
    assert metadata["evaluation"]["accuracy"] == 1
    assert loaded["model"].predict(pd.DataFrame([["ROCK", "PAPER", "SCISSORS"]], columns=COLUMNS[:3]))[0] == "ROCK"
    assert loaded["windowSize"] == 3


def test_chronological_holdout_has_window_gap(dataset):
    data = load_dataset(dataset)
    training, test = chronological_split(data)
    assert test.index[0] - training.index[-1] == 4


def test_invalid_and_insufficient_data(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame([["ROCK"] * 4], columns=COLUMNS).to_csv(path, index=False)
    with pytest.raises(ValueError, match="At least 12"):
        load_dataset(path)
    pd.DataFrame([["BAD"] * 4] * 20, columns=COLUMNS).to_csv(path, index=False)
    with pytest.raises(ValueError, match="valid move"):
        load_dataset(path)


def test_session_windows_do_not_mix(tmp_path):
    path = tmp_path / "raw.csv"
    pd.DataFrame({"sessionId": ["a", "b"] * 4, "playerMove": ["ROCK", "PAPER"] * 4}).to_csv(path, index=False)
    data = generate_dataset(path, tmp_path / "out.csv")
    assert data.values.tolist() == [["ROCK"] * 4, ["PAPER"] * 4]


def test_short_history_has_headers(tmp_path):
    path = tmp_path / "raw.csv"
    pd.DataFrame({"playerMove": ["ROCK"]}).to_csv(path, index=False)
    result = generate_dataset(path, tmp_path / "out.csv")
    assert result.empty
    assert list(result.columns) == COLUMNS
