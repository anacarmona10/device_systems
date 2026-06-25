from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoanCreate(BaseModel):

    user_id: int

    device_id: int

    status: str = "active"


class LoanUpdate(BaseModel):

    status: Optional[str] = None

    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):

    id: int

    user_id: int

    device_id: int

    loan_date: datetime

    return_date: Optional[datetime]

    status: str

    model_config = {
        "from_attributes": True
    }


class LoanDetailUser(BaseModel):

    id: int

    name: str

    email: str

    model_config = {
        "from_attributes": True
    }


class LoanDetailDevice(BaseModel):

    id: int

    name: str

    serial_number: str

    device_type: str

    model_config = {
        "from_attributes": True
    }


class LoanDetailResponse(BaseModel):

    id: int

    status: str

    user: LoanDetailUser

    device: LoanDetailDevice

    model_config = {
        "from_attributes": True
    }