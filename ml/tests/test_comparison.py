import joblib
import pandas as pd
import pytest

from src.comparison import compare_models
from src.dataset.dataset_generator import FEATURES, generate_dataset
from src.prediction import Predictor
from retrain import retrain


@pytest.fixture
def data(tmp_path):
    raw = tmp_path / "history.csv"
    pd.DataFrame({"playerMove": ["ROCK", "PAPER", "SCISSORS"] * 60}).to_csv(raw, index=False)
    path = tmp_path / "dataset.csv"
    generate_dataset(raw, path)
    return raw, path


def test_comparison_reports_baselines_and_serializable_winner(data, tmp_path):
    _, path = data
    output = tmp_path / "chosen.joblib"
    report = compare_models(path, output)
    assert set(report["models"]) == {"majority_baseline", "history_frequency", "decision_tree", "random_forest", "logistic_regression", "knn", "naive_bayes"}
    assert report["models"]["majority_baseline"]["holdout"]["accuracy"] < .4
    assert report["models"]["decision_tree"]["holdout"]["accuracy"] == 1
    assert Predictor(output).predict(["ROCK", "PAPER", "SCISSORS"])["predictedMove"] == "ROCK"
    assert report["selectedModel"] == max(report["models"], key=lambda name: report["models"][name]["selectionAccuracy"])
    assert joblib.load(output)["selection"]["method"] == "chronological_3_fold_cv"


def test_selection_does_not_use_final_holdout_labels(data, tmp_path):
    _, path = data
    original = compare_models(path)
    altered = pd.read_csv(path)
    altered.loc[int(len(altered) * .8) + 3:, "nextMove"] = "PAPER"
    changed = tmp_path / "altered.csv"
    altered.to_csv(changed, index=False)
    second = compare_models(changed)
    assert original["selectedModel"] == second["selectedModel"]
    assert [entry["selectionAccuracy"] for entry in original["models"].values()] == [entry["selectionAccuracy"] for entry in second["models"].values()]


def test_comparison_requires_enough_data(data, tmp_path):
    _, path = data
    short = tmp_path / "short.csv"
    pd.read_csv(path).iloc[:50].to_csv(short, index=False)
    with pytest.raises(ValueError, match="64"):
        compare_models(short)


def test_comparison_retraining_promotes_selected_model(data, tmp_path):
    raw, _ = data
    output = tmp_path / "model.joblib"
    report = retrain(raw, output, tmp_path / "report.json", compare=True)
    assert Predictor(output).artifact["modelName"] == report["comparison"]["selectedModel"]
