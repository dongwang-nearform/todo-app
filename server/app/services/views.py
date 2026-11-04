from datetime import date, timedelta

from sqlalchemy import select

from app.db import session_scope
from app.errors import AppError
from app.models import Todo
from app.parsing import parse_required_date
from app.schemas import PeriodOut, TodayOut, TodoOut

GRAINS = {"day", "week", "month", "year"}


def _out(row: Todo) -> TodoOut:
    return TodoOut.model_validate(row)


def _date(value: str, field: str) -> date:
    try:
        return parse_required_date(value)
    except ValueError as exc:
        raise AppError(f"{field} {exc}") from exc


def today(on_date_raw: str) -> TodayOut:
    on_date = _date(on_date_raw, "on_date")
    with session_scope() as session:
        rows = session.scalars(
            select(Todo)
            .where(Todo.copy_confirmed.is_(True), Todo.on_date == on_date)
            .order_by(Todo.position, Todo.id)
        ).all()
        next_todo_id = next((row.id for row in rows if row.state != "done"), None)
        return TodayOut(
            on_date=on_date,
            todos=[_out(row) for row in rows],
            next_todo_id=next_todo_id,
        )


def not_done() -> list[TodoOut]:
    with session_scope() as session:
        rows = session.scalars(
            select(Todo)
            .where(Todo.copy_confirmed.is_(True), Todo.state != "done")
            .order_by(Todo.list_id, Todo.position, Todo.id)
        ).all()
        return [_out(row) for row in rows]


def period(grain: str, anchor_raw: str) -> PeriodOut:
    if grain not in GRAINS:
        raise AppError("grain must be day, week, month, or year")
    anchor = _date(anchor_raw, "anchor")
    start, end = _bounds(grain, anchor)
    with session_scope() as session:
        dated = session.scalars(
            select(Todo)
            .where(
                Todo.copy_confirmed.is_(True),
                Todo.on_date.is_not(None),
                Todo.on_date >= start,
                Todo.on_date <= end,
            )
            .order_by(Todo.on_date, Todo.position, Todo.id)
        ).all()
        undated = session.scalars(
            select(Todo)
            .where(Todo.copy_confirmed.is_(True), Todo.on_date.is_(None))
            .order_by(Todo.position, Todo.id)
        ).all()
        return PeriodOut(
            grain=grain,
            anchor=anchor,
            todos=[_out(row) for row in dated],
            undated=[_out(row) for row in undated],
        )


def _bounds(grain: str, anchor: date) -> tuple[date, date]:
    if grain == "day":
        return anchor, anchor
    if grain == "week":
        start = anchor - timedelta(days=anchor.weekday())
        return start, start + timedelta(days=6)
    if grain == "month":
        start = anchor.replace(day=1)
        if anchor.month == 12:
            next_month = date(anchor.year + 1, 1, 1)
        else:
            next_month = date(anchor.year, anchor.month + 1, 1)
        return start, next_month - timedelta(days=1)
    return date(anchor.year, 1, 1), date(anchor.year, 12, 31)
