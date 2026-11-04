import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { create_list, list_lists, type ListOut } from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { Workspace } from '../../layout/Workspace.tsx'

export function ListsPage() {
  const [lists, setLists] = useState<ListOut[]>([])
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  function reload() {
    setLoading(true)
    list_lists()
      .then((rows) => {
        setLists(rows)
        setError('')
        setLoading(false)
      })
      .catch((caught: unknown) => {
        setError(errorDetail(caught))
        setLoading(false)
      })
  }

  useEffect(() => {
    reload()
  }, [])

  async function create(event: { preventDefault: () => void }) {
    event.preventDefault()
    setError('')
    try {
      await create_list({ name })
      setName('')
      reload()
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  return (
    <Workspace title="Lists" editor={null}>
      {!loading && !error && lists.length === 0 ? <p>No to-do lists.</p> : null}
      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
      {!loading ? (
        <ul className="plain">
          {lists.map((list) => (
            <li key={list.id}>
              <Link to={`/lists/${list.id}`}>{list.name}</Link>
            </li>
          ))}
        </ul>
      ) : null}
      <form onSubmit={(event) => void create(event)}>
        <label>
          Name
          <input value={name} onChange={(event) => setName(event.target.value)} />
        </label>
        <button type="submit" className="primary">
          Create a list
        </button>
      </form>
    </Workspace>
  )
}
