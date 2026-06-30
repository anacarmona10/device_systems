from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    field_validator
)

import re


class UserRegister(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre del usuario"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña segura"
    )

    role: str = Field(
        ...,
        description="Rol del usuario"
    )


    @field_validator("password")
    @classmethod
    def validar_password(cls, value):

        if " " in value:
            raise ValueError(
                "La contraseña no puede contener espacios"
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Debe contener una mayúscula"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Debe contener una minúscula"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Debe contener un número"
            )

        return value


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class Token(BaseModel):

    access_token: str

    token_type: str

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenData(BaseModel):

    email: EmailStr | None = None

    model_config = ConfigDict(
        from_attributes=True
    )