import { useEffect, useState } from 'react'
import { get_not_done, type TodoOut } from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { TodoWorkspace } from '../todo-editor/TodoWorkspace.tsx'

export function NotDonePage() {
  const [todos, setTodos] = useState<TodoOut[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    get_not_done()
      .then((rows) => {
        if (cancelled) return
        setTodos(rows)
        setError('')
        setLoading(false)
      })
      .catch((caught: unknown) => {
        if (cancelled) return
        setError(errorDetail(caught))
        setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [reloadKey])

  return (
    <TodoWorkspace
      title="Not done"
      todos={todos}
      loading={loading}
      error={error}
      onReload={() => setReloadKey((value) => value + 1)}
    />
  )
}
