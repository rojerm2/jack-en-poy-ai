# Architecture

React → Spring Boot → CSV history.
Python CSV → session-aware windows → encoder/decision tree → Joblib artifact.
FastAPI loads the local artifact once at startup and serves POST /predict and GET /health.
Spring Boot integration is next.
