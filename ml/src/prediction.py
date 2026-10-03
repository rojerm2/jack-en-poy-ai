import math
from pathlib import Path

import joblib
import pandas as pd
import sklearn

from src.dataset.dataset_generator import FEATURES, MOVES, WINDOW_SIZE
from src.training import DEFAULT_MODEL


class ModelUnavailable(RuntimeError):
    pass


class Predictor:
    def __init__(self, path=DEFAULT_MODEL):
        self.path = Path(path)
        self.artifact = None
        self.load()

    def load(self):
        try:
            artifact = joblib.load(self.path)
            if not isinstance(artifact, dict):
                raise ValueError("Invalid model artifact")
            if artifact.get("schemaVersion") != 1 or artifact.get("windowSize") != WINDOW_SIZE or artifact.get("moves") != list(MOVES):
                raise ValueError("Incompatible model schema")
            if artifact.get("sklearnVersion") != sklearn.__version__:
                raise ValueError("Retrain with the installed scikit-learn version")
            if not artifact.get("modelVersion") or not artifact.get("modelName"):
                raise ValueError("Missing model metadata")
            model = artifact["model"]
            if not set(model.classes_).issubset(MOVES):
                raise ValueError("Invalid model classes")
            probe = pd.DataFrame([["ROCK"] * WINDOW_SIZE], columns=FEATURES)
            if model.predict(probe)[0] not in MOVES:
                raise ValueError("Invalid prediction output")
            model.predict_proba(probe)
            self.artifact = artifact
        except Exception as error:
            raise ModelUnavailable("Model is missing, corrupt, or incompatible; train it locally") from error

    def predict(self, history):
        if not isinstance(history, (list, tuple)) or not WINDOW_SIZE <= len(history) <= 100:
            raise ValueError("Provide between 3 and 100 completed moves")
        if any(move not in MOVES for move in history):
            raise ValueError("History contains an invalid move")
        features = pd.DataFrame([list(history[-WINDOW_SIZE:])], columns=FEATURES)
        artifact = self.artifact
        model = artifact["model"]
        move = str(model.predict(features)[0])
        probabilities = {name: 0.0 for name in MOVES}
        probabilities.update(zip(model.classes_, map(float, model.predict_proba(features)[0])))
        if any(not math.isfinite(p) or not 0 <= p <= 1 for p in probabilities.values()) or not math.isclose(sum(probabilities.values()), 1, abs_tol=1e-6):
            raise ModelUnavailable("Model returned invalid probabilities")
        return {
            "predictedMove": move,
            "confidence": probabilities[move],
            "probabilities": probabilities,
            "modelName": artifact["modelName"],
            "modelVersion": artifact["modelVersion"],
            "historyLength": WINDOW_SIZE,
        }
