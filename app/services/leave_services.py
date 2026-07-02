from datetime import date

from app.models import leave_models
from app.repositories.attend_repo import AttendanceRepo
from app.utils.response import success_response, error_response


class LeaveService:

    def __init__(self):
        self.repo = AttendanceRepo()

    def leave(
        self,
        current_user,
        payload
    ):

        try:

            if payload.from_date > payload.to_date:
                return error_response(
                    "From Date Cannot be Greater Than To Date"
                )

            total_days = (
                payload.to_date -
                payload.from_date
            ).days + 1

            if payload.leave_type not in [
                "paid_leave",
                "unpaid_leave"
            ]:
                return error_response(
                    "Invalid Leave Type"
                )

            if (
                payload.leave_type == "paid_leave"
                and total_days > current_user.paid_leave
            ):
                return error_response(
                    f"You only have {current_user.paid_leave} paid leaves available"
                )

            leave = leave_models.Leave(
                user_id=current_user.id,
                leave_type=payload.leave_type,
                from_date=payload.from_date,
                to_date=payload.to_date,
                reason=payload.reason,
                leave_status_id=1
            )

            self.repo.create_leave(leave)

            return success_response(
                "Leave Applied Successfully"
            )

        except Exception as e:
            self.repo.rollback()
            return error_response(str(e))

        finally:
            self.repo.close()

    def get_all_leaves(
        self,
        current_admin
    ):

        try:

            leaves = self.repo.get_all_leaves(
                current_admin.company_id
            )

            result = []

            for leave in leaves:

                result.append({
                    "leave_id": leave.id,
                    "user_id": leave.user.id,
                    "name": leave.user.name,
                    "email": leave.user.email,
                    "leave_type": leave.leave_type,
                    "from_date": leave.from_date,
                    "to_date": leave.to_date,
                    "reason": leave.reason,
                    "status": (
                        leave.leave_status.status
                        if leave.leave_status
                        else "Pending"
                    ),
                    "created_at": leave.created_at
                })

            return success_response(
                "All Leave Requests",
                result
            )

        finally:
            self.repo.close()

    def update_leave_status(
        self,
        current_admin,
        payload
    ):

        try:

            leave = self.repo.get_leave_by_id(
                payload.leave_id
            )

            if not leave:
                return error_response(
                    "Leave not found"
                )

            if payload.status_id not in [2, 3]:
                return error_response(
                    "Status must be Approved(2) or Denied(3)"
                )

            if (
                payload.status_id == 3
                and not payload.admin_reason
            ):
                return error_response(
                    "Reason required for denied leave"
                )

            if payload.status_id == 2:

                if leave.leave_type == "paid_leave":

                    total_days = (
                        leave.to_date -
                        leave.from_date
                    ).days + 1

                    if leave.user.paid_leave < total_days:
                        return error_response(
                            f"Only {leave.user.paid_leave} paid leaves available"
                        )

                    leave.user.paid_leave -= total_days

            leave = self.repo.update_leave_status(
                leave,
                payload.status_id,
                payload.admin_reason,
                current_admin.id
            )

            return success_response(
                "Leave status updated successfully",
                {
                    "leave_id": leave.id,
                    "employee_name": leave.user.name,
                    "leave_type": leave.leave_type,
                    "status_id": leave.leave_status_id,
                    "admin_reason": leave.admin_reason,
                    "approved_by": current_admin.name,
                    "remaining_paid_leave": leave.user.paid_leave
                }
            )

        except Exception as e:
            self.repo.rollback()
            return error_response(str(e))

        finally:
            self.repo.close()

    def get_leave_balance(
        self,
        current_user
    ):

        try:

            today = date.today()

            if (
                current_user.last_leave_credit is None
                or current_user.last_leave_credit.month != today.month
                or current_user.last_leave_credit.year != today.year
            ):

                current_user = self.repo.update_monthly_leave(
                    current_user
                )

            return success_response(
                "Leave Balance Retrieved Successfully",
                {
                    "user_id": current_user.id,
                    "name": current_user.name,
                    "paid_leave": current_user.paid_leave,
                }
            )

        except Exception as e:
            self.repo.rollback()
            return error_response(str(e))

        finally:
            self.repo.close()

    def update_user(
        self,
        current_admin,
        payload
    ):

        try:

            user = self.repo.get_user_by_id(
                payload.user_id
            )

            if not user:
                return error_response(
                    "User not found"
                )

            user = self.repo.update_user(
                user,
                payload
            )

            return success_response(
                "User updated successfully",
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "salary": user.salary,
                    "paid_leave": user.paid_leave,
                }
            )

        except Exception as e:
            self.repo.rollback()
            return error_response(str(e))

        finally:
            self.repo.close()