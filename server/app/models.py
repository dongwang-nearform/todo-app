from datetime import date, time

from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class TodoList(Base):
    __tablename__ = "lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)


class Copy(Base):
    __tablename__ = "copies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_list_id: Mapped[int] = mapped_column(Integer, nullable=False)
    destination_list_id: Mapped[int] = mapped_column(Integer, nullable=False)
    on_date: Mapped[date] = mapped_column(Date, nullable=False)


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = (
        CheckConstraint(
            "state IN ('not_done', 'partial', 'done')",
            name="ck_todos_state",
        ),
        CheckConstraint("priority >= 1 AND priority <= 5", name="ck_todos_priority"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    list_id: Mapped[int] = mapped_column(
        ForeignKey("lists.id", ondelete="CASCADE"),
        nullable=False,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("todos.id", ondelete="CASCADE"),
        nullable=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False, default="not_done")
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=False, default="")
    on_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    at_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    alarm_at: Mapped[time | None] = mapped_column(Time, nullable=True)
    person_name: Mapped[str | None] = mapped_column(String, nullable=True)
    copy_id: Mapped[int | None] = mapped_column(ForeignKey("copies.id"), nullable=True)
    copy_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
