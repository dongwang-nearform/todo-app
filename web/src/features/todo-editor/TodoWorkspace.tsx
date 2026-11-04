import { useState, type ReactNode } from 'react'
import { update_todo, type TodoOut } from '../../api/client.ts'
import { errorDetail } from '../../api/errors.ts'
import { Workspace } from '../../layout/Workspace.tsx'
import { TodoEditor } from './TodoEditor.tsx'
import { TodoListView } from './TodoListView.tsx'

type EditorState =
  | { kind: 'edit'; todo: TodoOut }
  | { kind: 'create'; listId: number; parentId: number | null; parentTitle: string | null }

export function TodoWorkspace({
  title,
  todos,
  loading,
  error,
  nextTodoId,
  onReload,
  header,
  empty,
  sections,
  listId,
  defaultOnDate,
}: {
  title: string
  todos: TodoOut[]
  loading: boolean
  error: string
  nextTodoId?: number | null
  onReload: () => void
  header?: ReactNode
  empty?: ReactNode
  sections?: { heading: string; todos: TodoOut[] }[]
  listId?: number | null
  defaultOnDate?: string | null
}) {
  const [editor, setEditor] = useState<EditorState | null>(null)
  const [moveError, setMoveError] = useState('')
  const shown = [...todos, ...(sections ?? []).flatMap((section) => section.todos)]

  async function move(todo: TodoOut, direction: -1 | 1) {
    const siblings = shown
      .filter(
        (item) =>
          item.list_id === todo.list_id && (item.parent_id ?? null) === (todo.parent_id ?? null),
      )
      .slice()
      .sort((left, right) => left.position - right.position || left.id - right.id)
    const index = siblings.findIndex((item) => item.id === todo.id)
    const target = index + direction
    if (index < 0 || target < 0 || target >= siblings.length) return
    const next = siblings.slice()
    next.splice(target, 0, next.splice(index, 1)[0])
    setMoveError('')
    try {
      for (let position = 0; position < next.length; position += 1) {
        if (next[position].position !== position + 1) {
          await update_todo(next[position].id, { position: position + 1 })
        }
      }
      onReload()
    } catch (caught) {
      setMoveError(errorDetail(caught))
    }
  }

  const editorNode = editor ? (
    <TodoEditor
      key={
        editor.kind === 'edit'
          ? `edit-${editor.todo.id}`
          : `create-${editor.listId}-${editor.parentId ?? 'root'}`
      }
      listId={editor.kind === 'edit' ? editor.todo.list_id : editor.listId}
      todo={editor.kind === 'edit' ? editor.todo : null}
      parentId={editor.kind === 'create' ? editor.parentId : null}
      parentTitle={editor.kind === 'create' ? editor.parentTitle : null}
      defaultOnDate={editor.kind === 'create' ? (defaultOnDate ?? null) : null}
      onClose={() => setEditor(null)}
      onSaved={onReload}
      onAddSub={(todo) =>
        setEditor({
          kind: 'create',
          listId: todo.list_id,
          parentId: todo.id,
          parentTitle: todo.title,
        })
      }
      onCreateAnother={(nextListId) =>
        setEditor({ kind: 'create', listId: nextListId, parentId: null, parentTitle: null })
      }
    />
  ) : null

  return (
    <Workspace title={title} editor={editorNode}>
      {header}
      {listId != null ? (
        <div className="button-row">
          <button
            type="button"
            className={editor ? 'secondary' : 'primary'}
            onClick={() => setEditor({ kind: 'create', listId, parentId: null, parentTitle: null })}
          >
            Add to-do
          </button>
        </div>
      ) : null}
      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
      {moveError ? (
        <p className="error" role="alert">
          {moveError}
        </p>
      ) : null}
      {!loading && !error && todos.length === 0 ? empty : null}
      {!loading && !error ? (
        <TodoListView
          todos={todos}
          nextTodoId={nextTodoId}
          onOpen={(todo) => setEditor({ kind: 'edit', todo })}
          onMove={(todo, direction) => void move(todo, direction)}
        />
      ) : null}
      {!loading && !error
        ? (sections ?? []).map((section) => (
            <div key={section.heading}>
              <h2>{section.heading}</h2>
              <TodoListView
                todos={section.todos}
                onOpen={(todo) => setEditor({ kind: 'edit', todo })}
                onMove={(todo, direction) => void move(todo, direction)}
              />
            </div>
          ))
        : null}
    </Workspace>
  )
}
