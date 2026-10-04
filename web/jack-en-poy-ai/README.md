# Web game

Use Node 24 LTS. From this directory:

```sh
npm ci
npm run dev
npm test
npm run lint
npm run build
```

Open localhost:5173. Run the Spring Boot API on localhost:8080.
The first-person SVG hands chant Jack, En, Poy for 1.35 seconds. The current round's
result and score are revealed only after both the animation and API response complete.
Move controls are locked during a round. Reduced-motion settings remove hand movement.

Use R/P/S to play, or tab to the move buttons and press Enter. New game starts a fresh
server session and clears visible scores/recent rounds; saved CSV history is retained.
Prediction details appear after reveal. The last six rounds remain visible.

The Vite dev/preview proxy sends `/api` to localhost:8080. For a separately hosted API,
set `VITE_API_URL` before building (see `.env.example`). Requests time out after 10 seconds.
Serve `/api` through the same origin in a production deployment, or configure CORS.

Expand Session statistics after a round for prediction accuracy, computer win rates by strategy, sample counts, and your move distribution. Stats and scores come from the backend and remain hidden until reveal.

## Standalone browser demo

`npm run build:demo` writes `dist-demo/`, which plays locally without an API. The banner explains that model inference and saved history are unavailable. Set `VITE_BASE_PATH=/repository-name/` when building for a GitHub Pages project site.

`npm run test:e2e` verifies the built demo in Chromium. Install the test browser first with `npx playwright install chromium`; GitHub Actions also checks a phone viewport and publishes screenshots.
