import { ApiError } from './client.ts'
import { errorDetail } from './errors.ts'

test('errorDetail returns the API message', () => {
  expect(errorDetail(new ApiError('Title is required', 422))).toBe('Title is required')
})

test('errorDetail hides a non-API failure', () => {
  expect(errorDetail(new Error('socket'))).toBe("Couldn't save.")
})
