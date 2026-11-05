# Version reality-check — architecture spine

Verdict: **pass**

Reviewed: `ARCHITECTURE-SPINE.md` (Stack table, AD-10, AD-11, Structural Seed) against `.memlog.md` and the repo. Spine not edited. Brownfield: no starter live-defaults apply. The spine ratifies `server/`, `web/`, `compose.yaml`, and the two Dockerfiles; it does not claim the pins are upstream-latest.

Checked 2026-11-05. Every Stack row and every Docker/Compose claim below was confirmed against the named file. Where the memlog only recorded a Dockerfile string for a floating tag, this review also checked the live tag.

## Stack table

| Name | Spine | Repo | Memlog | Result |
| --- | --- | --- | --- | --- |
| Python | 3.12 | `server/Dockerfile`: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` and `python:3.12-slim-bookworm`. `server/pyproject.toml` and `server/uv.lock` `requires-python` are `>=3.11`. Structural Seed states both. | 2026-11-05, Dockerfile | Match |
| FastAPI | 0.162.0 | `pyproject.toml` `==0.162.0`. `uv.lock` 0.162.0, PyPI upload 2026-10-23. | 2026-11-04 PyPI; lock ratified 2026-11-05 | Match |
| uvicorn | 0.54.0 | Manifest `>=0.32`. `uv.lock` 0.54.0, upload 2026-09-25. | 2026-11-05 PyPI and lock | Match (lock resolution) |
| PostgreSQL | 18.6 | `compose.yaml` `postgres:18.6` | 2026-11-04 stable minor (19 GA planned 2026-11-19); file rechecked 2026-11-05 | Match |
| SQLAlchemy | 2.1.8 | `pyproject.toml` `==2.1.8`. `uv.lock` 2.1.8, upload 2026-11-04. | 2026-11-04 GitHub release | Match |
| psycopg | 3.3.8 | Manifest `psycopg[binary]>=3.2`. `uv.lock` 3.3.8 and `psycopg-binary` 3.3.8, including `cp312` manylinux and musllinux wheels for the 3.12 image. Upload 2026-11-04. No direct `psycopg` import under `server/`. | 2026-11-05 lock | Match (lock resolution). Fits Python 3.12. |
| Alembic | 1.20.1 | `pyproject.toml` `==1.20.1`. `uv.lock` upload 2026-10-22. `server/docker-entrypoint.sh` runs `alembic upgrade head` before uvicorn. | 2026-11-04 PyPI and changelog | Match. Memlog says released 2026-10-21; the lock upload is 2026-10-22. The spine pins the version, not the date. |
| Node | 22 | `web/Dockerfile` `node:22-alpine` | 2026-11-05 Dockerfile string only | Match. Live Node 22 line is 22.23.4 (2026-10-21). That satisfies Vite and `@vitejs/plugin-react` `^20.19.0 \|\| >=22.12.0`, Vitest `^22.12.0 \|\| ^24.0.0 \|\| >=26.0.0`, and jsdom’s transitive `@asamuzakjp/*` engines `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0`. |
| nginx | 1.27 | `web/Dockerfile` `nginxinc/nginx-unprivileged:1.27-alpine`. `web/nginx.conf` listens on 8080 and proxies `/api/` to `http://api:8000`. | 2026-11-05 Dockerfile string only | Match. Tag `1.27-alpine` still resolved on 2026-10-24. Upstream docs keep the `nginxinc` registry for releases before 1.31.7 mainline, so this tag is on the registry the Dockerfile names. |
| Vite | 8.3.5 | `web/package.json` exact. `package-lock.json` 8.3.5. | 2026-11-04 npm | Match. Peer of the React plugin (`vite: ^8.0.0`) and of Vitest (`^6.4.0 \|\| ^7.0.0 \|\| ^8.0.0`). |
| React | 19.3.1 | `package.json` and lock, `react` and `react-dom` 19.3.1. | 2026-11-04 plugin peer `react ^19.3.1`, then bound; lock holds the exact version | Match |
| react-router-dom | 7.18.5 | `package.json` exact. Lock 7.18.5 (`react-router` 7.18.5). Engines `node >=20`. | 2026-11-05 npm and lock | Match |
| @vitejs/plugin-react | 6.2.1 | `package.json` exact. Lock 6.2.1. | 2026-11-04 npm | Match |
| TypeScript | 6.0.3 | Manifest `~6.0.3`. Lock 6.0.3. | 2026-11-05 npm and lock | Match (lock resolution) |
| Vitest | 5.1.0 | Manifest `^5.1.0`. Lock 5.1.0. `package.json` script `test` is `vitest run`. | 2026-11-05 npm and lock | Match (lock resolution) |
| @playwright/test | 1.64.1 | Manifest `^1.64.1`. Lock 1.64.1, plus `playwright` and `playwright-core` 1.64.1. Engines `node >=20`. | 2026-11-05 npm and lock | Match (lock resolution) |
| pytest | 9.2.0 | Manifest `>=8`. `uv.lock` 9.2.0, upload 2026-10-27. `server/Dockerfile` test stage `CMD ["pytest", "-q"]`. | 2026-11-05 PyPI and lock | Match (lock resolution) |

No Stack row is a training-data assertion. Each one is either a 2026-11-04/05 memlog registry check, a lockfile/Dockerfile check, or both, and this review re-read the files.

## Docker and Compose claims

| Claim | Evidence | Result |
| --- | --- | --- |
| Images are `server/Dockerfile` targets `build`, `test`, `runtime`, and `web/Dockerfile` | Both files. Server stages are named `build`, `test`, `runtime`. Web has a `build` stage and an untagged nginx runtime. | Match |
| Compose services are `postgres`, `api`, `web`, `tests` | `compose.yaml` | Match |
| Only profile is `test`, and only `tests` uses it. Default stack is `postgres`, `api`, `web` | `tests.profiles: ["test"]`. No other profile. | Match |
| Published host ports bind `127.0.0.1`. API port is not published | Postgres `127.0.0.1:${POSTGRES_PORT:-5433}:5432`. Web `127.0.0.1:${WEB_PORT:-8080}:8080`. `api` has no `ports`. | Match |
| Profile `test` uses database `todo_test` and does not use the dev database | `tests.environment.DATABASE_URL` ends in `/todo_test`. `api` uses `/todo`. `server/docker/init-test-db.sql` creates `todo_test`. | Match |
| No cloud provider | No other compose file, Dockerfile, or cloud app manifest in the repo. | Match |
| API container and runtime image healthcheck call `GET /api/health` | `compose.yaml` `api.healthcheck` and `server/Dockerfile` `HEALTHCHECK` both `urlopen` `http://127.0.0.1:8000/api/health`. | Match |
| uvicorn listens on 8000 after `alembic upgrade head` | `server/docker-entrypoint.sh` | Match |
| nginx serves the built frontend and proxies `/api` to the API | `web/Dockerfile` copies `dist` to `/usr/share/nginx/html`. `web/nginx.conf` `try_files` plus `proxy_pass http://api:8000`. | Match |
| FastAPI serves `web/dist` only when that directory is present | `server/app/main.py` `DIST = parents[2] / "web" / "dist"`, mounted only if `DIST.is_dir()`. The runtime image does not copy `web/dist`; Compose serves the UI from nginx. The conditional claim holds. | Match |
| Local Vite proxies `/api` to `127.0.0.1:8000` and is not a second published product host | `web/vite.config.ts`. Compose publishes only the web container for the product origin. | Match |
| Playwright runs against the Compose web origin | `web/playwright.config.ts` `baseURL` defaults to `http://127.0.0.1:8080`, the published web port. | Match |
| Generated client calls relative `/api` paths | `web/src/api/client.ts` paths are `/api/...`. No embedded host. | Match |
| Interactive API docs are off | `server/app/main.py` `docs_url=None`, `redoc_url=None`, and `/docs` and `/redoc` return 404. | Match |

## Fit of named technologies

- FastAPI 0.162.0, SQLAlchemy 2.1.8, Alembic 1.20.1, and psycopg 3.3.8 are co-locked. psycopg 3.3.8 publishes CPython 3.12 wheels, so the runtime image tag fits the driver.
- Vite 8.3.5, `@vitejs/plugin-react` 6.2.1 (peer `vite ^8`), React 19.3.1 (plugin peer `react ^19.3.1`), and Vitest 5.1.0 (peer `vite ^8`) agree.
- `react-router-dom` 7.18.5 is the page router named in Consistency Conventions. Its lock engines accept Node 22.
- PostgreSQL 18.6 is the image the Compose file runs. The 2026-11-04 memlog check that 19 was still pre-GA remains inside its stated window (GA planned 2026-11-19; this review is 2026-11-05).

## Starter defaults

Not applicable. Brownfield. The spine does not adopt `create-vite` or a FastAPI starter; the versions are the lockfiles and image tags already in the repo.

## Notes that do not fail

1. **Lock resolution versus manifest pin (low).** uvicorn `>=0.32`, psycopg `>=3.2`, pytest `>=8`, TypeScript `~6.0.3`, Vitest `^5.1.0`, and `@playwright/test` `^1.64.1` are ranges. The Stack numbers match `uv.lock` and `package-lock.json` today. The next unlock can move them without a spine edit. They are not currently wrong, and the memlog records the lock check.
2. **Floating image tags (low).** `node:22-alpine`, `python:3.12-slim-bookworm`, `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`, and `nginxinc/nginx-unprivileged:1.27-alpine` float inside the version the spine names. The memlog checked the Dockerfile text. This review checked the Node 22 line (22.23.4) against the lockfile engines and confirmed the nginx 1.27 tag still exists on the registry the Dockerfile uses. `postgres:18.6` is a minor tag, not a floating major.
3. **Alembic date in the memlog.** “released 2026-10-21” versus lock upload `2026-10-22T03:24:35Z`. The spine version 1.20.1 matches the lock. No spine change.
4. **Transitive libraries are not stack rows.** Locked pydantic 2.14.2 and starlette 1.10.0 are FastAPI dependencies. The spine names Pydantic only as the JSON naming source. It does not pin them. That is consistent with ratifying the direct stack.

## Conclusion

The committed versions and the Docker/Compose topology were reality-checked against the repo, and the memlog records a registry or file check for each Stack row. Re-reading the lockfiles, Dockerfiles, Compose file, entrypoint, nginx config, Vite proxy, and Playwright base URL found no contradiction. Nothing in the spine is an unchecked version that needs to be replaced.
