import type { TodoOut } from '../api/client.ts'

export function todo(overrides: Partial<TodoOut> = {}): TodoOut {
  return {
    id: 1,
    list_id: 1,
    parent_id: null,
    position: 1,
    title: 'Rest',
    state: 'not_done',
    priority: 2,
    notes: '',
    on_date: '2026-11-04',
    at_time: null,
    alarm_at: null,
    person_name: null,
    copy_id: null,
    copy_confirmed: true,
    ...overrides,
  }
}
