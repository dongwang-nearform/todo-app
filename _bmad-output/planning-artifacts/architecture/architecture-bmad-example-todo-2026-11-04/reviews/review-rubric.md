# Rubric review — Architecture Spine (Todo App)

- **Artifact:** `ARCHITECTURE-SPINE.md`
- **Lens:** good-spine checklist (feature altitude, build substrate)
- **Evidence:** this file only. The PRD, addendum, README, `compose.yaml`, and the repo were not opened. Currency of Stack pins and brownfield ratification are judged only from what this spine asserts.
- **Verdict:** **fix**

The spine decides the right class of things for a feature altitude: one dataset, inward dependencies, one shipped origin, server-owned product rules, a closed HTTP surface, display-only alarms, one health probe, and a closed Compose/test path. Those are real divergence points, and most of the rules can be checked.

It is not handoff-ready. One deferral leaves the landing screen’s calendar day open. Three adopted rules contradict each other or their own contract. Sub-to-do visibility and list ordering are still free for the next level to invent. Configuration is a silent operational dimension.

## Checklist

| Check | Result |
| --- | --- |
| Fixes the real divergence points for the level below and misses none | **Fail.** Sub-to-do visibility, parent/list integrity, list `position`, copy-onto-existing positions, and not-done/period sort are unset. |
| Every AD Rule is enforceable and actually prevents its stated divergence | **Fail.** AD-1, AD-5, and AD-11 do not hold as written. AD-3’s “one origin” is looser than its Prevents. |
| Nothing under Deferred could let two units diverge | **Fail.** Which timezone “today” uses is still open, and it changes FR-2. |
| Named tech is verified-current or ratified from the existing project | **Inconclusive.** Pins are specific and internally consistent. This review did not check registries or lockfiles. nginx `1.27` and Node `22` are the only rows without a patch. |
| Ratifies rather than contradicts a brownfield codebase | **Inconclusive.** Scope says the shipped repo, and sources cite `README.md` and `compose.yaml`. Nothing in the spine names a file it is overriding. Not re-checked against the tree. |
| Covers the driving spec’s capabilities | **Pass on the spine’s own ids.** `binds` is FR-1–FR-13 and FR-15–FR-17. Each of those appears in the capability map. FR-14 is withdrawn and mapped to “no route”. The PRD was not opened, so a capability that never received an FR id would not show up here. |
| Inherited parent ADs are not weakened | **N/A.** No parent spine. `companions: []`. |
| Every owned dimension is decided, deferred, or an open question | **Fail.** Deployment, environments, and provider strategy are decided (Compose on one machine, `127.0.0.1`, no cloud, `test` profile / `todo_test`). Runtime configuration and operational signals other than the health probe are neither decided nor deferred. |

No Open Questions section exists. Deferred is doing two jobs, and one of those jobs is a live fork.

## Findings

### F1 — critical — “Today” timezone is deferred and still forks the landing feature

- **Where:** Deferred, first bullet; Consistency Conventions “Time”; `GET /api/views/today` and `GET /api/views/period`.
- **Check:** Deferred must not let two units diverge.
- **Defect:** The spine stores no zone, then refuses to say whose calendar day “today” is. `on_date` and `anchor` are caller-supplied, so the server will faithfully implement whatever date each client sends. The Today feature, the period feature, and Playwright can each pick local time, UTC, or the container clock. Near midnight they disagree by a day, which is a different to-do set on the screen the spine sets as `/`.
- **Why the deferral reason fails:** “So a zone is not invented here” is an argument for a decision (browser-local civil date in, no zone column, server does not read a clock to choose the day). It is not a reason the choice can wait.
- **Disposition:** autofix.
- **Fix:** Delete that Deferred bullet. Add a rule: the browser’s local calendar date is the only definition of today and of the period anchor; the server stores and filters `YYYY-MM-DD` and never derives “today” from its own clock; tests pin that date explicitly rather than reading container localtime.

### F2 — high — The local dev loop and the Compose port rule cannot both be true

- **Where:** AD-11 Rule; Structural Seed, paragraph beginning “Compose is the ship path.”
- **Check:** Rule prevents its stated divergence; environments are actually decided.
- **Defect:** AD-11 says published host ports bind to `127.0.0.1` and the API port is not published. The seed says a local Vite server proxies `/api` to `127.0.0.1:8000`. An unpublished Compose API is not on that address. The spine never says a host-run uvicorn is the process Vite is allowed to call.
- **Consequence:** One epic wires Vite at the host port and another honors “API port is not published.” One of those builds does not start.
- **Disposition:** autofix.
- **Fix:** State the two runtimes in one rule. Either Compose publishes `127.0.0.1:8000` for the API and the “not published” sentence is wrong, or Vite talks only to the web origin (nginx `/api`) and the `127.0.0.1:8000` sentence is wrong, or host-run uvicorn on `127.0.0.1:8000` is an allowed dev process and Compose still does not publish the API. Pick one.

### F3 — high — AD-1’s single database contradicts AD-11’s test database

- **Where:** AD-1 Rule; AD-11 Rule (“Profile `test` uses database `todo_test`”).
- **Check:** Rule is enforceable and matches its Prevents.
- **Defect:** AD-1’s Prevents is phone and desktop keeping different to-dos. Its Rule says one PostgreSQL database holds every to-do. AD-11 then requires a second database, `todo_test`, that must not touch the dev database. Both rules are adopted. A builder can satisfy either one.
- **Consequence:** Shared-database tests, or a refusal to add `todo_test`, both cite an adopted rule.
- **Disposition:** autofix.
- **Fix:** Narrow AD-1 to one database per running environment, shared by every client of that environment. Keep `todo_test` as the test environment’s database. The Prevents stays about clients, not about dev versus test.

### F4 — high — AD-5 does not stop a copy from showing before confirm

- **Where:** AD-5 Rule; API Contract intro; `GET /api/todos/{todo_id}`.
- **Check:** Rule prevents its stated divergence.
- **Defect:** Prevents says a pending copy must not exist only in one browser, and must not show up before confirm. The Rule hides the copy from lists and views only. `GET /api/todos/{todo_id}` returns “the to-do, including an unconfirmed copy.” The editor feature is a normal caller of get-by-id. Confirm’s dedicated read is already `GET /api/copies/{copy_id}`.
- **Consequence:** The editor epic renders pending copies; the view epics hide them. That is the split AD-5 names.
- **Disposition:** autofix.
- **Fix:** `GET /api/todos/{todo_id}` returns only `copy_confirmed` true (404 otherwise). Unconfirmed rows are readable only through `GET /api/copies/{copy_id}`. If get-by-id must return them, change the Prevents line so it no longer claims the copy cannot show before confirm, and name the editor as an allowed reader. The first fix matches the Prevents that is written.

### F5 — high — Sub-to-dos are a write-side field with no read-side or integrity rule

- **Where:** AD-4 (binds FR-10, Rule never mentions `parent_id`); `POST /api/lists/{list_id}/todos`; Views tables; capability map row “FR-10 sub-to-dos”.
- **Check:** Missed divergence for the level below; Rule does not cover a bound capability.
- **Defect:** The contract says `parent_id` creates a sub-to-do, delete cascades to sub-to-dos, and copy remaps parent links. It does not say whether today, not-done, or period include children, whether children are nested or flat, whether `parent_id` must be a row on the same `list_id`, or whether a cycle or a second level is rejected. AD-4 is the cited governor and its Rule is silent on all of that.
- **Consequence:** The lists epic and the three view epics will each pick a shape. Copy will remap a graph the views do not agree exists.
- **Disposition:** autofix.
- **Fix:** One rule, bound to FR-10: a sub-to-do’s `list_id` equals its parent’s; one level only; no cycles; views return sub-to-dos flat in the same array as other confirmed rows (or nested — state which); the not-done and period arrays use the same rule as today.

### F6 — medium — List order and copy positions are unspecified

- **Where:** `POST`/`PATCH /api/lists` (body is `{ name }` only; response includes `position`); `GET /api/lists/{list_id}/todos` (`position` order); `POST /api/copies` (new rows keep source `position`).
- **Check:** Missed divergence.
- **Defect:** Nothing assigns `position` on list create, and list PATCH cannot send it. To-do create is “to-do fields except ids and `copy_*`,” so `position` may be client-supplied, and nothing says it is unique per list. Copy keeps source positions onto a destination that may already have those positions.
- **Consequence:** List screens and the copy screen sort ties differently, or reject a copy the other epic accepts.
- **Disposition:** autofix.
- **Fix:** Server assigns list and to-do `position` (append). State whether copy renumbers onto the destination or fails when the destination is non-empty. Say the order is unique per list.

### F7 — medium — Not-done and period responses have no order

- **Where:** `GET /api/views/not-done`; `GET /api/views/period` (`todos` and `undated`).
- **Check:** Missed divergence. Today and list reads already pin `position` order.
- **Defect:** Those two views do not say sort. `next_todo_id` on today is defined as the first not-done row in that order, so order is load-bearing elsewhere and unset here.
- **Disposition:** autofix.
- **Fix:** Pin both arrays to the same order as list reads (`position`, and state the tie-break, even if it is `id`).

### F8 — medium — Required write fields stop at priority

- **Where:** API Contract “To-do body”; AD-4 Rule on partial.
- **Check:** AD-4’s “a write that breaks these is rejected” is not checkable for the fields it implies.
- **Defect:** Priority 1–5 and the state enum are enforceable. `title` and list `name` have no empty/blank rule. Partial “stores notes” does not say notes are required, or what happens to notes when state leaves `partial`. PATCH allows any non-id, non-`copy_*` field, including `list_id` and `state`, with no transition list.
- **Consequence:** One write path rejects a blank title or a partial without notes; another stores them. Both cite AD-4.
- **Disposition:** autofix the ones that are product rules (blank `title`, blank list `name`, notes required or not when `state` is `partial`). If any transition is illegal, say so; otherwise say any state may be patched to any other state.

### F9 — medium — Two clients, no write-conflict rule

- **Where:** AD-1 Prevents (phone and desktop share the data); no convention for concurrent PATCH.
- **Check:** The divergence AD-1 opens is not closed.
- **Defect:** Shared unauthenticated writes are the point of AD-1. Nothing says last-write-wins, row version, or reject-on-stale. The editor epic and any test epic can each invent one.
- **Disposition:** autofix. A deferral is the wrong basket: a deferred conflict policy still forks.
- **Fix:** One sentence. Last-write-wins on PATCH is enough for this scope if that is the choice. Do not leave it implied.

### F10 — medium — Playwright’s “Compose web origin” has no host

- **Where:** AD-11 Rule.
- **Check:** Rule is enforceable.
- **Defect:** Browser tests run against “the Compose web origin.” The `tests` service is on the Compose network; the published binding is `127.0.0.1` on the host. Those are different origins. The rule does not say which one Playwright opens, or that the web container is the server under test.
- **Disposition:** autofix.
- **Fix:** Name the origin the `tests` service calls (the Compose service DNS name and port), and say host `127.0.0.1` is for a browser on the machine, not for the `tests` container.

### F11 — medium — Runtime configuration and operational signals are a silent dimension

- **Where:** No section. AD-10 and AD-11 cover the probe, images, profiles, and localhost bind. Deferred’s provider bullet only pushes “a provider other than this machine” down.
- **Check:** Feature altitude owns deployment, environments, infra, and operations. A whole leftover slice left unspoken is a finding.
- **What is already decided:** Compose is the ship path; services are `postgres`, `api`, `web`, plus `tests` on profile `test`; web is the published origin; API port is not published (see F2); health is `GET /api/health`; boot runs `alembic upgrade head`; no cloud provider.
- **What is silent:** where the database URL and credentials come from (env in Compose versus hardcoded), which environment names exist beyond dev and `todo_test`, logging, and what happens to data on a new machine (no backup is a valid decision only if it is written). Schema change is a boot command, not a closed rule, so `create_all` and a hand-written migration both still fit.
- **Disposition:** autofix the config sentence; defer logging and backup only by naming them under Deferred with a reason that does not leave two connection strings in play.
- **Fix:** Compose environment is the only config source; one database URL per environment; product code does not embed a DSN. Schema changes ship as Alembic revisions only. Then one Deferred line each for log format and for backup, if those can actually wait.

### F12 — low — AD-3 allows a second product host while forbidding one

- **Where:** AD-3 Rule; Structural Seed (“FastAPI also serves `web/dist`”).
- **Check:** Prevents says “a second host.”
- **Defect:** nginx on the web container is the shipped origin, and FastAPI also serves `web/dist` when that directory is present. AD-11’s unpublished API port keeps the second server off the host, so this does not fork clients today. The Rule still describes two servers that can render the product.
- **Disposition:** autofix or ignore. Prefer a single clause: FastAPI serving `web/dist` is a dev convenience and is not a second origin in the Compose ship path; the browser origin remains the web container. Ignore if F2’s port fix already makes that obvious.

### F13 — low — Empty DELETE bodies and generated-client drift are unspecified

- **Where:** DELETE list and DELETE to-do (“empty”); AD-7 and Consistency Conventions “Client calls”; AD-11 ship/test path.
- **Defect:** “Empty” can be 204 or 200 with `{}`. `web/src/api` is “generated” but no ship or test step regenerates it or forbids a hand edit. Both are smaller than F4–F5 because AD-6 already closes the route list and AD-7 forbids a second to-do type.
- **Disposition:** autofix if cheap (204, and the generated client is produced from the server OpenAPI and not edited by hand). Otherwise ignore until an epic touches deletes or the client.

### F14 — low — Stack patch pins are uneven

- **Where:** Stack table.
- **Check:** Named tech verified-current or ratified.
- **Defect:** No in-spine contradiction among the pins. nginx is `1.27` and Node is `22`, with no patch, while every other row has one. This review did not re-check PyPI, npm, or the repo, so it does not call the pinned rows stale or invented.
- **Disposition:** ignore for the rubric verdict. Re-verify outside this review before treating the table as ratified.

## Deferred items that are safe

- **Working title.** Does not change a module boundary.
- **Ballet pickup at 2:30pm versus the lesson end.** The spine classifies this as a product assumption. `next_todo_id` is the first not-done row in `position` order, not a time comparison, so this assumption does not fork storage or the next-item query. Leave it.
- **A provider other than the machine that runs Compose.** AD-11 already decides there is no cloud provider. This bullet does not reopen that decision.
- **Authentication and calendar.** Already prohibited by AD-4 and AD-6. Repeating them under Deferred does not create a fork. Ignore the duplication.

## What is already solid

- AD-2 plus the health exception is a checkable dependency rule. Product routers do not own SQL; `routers/health.py` is the named `SELECT 1` exception.
- AD-6’s route table is closed: lists, to-dos, today, not-done, period, copy, confirm, health. Sign-in, calendar, alarm delivery, and a progress number are explicitly absent. Error envelope for product routes is `{ "detail": string }`. Health’s body is carved out in AD-10.
- AD-8 and the period response agree: dated rows in the period, undated confirmed rows in a separate `undated` set, heading “No date”, not painted onto a day. Week is Monday–Sunday. This one is enforceable.
- AD-9 is enforceable: `alarm_at` is stored and shown, rejected when `at_time` is null, and nothing fires it.
- AD-10 is enforceable: one URL, two bodies, 200 and 503, called from the API image healthcheck.
- AD-11’s closed set of images, services, and the `test` profile is the right shape once F2, F3, and F10 are aligned with it.
- FR-14 is the one bound-list exception, and both the map and Deferred send it to “no route.”

## Verdict

**fix.** Apply F1–F5 before epics are cut. F6–F11 are the same pass if the edit is already open; they are how the remaining forks sneak back in. F12–F14 do not block.
