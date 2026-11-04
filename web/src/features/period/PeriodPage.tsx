import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { get_period, type TodoOut } from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { localISODate } from '../../localDate.ts'
import { TodoWorkspace } from '../todo-editor/TodoWorkspace.tsx'

const GRAINS = ['day', 'week', 'month', 'year'] as const

export function PeriodPage() {
  const [params, setParams] = useSearchParams()
  const grain = params.get('grain') ?? 'day'
  const anchor = params.get('anchor') ?? localISODate()
  const [todos, setTodos] = useState<TodoOut[]>([])
  const [undated, setUndated] = useState<TodoOut[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    get_period(grain, anchor)
      .then((body) => {
        if (cancelled) return
        setTodos(body.todos)
        setUndated(body.undated)
        setError('')
        setLoading(false)
      })
      .catch((caught: unknown) => {
        if (cancelled) return
        setTodos([])
        setUndated([])
        setError(errorDetail(caught))
        setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [grain, anchor, reloadKey])

  function setGrain(nextGrain: string) {
    const next = new URLSearchParams(params)
    next.set('grain', nextGrain)
    next.set('anchor', anchor)
    setParams(next)
  }

  return (
    <TodoWorkspace
      title="Period"
      todos={todos}
      loading={loading}
      error={error}
      onReload={() => setReloadKey((value) => value + 1)}
      sections={[{ heading: 'No date', todos: undated }]}
      header={
        <>
          <div className="button-row">
            {GRAINS.map((item) => (
              <button
                key={item}
                type="button"
                className="secondary"
                aria-pressed={item === grain}
                onClick={() => setGrain(item)}
              >
                {item === 'day' ? 'Day' : item === 'week' ? 'Week' : item === 'month' ? 'Month' : 'Year'}
              </button>
            ))}
          </div>
          <label>
            Date
            <input
              type="date"
              value={anchor}
              onChange={(event) => {
                if (event.target.value === '') return
                const next = new URLSearchParams(params)
                next.set('grain', grain)
                next.set('anchor', event.target.value)
                setParams(next)
              }}
            />
          </label>
        </>
      }
    />
  )
}
