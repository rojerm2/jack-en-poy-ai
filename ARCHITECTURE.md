# Architecture

React POST /api/game/play → Spring Boot GameService → HttpMovePredictor POST /predict → FastAPI/Predictor → local Joblib pipeline.
GameService retains three completed moves per session and counters the prediction before recording the current move.
Insufficient history, disabled ML, timeout, HTTP error or invalid output uses random play.
CSV live history includes session ID, per-session round number and prediction metadata. Session state is in memory, bounded to 1000 LRU entries; requests serialize in this single-instance app.
Python raw CSV → session-aware windows → chronological training/holdout → atomic Joblib model.
