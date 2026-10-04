# Architecture

## Complete application

React sends `{playerMove, sessionId}` to `/api/game/play`. Nginx serves built assets and proxies
the same-origin API path. Java owns a bounded session cache, sends only the last three completed
moves to FastAPI, counters the returned prediction and evaluates the round. It appends a CSV row
before advancing session history/statistics. Storage failure returns 503 without advancing state.

If available inference sees three identical previous moves, Java uses the repetition rule instead
and records strategy ADAPTIVE. Mixed windows use ML. Warmup, disabled inference, timeout and invalid
responses use RANDOM. Rule rounds have no classifier confidence or model identity.

The browser starts the request and a cancellable 1.35-second reveal timer together. Controls stay
locked until both finish. Scores come from the backend snapshot. Requests/timers abort on unmount;
reduced-motion preferences remove hand motion without bypassing the reveal timing.

## Browser demo

A separate Vite build sets `VITE_DEMO_MODE=true`. `DemoGame` implements random play, repetition
counters and local statistics without HTTP requests. A visible notice states that no trained model
or saved gameplay is involved. New game resets the in-memory demo. GitHub Pages serves this build
under the repository base path; it does not host Java or Python.

## Data and model lifecycle

Legacy sample CSV is checked in. Live gameplay is a separate ignored CSV with session ID, round,
UTC timestamp, moves, result and strategy/prediction metadata. Dataset generation builds three-move
windows within each session and preserves chronological target order.

Training reserves the last 20% with a three-window gap. Model selection uses three expanding folds
within the training portion, then evaluates the fixed selection on holdout. Preprocessing and the
classifier share one artifact with dependency version, source hash, sample counts and evaluation.

Retraining freezes history, builds/validates a candidate, archives the previous model and replaces
it atomically under a local lock. Rollback validates an archive before replacing the active model.
The service checks file identity/time/size on requests and retains its last good predictor on failed
reload. No loaded model means HTTP 503.

## Deployment boundaries

Compose runs one Nginx, Java and Python container on a private network. Only Nginx is bound to the
host, on loopback by default. Containers use non-root users, read-only roots and writable named
volumes for history/models/reports. Health checks verify the web server, history storage and model
readiness. Nginx applies body/rate limits and browser security headers. Java shuts down gracefully.

The backend has an LRU limit of 1000 ephemeral sessions and serializes play. CSV writes are safe
within one process, not across independent backend instances. Restart/eviction loses session state;
CSV volumes remain. A lost response may leave a recorded round; later responses resynchronize scores.
There is no account system, shared database, automatic retraining scheduler or hosted backend.

CI validates application behavior, Docker readiness/fallback/history retention and release packaging.
Pages publishing follows successful validation. Release downloads include checksums and licensing.
