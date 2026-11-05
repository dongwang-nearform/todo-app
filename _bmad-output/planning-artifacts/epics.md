---
status: final
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/prd.md
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-bmad-example-todo-2026-11-04/ARCHITECTURE-SPINE.md
---

# bmad-example-todo - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for bmad-example-todo, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1: Tom can see every to-do list he created, and a second list appears as its own list.
FR-2: Tom can open Today and see that date's to-dos in list order, and he can identify the next to-do from that order.
FR-3: The not-done view shows every to-do that is not done, across all time. It includes a partial to-do and a not-done to-do from another date. It excludes a done to-do.
FR-4: Tom can open a day view, a week view, a month view, and a year view. A to-do with a time appears in the periods that contain that time, and a to-do outside the selected period does not. A confirmed to-do with no date appears under the dated rows in a section headed "No date".
FR-5: Tom can create a to-do, update its name, time, or priority, and delete it. A created to-do appears on the list he put it on. A deleted to-do no longer appears on any list or view.
FR-6: Tom can mark a to-do done, and mark a done to-do not done. Done removes it from the not-done view. Not done returns it.
FR-7: Today shows that day's to-dos in order and which one is next even when every one of them is still not done.
FR-8: Each to-do has a priority of 1, 2, 3, 4, or 5. 5 is highest. 1 is lowest. A priority outside 1 through 5 is rejected. Tom can change a priority, and the new value is what he sees.
FR-9: When more than one high-priority to-do is not done, the product does not select which one Tom must do. "Quick to finish" is his judgment and is not stored.
FR-10: Tom can add sub-to-dos to a to-do, and those sub-to-dos are visible with the to-do they belong to. Adding them does not remove mark-done-and-create-new.
FR-11: Tom can mark a to-do done and create a new to-do. He can do that instead of adding sub-to-dos, and he can add sub-to-dos instead. Neither path removes the other.
FR-12: Tom can set a time on a to-do, including an English drop-off at 9:00am, an English pickup at 10:00am, a ballet drop-off at 1:00pm, and a ballet pickup at 2:30pm.
FR-13: Tom can set an alarm on a time-bound to-do. A to-do with no time is not required to have an alarm. How far ahead the alarm fires is unstated.
FR-14: Out of scope for v1. No to-do offers an add-to-calendar action. The product does not create a to-do from a calendar event, and it does not keep a calendar.
FR-15: Tom can copy to-dos from one to-do list onto another, including onto Saturday's Today. A copy he has not confirmed does not appear on the destination. After he confirms, the copied to-dos appear. A later Saturday does not receive them unless he copies and confirms again. No other action creates a to-do without Tom creating it or confirming a copy.
FR-16: Tom can name another person, including his daughter or his wife, on a to-do. That person has no sign-in and no view of the to-do.
FR-17: Tom can mark a to-do partial and record notes, without marking it done. The state word is "partial." It shows no percent, count, or progress score. Notes are still there when he returns. A partial to-do stays in the not-done view and is distinct from done and from not started.

### NonFunctional Requirements

The PRD has no numbered non-functional section. These are the constraints written in Platform, Non-Goals, and MVP scope.

NFR-1: v1 is one responsive website. The same capabilities are usable at phone width and at desktop width. It is not a native iOS or Android app, a native desktop app, a public API, or a hardware device.
NFR-2: v1 has no authentication and no sign-in. Tom is not asked to identify himself.
NFR-3: v1 has no calendar. A to-do cannot be added to Google Calendar, Apple Calendar, or a calendar inside this product. The addendum repeats that ban and keeps the alarm.
NFR-4: The product does not automatically add to-dos. A copy does not land until Tom confirms it.

Recorded as success measures, not as build constraints: SM-1 (UJ-1 on the responsive site, including phone width), SM-2 (Saturday Today in order and what is next after copy and confirm), SM-3 (not-done view includes other-day and partial, excludes done), SM-C1 (do not optimize Saturday mark-done rate).

### Additional Requirements

Starter template: yes. The spine binds TypeScript "as installed with the Vite React starter" and does not pin a TypeScript version. That starter is the greenfield base for the web app and affects Epic 1 Story 1.

- One production process. FastAPI serves the API and the built frontend from the same origin. FastAPI does not render the product HTML. Interactive API docs are off in production. The API is not a public or third-party API.
- PostgreSQL 18.6 is the only database and runs beside that process. There is no account table. Anyone who can open the site can read and write through the app. The host and the provider are not chosen.
- Bound versions: Python >=3.10, FastAPI 0.162.0, PostgreSQL 18.6, SQLAlchemy 2.1.8, Alembic 1.20.1, Vite 8.3.5, React 19.3.1, @vitejs/plugin-react 6.2.1.
- Layered. `web` depends on the OpenAPI contract only. Routers depend on services. Services are the only callers of SQLAlchemy and the only writers. Product rules run in services.
- The web client is generated from OpenAPI into `web/src/api/`. Feature folders are `lists`, `today`, `not-done`, `period`, `todo-editor`, and `copy`. They call that client and do not declare their own to-do type. JSON is snake_case. The frontend does not hand-rename fields.
- Server modules are `routers/{lists,todos,views,copies}.py`, `services/{lists,todos,views,copies}.py`, `models.py`, and `schemas.py`. Each router calls only its matching service.
- Identifiers are integer primary keys. A to-do time is a calendar date plus a time-of-day. No timezone is stored. The browser sends `on_date` to Today. Errors are `{ "detail": string }`.
- To-do fields are `id`, `list_id`, `parent_id`, `position`, `title`, `state` (`not_done` | `partial` | `done`, default `not_done`), `priority` (required on create, 1–5), `notes`, `on_date`, `at_time`, `alarm_at` (rejected when `at_time` is null), `person_name`, `copy_id`, `copy_confirmed`. `title` is the words Tom sees.
- A normal create sets `copy_confirmed` true. UI reads return only confirmed rows, except `GET /api/copies/{copy_id}` and `GET /api/todos/{todo_id}`, which include an unconfirmed copy.
- Lists: `GET/POST /api/lists`, `PATCH/DELETE /api/lists/{list_id}`. Deleting a list deletes its to-dos.
- To-dos: `GET/POST /api/lists/{list_id}/todos`, `GET/PATCH/DELETE /api/todos/{todo_id}`. `parent_id` creates a sub-to-do. `PATCH` is how done, not done, partial, notes, priority, time, alarm, and person name are written. Deleting a to-do also deletes its sub-to-dos.
- Views: `GET /api/views/today?on_date=` returns `{ on_date, todos, next_todo_id }`. `next_todo_id` is the first confirmed to-do that day whose state is not `done`, or null, so a partial to-do can be next. `GET /api/views/not-done` returns confirmed to-dos whose state is not `done`, including partial and no date. `GET /api/views/period?grain=&anchor=` with grain `day` | `week` | `month` | `year` returns `{ grain, anchor, todos, undated }`.
- Copy: `POST /api/copies` with `{ source_list_id, destination_list_id, on_date }` copies every confirmed to-do on the source list, including sub-to-dos. New rows have `copy_confirmed` false and that `on_date`, and they appear in no view. `POST /api/copies/{copy_id}/confirm` sets `copy_confirmed` true. The server never creates a to-do on its own.
- No route exists for sign-in, calendar, alarm delivery, or a progress number. FR-14 has no route.
- Still not designed, so a story must not invent them: whether an alarm scheduler exists and how early an alarm fires; which timezone "today" uses; the hosting provider. Where `undated` is drawn is decided: a section headed "No date" under the dated rows.

### UX Design Requirements

No UX design contract was included. `DESIGN.md` and `EXPERIENCE.md` exist and are empty drafts. They were excluded.

### FR Coverage Map

FR-1: Epic 1, Story 1.2 — See every to-do list.
FR-2: Epic 2, Story 2.1 — Open Today in order.
FR-3: Epic 2, Story 2.2 — Not-done view across all time.
FR-4: Epic 4, Story 4.1 — Day, week, month, and year views. Undated rows render in a "No date" section under the dated rows.
FR-5: Epic 1, Stories 1.3, 1.4, and 1.7 — Create, update, and delete a to-do.
FR-6: Epic 1, Story 1.5, and Epic 2, Story 2.2 — Mark done and mark not done. The not-done view excludes done.
FR-7: Epic 2, Story 2.1 — What is next while to-dos stay not done.
FR-8: Epic 1, Story 1.3 — Priority 1 through 5, 5 highest.
FR-9: Epic 1, Story 1.3 — Tom chooses what to do first.
FR-10: Epic 1, Story 1.9 — Sub-to-dos.
FR-11: Epic 1, Story 1.9 — New to-do after marking one done.
FR-12: Epic 1, Story 1.7 — Set a time.
FR-13: Epic 1, Story 1.8 — Set an alarm time. Delivery is not designed.
FR-14: Epic 1, Story 1.3 — Withdrawn. No add-to-calendar action, no create-from-calendar, and no in-product calendar. Story 1.1 has no calendar route.
FR-15: Epic 3, Stories 3.1 and 3.2 — Copy, then confirm.
FR-16: Epic 1, Story 1.10 — Name a person who is not a user.
FR-17: Epic 1, Story 1.6, and Epic 2, Story 2.2 — Partial and notes. Partial stays in the not-done view.

## Epic List

### Epic 1: Keep a to-do
Tom can create lists and to-dos, set priority, time, and an alarm, mark done, not done, or partial with notes, add sub-to-dos or a follow-up to-do, and name a person. The product does not pick his first to-do and does not create to-dos for him.
**FRs covered:** FR-1, FR-5, FR-6, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-16, FR-17

### Epic 2: See today and what is still open
Tom can open Today in order and see what is next while those to-dos are not done. He can open the all-time not-done view, including partial to-dos and excluding done ones.
**FRs covered:** FR-2, FR-3, FR-7

### Epic 3: Copy a list onto a day
Tom can copy every confirmed to-do from one list onto a date, see that copy, and confirm it before it appears. A later Saturday stays empty until he copies again.
**FRs covered:** FR-15

### Epic 4: Browse a day, week, month, or year
Tom can open each period and see the dated to-dos inside it. Confirmed to-dos with no date render under those rows in a section headed "No date".
**FRs covered:** FR-4

## Epic 1: Keep a to-do

Tom can create lists and to-dos, set priority, time, and an alarm, mark done, not done, or partial with notes, add sub-to-dos or a follow-up to-do, and name a person. The product does not pick his first to-do and does not create to-dos for him.

### Story 1.1: Set up initial project from starter template

As a developer,
I want the project created from the Vite React starter,
So that the website, the API, and the database start from one known base.

**Requirements:** NFR-1, NFR-2, NFR-3

**Acceptance Criteria:**

**Given** the Vite React starter
**When** the developer clones it, installs dependencies, and applies the initial configuration
**Then** the web app uses Vite 8.3.5, React 19.3.1, @vitejs/plugin-react 6.2.1, and the TypeScript version that starter installs
**And** the server uses Python >=3.10, FastAPI 0.162.0, PostgreSQL 18.6, SQLAlchemy 2.1.8, and Alembic 1.20.1
**And** one process is configured to serve the API and the built frontend

**Given** that configured app
**When** Tom opens the site
**Then** FastAPI serves the built frontend from the same origin and does not render the product HTML
**And** interactive API docs are off
**And** he is not asked to sign in
**And** there is no sign-in route and no calendar route
**And** no to-do table exists yet

### Story 1.2: Open the site and keep lists

As a Tom,
I want to open the website and create named to-do lists,
So that I can see every list I keep without signing in.

**Requirements:** FR-1, NFR-1

**Acceptance Criteria:**

**Given** the site from Story 1.1, and no lists created yet
**When** he opens his lists
**Then** he sees that there are no to-do lists

**Given** he names a list
**When** the create succeeds
**Then** that list appears in the collection
**And** a second list appears as its own list

**Given** a list he already created
**When** he renames it
**Then** the new name is what he sees

**Given** a create or rename without a name
**When** the request is sent
**Then** the write is rejected with `{ "detail": string }`

**Given** a phone-width browser and a desktop-width browser
**When** he views and creates lists on each
**Then** both widths can see the collection and create a list

### Story 1.3: Add a to-do with a priority

As a Tom,
I want to add a to-do with a priority onto one of my lists,
So that I can see the work and choose which high-priority one to do first.

**Requirements:** FR-5, FR-8, FR-9, FR-14, NFR-4

**Acceptance Criteria:**

**Given** a list Tom created
**When** he adds a to-do with a title and a priority from 1 to 5
**Then** that to-do appears on that list
**And** it does not appear on a different list
**And** its state is `not_done`
**And** `copy_confirmed` is true
**And** the list shows to-dos in `position` order

**Given** a priority of 5 and a priority of 1 on two not-done to-dos
**When** he views the list
**Then** 5 outranks 1
**And** the product does not select either one as the to-do he must do
**And** the to-do has no "quick to finish" field

**Given** a priority outside 1 through 5, or a missing priority, or a missing title
**When** he tries to add the to-do
**Then** the write is rejected with `{ "detail": string }`
**And** no to-do is added

**Given** he has not submitted a create
**When** the list is loaded
**Then** the server has not created a to-do on its own

**Given** the lists feature from Story 1.2
**When** this screen reads or writes a to-do
**Then** it calls the generated OpenAPI client
**And** it does not declare its own to-do type
**And** JSON fields stay snake_case

**Given** a to-do on the list
**When** he views it
**Then** it offers no add-to-calendar action
**And** the product does not keep a calendar
**And** the product does not create a to-do from a calendar event

**Given** a phone-width browser and a desktop-width browser
**When** he adds a to-do and reads the list on each
**Then** both widths can add a to-do and see its priority

### Story 1.4: Change or delete a to-do

As a Tom,
I want to change a to-do's title, priority, or position, and delete a to-do or a whole list,
So that the list shows the work I still mean to keep.

**Requirements:** FR-5

**Acceptance Criteria:**

**Given** a to-do on a list
**When** he changes its title, its priority, or its position
**Then** the new title, priority, or `position` order is what he sees on that list

**Given** a priority outside 1 through 5
**When** he tries to change the priority
**Then** the write is rejected with `{ "detail": string }`
**And** the stored priority is unchanged

**Given** a to-do
**When** he deletes it
**Then** it no longer appears on any list

**Given** a list that has to-dos, and a second list that has its own to-dos
**When** he deletes the first list
**Then** that list and its to-dos no longer appear
**And** the second list and its to-dos still appear

**Given** a to-do id or a list id that does not exist
**When** he updates or deletes it
**Then** the write is rejected with `{ "detail": string }`

**Given** a phone-width browser and a desktop-width browser
**When** he changes and deletes a to-do on each
**Then** both widths can change the title and priority and can delete the to-do

### Story 1.5: Mark done and mark not done

As a Tom,
I want to mark a to-do done and mark a done to-do not done,
So that a finished to-do stays finished until I decide it is open again.

**Requirements:** FR-6

**Acceptance Criteria:**

**Given** a to-do whose state is `not_done`
**When** he marks it done
**Then** its state is `done`
**And** the list still shows it as done

**Given** a to-do whose state is `done`
**When** he marks it not done
**Then** its state is `not_done`
**And** the list shows it as not done

**Given** a state other than `not_done` or `done`
**When** he tries to set it
**Then** the write is rejected with `{ "detail": string }`
**And** the stored state is unchanged

**Given** a phone-width browser and a desktop-width browser
**When** he marks a to-do done and then not done on each
**Then** both widths can make either change

### Story 1.6: Mark partial and keep notes

As a Tom,
I want to mark a to-do partial and record notes,
So that unfinished work stays visible as partial, with the notes still there when I come back.

**Requirements:** FR-17

**Acceptance Criteria:**

**Given** a to-do whose state is `not_done` or `done`
**When** he marks it partial and saves notes
**Then** its state is `partial`
**And** the list shows the word "partial"
**And** it does not show a percent, a count, or a progress score
**And** the saved notes are what he sees when he returns

**Given** a to-do whose state is `partial`
**When** he marks it done
**Then** its state is `done`
**And** the notes are still there

**Given** a to-do whose state is `partial`
**When** he marks it not done
**Then** its state is `not_done`
**And** the notes are still there

**Given** a body that includes a progress number, percent, or count
**When** he saves the to-do
**Then** the stored to-do has no such field

**Given** a state other than `not_done`, `partial`, or `done`
**When** he tries to set it
**Then** the write is rejected with `{ "detail": string }`
**And** the stored state is unchanged

**Given** a phone-width browser and a desktop-width browser
**When** he marks a to-do partial and reads the notes on each
**Then** both widths show "partial" and the same notes

### Story 1.7: Set a date and a time

As a Tom,
I want to set a date and a time on a to-do,
So that Saturday's stops keep the clocks I mean, including English and ballet.

**Requirements:** FR-12, FR-5

**Acceptance Criteria:**

**Given** a to-do
**When** he sets `on_date` to a calendar date and `at_time` to a time of day
**Then** that date and time are what he sees
**And** no timezone is stored

**Given** the Saturday stops
**When** he stores them
**Then** an English drop-off can be 09:00:00
**And** an English pickup can be 10:00:00
**And** a ballet drop-off can be 13:00:00
**And** a ballet pickup can be 14:30:00

**Given** a to-do that already has a date or a time
**When** he clears `on_date` or `at_time`
**Then** the cleared field is null
**And** the other field is unchanged

**Given** an `on_date` that is not `YYYY-MM-DD`, or an `at_time` that is not `HH:MM:SS`
**When** he tries to save it
**Then** the write is rejected with `{ "detail": string }`
**And** the stored date and time are unchanged

**Given** a phone-width browser and a desktop-width browser
**When** he sets a date and a time on each
**Then** both widths show the same date and time

### Story 1.8: Set an alarm time

As a Tom,
I want to set an alarm time on a to-do that already has a time,
So that a time-bound to-do can carry an alarm without the product firing it in this version.

**Requirements:** FR-13

**Acceptance Criteria:**

**Given** a to-do whose `at_time` is set
**When** he sets `alarm_at` to a time of day
**Then** that alarm time is stored and shown
**And** no alarm fires
**And** there is no alarm-delivery route
**And** how early an alarm fires is not built

**Given** a to-do whose `at_time` is null
**When** he sets `alarm_at`
**Then** the write is rejected with `{ "detail": string }`
**And** `alarm_at` stays null

**Given** a to-do whose `at_time` and `alarm_at` are both set
**When** he clears `at_time` and leaves `alarm_at` set
**Then** the write is rejected with `{ "detail": string }`
**And** both stored values are unchanged

**Given** a to-do whose `at_time` and `alarm_at` are both set
**When** he clears both
**Then** both are null

**Given** a to-do with no time
**When** he leaves it without an alarm
**Then** the to-do is valid

**Given** a phone-width browser and a desktop-width browser
**When** he sets an alarm time on each
**Then** both widths show the same `alarm_at`

### Story 1.9: Add sub-to-dos and keep both split paths

As a Tom,
I want to add sub-to-dos to a to-do, and still mark it done and create a new to-do,
So that blocked or multi-part work can be split either way.

**Requirements:** FR-10, FR-11

**Acceptance Criteria:**

**Given** a to-do on a list
**When** he creates a sub-to-do with that to-do as `parent_id` on the same list
**Then** the sub-to-do is shown with that parent
**And** its `parent_id` is that to-do
**And** the parent remains on the list

**Given** a `parent_id` that does not exist, or a parent on a different list
**When** he tries to create the sub-to-do
**Then** the write is rejected with `{ "detail": string }`
**And** no sub-to-do is added

**Given** a parent with sub-to-dos, and another to-do that is not under that parent
**When** he deletes the parent
**Then** the parent and its sub-to-dos no longer appear
**And** the other to-do still appears

**Given** a parent that already has a sub-to-do
**When** he marks the parent done and creates a new to-do
**Then** the parent is `done`
**And** the new to-do exists
**And** he can still add another sub-to-do to a to-do
**And** neither path removes the other

**Given** a phone-width browser and a desktop-width browser
**When** he adds a sub-to-do on each
**Then** both widths show the sub-to-do with its parent

### Story 1.10: Name a person who is not a user

As a Tom,
I want to put his daughter's name or his wife's name on a to-do,
So that the to-do records who it involves without giving that person the app.

**Requirements:** FR-16

**Acceptance Criteria:**

**Given** a to-do
**When** he sets `person_name` to his daughter's name or his wife's name
**Then** the to-do shows that name
**And** there is no account for that person
**And** that person has no sign-in and no view of the to-do

**Given** a to-do whose `person_name` is set
**When** he clears it
**Then** `person_name` is null

**Given** a phone-width browser and a desktop-width browser
**When** he sets a person name on each
**Then** both widths show the same name

## Epic 2: See today and what is still open

Tom can open Today in order and see what is next while those to-dos are not done. He can open the all-time not-done view, including partial to-dos and excluding done ones.

### Story 2.1: Open Today and see what is next

As a Tom,
I want to open Today and see that day's to-dos in order, including what is next,
So that on Saturday I can follow the stops even when I do not mark them done.

**Requirements:** FR-2, FR-7, NFR-1

**Acceptance Criteria:**

**Given** confirmed to-dos whose `on_date` is the date he sends
**When** he opens Today with that `on_date`
**Then** the response is `{ on_date, todos, next_todo_id }`
**And** `todos` are those confirmed to-dos in `position` order
**And** a to-do with that `on_date` and a null `at_time` is included
**And** a to-do with a different `on_date` is excluded
**And** the server does not invent a timezone

**Given** the first not-done to-do in that order, which may be `partial`
**When** he opens Today
**Then** `next_todo_id` is that to-do
**And** done to-dos remain in `todos` and are skipped for `next_todo_id`

**Given** every to-do that day is `done`, or the day has no to-dos
**When** he opens Today
**Then** `next_todo_id` is null

**Given** every Saturday to-do is still `not_done`
**When** he opens Today
**Then** those to-dos are in order
**And** `next_todo_id` is the first of them

**Given** a request without `on_date`
**When** he opens Today
**Then** the request is rejected with `{ "detail": string }`

**Given** a phone-width browser and a desktop-width browser
**When** he opens Today on each
**Then** both widths show the same order and the same next to-do

### Story 2.2: Open the not-done view

As a Tom,
I want to see every to-do that is not done, across all time,
So that finished work drops out and partial work stays visible.

**Requirements:** FR-3, FR-6, FR-17, NFR-1

**Acceptance Criteria:**

**Given** a `not_done` to-do, a `partial` to-do, a `done` to-do, a not-done to-do on another date, and a not-done to-do with no `on_date`
**When** he opens the not-done view
**Then** the view includes the `not_done` to-do, the `partial` to-do, the other-date to-do, and the to-do with no `on_date`
**And** the view excludes the `done` to-do
**And** only `copy_confirmed` true rows are included

**Given** a phone-width browser and a desktop-width browser
**When** he opens the not-done view on each
**Then** both widths show the same not-done to-dos

## Epic 3: Copy a list onto a day

Tom can copy every confirmed to-do from one list onto a date, see that copy, and confirm it before it appears. A later Saturday stays empty until he copies again.

### Story 3.1: Copy a list without showing it

As a Tom,
I want to copy a list onto a date and look at that copy before it is added,
So that Saturday does not fill itself.

**Requirements:** FR-15, NFR-4

**Acceptance Criteria:**

**Given** a source list of confirmed to-dos, including sub-to-dos, and a destination list
**When** he copies that source onto an `on_date`
**Then** the response is `{ id, todos }`
**And** every confirmed source to-do, including sub-to-dos, is copied
**And** a done source to-do is copied too
**And** an unconfirmed source row is not copied
**And** each new row has `copy_confirmed` false, `copy_id` set, `list_id` of the destination, and that `on_date`
**And** a copied sub-to-do's `parent_id` points at the copied parent
**And** relative `position` order matches the source
**And** title, state, priority, notes, `at_time`, `alarm_at`, and `person_name` are copied

**Given** that unconfirmed copy
**When** he loads the destination list, Today for that date, or the not-done view
**Then** the copied to-dos do not appear

**Given** that copy id
**When** he opens the copy
**Then** he sees the unconfirmed to-dos

**Given** a missing source list, a missing destination list, or an invalid `on_date`
**When** he tries to copy
**Then** the write is rejected with `{ "detail": string }`
**And** no to-do is created

**Given** he has not submitted a copy or a create
**When** any list or view is loaded
**Then** the server has not created a to-do on its own

**Given** a phone-width browser and a desktop-width browser
**When** he reviews the pending copy on each
**Then** both widths show the same unconfirmed to-dos

### Story 3.2: Confirm a copy onto one day

As a Tom,
I want to confirm a copy before it appears, and only on the date I chose,
So that a later Saturday stays empty until I copy again.

**Requirements:** FR-15, NFR-1

**Acceptance Criteria:**

**Given** an unconfirmed copy onto a date
**When** he confirms it
**Then** those to-dos have `copy_confirmed` true
**And** they appear on the destination list
**And** they appear on Today for that `on_date`

**Given** he confirms the same copy again
**When** the second confirm finishes
**Then** no second set of to-dos is created

**Given** a confirmed copy onto one Saturday
**When** he opens Today for a later Saturday
**Then** that later day does not include those to-dos

**Given** a copy id that does not exist
**When** he tries to confirm it
**Then** the write is rejected with `{ "detail": string }`

**Given** a phone-width browser and a desktop-width browser
**When** he confirms a copy on each
**Then** both widths show the confirmed to-dos on that day

## Epic 4: Browse a day, week, month, or year

Tom can open each period and see the dated to-dos inside it. Confirmed to-dos with no date render under those rows in a section headed "No date".

### Story 4.1: Open a day, week, month, or year

As a Tom,
I want to open a day, a week, a month, or a year,
So that I can see the dated to-dos in that period, and the to-dos with no date under them.

**Requirements:** FR-4, NFR-1

**Acceptance Criteria:**

**Given** `grain` of `day`, `week`, `month`, or `year`, and an `anchor` date
**When** he opens the period
**Then** the response is `{ grain, anchor, todos, undated }`
**And** `todos` are confirmed to-dos whose `on_date` falls in the period that contains `anchor`
**And** a to-do outside that period is not in `todos`
**And** `undated` are confirmed to-dos with no `on_date`
**And** an unconfirmed to-do is in neither array
**And** a to-do with `on_date` and a null `at_time` is dated, so it is in `todos` when its date is inside the period

**Given** `grain` is `day`
**When** he opens the period
**Then** the period is that calendar date

**Given** `grain` is `week`
**When** he opens the period
**Then** the period is the Monday-through-Sunday week that contains `anchor`

**Given** `grain` is `month`
**When** he opens the period
**Then** the period is the calendar month of `anchor`

**Given** `grain` is `year`
**When** he opens the period
**Then** the period is the calendar year of `anchor`

**Given** the period screen
**When** it renders
**Then** it shows `todos` first
**And** under those rows it shows a section headed "No date"
**And** that section lists `undated`
**And** an undated to-do is not placed on a day inside the week, month, or year

**Given** a missing `grain`, a `grain` outside those four, or an `anchor` that is not a date
**When** he opens the period
**Then** the request is rejected with `{ "detail": string }`

**Given** a phone-width browser and a desktop-width browser
**When** he opens a period on each
**Then** both widths show the same dated to-dos
**And** both widths show the same "No date" section
