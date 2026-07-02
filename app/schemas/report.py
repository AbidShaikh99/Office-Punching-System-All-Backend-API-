from pydantic import BaseModel
from datetime import date
from typing import Optional


class CreateWorkReportSchema(BaseModel):

    report_date: date
    project_name: str
    task_name: str
    estimated_hours: float
    actual_hours: float
    progress: int
    task_status: str
    priority: str
    work_done: str
    next_day_plan: Optional[str] = None

