# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 7.3 — AI performance analytics. Next: 8 — Portfolio release and final v1.0.0 validation.

## Current implementation
- Full first-person game, session/keyboard controls and reveal gating.
- Backend-authoritative scores and per-session prediction accuracy, strategy win rates and move distribution.
- Read-only analytics endpoint and accessible frontend statistics panel with explicit denominators.
- Persistent CSV reports group model/version metrics, confusion matrices, confidence buckets and fallback reasons.
- Snapshot retraining/rollback/reload and chronological comparison of two baselines and five classifiers.

## Validation
33 Python tests, 11 frontend tests, frontend build/lint and 23 backend tests pass; the added analytics endpoint test also passes (24 total backend tests for final validation). Live CSV analytics CLI verified.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
