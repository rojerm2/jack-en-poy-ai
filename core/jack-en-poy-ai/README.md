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

GAME_ALLOWED_ORIGINS is a comma-separated list; defaults allow localhost/127.0.0.1 on ports 5173 (dev) and 4173 (preview). Configure explicit deployed origins when hosting separately.

Each play response includes server-authoritative session scores and analytics. `GET /api/game/analytics?sessionId=<UUID>` reads the same snapshot without playing a round. Rates are null when no relevant rounds exist. In-memory analytics are lost on restart/eviction; persistent offline analytics use the CSV.


When ML is available, three identical completed moves use an explicit repetition counter (strategy
`ADAPTIVE`). This prevents a stale model from repeatedly choosing the same losing counter. Adaptive
rounds have no model confidence and expose `adaptiveRounds`/`adaptiveWinRate` separately. Only prior
completed history is used; mixed windows remain ML and disabled/unavailable inference remains random.
