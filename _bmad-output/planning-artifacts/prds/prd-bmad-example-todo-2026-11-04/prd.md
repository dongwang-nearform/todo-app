---
title: Todo App
status: draft
created: 2026-11-04
updated: 2026-11-04
---

# PRD: Todo App

*Working title — confirm. Coaching draft: only confirmed sections are filled.*

## 1. Vision

This is a responsive website for one person. There is no native phone app. Tom keeps the lists. His daughter and his wife appear as names on his to-dos, not as people who sign in.

On a weekday morning he opens the website, including at phone width, chooses a high-priority to-do he can finish quickly, and marks it done. If work is blocked or has several parts, he marks it done and creates a new to-do, or he adds sub-to-dos. He can mark a to-do partial and record notes without marking it done. If it is time-bound, he sets an alarm. On Saturday he opens Today and follows the order, including other people's fixed times, and he checks what is next even when he does not mark a to-do done. Those Saturday to-dos are there because he copied them from another to-do list and confirmed the copy. The product does not add them.

The product exists so a packed day and an ordinary morning use the same to-do list. Finished or not, every to-do that is not done remains visible across all time. Day, week, month, and year views remain alongside that all-time not-done view. `[ASSUMPTION: day, week, month, and year views remain alongside the all-time not-done view.]` `[ASSUMPTION: the all-time not-done view is part of the purpose, not a later nice-to-have.]`

## 2. Target User

### 2.1 Jobs To Be Done

- **Weekday morning:** choose a high-priority to-do he can finish quickly, do it, and mark it done. Realizes UJ-1.
- **Blocked or multi-part work:** wait, then either mark it done and create a new to-do, or add sub-to-dos. Realizes UJ-1.
- **Time-bound work:** set an alarm. Realizes UJ-1.
- **Partial work:** mark a to-do partial and record notes, without marking it done. Partial is the state. There is no progress number.
- **Saturday:** copy to-dos from another to-do list, confirm the copy, then open Today and see what is next even when he does not mark them done. The product does not add those to-dos. Realizes UJ-2.
- **Open work:** see every to-do that is not done yet, across all time, and also by day, week, month, and year.
- **Other people:** keep his daughter's lessons and the Costco trip on his own to-dos. His daughter and his wife do not use the app. Realizes UJ-2.

### 2.2 Non-Users (v1)

- Tom's daughter and Tom's wife can be named on his to-dos. They do not have their own use of the app in v1.

### 2.3 Key User Journeys

**UJ-1. Tom starts the day by finishing what is high priority and quick.**

- **Persona + context:** Tom, every morning after he gets up. He uses the responsive website, including at phone width, to decide what to do first. There is no native phone app.
- **Entry state:** He has just gotten up and opens the website. He is not asked to sign in. Which to-do list or day he lands on is unstated.
- **Path:**
  1. He checks the app for to-dos that are important or high priority and quick to finish.
  2. He chooses one of those and does it first. The app does not auto-pick it.
  3. When he finishes it, he marks it done.
  4. If the job has several parts, or he is waiting on someone else, he waits. He then either marks this to-do done and creates a new to-do, or creates sub-to-dos. Both moves stay available.
  5. If he decides the to-do is time-bound, he sets an alarm.
- **Climax:** The quick, high-priority to-do is finished and marked done.
- **Resolution:** That to-do is done. Blocked or multi-part work is either a new to-do or sub-to-dos. Time-bound work has an alarm.
- **Edge case:** Waiting on another person. He does not leave the original to-do unchanged. He marks it done and creates a new to-do, or he breaks it into sub-to-dos.

**UJ-2. Tom runs Saturday from today's list by checking what is next.**

- **Persona + context:** Tom, every Saturday. His daughter has English and ballet. His wife goes to Costco with him. He is busy, so he may not mark to-dos done while the day is in motion. Mark-done from UJ-1 still exists.
- **Entry state:** He has just gotten up. The first thing he opens is Today on the responsive website. The stops are already there because he copied them from another to-do list and confirmed the copy. The product did not add them.
- **Path:**
  1. He checks today's list and reads each stop as its own to-do, in order: drop his daughter off at English at 9:00am; pick her up at 10:00am; go home and rest; go to Costco with his wife; drop his daughter off at ballet at 1:00pm; pick her up when ballet ends at 2:30pm. `[ASSUMPTION: ballet pickup is at 2:30pm, when the lesson ends.]`
  2. He does the day in that order.
  3. He may not mark each to-do done.
  4. He regularly opens the to-do list to see what is next.
- **Climax:** While the day is still going, the to-do list tells him the next stop.
- **Resolution:** Some or all of the to-dos may still be not done. Today holds the stops he copied and confirmed. The product will not place them on a later Saturday by itself.
- **Edge case:** He is too busy to mark to-dos done, and "what is next" is still obvious. The earlier 8:00am English time is withdrawn. Saturday English is drop-off at 9:00am and pickup at 10:00am.

## 3. Glossary

Terms below are the only names for these nouns. "Task" and "item" are not used.

- **To-do** — a single piece of work Tom owns. It is done, not done, or partial. It may have a priority, a time, an alarm, notes, and sub-to-dos.
- **Sub-to-do** — a to-do that belongs to another to-do.
- **To-do list** — a named collection of to-dos. Tom has more than one. A to-do list contains many to-dos.
- **Today** — today's to-dos, in order. UJ-2 opens this first.
- **Not-done view** — every to-do that is not done, across all time. A partial to-do is included. A done to-do is not.
- **Day, week, month, and year views** — to-dos bounded to that period. They sit beside the not-done view.
- **Priority** — an integer on a to-do from 1 to 5. 5 is highest. 1 is lowest.
- **Done** — Tom has marked the to-do finished. On Saturday he may leave a to-do not done on purpose.
- **Partial** — the state of a to-do that is neither done nor not done. The word is "partial." There is no progress number, percent, or count. Notes may be recorded on it.
- **Copy** — Tom's manual act of bringing to-dos from one to-do list onto another. The copies are not added until he confirms.

## 4. Features

Capabilities below are on one responsive website, usable at phone width and at desktop width. There is no native phone app. "Quick to finish" is Tom's judgment, not a field on the to-do. The product does not add to-dos by itself.

### 4.1 Lists and views

**Description:** Tom can see his to-do lists, open Today in order, see what is next, open the not-done view, and open a day, week, month, or year view. Realizes UJ-2 and the open-work job.

**Functional Requirements:**

#### FR-1: See every to-do list

Tom can see every to-do list he has.

**Consequences (testable):**
- A to-do list Tom created is visible in the collection of to-do lists.
- A second to-do list appears there as its own list.

#### FR-2: Open Today in order

Tom can open Today and see that day's to-dos in order, including what is next.

**Consequences (testable):**
- Today shows the current date's to-dos in list order.
- Tom can identify the next to-do from that order.

#### FR-3: Not-done view

Tom can open the not-done view and see every to-do that is not done, across all time.

**Consequences (testable):**
- A not-done to-do from another date appears in the not-done view.
- A partial to-do appears in the not-done view.
- A done to-do does not appear in the not-done view.

#### FR-4: Day, week, month, and year views

Tom can open a day view, a week view, a month view, and a year view.

**Consequences (testable):**
- A to-do with a time appears in the day, week, month, and year that contain that time.
- A to-do outside the selected period does not appear in that period's view.

**Notes:** Where a to-do with no time appears in these views is unstated.

### 4.2 To-do lifecycle

**Description:** Tom can create, update, and delete a to-do, mark it done, mark it not done, or mark it partial and record notes. Today still shows what is next when he leaves to-dos not done. Realizes UJ-1 and UJ-2.

**Functional Requirements:**

#### FR-5: Create, update, and delete

Tom can create a to-do, update it, and delete it. `[ASSUMPTION: delete stays, from the original dump. No journey showed it.]`

**Consequences (testable):**
- A created to-do appears on the to-do list Tom put it on.
- An update to its name, time, or priority is what he sees afterward.
- A deleted to-do no longer appears on any to-do list or view.

#### FR-6: Mark done and mark not done

Tom can mark a to-do done, and mark a done to-do not done. `[ASSUMPTION: marking not done stays, from the original dump.]`

**Consequences (testable):**
- Marking a to-do done removes it from the not-done view.
- Marking that to-do not done returns it to the not-done view.

#### FR-7: What is next without marking done

Today shows what is next even when the day's to-dos are not done. Realizes UJ-2.

**Consequences (testable):**
- With every Saturday to-do still not done, Today still shows those to-dos in order and which one is next.

#### FR-17: Partial and notes

Tom can mark a to-do partial and record notes on it, without marking it done. Partial is the whole state. There is no progress number.

**Consequences (testable):**
- A partial to-do is distinct from a done to-do and from a to-do he has not started.
- The to-do shows "partial." It does not show a percent, a count, or a progress score.
- Notes saved on it are still there when he returns.
- A partial to-do stays in the not-done view.

### 4.3 Priority

**Description:** Each to-do has a priority from 1 to 5. 5 is highest. 1 is lowest. Tom chooses which high-priority to-do to do first. Realizes UJ-1.

**Functional Requirements:**

#### FR-8: Set priority

Tom can set a priority on each to-do. The only values are 1, 2, 3, 4, and 5. 5 is highest. 1 is lowest.

**Consequences (testable):**
- A to-do rejects a priority outside 1 through 5.
- A priority of 5 outranks a priority of 1.
- Tom can change a to-do's priority, and the new priority is what he sees.

#### FR-9: Tom chooses what to do first

Tom chooses which high-priority to-do to do first. The product does not choose for him. Realizes UJ-1.

**Consequences (testable):**
- When more than one high-priority to-do is not done, the product does not select one of them as the one he must do.

### 4.4 Blocked work

**Description:** When a to-do has several parts, or Tom is waiting on someone, he can add sub-to-dos, or mark it done and create a new to-do. Both stay available. Realizes UJ-1.

**Functional Requirements:**

#### FR-10: Sub-to-dos

Tom can add sub-to-dos to a to-do.

**Consequences (testable):**
- Sub-to-dos are visible with the to-do they belong to.
- Adding sub-to-dos does not remove the option to mark that to-do done and create a new to-do.

#### FR-11: New to-do after done

Tom can mark a to-do done and create a new to-do. Realizes UJ-1.

**Consequences (testable):**
- After he marks a to-do done, he can create a new to-do.
- He can do this instead of adding sub-to-dos, and he can add sub-to-dos instead of this. Neither path removes the other.

### 4.5 Time

**Description:** A to-do can have a time and an alarm. Saturday's to-dos arrive only when he copies them from another to-do list and confirms. Realizes UJ-1 and UJ-2.

**Functional Requirements:**

#### FR-12: Set a time

Tom can set a time on a to-do.

**Consequences (testable):**
- The English drop-off can be stored at 9:00am and the pickup at 10:00am.
- The ballet drop-off can be stored at 1:00pm and the pickup at 2:30pm.

#### FR-13: Set an alarm

Tom can set an alarm on a time-bound to-do.

**Consequences (testable):**
- A time-bound to-do can have an alarm set on it.
- A to-do with no time is not required to have an alarm.

**Notes:** How far ahead the alarm fires is unstated.

#### FR-14: Add to a calendar

Out of scope for v1. Tom cannot add a to-do to Google Calendar, Apple Calendar, or any other calendar. This product does not keep a calendar.

**Consequences (testable):**
- No to-do offers an add-to-calendar action.
- The product does not create a to-do from a calendar event.

#### FR-15: Copy, then confirm

Tom can copy to-dos from one to-do list onto another, including onto Saturday's Today. The product does not add to-dos by itself. Copied to-dos are not added until Tom confirms.

**Consequences (testable):**
- A copy that Tom has not confirmed does not appear on the destination to-do list.
- After he confirms, the copied to-dos appear on the destination.
- A later Saturday does not receive those to-dos unless Tom copies and confirms again.
- No other action creates a to-do without Tom creating it or confirming a copy.

### 4.6 People on a to-do

**Description:** Tom can name his daughter or his wife on a to-do. They do not use the app. Realizes UJ-2.

**Functional Requirements:**

#### FR-16: Name a person who is not a user

Tom can name another person on a to-do. That person cannot use the app in v1. Realizes UJ-2.

**Consequences (testable):**
- A to-do can show his daughter's name or his wife's name.
- That person has no sign-in and no view of the to-do.

## 5. Non-Goals (Explicit)

- A person named on a to-do does not get an account, a shared to-do list, or a way to mark a to-do done in v1.
- The product does not choose which high-priority to-do Tom does first.
- v1 is one responsive website. It is not a native phone app, a native desktop app, a public API, or a hardware device.
- The product does not automatically add to-dos. A copy does not land until Tom confirms it.
- v1 has no authentication and no sign-in. Tom is not asked to identify himself.
- v1 has no calendar. A to-do cannot be added to Google Calendar, Apple Calendar, or a calendar inside this product.
- "Quick to finish" is not stored on the to-do.

## Platform

- One website. The same capabilities are usable at phone width and at desktop width.
- No native iOS or Android app in v1.

## 6. MVP Scope

v1 is the full confirmed set, including partial and notes. Native phone support is removed.

### 6.1 In Scope

- FR-1 through FR-17, except FR-14, on one responsive website.
- UJ-1 and UJ-2.

### 6.2 Out of Scope for MVP

- A person named on a to-do does not get an account, a shared to-do list, or a way to mark a to-do done.
- The product does not choose which high-priority to-do Tom does first.
- A native phone app, a native desktop app, a public API, and hardware.
- Automatic creation of to-dos, including automatic Saturday fill.
- Authentication and sign-in.
- Any calendar add, including Google Calendar and Apple Calendar. FR-14 is withdrawn.
- A stored "quick to finish" field.

Still open, and not deferred scope: where a to-do with no time appears in a period view, and how early an alarm fires.

## 7. Success Metrics

No usage target was supplied. These measure whether the two journeys and the not-done view work. They are not growth numbers.

**Primary**

- **SM-1:** On the responsive website, including at phone width, Tom completes UJ-1: he chooses a high-priority to-do and marks it done. Target: he can do this. Validates FR-6, FR-8, FR-9. There is no native phone app in this measure.
- **SM-2:** Saturday Today shows UJ-2's stops in order and what is next while those to-dos are not done, after Tom has copied and confirmed them. Target: he can do this. Validates FR-2, FR-7, FR-12, FR-15.

**Secondary**

- **SM-3:** The not-done view includes a not-done to-do from another day, includes a partial to-do, and excludes a done to-do. Target: all three are true. Validates FR-3, FR-17.

**Counter-metrics (do not optimize)**

- **SM-C1:** Saturday mark-done rate. UJ-2 succeeds when to-dos stay not done and Tom still knows what is next. Raising Saturday completion can mean the weekday habit is being pushed onto the packed day. Counterbalances SM-1.

## 8. Open Questions

Deferred. They do not block architecture. Owner: PM. Revisit when a builder would otherwise invent the behavior.

1. Where a to-do with no time appears in the week, month, and year views. Revisit when those views are designed.
2. How early an alarm fires. Revisit when the alarm is designed.
3. Working title is still "Todo App." Revisit before a user-facing name ships.

## 9. Assumptions Index

- Day, week, month, year, and the not-done view are in v1. Confirmed with the vision.
- Delete, and marking a done to-do not done, are in v1. Confirmed with FR-5 and FR-6.
- No authentication and no calendar in v1. Confirmed when those were removed. Alarm stays.
- Ballet pickup is at 2:30pm because the lesson ends then. `[ASSUMPTION: pickup and the lesson end are the same clock.]`
