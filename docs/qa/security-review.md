# Security review

Reviewed 4 November 2026 against the app in `server/` and `web/`. Scope is the running product: one user, no accounts, local Docker, and the browser UI.

## Findings

| Item | Result |
| --- | --- |
| SQL injection | Queries go through SQLAlchemy bound parameters. List and to-do text is stored as data, not concatenated into SQL. |
| Cross-site scripting | Titles, notes, names, and errors are rendered as React text. There is no `dangerouslySetInnerHTML`. |
| Path traversal | `GET /{path}` used to serve any file `web/dist / path` could resolve, including paths with `..`. The handler now resolves the candidate and serves it only when it is a file inside `web/dist`. Anything else receives `index.html`. |
| Mass assignment | Create and patch models ignore unknown fields. Priority rejects booleans and values outside 1–5. Alarm time is rejected when the to-do has no time of day. |
| Authentication | There is none, by product decision. Anyone who can reach the port can read and change the data. Compose publishes the site and Postgres on `127.0.0.1` only. |
| Secrets | The database password `todo` is the local default in Compose, Alembic, and the test fixture. It is not a production credential. Do not reuse it on a reachable host. |
| Interactive API docs | `/docs` and `/redoc` return 404. |
| Container user | The API process runs as uid 10001. The web image is `nginxinc/nginx-unprivileged`. |

## Remediations in this tree

- Path containment in `server/app/main.py`.
- Boolean priority rejected in `server/app/schemas.py`.
- Host port bindings limited to loopback in `compose.yaml`.

No further code change came out of this review. Adding accounts is out of scope for this version.
