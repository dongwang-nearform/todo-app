# Reconcile — shipped screens

Source: the running web app, plus the shipped decision that undated to-dos render under the dated rows in a section headed "No date", and that an alarm is shown and never fired.

## Kept

- Surfaces: Today, Not done, Lists, List, Period, Copy review.
- Light surface, system type, no component library, 768px break, land on Today.
- Dated rows first. "No date" under them, including when that list is empty.
- Alarm text on the row. No fire, no lead time, no notification permission.
- `alarm_at` without `at_time` fails and the screen shows the server `detail` string.

## Adjusted to the screen

- `{colors.done}` is `#746D68`, the value in `web/src/index.css`.
- The row prints the word Alarm before `alarm_at`.
- Today and Period use a date field. Period uses Day, Week, Month, and Year. Week, month, and year stay lists.
- Copy review rows do not open or move. Confirm opens Today on that date.

## Dropped

No qualitative idea from the draft was dropped. The draft's open rename of "Todo App" is closed here to the shipped document title. Alarm lead time stays undesigned, because v1 shows the time and does not fire it.
