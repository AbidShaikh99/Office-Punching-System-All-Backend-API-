from collections import defaultdict
from datetime import date
import calendar

from app.repositories.attend_repo import AttendanceRepo
from app.utils.response import *
from fastapi import HTTPException


class AttendanceService:

    def __init__(self):
        self.repo = AttendanceRepo()

    def my_attendance(
        self,
        current_user
    ):

        attendance = self.repo.get_user_attendance(
            current_user.id
        )

        return success_response(
            "Attendance fetched successfully",
            attendance
        )

    def list_attendance(
        self,
        current_admin
    ):

        attendance_records = self.repo.get_company_attendance(
            current_admin.company_id
        )

        grouped_data = defaultdict(list)

        for record in attendance_records:

            date_key = record.punch_in.date().isoformat()

            grouped_data[date_key].append(
                {
                    "attendance_id": record.id,
                    "user_id": record.user_id,
                    "user_name": record.user.name,
                    "punch_in": record.punch_in,
                    "punch_out": record.punch_out,
                    "punch_in_latitude": record.punch_in_latitude,
                    "punch_in_longitude": record.punch_in_longitude,
                    "punch_out_latitude": record.punch_out_latitude,
                    "punch_out_longitude": record.punch_out_longitude,
                }
            )

        response_data = []

        for date_key, records in grouped_data.items():

            response_data.append(
                {
                    "date": date_key,
                    "attendance": records
                }
            )

        return success_response(
            "Attendance fetched successfully",
            response_data
        )

    def list_salary(
        self,
        current_admin,
        user_id=None,
        month=None,
        year=None
    ):

        users = self.repo.get_user_month_data(
            current_admin.company_id
        )

        result = []

        if month and (month < 1 or month > 12):

            return error_response(
                "Please enter valid month"
            )

        if month and not year:

            return error_response(
                "Year is required when month is provided"
            )

        for user in users:

            if user_id and user.id != user_id:
                continue

            if month and year:

                attendances = self.repo.get_month_by_data(
                    user.id,
                    month,
                    year
                )

                month_days = calendar.monthrange(
                    year,
                    month
                )[1]

            else:

                attendances = self.repo.get_all_attendance(
                    user.id
                )

                today = date.today()

                month_days = calendar.monthrange(
                    today.year,
                    today.month
                )[1]

            approved_leaves = self.repo.get_approved_leaves(
                user.id,
                month,
                year
            )

            total_seconds = 0

            for attendance in attendances:

                if attendance.punch_in and attendance.punch_out:

                    duration = (
                        attendance.punch_out
                        -
                        attendance.punch_in
                    )

                    total_seconds += int(
                        duration.total_seconds()
                    )

            total_hours = round(
                total_seconds / 3600,
                2
            )

            worked_days = round(
                total_hours / 8,
                2
            )

            paid_leave_days = 0

            paid_leave_history = []

            for leave in approved_leaves:

                leave_days = (
                    leave.to_date
                    -
                    leave.from_date
                ).days + 1

                paid_leave_days += leave_days

                paid_leave_history.append(
                    {
                        "leave_id": leave.id,
                        "from_date": leave.from_date.strftime("%Y-%m-%d"),
                        "to_date": leave.to_date.strftime("%Y-%m-%d"),
                        "days": leave_days,
                        "reason": leave.reason
                    }
                )

            salary = float(
                user.salary or 0
            )

            per_day_salary = round(
                salary / month_days,
                2
            )

            payable_days = round(
                worked_days + paid_leave_days,
                2
            )

            earned_salary = round(
                payable_days * per_day_salary,
                2
            )

            missed_attendances = self.repo.get_missed_punch_outs(
                user.id,
                month,
                year
            )

            missed_punch_outs = []

            for item in missed_attendances:

                missed_punch_outs.append(
                    {
                        "attendance_id": item.id,
                        "date": item.punch_in.strftime("%Y-%m-%d"),
                        "punch_in_time": item.punch_in.strftime("%H:%M:%S")
                    }
                )

            result.append(
                {
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "monthly_salary": salary,
                    "total_working_hours": total_hours,
                    "worked_days": worked_days,
                    "perday_salary": per_day_salary,
                    "paid_leave_days": paid_leave_days,
                    "payable_days": payable_days,
                    "earned_salary": earned_salary,
                    "missed_punch_outs": missed_punch_outs,
                    "paid_leave": paid_leave_history
                }
            )

        return success_response(
            "Salary Report",
            result
        )

    def __del__(self):
        self.repo.close()