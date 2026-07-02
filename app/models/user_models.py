from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.database import Base



class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    salary = Column(Float, nullable=True)
    paid_leave = Column(Integer,nullable=False,default=0)
    last_leave_credit = Column(Date,nullable=True)
    company = relationship("Company", back_populates="users")
    attendance = relationship("Attendance", back_populates="user")
    leaves = relationship("Leave",foreign_keys="Leave.user_id",back_populates="user")
