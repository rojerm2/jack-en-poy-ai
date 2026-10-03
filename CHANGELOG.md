# Changelog

## Unreleased

- Fixed indefinite wrong counters when an offline model mispredicts repeated player moves.
  Three identical completed moves now use an explicit repetition strategy when ML is available.
- Added ADAPTIVE metadata, separate session/CSV analytics, and an accurate UI explanation.
- Regression coverage verifies all three moves, session isolation, changed-current-move behavior,
  unavailable-service fallback, reveal gating and separate statistics.
- Validation: 27 backend, 35 Python and 13 frontend tests; build/type checking/lint and the real-service
  smoke test pass, including six repetition counters across rock, paper and scissors.

## v1.0.0 — 2026-10-03

- Completed milestones 4.1–8: model training/prediction, Python service, backend ML integration,
  first-person animation, gameplay polish, retraining/rollback, model comparison and analytics.
- Added a cross-process integration smoke test and GitHub Actions validation.
- Pinned Python dependencies, validated clean installs/builds, and documented local setup and limits.
- Aligned frontend, backend and service versions at 1.0.0.
- Final validation: 33 Python, 24 backend and 11 frontend tests; builds/lint/type checking,
  zero npm audit findings, real-service smoke test and production browser gameplay passed.


## 7.3 — AI performance analytics

- Full first-person game, session/keyboard controls and reveal gating.
- Backend-authoritative scores and per-session prediction accuracy, strategy win rates and move distribution.
- Read-only analytics endpoint and accessible frontend statistics panel with explicit denominators.
- Persistent CSV reports group model/version metrics, confusion matrices, confidence buckets and fallback reasons.
- Snapshot retraining/rollback/reload and chronological comparison of two baselines and five classifiers.

Validation: 33 Python tests, 11 frontend tests, frontend build/lint and 23 backend tests pass; the added analytics endpoint test also passes (24 total backend tests for final validation). Live CSV analytics CLI verified.

## 7.2 — Model comparison

- Full animated React game and backend-owned session inference with random fallback.
- Snapshot retraining, archiving, rollback and validated service reload.
- Majority/frequency baselines plus tree, forest, logistic regression, KNN and Naive Bayes comparison.
- Three expanding chronological training folds select the model before final holdout evaluation.
- Selected-model retraining uses the same validated promotion workflow.

Validation: 30 Python tests pass, including unchanged selection when final holdout labels change. Comparison and selected-model CLI promotion verified on legacy data: logistic regression selected, 42.31% on 26 holdout rows. Frontend: 8 tests/build/lint; backend: 21 tests.

## 7.1 — Retraining workflow

- Animated React game with keyboard/session controls and reveal gating.
- Backend-owned three-move history, ML counter strategy, random fallback and session CSV metadata.
- Frozen-history retraining, minimum-data validation, CLI lock, model archives and rollback.
- Automatic validated model reload; failed replacements retain the last good model.

Validation: 26 Python tests pass, including retrain/rollback/locking/reload and failed-promotion safety. Real retraining CLI verified on the 146-round legacy sample. Frontend: 8 tests/build/lint. Backend: 21 tests.

## 6.2 — Gameplay/UI polish

- Full ML counter strategy with random fallback and server-owned history.
- First-person animated table with reveal gating and reduced-motion support.
- Keyboard R/P/S controls, new-session reset, six-round history and post-reveal prediction details.
- Configurable API URL, request timeout, local proxy and configurable CORS origins.
- Frontend dependency audit findings resolved with compatible updates.

Validation: 8 frontend tests, TypeScript build and lint pass. 21 Maven tests pass, including local CORS preflight. Real browser round/reveal/score/history and real Python inference verified. npm audit: 0 reported vulnerabilities.

## 6.1 — First-person Jack-En-Poy animation

- Chronological/session-aware ML pipeline, FastAPI service and backend counter strategy with fallback.
- First-person SVG hands on a responsive game table; three-beat 1.35-second chant.
- Input locking, abort cleanup, result/score reveal after animation and API completion.
- Reduced-motion support and accessible round status.

Validation: 5 frontend timing/error/score tests pass; TypeScript production build and lint pass. Narrow-layout browser screenshot verified. Backend: 20 tests; Python: 21 tests.

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

- Added raw CSV history, sliding-window dataset generation and the Python module.

## v0.2.0

- Added React/TypeScript gameplay, backend integration, scoreboard and loading/error states.

## v0.1.0

- Added Spring Boot game API, move/result domain types, random strategy and game-rule tests.
