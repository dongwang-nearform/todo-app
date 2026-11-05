import { render, screen } from '@testing-library/react'
import { TodoListView } from './TodoListView.tsx'
import { todo } from '../../test/todo.ts'

test('renders a nested sub-to-do and the partial note', () => {
  render(
    <TodoListView
      nextTodoId={1}
      todos={[
        todo({ id: 1, title: 'Rest', state: 'partial', notes: 'left the rest', priority: 5 }),
        todo({ id: 2, parent_id: 1, title: 'Child', position: 1 }),
        todo({ id: 3, parent_id: 2, title: 'Grandchild', position: 1 }),
      ]}
    />,
  )
  expect(screen.getByText('Next')).toBeTruthy()
  expect(screen.getByText('Grandchild')).toBeTruthy()
  expect(screen.getByText('left the rest')).toBeTruthy()
  expect(screen.getByText('partial')).toBeTruthy()
})

test('colors each priority numeral and tints its row', () => {
  const { container } = render(
    <TodoListView
      todos={[
        ...[1, 2, 3, 4, 5].map((priority) =>
          todo({ id: priority, title: `Task ${priority}`, priority, position: priority }),
        ),
        todo({ id: 6, title: 'Finished', state: 'done', priority: 1, position: 6 }),
        todo({ id: 7, title: 'Halfway', state: 'partial', priority: 5, position: 7 }),
      ]}
    />,
  )
  for (const priority of [1, 2, 3, 4, 5]) {
    const numerals = screen.getAllByText(String(priority))
    expect(numerals.length).toBeGreaterThan(0)
    for (const numeral of numerals) {
      expect(numeral.textContent).toBe(String(priority))
      expect(numeral.className).toBe(`priority priority-${priority}`)
    }
  }
  const rows = container.querySelectorAll('article.todo-row')
  expect(rows.length).toBe(7)
  for (const row of rows) {
    const numeral = row.querySelector('.priority')
    expect(row.classList.contains(`priority-row-${numeral?.textContent}`)).toBe(true)
  }
})

test('keeps mixed dates in the given order', () => {
  render(
    <TodoListView
      todos={[
        todo({ id: 1, title: 'Later', on_date: '2026-11-06', position: 1 }),
        todo({ id: 2, title: 'Earlier', on_date: '2026-11-04', position: 9 }),
      ]}
    />,
  )
  const titles = screen.getAllByText(/Later|Earlier/).map((node) => node.textContent)
  expect(titles).toEqual(['Later', 'Earlier'])
})
