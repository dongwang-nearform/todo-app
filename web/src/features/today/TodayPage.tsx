import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { get_today, type TodoOut } from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { localISODate } from '../../localDate.ts'
import { TodoWorkspace } from '../todo-editor/TodoWorkspace.tsx'

export function TodayPage() {
  const [params, setParams] = useSearchParams()
  const onDate = params.get('on_date') ?? localISODate()
  const [todos, setTodos] = useState<TodoOut[]>([])
  const [nextTodoId, setNextTodoId] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    get_today(onDate)
      .then((body) => {
        if (cancelled) return
        setTodos(body.todos)
        setNextTodoId(body.next_todo_id)
        setError('')
        setLoading(false)
      })
      .catch((caught: unknown) => {
        if (cancelled) return
        setTodos([])
        setNextTodoId(null)
        setError(errorDetail(caught))
        setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [onDate, reloadKey])

  return (
    <TodoWorkspace
      title="Today"
      todos={todos}
      loading={loading}
      error={error}
      nextTodoId={nextTodoId}
      defaultOnDate={onDate}
      onReload={() => setReloadKey((value) => value + 1)}
      empty={<p>No to-dos today.</p>}
      header={
        <label>
          Date
          <input
            type="date"
            value={onDate}
            onChange={(event) => {
              if (event.target.value === '') return
              const next = new URLSearchParams(params)
              next.set('on_date', event.target.value)
              setParams(next)
            }}
          />
        </label>
      }
    />
  )
}
