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
