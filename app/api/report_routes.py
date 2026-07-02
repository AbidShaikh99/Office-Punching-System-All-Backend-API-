from fastapi import APIRouter, Depends

from app.config.settings import get_current_user
from app.schemas.report import CreateWorkReportSchema
from app.services.reports_services import ReportService

report_router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

report_service = ReportService()


@report_router.post("/create")
def create_report(
    payload: CreateWorkReportSchema,
    current_user=Depends(get_current_user)
):
    return report_service.create_report(
        payload,
        current_user
    )


@report_router.get("/")
def get_reports(
    user_id: int = None,
    current_user=Depends(get_current_user)
):
    return report_service.get_reports(
        current_user,
        user_id
    )