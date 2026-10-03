# Architecture

React → Spring Boot session GameService → HTTP inference → FastAPI ModelManager/Predictor → Joblib pipeline.
Computer selection occurs before current-move recording. Failures use random fallback.
Raw live CSV → frozen snapshot → session windows → chronological training → validated candidate → archived old model → atomic promotion.
ModelManager watches timestamp/size on requests, swaps validated immutable predictors, and retains the previous model when reload fails. Local CLI owns training and rollback; no training/upload HTTP endpoint.
Game sessions are ephemeral, bounded to 1000, and serialize play operations.
