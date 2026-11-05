# Reconcile: shipped-decision

Input, verbatim: Keep the existing app. Do not rescope it. The decision already shipped: undated to-dos render in a "No date" section under the dated rows, and an alarm is shown but never fired.

Sources compared: `prd.md`, `addendum.md`. Neither file was modified.

## What the input requires

1. Keep the existing app.
2. Do not rescope it.
3. Treat one decision as already shipped, with two behaviors:
   - Undated to-dos render in a section labeled "No date", placed under the dated rows.
   - An alarm is shown, and it is never fired.

## Where it is captured

### Already shipped, No date, and the alarm — captured

`prd.md` records the decision as closed and shipped, and states both behaviors:

- Line 303: "The two former open behaviors are decided and shipped. An undated to-do renders in No date under the dated rows. An alarm is shown and never fired."
- Line 324: "This does not block the product that already shipped."
- Line 333: "Undated to-dos render in No date under the dated rows of the day, week, month, and year views. Confirmed with the shipped app."
- Line 332: "Alarm stays. The alarm is shown and never fired."

No date as a section under the dated rows:

- Line 70: "A to-do with no date is undated."
- Line 73: "**No date** — the section under the dated rows on a day, week, month, or year view. It holds undated to-dos."
- Line 78: "to-dos bounded to that period, shown as dated rows, with undated to-dos in No date under those rows."
- Line 126: "An undated to-do appears under the heading "No date", beneath those dated rows, on the day view, the week view, the month view, and the year view."
- Line 127: "No date is part of the period view that is open. It is not its own view. Changing the period does not remove the undated to-dos from No date."

Alarm shown and never fired:

- Line 49: "The alarm is shown on the to-do and is never fired."
- Line 72: "**Alarm** — a time shown on a time-bound to-do. It is never fired."
- Line 233: "The alarm is shown on that to-do."
- Line 234: "The alarm is never fired. When that time arrives, the product does not send or play anything."

`addendum.md` captures the alarm half, including the design consequence of never firing:

- "The alarm remains a product capability. It is shown on the to-do and is never fired, so there is no lead time and no delivery to design."

No date is not in `addendum.md`. It is specified in the PRD body. That absence is not a gap.

These points are fully captured: the decision has already shipped; undated to-dos render in a "No date" section under the dated rows; an alarm is shown and never fired. The FR text is more specific than the input (day, week, month, and year; not its own view; no send or play; no lead time and no delivery) and does not contradict it.

## Gaps

### 1. Keep the existing app

The input requires the current app to stay the baseline. The documents do not say that.

FR-4 and FR-13 restate the two shipped facts as capabilities and testable consequences ("Tom can open a day view…", "Tom can set an alarm…"). "Confirmed with the shipped app" (line 333) is evidence for the No date placement only. "Alarm stays" (line 332) and "The alarm remains a product capability" (addendum) keep only the alarm. Nothing says to keep the rest of the existing app.

### 2. Do not rescope it

The input forbids a scope change. Line 303 closes the two former open behaviors by marking them decided and shipped. It does not say this decision is not a rescope, and it does not freeze the app's scope.

§5 and §6.2 list specific cuts (no account for a named person, no auto-pick, no native app, no automatic to-dos, no auth, no calendar, no stored "quick to finish"). They do not state a general non-rescope. The addendum does not either.
