# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 4.1 — First ML model. Next: 4.2 — ML prediction module.

## Current implementation
- React game and Spring Boot API with CSV recording.
- Session-aware dataset generation and serialized decision tree/one-hot encoder.
- Chronological 114-sample training set, 26-sample holdout, three-window gap.
- Root documentation is now tracked; Python caches and environments are ignored.

## Validation
5 Python tests and 10 Maven tests passed; frontend baseline build/lint passed. Legacy holdout accuracy: 42.31%, a small single-player sample.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
