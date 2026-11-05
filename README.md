# Todo app

One person keeps lists of to-dos in the browser. The API and the pages are the app already built in this repo. This file is how to run it, test it, and ship it with Docker.

## Run the whole app

Docker Compose v2 (`docker compose`) is required.

```bash
docker compose up --build
```

Open http://127.0.0.1:8080. Postgres is published on `127.0.0.1:5433` so it does not collide with a Postgres already using 5432. The API is only reachable on the Compose network. The web container proxies `/api` to it.

`APP_ENV` defaults to `dev`. Override it when you start the stack:

```bash
APP_ENV=dev docker compose up --build
```

Logs and health:

```bash
docker compose logs
docker compose ps
```

The API serves `GET /api/health`. A database failure returns 503.

## Test profile

The test profile runs the API suite against a separate `todo_test` database. It truncates that database. It does not touch the dev database.

```bash
docker compose --profile test run --rm tests
```

## Local commands

Backend, with Postgres already accepting connections at `127.0.0.1:5432` and a `todo` role:

```bash
cd server
uv run pytest
```

Frontend:

```bash
cd web
npm test
npm run test:coverage
npm run build
```

End-to-end tests call the Compose web port. Start the stack first, then:

```bash
cd web
npx playwright install chromium
npm run test:e2e
```

## Layout

- `server/` FastAPI, SQLAlchemy, Alembic, pytest
- `web/` React and Vite, Vitest, Playwright
- `compose.yaml` Postgres 18.6, the API, and the web server
- `_bmad-output/` BMAD planning and the implementation spec
- `docs/qa/` coverage, accessibility, performance, and security notes
- `docs/ai-integration-log.md` how the work was done with agents
