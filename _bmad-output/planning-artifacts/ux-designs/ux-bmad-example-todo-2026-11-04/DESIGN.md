---
name: Todo App
description: A quiet responsive list for one person. Light surface, system type, no component library.
status: draft
sources:
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/prd.md
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-bmad-example-todo-2026-11-04/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/epics.md
updated: 2026-11-04
colors:
  background: '#F7F6F3'
  foreground: '#1C1917'
  muted: '#E7E5E4'
  muted-foreground: '#57534E'
  primary: '#1F4D3A'
  primary-foreground: '#FFFFFF'
  border: '#D6D3D1'
  priority-high: '#9A3412'
  partial: '#A16207'
  done: '#78716C'
  danger: '#9F1239'
  focus: '#1F4D3A'
typography:
  body:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.45'
  label:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: 0.01em
  title:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.25'
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
  gutter: 16px
  margin-phone: 16px
  margin-desktop: 24px
components:
  todo-row:
    background: '{colors.background}'
    foreground: '{colors.foreground}'
    border: '{colors.border}'
    radius: '{rounded.md}'
    padding: '{spacing.3}'
  next-marker:
    background: '{colors.muted}'
    foreground: '{colors.foreground}'
    radius: '{rounded.sm}'
  priority-high:
    foreground: '{colors.priority-high}'
    font: '{typography.label}'
  button-primary:
    background: '{colors.primary}'
    foreground: '{colors.primary-foreground}'
    radius: '{rounded.md}'
  partial-state:
    foreground: '{colors.partial}'
    font: '{typography.label}'
  done-state:
    foreground: '{colors.done}'
---

# Todo App — Design Spine

Working title remains "Todo App." `[ASSUMPTION: the name stays Todo App until a user-facing name is chosen.]`

## Brand & Style

This is a morning list for one person, Tom. It should feel like a sheet of paper he can scan at phone width before he leaves, and the same sheet on a desk. The words on the row do the work. Priority is a numeral he reads. "Next" is a label for the first to-do that day that is not done. The product does not dress one row up as the one he must do.

`[ASSUMPTION: light surface only. No dark theme in v1.]` `[ASSUMPTION: no downloaded font and no component library. The architecture binds React and Vite, and names no UI kit.]`

## Colors

`[ASSUMPTION: the hex values below. The PRD names no palette.]`

- **Paper (`{colors.background}`)** is the page. Rows sit on it. It is not a card grid.
- **Ink (`{colors.foreground}`)** is titles and body.
- **Stone (`{colors.muted}`, `{colors.muted-foreground}`, `{colors.border}`)** is chrome, the Next label, and secondary text.
- **Pine (`{colors.primary}`, `{colors.primary-foreground}`)** is the primary action: save, confirm a copy, create. It is not used to mark a recommended to-do.
- **High priority (`{colors.priority-high}`)** colors the numeral 5 only. A 1 uses ink. Color never replaces the numeral.
- **Partial (`{colors.partial}`)** colors the word "partial" only. The word is always present.
- **Done (`{colors.done}`)** colors a done row's title. The word "done" is always present.
- **Danger (`{colors.danger}`)** is delete only.
- **Focus (`{colors.focus}`)** is the keyboard focus ring, 2px, on `{colors.background}`.

## Typography

System UI only. `{typography.body}` for titles of to-dos and sentences. `{typography.label}` for priority, state, time, person name, and "Next". `{typography.title}` for the surface name: Today, the list name, the period.

One family. No display serif. A to-do title wraps. It is never truncated with an ellipsis on phone width.

## Layout & Spacing

The scale is `{spacing.1}` through `{spacing.6}`. Phone margin is `{spacing.margin-phone}`. Desktop margin is `{spacing.margin-desktop}`. Row padding is `{spacing.3}`. Gap between rows is `{spacing.2}`.

`[ASSUMPTION: the wide layout starts at 768px.]` Below 768px the page is one column and the nav is a single row of text links that wraps. At 768px and above, a nav column sits beside the surface. The surface itself stays one reading column, max 40rem. Week, month, and year do not become a wall of day cells. They stay lists.

## Elevation & Depth

Flat. Rows have a 1px `{colors.border}` and no shadow. The editor on a wide screen is a second column with the same border, not a floating card. A confirm step for a copy replaces the surface. It does not stack on a dialog that is already open.

## Shapes

`{rounded.md}` on rows and primary buttons. `{rounded.sm}` on the Next label. `{rounded.full}` is unused. Corners stay quiet so the list reads as lines of work.

## Components

**To-do row.** Anatomy, in reading order: priority numeral, title, state word when it is "partial" or "done", time when `at_time` is set, alarm time when `alarm_at` is set, person name when set. Notes for a partial to-do sit under the title in `{typography.body}`. Sub-to-dos indent `{spacing.4}` under their parent. A done title uses `{colors.done}`. The row stays on the list.

**Next marker.** The text "Next" in `{components.next-marker}`, placed on the row whose id is `next_todo_id`. It is a label, not a fill of pine.

**Priority.** The numeral 1–5. 5 uses `{colors.priority-high}`. The row is not sorted by this numeral.

**Primary button.** `{components.button-primary}`. One primary button per surface. Confirm copy uses it. Delete does not.

**Partial and done.** The words "partial" and "done". No bar, no percent, no count.

## Do's and Don'ts

Do keep a to-do as one row he can read without opening it.

Do show the state as a word.

Do use pine for actions he chose.

Don't mark a row as recommended, suggested, or quick.

Don't show a progress bar, a percent, a streak, or a celebration when he marks done.

Don't add a calendar control, a sign-in form, or a second theme.

Don't use color as the only sign of partial, done, next, or priority.
