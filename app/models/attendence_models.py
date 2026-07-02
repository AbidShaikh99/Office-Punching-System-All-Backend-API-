from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    punch_in = Column(DateTime, default=datetime.now, nullable=False)
    punch_out = Column(DateTime, nullable=True)
    punch_in_latitude = Column(Float, nullable=False)
    punch_in_longitude = Column(Float, nullable=False)
    punch_out_latitude = Column(Float, nullable=True)
    punch_out_longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="attendance")