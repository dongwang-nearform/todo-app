from sqlalchemy import func, select

from app.db import session_scope
from app.errors import AppError
from app.models import Todo, TodoList
from app.schemas import TodoCreate, TodoOut, TodoPatch

STATES = {"not_done", "partial", "done"}


def _title(value: str | None) -> str:
    cleaned = "" if value is None else value.strip()
    if not cleaned:
        raise AppError("Title is required")
    return cleaned


def _priority(value: int | None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
        raise AppError("Priority must be an integer from 1 to 5")
    return value


def _state(value: str | None) -> str:
    if value not in STATES:
        raise AppError("State must be not_done, partial, or done")
    return value


def _out(row: Todo) -> TodoOut:
    return TodoOut.model_validate(row)


def _require_list(session, list_id: int) -> TodoList:
    row = session.get(TodoList, list_id)
    if row is None:
        raise AppError("List not found", 404)
    return row


def _require_todo(session, todo_id: int) -> Todo:
    row = session.get(Todo, todo_id)
    if row is None:
        raise AppError("To-do not found", 404)
    return row


def _check_alarm(at_time, alarm_at) -> None:
    if alarm_at is not None and at_time is None:
        raise AppError("alarm_at requires at_time")


def list_todos(list_id: int) -> list[TodoOut]:
    with session_scope() as session:
        _require_list(session, list_id)
        rows = session.scalars(
            select(Todo)
            .where(Todo.list_id == list_id, Todo.copy_confirmed.is_(True))
            .order_by(Todo.position, Todo.id)
        ).all()
        return [_out(row) for row in rows]


def create_todo(list_id: int, body: TodoCreate) -> TodoOut:
    title = _title(body.title)
    priority = _priority(body.priority)
    state = "not_done" if body.state is None else _state(body.state)
    _check_alarm(body.at_time, body.alarm_at)
    with session_scope() as session:
        _require_list(session, list_id)
        if body.parent_id is not None:
            parent = session.get(Todo, body.parent_id)
            if parent is None:
                raise AppError("Parent to-do not found")
            if parent.list_id != list_id:
                raise AppError("Parent to-do is on a different list")
        if body.position is None:
            max_position = session.scalar(
                select(func.max(Todo.position)).where(Todo.list_id == list_id)
            )
            position = (max_position or 0) + 1
        else:
            position = body.position
        row = Todo(
            list_id=list_id,
            parent_id=body.parent_id,
            position=position,
            title=title,
            state=state,
            priority=priority,
            notes="" if body.notes is None else body.notes,
            on_date=body.on_date,
            at_time=body.at_time,
            alarm_at=body.alarm_at,
            person_name=_person(body.person_name) if body.person_name is not None else None,
            copy_id=None,
            copy_confirmed=True,
        )
        session.add(row)
        session.flush()
        return _out(row)


def get_todo(todo_id: int) -> TodoOut:
    with session_scope() as session:
        return _out(_require_todo(session, todo_id))


def update_todo(todo_id: int, body: TodoPatch) -> TodoOut:
    fields = body.model_fields_set
    with session_scope() as session:
        row = _require_todo(session, todo_id)
        if "title" in fields:
            row.title = _title(body.title)
        if "priority" in fields:
            row.priority = _priority(body.priority)
        if "state" in fields:
            row.state = _state(body.state)
        if "notes" in fields:
            row.notes = "" if body.notes is None else body.notes
        if "position" in fields:
            if body.position is None:
                raise AppError("Position is required")
            row.position = body.position
        if "person_name" in fields:
            row.person_name = _person(body.person_name)
        if "on_date" in fields:
            row.on_date = body.on_date
        if "at_time" in fields:
            row.at_time = body.at_time
        if "alarm_at" in fields:
            row.alarm_at = body.alarm_at
        _check_alarm(row.at_time, row.alarm_at)
        session.flush()
        return _out(row)


def delete_todo(todo_id: int) -> None:
    with session_scope() as session:
        row = _require_todo(session, todo_id)
        session.delete(row)


def _person(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None
