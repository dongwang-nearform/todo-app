---
title: 'Todo App'
type: 'feature'
created: '2026-11-04'
status: 'done'
route: 'dispatch'
baseline_commit: 'NO_VCS'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/epics.md'
  - '{project-root}/_bmad-output/planning-artifacts/architecture/architecture-bmad-example-todo-2026-11-04/ARCHITECTURE-SPINE.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-bmad-example-todo-2026-11-04/EXPERIENCE.md'
  - '{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-bmad-example-todo-2026-11-04/DESIGN.md'
  - '{project-root}/_bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/addendum.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repository has planning contracts and no product. Tom cannot open a site, keep lists, or run a Saturday from Today.

**Approach:** Build the full v1 in `server/` and `web/`: one FastAPI process, PostgreSQL, and a Vite React client. Stories 1.1 through 4.1 in `epics.md` are the acceptance contract. `ARCHITECTURE-SPINE.md` is the technical contract. `DESIGN.md` and `EXPERIENCE.md` are the look and behavior contract. Where Story 4.1 says the period screen adds no region for undated rows, `EXPERIENCE.md` wins: dated rows first, then a "No date" list.

## Boundaries & Constraints

**Always:**
- Versions: Python >=3.10, FastAPI 0.162.0, PostgreSQL 18.6, SQLAlchemy 2.1.8, Alembic 1.20.1, Vite 8.3.5, React 19.3.1, @vitejs/plugin-react 6.2.1. TypeScript is whatever the Vite React starter installs.
- Layered. The browser calls only the generated OpenAPI client. Routers call services. Services are the only SQLAlchemy callers and the only writers. JSON is snake_case. Errors are `{ "detail": string }`.
- Production shape: one origin, FastAPI serves the built frontend and does not render product HTML. Interactive API docs off. Local development may use the Vite dev server plus the API.
- Local PostgreSQL comes from a Compose file in the repo. No cloud host.
- One dataset, no account table, no sign-in. Priority 1–5, 5 highest. State is `not_done`, `partial`, or `done`. Partial stores notes and no progress number. The server never creates a to-do on its own. `copy_confirmed` hides a copy until confirm. `alarm_at` is stored and shown, and rejected when `at_time` is null. No alarm is fired. Times are a date plus a time of day, no timezone. Today requires `on_date` from the browser. A week is Monday through Sunday containing the anchor.
- The site opens on Today. Below 768px, one column and the editor replaces the list. At 768px and above, a nav column, one reading column, and the editor beside the list. Tokens come from `DESIGN.md`. No component library and no downloaded font.
- Tables and columns appear with the story that first needs them, in story order.

**Never:**
- Sign-in, accounts, calendar routes, add-to-calendar actions, create-from-calendar, alarm delivery, a progress number, or a "quick to finish" field.
- A second to-do type in the browser. Hand-renamed JSON fields. A router that writes the database.
- Editing `_bmad/`, `.agents/`, or files under `_bmad-output/planning-artifacts/`.
- Inventing a dark theme, a recommended-row treatment, or a place for undated rows other than the "No date" list.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Open site | No session | Today, no sign-in, docs off | N/A |
| Lists | Create, rename, empty name | Named lists appear; empty name rejected | `{ "detail": string }` |
| Create to-do | Title and priority 1–5 | Row on that list, `not_done`, `copy_confirmed` true, position order. 5 outranks 1. Nothing is preselected. | Missing title, missing priority, or priority outside 1–5 rejected |
| Update and delete | Title, priority, position; delete to-do; delete list | List matches the write. Delete list removes its to-dos only. | Unknown id rejected; bad priority leaves the stored value |
| Done and partial | `done`, `not_done`, `partial` plus notes | Words "done" and "partial". No percent. Notes remain. Partial can return to either other state. | Any other state rejected |
| Time and alarm | `on_date`, `at_time`, `alarm_at` | Saturday clocks can be stored. No timezone. Alarm shown, never fired. | Bad formats rejected. `alarm_at` rejected when `at_time` is null. |
| Sub-to-dos and person | `parent_id` on the same list; `person_name` | Sub-to-do shown with parent. Delete parent deletes sub-to-dos. Mark-done-and-create stays available. Name is text, with no account. | Missing or cross-list parent rejected |
| Today and not-done | `on_date`; states | Today is confirmed rows for that date in position order, plus `next_todo_id` (first not `done`, partial allowed). Not-done is confirmed, not `done`, any date or none. | Missing `on_date` rejected |
| Copy | Source list, destination, `on_date`, then confirm | Pending rows invisible on lists and views. Confirm shows them on that date only. Second confirm does not duplicate. A later date stays empty. | Missing list or bad date rejected |
| Period | `grain` day, week, month, or year, plus `anchor` | Dated confirmed rows in the period. Undated confirmed rows under the heading "No date". | Bad grain or anchor rejected |

</frozen-after-approval>

## Code Map

- No `server/` or `web/` tree exists. Do not reuse or modify `_bmad/`, `.agents/`, or `_bmad-output/planning-artifacts/`.
- `epics.md` — story acceptance, Stories 1.1–4.1. Story 4.1's "no undated region" line is superseded by the frozen intent.
- `ARCHITECTURE-SPINE.md` — routes, fields, module paths, versions.
- `EXPERIENCE.md` and `DESIGN.md` — surfaces, copy, landing, width, tokens.
- New code lives only under `server/` and `web/`, plus a repo-root Compose file for PostgreSQL 18.6.

## Tasks & Acceptance

**Execution:**
- [x] `compose.yaml` -- PostgreSQL 18.6 for local runs -- the host is not chosen
- [x] `web/` -- Vite React starter at the bound versions; TypeScript as the starter installs it -- Story 1.1
- [x] `server/app/` -- FastAPI 0.162.0 app, same-origin built frontend, docs off, no auth or calendar routes -- Story 1.1
- [x] `server/app/models.py`, `server/app/schemas.py`, `server/alembic/` -- tables only as each story needs them; services are the only writers -- spine
- [x] `server/app/routers/lists.py`, `server/app/services/lists.py`, `web/src/features/lists/` -- list collection, create, rename -- Story 1.2
- [x] `server/app/routers/todos.py`, `server/app/services/todos.py`, `web/src/features/todo-editor/` -- create, update, delete, state, time, alarm, sub-to-dos, person name -- Stories 1.3–1.10
- [x] `web/src/api/` -- generated OpenAPI client; the only to-do type; snake_case kept -- spine
- [x] `server/app/routers/views.py`, `server/app/services/views.py`, `web/src/features/today/`, `web/src/features/not-done/`, `web/src/features/period/` -- Today, not-done, period with the "No date" list -- Stories 2.1, 2.2, 4.1
- [x] `server/app/routers/copies.py`, `server/app/services/copies.py`, `web/src/features/copy/` -- copy, hide until confirm, confirm once -- Stories 3.1, 3.2
- [x] `server/tests/` -- one test module per service, covering the I/O matrix -- the matrix is the unit and integration contract

**Acceptance Criteria:**
- Given the bound starter and a local Postgres, when Tom opens the site, then he lands on Today, is not asked to sign in, and finds no calendar or alarm-delivery route.
- Given Stories 1.2 through 4.1, when each story's acceptance in `epics.md` is exercised, then it passes, except the period screen shows undated confirmed to-dos under "No date".
- Given phone width and a width of at least 768px, when the same flows run, then both widths can complete them.
- Given `DESIGN.md`, when a row shows priority, partial, done, or Next, then the word or numeral is present and pine is not used as a "do this" marker.

## Implementation Notes

- 2026-11-04: `uv run pytest` in `server/` — 11 passed. Each I/O matrix row has a covering test that ran. `npm run build` in `web/` exited 0.
- Docker is not installed, so `docker compose up -d` did not run. Tests used Homebrew PostgreSQL 18.6 on localhost, which is the version `compose.yaml` pins.
- SQLAlchemy 2.1.8 requires Python >=3.11. This machine is 3.12. The spec's 3.10 floor is not what the pinned SQLAlchemy accepts.
- Routers do not open a database session. The index route renders Today. The period page renders a "No date" section.
- 2026-11-04 review: patches applied for the Postgres 18 volume and localhost bind, dist path containment, boolean priority, nested sub-to-dos, same-list reorder, period date order, empty date, confirm-while-loading, and done-text contrast. `uv run pytest` — 11 passed. `npm run build` exited 0. Docker is still not installed, so Compose was not started. Browser check on the running site: Today, a new list, partial with notes, a nested sub-to-do, copy confirm, the period "No date" section, an ignored empty date, phone width as one column, and desktop width with the editor beside the list. `/docs` and `/redoc` return 404. Nothing was deferred.

## Spec Change Log

## Review Triage Log

- medium — `compose.yaml` Postgres 18 volume at `/var/lib/postgresql/data` does not persist. The image keeps data under `/var/lib/postgresql`. The same finding's missing app service is not a defect: the spec's Compose file is the database only.
- low — `compose.yaml` publishes `5432` on every interface with the local `todo` password. Binding to localhost is the direct correction. The password itself matches the local database the spec asked for.
- high — `server/app/main.py` `frontend()` serves `web/dist / full_path` when `is_file()` is true, and `..` is not confined to `web/dist`.
- low — rejected. Pending copies stay invisible until confirm, which is the spec. A resume or cancel screen is more than a direct correction, and the review page is the confirm path.
- medium — `create_copy` copies source `position` values, so destination rows can interleave. The parent-missing abort is the right failure when that parent was not copied.
- low — rejected. Confirm stays visible during load; that part is patched with the button disable below. Copy review is not required to show the destination name, and unconfirmed rows are not required to open the editor.
- medium — `grouped()` renders one level. A sub-to-do of a sub-to-do is stored and then omitted.
- medium — `move()` treats every row with the same `parent_id` as a sibling, including other lists, and equal positions can become `0`.
- medium — `grouped()` sorts only by `position`, so a period's dated rows leave the date order the API returned. Today already has a date control, so "Today never shows the date" is not true.
- medium — clearing the date input sets an empty `on_date` or `anchor`, the request fails, and the page says it couldn't save.
- low — `#78716C` on `#F7F6F3` is just under 4.5:1. The correction is a darker done color in the stylesheet.
- low — rejected. Escape closing an unsaved editor without a second confirm is the experience contract. Focus return and `aria-busy` add complexity for a case everyday use does not depend on.
- medium — `TodoCreate` accepts `priority: true` and stores it as `1`.
- medium — same cross-list reorder as the `move()` row above. Not a separate defect.

## Design Notes

Routers stay thin. A rule such as priority range, copy visibility, or alarm-without-time lives in the matching service. The period feature reads `undated` from `GET /api/views/period` and renders it under the dated rows. It does not drop the array and it does not paint undated rows onto a day cell.

## Verification

**Commands:**
- `docker compose up -d` -- expected: PostgreSQL 18.6 accepts connections
- `cd server && uv run pytest` -- expected: I/O matrix tests pass
- `cd web && npm run build` -- expected: the Vite build exits 0

**Manual checks (if no CLI):**
- Phone width and desktop width both open Today, create a list and a to-do, mark partial, copy and confirm, and show "No date" on a period view.
