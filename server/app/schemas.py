from datetime import date, time
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, field_serializer

from app.parsing import parse_optional_date, parse_optional_time

def _reject_bool(value: object) -> object:
    if isinstance(value, bool):
        raise ValueError("Priority must be an integer from 1 to 5")
    return value


OptionalDate = Annotated[date | None, BeforeValidator(parse_optional_date)]
OptionalTime = Annotated[time | None, BeforeValidator(parse_optional_time)]
Priority = Annotated[int | None, BeforeValidator(_reject_bool)]


class ListCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None


class ListUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None


class ListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    position: int


class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    priority: Priority = None
    state: str | None = None
    notes: str | None = None
    on_date: OptionalDate = None
    at_time: OptionalTime = None
    alarm_at: OptionalTime = None
    person_name: str | None = None
    parent_id: int | None = None
    position: int | None = None


class TodoPatch(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    priority: Priority = None
    state: str | None = None
    notes: str | None = None
    on_date: OptionalDate = None
    at_time: OptionalTime = None
    alarm_at: OptionalTime = None
    person_name: str | None = None
    position: int | None = None


class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    list_id: int
    parent_id: int | None
    position: int
    title: str
    state: str
    priority: int
    notes: str
    on_date: date | None
    at_time: time | None
    alarm_at: time | None
    person_name: str | None
    copy_id: int | None
    copy_confirmed: bool

    @field_serializer("on_date")
    def serialize_date(self, value: date | None) -> str | None:
        return None if value is None else value.isoformat()

    @field_serializer("at_time", "alarm_at")
    def serialize_time(self, value: time | None) -> str | None:
        return None if value is None else value.strftime("%H:%M:%S")


class TodayOut(BaseModel):
    on_date: date
    todos: list[TodoOut]
    next_todo_id: int | None

    @field_serializer("on_date")
    def serialize_date(self, value: date) -> str:
        return value.isoformat()


class PeriodOut(BaseModel):
    grain: str
    anchor: date
    todos: list[TodoOut]
    undated: list[TodoOut]

    @field_serializer("anchor")
    def serialize_anchor(self, value: date) -> str:
        return value.isoformat()


class CopyCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_list_id: int | None = None
    destination_list_id: int | None = None
    on_date: str | None = None


class CopyOut(BaseModel):
    id: int
    todos: list[TodoOut]
