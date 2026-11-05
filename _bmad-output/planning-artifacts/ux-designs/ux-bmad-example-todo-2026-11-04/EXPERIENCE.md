---
name: Todo App
status: final
sources:
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/prd.md
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-bmad-example-todo-2026-11-04/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/epics.md
updated: 2026-11-05
---

# Todo App — Experience Spine

`DESIGN.md` is the visual identity. This spine is how the site behaves. No separate mockups. The running screens are the picture. These spines win on conflict with any later picture.

## Foundation

One responsive website. Phone width and desktop width. No native app. No component library. Light mode only. Tom is the only person who uses it. He is not asked to sign in. `DESIGN.md` holds color, type, and shape.

## Information Architecture

| Surface | Reached from | Purpose |
|---|---|---|
| Today | App open | That date's to-dos in position order, and which one is next |
| Not done | Nav | Every confirmed to-do that is not done, across all time |
| Lists | Nav | Every to-do list |
| List | A list row | Confirmed to-dos on that list, and the editor |
| Period | Nav, then Day, Week, Month, or Year | Dated to-dos in the period, then undated to-dos under them |
| Copy review | A list, action "Copy onto a date" | The pending copy, invisible everywhere else until confirm |

Opening the site lands on Today.

The editor is on the list surface. Below 768px the editor replaces the list until he saves or closes it. At 768px and above it sits beside the list. Copy review replaces the current surface. Nothing stacks a second dialog on top.

A week is Monday through Sunday containing the anchor. That matches Story 4.1.

## Voice and Tone

The nouns are the glossary. Say to-do, sub-to-do, list, Today, partial, done. Do not say task or item.

| Do | Don't |
|---|---|
| "Next" | "Do this first" |
| "partial" | "50%" or "in progress" |
| "No to-dos today." | "You're all caught up!" |
| "Confirm copy" | "Smart add" |
| The server `detail` string | "Couldn't save." or a second error sentence |

## Component Patterns

| Component | Use | Behavioral rules |
|---|---|---|
| To-do row | Today, list, not done, period | Shows priority, title, "partial" or "done" when that is the state, `at_time` when set, the word Alarm and `alarm_at` when set, and the person name when set. Opens the editor. Move up and Move down change `position`. Does not select itself. |
| Copy review row | Copy review | Same visible fields as a to-do row. Does not open the editor. No move controls. |
| Next marker | Today only | On the row `next_todo_id`. Hidden when that id is null. A partial row can carry it. A done row cannot. |
| Priority | Every row | 1 through 5, 5 highest. The list order stays `position`. He moves a row up or down. The product does not sort by priority. |
| State control | Editor | Sets `not_done`, `partial`, or `done`. Partial stores notes. No percent, count, or score control exists. The editor shows "State not done", "State partial", or "State done". |
| Partial and done | Any list of to-dos | The words only. A partial row shows its notes under the title. |
| Sub-to-do | List, under its parent | Created with that parent. Indented under it. Deleting the parent removes the sub-to-dos from the list. Mark done and create a new to-do stays available. |
| Copy review | After copy, before confirm | Lists the pending rows. Confirm copy is the primary button and stays disabled until those rows have loaded. Until confirm, those rows are absent from Today, the destination list, not done, and period. Confirm opens Today on that date. |
| Primary button | Lists, List, editor, copy review | Create a list, Add to-do while the editor is closed, Save, and Confirm copy. One primary button on the surface. |
| Secondary button | Today, List, Not done, Period, editor | Move up, Move down, Close, Mark done, Mark not done, Mark partial, Mark done and create a new to-do, Add sub-to-do, Rename, Copy onto a date, Day, Week, Month, Year, and Add to-do while the editor is open. |
| Danger button | Editor, List | Delete and Delete list. |
| Field | Today, Period, Lists, List, editor | A date field on Today or Period changes the day shown. An empty value does not. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| No lists | Lists | "No to-do lists." |
| Empty Today | Today | "No to-dos today." `next_todo_id` is null. |
| Empty not done | Not done | The heading only. No empty sentence. |
| Empty period | Period | After a successful load, no empty sentence for the dated rows. The "No date" heading still shows. |
| All done today | Today | The rows stay, each marked done. No Next marker. |
| Partial | Any list of to-dos | The word "partial" and the notes. The row remains on not done. |
| Done | List, Today, period | The word "done". Absent from not done. |
| Pending copy | Copy review | Visible here only. |
| Save failed | Editor, copy, move | Show the server `detail` string. Keep what he typed. |
| Loading | Any surface | The surface name stays. Rows appear when the response arrives. No empty sentence while the request is open. A failed load shows the `detail` string and no rows. |

## Interaction Primitives

Phone width is the hard case. Every action is a control with a visible name. Move up and Move down change `position`. Drag is not required.

On a keyboard, Tab follows the visual order. Enter activates the focused control. Escape closes the editor and returns to the list without a second confirm. The focus ring uses `{colors.focus}`.

Period's pressed grain is the one showing. The list surface has Rename, a destination list, a date, and Copy onto a date above the rows. Lists shows Name and Create a list with the rows, including when there are none.

He cannot sign in. A named person has no view. No control creates a to-do from a calendar event. A date field sets `on_date` only.

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

Same capabilities at both widths. No native iOS or Android app.

## Undated to-dos

On a period surface, dated to-dos render first, in position order. Confirmed to-dos with no `on_date` render under them in a section headed "No date". They are not placed on a day inside the week, month, or year. After a successful load, the heading stays when that list is empty.

Story 4.1 matches this section.

## Alarm

The row shows the word Alarm and `alarm_at` when `alarm_at` is set. v1 stores that time and does not fire it. It does not ask for a lead time and has no notification permission step.

A to-do with no `at_time` cannot gain an `alarm_at`. The write fails, the editor keeps what he typed, and the screen shows the server `detail` string.

## Key Flows

### UJ-1. Tom starts the day by finishing what is high priority and quick

1. Tom opens the site on his phone after he gets up. Today is showing. He is not asked to sign in.
2. He reads the rows. Priority is a numeral. Nothing is marked as the one he should do. "Quick to finish" is his judgment.
3. He picks a high-priority row himself and does the work.
4. **Climax:** He marks it done. The row stays on Today with the word "done". If it was the next row, Next moves to the following not-done row, or disappears.
5. If the work is blocked or has several parts, he either marks it done and creates a new to-do, or adds sub-to-dos. Both stay available. If it is time-bound, he sets `at_time` and may set `alarm_at`. The alarm is stored and shown. It does not fire.
6. If a write fails, the row stays as it was and the screen shows the server `detail` string. He can retry.

### UJ-2. Tom runs Saturday from Today by checking what is next

1. Earlier, Tom copies a list onto Saturday and confirms. Until he confirms, Saturday's Today does not show those rows. If confirm fails, the rows stay on copy review and the screen shows the server `detail` string.
2. Saturday morning he opens the site. Today already holds the to-dos in order: English drop-off 09:00:00, English pickup 10:00:00, home and rest, Costco with his wife, ballet drop-off 13:00:00, ballet pickup 14:30:00.
3. He may leave them not done.
4. **Climax:** He looks at Today and the Next marker is on the first not-done to-do. A later Saturday does not contain these rows unless he copies and confirms again.
