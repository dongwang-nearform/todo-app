---
title: Todo App
status: final
created: 2026-11-04
updated: 2026-11-05
---

# PRD: Todo App

*Working title. See §8.*

## 1. Vision

This PRD describes shipped v1: one responsive website for one person. Tom keeps the lists. His daughter and his wife appear as names on his to-dos, not as people who sign in.

UJ-1 is the weekday morning. He chooses a high-priority to-do he can finish quickly and marks it done. He can split blocked work, mark a to-do partial, or set an alarm. UJ-2 is Saturday. He opens Today, follows the order of the to-dos he copied from another to-do list and confirmed, and checks Next even when he does not mark a to-do done.

The product exists so a packed day and an ordinary morning use the same to-do list. Every to-do that is not done remains visible across all time. Day, week, month, and year views remain alongside that all-time not-done view.

## 2. Target User

### 2.1 Jobs To Be Done

- **Weekday morning:** choose a high-priority to-do he can finish quickly, do it, and mark it done. Realizes UJ-1.
- **Blocked or multi-part work:** wait, then either mark it done and create a new to-do, or add sub-to-dos. Realizes UJ-1.
- **Time-bound work:** set an alarm. Realizes UJ-1.
- **Partial work:** mark a to-do partial and record notes, without marking it done. No journey. Realizes FR-17.
- **Saturday:** copy to-dos from another to-do list, confirm the copy, then open Today and see Next even when he does not mark them done. Realizes UJ-2.
- **Open work:** see every to-do that is not done yet, across all time, and also by day, week, month, and year. No journey. Realizes FR-3 and FR-4.
- **Other people:** keep his daughter's lessons and the Costco trip on his own to-dos. His daughter and his wife do not use the app. Realizes UJ-2.

### 2.2 Non-Users (v1)

- Tom's daughter and Tom's wife can be named on his to-dos. They do not use the app in v1.

### 2.3 Key User Journeys

**UJ-1. Tom starts the day by finishing what is high priority and quick.**

- **Persona + context:** Tom, every morning after he gets up. He uses the responsive website, including at phone width, to decide what to do first.
- **Entry state:** He has just gotten up and opens the website. It opens on Today. He is not asked to sign in.
- **Path:**
  1. He checks the app for to-dos that are high priority and quick to finish.
  2. He chooses one of those and does it first. The app does not auto-pick it.
  3. When he finishes it, he marks it done.
  4. If the to-do has several parts, or he is waiting on someone else, he waits. He then either marks this to-do done and creates a new to-do, or creates sub-to-dos. Both moves stay available.
  5. If he decides the to-do is time-bound, he sets an alarm.
- **Climax:** The quick, high-priority to-do is finished and marked done.
- **Resolution:** That to-do is done. Blocked or multi-part work is either a new to-do or sub-to-dos. Time-bound work has an alarm. The alarm is shown on the to-do and is never fired.
- **Edge case:** Waiting on another person. He does not leave the original to-do unchanged. He marks it done and creates a new to-do, or he breaks it into sub-to-dos.

**UJ-2. Tom runs Saturday from Today by checking what is next.**

- **Persona + context:** Tom, every Saturday. His daughter has English and ballet. His wife goes to Costco with him. He is busy, so he may not mark to-dos done while the day is in motion. Mark-done from UJ-1 still exists.
- **Entry state:** He has just gotten up. The website opens on Today. The to-dos are already there because he copied them from another to-do list and confirmed the copy. The product did not add them.
- **Path:**
  1. He checks Today and reads each to-do in order: drop his daughter off at English at 9:00 AM; pick her up at 10:00 AM; go home and rest; go to Costco with his wife; drop his daughter off at ballet at 1:00 PM; pick her up when ballet ends at 2:30 PM. `[ASSUMPTION: ballet pickup is at 2:30 PM, when the lesson ends.]`
  2. He does the day in that order.
  3. He may not mark each to-do done.
  4. He regularly opens Today to see what is next.
- **Climax:** While the day is still going, Today shows Next on the next to-do.
- **Resolution:** Some or all of the to-dos may still be not done. Today holds the to-dos he copied and confirmed. The product will not place them on a later Saturday by itself.
- **Edge case:** He is too busy to mark to-dos done. Next is still the first to-do in Today's order that is not done.

## 3. Glossary

Terms below are the only names for these nouns. "Task" and "item" are not used.

- **To-do** — a single piece of work Tom owns. It has a title. It is done, not done, or partial. It may have a priority, a date, a time, an alarm, notes, a named person, and sub-to-dos.
- **Title** — the words that name a to-do. This is not the person named on it.
- **Date** — the calendar day on a to-do, when it has one. A to-do with no date is undated.
- **Time** — the clock time on a to-do, such as 9:00 AM. It is not the date.
- **Time-bound** — a to-do that has a time.
- **Alarm** — a clock time of its own, shown on a time-bound to-do. It can differ from that to-do's time. It is never fired.
- **No date** — the section under the dated rows on a day, week, month, or year view. It holds undated to-dos.
- **Sub-to-do** — a to-do that belongs to another to-do. It can belong to a sub-to-do. It has its own title, state, priority, date, time, and alarm.
- **To-do list** — a named collection of to-dos. Tom has more than one. A to-do list contains many to-dos.
- **Today** — confirmed to-dos, from every to-do list, whose date is the date the website is using as today. They appear in the order Tom set. The website opens here. Today is not a to-do list. UJ-2 opens this first.
- **Next** — the first to-do in Today's order whose state is not done. A partial to-do can be Next. That row shows the word "Next". If every to-do on Today is done, there is no Next.
- **Not-done view** — every confirmed to-do that is not done, across all time, including a to-do with no date. A partial to-do is included. A done to-do is not.
- **Day, week, month, and year views** — to-dos bounded to that period, shown as dated rows, with undated to-dos in No date under those rows. A week is Monday through Sunday. They sit beside the not-done view. They are not Today.
- **Priority** — an integer on a to-do from 1 to 5. 5 is highest. 1 is lowest. The product shows the number. It does not sort or filter by it.
- **High-priority** — Tom's judgment of a priority number while he decides what to do first. The product does not define a cutoff.
- **Done** — Tom has marked the to-do finished. On Saturday he may leave a to-do not done on purpose.
- **Partial** — a state beside done and not done. A partial to-do counts as not done in the not-done view and can be Next. The word is "partial." There is no progress number, percent, or count. Notes may be recorded on it.
- **Copy** — Tom's manual act of bringing every confirmed to-do from one to-do list onto another, with one date he sets for that copy. The copies are not added until he confirms.

## 4. Features

Capabilities below are on one responsive website, usable at phone width and at desktop width. One set of to-dos: both widths show the same to-dos, and anyone who opens the website can see and edit them. "Quick to finish" is Tom's judgment, not a field on the to-do.

### 4.1 Lists and views

**Description:** Tom can see his to-do lists, open Today in order, see Next, open the not-done view, and open a day, week, month, or year view. Realizes UJ-2 and the open-work job.

**Functional Requirements:**

#### FR-1: See every to-do list

Tom can see every to-do list he has. He can create a to-do list, rename it, and delete it.

**Consequences (testable):**
- A to-do list Tom created is visible in the collection of to-do lists.
- A second to-do list appears there as its own list.
- A renamed to-do list shows the new name.
- Deleting a to-do list removes that list and its to-dos, and leaves every other to-do list in place.

#### FR-2: Open Today in order

Tom can open Today and see that day's confirmed to-dos in the order he set, including Next. Today is not a to-do list. The website opens on Today.

**Consequences (testable):**
- Today shows confirmed to-dos from every to-do list whose date is the date the website is using as today. That date comes from the browser. The product stores no timezone.
- Tom can move a to-do up or down. Today uses that order.
- Next is the first to-do in that order that is not done, including a partial to-do, and that row shows "Next".
- When every to-do on Today is done, no row shows "Next".
- Today does not include an undated to-do. Undated to-dos appear in No date on the period views.

#### FR-7: What is next without marking done

Today shows Next even when the day's to-dos are not done. Next is as defined in the Glossary. Realizes UJ-2.

**Consequences (testable):**
- With every Saturday to-do still not done, Today still shows those to-dos in order, and Next is the first of them.

#### FR-3: Not-done view

Tom can open the not-done view and see every to-do that is not done, across all time.

**Consequences (testable):**
- A not-done to-do from another date appears in the not-done view.
- A partial to-do appears in the not-done view.
- A done to-do does not appear in the not-done view.

#### FR-4: Day, week, month, and year views

Tom can open a day view, a week view, a month view, and a year view.

**Consequences (testable):**
- A to-do with a date appears in the dated rows of the day, week, month, and year that contain that date.
- A to-do outside the selected period does not appear in that period's dated rows.
- An undated to-do appears under the heading "No date", beneath those dated rows, on the day view, the week view, the month view, and the year view.
- No date is part of the period view that is open. It is not its own view. Changing the period does not remove the undated to-dos from No date.
- A week runs Monday through Sunday and contains the date he is viewing. A month is that calendar month. A year is that calendar year.

### 4.2 To-do lifecycle

**Description:** Tom can create, update, and delete a to-do, mark it done, mark it not done, or mark it partial and record notes. Realizes UJ-1.

**Functional Requirements:**

#### FR-5: Create, update, and delete

Tom can create a to-do, update it, and delete it.

**Consequences (testable):**
- A created to-do appears on the to-do list Tom put it on.
- An update to its title, date, time, or priority is what he sees afterward. He can set a date and he can clear it.
- A deleted to-do no longer appears on any to-do list or view. Deleting a to-do also deletes its sub-to-dos.

#### FR-6: Mark done and mark not done

Tom can mark a to-do done, and mark a done to-do not done.

**Consequences (testable):**
- Marking a to-do done removes it from the not-done view.
- Marking that to-do not done returns it to the not-done view.

#### FR-17: Partial and notes

Tom can mark a to-do partial and record notes on it, without marking it done. Partial is the whole state. There is no progress number.

**Consequences (testable):**
- A partial to-do is distinct from a done to-do and from a not-done to-do.
- The to-do shows "partial." It does not show a percent, a count, or a progress score.
- Notes saved on it are still there when he returns.
- A partial to-do stays in the not-done view.

### 4.3 Priority

**Description:** Tom sets a priority and chooses which to-do to do first. Realizes UJ-1.

**Functional Requirements:**

#### FR-8: Set priority

Tom can set a priority on each to-do. The only values are 1, 2, 3, 4, and 5. 5 is highest. 1 is lowest.

**Consequences (testable):**
- A to-do rejects a priority outside 1 through 5.
- A priority of 5 outranks a priority of 1. The product shows 5 as the highest. It shows each priority as its number.
- Tom can change a to-do's priority, and the new priority is what he sees.
- The product does not sort or filter the list to high-priority to-dos.

#### FR-9: Tom chooses what to do first

Tom chooses which high-priority to-do to do first. The product does not choose for him. Realizes UJ-1.

**Consequences (testable):**
- When more than one high-priority to-do is not done, the product does not select one of them as the one he must do.

### 4.4 Blocked work

**Description:** When work is blocked, both paths stay available: sub-to-dos, or mark done and create a new to-do. Realizes UJ-1.

**Functional Requirements:**

#### FR-10: Sub-to-dos

Tom can add sub-to-dos to a to-do.

**Consequences (testable):**
- Sub-to-dos are visible with the to-do they belong to.
- A sub-to-do keeps its own state, priority, date, time, and alarm.
- A sub-to-do may belong to another sub-to-do, and that nested sub-to-do is still shown.
- Deleting a to-do deletes its sub-to-dos.
- Adding sub-to-dos does not remove the option to mark that to-do done and create a new to-do.

#### FR-11: New to-do after done

Tom can mark a to-do done and create a new to-do. Realizes UJ-1.

**Consequences (testable):**
- After he marks a to-do done, he can create a new to-do.
- He can do this instead of adding sub-to-dos, and he can add sub-to-dos instead of this. Neither path removes the other.

### 4.5 Time

**Description:** A to-do can have a time and an alarm. Realizes UJ-1.

**Functional Requirements:**

#### FR-12: Set a time

Tom can set a time on a to-do.

**Consequences (testable):**
- The English drop-off can be stored at 9:00 AM and the pickup at 10:00 AM.
- The ballet drop-off can be stored at 1:00 PM and the pickup at 2:30 PM.

#### FR-13: Set an alarm

Tom can set an alarm on a time-bound to-do.

**Consequences (testable):**
- A time-bound to-do can have an alarm set on it. The alarm is its own clock time and can differ from the to-do's time.
- The alarm is shown on that to-do.
- The alarm is never fired. When that time arrives, the product does not send or play anything.
- A to-do with no time cannot have an alarm.

#### FR-14: Add to a calendar

Withdrawn. See §5.

### 4.6 Copy

**Description:** Saturday's to-dos arrive only when Tom copies them from another to-do list and confirms. Realizes UJ-2.

**Functional Requirements:**

#### FR-15: Copy, then confirm

Tom can copy every confirmed to-do from one to-do list onto another and set one date for that copy. Copied to-dos are not added until Tom confirms. Today then shows them when that date is the date the website is using as today.

**Consequences (testable):**
- The copy includes every confirmed to-do on the source to-do list. Tom does not pick a subset. An unconfirmed to-do on the source is not copied.
- Each copy keeps the source to-do's title, state, priority, notes, time, alarm, named person, order, and sub-to-do relationships. Every copied to-do takes the date Tom set for the copy.
- A copy that Tom has not confirmed does not appear on the destination to-do list, on Today, in the not-done view, or on a period view. The product does not offer a way to cancel. Leaving it unconfirmed keeps it hidden.
- After he confirms, the copied to-dos appear on the destination. Confirming that same copy again does not add a second set.
- A later Saturday does not receive those to-dos unless Tom copies and confirms again.
- No other action creates a to-do without Tom creating it or confirming a copy.

### 4.7 People on a to-do

**Description:** Tom can name his daughter or his wife on a to-do. They do not use the app. Realizes UJ-2.

**Functional Requirements:**

#### FR-16: Name a person who is not a user

Tom can name another person on a to-do. That person cannot use the app in v1. Realizes UJ-2.

**Consequences (testable):**
- A to-do can show his daughter's name or his wife's name.
- That person has no sign-in and no view of the to-do.

## 5. Non-Goals and Out of Scope

- A person named on a to-do does not get an account, a shared to-do list, or a way to mark a to-do done in v1.
- The product does not choose which high-priority to-do Tom does first.
- v1 is one responsive website. It is not a native phone app, a native desktop app, a public API, or a hardware device.
- The product does not automatically add to-dos. A copy is not added until Tom confirms it.
- v1 has no authentication and no sign-in. Tom is not asked to identify himself. Anyone who opens the website can see and edit the same to-dos.
- v1 has no calendar. FR-14 is withdrawn. Tom cannot add a to-do to Google Calendar, Apple Calendar, or any other calendar, and this product does not keep one. No to-do offers an add-to-calendar action. The product does not create a to-do from a calendar event.
- "Quick to finish" is not stored on the to-do.

## 6. MVP Scope

v1 is the full set of requirements, including partial and notes, on one responsive website. §5 is out of scope, not deferred work.

### 6.1 In Scope

- FR-1 through FR-17, except FR-14, on one responsive website.
- UJ-1 and UJ-2.

## 7. Success Metrics

No usage target was supplied. These measure whether the two journeys and the not-done view work. They are not growth numbers.

**Primary**

- **SM-1:** On the responsive website, including at phone width, Tom completes UJ-1: he chooses a high-priority to-do and marks it done. Target: he can do this. Validates FR-6, FR-8, FR-9.
- **SM-2:** On Saturday, Today shows UJ-2's to-dos in order and shows Next while those to-dos are not done, after Tom has copied and confirmed them. Target: he can do this. Validates FR-2, FR-7, FR-12, FR-15.

**Secondary**

- **SM-3:** The not-done view includes a not-done to-do from another day, includes a partial to-do, and excludes a done to-do. Target: all three are true. Validates FR-3, FR-17.

**Counter-metrics (do not optimize)**

- **SM-C1:** Saturday mark-done rate. UJ-2 succeeds when to-dos stay not done and Tom still sees Next. Raising Saturday completion can mean the weekday habit is being pushed onto the packed day. Counterbalances SM-1. How to observe the rate was not supplied. Treat SM-C1 as a guardrail, not a computed metric.

## 8. Open Questions

Deferred. Owner: PM. Revisit before a different user-facing name ships. This does not block shipped v1.

1. The working title is still "Todo App."

## 9. Assumptions Index

- `[ASSUMPTION: ballet pickup is at 2:30 PM, when the lesson ends.]` UJ-2 and FR-12 use 2:30 PM on that basis. The lesson end and the pickup were not stated as two different clocks.
