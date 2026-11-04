import { useEffect, useState } from 'react'
import {
  create_todo,
  delete_todo,
  update_todo,
  type TodoOut,
} from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { toHms } from '../../localDate.ts'

export function TodoEditor({
  listId,
  todo,
  parentId,
  parentTitle,
  defaultOnDate,
  onClose,
  onSaved,
  onAddSub,
  onCreateAnother,
}: {
  listId: number
  todo: TodoOut | null
  parentId: number | null
  parentTitle: string | null
  defaultOnDate: string | null
  onClose: () => void
  onSaved: () => void
  onAddSub: (todo: TodoOut) => void
  onCreateAnother: (listId: number) => void
}) {
  const [title, setTitle] = useState(todo?.title ?? '')
  const [priority, setPriority] = useState(todo ? String(todo.priority) : '')
  const [notes, setNotes] = useState(todo?.notes ?? '')
  const [onDate, setOnDate] = useState(todo?.on_date ?? defaultOnDate ?? '')
  const [atTime, setAtTime] = useState(todo?.at_time ?? '')
  const [alarmAt, setAlarmAt] = useState(todo?.alarm_at ?? '')
  const [personName, setPersonName] = useState(todo?.person_name ?? '')
  const [state, setState] = useState(todo?.state ?? 'not_done')
  const [error, setError] = useState('')

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  function fields() {
    return {
      title,
      priority: priority === '' ? null : Number(priority),
      notes,
      on_date: onDate || null,
      at_time: atTime ? toHms(atTime) : null,
      alarm_at: alarmAt ? toHms(alarmAt) : null,
      person_name: personName || null,
    }
  }

  async function save() {
    setError('')
    try {
      if (todo) {
        await update_todo(todo.id, fields())
      } else {
        await create_todo(listId, { ...fields(), parent_id: parentId })
      }
      onSaved()
      onClose()
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  async function mark(next: 'done' | 'not_done' | 'partial') {
    if (!todo) return
    setError('')
    try {
      const saved = await update_todo(todo.id, {
        state: next,
        notes: next === 'partial' ? notes : undefined,
      })
      setState(saved.state)
      setNotes(saved.notes)
      onSaved()
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  async function markDoneAndCreate() {
    if (!todo) return
    setError('')
    try {
      await update_todo(todo.id, { state: 'done' })
      onSaved()
      onCreateAnother(todo.list_id)
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  async function remove() {
    if (!todo) return
    setError('')
    try {
      await delete_todo(todo.id)
      onSaved()
      onClose()
    } catch (caught) {
      setError(errorDetail(caught))
    }
  }

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault()
        void save()
      }}
    >
      {parentTitle ? <p className="meta">Sub-to-do of {parentTitle}</p> : null}
      <label>
        Title
        <input value={title} onChange={(event) => setTitle(event.target.value)} />
      </label>
      <label>
        Priority
        <select value={priority} onChange={(event) => setPriority(event.target.value)} required>
          <option value="">Priority</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </label>
      <label>
        Notes
        <textarea value={notes} onChange={(event) => setNotes(event.target.value)} />
      </label>
      <label>
        Date
        <input type="date" value={onDate} onChange={(event) => setOnDate(event.target.value)} />
      </label>
      <label>
        Time
        <input
          type="time"
          step={1}
          value={atTime}
          onChange={(event) => setAtTime(event.target.value)}
        />
      </label>
      <label>
        Alarm
        <input
          type="time"
          step={1}
          value={alarmAt}
          onChange={(event) => setAlarmAt(event.target.value)}
        />
      </label>
      <label>
        Person
        <input value={personName} onChange={(event) => setPersonName(event.target.value)} />
      </label>
      {todo ? <p className="meta">State {state === 'not_done' ? 'not done' : state}</p> : null}
      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
      <div className="button-row">
        <button type="submit" className="primary">
          Save
        </button>
        <button type="button" className="secondary" onClick={onClose}>
          Close
        </button>
        {todo ? (
          <>
            <button type="button" className="secondary" onClick={() => void mark('done')}>
              Mark done
            </button>
            <button type="button" className="secondary" onClick={() => void mark('not_done')}>
              Mark not done
            </button>
            <button type="button" className="secondary" onClick={() => void mark('partial')}>
              Mark partial
            </button>
            <button type="button" className="secondary" onClick={() => void markDoneAndCreate()}>
              Mark done and create a new to-do
            </button>
            <button type="button" className="secondary" onClick={() => onAddSub(todo)}>
              Add sub-to-do
            </button>
            <button type="button" className="danger" onClick={() => void remove()}>
              Delete
            </button>
          </>
        ) : null}
      </div>
    </form>
  )
}
