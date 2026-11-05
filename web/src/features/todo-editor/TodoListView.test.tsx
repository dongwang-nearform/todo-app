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
