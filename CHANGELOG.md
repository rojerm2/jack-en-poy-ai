# Changelog

## 5.2 — Spring Boot ML integration

- FastAPI predictor and chronological/session-aware training pipeline.
- Server-owned session history, ML counter strategy, bounded inference timeout and random fallback.
- Validated game requests, separate live CSV with prediction metadata and sequential round numbers.
- Browser session ID propagation; storage errors do not advance completed history.

Validation: 20 Maven tests pass, covering history isolation/no current-move leakage, timeout/unavailable/invalid inference, CSV and HTTP validation. Frontend build/lint pass. Python suite: 21 passed.

## 5.1 — Python prediction service

- React game and Spring Boot CSV collection.
- Session-aware dataset pipeline, chronological training and validated prediction CLI.
- FastAPI POST /predict and GET /health with typed validation and unavailable-model responses.

Validation: 21 Python tests pass, including service readiness, inference, validation, and absent model cases. Backend and frontend baseline checks passed.

## 4.2 — ML prediction module

- Existing React game, Spring Boot API and CSV collection.
- Session-aware windows, chronological decision-tree training, atomic artifact serialization.
- Validated model loading, last-three-move prediction, class probabilities and model metadata.
- Root documentation and ignored local runtime files.

Validation: 13 Python tests pass; prediction CLI verified against the locally trained legacy model. Backend baseline: 10 tests pass. Frontend build/lint pass.

## 4.1 — First ML model

- React game and Spring Boot API with CSV recording.
- Session-aware dataset generation and serialized decision tree/one-hot encoder.
- Chronological 114-sample training set, 26-sample holdout, three-window gap.
- Root documentation is now tracked; Python caches and environments are ignored.

Validation: 5 Python tests and 10 Maven tests passed; frontend baseline build/lint passed. Legacy holdout accuracy: 42.31%, a small single-player sample.

## v0.3.0

### Added

- Python Machine Learning project
- ML project folder structure
- requirements.txt
- Dataset Generator
- Sliding Window algorithm
- Processed training dataset generation
- Dataset validation pipeline

### Changed

- Separated raw gameplay history from ML training data.
- Introduced feature engineering stage before model training.

---

## v0.2.0

- React frontend
- Backend integration

---

## v0.1.0

- Spring Boot backend

# Changelog

## v0.2.0

### Added

- React frontend
- TypeScript models
- Tailwind CSS
- Axios integration
- Home page
- Header component
- Footer component
- ScoreBoard component
- ResultCard component
- MoveButton component
- Dynamic game state
- Live scoreboard
- Loading indicator
- Error handling

### Changed

- Connected frontend to Spring Boot backend
- HomePage now manages application state
- Components receive data through props

### Fixed

- N/A

---

## v0.1.0

### Added

- Spring Boot backend
- REST API
- DTOs
- Validation
- Exception handling
- Winner evaluator
- Random move generator
- Unit tests
