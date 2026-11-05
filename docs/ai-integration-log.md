# AI integration log

This log covers the BMAD pass that produced the app in this repo, and the later pass that added tests, Docker, and the QA notes. Dates are 4 November 2026.

## Agent usage

- BMAD product, architecture, UX, and epic skills wrote the planning artifacts under `_bmad-output/planning-artifacts/`. The epics file is final. The PRD, architecture spine, UX documents, and product brief were still drafts when the test and deploy work started.
- `bmad-build` implemented the app in `server/` and `web/` from `spec-todo-app.md`. The spec is `done`.
- A review inside that build found a path traversal in the static-file route, a boolean priority that became `1`, nested sub-to-dos that the list did not render, and move-up/down that could cross lists. Those were patched in the same build and covered by the existing pytest run (11 tests, then 12 after the health check).
- The test, Docker, coverage, accessibility, and security work in this pass was done in the same chat as the build, after the user approved proceeding without further questions. QA was not present during feature code. That is a real gap relative to the assignment's "QA from day one" line, and it is why this pass exists.

## MCP and tools

- The IDE browser was used to walk Today, Lists, partial, nested sub-to-dos, copy confirm, and the period "No date" section at phone width and desktop width.
- Docker was not installed during the first build. Tests ran against Homebrew PostgreSQL 18.6. Docker Compose v5.6.1 was installed later and is what `docker compose up` uses.
- No Postman MCP session was used. API checks are pytest with FastAPI's test client.

## Test generation

- Story acceptance criteria were Given/When/Then. They were not split into unit, integration, and end-to-end sections. There is no Test Architect module in this BMAD install, so that split was not produced by a skill.
- The implementation added pytest for the HTTP matrix, then Vitest for pages and the editor, then five Playwright journeys: empty state, create, complete, delete, and a rejected save. An axe scan of the main screens rides with the Playwright file.
- Generated tests miss the copy-confirm race, alarm-without-time through the UI, and a real second browser session. The API tests cover alarm-without-time and copy.

## Debugging

- Pytest could not connect until Homebrew Postgres was started and the `todo` role existed.
- The frontend catch-all joined the request path onto `web/dist` and could leave that directory with `..`. The fix resolves the path and serves the file only when it stays inside `web/dist`.
- Pydantic treated JSON `true` as priority `1`. A validator rejects booleans before that coercion.
- Clearing a date input used to send an empty query and show "Couldn't save." The pages now ignore an empty date.

## Limitations

- Story 4.1 in the final epics file still says the period screen adds no region for undated rows. The UX document and the app show a "No date" section. The epics file was left for `bmad-correct-course` rather than edited inside the build.
- SQLAlchemy 2.1.8 requires Python 3.11 or newer. The machine used 3.12. The image uses 3.12.
- Coverage excludes the generated OpenAPI client and `main.tsx`. The server suite is about 95% line coverage. The Vitest suite is about 76% line coverage. Playwright is not included in those percentages.
- Human judgment was required for the scope decision: keep this larger app, because the assignment allows a different product when the method is followed, instead of cutting back to the short reference PRD.
