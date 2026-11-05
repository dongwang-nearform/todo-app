# Coverage

Measured 4 November 2026. The gate is 70% line coverage on each suite. Generated `web/src/api/client.ts` and `web/src/main.tsx` are excluded. Playwright is not part of these percentages.

| Suite | Command | Result |
| --- | --- | --- |
| API | `cd server && uv run pytest` | 12 passed, 94.52% lines |
| API in Compose | `docker compose --profile test run --rm tests` | 12 passed, 93.66% lines |
| Web unit and component | `cd web && npm run test:coverage` | 13 passed, 76.08% lines, 73.94% statements, 73.38% functions |

The Compose run is a little lower because that image does not contain `web/dist`, so the static-file branch in `server/app/main.py` is not taken.

## Gaps

- `server/app/parsing.py` is 66%. The uncovered lines are invalid date and time strings that the HTTP tests only hit in part.
- `GET /api/health` returning 503 is untested. The suite only sees a live database.
- Web coverage is thin on the create-list failure path, the alarm field, and delete-from-the-editor. The Playwright file covers create, complete, delete, the empty day, and a rejected save through the browser.
