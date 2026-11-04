import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { confirm_copy, get_copy, type TodoOut } from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { Workspace } from '../../layout/Workspace.tsx'
import { TodoListView } from '../todo-editor/TodoListView.tsx'

export function CopyReviewPage() {
  const params = useParams()
  const navigate = useNavigate()
  const copyId = Number(params.copyId)
  const [todos, setTodos] = useState<TodoOut[]>([])
  const [loading, setLoading] = useState(true)
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setLoaded(false)
    get_copy(copyId)
      .then((body) => {
        if (cancelled) return
        setTodos(body.todos)
        setError('')
        setLoaded(true)
        setLoading(false)
      })
      .catch((caught: unknown) => {
        if (cancelled) return
        setError(errorDetail(caught))
        setLoaded(false)
        setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [copyId])

  async function confirm() {
    setError('')
    try {
      const body = await confirm_copy(copyId)
      const onDate = body.todos[0]?.on_date
      navigate(onDate ? `/?on_date=${onDate}` : '/')
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  return (
    <Workspace title="Copy review" editor={null}>
      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
      {!loading ? <TodoListView todos={todos} /> : null}
      <button type="button" className="primary" disabled={!loaded} onClick={() => void confirm()}>
        Confirm copy
      </button>
    </Workspace>
  )
}
