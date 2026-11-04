import type { TodoOut } from '../../api/client.ts'

function byPosition(a: TodoOut, b: TodoOut): number {
  return a.position - b.position || a.id - b.id
}

type Node = { todo: TodoOut; children: Node[] }

function tree(todos: TodoOut[]): Node[] {
  const preserveOrder = new Set(todos.map((todo) => todo.on_date)).size > 1
  const ids = new Set(todos.map((todo) => todo.id))
  const children = new Map<number, TodoOut[]>()
  const tops: TodoOut[] = []
  for (const todo of todos) {
    if (todo.parent_id != null && ids.has(todo.parent_id)) {
      const list = children.get(todo.parent_id) ?? []
      list.push(todo)
      children.set(todo.parent_id, list)
    } else {
      tops.push(todo)
    }
  }
  const order = (items: TodoOut[]) => (preserveOrder ? items : items.slice().sort(byPosition))
  const nodes = (items: TodoOut[]): Node[] =>
    order(items).map((todo) => ({
      todo,
      children: nodes(children.get(todo.id) ?? []),
    }))
  return nodes(tops)
}

function RowBody({ todo, next }: { todo: TodoOut; next: boolean }) {
  return (
    <>
      {next ? <span className="next-marker">Next</span> : null}
      <span className={todo.priority === 5 ? 'priority priority-high' : 'priority'}>{todo.priority}</span>
      <span className={todo.state === 'done' ? 'todo-title is-done' : 'todo-title'}>{todo.title}</span>
      {todo.state === 'partial' ? <span className="state-partial">partial</span> : null}
      {todo.state === 'done' ? <span className="state-done">done</span> : null}
      {todo.at_time ? <span className="meta">{todo.at_time}</span> : null}
      {todo.alarm_at ? <span className="meta">Alarm {todo.alarm_at}</span> : null}
      {todo.person_name ? <span className="meta">{todo.person_name}</span> : null}
      {todo.state === 'partial' && todo.notes ? <span className="notes">{todo.notes}</span> : null}
    </>
  )
}

function Row({
  todo,
  next,
  depth,
  onOpen,
  onMove,
}: {
  todo: TodoOut
  next: boolean
  depth: number
  onOpen?: (todo: TodoOut) => void
  onMove?: (todo: TodoOut, direction: -1 | 1) => void
}) {
  return (
    <article
      className={depth > 0 ? 'todo-row sub' : 'todo-row'}
      style={depth > 0 ? { marginLeft: `calc(var(--space-4) * ${depth})` } : undefined}
    >
      {onOpen ? (
        <button type="button" className="open-row" onClick={() => onOpen(todo)}>
          <RowBody todo={todo} next={next} />
        </button>
      ) : (
        <div className="open-row">
          <RowBody todo={todo} next={next} />
        </div>
      )}
      {onMove ? (
        <div className="row-actions">
          <button type="button" onClick={() => onMove(todo, -1)}>
            Move up
          </button>
          <button type="button" onClick={() => onMove(todo, 1)}>
            Move down
          </button>
        </div>
      ) : null}
    </article>
  )
}

export function TodoListView({
  todos,
  nextTodoId,
  onOpen,
  onMove,
}: {
  todos: TodoOut[]
  nextTodoId?: number | null
  onOpen?: (todo: TodoOut) => void
  onMove?: (todo: TodoOut, direction: -1 | 1) => void
}) {
  function branch(node: Node, depth: number) {
    return (
      <div key={node.todo.id}>
        <Row
          todo={node.todo}
          next={nextTodoId != null && node.todo.id === nextTodoId}
          depth={depth}
          onOpen={onOpen}
          onMove={onMove}
        />
        {node.children.map((child) => branch(child, depth + 1))}
      </div>
    )
  }

  return <div className="todo-list">{tree(todos).map((node) => branch(node, 0))}</div>
}
