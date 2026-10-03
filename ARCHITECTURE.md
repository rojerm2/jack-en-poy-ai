# Architecture

```text
React / TypeScript (Vite)
  POST /api/game/play {playerMove, sessionId}
           |
Spring Boot GameController → GameService (serialized per-round orchestration)
           |                |
           |                └── in-memory session history + score/statistics
           |
HttpMovePredictor → POST /predict {history: last 3 completed moves}
           |                     |
           |                FastAPI → ModelManager → validated Predictor
           |                                          |
           |                                     Joblib pipeline
           |                               one-hot encoder + selected classifier
           |
Override three identical completed moves (ADAPTIVE), then counter or random fallback
           |
WinnerEvaluator → CsvGameHistoryStore → append-only local live CSV
           |
Commit current move to session history and return result/analytics snapshot
           |
React waits for API + 1.35-second chant, then reveals result, scores and statistics
```

## Data and model lifecycle

Legacy sample CSV is checked in. Live history is a separate ignored CSV. Each live row records
session ID, per-session round number, UTC timestamp, moves, result, strategy, predicted move,
confidence, model name/version and fallback reason. Dataset generation builds three-move windows
within sessions in chronological target order; legacy rows form one sample session.

Training reserves the last 20% with a three-window gap for evaluation. Model comparison performs
three expanding chronological folds only within the training portion, then evaluates the fixed
selection on holdout. Preprocessing and model share one pipeline/artifact. Artifacts include
schema, dependency/model version, source hash, sample counts and evaluation.

Retraining freezes raw data, builds and validates a candidate, archives the previous model, and
replaces it atomically under a local file lock. Rollback validates a local archive before replacing
the active model. ModelManager checks file identity/timestamp/size on requests and swaps complete
predictors under a lock. A failed reload retains the last good model; no loaded model means 503.

## State and failure behavior

- The backend owns history; client requests cannot supply inference history.
- Computer selection occurs before current-move persistence/history updates.
- If ML is available and all three previous completed moves match, an explicit ADAPTIVE rule predicts
  that repeated move. Mixed windows still use ML; disabled/unavailable inference remains random.
- Adaptive round counts/win rates and CSV prediction accuracy are separate from ML accuracy/confidence.
  The streak rule cannot see the current move and can be beaten when the player changes moves.
- First three completed rounds, disabled inference, HTTP errors, timeouts and invalid responses use random play.
- History I/O failure returns 503; no session history/statistics update occurs.
- Session scores/statistics appear in play responses and a read-only GET endpoint.
- CSV analytics report persistent observed rates, model versions and confidence buckets.
- Session rates are null until their denominator is nonzero; warmup is excluded from prediction accuracy.
- Browser controls lock during a round, requests/timers abort on unmount, and reduced-motion settings remove motion.

## Runtime boundaries

Java 21/Spring Boot 4.1, Node 24/React 19, Python 3.12/scikit-learn. One backend instance maintains
an LRU limit of 1000 ephemeral sessions and serializes play. Restart/eviction loses session state.
CSV writes are serialized in that instance, not across multiple backend processes. There is no
shared database, authentication, automated scheduler, or public deployment. The global model
uses three previous moves; it is not per-player online learning. A lost HTTP response can leave
a recorded round, and future successful responses resynchronize scores.

## Verification

Unit/integration tests cover all game outcomes, request validation, history isolation/no current
move leakage, inference fallback, CSV persistence, analytics, preprocessing, serialization,
chronological selection, retraining/rollback/reload, animation ordering and UI recovery. The
cross-process smoke script packages Java separately and starts isolated services/data. The
GitHub Actions validation workflow repeats the Python, Java, frontend and smoke checks.
