# Contributing

Open an issue for a bug or a proposed change. Include steps to reproduce, expected/actual behavior,
and the relevant browser/runtime or Docker version. Avoid including live gameplay history or secrets.
Discuss larger changes before implementing them so the scope can be reviewed.

## Development

Follow the local setup in README.md. Use Java 21, Node 24, Python 3.12 and the checked-in lockfiles.
Create a branch in your fork, keep the diff focused, and update documentation when behavior changes.
Commit messages should describe the concrete change, for example `fix(game): reject invalid sessions`.

## Verification

```sh
# web/jack-en-poy-ai
npm ci
npm run typecheck
npm test
npm run lint
npm run build
npm run build:demo
npx playwright install chromium
npm run test:e2e
npm audit --audit-level=high

# core/jack-en-poy-ai
./mvnw clean verify

# ml, with the Python environment active
python -m pip check
python -m pytest

# repository root, after packaging Java
python scripts/smoke_test.py
python scripts/container_smoke.py
```

Use `mvnw.cmd` on Windows. CI repeats the application and deployment checks. Add regression tests
for behavior changes; include the relevant verification results in the pull request.

## Contracts to preserve

- Choose computer moves using completed history only; never send the current move to Python.
- Keep CSV sessions separate when generating training windows.
- Keep holdout rows outside training and model selection.
- Reveal outcomes only after both the API and animation finish.
- Distinguish ML predictions, repetition rules and random fallback in analytics.
- Keep the browser demo independent of Java/Python and label it clearly.

Contributions are licensed under the repository's MIT license. Report vulnerabilities as described
in SECURITY.md rather than posting exploit details in a public issue.

## Dependency maintenance
Dependabot groups routine updates monthly with one open request per ecosystem. npm and Docker
major-version upgrades require a deliberate migration; Python Docker updates stay on 3.12.
Keep Node types on Node 24 and TypeScript on the version supported by typescript-eslint.
Pydantic pins its core package exactly, so refresh both lock entries together after dependency
resolution instead of accepting an independent pydantic-core update. All updates must pass the
application, browser and container checks before merging. Historical failed runs remain in Actions
even after a later successful run fixes the branch.
