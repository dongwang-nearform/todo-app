---
title: Sprint Change Proposal
status: approved
created: 2026-11-05
project: bmad-example-todo
mode: batch
scope: minor
---

# Sprint Change Proposal: No date section

Approved in the invoking request. The app stays as shipped. This correction only aligns the story and the brief with that screen.

## 1. Issue Summary

Story 4.1 said the period screen shows dated rows and adds no layout region for `undated`. The shipped period screen does the opposite: dated rows first, then a section headed "No date" that lists confirmed to-dos with no `on_date`. The product brief still listed that placement as open.

The same request records a second shipped fact: an alarm is shown and never fired. Story 1.8 already says that. This correction does not edit the alarm.

Evidence:

- `web/src/features/period/PeriodPage.tsx` passes `undated` to a section headed "No date" under the dated rows.
- `EXPERIENCE.md` already specified that section. It also told a later builder to change Story 4.1.
- `docs/ai-integration-log.md` left the epics file for this correction.
- Story 1.8 already stores `alarm_at`, shows it, and states that no alarm fires.

## 2. Impact Analysis

### Epic impact

Epic 4 can still finish on the existing plan. The epic goal and Story 4.1 were the only planning text that forbade the section the app already renders. No epic is added, removed, deferred, or reordered. Epics 1 through 3 are unchanged. Story 1.8 is unchanged.

### Story impact

Story 4.1 is the only story whose acceptance changed. Future stories do not depend on hiding undated rows.

### Artifact conflicts

| Artifact | Result |
| --- | --- |
| `epics.md` | Edited. Story 4.1, the Epic 4 goal, FR-4, and the coverage line now require the "No date" section. |
| Product brief | Edited. The undated-placement open item is closed. Alarm lead time, weekday landing, and the working title stay open. |
| `EXPERIENCE.md` | One sentence edited. It no longer says Story 4.1 must change. The section behavior was already the shipped one. |
| PRD | Not edited. FR-4 notes, MVP scope, and open question 1 still say placement is unstated. |
| Architecture spine | Not edited. The period contract and the Deferred list still say the screen has not decided where `undated` is drawn. |
| Spec | Not edited. It still says Story 4.1's old "no region" line is superseded. |
| App | Not edited. |

### Technical impact

None. No route, payload, schema, or screen change. `GET /api/views/period` already returns `undated`. The period page already renders it under the dated rows. An alarm is stored and shown. Nothing fires it.

## 3. Recommended Approach

**Direct adjustment.** Modify the story and close the brief item. Do not roll back the period screen. Do not cut or expand MVP scope.

The rollback path is not viable. Reverting the "No date" section would throw away the shipped decision in order to match a stale acceptance line.

An MVP review is not viable. The user required the existing app to stay, and the section is already in v1.

Effort is low. Risk to the running app is low. There is no timeline change. The residual risk is documentation drift: the PRD, the architecture spine, and the spec still describe placement as open or as an exception to Story 4.1. A later planning pass can reopen it from those files. This run does not edit them.

## 4. Detailed Change Proposals

Applied.

### Stories

Story: 4.1 Open a day, week, month, or year

Section: Epic goal, requirement text, and acceptance criteria in `epics.md`

OLD:

```
Tom can open each period and see the dated to-dos inside it. The payload can return undated to-dos. The screen placement of those undated rows is still open, so this epic does not invent it.
```

```
So that I can see the dated to-dos in that period.
```

```
**Then** it shows `todos`
**And** it does not add a layout region for `undated`
```

```
**Then** both widths show the same dated to-dos
```

NEW:

```
Tom can open each period and see the dated to-dos inside it. Confirmed to-dos with no date render under those rows in a section headed "No date".
```

```
So that I can see the dated to-dos in that period, and the to-dos with no date under them.
```

```
**Then** it shows `todos` first
**And** under those rows it shows a section headed "No date"
**And** that section lists `undated`
**And** an undated to-do is not placed on a day inside the week, month, or year
```

```
**Then** both widths show the same dated to-dos
**And** both widths show the same "No date" section
```

FR-4's last sentence now states the same placement. The coverage line no longer says placement stays open. The "still not designed" list no longer includes where `undated` is drawn. A to-do with `on_date` and a null `at_time` stays in `todos`. That rule did not change.

Rationale: the acceptance now matches the shipped period screen. The epic file no longer forbids the section the story requires.

### Brief

Section: Scope in `brief.md`

OLD:

```
Still open, and not deferred to a later version: where a to-do with no time appears in the week, month, and year views; how early an alarm fires; which list or day a weekday morning lands on. The user-facing name is still "Todo App."
```

NEW:

```
A to-do with no date appears in the day, week, month, and year views in a "No date" section under the dated rows. That placement is closed.

Still open, and not deferred to a later version: how early an alarm fires; which list or day a weekday morning lands on. The user-facing name is still "Todo App."
```

Rationale: the open item was undated placement. It is closed against the shipped section. The other open items stay open. "No date" means no `on_date`, which is the `undated` array. A dated to-do with no clock time stays on its date.

### UI/UX

Section: Undated to-dos in `EXPERIENCE.md`

OLD:

```
Story 4.1 currently says the period screen does not add a layout region for `undated`. This spine adds that region. The story acceptance criterion has to change before a builder can satisfy both.
```

NEW:

```
Story 4.1 matches this section: dated rows first, then undated rows under the heading "No date".
```

Rationale: the behavior text was already correct. The leftover instruction would have reopened Story 4.1.

### Alarm

No edit. Story 1.8 already requires `alarm_at` to be stored and shown, and it requires that no alarm fires. The brief's question about how early an alarm fires stays open.

### PRD and architecture

No edit. Recorded here so the drift is visible.

- PRD FR-4 notes: "Where a to-do with no time appears in these views is unstated."
- PRD §6 and open question 1: placement is still open.
- Architecture period row: "The screen does not yet decide where `undated` is drawn."
- Architecture Deferred: "Placement is still open."
- Spec: Story 4.1's old line is still described as superseded.

## 5. Implementation Handoff

**Scope: Minor.**

No implementation handoff. The screen and the alarm behavior already shipped. Success is the document alignment below, and it is met.

Success criteria:

- Story 4.1 requires the "No date" section under the dated rows.
- The brief no longer lists undated placement as open.

Out of this handoff: app code, a new epic, alarm delivery, alarm lead time, weekday landing, the working title, and edits to the PRD, the architecture spine, or the spec.

## Checklist

1. Trigger and context — [x] Done. Trigger is Story 4.1 against the shipped "No date" section. The alarm fact is already in Story 1.8.
2. Epic impact — [x] Done. Epic 4 text updated. No other epic changes. Order unchanged.
3. Artifact conflicts — [x] Done for the story, the brief, and the stale UX instruction. [!] PRD, architecture spine, and spec still describe placement as open or overridden. Left unchanged on purpose.
4. Path forward — [x] Done. Direct adjustment. Rollback not viable. MVP review not viable.
5. Proposal components — [x] Done. This document.
6. Review and handoff — [x] Done. Approved by the invoking request, limited to this alignment. No `sprint-status.yaml` exists, and no epic or story was added or removed, so that update is [N/A]. No developer handoff.
