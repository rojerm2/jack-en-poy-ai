import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import confusion_matrix

from retrain import atomic_json
from src.dataset.dataset_generator import MOVES
from src.training import ROOT


def summarize(history):
    data = pd.read_csv(history)
    required = {"playerMove", "computerMove", "result"}
    if not required.issubset(data.columns) or not data["playerMove"].isin(MOVES).all() or not data["computerMove"].isin(MOVES).all():
        raise ValueError("History requires valid player/computer moves and results")
    if not data["result"].isin(["PLAYER_WIN", "COMPUTER_WIN", "DRAW"]).all():
        raise ValueError("Invalid round result")
    if "strategy" not in data:
        data["strategy"] = "LEGACY"
    if not data["strategy"].isin(["ML", "RANDOM", "LEGACY"]).all():
        raise ValueError("Invalid strategy")
    ml = data[data["strategy"] == "ML"].copy()
    if len(ml) and (not {"predictedMove", "confidence", "modelName", "modelVersion"}.issubset(ml.columns) or not ml["predictedMove"].isin(MOVES).all()):
        raise ValueError("ML rounds require prediction metadata")
    if len(ml):
        ml["confidence"] = pd.to_numeric(ml["confidence"], errors="coerce")
        if not ml["confidence"].between(0, 1).all() or ml[["modelName", "modelVersion"]].isna().any().any():
            raise ValueError("Invalid prediction metadata")
    strategies = {}
    for name, group in data.groupby("strategy"):
        strategies[name] = {"rounds": len(group), "computerWinRate": float((group["result"] == "COMPUTER_WIN").mean())}
    by_model = []
    if len(ml):
        for (name, version), group in ml.groupby(["modelName", "modelVersion"]):
            by_model.append({"modelName": name, "modelVersion": version, "predictions": len(group), "predictionAccuracy": float((group["predictedMove"] == group["playerMove"]).mean()), "averageConfidence": float(group["confidence"].mean())})
    buckets = []
    if len(ml):
        for low, high in [(0, .5), (.5, .75), (.75, 1.01)]:
            group = ml[(ml["confidence"] >= low) & (ml["confidence"] < high)]
            buckets.append({"range": f"{low:.0%}–{min(high, 1):.0%}", "predictions": len(group), "observedAccuracy": float((group["predictedMove"] == group["playerMove"]).mean()) if len(group) else None})
    return {
        "totalRounds": len(data),
        "results": {name: int((data["result"] == name).sum()) for name in ["PLAYER_WIN", "COMPUTER_WIN", "DRAW"]},
        "moveCounts": {move: int((data["playerMove"] == move).sum()) for move in MOVES},
        "strategies": strategies,
        "mlPredictions": len(ml),
        "predictionAccuracy": float((ml["predictedMove"] == ml["playerMove"]).mean()) if len(ml) else None,
        "labels": list(MOVES),
        "predictionConfusionMatrix": confusion_matrix(ml["playerMove"], ml["predictedMove"], labels=MOVES).tolist() if len(ml) else [[0] * 3 for _ in MOVES],
        "models": by_model,
        "confidenceBuckets": buckets,
        "fallbackReasons": {str(name): int(count) for name, count in data.get("fallbackReason", pd.Series(dtype=str)).dropna().value_counts().items()},
        "interpretation": "Observed session rounds are not a controlled experiment. Classifier probabilities are not calibrated win probabilities.",
    }


def main():
    parser = argparse.ArgumentParser(description="Report observed gameplay and inference performance")
    parser.add_argument("--history", type=Path, default=ROOT / "data/raw/live-history.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/analytics.json")
    args = parser.parse_args()
    try:
        if args.history.resolve() == args.output.resolve():
            raise ValueError("Output must not overwrite history")
        report = summarize(args.history)
        atomic_json(report, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Analytics failed: {error}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
