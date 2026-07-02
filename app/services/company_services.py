from datetime import date
import calendar

from fastapi import HTTPException

from app.repositories.attend_repo import AttendanceRepo
from app.services.user_services import UserService
from app.utils.response import success_response
from app.schemas.user import AttendanceOut, CompanyOut


class CompanyServices:

    def __init__(self):
        self.repo = AttendanceRepo()

    def miss_punchout(
        self,
        current_user
    ):

        attendances = self.repo.miss_out_punch(
            current_user.id
        )

        return success_response(
            "Punch Out Fetch Successfully.",
            [
                AttendanceOut.model_validate(item)
                for item in attendances
            ]
        )

    def list_companies(
        self,
        current_admin
    ):

        companies = self.repo.get_company_list(
            current_admin.company_id
        )

        return success_response(
            "Companies fetched successfully",
            [
                CompanyOut.model_validate(company)
                for company in companies
            ]
        )

    def update_company(
        self,
        company_id,
        payload,
        current_admin
    ):

        company = self.repo.get_company_by_id(
            company_id
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        if company.id != current_admin.company_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update this company"
            )

        company.company_name = payload.company_name
        company.company_category = payload.company_category
        company.latitude = payload.latitude
        company.longitude = payload.longitude

        self.repo.commit()
        self.repo.refresh(company)

        return success_response(
            "Company updated successfully",
            CompanyOut.model_validate(company)
        )

    def attendance_action(
        self,
        payload,
        current_user
    ):

        company = current_user.company

        if not company:
            raise HTTPException(
                status_code=400,
                detail="Company not assigned"
            )

        distance = UserService.calculate_distance_meters(
            payload.latitude,
            payload.longitude,
            company.latitude,
            company.longitude
        )

        if distance > 10:
            raise HTTPException(
                status_code=400,
                detail="You are not at the authorized location"
            )

        last_attendance = self.repo.get_today_open_attendance(
            current_user.id
        )

        if not last_attendance:

            attendance = self.repo.create_attendance(
                current_user.id,
                payload.latitude,
                payload.longitude
            )

            return success_response(
                "Punch In Successfully",
                AttendanceOut.model_validate(attendance)
            )

        if last_attendance.punch_out is None:

            attendance = self.repo.punch_out_attendance(
                last_attendance,
                payload.latitude,
                payload.longitude
            )

            return success_response(
                "Punch Out Successfully",
                AttendanceOut.model_validate(attendance)
            )

        attendance = self.repo.create_attendance(
            current_user.id,
            payload.latitude,
            payload.longitude
        )

        return success_response(
            "Punch In Successfully",
            AttendanceOut.model_validate(attendance)
        )

    def salary_details(
        self,
        current_user
    ):

        attendances = self.repo.get_month_data(
            current_user.id
        )

        total_seconds = 0

        for attendance in attendances:

            if attendance.punch_in and attendance.punch_out:

                duration = (
                    attendance.punch_out -
                    attendance.punch_in
                )

                total_seconds += int(
                    duration.total_seconds()
                )

        total_hours = round(
            total_seconds / 3600,
            2
        )

        today = date.today()

        month_days = calendar.monthrange(
            today.year,
            today.month
        )[1]

        if current_user.salary is None:

            raise HTTPException(
                status_code=400,
                detail="Salary not assigned by admin"
            )

        salary = float(
            current_user.salary
        )

        per_day_salary = round(
            salary / month_days,
            2
        )

        worked_days = round(
            total_hours / 8,
            2
        )

        earned_salary = round(
            worked_days * per_day_salary,
            2
        )

        return success_response(
            "Salary Details",
            {
                "monthly_salary": salary,
                "month_days": month_days,
                "total_working_hours": total_hours,
                "worked_days": worked_days,
                "per_day_salary": per_day_salary,
                "earned_salary": earned_salary
            }
        )