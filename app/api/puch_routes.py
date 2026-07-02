from fastapi import APIRouter, Depends

from app.config.settings import (
    get_current_user,
    require_admin,
)
from app.schemas.user import (
    AdminCreateSchema,
    LoginSchema,
    UserCreateSchema,
    CompanyCreateSchema,
    PunchSchema,
    AttendanceCreate,
)
from app.services.user_services import UserService
from app.services.attendance_services import AttendanceService
from app.services.company_services import CompanyServices

punch_router = APIRouter(prefix="/punch", tags=["Punch"])

company_service = CompanyServices()

attendence_services = AttendanceService()

@punch_router.get("/my-attendance")
def my_attendance(
    current_user=Depends(get_current_user),
):
    return attendence_services.my_attendance(
        current_user,
    )

@punch_router.post("/tap")
def tap(
    payload: AttendanceCreate,
    current_user=Depends(get_current_user)
):
    return company_service.attendance_action(
        payload,
        current_user
    )

@punch_router.get("/miss_punch")
def miss_punch(
    user = Depends(get_current_user)
):
    return company_service.miss_punchout(
        user
    )
