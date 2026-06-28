from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class LoanStatusEnum(str, Enum):
    active = "active"
    returned = "returned"
    overdue = "overdue"

class LoanCreate(BaseModel):

    user_id: int

    device_id: int

    status: LoanStatusEnum = LoanStatusEnum.active


class LoanUpdate(BaseModel):

    status: LoanStatusEnum

    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):

    id: int

    user_id: int

    device_id: int

    loan_date: datetime

    return_date: Optional[datetime]

    status: LoanStatusEnum

    model_config = {
        "from_attributes": True
    }


class LoanUserResponse(BaseModel):

    id: int

    name: str

    email: str

    model_config = {
        "from_attributes": True
    }


class LoanDeviceResponse(BaseModel):

    id: int

    name: str

    serial_number: str

    device_type: str

    model_config = {
        "from_attributes": True
    }


class LoanDetailResponse(BaseModel):

    id: int

    status: LoanStatusEnum

    user: LoanUserResponse

    device: LoanDeviceResponse

    model_config = {
        "from_attributes": True
    }