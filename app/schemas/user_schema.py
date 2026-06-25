from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional

# Roles permitidos
class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# Modelo de entrada (para crear un usuario)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr
    role: RoleEnum
    is_active: bool

# Esto es para la actualización de usuarios para que todos los campos no sean obligatorios en ese caso 
class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


# Modelo de respuesta (lo que la API devuelve)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}

