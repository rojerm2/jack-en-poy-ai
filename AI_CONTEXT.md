# Project context

Jack-En-Poy AI 1.1.0 is an MIT-licensed rock-paper-scissors project with React, Spring Boot and FastAPI.
The release ships a complete Docker Compose stack and a separate GitHub Pages browser demo.
The public demo has no hosted backend; Docker is the supported way to try the full application.

## Current behavior
- First-person SVG hands, keyboard controls, session reset, recent rounds and delayed outcome reveal.
- Backend-owned completed history, ML counters, explicit ADAPTIVE repetition rules and random fallback.
- Separate ML/rule/random statistics; CSV collection and offline analytics.
- Session-aware training, chronological model comparison, validated retraining/rollback and model reload.
- Private non-root containers, read-only roots, persistent CSV/model/report volumes, health checks and proxy limits.
- Clearly labeled browser demo with no API requests, ML inference or persisted gameplay.
- Pinned CI actions, container/application checks, Pages publishing and checksummed release artifacts.

## Scope and limits
Java serializes rounds and caches up to 1000 in-memory sessions. Restart/eviction resets session state;
CSV volumes remain. Request deduplication and shared session storage are future work. The classifier
is global and does not train during play. A lost response may represent a saved round.
The legacy sample selects logistic regression with 42.31% holdout accuracy on 26 rows; this small
reused sample does not establish general improvement over random play. Confidence is uncalibrated.

## Working conventions
- Java 21, Node 24, Python 3.12; use Maven/npm/Python lockfiles.
- Predict only from previous completed rounds and never use the current move in selection.
- Keep ML, rule and random-play denominators separate. Never label the browser demo as trained ML.
- Keep holdout rows outside fitting/selection and protect active models during retraining.
- Keep live history, artifacts, environments and build outputs out of Git.
- Validate logical changes, update current documentation and use ordinary non-destructive commits/pushes.
- Root documentation is canonical. README/CONTRIBUTING/deployment docs describe public workflows.
