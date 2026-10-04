# Changelog

## 1.1.0 — 2026-10-04

### Added
- Docker Compose deployment with non-root images, private services, health checks and persistent data volumes.
- Standalone browser demo for GitHub Pages, with local random play and repetition counters.
- Repetition counters that stop an offline model from repeating the same losing computer move.
- Separate repetition statistics and explicit strategy explanations in the UI.
- Release bundles/checksums, MIT licensing, contribution/security guidance and automated dependency updates.

### Changed
- Updated Spring Boot to 4.1.1 and aligned module versions at 1.1.0.
- Restricted container runtime writes, added proxy request/rate limits and enabled graceful backend shutdown.
- Pinned CI actions and added Docker deployment validation before Pages publishing.

## 1.0.0 — 2026-10-03

- Added validated training/prediction, FastAPI inference and backend ML counters with random fallback.
- Added first-person animation, keyboard/session controls and post-reveal prediction details.
- Added snapshot retraining, model archives/rollback, chronological comparison and performance analytics.
- Added application tests, real-service integration validation and reproducible local setup.

## 0.3.0

- Added CSV gameplay collection and three-move dataset generation.

## 0.2.0

- Added React gameplay, backend integration, scores and loading/error states.

## 0.1.0

- Added the Spring Boot game API, random strategy and game-rule tests.
