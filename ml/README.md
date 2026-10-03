# Move prediction

Use Python 3.12 or later. From `ml/`:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate; Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.dataset.main
python train.py
python -m pytest
```

The encoder and decision tree are serialized together in `models/player-move.joblib`.
The training report includes chronological holdout accuracy, confusion matrix, sample counts,
dependency version, and source SHA-256. The last 20% is reserved for evaluation, with a
three-window gap. Evaluation rows are never fitted. Only load locally created Joblib files.

The checked-in CSV is a small legacy example from one player. Its score is not evidence
of general prediction quality. Uniform random prediction has expected accuracy 1/3.
Synthetic sequences appear only in tests.

## Local prediction

`python predict.py ROCK PAPER SCISSORS` uses the last three completed moves, oldest first.
The result includes the predicted move, class probabilities, model name and version.
Confidence is an uncalibrated classifier probability, not a promised success rate.
Missing or incompatible artifacts require retraining.

## HTTP service

```sh
python -m uvicorn service:app --host 127.0.0.1 --port 8001
```

`GET /health` returns readiness and model metadata. `POST /predict` accepts only
`{"history":["ROCK","PAPER","SCISSORS"]}`. History has exactly three completed
moves, oldest first. Invalid requests return 422; missing or incompatible models
return 503. The current player move is forbidden in this contract.
`MODEL_PATH` overrides the model file. The service is local by default.

## Retraining and rollback

```sh
python retrain.py
# Or use the legacy sample explicitly:
python retrain.py --history data/raw/game-history.csv
python retrain.py --rollback models/archive/<previous-model>.joblib
```

The workflow freezes a raw history snapshot, generates session-aware windows, trains
and validates a candidate, archives the current model, and atomically replaces it.
It requires at least 16 windows and two training classes. Insufficient/invalid data
leaves the active model unchanged. Reports include source hashes, version, sample
counts, evaluation and rollback archive. A model lock prevents overlapping CLI runs.
After a crashed run, remove `models/player-move.lock` only after checking no training
process is active. Start the workflow manually after collecting more complete rounds.

The service checks the file timestamp/size on requests and reloads validated replacements.
Missing/corrupt replacements keep the last valid in-memory model and set `reloadFailed`
in readiness. If no model has ever loaded, inference returns 503 until one appears.
No HTTP training/upload endpoint is exposed.

## Model comparison

```sh
python compare.py
python retrain.py --history data/raw/game-history.csv --compare
```

Compare majority and last-three-move frequency baselines with Decision Tree, Random
Forest, Logistic Regression, KNN and Gaussian Naive Bayes. Three expanding chronological
folds with a three-window gap select the highest mean accuracy within the training 80%.
Ties prefer earlier, simpler candidates. Models that cannot fit a fold are reported as
unavailable. The final holdout is excluded from selection and reported afterward with
accuracy, confusion matrix and per-class metrics. Uniform random expected accuracy is 1/3.

Comparison requires at least 64 windows. `compare.py` writes a report and does not promote
a model. `retrain.py --compare` uses the same comparison to validate/archive/promote the
selected candidate through the retraining workflow. All scores are specific to the supplied
history; repeated comparison of a small reused holdout is not an independent experiment.
