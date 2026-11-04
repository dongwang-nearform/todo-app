---
name: Todo App
status: draft
sources:
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/prd.md
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-bmad-example-todo-2026-11-04/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/epics.md
updated: 2026-11-04
---

# Todo App — Experience Spine

`DESIGN.md` is the visual identity. This spine is how the site behaves. No mockups. Spine wins on conflict with any later picture.

## Foundation

One responsive website. Phone width and desktop width. No native app. No component library. `[ASSUMPTION: light mode only.]` Tom is the only person who uses it. He is not asked to sign in. `DESIGN.md` holds color, type, and shape.

## Information Architecture

| Surface | Reached from | Purpose |
|---|---|---|
| Today | App open | That date's to-dos in position order, and which one is next |
| Not done | Nav | Every confirmed to-do that is not done, across all time |
| Lists | Nav | Every to-do list |
| List | A list row | Confirmed to-dos on that list, and the editor |
| Period | Nav, then day, week, month, or year | Dated to-dos in the period, then undated to-dos under them |
| Copy review | A list, action "Copy onto a date" | The pending copy, invisible everywhere else until confirm |

`[ASSUMPTION: opening the site lands on Today. The PRD left the landing surface unstated. UJ-2 already starts on Today, and UJ-1 can scan priority from that same list.]`

The editor is the list surface. `[ASSUMPTION: below 768px the editor replaces the list until he saves or closes it. At 768px and above it sits beside the list.]` Copy review replaces the current surface. Nothing stacks a second dialog on top.

A week is Monday through Sunday containing the anchor. That matches Story 4.1.

## Voice and Tone

The nouns are the glossary. Say to-do, sub-to-do, list, Today, partial, done. Do not say task or item.

| Do | Don't |
|---|---|
| "Next" | "Do this first" |
| "partial" | "50%" or "in progress" |
| "No to-dos today." | "You're all caught up!" |
| "Confirm copy" | "Smart add" |
| "Couldn't save." | A second error format besides the server `detail` string |

## Component Patterns

| Component | Use | Behavioral rules |
|---|---|---|
| To-do row | Today, list, not done, period, copy review | Shows priority, title, state word, time, alarm time, and person name when those values exist. Opens the editor. Does not select itself. |
| Next label | Today only | On the row `next_todo_id`. Hidden when that id is null. A partial row can carry it. A done row cannot. |
| Priority numeral | Every row | 1 through 5, 5 highest. The list order stays `position`. He moves a row up or down. The product does not sort by priority. |
| State control | Editor | Sets `not_done`, `partial`, or `done`. Partial stores notes. No percent, count, or score control exists. |
| Sub-to-do | List, under its parent | Created with that parent. Indented under it. Deleting the parent removes the sub-to-dos from the list. Mark done and create a new to-do stays available. |
| Copy review | After copy, before confirm | Lists the pending rows. Confirm is the primary button. Until confirm, those rows are absent from Today, the destination list, not done, and period. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| No lists | Lists | "No to-do lists." One action: create a list. |
| Empty Today | Today | "No to-dos today." `next_todo_id` is null. |
| All done today | Today | The rows stay, each marked done. No Next label. |
| Partial | Any list of to-dos | The word "partial" and the notes. The row remains on not done. |
| Done | List, Today, period | The word "done". Absent from not done. |
| Pending copy | Copy review | Visible here only. |
| Save failed | Editor, copy | Show the server `detail` string. Keep what he typed. |
| Loading | Any surface | The surface name stays. Rows appear when the response arrives. No second empty message while the request is open. |

## Interaction Primitives

Phone width is the hard case. Every action is a control with a visible name. Move up and move down change `position`. Drag is not required.

On a keyboard, Tab follows the visual order. Enter opens the focused row. Escape closes the editor and returns to the list without a second confirm. The focus ring uses `{colors.focus}`.

He cannot sign in. A named person has no view. No control adds a calendar or creates a to-do from a calendar event.

## Accessibility Floor

Behavioral. Contrast lives in `DESIGN.md`.

- WCAG 2.2 AA for text on `{colors.background}` and for `{colors.primary-foreground}` on `{colors.primary}`.
- Priority, partial, done, and Next are each a word or a numeral, not a color alone.
- The surface name is the page heading and is announced on navigation.
- Buttons name the action: "Mark done", "Mark not done", "Mark partial", "Confirm copy", "Delete".
- The error `detail` string is announced when a write fails.
- Touch targets for row actions are at least 44px on the short side.

## Responsive & Platform

| Width | Behavior |
|---|---|
| Below 768px | One column. Nav is text links. Editor replaces the list. |
| 768px and above | Nav column plus one reading column. Editor sits beside the list. |

`[ASSUMPTION: 768px is the break.]` Same capabilities at both widths. No native iOS or Android app.

## Undated to-dos

`[ASSUMPTION: on a period surface, dated to-dos render first, in position order. Confirmed to-dos with no on_date render under them in a list headed "No date". They are not placed on a day inside the week, month, or year.]`

Story 4.1 currently says the period screen does not add a layout region for `undated`. This spine adds that region. The story acceptance criterion has to change before a builder can satisfy both.

## Alarm

`[ASSUMPTION: the row shows alarm_at when it is set. v1 does not fire an alarm, does not ask how early, and has no notification permission step. The architecture left delivery undesigned.]`

A to-do with no `at_time` cannot gain an `alarm_at`. The editor refuses that write and shows the `detail` string.

## Key Flows

### UJ-1. Tom starts the day by finishing what is high priority and quick

1. Tom opens the site on his phone after he gets up. Today is showing. He is not asked to sign in.
2. He reads the rows. Priority is a numeral. Nothing is marked as the one he should do. "Quick to finish" is his judgment.
3. He picks a high-priority row himself and does the work.
4. **Climax:** He marks it done. The row stays on Today with the word "done". If it was the next row, Next moves to the following not-done row, or disappears.
5. If the work is blocked or has several parts, he either marks it done and creates a new to-do, or adds sub-to-dos. Both stay available. If it is time-bound, he sets `at_time` and may set `alarm_at`. The alarm is stored and shown. It does not fire.

### UJ-2. Tom runs Saturday from today's list by checking what is next

1. Earlier, Tom copies a list onto Saturday and confirms. Until he confirms, Saturday's Today does not show those rows.
2. Saturday morning he opens the site. Today already holds the stops in order: English drop-off 09:00:00, English pickup 10:00:00, home and rest, Costco with his wife, ballet drop-off 13:00:00, ballet pickup 14:30:00.
3. He may leave them not done.
4. **Climax:** He looks at Today and the Next label is on the first not-done stop. A later Saturday does not contain these rows unless he copies and confirms again.
