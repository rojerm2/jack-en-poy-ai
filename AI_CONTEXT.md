# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 7.2 — Model comparison. Next: 7.3 — AI performance analytics.

## Current implementation
- Full animated React game and backend-owned session inference with random fallback.
- Snapshot retraining, archiving, rollback and validated service reload.
- Majority/frequency baselines plus tree, forest, logistic regression, KNN and Naive Bayes comparison.
- Three expanding chronological training folds select the model before final holdout evaluation.
- Selected-model retraining uses the same validated promotion workflow.

## Validation
30 Python tests pass, including unchanged selection when final holdout labels change. Comparison and selected-model CLI promotion verified on legacy data: logistic regression selected, 42.31% on 26 holdout rows. Frontend: 8 tests/build/lint; backend: 21 tests.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
