from fastapi import APIRouter

from app.schemas import CopyCreate, CopyOut
from app.services import copies as copies_service

router = APIRouter(prefix="/api/copies", tags=["copies"])


@router.post("", operation_id="create_copy", status_code=201)
def create_copy(body: CopyCreate) -> CopyOut:
    return copies_service.create_copy(
        body.source_list_id,
        body.destination_list_id,
        body.on_date,
    )


@router.get("/{copy_id}", operation_id="get_copy")
def get_copy(copy_id: int) -> CopyOut:
    return copies_service.get_copy(copy_id)


@router.post("/{copy_id}/confirm", operation_id="confirm_copy")
def confirm_copy(copy_id: int) -> CopyOut:
    return copies_service.confirm_copy(copy_id)
