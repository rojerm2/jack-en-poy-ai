# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 4.2 — ML prediction module. Next: 5.1 — Python prediction service.

## Current implementation
- Existing React game, Spring Boot API and CSV collection.
- Session-aware windows, chronological decision-tree training, atomic artifact serialization.
- Validated model loading, last-three-move prediction, class probabilities and model metadata.
- Root documentation and ignored local runtime files.

## Validation
13 Python tests pass; prediction CLI verified against the locally trained legacy model. Backend baseline: 10 tests pass. Frontend build/lint pass.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
