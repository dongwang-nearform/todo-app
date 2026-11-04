from fastapi import APIRouter, Response

from app.schemas import TodoCreate, TodoOut, TodoPatch
from app.services import todos as todos_service

router = APIRouter(tags=["todos"])


@router.get("/api/lists/{list_id}/todos", operation_id="list_todos")
def list_todos(list_id: int) -> list[TodoOut]:
    return todos_service.list_todos(list_id)


@router.post("/api/lists/{list_id}/todos", operation_id="create_todo", status_code=201)
def create_todo(list_id: int, body: TodoCreate) -> TodoOut:
    return todos_service.create_todo(list_id, body)


@router.get("/api/todos/{todo_id}", operation_id="get_todo")
def get_todo(todo_id: int) -> TodoOut:
    return todos_service.get_todo(todo_id)


@router.patch("/api/todos/{todo_id}", operation_id="update_todo")
def update_todo(todo_id: int, body: TodoPatch) -> TodoOut:
    return todos_service.update_todo(todo_id, body)


@router.delete("/api/todos/{todo_id}", operation_id="delete_todo", status_code=204)
def delete_todo(todo_id: int) -> Response:
    todos_service.delete_todo(todo_id)
    return Response(status_code=204)
