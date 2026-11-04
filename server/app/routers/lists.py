from fastapi import APIRouter, Response

from app.schemas import ListCreate, ListOut, ListUpdate
from app.services import lists as lists_service

router = APIRouter(prefix="/api/lists", tags=["lists"])


@router.get("", operation_id="list_lists")
def list_lists() -> list[ListOut]:
    return lists_service.list_lists()


@router.post("", operation_id="create_list", status_code=201)
def create_list(body: ListCreate) -> ListOut:
    return lists_service.create_list(body.name)


@router.patch("/{list_id}", operation_id="update_list")
def update_list(list_id: int, body: ListUpdate) -> ListOut:
    return lists_service.rename_list(list_id, body.name)


@router.delete("/{list_id}", operation_id="delete_list", status_code=204)
def delete_list(list_id: int) -> Response:
    lists_service.delete_list(list_id)
    return Response(status_code=204)
