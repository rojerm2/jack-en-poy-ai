# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 5.2 — Spring Boot ML integration. Next: 6.1 — First-person Jack-En-Poy animation.

## Current implementation
- FastAPI predictor and chronological/session-aware training pipeline.
- Server-owned session history, ML counter strategy, bounded inference timeout and random fallback.
- Validated game requests, separate live CSV with prediction metadata and sequential round numbers.
- Browser session ID propagation; storage errors do not advance completed history.

## Validation
20 Maven tests pass, covering history isolation/no current-move leakage, timeout/unavailable/invalid inference, CSV and HTTP validation. Frontend build/lint pass. Python suite: 21 passed.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
