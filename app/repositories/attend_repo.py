from sqlalchemy import func, extract
from datetime import date
from app.db.database import SessionLocal
from app.models import user_models
from app.models import company_models
from app.models import attendence_models
from app.models import leave_models
from app.models import leave_request_models
from app.models.attendence_models import Attendance


class AttendanceRepo:

    def __init__(self):
        self.db = SessionLocal()

    def commit(self):
        self.db.commit()

    def refresh(self, obj):
        self.db.refresh(obj)

    def close(self):
        self.db.close()

    def get_user_by_email(self, email):
        return (
            self.db.query(user_models.User)
            .filter(user_models.User.email == email)
            .first()
        )

    def create_user(self, user):
        self.db.add(user)
        self.commit()
        self.db.refresh(user)
        return user

    def get_company_users(self, company_id):
        return (
            self.db.query(user_models.User)
            .filter(user_models.User.company_id == company_id)
            .order_by(user_models.User.id.desc())
            .all()
        )

    def create_company(self, company):
        self.db.add(company)
        self.db.flush()
        return company

    def get_company_by_id(self, company_id):
        return (
            self.db.query(company_models.Company)
            .filter(company_models.Company.id == company_id)
            .first()
        )

    def get_company_list(self, company_id):
        return (
            self.db.query(company_models.Company)
            .filter(company_models.Company.id == company_id)
            .order_by(company_models.Company.id.desc())
            .all()
        )

    def get_open_attendance(self, user_id):
        return (
            self.db.query(Attendance)
            .filter(
                Attendance.user_id == user_id,
                Attendance.punch_out.is_(None)
            )
            .order_by(Attendance.punch_in.desc())
            .first()
        )

    def create_attendance(self, user_id, latitude, longitude):
        attendance = attendence_models.Attendance(
            user_id=user_id,
            punch_in_latitude=latitude,
            punch_in_longitude=longitude,
        )

        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)

        return attendance

    def punch_out_attendance(self, attendance, latitude, longitude):
        attendance.punch_out = func.now()
        attendance.punch_out_latitude = latitude
        attendance.punch_out_longitude = longitude

        self.db.commit()
        self.db.refresh(attendance)

        return attendance

    def get_company_attendance(self, company_id):
        return (
            self.db.query(attendence_models.Attendance)
            .join(user_models.User)
            .filter(user_models.User.company_id == company_id)
            .order_by(attendence_models.Attendance.punch_in.desc())
            .all()
        )

    def get_user_attendance(self, user_id):
        return (
            self.db.query(attendence_models.Attendance)
            .filter(attendence_models.Attendance.user_id == user_id)
            .order_by(attendence_models.Attendance.id.desc())
            .all()
        )

    def get_today_open_attendance(self, user_id):
        return (
            self.db.query(attendence_models.Attendance)
            .filter(attendence_models.Attendance.user_id == user_id)
            .order_by(attendence_models.Attendance.id.desc())
            .first()
        )

    def get_user_profile(self, user):
        return (
            self.db.query(user_models.User)
            .filter(user_models.User.id == user.id)
            .first()
        )

    def get_user_details(self, user_id):
        return (
            self.db.query(attendence_models.Attendance)
            .filter(attendence_models.Attendance.user_id == user_id)
            .all()
        )

    def miss_out_punch(self, user_id):
        return (
            self.db.query(attendence_models.Attendance)
            .filter(
                attendence_models.Attendance.user_id == user_id,
                attendence_models.Attendance.punch_out.is_(None)
            ).all()
        )

    def get_month_data(self, user_id):
        today = date.today()
        return (
            self.db.query(attendence_models.Attendance)
            .filter(
                attendence_models.Attendance.user_id == user_id,
                extract("month", attendence_models.Attendance.punch_in) == today.month,
                extract("year", attendence_models.Attendance.punch_in) == today.year,
                attendence_models.Attendance.punch_out.isnot(None)
            ).all()
        )

    def get_user_month_data(self, company_id):
        return (
            self.db.query(user_models.User)
            .filter(
                user_models.User.company_id == company_id,
                user_models.User.role == "user",
            )
            .all()
        )

    def get_missed_punch_outs(self, user_id=None, month=None, year=None):
        query = self.db.query(attendence_models.Attendance).filter(
            attendence_models.Attendance.punch_out.is_(None)
        )

        if user_id:
            query = query.filter(attendence_models.Attendance.user_id == user_id)

        if month:
            query = query.filter(
                extract("month", attendence_models.Attendance.punch_in) == month
            )

        if year:
            query = query.filter(
                extract("year", attendence_models.Attendance.punch_in) == year
            )

        return query.all()

    def get_month_by_data(self, user_id=None, month=None, year=None):
        query = self.db.query(attendence_models.Attendance)

        if user_id:
            query = query.filter(attendence_models.Attendance.user_id == user_id)

        if month:
            query = query.filter(
                extract("month", attendence_models.Attendance.punch_in) == month
            )

        if year:
            query = query.filter(
                extract("year", attendence_models.Attendance.punch_in) == year
            )

        return query.all()

    def create_leave(self, leave):
        self.db.add(leave)
        self.db.commit()
        self.db.refresh(leave)
        return leave

    def get_all_leaves(self, company_id):
        return (
            self.db.query(leave_models.Leave)
            .join(
                user_models.User,
                leave_models.Leave.user_id == user_models.User.id
            )
            .filter(user_models.User.company_id == company_id)
            .all()
        )

    def get_leave_by_id(self, leave_id):
        return (
            self.db.query(leave_models.Leave)
            .filter(leave_models.Leave.id == leave_id)
            .first()
        )

    def update_leave_status(self, leave, status_id, admin_reason, approved_by):
        leave.leave_status_id = status_id
        leave.admin_reason = admin_reason
        leave.approved_by = approved_by
        self.db.commit()
        self.db.refresh(leave)
        return leave

    def update_monthly_leave(self, user):
        today = date.today()
        if (
            user.last_leave_credit is None
            or user.last_leave_credit.month != today.month
            or user.last_leave_credit.year != today.year
        ):
            user.paid_leave += 1
            user.last_leave_credit = today
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_user(self, user, payload):
        if payload.name is not None:
            user.name = payload.name
        if payload.email is not None:
            user.email = payload.email
        if payload.salary is not None:
            user.salary = payload.salary
        if payload.paid_leave:
            user.paid_leave += 1
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id):
        return self.db.query(user_models.User).filter(
            user_models.User.id == user_id
        ).first()

    def get_all_attendance(self, user_id):
        return (
            self.db.query(attendence_models.Attendance)
            .filter(attendence_models.Attendance.user_id == user_id)
            .all()
        )

    def get_approved_leaves(self, user_id, month=None, year=None):
        query = (
            self.db.query(leave_models.Leave)
            .filter(
                leave_models.Leave.user_id == user_id,
                leave_models.Leave.leave_status_id == 2,
                leave_models.Leave.leave_type == "paid_leave"
            )
        )
        if month:
            query = query.filter(
                extract("month", leave_models.Leave.from_date) == month
            )
        if year:
            query = query.filter(
                extract("year", leave_models.Leave.from_date) == year
            )
        return query.all()

    def get_user_by_idd(self, user_id):
        return (
            self.db.query(user_models.User)
            .filter(user_models.User.id == user_id)
            .first()
        )