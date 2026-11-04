from fastapi import APIRouter

from app.schemas import PeriodOut, TodayOut, TodoOut
from app.services import views as views_service

router = APIRouter(prefix="/api/views", tags=["views"])


@router.get("/today", operation_id="get_today")
def get_today(on_date: str) -> TodayOut:
    return views_service.today(on_date)


@router.get("/not-done", operation_id="get_not_done")
def get_not_done() -> list[TodoOut]:
    return views_service.not_done()


@router.get("/period", operation_id="get_period")
def get_period(grain: str, anchor: str) -> PeriodOut:
    return views_service.period(grain, anchor)
