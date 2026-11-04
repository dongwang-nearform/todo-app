from sqlalchemy import func, select

from app.db import session_scope
from app.errors import AppError
from app.models import TodoList
from app.schemas import ListOut


def _name(value: str | None) -> str:
    cleaned = "" if value is None else value.strip()
    if not cleaned:
        raise AppError("List name is required")
    return cleaned


def _out(row: TodoList) -> ListOut:
    return ListOut.model_validate(row)


def list_lists() -> list[ListOut]:
    with session_scope() as session:
        rows = session.scalars(select(TodoList).order_by(TodoList.position, TodoList.id)).all()
        return [_out(row) for row in rows]


def create_list(name: str | None) -> ListOut:
    cleaned = _name(name)
    with session_scope() as session:
        max_position = session.scalar(select(func.max(TodoList.position))) or 0
        row = TodoList(name=cleaned, position=max_position + 1)
        session.add(row)
        session.flush()
        return _out(row)


def rename_list(list_id: int, name: str | None) -> ListOut:
    cleaned = _name(name)
    with session_scope() as session:
        row = session.get(TodoList, list_id)
        if row is None:
            raise AppError("List not found", 404)
        row.name = cleaned
        session.flush()
        return _out(row)


def delete_list(list_id: int) -> None:
    with session_scope() as session:
        row = session.get(TodoList, list_id)
        if row is None:
            raise AppError("List not found", 404)
        session.delete(row)
