import pandas as pd
import pytest
from analytics import summarize


def test_counts_predictions_and_strategy_rates_separately(tmp_path):
    path = tmp_path / "history.csv"
    pd.DataFrame([
        {"playerMove": "ROCK", "computerMove": "PAPER", "result": "COMPUTER_WIN", "strategy": "RANDOM", "fallbackReason": "insufficient_history"},
        {"playerMove": "ROCK", "computerMove": "PAPER", "result": "COMPUTER_WIN", "strategy": "ML", "predictedMove": "ROCK", "confidence": .8, "modelName": "tree", "modelVersion": "v1"},
        {"playerMove": "SCISSORS", "computerMove": "PAPER", "result": "PLAYER_WIN", "strategy": "ML", "predictedMove": "ROCK", "confidence": .6, "modelName": "tree", "modelVersion": "v1"},
    ]).to_csv(path, index=False)
    report = summarize(path)
    assert report["mlPredictions"] == 2
    assert report["predictionAccuracy"] == .5
    assert report["strategies"]["RANDOM"]["computerWinRate"] == 1
    assert report["strategies"]["ML"]["computerWinRate"] == .5
    assert report["fallbackReasons"]["insufficient_history"] == 1
    assert report["models"][0]["averageConfidence"] == pytest.approx(.7)


def test_legacy_and_empty_history_have_no_prediction_accuracy(tmp_path):
    path = tmp_path / "legacy.csv"
    pd.DataFrame([{"playerMove": "ROCK", "computerMove": "PAPER", "result": "COMPUTER_WIN"}]).to_csv(path, index=False)
    assert summarize(path)["predictionAccuracy"] is None
    pd.DataFrame(columns=["playerMove", "computerMove", "result"]).to_csv(path, index=False)
    assert summarize(path)["totalRounds"] == 0


def test_rejects_invalid_ml_metadata(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame([{"playerMove": "ROCK", "computerMove": "PAPER", "result": "COMPUTER_WIN", "strategy": "ML", "predictedMove": "BAD"}]).to_csv(path, index=False)
    with pytest.raises(ValueError, match="metadata"):
        summarize(path)
