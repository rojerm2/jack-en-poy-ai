FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /build/core/jack-en-poy-ai
COPY core/jack-en-poy-ai/ ./
COPY LICENSE /build/LICENSE
RUN chmod +x mvnw && ./mvnw --batch-mode -DskipTests package

FROM eclipse-temurin:21-jre-jammy
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --create-home app \
    && mkdir -p /app /data/history && chown -R app:app /app /data
WORKDIR /app
COPY --from=build /build/core/jack-en-poy-ai/target/jack-en-poy-ai-1.1.0.jar app.jar
COPY LICENSE /app/LICENSE
USER 10001:10001
ENV GAME_HISTORY_PATH=/data/history/live-history.csv
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=3 \
    CMD curl --fail --silent http://127.0.0.1:8080/api/health || exit 1
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75", "-jar", "/app/app.jar"]
