from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class DeviceTypeEnum(str, Enum):
    laptop = "laptop"
    tablet = "tablet"
    proyector = "proyector"
    camara = "camara"
    router = "router"
    monitor = "monitor"


class DeviceCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del dispositivo"
    )

    serial_number: str = Field(
        ...,
        min_length=3,
        description="Número de serie"
    )

    device_type: DeviceTypeEnum

    brand: Optional[str] = None

    is_available: bool = True


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=3
    )

    serial_number: Optional[str] = None

    device_type: Optional[DeviceTypeEnum] = None

    brand: Optional[str] = None

    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: DeviceTypeEnum
    brand: Optional[str]
    is_available: bool

    model_config = {
        "from_attributes": True
    }