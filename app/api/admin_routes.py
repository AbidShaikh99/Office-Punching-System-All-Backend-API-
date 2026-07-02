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
    SalarySchemas,
)
from app.services.user_services import *
from app.services.attendance_services import AttendanceService
from app.services.company_services import CompanyServices
from app.api.auth_routes import user_services, leave_services
from app.api.puch_routes import attendence_services, company_service


admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/users")
def create_user(
    payload: UserCreateSchema,
    current_admin=Depends(require_admin),
):
    return user_services.create_user(
        payload,
        current_admin,
    )


@admin_router.get("/users")
def list_users(
    current_admin=Depends(require_admin),
):
    return user_services.list_users(
        current_admin,
    )


@admin_router.get("/companies")
def list_companies(
    current_admin=Depends(require_admin),
):
    return company_service.list_companies(
        current_admin,
    )


@admin_router.put("/companies/{company_id}")
def update_company(
    company_id: int,
    payload: CompanyCreateSchema,
    current_admin=Depends(require_admin),
):
    return company_service.update_company(
        company_id,
        payload,
        current_admin,
    )


@admin_router.get("/attendance")
def list_attendance(
    current_admin=Depends(require_admin),
):
    return attendence_services.list_attendance(
        current_admin,
    )

@admin_router.post("/all/salary")
def get_all_by_user_salary(
    payload: SalarySchemas,
    current_admin = Depends(require_admin)
):
    return attendence_services.list_salary(
        
        current_admin,
        payload.user_id,
        payload.month,
        payload.year
    )