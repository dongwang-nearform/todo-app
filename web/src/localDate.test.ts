import { localISODate, toHms } from './localDate.ts'

test('localISODate uses the local calendar day', () => {
  expect(localISODate(new Date(2026, 10, 4, 23, 30))).toBe('2026-11-04')
})

test('toHms adds seconds to a minute value', () => {
  expect(toHms('08:30')).toBe('08:30:00')
  expect(toHms('08:30:01')).toBe('08:30:01')
})
