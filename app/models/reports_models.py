from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.leave_request_models import LeaveStatus
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Date,
    Text,
    ForeignKey
)

from app.db.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index= True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    company_id = Column(Integer,ForeignKey("companies.id"),nullable=False)
    report_date = Column(Date, nullable= True)
    project_name = Column(String(255), nullable= True)
    task_name = Column(String(255), nullable= True)
    estimated_hours = Column(Integer,nullable=False)

    actual_hours = Column(Integer,nullable=False)
    task_status = Column(String(30),default="pending")
    priority = Column(String(20),default="Medium")
    work_done = Column(Text,nullable=False)
    next_day_plan = Column(Text)
    
    created_at = Column(DateTime,default=datetime.now)

    updated_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)