# Accessibility

Measured 4 November 2026 with `@axe-core/playwright` against the Compose site at http://127.0.0.1:8080.

The scan uses the tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, and `wcag22aa`. A violation fails the test when its impact is critical or serious.

Pages: Today on an empty day, Lists, Not done, and Period.

Result: `npm run test:e2e` passed, including this scan. No critical or serious violations were reported.

The done-text color in the stylesheet is `#746d68` on `#f7f6f3`, about 4.7:1. That change was made during the earlier review so done text clears the 4.5:1 text contrast floor.
