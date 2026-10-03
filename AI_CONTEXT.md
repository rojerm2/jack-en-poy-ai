# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 7.1 — Retraining workflow. Next: 7.2 — Model comparison.

## Current implementation
- Animated React game with keyboard/session controls and reveal gating.
- Backend-owned three-move history, ML counter strategy, random fallback and session CSV metadata.
- Frozen-history retraining, minimum-data validation, CLI lock, model archives and rollback.
- Automatic validated model reload; failed replacements retain the last good model.

## Validation
26 Python tests pass, including retrain/rollback/locking/reload and failed-promotion safety. Real retraining CLI verified on the 146-round legacy sample. Frontend: 8 tests/build/lint. Backend: 21 tests.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
