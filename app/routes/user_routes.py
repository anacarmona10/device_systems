from fastapi import APIRouter, HTTPException, Query, Response, Depends
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum
from typing import Optional
from app.services.user_service import (
    obtener_todos_los_usuarios,
    crear_nuevo_usuario,
    actualizar_usuario_completo,
    actualizar_usuario_parcial,
    eliminar_usuario,
    correo_existe
)
from app.schemas.user_schema import UserUpdate


from app.dependencies.user_dependencies import (
    get_user_or_404,
    validar_email_unico
)

router = APIRouter()

from app.data.users_db import usuarios_db

def agregar_cabeceras(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"


# GET de todos
@router.get("/users", response_model=list[UserResponse])
def listar_usuarios(
    response: Response,
    role: Optional[RoleEnum]=Query(None),
    is_active: Optional[bool]=Query(None)
):

    agregar_cabeceras(response)

    return obtener_todos_los_usuarios(
        role,
        is_active
    )

# GET /users/{user_id} — por ID
@router.get("/users/{user_id}", response_model=UserResponse)

def obtener_usuario(
    response: Response,
    usuario=Depends(get_user_or_404)
):

    agregar_cabeceras(response)

    return usuario


# post
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)

def crear_usuario(
    usuario: UserCreate,
    response: Response
):

    agregar_cabeceras(response)

    validar_email_unico(usuario.email)

    return crear_nuevo_usuario(usuario)


@router.put("/users/{user_id}", response_model=UserResponse)
def actualizar_usuario(
    user_id: int,
    usuario: UserCreate,
    response: Response
):

    agregar_cabeceras(response)

    usuario_existente = get_user_or_404(user_id)

    for u in usuarios_db:
        if (
            u["email"] == usuario.email
            and u["id"] != user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    return actualizar_usuario_completo(
        user_id,
        usuario
    )



@router.patch("/users/{user_id}", response_model=UserResponse)
def actualizar_usuario_parcialmente(
    user_id: int,
    usuario: UserUpdate,
    response: Response
):

    agregar_cabeceras(response)

    get_user_or_404(user_id)

    datos = usuario.model_dump(exclude_unset=True)

    if not datos:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    if "email" in datos:

        for u in usuarios_db:

            if (
                u["email"] == datos["email"]
                and u["id"] != user_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="El correo ya está registrado"
                )

    return actualizar_usuario_parcial(
        user_id,
        datos
    )



@router.delete("/users/{user_id}")
def eliminar_usuario_endpoint(
    user_id: int,
    response: Response
):

    agregar_cabeceras(response)

    get_user_or_404(user_id)

    eliminar_usuario(user_id)

    return {
        "message": "Usuario eliminado correctamente"
    }