from datetime import datetime
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class CompanyCreateSchema(BaseModel):
    company_name: str = Field(min_length=2)
    company_category: str = Field(min_length=2)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class AdminCreateSchema(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    company: CompanyCreateSchema
    # latitude: float = Field(ge=-90, le=90)
    # longitude: float = Field(ge=-180, le=180)
    


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    salary: float = Field(
        gt=0,
        description="Monthly Salary"
    )
    # latitude: float = Field(ge=-90, le=90)
    # longitude: float = Field(ge=-180, le=180)


class PunchSchema(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class CompanyOut(BaseModel):
    id: int
    company_name: str
    company_category: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}

class UserLog(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    paid_leave: int
  
    company: CompanyOut
    
    model_config = {"from_attributes": True}

from typing import Optional

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    salary: float

    paid_leave: int

    company: CompanyOut

    model_config = {"from_attributes": True}

class UserProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    paid_leave_balance: int
    company:CompanyOut
    
    model_config = {"from_attributes": True}
    
class AttendanceCreate(BaseModel):
    latitude: float
    longitude: float

class AttendanceOut(BaseModel):
    id: int
    user_id: int
    punch_in: datetime
    punch_out: Optional[datetime] = None
    punch_in_latitude: float
    punch_in_longitude: float
    punch_out_latitude: Optional[float] = None
    punch_out_longitude: Optional[float] = None

    model_config = {"from_attributes": True}

class SalarySchemas(BaseModel):
    user_id: Optional[int]
    month: Optional[int]
    year:  Optional[int]


class LeaveSchemas(BaseModel):
    leave_type : str
    from_date : date
    to_date: date
    reason: str
    
class LeaveStatusUpdate(BaseModel):
    leave_id: int
    status_id: int
    admin_reason: Optional[str] = None


class UpdateUserSchemas(BaseModel):
    user_id : int
    name : Optional[str] = None
    email : Optional[str] = None
    salary : Optional[float] = None 
    paid_leave : Optional[int] = None
