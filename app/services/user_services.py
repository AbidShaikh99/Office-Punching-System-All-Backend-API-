from collections import defaultdict
from math import radians, sin, cos, sqrt, atan2
from datetime import date

from fastapi import HTTPException

from app.schemas.user import *
from app.models import (
    user_models,
    company_models,
    attendence_models
)

from app.repositories.attend_repo import AttendanceRepo

from app.config.settings import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.utils.response import success_response


class UserService:

    def __init__(self):
        self.repo = AttendanceRepo()

    
    def calculate_distance_meters(lat1, lon1, lat2, lon2):
        R = 6371000

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1))
            * cos(radians(lat2))
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def register_admin(self, payload):

        existing_user = self.repo.get_user_by_email(
            payload.email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        company = company_models.Company(
            company_name=payload.company.company_name,
            company_category=payload.company.company_category,
            latitude=payload.company.latitude,
            longitude=payload.company.longitude,
        )

        self.repo.create_company(company)

        admin = user_models.User(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
            role="admin",
            company_id=company.id,
        )

        self.repo.create_user(admin)

        return success_response(
            "Admin profile created successfully",
            UserLog.model_validate(admin)
        )

    def login(self, payload):

        user = self.repo.get_user_by_email(
            payload.email
        )

        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials"
            )

        if not verify_password(
            payload.password,
            user.password
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials"
            )

        token = create_access_token(
            {
                "user_id": user.id,
                "role": user.role,
            }
        )

        return {
            "status": True,
            "message": "Login successfully",
            "access_token": token,
            "token_type": "bearer",
            "user": UserLog.model_validate(user),
        }

    def create_user(
        self,
        payload,
        current_admin
    ):

        existing_user = self.repo.get_user_by_email(
            payload.email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user = user_models.User(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
            role="user",
            company_id=current_admin.company_id,
            salary=payload.salary,
            last_leave_credit=date.today(),
            paid_leave=0,
        )

        self.repo.create_user(user)

        return success_response(
            "User profile created successfully",
            [UserOut.model_validate(user)]
        )

    def list_users(
        self,
        current_admin
    ):

        users = self.repo.get_company_users(
            current_admin.company_id
        )

        return success_response(
            "Users fetched successfully",
            [
                UserLog.model_validate(user)
                for user in users
            ]
        )

    def profile_user(
        self,
        current_user
    ):

        user = self.repo.get_user_profile(
            current_user
        )

        return success_response(
            "User Profile",
            UserProfile.model_validate(user)
        )

    def user_details(
        self,
        user_id
    ):

        attendances = self.repo.get_user_details(
            user_id
        )

        grouped_data = {}

        for attendance in attendances:

            date_key = attendance.punch_in.strftime("%Y-%m-%d")

            if date_key not in grouped_data:

                grouped_data[date_key] = {
                    "date": date_key,
                    "logs": [],
                    "total_seconds": 0
                }

            grouped_data[date_key]["logs"].append(
                {
                    "type": "Punch In",
                    "time": attendance.punch_in.strftime("%H:%M:%S")
                }
            )

            if attendance.punch_out:

                grouped_data[date_key]["logs"].append(
                    {
                        "type": "Punch Out",
                        "time": attendance.punch_out.strftime("%H:%M:%S")
                    }
                )

                duration = (
                    attendance.punch_out
                    - attendance.punch_in
                )

                grouped_data[date_key]["total_seconds"] += int(
                    duration.total_seconds()
                )

        result = []

        for value in grouped_data.values():

            seconds = value.pop("total_seconds")

            h = seconds // 3600
            m = (seconds % 3600) // 60
            s = seconds % 60

            value["total_hours"] = f"{h:02}:{m:02}:{s:02}"

            result.append(value)

        result.sort(
            key=lambda x: x["date"],
            reverse=True
        )

        return success_response(
            "User History",
            result
        )