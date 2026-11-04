import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  create_copy,
  delete_list,
  list_lists,
  list_todos,
  update_list,
  type ListOut,
  type TodoOut,
} from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { TodoWorkspace } from '../todo-editor/TodoWorkspace.tsx'

export function ListPage() {
  const params = useParams()
  const navigate = useNavigate()
  const listId = Number(params.listId)
  const [lists, setLists] = useState<ListOut[]>([])
  const [todos, setTodos] = useState<TodoOut[]>([])
  const [name, setName] = useState('')
  const [destination, setDestination] = useState('')
  const [onDate, setOnDate] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)
  const list = lists.find((item) => item.id === listId) ?? null

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    Promise.all([list_lists(), list_todos(listId)])
      .then(([nextLists, nextTodos]) => {
        if (cancelled) return
        setLists(nextLists)
        setTodos(nextTodos)
        const found = nextLists.find((item) => item.id === listId)
        setName(found?.name ?? '')
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
  }, [listId, reloadKey])

  async function rename(event: { preventDefault: () => void }) {
    event.preventDefault()
    setError('')
    try {
      await update_list(listId, { name })
      setReloadKey((value) => value + 1)
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  async function remove() {
    setError('')
    try {
      await delete_list(listId)
      navigate('/lists')
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  async function copy(event: { preventDefault: () => void }) {
    event.preventDefault()
    setError('')
    try {
      const created = await create_copy({
        source_list_id: listId,
        destination_list_id: Number(destination),
        on_date: onDate,
      })
      navigate(`/copies/${created.id}`)
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  return (
    <TodoWorkspace
      title={list?.name ?? 'List'}
      todos={todos}
      loading={loading}
      error={error}
      onReload={() => setReloadKey((value) => value + 1)}
      listId={Number.isInteger(listId) ? listId : null}
      header={
        <>
          <form onSubmit={(event) => void rename(event)}>
            <label>
              Name
              <input value={name} onChange={(event) => setName(event.target.value)} />
            </label>
            <button type="submit" className="secondary">
              Rename
            </button>
          </form>
          <form onSubmit={(event) => void copy(event)}>
            <label>
              Destination list
              <select
                value={destination}
                onChange={(event) => setDestination(event.target.value)}
                required
              >
                <option value="">Destination list</option>
                {lists.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Date
              <input
                type="date"
                value={onDate}
                onChange={(event) => setOnDate(event.target.value)}
                required
              />
            </label>
            <button type="submit" className="secondary">
              Copy onto a date
            </button>
          </form>
          <button type="button" className="danger" onClick={() => void remove()}>
            Delete list
          </button>
        </>
      }
    />
  )
}
