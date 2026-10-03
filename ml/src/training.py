from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile

import joblib
import pandas as pd
import sklearn
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from src.dataset.dataset_generator import COLUMNS, FEATURES, MOVES, WINDOW_SIZE

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/processed/training-data.csv"
DEFAULT_MODEL = ROOT / "models/player-move.joblib"


def load_dataset(path):
    data = pd.read_csv(path)
    if list(data.columns) != COLUMNS or not data.isin(MOVES).all().all():
        raise ValueError(f"Dataset requires valid move columns: {COLUMNS}")
    if len(data) < 12:
        raise ValueError("At least 12 training windows are required")
    return data


def chronological_split(data):
    cutoff = int(len(data) * 0.8)
    train, test = data.iloc[:cutoff], data.iloc[cutoff + WINDOW_SIZE:]
    if test.empty or train["nextMove"].nunique() < 2:
        raise ValueError("Need a nonempty holdout and at least two training classes")
    return train, test


def make_pipeline(classifier=None):
    return Pipeline([
        ("encoding", OneHotEncoder(categories=[list(MOVES)] * WINDOW_SIZE, sparse_output=False)),
        ("classifier", classifier if classifier is not None else DecisionTreeClassifier(max_depth=5, min_samples_leaf=2, random_state=42)),
    ])


def evaluate(model, test):
    actual = test["nextMove"]
    predicted = model.predict(test[FEATURES])
    return {
        "accuracy": float(accuracy_score(actual, predicted)),
        "randomBaselineAccuracy": 1 / 3,
        "samples": len(test),
        "labels": list(MOVES),
        "confusionMatrix": confusion_matrix(actual, predicted, labels=MOVES).tolist(),
        "classificationReport": classification_report(actual, predicted, labels=MOVES, output_dict=True, zero_division=0),
    }


def atomic_dump(artifact, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".joblib")
    os.close(fd)
    try:
        joblib.dump(artifact, temporary)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def train(dataset=DEFAULT_DATA, output=DEFAULT_MODEL):
    dataset, output = Path(dataset), Path(output)
    data = load_dataset(dataset)
    training, holdout = chronological_split(data)
    model = make_pipeline()
    model.fit(training[FEATURES], training["nextMove"])
    metrics = evaluate(model, holdout)
    created = datetime.now(timezone.utc).isoformat()
    artifact = {
        "schemaVersion": 1,
        "windowSize": WINDOW_SIZE,
        "moves": list(MOVES),
        "modelName": "decision_tree",
        "modelVersion": created,
        "sklearnVersion": sklearn.__version__,
        "datasetSha256": hashlib.sha256(dataset.read_bytes()).hexdigest(),
        "trainingSamples": len(training),
        "evaluation": metrics,
        "model": model,
    }
    atomic_dump(artifact, output)
    return {key: value for key, value in artifact.items() if key != "model"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Train and serialize the baseline decision tree")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_MODEL)
    args = parser.parse_args()
    print(json.dumps(train(args.dataset, args.output), indent=2))
