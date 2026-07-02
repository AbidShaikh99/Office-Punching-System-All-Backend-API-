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
    LeaveSchemas,
    LeaveStatusUpdate,
    UpdateUserSchemas,
)
from app.services.user_services import UserService
from app.services.attendance_services import AttendanceService
from app.services.company_services import CompanyServices
from app.services.leave_services import LeaveService
from app.api.puch_routes import company_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
user_services = UserService()
leave_services = LeaveService()

@auth_router.post("/register-admin")
def register_admin(
    payload: AdminCreateSchema,
):
    return user_services.register_admin(payload)


@auth_router.post("/login")
def login(
    payload: LoginSchema,
):
    return user_services.login(payload)


@auth_router.get("/me")
def my_profile(
    current_user=Depends(get_current_user),
):
    return user_services.profile_user(
        current_user
    )

@auth_router.get("/data")
def get_details(
    current_user= Depends(get_current_user)
):
    return user_services.user_details(
        current_user.id,
    )

@auth_router.get("/salary")
def get_salary_details(
    current_user = Depends(get_current_user)
):
    return company_service.salary_details(
        current_user
    )

@auth_router.post("/leave")
def apply_leave(
    payload: LeaveSchemas,
    current_user=Depends(
        get_current_user
    )
):
    return leave_services.leave(
        current_user,
        payload
    )

@auth_router.get("/admin/leaves")
def get_all_leaves(
    current_admin=Depends(require_admin)
):
    return leave_services.get_all_leaves(
        current_admin
    )

@auth_router.put("/leave/status")
def update_leave_status(
    payload: LeaveStatusUpdate,
    current_admin = Depends(
        get_current_user
    )
):
    return leave_services.update_leave_status(
        current_admin,
        payload
    )

@auth_router.get("/leave/balance")
def get_leave_balance(
    current_user = Depends(get_current_user)
):
    return leave_services.get_leave_balance(
        current_user
    )

@auth_router.put("/update/user")
def update_user(
    payload: UpdateUserSchemas,
    current_admin = Depends(require_admin)
):
    return leave_services.update_user(
        
        current_admin,
        payload
    )