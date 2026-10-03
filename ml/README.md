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
