#!/bin/sh
set -eu
if [ ! -f "$MODEL_PATH" ]; then
    cp /app/seed/player-move.joblib "$MODEL_PATH"
fi
exec "$@"
