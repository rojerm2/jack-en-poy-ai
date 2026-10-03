from pathlib import Path

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from src.dataset.dataset_generator import FEATURES, MOVES, WINDOW_SIZE
from src.training import atomic_dump, chronological_split, evaluate, load_dataset, make_artifact, make_pipeline


class HistoryFrequencyClassifier(ClassifierMixin, BaseEstimator):
    def fit(self, X, y):
        self.classes_ = np.array(MOVES)
        self.n_features_in_ = X.shape[1]
        return self

    def predict_proba(self, X):
        # Each encoder block uses the same fixed ROCK/PAPER/SCISSORS order.
        return np.asarray(X).reshape(-1, WINDOW_SIZE, len(MOVES)).sum(axis=1) / WINDOW_SIZE

    def predict(self, X):
        return self.classes_[self.predict_proba(X).argmax(axis=1)]


def candidates():
    return {
        "majority_baseline": DummyClassifier(strategy="most_frequent"),
        "history_frequency": HistoryFrequencyClassifier(),
        "decision_tree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=2, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=100, max_depth=6, min_samples_leaf=2, random_state=42, n_jobs=1),
        "logistic_regression": LogisticRegression(max_iter=500, random_state=42),
        "knn": KNeighborsClassifier(n_neighbors=5),
        "naive_bayes": GaussianNB(),
    }


def compare_models(dataset, output=None):
    dataset = Path(dataset)
    data = load_dataset(dataset)
    if len(data) < 64:
        raise ValueError("Model comparison requires at least 64 windows")
    training, holdout = chronological_split(data)
    splits = list(TimeSeriesSplit(n_splits=3, gap=WINDOW_SIZE).split(training))
    results = {}
    pipelines = {}
    for name, classifier in candidates().items():
        model = make_pipeline(classifier)
        folds = []
        try:
            for train_indices, validation_indices in splits:
                fold_model = clone(model)
                fit = training.iloc[train_indices]
                validation = training.iloc[validation_indices]
                fold_model.fit(fit[FEATURES], fit["nextMove"])
                folds.append(float(accuracy_score(validation["nextMove"], fold_model.predict(validation[FEATURES]))))
            results[name] = {"selectionAccuracy": float(np.mean(folds)), "foldAccuracies": folds}
            pipelines[name] = model
        except ValueError as error:
            results[name] = {"unavailable": str(error)}

    eligible = [name for name in results if "selectionAccuracy" in results[name]]
    if not eligible:
        raise ValueError("No model could be evaluated on chronological folds")
    # Holdout scores are reported only after selection is fixed.
    selected = max(eligible, key=lambda name: results[name]["selectionAccuracy"])
    for name in eligible:
        model = pipelines[name]
        model.fit(training[FEATURES], training["nextMove"])
        results[name]["holdout"] = evaluate(model, holdout)
    artifact = make_artifact(pipelines[selected], selected, dataset, training, holdout)
    artifact["selection"] = {"method": "chronological_3_fold_cv", "gap": WINDOW_SIZE, "accuracy": results[selected]["selectionAccuracy"]}
    report = {
        "selectedModel": selected,
        "selectionMethod": "mean accuracy on three expanding chronological training folds; ties favor earlier/simple baselines",
        "windowGap": WINDOW_SIZE,
        "trainingSamples": len(training),
        "holdoutSamples": len(holdout),
        "datasetSha256": artifact["datasetSha256"],
        "sklearnVersion": artifact["sklearnVersion"],
        "randomExpectedAccuracy": 1 / 3,
        "models": results,
    }
    if output:
        atomic_dump(artifact, output)
    return report
