import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, vi } from 'vitest'
import { CopyReviewPage } from './copy/CopyReviewPage.tsx'
import { ListsPage } from './lists/ListsPage.tsx'
import { NotDonePage } from './not-done/NotDonePage.tsx'
import { PeriodPage } from './period/PeriodPage.tsx'
import { TodayPage } from './today/TodayPage.tsx'
import { TodoEditor } from './todo-editor/TodoEditor.tsx'
import { todo } from '../test/todo.ts'

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

afterEach(() => {
  vi.unstubAllGlobals()
})

test('Today shows the empty state', async () => {
  vi.stubGlobal('fetch', () =>
    Promise.resolve(json({ on_date: '1999-01-01', todos: [], next_todo_id: null })),
  )
  render(
    <MemoryRouter initialEntries={['/?on_date=1999-01-01']}>
      <TodayPage />
    </MemoryRouter>,
  )
  expect(await screen.findByText('No to-dos today.')).toBeTruthy()
})

test('Lists shows the empty state', async () => {
  vi.stubGlobal('fetch', () => Promise.resolve(json([])))
  render(
    <MemoryRouter>
      <ListsPage />
    </MemoryRouter>,
  )
  expect(await screen.findByText('No to-do lists.')).toBeTruthy()
})

test('Not done shows a load error', async () => {
  vi.stubGlobal('fetch', () => Promise.resolve(json({ detail: 'Database unavailable' }, 503)))
  render(
    <MemoryRouter>
      <NotDonePage />
    </MemoryRouter>,
  )
  expect(await screen.findByRole('alert')).toHaveProperty('textContent', 'Database unavailable')
})

test('Period renders the No date section', async () => {
  vi.stubGlobal('fetch', () =>
    Promise.resolve(
      json({
        grain: 'week',
        anchor: '2026-11-04',
        todos: [todo({ title: 'Dated' })],
        undated: [todo({ id: 2, title: 'Undated', on_date: null })],
      }),
    ),
  )
  render(
    <MemoryRouter initialEntries={['/period?grain=week&anchor=2026-11-04']}>
      <PeriodPage />
    </MemoryRouter>,
  )
  expect(await screen.findByText('No date')).toBeTruthy()
  expect(screen.getByText('Undated')).toBeTruthy()
})

test('Copy review keeps confirm disabled until the copy loads', async () => {
  vi.stubGlobal('fetch', () => Promise.resolve(json({ id: 4, todos: [todo()] })))
  render(
    <MemoryRouter initialEntries={['/copies/4']}>
      <Routes>
        <Route path="/copies/:copyId" element={<CopyReviewPage />} />
      </Routes>
    </MemoryRouter>,
  )
  await waitFor(() => {
    expect((screen.getByRole('button', { name: 'Confirm copy' }) as HTMLButtonElement).disabled).toBe(false)
  })
  expect(screen.getByText('Rest')).toBeTruthy()
  fireEvent.click(screen.getByRole('button', { name: 'Confirm copy' }))
})

test('the editor shows the API error when save is rejected', async () => {
  vi.stubGlobal('fetch', () => Promise.resolve(json({ detail: 'Title is required' }, 422)))
  render(
    <TodoEditor
      listId={1}
      todo={null}
      parentId={null}
      parentTitle={null}
      defaultOnDate={null}
      onClose={() => undefined}
      onSaved={() => undefined}
      onAddSub={() => undefined}
      onCreateAnother={() => undefined}
    />,
  )
  fireEvent.submit(document.querySelector('form') as HTMLFormElement)
  expect(await screen.findByRole('alert')).toHaveProperty('textContent', 'Title is required')
})
