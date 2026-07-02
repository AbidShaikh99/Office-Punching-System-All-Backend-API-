from collections import defaultdict

from app.models import reports_models
from app.repositories.report_repo import ReportRepo
from app.repositories.attend_repo import AttendanceRepo
from app.utils.response import success_response, error_response


class ReportService:

    def __init__(self):
        self.report_repo = ReportRepo()
        self.attendance_repo = AttendanceRepo()

    def create_report(
        self,
        payload,
        current_user
    ):

        try:

            report = reports_models.Report(
                user_id=current_user.id,
                company_id=current_user.company_id,
                report_date=payload.report_date,
                project_name=payload.project_name,
                task_name=payload.task_name,
                estimated_hours=payload.estimated_hours,
                actual_hours=payload.actual_hours,
                task_status=payload.task_status,
                priority=payload.priority,
                work_done=payload.work_done,
                next_day_plan=payload.next_day_plan,
            )

            self.report_repo.create_report(
                report
            )

            return success_response(
                "Report Created Successfully"
            )

        except Exception as e:

            self.report_repo.rollback()

            return error_response(
                str(e)
            )

    def get_reports(
        self,
        current_user,
        user_id=None
    ):

        if current_user.role == "user":

            reports = self.report_repo.get_reports(
                current_user.id
            )

        else:

            if user_id:

                user = self.attendance_repo.get_user_by_idd(
                    user_id
                )

                if not user:

                    return error_response(
                        "User not found"
                    )

                if (
                    user.company_id
                    !=
                    current_user.company_id
                ):

                    return error_response(
                        "User does not belong to your company"
                    )

                reports = self.report_repo.get_reports(
                    user.id
                )

            else:

                reports = self.report_repo.get_company_reports(
                    current_user.company_id
                )

        grouped_data = defaultdict(
            lambda: {
                "total_tasks": 0,
                "total_estimate_hours": 0,
                "total_actual_hours": 0,
                "reports": []
            }
        )

        for report in reports:

            report_date = report.report_date.strftime(
                "%Y-%m-%d"
            )

            grouped_data[report_date]["total_tasks"] += 1
            grouped_data[report_date]["total_estimate_hours"] += report.estimated_hours
            grouped_data[report_date]["total_actual_hours"] += report.actual_hours

            grouped_data[report_date]["reports"].append(
                {
                    "report_id": report.id,
                    "project_name": report.project_name,
                    "task_name": report.task_name,
                    "estimated_hours": report.estimated_hours,
                    "actual_hours": report.actual_hours,
                    "task_status": report.task_status,
                    "priority": report.priority,
                    "work_done": report.work_done,
                    "next_day_plan": report.next_day_plan,
                }
            )

        result = []

        for report_date, value in grouped_data.items():

            result.append(
                {
                    "date": report_date,
                    "total_tasks": value["total_tasks"],
                    "total_estimated_hours": value["total_estimate_hours"],
                    "total_actual_hours": value["total_actual_hours"],
                    "reports": value["reports"],
                }
            )

        return success_response(
            "Reports Retrieved Successfully",
            result
        )

    def __del__(self):
        self.report_repo.close()
        self.attendance_repo.close()