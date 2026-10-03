# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 5.1 — Python prediction service. Next: 5.2 — Spring Boot ML integration.

## Current implementation
- React game and Spring Boot CSV collection.
- Session-aware dataset pipeline, chronological training and validated prediction CLI.
- FastAPI POST /predict and GET /health with typed validation and unavailable-model responses.

## Validation
21 Python tests pass, including service readiness, inference, validation, and absent model cases. Backend and frontend baseline checks passed.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
