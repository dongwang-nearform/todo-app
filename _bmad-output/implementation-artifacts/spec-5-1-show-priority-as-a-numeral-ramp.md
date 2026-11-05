---
title: 'Show priority as a numeral ramp'
type: 'feature'
created: '2026-11-05'
status: 'done'
baseline_commit: '888131c9d90d6210adbfc0cb2602d9f39b34c554'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/planning-artifacts/ux-designs/ux-bmad-example-todo-2026-11-04/DESIGN.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The priority numeral is ink for 1 to 4 and rust only for 5. Tom cannot read the middle of the range by color, and the 5-only rule does not match the signed-off ramp in `DESIGN.md`.

**Approach:** Color the numeral by its value using `priority-1` through `priority-5` from `DESIGN.md`. Fill the row with the pale `priority-N-bg` token for that value.

## Boundaries & Constraints

**Always:** The numeral text is always present. Each priority value maps to one token and one class. Priority stays an integer from 1 to 5, and the API is unchanged. Row order, the Next marker, state words, and meta text are unchanged. A done or partial row keeps its priority color, because the spine colors only the title and the state word for those states.

**Never:** No priority border or badge. No sorting by priority. No use of the numeral hex as a row fill. No server, schema, or route change. No code comments that cite stories, epics, or AI workflow.

</frozen-after-approval>

## Code Map

- `web/src/index.css` -- `:root` token `--color-priority-high` (line 9) and the `.priority-high` rule (about line 222). These become five tokens and five classes.
- `web/src/features/todo-editor/TodoListView.tsx` -- `RowBody` builds the numeral's class with `todo.priority === 5`. This becomes `priority priority-${todo.priority}`.
- `web/src/features/todo-editor/TodoListView.test.tsx` -- existing tests use testing-library and the `todo()` fixture from `web/src/test/todo.ts`. The new priority test goes here.
- `web/src/api/client.ts` -- `TodoOut.priority: number`. Reference only. Do not change.

## Tasks & Acceptance

**Execution:**
- [x] `web/src/features/todo-editor/TodoListView.test.tsx` -- add a failing test first: for priorities 1 to 5, the numeral text is the value and its class is `priority priority-N`. Red first.
- [x] `web/src/index.css` -- replace `--color-priority-high` with `--color-priority-1` through `--color-priority-5`, using the `DESIGN.md` values. Replace `.priority-high` with `.priority-1` through `.priority-5`. One token and one class per value.
- [x] `web/src/features/todo-editor/TodoListView.tsx` -- set the numeral class to `priority priority-${todo.priority}` in `RowBody`. Remove the 5-only conditional.

**Acceptance Criteria:**
- Given a to-do with priority 1, 2, 3, 4, or 5, when the list renders, then the numeral shows that value with class `priority-N`.
- Given any priority, when the row renders, then the row background is `priority-N-bg` and priority adds no border or badge.
- Given a to-do with priority 5 and a to-do with priority 1, both not done, when the list renders, then row order and the Next marker are unchanged.
- Given each of the five colors on `--color-background` for 13px label text, when the contrast is measured, then each is at least 4.5:1.
- Given this change ships, then no route, schema, or validation changes.

## Verification

**Commands:**
- `cd web && npx vitest run src/features/todo-editor/TodoListView.test.tsx` -- expected: the new priority test passes after the red step.
- `cd web && npm test` -- expected: all tests pass.
- `cd web && npm run lint` -- expected: no errors.
- `cd web && npm run build` -- expected: `tsc -b` and `vite build` succeed.

**Manual checks (if no CLI):**
- At phone width and desktop width, a list with priorities 1 through 5 shows five numeral colors. Priorities 1 and 2 look close, and so do 4 and 5, so read the numeral itself.
- In grayscale, every numeral is still readable.

## Implementation Notes

- Baseline `888131c`. Production change: the numeral class is `priority priority-N` for every row, and `.priority-1` through `.priority-5` replace `.priority-high`.
- Live Today list not walked: the API and Vite were not running. Phone width was not applied in the static check, so the manual phone and desktop check above is still open.
- Priority 4 sits at 4.79:1. It passes 4.5:1, but a later token edit could drop it below.
- 2026-11-05 follow-up: the user asked for row backgrounds. The numeral hexes cannot be the fill. Pale washes are `priority-1-bg` #F0F9FF through `priority-5-bg` #FFF7ED. The row class is `priority-row-N`. Numeral classes stay.

## Review Triage Log

Review ran with three reviewers: blind hunter (3 minimum findings, returned 7), edge-case hunter (1), verification-gap (none).

| # | Source | Finding | Verdict | Route and evidence |
| --- | --- | --- | --- | --- |
| 1 | blind | Test checks only `className`, so a missing `.priority-N` rule would still pass | low | Rejected. Every rule is present in the diff. The test cannot read CSS, so a fix needs a CSS-parsing test, which adds complexity. |
| 2 | blind | Test fixture misses done and partial rows | low | Patch applied as a test-only hardening. The code already keeps the color on those rows, so no bad outcome occurs today. The spec's Always rule requires it, so the test now covers a done row at priority 1 and a partial row at priority 5. |
| 3 | blind | Test fixture misses sort order and the Next marker | false | This diff touches neither the sort nor the Next marker, and the existing tests cover both. |
| 4 | blind | Acceptance wording says `priority-N`, the task says `priority priority-N`, and the criteria omit the hexes and removal of the old rules | low | Rejected. Its fix edits the spec, which the triage rules exclude. Removal and hexes are in Tasks. |
| 5 | blind | Sprint status still `in-progress` while the spec is `in-review` | low | Patch applied directly. `5-1` is now `review`. |
| 6 | blind | Priority 4 at 4.79:1 is thin | false | Measured at 4.79:1, which passes 4.5:1. A future token edit is a spec-level concern, recorded in Implementation Notes. |
| 7 | edge | Priority outside 1 to 5 would produce `priority-0` and an uncolored numeral | low | Rejected. The server rejects any priority outside 1 to 5 (FR-8). The guard adds a branch the contract makes unreachable. |
| 8 | blind | Numerals are hidden under 768px when the editor is open | false | Pre-existing. `index.css` hides `.editor-open .list-body` under 767px. This diff does not touch it. |
| 9 | verification-gap | No gaps | none | Nothing to route. |

No intent gap, no bad spec, no loopback. `review_loop_iteration` stays `0`.
