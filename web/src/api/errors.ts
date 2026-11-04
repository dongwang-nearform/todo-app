import { ApiError } from './client.ts'

export function errorDetail(error: unknown): string {
  if (error instanceof ApiError && error.message) return error.message
  return "Couldn't save."
}
