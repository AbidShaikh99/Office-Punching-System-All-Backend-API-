from datetime import datetime
from sqlalchemy.orm import relationship

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

class LeaveStatus(Base):
    __tablename__ = "leave_status"
    
    
    id = Column(Integer, primary_key=True)
    status = Column(String)
    leaves = relationship("Leave",back_populates="leave_status")
     