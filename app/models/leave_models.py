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


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    leave_status_id = Column(Integer,ForeignKey("leave_status.id"))
    leave_type = Column(String)
    from_date = Column(Date)
    to_date = Column(Date)
    reason = Column(Text)
    
    admin_reason = Column(Text,nullable=True)
    approved_by = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime, default= datetime.now)
    user = relationship("User",foreign_keys=[user_id],back_populates="leaves")
    admin = relationship("User",foreign_keys=[approved_by])
    leave_status = relationship("LeaveStatus", back_populates="leaves")
    