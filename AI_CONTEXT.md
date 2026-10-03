# Project context

Jack-En-Poy AI is a React/TypeScript game, Spring Boot API, and Python move predictor.
The current completed milestone is 6.2 — Gameplay/UI polish. Next: 7.1 — Retraining workflow.

## Current implementation
- Full ML counter strategy with random fallback and server-owned history.
- First-person animated table with reveal gating and reduced-motion support.
- Keyboard R/P/S controls, new-session reset, six-round history and post-reveal prediction details.
- Configurable API URL, request timeout, local proxy and configurable CORS origins.
- Frontend dependency audit findings resolved with compatible updates.

## Validation
8 frontend tests, TypeScript build and lint pass. 21 Maven tests pass, including local CORS preflight. Real browser round/reveal/score/history and real Python inference verified. npm audit: 0 reported vulnerabilities.

## Working conventions
- Canonical documentation lives at the repository root and is tracked by Git.
- Java 21, Node 24, Python 3.12; use the Maven wrapper and the frontend lockfile.
- Predict using only the player's previous completed rounds; never send the current move to inference.
- Local game history and generated model/report files are ignored. The checked-in legacy history is sample data.
- Changes should be validated, documented, committed, and normally pushed by milestone.
