from app.models import reports_models
from app.models import user_models
from app.db.database import SessionLocal
        


class ReportRepo:
    
    def __init__(self):
        self.db = SessionLocal()

    def commit(self):
        self.db.commit()
        
    def refresh(self, obj):
        self.db.refresh(obj)

    def close(self):
        self.db.close()
    
    
    def create_report(
        self,
        report
    ):

        self.db.add(report)

        self.commit()

        self.refresh(report)

        return report

    def get_reports(
        self,
        user_id
    ):

        return (
            self.db.query(
                reports_models.Report
            )
            .filter(
                reports_models.Report.user_id == user_id
            )
            .order_by(
                reports_models.Report.report_date.desc(),
                reports_models.Report.id.desc()
            )
            .all()
        )

    def get_company_reports(
        self,
        company_id
    ):

        return (
            self.db.query(
                reports_models.Report
            )
            .join(
                user_models.User,
                reports_models.Report.user_id == user_models.User.id
            )
            .filter(
                user_models.User.company_id == company_id
            )
            .order_by(
                reports_models.Report.report_date.desc()
            )
            .all()
        )