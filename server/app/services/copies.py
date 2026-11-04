from sqlalchemy import select

from app.db import session_scope
from app.errors import AppError
from app.models import Copy, Todo, TodoList
from app.parsing import parse_required_date
from app.schemas import CopyOut, TodoOut


def _out(row: Todo) -> TodoOut:
    return TodoOut.model_validate(row)


def _copy_out(copy_id: int, rows: list[Todo]) -> CopyOut:
    return CopyOut(id=copy_id, todos=[_out(row) for row in rows])


def _rows_for_copy(session, copy_id: int) -> list[Todo]:
    return list(
        session.scalars(
            select(Todo).where(Todo.copy_id == copy_id).order_by(Todo.position, Todo.id)
        ).all()
    )


def create_copy(
    source_list_id: int | None,
    destination_list_id: int | None,
    on_date_raw: str | None,
) -> CopyOut:
    if source_list_id is None:
        raise AppError("Source list not found", 404)
    if destination_list_id is None:
        raise AppError("Destination list not found", 404)
    try:
        on_date = parse_required_date(on_date_raw)
    except ValueError as exc:
        raise AppError(f"on_date {exc}") from exc
    with session_scope() as session:
        if session.get(TodoList, source_list_id) is None:
            raise AppError("Source list not found", 404)
        if session.get(TodoList, destination_list_id) is None:
            raise AppError("Destination list not found", 404)
        source_rows = session.scalars(
            select(Todo)
            .where(Todo.list_id == source_list_id, Todo.copy_confirmed.is_(True))
            .order_by(Todo.position, Todo.id)
        ).all()
        copy = Copy(
            source_list_id=source_list_id,
            destination_list_id=destination_list_id,
            on_date=on_date,
        )
        session.add(copy)
        session.flush()
        id_map: dict[int, int] = {}
        created: list[tuple[Todo, int | None]] = []
        for source in source_rows:
            row = Todo(
                list_id=destination_list_id,
                parent_id=None,
                position=source.position,
                title=source.title,
                state=source.state,
                priority=source.priority,
                notes=source.notes,
                on_date=on_date,
                at_time=source.at_time,
                alarm_at=source.alarm_at,
                person_name=source.person_name,
                copy_id=copy.id,
                copy_confirmed=False,
            )
            session.add(row)
            session.flush()
            id_map[source.id] = row.id
            created.append((row, source.parent_id))
        for row, parent_id in created:
            if parent_id is None:
                continue
            if parent_id not in id_map:
                raise AppError("Parent to-do was not copied")
            row.parent_id = id_map[parent_id]
        session.flush()
        return _copy_out(copy.id, _rows_for_copy(session, copy.id))


def get_copy(copy_id: int) -> CopyOut:
    with session_scope() as session:
        if session.get(Copy, copy_id) is None:
            raise AppError("Copy not found", 404)
        return _copy_out(copy_id, _rows_for_copy(session, copy_id))


def confirm_copy(copy_id: int) -> CopyOut:
    with session_scope() as session:
        if session.get(Copy, copy_id) is None:
            raise AppError("Copy not found", 404)
        rows = _rows_for_copy(session, copy_id)
        for row in rows:
            row.copy_confirmed = True
        session.flush()
        return _copy_out(copy_id, rows)
