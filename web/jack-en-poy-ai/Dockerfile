FROM node:24-bookworm-slim AS build
WORKDIR /build
COPY web/jack-en-poy-ai/package*.json ./
RUN npm ci
COPY web/jack-en-poy-ai/ ./
RUN npm run build

FROM nginxinc/nginx-unprivileged:stable-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /build/dist/ /usr/share/nginx/html/
COPY LICENSE /usr/share/nginx/html/LICENSE
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8080/health || exit 1
