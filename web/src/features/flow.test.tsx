import { fireEvent, render, screen } from '@testing-library/react'
import { vi } from 'vitest'
import App from '../App.tsx'
import { todo } from '../test/todo.ts'

function json(body: unknown, status = 200) {
  return Promise.resolve(
    new Response(JSON.stringify(body), {
      status,
      headers: { 'Content-Type': 'application/json' },
    }),
  )
}

test('opens a list, edits a to-do, and reorders it', async () => {
  const rows = [todo({ title: 'Rest' }), todo({ id: 2, title: 'Other', position: 2 })]
  vi.stubGlobal('fetch', (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input)
    const method = init?.method ?? 'GET'
    if (url.includes('/api/views/today')) {
      return json({ on_date: '2026-11-04', todos: [], next_todo_id: null })
    }
    if (url.includes('/api/views/not-done')) return json([])
    if (url.includes('/api/views/period')) {
      return json({ grain: 'day', anchor: '2026-11-04', todos: [], undated: [] })
    }
    if (method === 'PATCH' && url.includes('/api/todos/')) {
      return json(todo({ state: 'done', title: 'Rest' }))
    }
    if (method === 'DELETE' && url.includes('/api/todos/')) return Promise.resolve(new Response(null, { status: 204 }))
    if (method === 'POST' && /\/api\/lists\/\d+\/todos/.test(url)) {
      return json(todo({ id: 9, title: 'Child', parent_id: 1 }), 201)
    }
    if (method === 'PATCH' && url.includes('/api/lists/')) {
      return json({ id: 1, name: 'Weekend', position: 1 })
    }
    if (method === 'POST' && url.includes('/api/copies')) return json({ id: 4, todos: [] }, 201)
    if (url.includes('/api/copies/')) return json({ id: 4, todos: [todo()] })
    if (url.includes('/todos')) return json(rows)
    if (url.includes('/api/lists')) return json([{ id: 1, name: 'Saturday', position: 1 }])
    return json({ detail: `unhandled ${method} ${url}` }, 500)
  })

  window.history.pushState({}, '', '/lists/1')
  render(<App />)

  expect(await screen.findByRole('heading', { name: 'Saturday' })).toBeTruthy()
  fireEvent.click(await screen.findByRole('button', { name: /Rest/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Mark done' }))
  expect(await screen.findByText('State done')).toBeTruthy()
  await screen.findByRole('button', { name: /Rest/ })

  fireEvent.click(screen.getByRole('button', { name: 'Mark partial' }))
  fireEvent.click(screen.getByRole('button', { name: 'Add sub-to-do' }))
  expect(await screen.findByText('Sub-to-do of Rest')).toBeTruthy()
  fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Child' } })
  fireEvent.change(screen.getByLabelText('Priority'), { target: { value: '4' } })
  fireEvent.change(screen.getByLabelText('Notes'), { target: { value: 'note' } })
  fireEvent.change(screen.getByLabelText('Person'), { target: { value: 'Tom' } })
  fireEvent.submit(screen.getByRole('button', { name: 'Save' }).closest('form') as HTMLFormElement)
  await screen.findByRole('button', { name: /Rest/ })

  fireEvent.click(screen.getAllByRole('button', { name: 'Move up' })[0])
  fireEvent.click(screen.getAllByRole('button', { name: 'Move down' })[0])
  await screen.findByRole('button', { name: /Rest/ })
  fireEvent.submit(screen.getByRole('button', { name: 'Rename' }).closest('form') as HTMLFormElement)
  fireEvent.click(screen.getByRole('button', { name: 'Delete list' }))
  expect(await screen.findByRole('heading', { name: 'Lists' })).toBeTruthy()

  fireEvent.click(screen.getByRole('link', { name: 'Today' }))
  expect(await screen.findByRole('heading', { name: 'Today' })).toBeTruthy()
  fireEvent.change(screen.getByLabelText('Date'), { target: { value: '' } })
  fireEvent.change(screen.getByLabelText('Date'), { target: { value: '2026-11-05' } })
  fireEvent.click(screen.getByRole('link', { name: 'Period' }))
  expect(await screen.findByRole('heading', { name: 'Period' })).toBeTruthy()
  fireEvent.click(screen.getByRole('button', { name: 'Week' }))
  fireEvent.click(screen.getByRole('link', { name: 'Not done' }))
  expect(await screen.findByRole('heading', { name: 'Not done' })).toBeTruthy()
})
