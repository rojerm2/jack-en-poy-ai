# Jack-En-Poy AI

Rock-Paper-Scissors built with React, Spring Boot, and a scikit-learn prediction service.
The computer uses your previous three completed moves to predict the next move and
counters that prediction. It uses random play during warmup or when inference is unavailable.

Version **1.0.0**.

## Features

- First-person SVG hands, a Jack-En-Poy chant, and results revealed after the animation.
- Keyboard controls, session scores, recent rounds, and reduced-motion support.
- Server-owned player history, bounded HTTP inference, and random fallback.
- Session-aware CSV collection, reproducible datasets, model comparison and retraining.
- Prediction accuracy, win rates by strategy, move distribution, and offline model/version reports.

## Repository

| Directory | Purpose |
| --- | --- |
| `web/jack-en-poy-ai` | React 19, TypeScript, Vite and Tailwind |
| `core/jack-en-poy-ai` | Spring Boot REST API, Java 21 and Maven wrapper |
| `ml` | Dataset, training, comparison, inference and analytics |
| `scripts/smoke_test.py` | Real Java/Python integration with temporary ports and data |

## Local setup

Prerequisites: **JDK 21**, **Node 24**, and **Python 3.12** available on PATH. Maven is
provided by the wrapper. Use three terminals. Commands below use PowerShell.

### 1. Train and start Python

```powershell
cd ml
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m src.dataset.main
.\.venv\Scripts\python.exe train.py
.\.venv\Scripts\python.exe -m uvicorn service:app --host 127.0.0.1 --port 8001
```

Training starts with the small checked-in legacy sample. The resulting artifact is local
and ignored by Git. `GET http://127.0.0.1:8001/health` reports model readiness. The game
also works without this service; all rounds then use random play.

### 2. Start the game API

```powershell
cd core/jack-en-poy-ai
.\mvnw.cmd spring-boot:run
```

### 3. Start the frontend

```powershell
cd web/jack-en-poy-ai
npm ci
npm run dev
```

Open **http://127.0.0.1:5173**. Choose a move or press R/P/S. The first three rounds of
each session are random. The fourth round can use inference. New game clears visible
scores and starts a fresh session while retaining saved history.

On Linux/macOS use `python3 -m venv .venv`, `.venv/bin/python` and `./mvnw` in place of
the Windows Python environment and wrapper commands. Other commands are the same.

## API contract

`POST /api/game/play`

```json
{"playerMove":"ROCK","sessionId":"00000000-0000-4000-8000-000000000001"}
```

Omit sessionId to start a server-generated session and reuse the returned ID. The response
wraps `success`, `message`, and `data`. Data includes moves, result, session ID, round number,
prediction metadata, and an authoritative analytics/score snapshot. Invalid moves or sessions
return 400. History-storage failure returns 503 and does not advance completed history.

`GET /api/game/analytics?sessionId=<UUID>` reads session statistics without playing.
`POST http://127.0.0.1:8001/predict` accepts only three completed moves:

```json
{"history":["ROCK","PAPER","SCISSORS"]}
```

The current move is never included in that request. Python returns a predicted move,
probabilities, confidence and model version. Invalid requests return 422; an unavailable
model returns 503. The backend handles inference errors through random fallback.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `ML_SERVICE_URL` | `http://127.0.0.1:8001` | Backend inference service |
| `ML_ENABLED` | `true` | Set false for random play |
| `ML_TIMEOUT_MS` | `600` | Backend inference timeout |
| `GAME_HISTORY_PATH` | `../../ml/data/raw/live-history.csv` | Relative to the backend working directory |
| `GAME_ALLOWED_ORIGINS` | localhost/127.0.0.1 on ports 5173 (dev) and 4173 (preview) | Explicit comma-separated CORS origins |
| `MODEL_PATH` | `ml/models/player-move.joblib` | Resolved within the Python module by default |
| `VITE_API_URL` | `/api` | Frontend API URL at build time |

Vite dev and preview proxy `/api` to the local backend. A deployed frontend needs a same-origin
`/api` proxy or an explicit build-time URL and CORS origin. Python uses loopback in these setup
commands. There is no authentication or public-hosting configuration in this portfolio release.

## Retraining and evaluation

From `ml/`, using the environment's Python:

```powershell
.\.venv\Scripts\python.exe retrain.py
.\.venv\Scripts\python.exe retrain.py --compare
.\.venv\Scripts\python.exe compare.py
.\.venv\Scripts\python.exe analytics.py
.\.venv\Scripts\python.exe predict.py ROCK PAPER SCISSORS
```

Retraining reads a frozen live-history snapshot and requires at least 16 windows and two
training classes. Comparison requires 64 windows. Short sessions contribute no windows until
their fourth recorded move. Collect enough complete rounds before retraining. For a reproducible
sample comparison, use `retrain.py --history data/raw/game-history.csv --compare`.

The workflow validates a candidate, archives the active model and replaces it atomically.
`retrain.py --rollback models/archive/<file>.joblib` restores a locally created archive.
The running service loads validated replacements on requests and keeps its last valid model
if a replacement fails. A local model lock prevents concurrent retraining operations.

Comparison covers majority/frequency baselines, Decision Tree, Random Forest, Logistic
Regression, KNN and Gaussian Naive Bayes. The last 20% forms a holdout with a three-window gap.
Three chronological folds within training data select the model; the holdout is reported afterward.

On the checked-in 146-round legacy sample, selection chose logistic regression, with **42.31%
accuracy over 26 holdout rows**. Uniform random expected accuracy is 33.33%. This is a small,
single-player reused sample, so it does not establish general improvement over random play.
Classifier confidence is uncalibrated. Live strategy win rates describe different rounds,
not a controlled experiment. Reports in `ml/reports/` include denominators and model versions.

## Validation

```powershell
# Frontend directory
npm ci
npm run typecheck
npm test
npm run lint
npm run build
npm audit --audit-level=high

# Backend directory
.\mvnw.cmd clean verify

# Python directory
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest

# Repository root, after packaging the backend
ml\.venv\Scripts\python.exe scripts/smoke_test.py
```

The smoke test starts the actual packaged Java application and Python service with isolated
ports/model/history, verifies gameplay without Python, ML counters after warmup, fallback after
service shutdown, authoritative scores, and persistent analytics, then stops its own processes.
It never adds rows to the sample or live developer history. GitHub Actions runs the same validation
on pushes and pull requests.

## Limits and next work

This is a single-instance local application. Up to 1000 sessions are kept in memory and play
operations are serialized. Restart/eviction resets inference history and session statistics;
recorded CSV history remains available. A lost HTTP response can represent a recorded round;
the next successful response resynchronizes scores. Request deduplication and shared persistent
sessions are future work. The model is global rather than personalized per player.

Future work includes larger independent datasets, calibrated confidence, persistent session
storage, request deduplication, drift monitoring and deployment/authentication appropriate to
the intended hosting environment. See [TODO.md](TODO.md).

## Documentation

[AI_CONTEXT.md](AI_CONTEXT.md) describes current state. [ARCHITECTURE.md](ARCHITECTURE.md),
[DECISIONS.md](DECISIONS.md), and [CHANGELOG.md](CHANGELOG.md) record design and milestones.
Module READMEs contain additional commands. Root documents are canonical and tracked;
the earlier ignored `internal_docs/` copies are local mirrors.
