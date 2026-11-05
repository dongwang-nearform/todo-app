# Adversarial review — architecture spine

Verdict: **fix**

Target: `ARCHITECTURE-SPINE.md` (feature altitude, shipped to-do app). Spine was not edited.

Method: for each candidate hole, name two units one level down (epics/stories already in scope: lists, to-do edits, Today/Next, not-done, period, copy/confirm). A hole counts only when both units can obey every written AD and the API Contract sentences and still ship incompatible shared data, two owners of one entity, or two mutation paths. Product scope was not added. Pairs that only work if one unit breaks a written sentence are listed at the end and are not findings.

Binding an FR id is not a rule. Several clashes below are FR consequences (order Tom set, sub-to-do keeps its own state, the date comes from the browser, notes still there on return) that never made it into a Rule. A story can satisfy the Rule text and miss the bound FR.

---

## 1. `position` is not one order

- **Severity:** critical
- **Location:** API Contract, to-do body and the list/today/copy responses; AD-6; no AD owns order
- **Units:** Epic 1 move/create (`features/todo-editor`, `services/todos`) and Epic 2 Today (`services/views`, `features/today`). Epic 3 copy joins the same clash.
- **Both obey:** List GET and Today are "`position` order". Copy "keeps … `position`". PATCH may send `position` ("any to-do field except ids and `copy_*`"). Nothing says the integer is unique, what group it is unique in, what `PATCH position` does to other rows, or how ties break. Nothing says the Today screen must render the server array or use `next_todo_id` as Next.
- **Clash:** Story A treats `position` as a dense `1..n` among siblings (same `list_id` and same `parent_id`) and writes those integers with several absolute PATCHes. Story B treats `PATCH {position: k}` as "insert at k and shift the whole list". Story C builds Today as a flat `ORDER BY position` across every list and sets `next_todo_id` to the first row whose state is not `done`. Story D renders a parent/child tree and may treat the earliest `at_time` as Next. Copy keeps source integers, so destination rows and other lists routinely share a number. Ties have no required second key, so "the first" is not a single row. After one move-up, Next on Saturday is a different to-do in each build.
- **Close with:** One AD, one total order, owned by `services/todos` except for the copy renumber below. Sibling group = same `list_id` and same `parent_id` (null is a group). Inside a group, `position` is the dense unique sequence `1..n`. Omitted on create → append. `PATCH position` moves that row inside its group and rewrites that group to `1..n` in the same call; it does not renumber other groups and it does not leave duplicates. Copy keeps relative order inside each copied group; on a collision with the destination group it appends after that group's max and rewrites the copied group (tighten the "keeps position" sentence so it cannot create a duplicate). Every array that says position order sorts by `position`, then `id`. Today, which mixes lists, sorts by the list's `position`, then `position`, then `id`. `next_todo_id` is the first row in that Today array whose state is not `done`. The Today screen renders that array and marks that id. It does not reorder by time or priority.

## 2. PATCH does not say what an absent field means

- **Severity:** critical
- **Location:** `PATCH /api/todos/{todo_id}`; "state defaults to `not_done`"; Consistency Conventions, State
- **Units:** Epic 1 mark-done and Epic 1 editor save. Both are the same route and the same row.
- **Both obey:** The body is "any to-do field except ids and `copy_*`". Mark-done, partial, notes, priority, time, alarm, and person name are all this PATCH. The default state is specified for create, not for a missing key on update. Null and omission are not distinguished. No AD says the server may change only keys that are present.
- **Clash:** Story A sends `{ "state": "done" }` and requires title, priority, time, notes, and date to stay. Story B treats the body as the full mutable record: a missing `state` becomes `not_done`, a missing `at_time` clears the time, a JSON `null` and a missing key are the same. The editor save sends title, priority, notes, date, time, alarm, and person, and does not send `state`. Under A, that save keeps `done` / `partial`. Under B, it clears them. Under B, Story A's mark-done body wipes the title and the time. Phone and desktop (AD-1) then persist different rows from the same buttons.
- **Close with:** Tighten AD-6 / the PATCH row. The body is a merge: only keys present in the JSON change; omitted keys stay; JSON `null` clears a nullable field and is rejected for a required field (`title`, `priority`, `state`, `position`, `notes`). `notes` null is stored as empty string if notes stay non-null. State is not defaulted on update. One PATCH changes one row (see finding 5).

## 3. Two owners of the to-do tree

- **Severity:** high
- **Location:** `parent_id` on create; "except ids and `copy_*`"; `DELETE /api/lists/{list_id}`; `DELETE /api/todos/{todo_id}`; ER diagram (no referential action)
- **Units:** Epic 1 sub-to-dos and Epic 1 delete (list and to-do).
- **Both obey:** "`parent_id` creates a sub-to-do." The PATCH exclusion is the word "ids", which can mean the row `id` only, or also `list_id` and `parent_id` (`copy_*` is called out separately, so `list_id` / `parent_id` are not obviously excluded). Delete-list "deletes its to-dos" (rows with that `list_id`). Delete-todo "also deletes its sub-to-dos" (walk `parent_id`). Neither sentence says the parent must be on the same list, that the graph is a tree, that `list_id` is fixed after create, or whether grandchildren follow. The ER diagram draws the links and does not say `ON DELETE`.
- **Clash:** Story A creates a child on list 2 whose `parent_id` is a row on list 1, and PATCHes `list_id` or `parent_id` later, including a cycle. Story B deletes a list by `list_id` only, so the child on list 2 survives with a dead parent, and deletes a to-do one level deep, so a grandchild remains. Story B′ walks `parent_id` across lists and deletes the other list's child. After the same user action, the surviving rows differ. A cycle makes the walk non-terminating while both stories still match the sentences.
- **Close with:** One AD. `list_id` is set only by the create URL and never by PATCH. `parent_id` is set on create or PATCH, must reference a to-do on that same list, and must not create a cycle (the graph is a tree). Delete-todo deletes the row and every descendant, on that list only. Delete-list deletes the list and every to-do with that `list_id` (descendants cannot sit elsewhere). `services/todos` performs to-do deletes; `services/lists` deletes a list only by calling that behavior. State the FK action: `list_id` and `parent_id` are `ON DELETE CASCADE`, matching those walks.

## 4. Alarm rejection is not pinned to the merged row

- **Severity:** high
- **Location:** To-do body, `alarm_at`; AD-4 "a write that breaks these is rejected"
- **Units:** Epic 1 set-time and Epic 1 set-alarm. One PATCH, one row.
- **Both obey:** "`alarm_at` … Rejected when `at_time` is null." Both stories reject a stored alarm with no time. The sentence does not say whether the check sees the row before the PATCH or the row after every key in the body is applied.
- **Clash:** The editor's save sets time and alarm in one body on a row that had neither. Story A checks the merged row and accepts `{ at_time, alarm_at }` together. Story B rejects because `alarm_at` is present while the stored `at_time` is still null. The same body is 200 in one build and 422 in the other. Clearing time is the mirror: `{ "at_time": null }` with an existing alarm. Story A rejects because the merged row is illegal. Story B rejects only when the body itself contains a non-null `alarm_at`. One of those builds then leaves an alarm with no time, which a later read still has to reject.
- **Close with:** Tighten the alarm sentence. Validate the row after the merge. A single PATCH may set `at_time` and `alarm_at` together. If the merged row has `alarm_at` set and `at_time` null, reject. Do not clear `alarm_at` implicitly. Clearing a time while an alarm is set requires `alarm_at: null` in that same body (or the write is rejected).

## 5. Mark-done can legally rewrite descendants

- **Severity:** high
- **Location:** AD-4 state enum; PATCH "this is how mark-done … [is] written"
- **Units:** Epic 1 mark-done and Epic 1 sub-to-dos.
- **Both obey:** State is `not_done`, `partial`, or `done`. A write of one of those values is legal. PATCH is how mark-done is written. No AD says a state write touches only the row in the URL. "The server never creates a to-do on its own" does not forbid extra updates. AD-4 binds FR-10, but the Rule never says a sub-to-do keeps its own state.
- **Clash:** Story A PATCHes the parent's `state` and leaves each descendant's `state` as stored. Story B, inside `services/todos`, also sets every descendant to `done` (or back to `not_done`). Both return the parent. The not-done view and Next then either still show the children or drop them. Same button, different rows.
- **Close with:** A state, notes, priority, time, alarm, or person-name write updates that one row. Descendants keep their own values. Delete is the only cascade (finding 3).

## 6. Two owners of an unconfirmed copy

- **Severity:** high
- **Location:** AD-5; `GET/PATCH/DELETE /api/todos/{todo_id}`; `POST /api/copies` and confirm
- **Units:** Epic 3 copy/confirm (`services/copies`) and Epic 1 editor/delete (`services/todos`).
- **Both obey:** AD-5 hides an unconfirmed copy from lists and views only. `GET /api/todos/{todo_id}` "includ[es] an unconfirmed copy", so the editor may load it. PATCH and DELETE name `{todo_id}` and do not exempt `copy_confirmed = false`. Confirm "returns the same to-dos with `copy_confirmed` true" and does not say the set is frozen at `POST /api/copies`. AD-7 sends each router to its own service, so both services write `todos`.
- **Clash:** Story A inserts the batch and, on confirm, flips `copy_confirmed` on whatever `copy_id` still points at, expecting the POST snapshot. Story B PATCHes a pending row's title (or DELETEs it and its copied children) through the to-do routes. Confirm then publishes a different set than the one the copy screen showed, or a smaller set. "The same to-dos" is satisfied by both "the rows as inserted" and "the rows that remain". There is no cancel route, but delete is a second way to cancel.
- **Close with:** `services/copies` is the only writer that inserts rows with `copy_confirmed` false and the only writer of `copy_id` / `copy_confirmed`. Until confirm, `services/todos` rejects PATCH and DELETE of those rows with `{ "detail": string }`. Confirm only flips `copy_confirmed` on the rows still stored for that `copy_id`; it does not re-copy from the source. A second confirm returns those rows and does not insert another set.

## 7. Two servers for one client route, no shared fallback

- **Severity:** high
- **Location:** AD-3; Structural Seed; Consistency Conventions, Landing
- **Units:** Epic 1 compose web image (`web/Dockerfile`, nginx) and Epic 1 API process serving `web/dist`.
- **Both obey:** AD-3 says both exist. nginx "serves the built frontend and proxies `/api`". FastAPI "serves those files" when `web/dist` is present. Neither sentence says a client route (`/`, `/not-done`, `/lists`, `/lists/:listId`, `/period`, `/copies/:copyId`) must return `index.html` when the path is not a file. Conventions name the routes; they are not an AD.
- **Clash:** Story A uses `try_files` to `index.html`, so a refresh of `/period` loads the app. Story B mounts the directory as static files and returns 404 for `/period` because no such file exists. `/api` works in both. Deep links and reloads succeed on the Compose origin and fail on the API-served dist. Same landing table, two hosts.
- **Close with:** Tighten AD-3. Both hosts use one fallback: a GET that is not `/api`, not an existing file under the built frontend, and not the OpenAPI document returns the built `index.html`. Do not add a second product origin.

## 8. "Which timezone today uses" still lets two screens pick two dates

- **Severity:** high
- **Location:** Deferred; Consistency Conventions, Time; `GET /api/views/today?on_date=`; `GET /api/views/period?anchor=`
- **Units:** Epic 2 Today and Epic 4 period. Also the two browsers AD-1 is about.
- **Both obey:** The server stores no zone and does not invent one. `on_date` and `anchor` are client-supplied `YYYY-MM-DD`. The deferral records the question and does not bind either client. No AD says which clock produces that date. A story that stores a zone would break the time convention; these stories do not.
- **Clash:** Story A sends the browser's local calendar date (`getFullYear` / `getMonth` / `getDate`). Story B sends `toISOString().slice(0, 10)` (UTC). Near a zone boundary, Today and the day view request different dates, and a phone and a desktop do too. One database, two "todays". The deferral is the hole: it parks a divergence the level below has to invent.
- **Close with:** Remove the deferral. One AD: the date the website uses as today is the browser's local calendar date. Today and period both use that. The server never computes "today" and never stores a zone. `on_date` on a to-do stays a zone-less date.

## 9. Blank title and blank list name are both legal

- **Severity:** medium
- **Location:** To-do body `title`; `POST/PATCH /api/lists` `{ name }`; AD-4 (no title rule)
- **Units:** Epic 1 create/rename list and Epic 1 create/update to-do.
- **Both obey:** `title` is a string. `name` is the list body. Priority is the only create field the spine marks required. AD-4's rejection list does not include an empty name. Both stories return `{ "detail": string }` when they do reject.
- **Clash:** Story A rejects a missing or blank (after trim) title or list name. Story B stores `""` or `"   "`. The collection and the to-do row then either gain a nameless entry or refuse it.
- **Close with:** Empty or whitespace-only `title` and list `name` are rejected. Stored values are trimmed.

## 10. Copy onto the same list

- **Severity:** medium
- **Location:** `POST /api/copies` `{ source_list_id, destination_list_id, on_date }`
- **Units:** Two Epic 3 implementations of the same route.
- **Both obey:** The body is those three fields. The rule copies every confirmed to-do on the source onto the destination. It never says the ids differ. AD-5 still hides the rows until confirm.
- **Clash:** Story A rejects `source_list_id == destination_list_id`. Story B copies the list onto itself, keeps positions (finding 1), and on confirm doubles every row. Same request, 422 versus a second set.
- **Close with:** The two list ids must differ. Otherwise reject with `{ "detail": string }` and insert nothing.

## 11. List `position` is a field with no order

- **Severity:** medium
- **Location:** `GET/POST /api/lists`; PATCH list body is `{ name }` only
- **Units:** Two Epic 1 list stories. The lists page renders the array it receives.
- **Both obey:** The collection item is `{ id, name, position }`. POST takes `{ name }` and does not say how `position` is chosen. GET does not say the array order. PATCH cannot change `position`, so whatever create wrote is permanent.
- **Clash:** Story A assigns `max+1` and returns lists ordered by `position`, then `id`. Story B assigns `0` to the newest list, or returns rows ordered by `name` or `id`. Both payloads match the table. The collection order differs, and no later route can repair it.
- **Close with:** List `position` is a dense `1..n` in creation order (`max+1`, unique). `GET /api/lists` returns that order, tie-broken by `id`. This spine does not include list reorder; do not add a position field on PATCH unless an AD defines the move.

## 12. Not-done and multi-date period arrays have no order

- **Severity:** medium
- **Location:** `GET /api/views/not-done`; `GET /api/views/period` `todos` and `undated`; AD-8
- **Units:** Epic 2 not-done and Epic 4 period.
- **Both obey:** Not-done is "confirmed to-dos whose `state` is not `done`", with no order. Period `todos` are confirmed rows whose `on_date` falls in the grain; `undated` are confirmed rows with no `on_date`. AD-8 orders the screen as dated rows, then the "No date" section. It does not order rows inside either array. AD-4 binds FR-8 but the Rule does not say "do not sort by priority". A client that preserves server order whenever the set spans more than one date (the shipped list view does) will show whatever the service returned.
- **Clash:** Story A sorts not-done and period dated rows by `on_date`, then `position`, then `id`, and undated by `position`, then `id`. Story B sorts those arrays by `priority` descending. Both satisfy AD-8's section order. The not-done page and the week/month/year pages show different rows first.
- **Close with:** Name the sort on each array. Not-done: `on_date` ascending with nulls last, then `position`, then `id`. Period `todos`: `on_date`, then `position`, then `id`. Period `undated`: `position`, then `id`. No view sorts or filters by priority.

## 13. Notes can be wiped when the state leaves `partial`

- **Severity:** medium
- **Location:** AD-4 "Partial stores notes and does not store a progress number."
- **Units:** Epic 1 partial/notes and Epic 1 mark-done / mark-not-done.
- **Both obey:** Partial is a state. It stores notes. It does not store a progress number. The sentence does not say notes are cleared when state changes, and it does not say other states may not store notes. AD-4 binds FR-17, but the Rule does not say notes are still there on return.
- **Clash:** Story A leaves `notes` in place across `partial` → `done` → `partial`. Story B clears `notes` whenever the new state is not `partial`, reading "partial stores notes" as "only partial stores notes". The next visit shows the old notes or a blank. The screen can hide notes unless state is `partial` either way; the stored value still diverges.
- **Close with:** `notes` is ordinary text on the row, default empty, kept across state changes. Partial does not add a progress field. Showing notes only while state is `partial` is a display rule, not a write.

---

## Pairs that do not count

These look like holes and are not, because one side breaks a written sentence:

- Validation `detail` as a FastAPI array of objects. AD-6 already says `{ "detail": string }`. The array handler does not obey.
- Clearing `alarm_at` inside the server when the client only clears `at_time`. The contract says that alarm is rejected, not repaired.
- A new sign-in, calendar, alarm-delivery, progress, or second health route. AD-6 and AD-10 already forbid them.
- Today including undated rows, or a period view dropping the "No date" section. AD-8 and the today response already forbid that.
- A primary sort of Today by `at_time` or `priority` on the server. The today row already says `position` order. The hole that remains is the undefined group, the tie-break, the PATCH move, and a client that ignores `next_todo_id` (finding 1).
- Storing a timezone on the row. The time convention already forbids it. The open hole is two clients choosing two calendar dates (finding 8).

## What held

AD-1 (one database, no account), AD-2 (writers are services; health is `SELECT 1` only), AD-9 (alarm is stored and shown, never fired), AD-10 (one health probe and body), and AD-11 (one compose file, one test profile, pinned images) do not by themselves yield a both-obey pair. AD-7's module list is tight enough that a second to-do type or a router calling the wrong service is a violation, not a hole. Week bounds (Monday–Sunday), the state enum, priority 1–5 with 5 highest, and "no list and no view returns an unconfirmed copy" are enforceable as written.
