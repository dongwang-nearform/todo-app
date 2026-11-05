---
name: Todo App
description: A quiet responsive list for one person. Light surface, system type, no component library.
status: final
sources:
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/prd.md
  - _bmad-output/planning-artifacts/prds/prd-bmad-example-todo-2026-11-04/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-bmad-example-todo-2026-11-04/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/epics.md
updated: 2026-11-05
colors:
  background: '#F7F6F3'
  foreground: '#1C1917'
  muted: '#E7E5E4'
  muted-foreground: '#57534E'
  primary: '#1F4D3A'
  primary-foreground: '#FFFFFF'
  border: '#D6D3D1'
  priority-1: '#57534E'
  priority-2: '#44403C'
  priority-3: '#1C1917'
  priority-4: '#C2410C'
  priority-5: '#9A3412'
  priority-1-bg: '#F0F9FF'
  priority-2-bg: '#F0FDFA'
  priority-3-bg: '#F7FEE7'
  priority-4-bg: '#FEFCE8'
  priority-5-bg: '#FFF7ED'
  partial: '#A16207'
  done: '#746D68'
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
  priority-numeral:
    foreground: '{colors.priority-1}'
    font: '{typography.label}'
  button-primary:
    background: '{colors.primary}'
    foreground: '{colors.primary-foreground}'
    radius: '{rounded.md}'
  button-secondary:
    background: '{colors.background}'
    foreground: '{colors.foreground}'
    border: '{colors.border}'
    radius: '{rounded.md}'
  button-danger:
    background: '{colors.background}'
    foreground: '{colors.danger}'
    border: '{colors.danger}'
    radius: '{rounded.md}'
  field:
    background: '{colors.background}'
    foreground: '{colors.foreground}'
    border: '{colors.border}'
    radius: '{rounded.sm}'
  partial-state:
    foreground: '{colors.partial}'
    font: '{typography.label}'
  done-state:
    foreground: '{colors.done}'
---

# Todo App — Design Spine

The document title is Todo App.

## Brand & Style

This is a morning list for one person, Tom. It should feel like a sheet of paper he can scan at phone width before he leaves, and the same sheet on a desk. The words on the row do the work. Priority is a numeral he reads. "Next" is a label for the first to-do that day that is not done. The product does not dress one row up as the one he must do.

Light surface only. No dark theme. No downloaded font and no component library.

## Colors

Text on `{colors.background}`, and `{colors.primary-foreground}` on `{colors.primary}`, meet WCAG 2.2 AA. Color never replaces a word or a numeral.

- **Paper (`{colors.background}`)** is the page. Rows sit on it. It is not a card grid.
- **Ink (`{colors.foreground}`)** is titles and body.
- **Stone (`{colors.muted}`, `{colors.muted-foreground}`, `{colors.border}`)** is chrome, the Next marker, secondary text, and the alarm time.
- **Pine (`{colors.primary}`, `{colors.primary-foreground}`)** is the one primary action on a surface. It is not used to mark a recommended to-do.
- **Priority (`{colors.priority-1}` to `{colors.priority-5}`)** colors the priority numeral by its value, a single-hue ramp. Priority 1 is stone, 2 is dark stone, 3 is ink, 4 and 5 are rust. The numeral is always present.
- **Priority row (`{colors.priority-1-bg}` to `{colors.priority-5-bg}`)** fills the row. The fills are pale: cool, teal, lime, yellow, orange. They are not the numeral hexes. A wash of those hexes drops "done", "partial", and the 4 numeral under 4.5:1. The page behind the rows stays paper.
- **Partial (`{colors.partial}`)** colors the word "partial" only. The word is always present.
- **Done (`{colors.done}`)** colors a done row's title and the word "done". The word is always present.
- **Danger (`{colors.danger}`)** is Delete, Delete list, and a failed write's `detail` string.
- **Focus (`{colors.focus}`)** is the keyboard focus ring, 2px, offset 2px, on `{colors.background}`.

## Typography

System UI only. `{typography.body}` for titles of to-dos and sentences. `{typography.label}` for priority, state, time, the alarm line, person name, nav, and "Next". `{typography.title}` for the surface name and for the "No date" heading.

One family. No display serif. A to-do title wraps. It is never truncated with an ellipsis on phone width.

## Layout & Spacing

The scale is `{spacing.1}` through `{spacing.6}`. Phone margin is `{spacing.margin-phone}`. Desktop margin is `{spacing.margin-desktop}`. Row padding is `{spacing.3}`. Gap between rows is `{spacing.2}`.

The wide layout starts at 768px. Below 768px the page is one column and the nav is a single row of text links that wraps. At 768px and above, a nav column sits beside the surface. The surface itself stays one reading column, max 40rem. Week, month, and year stay lists. They do not become a wall of day cells.

The current nav link is underlined. The others are not.

## Elevation & Depth

Flat. Rows have a 1px `{colors.border}` and no shadow. The editor on a wide screen is a second column with the same border, not a floating card. Copy review replaces the surface. It does not open a dialog.

## Shapes

`{rounded.md}` on rows, buttons, and the editor. `{rounded.sm}` on the Next marker and on fields. `{rounded.full}` and `{rounded.lg}` are unused. Corners stay quiet so the list reads as lines of work.

## Components

**To-do row.** `{components.todo-row}`. Anatomy, in reading order: priority numeral, title, state word when it is "partial" or "done", time when `at_time` is set, the word Alarm and the time when `alarm_at` is set, person name when set. The alarm line uses `{colors.muted-foreground}` and `{typography.label}`. Notes for a partial to-do sit under the title in `{typography.body}`. Sub-to-dos indent `{spacing.4}` under their parent. A done title uses `{colors.done}`. The row stays on the list.

**Next marker.** The text "Next" in `{components.next-marker}`, with `{spacing.2}` of horizontal padding, placed on the row whose id is `next_todo_id`. It is a label, not a fill of pine.

**Priority.** The numeral 1–5 in `{components.priority-numeral}`, colored by value from `{colors.priority-1}` to `{colors.priority-5}`. The row background is `{colors.priority-1-bg}` through `{colors.priority-5-bg}`. The row is not sorted by this numeral, and priority adds no border or badge.

**Primary button.** `{components.button-primary}`. One primary button on a surface: Save, Confirm copy, Create a list, or Add to-do while the editor is closed.

**Secondary button.** `{components.button-secondary}`. Transparent fill, ink text, 1px `{colors.border}`.

**Danger button.** `{components.button-danger}`. Transparent fill, `{colors.danger}` text and border.

**Field.** `{components.field}`. Full width, 1px border, at least 44px tall. The label sits above the control in `{typography.label}`.

**Partial and done.** The word "partial" uses `{components.partial-state}`. The word "done" and a done title use `{components.done-state}`. No bar, no percent, no count.

## Do's and Don'ts

Do keep a to-do as one row he can read without opening it.

Do show the state as a word.

Do use pine for the one primary action on the surface.

Do pick a day with a date field.

Don't mark a row as recommended, suggested, or quick.

Don't show a progress bar, a percent, a streak, or a celebration when he marks done.

Don't turn week, month, or year into a grid of day cells.

Don't add a sign-in form or a second theme.

Don't draw an alarm icon.

Don't use color as the only sign of partial, done, next, or priority.
