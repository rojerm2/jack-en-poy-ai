# Deployment and operations

## Supported layout

The release supports one Docker Compose stack. The web container serves built files through Nginx
and proxies `/api` to Java. Java and Python use a private internal network. The web container also joins a host-facing network for its published loopback port. Runtime
containers use unprivileged users, read-only root filesystems, temporary filesystems and memory limits.
The proxy limits request bodies to 4 KiB and API traffic to 5 requests/second/IP with a burst of 10.

The GitHub Pages build is a separate browser demo. It has no backend URL, makes no API requests,
and runs no trained model. It can be used even when all Docker/local services are stopped.

## Start, check and stop

From the repository root:

```sh
docker compose up --build --detach --wait
docker compose ps
curl --fail http://localhost:8088/api/health
docker compose logs --follow
docker compose stop
```

`GET /api/health` checks that Java can write gameplay history. Python's `/health` checks that a
validated model is loaded. Python failure does not make the Java API unavailable; gameplay falls
back to random selection. Container health checks and restart policies expose failures to Docker.

## Configuration

Copy `deploy/.env.example` to `.env` at the repository root when changing Compose defaults.

| Setting | Default | Purpose |
| --- | --- | --- |
| `WEB_BIND` | `127.0.0.1` | Host interface for the web entry point |
| `WEB_PORT` | `8088` | Host web port |
| `GAME_ALLOWED_ORIGINS` | localhost/127.0.0.1:8088 | Explicit browser origins |
| `ML_SERVICE_URL` | http://ml:8001 in Compose | Backend-to-Python URL |
| `ML_TIMEOUT_MS` | 600 | Inference timeout in milliseconds |
| `ML_ENABLED` | true | Backend inference switch |
| `GAME_HISTORY_PATH` | /data/history/live-history.csv in Compose | Writable history path |
| `MODEL_PATH` | /app/models/player-move.joblib in Compose | Active Python artifact |

For a public server, place an HTTPS reverse proxy in front of the loopback web entry point and
set the exact public origin in `GAME_ALLOWED_ORIGINS`. Do not publish Java/Python ports. There is
no hosted backend for this repository's Pages demo and no public server provisioned by this release.

## Data and models

Named volumes `history`, `models` and `reports` persist across `docker compose down` and subsequent
startup. Avoid `down --volumes` when retaining data; that command removes the volumes. Backend
sessions are intentionally ephemeral, so restarting Java clears visible session scores and the
three-move inference window. Existing CSV rows remain available for analysis/training.

The first model is selected at image build time from the checked-in sample. On first startup the
image seeds an empty model volume. Existing models are retained during upgrades. To retrain:

```sh
docker compose exec ml python retrain.py --history /data/history/live-history.csv --compare
docker compose exec ml python analytics.py --history /data/history/live-history.csv
docker compose exec ml python retrain.py --rollback models/archive/<previous-model>.joblib
```

Retraining comparison requires at least 64 session-aware windows. Short/invalid datasets leave
the current artifact intact. Candidate validation, model archives and atomic promotion protect
the active model. Requests load valid replacements and retain the last good model if reload fails.
Only load trusted locally trained or release-provided Joblib artifacts.

## Backup and restore

Stop the stack before taking a consistent backup. On Linux/macOS, with Docker's default project name:

```sh
docker compose stop
mkdir -p backups
docker run --rm --network none -v jack-en-poy_history:/data:ro -v "$PWD/backups:/backup" alpine:3.23 tar -czf /backup/history.tar.gz -C /data .
docker run --rm --network none -v jack-en-poy_models:/data:ro -v "$PWD/backups:/backup" alpine:3.23 tar -czf /backup/models.tar.gz -C /data .
docker run --rm --network none -v jack-en-poy_reports:/data:ro -v "$PWD/backups:/backup" alpine:3.23 tar -czf /backup/reports.tar.gz -C /data .
docker compose start
```

Keep backups outside the repository. Custom Compose project names change the volume prefix;
inspect `docker volume ls` first. Restore into new empty volumes while the stack is stopped:

```sh
docker run --rm --network none -v jack-en-poy_history:/data -v "$PWD/backups:/backup:ro" alpine:3.23 tar -xzf /backup/history.tar.gz -C /data
docker run --rm --network none -v jack-en-poy_models:/data -v "$PWD/backups:/backup:ro" alpine:3.23 tar -xzf /backup/models.tar.gz -C /data
docker run --rm --network none -v jack-en-poy_reports:/data -v "$PWD/backups:/backup:ro" alpine:3.23 tar -xzf /backup/reports.tar.gz -C /data
```

The archive retains ownership. Runtime services use UID 10001. Do not mix a legacy sample CSV
with the live-history schema. Retention is an operator responsibility; this project does not
automatically delete gameplay history.

## Updates and rollback

Back up the volumes, check out a release tag and rebuild:

```sh
git fetch --tags
git checkout v1.1.0
docker compose up --build --detach --wait
```

To roll back, check out the previously validated release and repeat the build. Retain the matching
model archive and dependency versions. The sample model schema requires the exact scikit-learn
version recorded in its artifact. Do not replace a validated deployment with untested dependency updates.

## Release verification

```sh
python scripts/container_smoke.py
```

This verifier uses a unique disposable Compose project. It builds all images, checks readiness,
security headers and private service ports, plays repeated rock against Python, stops inference
to verify fallback, and restarts Java to confirm CSV retention. It removes only its own test
containers/volumes. Run it when port 8088 is free. CI executes this check on Linux before Pages deployment.
