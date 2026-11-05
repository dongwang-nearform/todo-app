---
title: Todo App
status: approved
created: 2026-11-04
updated: 2026-11-05
---

# Product Brief: Todo App

*Approved. Source is `prd.md` only. Working title. Inferences are marked [ASSUMPTION]. What the PRD does not say is marked unknown.*

## Executive Summary

The product exists so a packed day and an ordinary morning use the same to-do list. Every to-do that is not done stays visible across all time. Day, week, month, and year views sit alongside that not-done view.

Todo App is a responsive website for one person, Tom. He keeps the lists. His daughter and his wife appear as names on his to-dos. They do not sign in. There is no native phone app. The same site works at phone width and at desktop width, and he is not asked to identify himself.

On a weekday morning he opens the site, chooses a high-priority to-do he can finish quickly, and marks it done. The product does not choose for him.

On Saturday he opens Today and follows an order that includes other people's fixed times. He checks what is next even when he does not mark a to-do done. Saturday's to-dos are on Today because he copied them from another list and confirmed the copy.

## The Problem

The PRD does not describe a separate problem, how Tom copes today, or what the status quo costs.

[ASSUMPTION: the purpose sentence is the problem. A packed day and an ordinary morning need to be the same list, and a to-do that is not done needs to stay visible across all time. The PRD does not say this is painful, what he does instead, or what it costs him.]

## The Solution

Tom has more than one named to-do list. Today shows that day's to-dos in order and which one is next, including when none are marked done. The not-done view shows every to-do that is not done, across all time. Partial to-dos are in it. He can mark a to-do partial and write notes without marking it done. Partial is a state. Done to-dos are out of the not-done view. Day, week, month, and year views show to-dos whose time falls in that period.

He creates, updates, and deletes to-dos. He marks a to-do done, and he marks a done to-do not done. If work is blocked or has several parts, he marks it done and creates a new to-do, or he adds sub-to-dos. Both ways stay available. He sets a priority from 1 to 5. 5 is highest. He sets a time. He sets an alarm on a time-bound to-do. He names another person on a to-do. He copies to-dos from one list onto another. Nothing from that copy appears until he confirms.

"Quick to finish" is his judgment in the moment. It is not stored on the to-do.

## What this refuses

These are commitments in the PRD. The PRD does not claim them as an advantage over any other product. Unknown: any difference from another product.

- The product does not choose his first to-do.
- The product does not add a to-do by itself. An unconfirmed copy stays off the destination list. The product does not place copied to-dos on a later Saturday by itself.
- A person named on a to-do gets no account, no shared list, and no way to mark it done.
- v1 has no sign-in.
- v1 has no calendar, and a to-do cannot be added to Google Calendar or Apple Calendar.
- Partial has no progress number, percent, count, or score.
- Saturday can succeed while to-dos stay not done. Raising the Saturday mark-done rate can mean the weekday habit is being pushed onto the packed day.

## Who This Serves

Tom is the user. On weekday mornings he finishes a high-priority to-do he can do quickly. On Saturdays he runs a day of other people's fixed times, including his daughter's lessons and a Costco trip with his wife. He may be too busy to mark those done. The next stop still has to be obvious.

His daughter and his wife are not users in v1. Their names can appear on his to-dos.

## Success Criteria

No usage target was supplied. Success means the journeys work.

- On the website, including at phone width, Tom chooses a high-priority to-do and marks it done.
- On Saturday, after he has copied and confirmed, Today shows the stops in order and what is next while those to-dos are not done.
- The not-done view includes a not-done to-do from another day, includes a partial to-do, and excludes a done to-do.
- Saturday mark-done rate is a counter-metric. Do not optimize it.

## Scope

v1 is the confirmed set. In: more than one to-do list; Today and what is next; the not-done view; day, week, month, and year views; create, update, and delete; done and not done; partial with notes; priority 1 to 5; sub-to-dos, or mark done and create a new to-do; time; alarm; copy, then confirm; names of people who are not users. Both journeys are in.

Out: a native phone app, a native desktop app, a public API, hardware, accounts and sign-in, any calendar, automatic to-dos, the product choosing what is first, and a stored "quick to finish" field.

A to-do with no date appears in the day, week, month, and year views in a "No date" section under the dated rows. That placement is closed.

Still open, and not deferred to a later version: how early an alarm fires; which list or day a weekday morning lands on. The user-facing name is still "Todo App."

## Vision

The confirmed vision is the purpose sentence in the Executive Summary.

## Unknowns

- How Tom copes today, and what that costs him, beyond the assumption in The Problem.
- Any user other than Tom.
- Why this product exists beyond the purpose sentence.
- A horizon past v1.
- A usage number or a business number.
- The open items in Scope.
