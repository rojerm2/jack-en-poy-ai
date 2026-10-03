# Game API

Use JDK 21 and the Maven wrapper. From this directory:

```sh
./mvnw test
./mvnw spring-boot:run
# Windows: .\mvnw.cmd test; .\mvnw.cmd spring-boot:run
```

`POST /api/game/play`: `{"playerMove":"ROCK","sessionId":"a UUID"}`.
Omit sessionId on a first request to let the server create one; reuse the returned ID.
The server owns the last three completed moves. Each response includes the session,
round number, moves, result, strategy, prediction confidence and fallback reason.
The first three rounds are random. Then the computer counters the predicted player move.

`ML_SERVICE_URL` defaults to `http://127.0.0.1:8001`; `ML_TIMEOUT_MS` defaults to 600.
Set `ML_ENABLED=false` to use random play. Any service failure uses random fallback.
`GAME_HISTORY_PATH` defaults to `../../ml/data/raw/live-history.csv`; legacy sample CSVs
are preserved. Storage failure returns 503 and does not advance in-memory history.

This is a single-instance portfolio app. Sessions are in memory, with a 1000-session
LRU bound. Restarting the API or eviction loses that session's inference history.
Requests are serialized to keep prediction, recording and history updates in order.

GAME_ALLOWED_ORIGINS is a comma-separated list; defaults allow localhost:5173 and 127.0.0.1:5173. Configure explicit deployed origins when hosting separately.
