# Project context

Jack-En-Poy AI v1.0.0 is a React/TypeScript game, Spring Boot API, and Python move predictor.
All planned milestones 4.1 through 8 are complete. TODO.md contains future improvements.

## Current implementation
- First-person SVG hands, three-beat animation, delayed result/score reveal, keyboard controls and session reset.
- Backend-owned completed history, ML counter strategy, bounded inference timeout and random fallback.
- Repetition correction after v1.0.0: three identical completed moves override available ML inference
  with an explicit ADAPTIVE counter. Separate UI/CSV/session statistics avoid reporting it as ML.
  Mixed windows use ML; unavailable/disabled inference remains random. The current move is never used.
- Server-authoritative scores, session analytics and persistent CSV metadata; read-only analytics endpoint.
- Session-aware datasets, serialized preprocessing/model, typed prediction service and validated model reload.
- Snapshot retraining, model archives/rollback, chronological comparison of two baselines and five classifiers.
- Frontend/backend/service version 1.0.0, pinned Python dependencies, GitHub Actions and isolated cross-process smoke test.

## Final validation
Clean dependency installation and checks passed using Java 21, Node 24 and Python 3.12.
35 Python tests, 27 backend tests and 13 frontend tests pass after the repetition correction. Type checking, lint, production
build, Maven clean verify and pip check pass; npm audit reports zero vulnerabilities.
Dataset generation, training, serialization, prediction, comparison, retraining and analytics CLIs pass.
The actual packaged Java/Python smoke test verifies offline random play, online ML counters from
completed history, all three repeated-move counters, service-failure fallback, authoritative scores
and persistent CSV analytics. A regression test reproduced the scissors loop before the correction.
The production browser preview verifies reveal/input locking, scores, fourth-round inference,
statistics and new-session reset. Remote CI status is separate from these local checks.

## Evaluation and limits
The checked-in 146-round legacy sample selects logistic regression using training-only chronological
folds. Holdout accuracy is 42.31% over 26 rows; this small reused sample does not establish general
improvement over random play. Confidence is uncalibrated and strategy rates are observational.
One backend instance keeps up to 1000 ephemeral sessions and serializes play. Restart/eviction loses
session state. A lost response can represent a recorded round; the next response resynchronizes scores.
The model is global. No authentication, shared database or public deployment is configured.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Use Java 21, Node 24 and Python 3.12, the Maven wrapper and dependency lockfiles.
- Predict only from previous completed rounds; never send the current move to inference.
- Keep live history, generated models/reports, environments and build outputs out of Git.
- Validate, document, review and commit logical changes; use normal non-destructive pushes.
- Follow README.md for reproducible setup and TODO.md for future work.
