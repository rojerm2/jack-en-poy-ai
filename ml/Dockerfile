FROM python:3.12-slim-bookworm AS build
WORKDIR /app
COPY ml/requirements-lock.txt ./
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY ml/ ./
RUN python -m src.dataset.main \
    && python retrain.py --history data/raw/game-history.csv --compare \
        --output /app/seed/player-move.joblib --report /app/seed/training-report.json

FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 MODEL_PATH=/app/models/player-move.joblib
RUN useradd --uid 10001 --create-home app \
    && mkdir -p /app/models /app/reports /data/history \
    && chown -R app:app /app /data
WORKDIR /app
COPY --from=build /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY --from=build --chown=app:app /app/seed/ /app/seed/
COPY --chown=app:app ml/src/ /app/src/
COPY --chown=app:app ml/*.py ml/requirements-lock.txt /app/
COPY --chown=app:app ml/docker-entrypoint.sh /app/docker-entrypoint.sh
COPY LICENSE /app/LICENSE
RUN chmod +x /app/docker-entrypoint.sh
USER 10001:10001
EXPOSE 8001
HEALTHCHECK --interval=15s --timeout=4s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/health', timeout=2)"
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1", "--no-access-log"]
