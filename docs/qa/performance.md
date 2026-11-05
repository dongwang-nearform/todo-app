# Performance

Measured 5 November 2026 against the Compose site at http://127.0.0.1:8080 with Chrome DevTools in the IDE browser.

## Setup

- Page: Today, `?on_date=2026-11-05`, with 60 seeded to-dos on that date.
- Viewport: 390 × 844 at 2× device scale, mobile emulation on.
- CPU: 4× throttling through `Emulation.setCPUThrottlingRate`. A fixed loop ran 16 ms unthrottled and 47 ms throttled, so the throttle was active.
- Seed data was deleted afterward.

## Results

| Measure | Value |
| --- | --- |
| First Contentful Paint, 4× CPU | about 1.03 s (two reloads: 1040 ms and 1028 ms) |
| DOMContentLoaded and load, reload | about 25 ms |
| Long tasks during page load | none recorded |
| Opening one to-do in the editor, 4× CPU | 9 ms, no long tasks |
| Built CSS | 4.16 kB (1.20 kB gzip) |
| Built JavaScript | 274.51 kB (86.27 kB gzip), one chunk |

## Not measured

- Largest Contentful Paint. The browser reported no entry on these loads, so I have no value for it.
- A cold load with the cache off. I set the cache-disable flag, but the document still came from cache (300-byte transfer), so the reloads above are not cold.
- A Performance trace file. The numbers come from the Performance API, not a trace recording.
- A device profile below 4× and a real phone.

## Reading

Page load is cheap once the bundle is cached. The First Contentful Paint at 4× is the number to watch. It is about one second on a throttled CPU, most likely the single 274 kB script before React mounts. A route-split build or a smaller bundle is the next step if that matters. Editor open is fast with 60 rows.
